#  »»» SupprimerEmission.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

from bs4 import BeautifulSoup
import tkinter as tk
import customtkinter as ctk
import os
import json
import WebsiteManager
import Errors

noms_fichiers_podcasts = ["podcasts-chroniques-scientifiques.html", "podcasts-chroniques-touristiques.html", "podcasts-chroniques-culturelles.html", "podcasts-portraits.html"]
noms_chroniques_podcasts = {}

# Création de la fenêtre CustomTkinter
app = ctk.CTk()
app.geometry("775x400")
app.title("ModifierSiteWeb")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

try :
    # Récupération des podcasts depuis le fichier podcasts.json
    with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'r', encoding='utf8') as f :
        data = json.load(f)
    for podcast in data :
        noms_chroniques_podcasts[podcast["nom_chronique"]] = podcast["fichier_html"]
except Exception as e :
    Errors.raise_error(app, "Erreur lors du chargement des podcasts", "SupprimerÉmission.py", mail=True, specific_error=e, additional_infos={"JSON content" : data})

def delete_program(nom_émission) :
    global app
    try :
        # Ouverture du fichier HTML (page web) des émissions
        try :
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "r", encoding="utf-8") as f :
                # Conversion en objet BeautifulSoup
                soup = BeautifulSoup(f, "html.parser")
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de l'ouverture du fichier HTML des émissions", "SupprimerÉmission.py", mail=True, specific_error=e)
        # Copie du contenu de la page en cas d'erreur
        soup_copy = soup
        # Récupération de tous les titres des émissions surla page web
        noms_émissions = soup.find_all("h2", {"class" : "titre-émission"})
        # Suppression de l'émission dont le nom correspond à celui sélectionné
        for nom_émission in noms_émissions :
            if nom_émission.text == nom_émission :
                nom_émission.find_parent('div', class_ = "div-émission-background").decompose()
                break
        # Écriture dans le fichier HTML
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "w", encoding="utf-8") as f :
            f.write(str(soup))

    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la suppression de l'émission", "SupprimerÉmission.py", mail=True, specific_error=e, additional_infos={"Nom de l'émission" : nom_émission})

    try :
        for podcast in noms_chroniques_podcasts :
            # Ouverture de chaque fichier HTML des podcasts et conversion en objet BeautifulSoup
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[podcast]}", "r", encoding="utf-8") as f :
                soup = BeautifulSoup(f, "html.parser")
            # Suppression des podcasts appartenant à l'émission sélectionnée
            dates_podcasts = soup.find_all("h3", {"class" : "date-émission"})
            for date_podcast in dates_podcasts :
                if date_podcast.text.split(" - ")[0] == nom_émission :
                    date_podcast.find_parent('div', class_ = "div-émission-background").decompose()
                    break

    except Exception as e :
        try :
            # En cas d'erreur avec les podcasts, annule la suppression de l'émission de base
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "w", encoding="utf-8") as f :
                f.write(str(soup_copy))
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de la suppression des podcasts", "SupprimerÉmission.py", mail=True, specific_error=e, additional_infos={"Nom de l'émission" : nom_émission, "Podcasts" : noms_chroniques_podcasts, "Statut" : "Failed to reset after podcasts failed"})
            return
        Errors.raise_error(app, "Erreur lors de la suppression des podcasts", "SupprimerÉmission.py", mail=True, specific_error=e, additional_infos={"Nom de l'émission" : nom_émission, "Podcasts" : noms_chroniques_podcasts})
        return
    
    WebsiteManager.finish_window(app)

def main() :
    # Ouverture du fichier HTML des émissions et conversion en objet BeautifulSoup
    try :
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "r", encoding="utf-8") as f :
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'ouverture du fichier HTML des émissions'", "SupprimerÉmission.py", mail=True, specific_error=e)
        return

    # Récupération des noms de toutes les émissions
    émissions = soup.find_all("h2", {"class" : "titre-émission"})
    noms_émissions = []
    for émission in émissions :
        noms_émissions.append(émission.text)

    # Création des éléments à afficher dans la fenêtre
    label_émission_à_supprimer = ctk.CTkLabel(master=app, text="Sélectionnez l'émission à supprimer")
    label_émission_à_supprimer.pack(pady=5)

    dropdown = ctk.CTkOptionMenu(master=app, values=noms_émissions, command=delete_program) # Menu déroulant contenant la liste des émissions
    dropdown.pack(pady=0)

    app.mainloop()