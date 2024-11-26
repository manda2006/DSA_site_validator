# Validator

Validator est une application web construite avec Django et Tailwind CSS. Le projet inclut un système d'authentification avec une page de connexion personnalisée et une page d'accueil pour les utilisateurs connectés. 

## Fonctionnalités

- **Authentification** :
  - Page de connexion pour les utilisateurs.
  - Redirection automatique après connexion ou déconnexion.
  - Utilisation du système utilisateur par défaut de Django.

- **Styling** :
  - Intégration de **Tailwind CSS** pour un design moderne et réactif.
  - Utilisation de **django-widget-tweaks** pour personnaliser les champs de formulaire.

- **Sécurité** :
  - Protection CSRF sur tous les formulaires.
  - Requêtes POST pour les actions sensibles (connexion et déconnexion).

## Prérequis

- Python 3.8+
- Django 4.0+
- Node.js (pour gérer les dépendances de Tailwind CSS)

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-utilisateur/validator.git
cd validator
```
## Environment and dependencies installation
```
python -m venv .venv
.venv\Scripts\activate
.venv\Scripts\python -m pip install -r requirements.txt
python manage.py tailwind install
```

# Deployment in development
bash 01 : 
```
.venv\Scripts\activate
cd validator
python manage.py tailwind start
```
bash 02 :
```
.venv\Scripts\activate
cd validator
python manage.py runserver

```