import json
import os
from pathlib import Path
import subprocess

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3.8:27b-mlx"

SYSTEM_PROMPT = (
    "Tu es un assistant de code. "
    "Utilise les outils à ta disposition pour lire les fichiers avant de répondre."
)

WORKDIR = Path.cwd().resolve()

# description de l'outil au format JSON Schema, c'est tout ce que le modele sait de lui
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lit le contenu d'un fichier texte et le renvoie.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif du fichier à lire",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Ecris du contenu dans un fichier texte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif du fichier à écrire",
                    },
                    "content": {
                        "type": "string",
                        "description": "Contenu à écrire dans le fichier",
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
            "description": "Exécute une commande shell et renvoie le résultat.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Commande shell à exécuter",
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
            "description": "Liste les fichiers dans un répertoire.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif du répertoire à lister",
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
            "description": "Remplace une chaîne de caractères dans un fichier texte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif du fichier à éditer",
                    },
                    "old": {
                        "type": "string",
                        "description": "Chaîne de caractères à remplacer",
                    },
                    "new": {
                        "type": "string",
                        "description": "Nouvelle chaîne de caractères",
                    },
                },
                "required": ["path", "old", "new"],
            },
        },
    },
]


def read_file(path: str) -> str:
    try:
        return safe_path(path).read_text()
    except Exception as e:
        # on renvoie l'erreur au modele plutot que de planter, il pourra se corriger
        return f"Erreur : {e}"


def write_file(path, content) -> str:
    try:
        safe_path(path).parent.mkdir(parents=True, exist_ok=True)
        safe_path(path).write_text(content)
        return "OK"
    except Exception as e:
        return f"Erreur : {e}"

def run_command(command: str) -> str:
    print(f"\n$ {command}")
    if input("Exécuter ? [o/N] ").strip().lower() != "o":
        return "Commande refusée par l'utilisateur"
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        return "Erreur : la commande a dépassé 60 secondes"
    output = f"code de retour : {result.returncode}\n{result.stdout}{result.stderr}"
    return output[-4000:]


def list_files(path: str) -> str:
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Erreur : {e}"

    
def edit_file(path: str, old: str, new: str) -> str:
    try:
        content = safe_path(path).read_text()
        if old not in content:
            return f"Erreur : la chaîne '{old}' n'a pas été trouvée dans le fichier"
        elif content.count(old) > 1:
            return f"Erreur : la chaîne '{old}' apparaît plusieurs fois dans le fichier"
        else:
            content = content.replace(old, new)
            safe_path(path).write_text(content)
            return "OK"
    except Exception as e:
        return f"Erreur : {e}"


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
        return f"Erreur : outil inconnu '{name}'"


def safe_path(path: str) -> Path:
    resolved = (WORKDIR / path).resolve()
    if not resolved.is_relative_to(WORKDIR):
        raise ValueError(f"accès refusé, '{path}' est en dehors du dossier de travail")
    return resolved


def run(user_request: str) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_request},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        message = response.choices[0].message

        # l'historique doit contenir la réponse du modèle, y compris ses appels d'outils
        # sinon il ne pourra pas relier les résultats à ses demandes
        messages.append(message)

        if not message.tool_calls:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            # les arguments arrivent sous forme de texte JSON pas d'objet Python
            arguments = json.loads(tool_call.function.arguments)
            print(f"🔧 {name}({arguments})")

            result = execute_tool(name, arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )


if __name__ == "__main__":
    while True:
        request = input("\n> ")
        if request.strip() in ("exit", "quit"):
            break
        run(request)
