
## Création de l'image

TODO

## Authentification

### Creation :
Envoie l'image du photomaton

### Avant d'envoyer l'appareil au client

#. on crée le client sur l'interface

### Validation de la réception / configuration de la part du client


#. Le client reçoit le photomaton

    Si il ne trouve pas de connexion internet :
        il active le mode adhoc et affiche le SSID et le Mdp pour se connecter.
        quand le client se connect il est dessuite renvoyer vers une page pour qu'il indique les parametre de connexion.
        puis le photomaton redemarre.

#. une fois connecter 
    Si il n'est lié a aucun client (premier utilisation)
        le photo lui propose un code a retaper sur l'interface web que seul une personne authentifier peux avoir accées.
        une fois connecter le photomaton redemarre

        # connexion du photomaton au server
            requete Socket.io via le photomaton au serveur.
            le serveur accepte au Socket et crée un code a 8 caratere (minuscule majuscule) qu'il stock dans une table temporaire (table : paillasson) avec l'id du photomaton
            le serveur renvoi un message sur le photomaton avec le code
            le photomaton affiche le code avec un message connect toi et tape le code ...
            le photomaton est a attente d'une reponse 

        # le client se connecte sur sont compte :
            il va sur la page "enregistrer mon photomaton".
            il tape le code donner sur le photomaton.
            le serveur recupere le code et regarde si il est dans la table [paillasson]
                si oui : il crée une nouvelle ligne dans les photomaton et la lie au client.
                    il recupere l'id du photomaton
                    il crée une clé pour que le photomaton lui renvois les photo via des requete post
                    il envoie l'id et la clef au photomaton
                    le serveur recupere le code le lie aux client

    Si deja connecter (a deja un id et un clé)
        si le photomaton est connecter a internet
            "Envoie des photos" toutes les 5 minutes
            le photomaton démare et charge les parametres du le site.
            et les met a jour sur dans sa base de donnée et dossier template.


        si le photomaton n'est pas connecter a internet
            test de connexion.
            le photomaton démare et charge de sa base.
            essaye d'envoyer les photos sur le site tous les 5 minutes
            Envoie des photos




## fonction de Envoie des photos :
    si il y a des photo dans PhotoQueue
        si impossible 
            il ne fais rien
        sinon :
            il essaye d'envoyer les photo avec son ID et sa clé en parametre.
            il controle quelle sont bien envoyer 
            il vide la liste PhotoQueue. 
            il vide le dossier.



## lance le photomaton.
    - a chaque prise de photo il stocke celle-ci avec un nom (DDmmmY_HHMMSS.jpg) dans un dossier
    - crée une entrer avec le nom de la photo dans un table sur la base de donnée interne au photomaton (PhotoQueue)

            



### Technologie du photomaton 

Raspberry Pi 4 (ARM) ou ordinateur Atom (x86):
    

## software(lib) :
    - interface / Kivy ou Pygame
    - gestion video OPENCV
    - communication internet via request
    - dbus pour la gestion de la connexion wifi adhoc au debut
    - flask pour le petit programme d'auto connexion.
    - Socket.io


## question?
    - peut-on enlever La GUI de base (gnome ou autre...) sur linux pour ameliorer la
    vitesse du pc