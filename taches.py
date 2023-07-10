from datetime import datetime
import os
import json


def demande_choix_menu(message, limite):
    choix = input(message)
    while not choix.isnumeric() or int(choix) not in range(1, limite):
        print(f"Veuillez entrer un chiffre entre : 1 et {limite}")
        return demande_choix_menu(message, limite)
    return choix


def saisieNom(message):
    nom = input(message)
    if nom.isdigit():
        print("Veuillez entrer un nom corret.")
        return saisieNom(message)
    return nom


def saisieDate():
    daty = input("Veuillez entrer la date limite sous le format JJ-MM-AA: ")
    try:
        datetime.strptime(daty, "%d-%m-%y")
        if datetime.strptime(daty, "%d-%m-%y") < datetime.now():
            print("Date déjà depassé, merci de taper une nouvelle date.")
            return saisieDate()
        return daty

    except:
        print("Erreur, veuillez entrer une date valide, format JJ-MM-AA: ")
        return saisieDate()


def ajouterTache(liste):
    nom = saisieNom("Veuillez entrer le nom du tache: ")
    delai = saisieDate()
    liste.append({'nom': nom, 'deadline': delai, 'statut': "Non terminé"})
    enregistrementTaches(liste)


def modifierTache(liste):
    numero_du_tache = int(demande_choix_menu(
        "Veuillez entrer le numero du tache à modifier svp: ", len(liste)+1))
    changer_le_nom = input("Voulez-vous changer le nom?(Y/N)")
    if changer_le_nom.lower() == "y":
        nouveau_nom = saisieNom("Veuillez entrer le nouveau nom: ")
        liste[numero_du_tache-1]['nom'] = nouveau_nom
    changer_le_delai = input("Voulez-vous changer le délai?(Y/N)")
    if changer_le_delai.lower() == "y":
        nouveau_delai = saisieDate()
        liste[numero_du_tache-1]['deadline'] = nouveau_delai
    statut_terminé = input("Le tache est terminé? (Y/N)")
    if statut_terminé.lower() == "y":
        liste[numero_du_tache-1]['statut'] = "Terminé"

    enregistrementTaches(liste)


def afficherTaches(liste):
    if liste == []:
        print("Aucune tache")
        return None
    for i, tache in enumerate(liste):
        delai_restant = datetime.strptime(
            tache['deadline'], "%d-%m-%y") - datetime.now()
        print(
            f"Tache nº`{i+1}: \"{tache['nom']}\" | delai restant: {delai_restant.days} jours, {delai_restant.seconds // 3600} heure et {(delai_restant.seconds % 3600) // 60} minutes | statut: {tache['statut']}")


def supprimerTache(liste):
    numero_du_tache = int(demande_choix_menu(
        "Veuillez entrer le numero du tache à supprimer svp: ", len(liste)+1))
    liste.remove(liste[numero_du_tache-1])
    enregistrementTaches(liste)


def chargementTaches(nom):
    with open(f"{nom}.json", "r") as f:
        taches = json.load(f)
    return taches


def enregistrementTaches(liste):
    with open(f"{nom}.json", "w") as f:
        json.dump(liste, f)


print("====== APPLICATION GESTIONNAIRE DE TACHE ======\n\n")

nom = saisieNom("Votre nom svp: ")

if os.path.isfile(f"{nom}.json"):
    taches = chargementTaches(nom)
else:
    taches = []

print("Bienvenue dans ce programme de gestionnaire des taches.\n")
while (True):
    print("""Tapez:
    1 Pour afficher la liste des taches.
    2 Pour ajouter une tache.
    3 Pour modifier une tache.
    4 Pour supprimer une tache.
    5 Pour quitter
    """)

    reponse = demande_choix_menu("\nVotre reponse svp: ", 6)

    if reponse == "1":
        afficherTaches(taches)
    elif reponse == "2":
        ajouterTache(taches)
    elif reponse == "3":
        modifierTache(taches)
    elif reponse == "4":
        supprimerTache(taches)
    else:
        break
    print()
