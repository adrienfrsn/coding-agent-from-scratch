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

## Context management

With a local model the context window is small, and a single large file or a verbose test run can fill it. The agent handles this in three steps:

- **Measure**: every turn prints the context size, taken from the `usage` field of the response: `[step 3] context: 5120 / 32768 tokens (16%)`.
- **Limit**: `read_file` returns at most 300 lines, and `run_command` / `list_files` keep the last 200 lines, where errors and test summaries are. The truncation is always explicit (`[truncated, lines 1-300 out of 1200, call read_file with offset=301 to read the rest]`), so the model knows that something is missing and how to get it.
- **Compact**: when the context goes over 75% of the limit, the agent asks the model to summarize the work done so far (goal, files, changes, test results, what remains), then restarts from the system prompt, the original request and that summary.

The limit is set by `CONTEXT_LIMIT` (default `32768`) and must match the model's `num_ctx`.

## Project instructions (AGENTS.md)

If an `AGENTS.md` file exists in the working directory, its content is appended to the system prompt (it is re-read on each request and kept after compaction). Use it to describe the project: layout, how to run the tests, conventions. Set `AGENTS_MD=0` to ignore it, e.g. to compare success rates with and without it in `eval.py`.

## Security

Security is built in several layers, each covering what the others do not:

- **Command confirmation**: every shell command is displayed and must be explicitly approved. Refusal is the default behavior.
- **Timeout**: a command that runs longer than 60 seconds is interrupted.
- **Working directory sandbox**: file tools resolve every path and refuse anything outside the directory the agent was started in.
- **Truncated output**: only the end of a command's output is returned to the model, so as not to saturate its context (see [Context management](#context-management)).
- **Errors returned to the model**: a tool that fails does not crash the agent, it returns the error so the model can correct itself.

### A concrete example

Asking the agent to read `~/.zshrc` gives this:

```
> read the content of the file ~/.zshrc
[tool] read_file({'path': '~/.zshrc'})
[tool] run_command({'command': 'cat ~/.zshrc'})

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
pip install -r requirements.txt
```

The context window is essential: with Ollama's default value, the tool definitions and a few file reads are enough to exceed it, and the beginning of the conversation is silently truncated.

## Usage

```bash
python agent.py
```

```
> create a Java hello world, compile it and run it
```

The agent uses Ollama's OpenAI-compatible API, so it also works with LM Studio or any other compatible server: set `OLLAMA_URL` (default `http://localhost:11434/v1`) and `MODEL` (default `qwen-coder`).

## Evaluation

`eval.py` measures the agent's reliability. Each folder in `tasks/` contains a `repo/` (the starting project) and a `task.json` (`prompt`, `check`, `protected`), and optionally a `hidden/` folder of tests the agent never sees. For each task, the runner copies the project into a temporary folder, runs `agent.py --task "..." --yes` (3 attempts, since the agent is not deterministic), restores the `protected` files (the original tests), copies the `hidden/` tests into the project, then runs the `check` command itself. It never trusts the agent when it claims to have succeeded.

The 19 tasks are in two groups:

- **Basic** (13): simple bugs (bounds, empty list, `None`, operator, pagination), a bug spanning two files, features to add, refactoring, Java, and a 300-line file.
- **Advanced** (6), closer to real work:
  - `multi-bug-package`: three independent bugs in a package with a separate `tests/` folder
  - `root-cause`: the failing test points at `billing.py`, but the bug is in a shared helper; hidden tests reject a fix of the symptom only
  - `feature-from-spec`: write an arithmetic expression parser from `SPEC.md`; the visible tests are a sample, hidden tests cover the whole spec
  - `rename-api`: rename a function across four files, including a module-qualified call and an aliased import
  - `lru-cache`: two subtle eviction bugs plus a missing `stats()` method
  - `java-multi-file`: two bugs across two Java classes, checked by an executable `Main`

Four advanced tasks ship an `AGENTS.md` describing the project (layout, how to run the tests, never the fix). Run `AGENTS_MD=0 python eval.py` to measure the agent without it.

`--yes` removes the `run_command` confirmation: only use it in a container.

```bash
docker run --rm -it -v "$PWD":/app -w /app \
  -e OLLAMA_URL=http://host.docker.internal:11434/v1 python:3.12 bash
pip install -r requirements.txt
python eval.py
```

The Java tasks require `javac` in the container (`apt-get install -y default-jdk-headless`).
