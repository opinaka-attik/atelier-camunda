# 02 - Concepts Cles Camunda 8

## Architecture Camunda 8

```
┌─────────────────────────────────────────────────────────┐
│                     Votre Application                    │
│  (Python, Java, Node.js, etc.)                          │
└────────────────┬───────────────────────────────────────┘
                 │ gRPC / REST API
┌────────────────▼───────────────────────────────────────┐
│                    ZEEBE (Moteur BPMN)                  │
│  - Execute les processus BPMN                          │
│  - Distribue les jobs aux workers                      │
│  - Gere l'etat des instances                           │
└────────────────┬───────────────────────────────────────┘
                 │ Exporte les evenements
┌────────────────▼───────────────────────────────────────┐
│              ELASTICSEARCH (Stockage)                   │
│         ┌───────────────┐  ┌──────────────┐           │
│         │    OPERATE    │  │   TASKLIST   │           │
│         │  (Monitoring) │  │  (UI Tasks)  │           │
│         └───────────────┘  └──────────────┘           │
└────────────────────────────────────────────────────────┘
```

## Concepts fondamentaux

### Process Definition vs Process Instance
- **Process Definition** : le schema BPMN deploye (comme une classe)
- **Process Instance** : une execution concrete du processus (comme un objet)

### Variables
Chaque instance a ses propres variables (JSON) :
```json
{ "employeeId": "E001", "nbJours": 5, "score": 720 }
```

### Service Task + Job Worker
```
BPMN                          Python
─────────────────────         ──────────────────────
Service Task                  @worker.task(type="X")
  type="check-stock"  ──────► async def handler(...):
                                  return {"result": ...}
```

### FEEL (Expression Language)
Language d'expression utilise dans les conditions Camunda :
```
=score >= 700           # condition simple
=score >= 500 and score < 700  # AND
=list contains(["A","B"], categorie)  # liste
=decision = "approuve"  # comparaison string
```

### IoMapping (Input/Output)
Filtre les variables entre process et worker :
```xml
<zeebe:ioMapping>
  <zeebe:input source="=montant" target="montant" />
  <zeebe:output source="=totalPrice" target="totalPrice" />
</zeebe:ioMapping>
```

## Comparaison Camunda vs n8n

| Aspect          | Camunda 8          | n8n                    |
|-----------------|--------------------|-----------------------|
| Standard        | BPMN 2.0 / DMN     | Proprietary           |
| Use case        | Business processes | Automation/integration|
| Human tasks     | Natif (Tasklist)   | Non natif             |
| Long running    | Mois/annees        | Minutes/heures        |
| Complexity      | Elevee             | Faible                |
| Language        | FEEL, Java, Python | JavaScript            |
| Monitoring      | Operate (riche)    | Execution logs        |
