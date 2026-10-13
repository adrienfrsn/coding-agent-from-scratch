# Agent de code local

Un agent de code construit from scratch en Python, conçu pour tourner **entièrement en local** avec un modèle open source via [Ollama](https://ollama.com). Aucune ligne de code ne quitte la machine.

Ce projet est avant tout un projet d'apprentissage pour comprendre de l'intérieur comment fonctionnent les agents de code comme Claude Code ou OpenCode, en les reconstruisant étape par étape.

## Pourquoi un agent local ?

La plupart des agents de code sont pensés pour de gros modèles cloud. Un modèle local impose des contraintes différentes, qui en font un problème d'ingénierie intéressant :

- **un contexte plus petit**, où chaque token compte
- **des appels d'outils moins fiables**, qu'il faut rendre robustes
- **un raisonnement plus limité**, qui demande des outils simples et bien décrits
- **une vitesse plus faible**, où chaque tour de boucle inutile se ressent

En contrepartie la confidentialité est totale et le coût d'utilisation est nul.

## Fonctionnement

Le cœur de l'agent est une boucle :

```
messages = [prompt système, demande de l'utilisateur]
tant que vrai :
    réponse = llm(messages, outils disponibles)
    si la réponse ne contient aucun appel d'outil : afficher et arrêter
    pour chaque appel d'outil :
        résultat = exécuter(outil, arguments)
        ajouter le résultat aux messages
```

Le modèle ne fait que **choisir** quel outil appeler, à partir de leur nom et de leur description. C'est le code de l'agent qui **exécute**, et c'est donc là que se jouent la fiabilité et la sécurité.

## Outils disponibles

| Outil | Rôle |
|---|---|
| `read_file` | Lire le contenu d'un fichier |
| `write_file` | Créer ou réécrire un fichier |
| `edit_file` | Remplacer une chaîne exacte et unique dans un fichier |
| `list_files` | Lister le contenu d'un dossier |
| `run_command` | Exécuter une commande shell, après confirmation |

`edit_file` remplace une chaîne précise plutôt que de réécrire le fichier entier : c'est plus rapide, beaucoup moins coûteux en contexte, et évite que le modèle modifie par erreur le reste du fichier. La modification est refusée si la chaîne est introuvable ou présente plusieurs fois, pour ne jamais éditer le mauvais endroit.

## Sécurité

La sécurité est construite en plusieurs couches, chacune couvrant ce que les autres ne couvrent pas :

- **Confirmation des commandes** : chaque commande shell est affichée et doit être validée explicitement. Le refus est le comportement par défaut.
- **Timeout** : une commande qui dépasse 60 secondes est interrompue.
- **Sorties tronquées** : seule la fin de la sortie d'une commande est renvoyée au modèle, pour ne pas saturer son contexte.
- **Erreurs renvoyées au modèle** : un outil qui échoue ne fait pas planter l'agent, il renvoie l'erreur pour que le modèle puisse se corriger.

### Un exemple concret

Demander à l'agent de lire `~/.zshrc` donne ceci :

```
> lis le contenu du fichier ~/.zshrc
🔧 read_file({'path': '~/.zshrc'})
🔧 run_command({'command': 'cat ~/.zshrc'})

$ cat ~/.zshrc
Exécuter ? [o/N]
```

Bloqué par `read_file`, le modèle a immédiatement tenté de contourner l'obstacle avec une commande shell. Il n'est pas malveillant, il cherche simplement à accomplir la demande. C'est la confirmation qui l'a arrêté.

Ce test illustre pourquoi une protection dans un seul outil ne suffit jamais, et pourquoi une consigne dans le prompt n'est pas une protection. La sécurité d'un agent doit être garantie par le code.

## Installation

Prérequis : Python 3.12, Ollama, et une machine capable de faire tourner le modèle choisi (environ 20 Go de mémoire pour un modèle de 27B). Le projet est développé et testé sur un MacBook Pro M2 Max 64 Go. Sur Linux ou Windows, utiliser une variante GGUF du modèle plutôt que la variante MLX.

Télécharger un modèle (ici Qwen mais n'importe quel modèle compatible avec l'appel d'outils fonctionne) :

```bash
ollama pull qwen3.8:27b-mlx
```

Créer un fichier `Modelfile` pour augmenter la fenêtre de contexte :

```
FROM qwen3.8:27b-mlx
PARAMETER num_ctx 32768
```

Puis créer la variante du modèle et l'environnement Python :

```bash
ollama create qwen-coder -f Modelfile
python -m venv .venv
source .venv/bin/activate
pip install openai
```

La fenêtre de contexte est essentielle : avec la valeur par défaut d'Ollama, les définitions d'outils et quelques lectures de fichiers suffisent à la dépasser, et le début de la conversation est tronqué silencieusement.

## Utilisation

```bash
python agent.py
```

```
> crée un hello world en Java, compile-le et lance-le
```

L'agent utilise l'API compatible OpenAI d'Ollama, il fonctionne aussi avec LM Studio ou tout autre serveur compatible, en changeant simplement l'URL et le nom du modèle.
