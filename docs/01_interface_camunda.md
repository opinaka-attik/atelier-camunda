# 01 - Interface Camunda 8

## Vue d'ensemble des composants

Camunda 8 est compose de plusieurs services distincts :

| Composant     | Role                                              |
|---------------|---------------------------------------------------|
| **Zeebe**     | Moteur BPMN - execute les processus               |
| **Operate**   | Monitoring - visualise les instances en cours     |
| **Tasklist**  | Portail - gere les taches humaines (User Tasks)   |
| **Modeler**   | Editeur BPMN/DMN (desktop ou web)                 |

## Operate (http://localhost:8081)

### Navigation
- **Processes** : liste des processus deployes
- **Instances** : toutes les instances en cours / terminees
- **Incidents** : erreurs et exceptions
- **Dashboard** : vue globale KPIs

### Visualiser une instance
1. Processes > cliquer sur un processus
2. Cliquer sur une instance
3. Le diagramme BPMN s'affiche avec l'etat de chaque noeud :
   - **Vert** : token actif ici
   - **Gris** : passe
   - **Rouge** : incident

### Filtres utiles
```
State: ACTIVE | COMPLETED | CANCELED | INCIDENT
Process: nom du processus
Version: numero de version
```

## Tasklist (http://localhost:8082)

### Navigation
- **Tasks** : liste des taches assignees
- **All tasks** : toutes les taches (tous assignees)
- **Claimed by me** : mes taches

### Completer une Human Task
1. Tasklist > Tasks
2. Cliquer sur une tache
3. Remplir le formulaire
4. Cliquer **Complete**

## Camunda Modeler (desktop)

### Raccourcis claviers
| Action            | Raccourci          |
|-------------------|--------------------|
| Nouveau fichier   | Ctrl+N             |
| Ouvrir            | Ctrl+O             |
| Sauvegarder       | Ctrl+S             |
| Deployer          | Ctrl+Shift+D       |
| Zoom avant/arriere| Ctrl + / Ctrl -    |
| Chercher element  | Ctrl+F             |

### Types d'elements BPMN

| Element           | Icone  | Usage                              |
|-------------------|--------|------------------------------------||
| Start Event       | Cercle | Debut du processus                 |
| End Event         | Cercle epais | Fin du processus             |
| Service Task      | Rectangle + engrenage | Tache automatique     |
| User Task         | Rectangle + bonhomme | Tache humaine         |
| Gateway XOR       | Losange + X | Branchement exclusif          |
| Gateway Parallel  | Losange + + | Branchement parallele         |
| Message Event     | Cercle + enveloppe | Echange de messages    |
