#  »»» ModifierAgenda.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import json
import tkinter as tk
import customtkinter as ctk
import os
import shutil
import Errors

# Définition des variables
image = ""
bouton_url_image = ""
label_url_image = ""
entrée_date = ""
entrée_titre = ""
entrée_infos = ""

# Création de la fenêtre CustomTkinter
app = ctk.CTk()
app.geometry("775x400")
app.title("EditCalendar")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def WriteJson(titre, date, description, image) :
    # Création d'un dictionnaire à écrire dans le fichier calendar.json
    données = {}
    données["titre"] = titre
    données["date"] = date
    données["description"] = description
    données["image"] = image
    # Ouverture du fichier de stockage JSON et écriture des données
    try :
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/calendar.json", 'w') as f:
            json.dump(données, f, indent=4)
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'écriture dans agenda.json", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Données à écrire" : données})

def GetImage():
    global image
    global bouton_url_image
    global label_url_image

    # Changement du texte du bouton de sélectuon de l'affiche
    bouton_url_image.configure(text="Changer l'affiche")
    # Demande à l'utilisateur de sélectionner le fichier de l'affiche
    image = tk.filedialog.askopenfilename(title="Sélectionner l'affiche",
                                                       filetypes=(("Fichiers JPG", "*.jpg"), ("Fichiers PNG", "*.png"), ("Tous les fichiers", "*.*")))
    # Vérification du format de fichier
    if image.split(".")[-1] != "png" and image.split(".")[-1] != "jpg" :
            Errors.raise_error(app, "Format de fichier invalide ! Fichier PNG ou JPG nécessaires", "AjouterÉmission.py")
            return
    # Affichage du chemin de l'affiche sélectionnnée dans la fenêtre
    label_url_image.configure(text=f"Affiche sélectionnée : " + image)

    try :
        shutil.move(image, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Affiches/")
    except shutil.SameFileError :
        try :
            # Si le fichier est déjà présent dans la destination, on le supprime et le remplace par le nouveau fichier
            os.remove(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Affiches/{os.path.basename(image).split(".")[-1]}")
            shutil.move(image, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Affiches/")
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de la copie de l'image", "ModifierAgenda.py", mail=True, specific_error=e, additional_infos={"Chemin d'origine" : image, "Destination" : f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Affiches/{os.path.basename(image).split(".")[-1]}"})
    except shutil.Error :
        Errors.raise_error(app, "Erreur lors de la copie de l'image", "ModifierAgenda.py", mail=True, specific_error=e, additional_infos={"Chemin d'origine" : image, "Destination" : f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Affiches/{os.path.basename(image).split(".")[-1]}"})

def GetInfos():
    global entrée_date
    global entrée_titre
    global entrée_infos
    global titre
    global date
    global description

    # Récupération du contenu des champs d'entrée
    titre = entrée_titre.get()
    date = entrée_date.get()
    description = entrée_infos.get()

    # Appel de la fonction pour l'écriture des informations dans le fichier JSON
    WriteJson(titre, date, description, image)

def main() :
    # Création et affichage des éléments dans la fenâtre
    entrée_titre = ctk.CTkEntry(master=app, placeholder_text="Titre de l'émission", width=200)
    entrée_titre.pack(pady=10)

    entrée_date = ctk.CTkEntry(master=app, placeholder_text="Date de l'émission", width=200)
    entrée_date.pack(pady=10)

    entrée_infos = ctk.CTkEntry(master=app, placeholder_text="Description de l'émission", width=200)
    entrée_infos.pack(pady=10)

    label_url_image = ctk.CTkLabel(master=app, text="Aucune affiche sélectionnée", width=165)
    label_url_image.pack(pady=5)

    bouton_url_image = ctk.CTkButton(master=app, text="Sélectionner une affiche", command=GetImage)
    bouton_url_image.pack(pady=0)

    bouton_titre_date_audio = ctk.CTkButton(master=app, text="Confirmer les informations", command=GetInfos, fg_color="white", text_color="black", hover_color="grey")
    bouton_titre_date_audio.pack(pady=30)

    app.mainloop()