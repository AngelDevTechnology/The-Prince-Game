# The Prince Game

**The Prince Game** est un projet de jeu vidéo développé en Python. Il explore un univers de stratégie et de gestion dans lequel les personnages, les relations et les intrigues politiques ont vocation à jouer un rôle central.

Le projet est actuellement en cours de développement. Son architecture, ses mécaniques et son contenu sont encore amenés à évoluer.

---

## État du projet

Le développement se poursuivra au cours du **deuxième et du troisième trimestre**.

À ce stade :

- L'application est encore rudimentaire et constitue une première version du jeu.
- Les rôles et les différentes fonctions des personnages ne sont pas encore définis.
- Les mécaniques de jeu sont incomplètes et susceptibles de changer.
- De nouvelles fonctionnalités et améliorations seront progressivement intégrées.

Ce projet ne constitue donc pas une version finale ou une expérience de jeu complète.

---

## Prérequis

Avant de lancer le projet, assurez-vous de disposer des éléments suivants :

- **Python 3.12.8** — version requise.
- **GCC** et les outils de compilation nécessaires.
- **UV** (facultatif), si vous souhaitez utiliser le gestionnaire d'environnement et de dépendances UV.

La compilation de l'extension Cython nécessite un compilateur C compatible avec votre environnement.

Sur Debian / Ubuntu, vous pouvez installer les outils nécessaires avec :

```bash
sudo apt update
sudo apt install build-essential
```

---

## Installation

Deux méthodes d'installation sont disponibles. Vous pouvez utiliser UV ou l'environnement virtuel Python classique.

### Méthode 1 — Avec UV

Installez Python 3.12.8 si nécessaire :

```bash
uv python install 3.12.8
```

Créez l'environnement virtuel :

```bash
uv venv --python 3.12.8
```

Activez-le :

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows — PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

Installez les dépendances :

```bash
uv pip install -r requirements.txt
```

### Méthode 2 — Avec Python classique

Vérifiez que Python 3.12.8 est installé :

```bash
python --version
```

Créez l'environnement virtuel :

```bash
python -m venv .venv
```

Activez-le :

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows — PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

Mettez pip à jour et installez les dépendances :

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Compilation de l'extension Cython

Le projet utilise Cython pour compiler certaines parties du code en extensions natives.

La compilation doit être réalisée depuis la racine du projet, avec le même environnement Python que celui utilisé pour lancer le jeu.

**Avec UV :**

```bash
uv run --active python setup.py build_ext --inplace
```

**Avec Python classique :**

```bash
python setup.py build_ext --inplace
```

Cette étape doit être effectuée après l'installation des dépendances.

---

## Lancement du jeu

Une fois les dépendances installées et l'extension compilée, vous pouvez lancer l'application.

**Avec UV :**

```bash
uv run --active python main.py
```

**Avec Python classique :**

```bash
python main.py
```

---

## Qualité et formatage du code

Le projet utilise **Ruff** pour l'analyse statique, la vérification des conventions et le formatage du code Python.

Vérifier les éventuels problèmes :

```bash
ruff check .
```

Corriger automatiquement les problèmes détectés lorsque possible :

```bash
ruff check --fix .
```

Vérifier le formatage :

```bash
ruff format --check .
```

Appliquer le formatage :

```bash
ruff format .
```

Si Ruff n'est pas installé dans l'environnement :

```bash
uv pip install ruff
```

Ou avec Python classique :

```bash
python -m pip install ruff
```

---

## Technologies utilisées

Le projet s'appuie notamment sur les technologies suivantes :

- **Python** — langage principal.
- **Cython** — compilation de certaines parties du code.
- **NumPy** — calcul numérique et manipulation de données.
- **OpenGL** — rendu graphique.
- **GLFW** — gestion de la fenêtre et des événements.
- **Dear ImGui** — interface utilisateur et outils d'interface.
- **SQLite** — stockage des données du jeu.
- **Ruff** — analyse et formatage du code.
- **UV** — gestion de l'environnement et des dépendances (facultatif).

---

## Auteurs

**Elie CADUSSEAU**  
**Angel LAPEYRE**

---

*The Prince Game — Projet en cours de développement.*