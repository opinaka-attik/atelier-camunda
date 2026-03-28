# 04 - Depannage Camunda 8

## Probleme 1 : Elasticsearch ne demarre pas

**Symptome** : `zeebe` en attente, `operate` ne repond pas

**Cause** : RAM insuffisante ou vm.max_map_count trop bas

**Solution** :
```bash
# Sur Linux/WSL
sudo sysctl -w vm.max_map_count=262144

# Verification
cat /proc/sys/vm/max_map_count

# Verifier logs
docker compose logs elasticsearch | tail -30
```

---

## Probleme 2 : Worker Python - Connexion refusee

**Symptome** :
```
grpc._channel._InactiveRpcError: StatusCode.UNAVAILABLE
failed to connect to all addresses
```

**Solutions** :
```bash
# Verifier que Zeebe tourne
docker compose ps zeebe

# Tester la connexion gRPC
zbctl status --address localhost:26500 --insecure

# Attendre le demarrage complet (60-90 secondes)
docker compose logs zeebe | grep "Broker is ready"
```

---

## Probleme 3 : Processus BPMN deploye mais instances restent ACTIVE

**Symptome** : L'instance ne progresse pas, reste sur un Service Task

**Cause** : Aucun worker ne poll ce type de job

**Solution** :
```bash
# Verifier quel type de job est bloque dans Operate
# Operate > Instance > voir l'element rouge ou en attente

# Verifier que le worker est lance avec le bon task_type
# Ex: si BPMN a type="check-stock", le worker doit avoir
# @worker.task(task_type="check-stock", ...)

# Lancer le bon worker
python workers/worker_02_04_services.py
```

---

## Probleme 4 : INCIDENT dans Operate

**Symptome** : Instance en rouge dans Operate, badge "INCIDENT"

**Solutions** :
```bash
# 1. Cliquer sur l'incident dans Operate pour voir le message d'erreur
# 2. Corriger le worker
# 3. Retenter le job dans Operate : bouton "Retry" sur l'incident
```

**Erreurs frequentes** :
- `Variable not found` : la variable d'input n'existe pas dans l'instance
- `Job timeout` : timeout_ms trop court, augmenter la valeur
- `Worker threw exception` : voir les logs du worker Python

---

## Probleme 5 : Tasklist ne montre pas les taches

**Symptome** : Tasklist vide alors qu'une User Task est en attente

**Solutions** :
1. Verifier que le `assignee` ou `candidateGroups` correspond a votre user
2. Dans le BPMN module 04 : `candidateGroups="managers"` → se connecter comme `demo`
3. Tasklist > **All tasks** (pas "Claimed by me")
4. Actualiser la page (F5)

---

## Probleme 6 : Worker AI - Erreur Groq 401

**Symptome** :
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
```

**Solution** :
```bash
# Verifier la cle
echo $GROQ_API_KEY

# La cle doit commencer par sk-
export GROQ_API_KEY=sk-xxxxxxxxxxxx

# Tester directement
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY" | head -c 100
```

---

## Commandes utiles zbctl

```bash
# Installer zbctl
curl -LO https://github.com/camunda/zeebe/releases/latest/download/zbctl.linux
chmod +x zbctl.linux && sudo mv zbctl.linux /usr/local/bin/zbctl

# Verifier l'etat de Zeebe
zbctl status --address localhost:26500 --insecure

# Lister les processus deployes
zbctl get workflows --address localhost:26500 --insecure

# Creer une instance simple
zbctl create instance PROCESS_ID --address localhost:26500 --insecure

# Creer une instance avec variables
zbctl create instance PROCESS_ID \
  --variables '{"key":"value"}' \
  --address localhost:26500 --insecure
```
