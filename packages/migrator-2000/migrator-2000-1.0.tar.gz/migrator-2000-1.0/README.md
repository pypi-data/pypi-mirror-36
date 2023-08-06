# Migrator

Migrator est un script écrit en Python permettant d'effectuer des migrations de base de donnée d'un serveur à un autre.

## Features

* Server files configuration
* Structure files configuration
* Ssh dump system
* Ssh import system

## Dependencies
* Python2.7

## Préparer le script

Tout d'abord il faut cloner le projet
```bash
git clone git@gitlab.com:Beemoov/common/other/migrator.git
cd migrator
```

Puis installer les dépendences

```bash
pip install click
```

## Configurer le script

Il faut créer deux fichiers de configuration pour le serveur A et B (configs/servers/*.json)
```json
{
  "database": {
    "host": "myserver.servers.com",
    "user": "root",
    "password": "root",
    "name": "mydb"
  },
  "ssh": {
    "host": "myserver.servers.com",
    "user": "root",
    "port": "6666"
  }
}
```

Puis créer un fichier de configuration pour décrire le dump qui sera effectué (configs/tables/*.json)
```json
[
  {
    "name": "conditions",
    "where": ""
  },
  {
    "name": "consequences",
    "where": "id > 20000"
  },
  {
    "name": "dialog_actors dialog_scenes_sounds",
    "where": "sceneId > 99999"
  }
]
```

## Lancer le script

```bash
python migrate.py <serverA> <serverB> <structure> [--mysql/--ssh]
```
* serverA - Correspond au nom du fichier de configuration du server A (Dump)
* serverB - Correspond au nom du fichier de configuration du server B (Import)
* structure - Correspond au nom du fichier décrivant le Dump
* method* [ssh|mysql] - Permet de définir la méthode pour le dump et l'import (default: mysql)

### Credits

* Author | Martin Paucot <martin@beemoov.com>