# 03 - Guide des Modules

## Module 01 - Hello World

### Objectif
Prendre en main Camunda : deployer un BPMN et lancer une instance.

### Etapes
1. Deployer `processes/01_hello_process.bpmn` via Camunda Modeler
2. Lancer le worker :
```bash
python workers/worker_01_hello.py
```
3. Creer une instance via zbctl :
```bash
zbctl create instance hello-process --address localhost:26500 --insecure
```
4. Verifier dans Operate : http://localhost:8081

---

## Module 02 - Service Task (Commande)

### Objectif
Chainer 3 Service Tasks avec IoMapping de variables.

### Lancer
```bash
python workers/worker_02_04_services.py

# Creer une instance avec variables
zbctl create instance service-task-process \
  --variables '{"productId":"PROD-42","quantity":3,"unitPrice":29.99}' \
  --address localhost:26500 --insecure
```

### Resultat attendu dans le terminal worker
```
[check-stock] Product=PROD-42 | Stock=67
[calculate-price] qty=3 x 29.99 EUR = 107.96 EUR TTC
[send-confirmation] Confirmation envoyee : CMD-20260328155600
```

---

## Module 03 - Gateway XOR (Credit)

### Objectif
Router dynamiquement selon une variable calculee (score credit).

```bash
# Score >= 700 : branche approuve
zbctl create instance gateway-process \
  --variables '{"montant":5000,"revenu":50000}' \
  --address localhost:26500 --insecure

# Score < 500 : branche refuse
zbctl create instance gateway-process \
  --variables '{"montant":45000,"revenu":20000}' \
  --address localhost:26500 --insecure
```

### Verifier la branche prise
Operate > Instances > cliquer l'instance > voir le token sur la bonne branche

---

## Module 04 - Human Task (Conge)

### Objectif
Gerer une approbation humaine via Tasklist.

```bash
# 1. Lancer le worker
python workers/worker_02_04_services.py

# 2. Creer une instance
zbctl create instance human-task-process \
  --variables '{"employeeId":"E001","managerId":"demo","nbJours":5}' \
  --address localhost:26500 --insecure
```

### Completer la tache humaine
1. Ouvrir Tasklist : http://localhost:8082
2. Se connecter : demo / demo
3. Cliquer sur la tache "Valider Conge Manager"
4. Remplir : `decision = approuve` et `commentaire = OK`
5. Cliquer **Complete**
6. Verifier dans Operate que le process est complete

---

## Module 05 - AI Agent Groq

### Objectif
Integrer un LLM Groq dans un workflow BPMN avec Human-in-the-loop.

```bash
# Configurer la cle Groq
export GROQ_API_KEY=sk-xxxxxxxxxxxx

# Lancer le worker AI
python workers/worker_05_ai_agent.py

# Creer une instance
zbctl create instance ai-agent-process \
  --variables '{"documentUrl":"https://example.com/doc.txt","analyseType":"resume"}' \
  --address localhost:26500 --insecure
```

### Deux cas possibles
- **score_confiance >= 0.85** : traitement automatique (pas de tache humaine)
- **score_confiance < 0.85** : tache humaine dans Tasklist pour decision finale

### Resultat worker
```
[extract-text] Extraction depuis : https://example.com/doc.txt
[ai-analyze] Type=resume | Texte (87 chars)
[ai-analyze] Sentiment=positif | Confiance=0.92
[auto-process] Traitement automatique : AUTO-20260328160000
```
