import argparse
import json
import os
from pathlib import Path
import subprocess
import time

from openai import OpenAI

client = OpenAI(base_url=os.environ.get("OLLAMA_URL", "http://localhost:11434/v1"), api_key="ollama")
MODEL = "qwen2.5:7b"

SYSTEM_PROMPT = (
    "You are an autonomous coding agent. "
    "Method: 1) explore the project with list_files and read_file, "
    "2) run the tests to see what fails, "
    "3) fix with edit_file, always reading the file first, "
    "4) rerun the tests after every change. "
    "Only stop once all tests pass, then summarize what you changed in two sentences. "
    "If access to a file is denied, do not try to work around it."
)

WORKDIR = Path.cwd().resolve()

CONTEXT_LIMIT = int(os.environ.get("CONTEXT_LIMIT", 32768))
COMPACT_THRESHOLD = 0.75
MAX_FILE_LINES = 300
MAX_OUTPUT_LINES = 200

COMPACT_PROMPT = (
    "The context is almost full. Summarize the work done so far so you can continue "
    "from this summary alone: the goal, the files explored and what they contain, "
    "the changes made, the last test results, and what remains to do. "
    "Be concise and factual, keep exact file names and error messages."
)

# tool description in JSON Schema format, it is all the model knows about the tool
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": f"Reads a text file and returns it, at most {MAX_FILE_LINES} lines at a time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path of the file to read",
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Line to start from (1 = first line). Use it to read the rest of a truncated file.",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path of the file to write",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Runs a shell command and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Shell command to run",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists the files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path of the directory to list",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replaces a string in a text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path of the file to edit",
                    },
                    "old": {
                        "type": "string",
                        "description": "String to replace",
                    },
                    "new": {
                        "type": "string",
                        "description": "New string",
                    },
                },
                "required": ["path", "old", "new"],
            },
        },
    },
]

MAX_STEPS = 25
AUTO_YES = False  # --yes: skips the run_command confirmation (container only)


def read_file(path: str, offset: int = 1) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        start = max(offset, 1) - 1
        chunk = lines[start : start + MAX_FILE_LINES]
        content = "\n".join(chunk)
        if start > 0 or start + len(chunk) < len(lines):
            end = start + len(chunk)
            content += (
                f"\n[truncated, lines {start + 1}-{end} out of {len(lines)}"
                + (f", call read_file with offset={end + 1} to read the rest]" if end < len(lines) else "]")
            )
        return content
    except Exception as e:
        # return the error to the model instead of crashing, so it can correct itself
        return f"Error: {e}"


def write_file(path, content) -> str:
    try:
        safe_path(path).parent.mkdir(parents=True, exist_ok=True)
        safe_path(path).write_text(content)
        return "OK"
    except Exception as e:
        return f"Error: {e}"

def run_command(command: str) -> str:
    print(f"\n$ {command}")
    if not AUTO_YES and input("Run? [y/N] ").strip().lower() != "y":
        return "Command rejected by the user"
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        return "Error: the command took longer than 60 seconds"
    output = f"{result.stdout}{result.stderr}"
    return f"return code: {result.returncode}\n{truncate_tail(output)}"


def truncate_tail(text: str) -> str:
    """Keeps the end of a long output, where errors and test summaries are."""
    lines = text.splitlines()
    if len(lines) > MAX_OUTPUT_LINES:
        kept = lines[-MAX_OUTPUT_LINES:]
        text = f"[truncated, last {MAX_OUTPUT_LINES} lines out of {len(lines)}]\n" + "\n".join(kept)
    # safety net for a few huge lines (minified files, binary output...)
    if len(text) > 8000:
        text = "[truncated, last 8000 characters]\n" + text[-8000:]
    return text


def list_files(path: str) -> str:
    try:
        return truncate_tail("\n".join(sorted(os.listdir(safe_path(path)))))
    except Exception as e:
        return f"Error: {e}"

    
def edit_file(path: str, old: str, new: str) -> str:
    try:
        content = safe_path(path).read_text()
        if old not in content:
            return f"Error: the string '{old}' was not found in the file"
        elif content.count(old) > 1:
            return f"Error: the string '{old}' appears several times in the file"
        else:
            content = content.replace(old, new)
            safe_path(path).write_text(content)
            return "OK"
    except Exception as e:
        return f"Error: {e}"


def execute_tool(name: str, arguments: dict) -> str:
    if name == "read_file":
        return read_file(**arguments)
    elif name == "write_file":
        return write_file(**arguments)
    elif name == "run_command":
        return run_command(**arguments)
    elif name == "list_files":
        return list_files(**arguments)
    elif name == "edit_file":
        return edit_file(**arguments)
    else:
        return f"Error: unknown tool '{name}'"


def safe_path(path: str) -> Path:
    resolved = (WORKDIR / path).resolve()
    if not resolved.is_relative_to(WORKDIR):
        raise ValueError(f"access denied, '{path}' is outside the working directory")
    return resolved


def compact(messages: list, user_request: str) -> list:
    print("\n🗜️  Compacting the context...")
    response = client.chat.completions.create(
        model=MODEL, messages=messages + [{"role": "user", "content": COMPACT_PROMPT}]
    )
    summary = response.choices[0].message.content
    print(f"📝 Summary:\n{summary}\n")
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_request},
        {
            "role": "user",
            "content": "Summary of the work done so far (the earlier conversation was "
            f"compacted):\n{summary}\n\nContinue the task from here.",
        },
    ]


def run(user_request: str) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_request},
    ]
    history = []  # to detect repetitions
    start = time.time()

    for step in range(1, MAX_STEPS + 1):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        message = response.choices[0].message
        messages.append(message)

        used = response.usage.total_tokens if response.usage else 0
        print(f"📏 [{step}] context: {used} / {CONTEXT_LIMIT} tokens ({used / CONTEXT_LIMIT:.0%})")

        if not message.tool_calls:
            print(message.content)
            print(f"\nDone in {step} turns, {time.time() - start:.0f} s")
            return

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                result = f"Error: invalid JSON arguments ({e}). Try again with valid JSON."
            else:
                print(f"🔧 {name}({arguments})")
                call = (name, json.dumps(arguments, sort_keys=True))
                if len(history) >= 3 and all(h == call for h in history[-3:]):
                    result = "Error: repetition detected. Change your approach."
                else:
                    history.append(call)
                    result = execute_tool(name, arguments)

            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )
            used += len(result) // 4  # estimate (~4 characters per token)

        if used > COMPACT_THRESHOLD * CONTEXT_LIMIT:
            messages = compact(messages, user_request)

    print(f"\nLimit of {MAX_STEPS} turns reached, task aborted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", help="run a single request then exit")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="run commands without confirmation (container only)",
    )
    args = parser.parse_args()
    AUTO_YES = args.yes

    if args.task:
        run(args.task)
    else:
        while True:
            request = input("\n> ")
            if request.strip() in ("exit", "quit"):
                break
            run(request)
