# Projet 9 pour la formation Développeur Python d’OpenClassrooms
## Installation
Une fois que vous avez cloné le dépôt sur votre machine locale, vous devez installer un environnement virtuel.
Exécutez ces commandes depuis le répertoire racine du dépôt.

```
python -m venv env
source env/bin/activate
```
Ensuite, installez les paquets requis depuis le fichier requirements.txt

```
pip install -r requirements.txt
```

## Fonctionnement
Déplacez-vous dans le dossier contenant l'application Django complète, puis lancez le serveur.

```
cd litrevu
python manage.py runserver
```

Une fois que le serveur est lancé, il vous indiquera l’adresse depuis laquelle vous pouvez y accéder, généralement http://127.0.0.1:8000/.
La première page affichée est une page de connexion. Vous pouvez trouver des identifiants de test dans le fichier "users.txt" à la racine du dépôt.
Utilisez-les pour vous connecter et, à partir de là, l’utilisation du site devrait être intuitive et facile.

# Projet 9 for the OpenClassrooms Python Developer Training Porgramme

## Installation
Once you have cloned the repository to your local machine, you need to install a virtual environment. 
Run these commands from the root directory in the repo.


```
python -m venv env
source env/bin/activate
```

Then install the required packages from the requirements.txt

```
pip install -r requirements.txt
```

## Operation
Move into the folder containing the full Django app, then launch the server.
```
cd litrevu
python manage.py runserver
```
Once the server has loaded, it will tell you the address you can launch it from, usually http://127.0.0.1:8000/.
The first page you see is a sign-in page. You can find some test account details in "users.txt" in the root 
directory of the repo. Use these to log in and from there the operation of the site should be intuitve and easy to use.


