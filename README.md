# atelier-camunda

> Atelier pratique **Camunda 8** — BPMN 2.0, DMN, Service Tasks, Human Tasks et AI Agents. Self-hosted Docker.

## Demarrage rapide

```bash
git clone https://github.com/opinaka-attik/atelier-camunda
cd atelier-camunda/docker
docker compose up -d
```

| Interface  | URL                   | Role                      |
|------------|-----------------------|---------------------------|
| Operate    | http://localhost:8081 | Monitoring instances BPMN |
| Tasklist   | http://localhost:8082 | Human Tasks               |
| Zeebe gRPC | localhost:26500       | Workers Python            |

> Login Operate/Tasklist : **demo / demo**

## Modules

| # | Processus BPMN                  | Worker Python               | Concepts                        |
|---|----------------------------------|-----------------------------|---------------------------------|
| 01 | `01_hello_process.bpmn`         | `worker_01_hello.py`        | Deploy, Instance, Service Task  |
| 02 | `02_service_task.bpmn`          | `worker_02_04_services.py`  | IoMapping, variables, chaining  |
| 03 | `03_gateway_condition.bpmn`     | `worker_02_04_services.py`  | Gateway XOR, conditions FEEL    |
| 04 | `04_human_task.bpmn`            | `worker_02_04_services.py`  | User Task, Tasklist, approbation|
| 05 | `05_ai_agent_process.bpmn`      | `worker_05_ai_agent.py`     | AI Groq, Human-in-the-loop      |

## Structure

```
atelier-camunda/
├── processes/          ← 5 processus BPMN 2.0
├── workers/            ← 3 workers Python (pyzeebe)
├── docs/               ← 5 fichiers documentation
│   ├── 00_installation.md
│   ├── 01_interface_camunda.md
│   ├── 02_concepts_cles.md
│   ├── 03_guide_modules.md
│   └── 04_depannage.md
└── docker/
    └── docker-compose.yml  ← Zeebe + Operate + Tasklist + Elasticsearch
```

## Prerequis

```bash
# Python
pip install pyzeebe requests

# Groq (module 05)
export GROQ_API_KEY=sk-xxxxxxxxxxxx

# zbctl (CLI optionnel)
curl -LO https://github.com/camunda/zeebe/releases/latest/download/zbctl.linux
chmod +x zbctl.linux && sudo mv zbctl.linux /usr/local/bin/zbctl
```

## Collection des ateliers

| Atelier | Port | Categorie |
|---------|------|-----------|
| [atelier-dify](https://github.com/opinaka-attik/atelier-dify) | 3000 | AI Apps |
| [atelier-langflow](https://github.com/opinaka-attik/atelier-langflow) | 7860 | AI Agents |
| [atelier-flowise](https://github.com/opinaka-attik/atelier-flowise) | 3001 | RAG/Chatbots |
| [atelier-n8n](https://github.com/opinaka-attik/atelier-n8n) | 5678 | Automatisation |
| [atelier-activepieces](https://github.com/opinaka-attik/atelier-activepieces) | 8080 | Automatisation |
| [atelier-budibase](https://github.com/opinaka-attik/atelier-budibase) | 10000 | Internal Tools |
| [atelier-maxun](https://github.com/opinaka-attik/atelier-maxun) | 5173 | Scraping |
| [atelier-dataiku](https://github.com/opinaka-attik/atelier-dataiku) | 10000 | Data Engineering |
| **atelier-camunda** | **8081/8082** | **BPM / Workflow Engine** |
