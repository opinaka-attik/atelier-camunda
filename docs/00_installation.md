# 00 - Installation Camunda 8

## Prerequis
- Docker & Docker Compose
- Python 3.10+ (pour les workers)
- 4 Go RAM minimum (Elasticsearch est gourmand)
- Cle API Groq (module 05) : https://console.groq.com

## Demarrage rapide

```bash
git clone https://github.com/opinaka-attik/atelier-camunda
cd atelier-camunda/docker
docker compose up -d
```

## Verification

```bash
docker compose ps
# zeebe       Up   26500/tcp, 9600/tcp
# operate     Up   0.0.0.0:8081->8080/tcp
# tasklist    Up   0.0.0.0:8082->8080/tcp
# elasticsearch Up 0.0.0.0:9200->9200/tcp
```

## Interfaces web

| Service       | URL                        | Role                          |
|---------------|----------------------------|-------------------------------|
| Operate       | http://localhost:8081      | Monitoring instances BPMN     |
| Tasklist      | http://localhost:8082      | Gestion Human Tasks           |
| Elasticsearch | http://localhost:9200      | Stockage donnees Zeebe        |
| Zeebe gRPC    | localhost:26500            | API workers Python            |

> Identifiants par defaut Operate/Tasklist : **demo / demo**

## Installation workers Python

```bash
cd atelier-camunda
pip install pyzeebe requests

# Configurer la cle Groq (module 05)
export GROQ_API_KEY=sk-xxxxxxxxxxxx
```

## Deployer un processus

1. Ouvrir **Camunda Modeler** (https://camunda.com/download/modeler/)
2. File > Open > selectionner un fichier `processes/*.bpmn`
3. Cliquer **Deploy** (icone rocket) > Target : `localhost:26500`
4. Ou via CLI zbctl :
```bash
zbctl deploy processes/01_hello_process.bpmn --address localhost:26500 --insecure
```

## Arreter

```bash
docker compose down
# Supprimer les donnees
docker compose down -v
```
