# Local coding agent

A coding agent built from scratch in Python, designed to run **entirely locally** with an open-source model via [Ollama](https://ollama.com). Not a single line of code leaves your machine.

This is first and foremost a learning project, to understand from the inside how coding agents like Claude Code or OpenCode work, by rebuilding them step by step.

## Why a local agent?

Most coding agents are designed for large cloud models. A local model imposes different constraints, which make it an interesting engineering problem:

- **a smaller context**, where every token counts
- **less reliable tool calls**, which must be made robust
- **more limited reasoning**, which calls for simple, well-described tools
- **lower speed**, where every unnecessary loop iteration is felt

In return, privacy is total and the cost of use is zero.

## How it works

The core of the agent is a loop:

```
messages = [system prompt, user request]
while true:
    response = llm(messages, available tools)
    if the response contains no tool call: print it and stop
    for each tool call:
        result = execute(tool, arguments)
        append the result to messages
```

The model only **chooses** which tool to call, based on their name and description. It is the agent's code that **executes**, and that is therefore where reliability and security are decided.

## Available tools

| Tool | Purpose |
|---|---|
| `read_file` | Read the content of a file |
| `write_file` | Create or rewrite a file |
| `edit_file` | Replace an exact, unique string in a file |
| `list_files` | List the content of a directory |
| `run_command` | Run a shell command, after confirmation |

`edit_file` replaces a specific string rather than rewriting the whole file: it is faster, much cheaper in context, and prevents the model from accidentally changing the rest of the file. The edit is rejected if the string is not found or appears several times, so the wrong place is never edited.

## Security

Security is built in several layers, each covering what the others do not:

- **Command confirmation**: every shell command is displayed and must be explicitly approved. Refusal is the default behavior.
- **Timeout**: a command that runs longer than 60 seconds is interrupted.
- **Truncated output**: only the end of a command's output is returned to the model, so as not to saturate its context.
- **Errors returned to the model**: a tool that fails does not crash the agent, it returns the error so the model can correct itself.

### A concrete example

Asking the agent to read `~/.zshrc` gives this:

```
> read the content of the file ~/.zshrc
🔧 read_file({'path': '~/.zshrc'})
🔧 run_command({'command': 'cat ~/.zshrc'})

$ cat ~/.zshrc
Run? [y/N]
```

Blocked by `read_file`, the model immediately tried to work around the obstacle with a shell command. It is not malicious, it is simply trying to fulfill the request. It was the confirmation that stopped it.

This test illustrates why protection in a single tool is never enough, and why an instruction in the prompt is not a protection. An agent's security must be guaranteed by the code.

## Installation

Prerequisites: Python 3.12, Ollama, and a machine able to run the chosen model (about 20 GB of memory for a 27B model). The project is developed and tested on a MacBook Pro M2 Max 64 GB. On Linux or Windows, use a GGUF variant of the model rather than the MLX variant.

Download a model (Qwen here, but any model that supports tool calling works):

```bash
ollama pull qwen3.8:27b-mlx
```

Create a `Modelfile` to increase the context window:

```
FROM qwen3.8:27b-mlx
PARAMETER num_ctx 32768
```

Then create the model variant and the Python environment:

```bash
ollama create qwen-coder -f Modelfile
python -m venv .venv
source .venv/bin/activate
pip install openai
```

The context window is essential: with Ollama's default value, the tool definitions and a few file reads are enough to exceed it, and the beginning of the conversation is silently truncated.

## Usage

```bash
python agent.py
```

```
> create a Java hello world, compile it and run it
```

The agent uses Ollama's OpenAI-compatible API, so it also works with LM Studio or any other compatible server, by simply changing the URL and the model name.


## Evaluation

`eval.py` measures the agent's reliability. Each folder in `tasks/` contains a `repo/` (the starting project) and a `task.json` (`prompt`, `check`, `protected`). For each task, the runner copies the project into a temporary folder, runs `agent.py --task "..." --yes` (3 attempts, since the agent is not deterministic), restores the `protected` files (the original tests), then runs the `check` command itself. It never trusts the agent when it claims to have succeeded.

The 13 tasks cover: simple bugs (bounds, empty list, `None`, operator, pagination), a bug spanning two files, features to add, refactoring, Java, and a 300-line file.

`--yes` removes the `run_command` confirmation: only use it in a container.

```bash
docker run --rm -it -v "$PWD":/app -w /app \
  -e OLLAMA_URL=http://host.docker.internal:11434/v1 python:3.12 bash
pip install openai pytest
python eval.py
```

The Java tasks require `javac` in the container (`apt-get install -y default-jdk-headless`).

Reference score:
- Qwen 3.8 27b: 90%
- Qwen 2.5 7b: 15%
