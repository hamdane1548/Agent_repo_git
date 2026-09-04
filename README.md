<div align="center">

# 🤖 AI Git Agent

### Intelligent GitHub Repository Analysis & AI-Powered Developer Agents

**Analyze · Understand · Reason · Automate**

An agentic AI system designed to analyze GitHub repositories,
understand project requirements, and orchestrate specialized AI agents
to assist developers.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Agents-1C3C3C?logo=langchain)](https://www.langchain.com/)
[![Kafka](https://img.shields.io/badge/Apache%20Kafka-Event%20Driven-231F20?logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Integration-181717?logo=github&logoColor=white)](https://github.com/)

</div>
<img width="1957" height="994" alt="image" src="https://github.com/user-attachments/assets/4e66bc2b-85ea-4f16-819e-6ded2582513c" />
# 🤖 AI Git Agent

> **AI-powered GitHub Repository Analysis & Job Matching Agent**

AI Git Agent est une application basée sur l’**Intelligence Artificielle Agentique** permettant d’analyser automatiquement des dépôts GitHub et d’évaluer leur pertinence par rapport à une **offre d’emploi** donnée.

L’objectif du projet est d’automatiser une partie du processus d’analyse technique en utilisant des **LLM, des agents intelligents et une architecture distribuée basée sur Kafka**.

---

## 📌 Fonctionnalités

* 🔎 Analyse automatique de dépôts GitHub
* 📂 Extraction des informations importantes des repositories
* 🧠 Analyse du contenu du projet avec un LLM
* 💼 Comparaison entre un profil / CV et une Job Description
* 🛠️ Analyse des technologies utilisées dans le repository
* 🤖 Utilisation d'agents IA spécialisés
* ⚡ Traitement parallèle des repositories
* 📡 Communication asynchrone avec Apache Kafka
* 🆔 Utilisation d'un `request_id` pour suivre chaque traitement
* 📊 Génération d'un résultat final basé sur les différentes analyses

---

# 🏗️ Architecture globale

L'application est organisée autour d'un **pipeline d'agents IA** permettant de décomposer le traitement en plusieurs étapes indépendantes.

```text
                         ┌──────────────────────┐
                         │       Client         │
                         │  Profile + Job Desc  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI / CLI   │
                         │    Main Controller   │
                         └──────────┬───────────┘
                                    │
                              request_id
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Pipeline Manager   │
                         └──────────┬───────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
             ┌──────────┐    ┌──────────┐    ┌──────────┐
             │ GitHub   │    │ Profile  │    │   Job    │
             │  Agent   │    │  Agent   │    │  Agent   │
             └────┬─────┘    └────┬─────┘    └────┬─────┘
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Kafka       │
                         │ Event / Message  │
                         │     Broker       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Analysis Agents  │
                         │   / Workers      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Result Aggregator│
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Final Evaluation │
                         └──────────────────┘
```

---

## 🔄 Fonctionnement

Le traitement commence par une requête contenant les informations nécessaires à l'analyse :

```text
Profile
   +
Job Description
   +
GitHub Repositories
   +
Tech Stack
```

Un `request_id` unique est ensuite généré afin d'identifier l'ensemble du traitement.

Le pipeline exécute ensuite différentes étapes :

### 1. Repository Collection

L'agent récupère les informations des repositories GitHub :

* nom
* description
* langage
* technologies
* structure du projet
* fichiers importants
* README
* dépendances

### 2. Repository Analysis

Les informations récupérées sont envoyées à des agents spécialisés utilisant un LLM afin d'analyser le repository.

L'agent peut notamment déterminer :

* les technologies réellement utilisées ;
* la complexité du projet ;
* les compétences démontrées ;
* les pratiques de développement ;
* la pertinence du projet par rapport au poste.

### 3. Profile Analysis

Le profil du candidat est analysé afin d'identifier :

* compétences techniques ;
* expériences ;
* technologies maîtrisées ;
* projets réalisés.

### 4. Job Description Analysis

La Job Description est transformée en ensemble de critères techniques et fonctionnels.

Exemple :

```text
Job Description
       │
       ▼
┌────────────────────┐
│ Required Skills    │
├────────────────────┤
│ Python             │
│ Docker             │
│ Kafka              │
│ LangChain          │
│ AWS                │
└────────────────────┘
```

### 5. Matching

Les informations du profil, des repositories et de la Job Description sont finalement comparées.

```text
Candidate Profile
        │
        ├──────────────┐
        │              │
        ▼              ▼
Repositories      Job Description
        │              │
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │ AI Matching  │
        │    Agent     │
        └──────┬───────┘
               ▼
        Compatibility Score
```

---

# ⚡ Évolution de l'architecture

Le projet a évolué progressivement afin d'améliorer ses performances et sa scalabilité.

### Version 1 — Single Thread

Initialement, le pipeline exécutait les différentes étapes de manière séquentielle.

```text
Request
   │
   ▼
Step 1
   │
   ▼
Step 2
   │
   ▼
Step 3
   │
   ▼
Step 4
   │
   ▼
Result
```

Cette architecture était simple mais présentait un problème important : **chaque étape devait attendre la fin de l'étape précédente**.

---

### Version 2 — Multithreading

Le traitement a ensuite été amélioré grâce au parallélisme.

```text
                 Request
                    │
                    ▼
              Pipeline Manager
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Thread 1  Thread 2  Thread 3
          │         │         │
       Agent A   Agent B   Agent C
          │         │         │
          └─────────┼─────────┘
                    ▼
                 Result
```

Cette approche permet d'exécuter plusieurs tâches indépendantes simultanément.

Cependant, elle présente certaines limites :

* gestion plus complexe des threads ;
* communication limitée entre processus ;
* difficulté à scaler horizontalement ;
* risque de blocage ;
* couplage plus important entre les composants.

---

### Version 3 — Architecture distribuée avec Kafka

Pour améliorer la scalabilité et découpler les composants, **Apache Kafka** a été introduit.

```text
                 ┌───────────────┐
                 │    Request    │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    Producer   │
                 └───────┬───────┘
                         │
                         ▼
                 ╔═══════════════╗
                 ║     Kafka     ║
                 ║    Topics     ║
                 ╚═══════╤═══════╝
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         ┌────────┐ ┌────────┐ ┌────────┐
         │Worker 1│ │Worker 2│ │Worker 3│
         │ Agent  │ │ Agent  │ │ Agent  │
         └───┬────┘ └───┬────┘ └───┬────┘
             │          │          │
             └──────────┼──────────┘
                        ▼
                 ┌──────────────┐
                 │    Result    │
                 │   Consumer   │
                 └──────────────┘
```

Kafka permet notamment :

* de découpler les producteurs et les consommateurs ;
* de traiter plusieurs requêtes simultanément ;
* de distribuer les tâches entre plusieurs workers ;
* d'améliorer la résilience du système ;
* de faciliter le scaling horizontal.

---

# 🧩 Architecture des composants

Le projet est composé de plusieurs composants spécialisés.

```text
AI Git Agent
│
├── API / CLI
│
├── Pipeline
│   ├── Repository Pipeline
│   ├── Profile Pipeline
│   └── Job Analysis Pipeline
│
├── AI Agents
│   ├── GitHub Agent
│   ├── Repository Analysis Agent
│   ├── Profile Agent
│   ├── Job Description Agent
│   └── Matching Agent
│
├── Messaging
│   └── Apache Kafka
│
├── LLM Layer
│   └── Mistral
│
└── Infrastructure
    ├── Docker
    └── PostgreSQL / MongoDB / Qdrant
```

---

# 📨 Communication avec Kafka

Chaque traitement est associé à un identifiant unique :

```text
request_id = UUID
```

Cet identifiant permet de suivre une requête à travers les différents services.

Exemple :

```json
{
  "request_id": "8f2c1b7e-...",
  "repository": "github.com/user/project",
  "profile": "...",
  "job_description": "..."
}
```

Les workers consomment ensuite les messages depuis les topics Kafka correspondants.

Le résultat contient également le `request_id` :

```json
{
  "request_id": "8f2c1b7e-...",
  "status": "completed",
  "score": 87,
  "analysis": "..."
}
```

Le consumer peut ainsi attendre uniquement la réponse correspondant à la requête demandée.

---

# 🛠️ Technologies utilisées

| Technologie     | Utilisation                 |
| --------------- | --------------------------- |
| 🐍 Python       | Langage principal           |
| 🤖 LangChain    | Orchestration des agents IA |
| 🧠 Mistral      | Large Language Model        |
| 📨 Apache Kafka | Communication asynchrone    |
| 🐳 Docker       | Conteneurisation            |
| 🚀 FastAPI      | API backend                 |
| 🐙 GitHub API   | Accès aux repositories      |
| 🗄️ PostgreSQL  | Stockage des données        |
| 🔎 Qdrant       | Vector Database             |
| 📦 Pydantic     | Validation des données      |
| 📝 Loguru       | Logging                     |

---

# 📁 Structure du projet

```text
ai-git-agent/
│
├── app/
│   ├── agents/
│   │   ├── github_agent/
│   │   ├── profile_agent/
│   │   ├── job_agent/
│   │   └── matching_agent/
│   │
│   ├── pipeline/
│   │   ├── pipeline.py
│   │   └── steps/
│   │
│   ├── kafka/
│   │   ├── producer.py
│   │   ├── consumer.py
│   │   └── topics.py
│   │
│   ├── models/
│   ├── services/
│   ├── config/
│   └── utils/
│
├── tests/
│
├── docker/
│
├── docker-compose.yml
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/<username>/ai-git-agent.git
cd ai-git-agent
```

### 2. Créer l'environnement Python

```bash
python -m venv .venv
```

Linux/macOS :

```bash
source .venv/bin/activate
```

Windows :

```bash
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créer un fichier `.env` :

```env
MISTRAL_API_KEY=your_api_key
GITHUB_TOKEN=your_github_token

KAFKA_BOOTSTRAP_SERVERS=localhost:9092

DATABASE_URL=your_database_url
```

---

# 🐳 Lancer l'infrastructure

Les services nécessaires peuvent être lancés avec Docker Compose :

```bash
docker compose up -d
```

Vérifier les containers :

```bash
docker compose ps
```

Arrêter les services :

```bash
docker compose down
```

---

# ▶️ Exécution

Le pipeline peut être lancé avec :

```bash
python main.py
```

Les paramètres peuvent contenir :

```text
Profile
Job Description
Repositories
Tech Stack
```

Exemple conceptuel :

```bash
python main.py \
    --profile profile.json \
    --job job_description.txt \
    --repositories repositories.json
```

---

# 🔬 Exemple de workflow

```text
User Request
     │
     ▼
Generate request_id
     │
     ▼
Retrieve GitHub repositories
     │
     ▼
Analyze repositories
     │
     ▼
Analyze candidate profile
     │
     ▼
Analyze Job Description
     │
     ▼
Kafka Events
     │
     ▼
Parallel AI Workers
     │
     ▼
Aggregate results
     │
     ▼
AI Matching
     │
     ▼
Final Report
```

---

# 🎯 Objectifs du projet

Les principaux objectifs sont :

* automatiser l'analyse des compétences techniques ;
* exploiter les repositories GitHub comme source d'information ;
* utiliser des agents IA spécialisés ;
* réduire le temps nécessaire à l'évaluation d'un profil ;
* permettre le traitement parallèle de plusieurs tâches ;
* construire une architecture distribuée et scalable.

---

# 🔮 Perspectives

Plusieurs améliorations peuvent être envisagées :

* ajout de davantage d'agents spécialisés ;
* amélioration du système de scoring ;
* intégration de plusieurs LLM ;
* ajout d'un système de mémoire pour les agents ;
* monitoring avec Prometheus et Grafana ;
* orchestration avec Kubernetes ;
* amélioration de la gestion des erreurs Kafka ;
* mise en place d'un système de retry et dead-letter topics ;
* ajout d'une interface web pour visualiser les analyses.

---

# 👨‍💻 Projet

**AI Git Agent**

Projet académique / expérimental autour de l'**Agentic AI**, des **LLM** et des architectures distribuées.

### Concepts clés

`Agentic AI` · `LLM` · `LangChain` · `Kafka` · `Python` · `GitHub` · `FastAPI` · `Docker` · `RAG` · `Vector Database`
