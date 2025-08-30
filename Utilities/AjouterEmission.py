#  »»» AjouterÉmission.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import pandas as pd
import json
import tkinter as tk
import customtkinter as ctk
import os
import shutil
from pydub import AudioSegment
from bs4 import BeautifulSoup
from datetime import datetime
import Errors
import WebsiteManager
import SupprimerEmission

# Définition des variables
chroniques = []
spreadsheet_path = ""
spreadsheet_title = ""
spreadsheet_date = ""
noms_chroniques_podcasts = {}
audio_path = ""
AudioSegment.converter = "ffmpeg"

# Création de la fenêtre CustomTkinter
app = ctk.CTk()
app.geometry("775x400")
app.title("AjouterÉmission")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

try :
    # Récupération des podcasts depuis le fichier podcasts.json
    with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'r', encoding='utf8') as f :
        data = json.load(f)
    for podcast in data :
        noms_chroniques_podcasts[podcast["nom_chronique"]] = podcast["fichier_html"]
except Exception as e :
    Errors.raise_error(app, "Erreur lors du chargement des podcasts", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"JSON content" : data})

# Représentation des chroniques sous forme de classes pour que chacune ait ses attributs
class Chronique:
    def __init__(self, type_chronique, nom_chronique, index, timestamp):
        self.type = type_chronique
        self.nom = nom_chronique
        self.index = index
        self.timestamp = timestamp
        self.timestamp_réel = timestamp
        self.podcast = False
        self.fichier = ""

def read_spreadsheet(path):
    global chroniques
    global noms_chroniques_podcasts
    
    try :
        # Lecture du fichier Excel
            # ╚> Convertion en objet Pandas pour la lecture du fichier
        file = pd.read_excel(path, sheet_name=0, converters={'Début (MM:SS)' : str}, header=None)
            # ╚> Vérification de la mise en page du fichier (noms des colonnes)
        if file.iloc[0,0] != "Nom/type de la chronique" or file.iloc[0,1] != "Début (MM:SS)" or file.iloc[0,2] != "Nom pour le podcast" :
            Errors.raise_error(app, "Mise en page du fichier Excel incorrecte !", "AjouterÉmission.py")
            return
        height, width = file.shape
        
        for i in range(1, height) :
            # Création des nouvelles chroniques
            nouvelle_chronique = Chronique(type_chronique=file.iloc[i,0], nom_chronique=None, index=i, timestamp=file.iloc[i, 1])
            chroniques.append(nouvelle_chronique)
            # Si la chronique est un podcast, récupération du sujet pour le podcast
            if nouvelle_chronique.type in noms_chroniques_podcasts :
                nouvelle_chronique.podcast = True
                nouvelle_chronique.nom = file.iloc[i, 2]
                # Vérification de la mise en page
                if file.iloc[i, 2] == "nan" :
                    Errors.raise_error(app, "Mise en page du fichier Excel incorrecte !", "AjouterÉmission.py")
                    return
            # Récupération des temps de début des chroniques
            timestamp_minutes = nouvelle_chronique.timestamp.split(":")[0]
            timestamp_secondes = nouvelle_chronique.timestamp.split(":")[1]
            # Conversion en nombre de secondes
            if str(timestamp_minutes[0]) == "0":
                timestamp_minutes = timestamp_minutes[1:]
            if str(timestamp_secondes[0]) == "0":
                timestamp_secondes = timestamp_secondes[1:]
            nouvelle_chronique.timestamp_réel = int(timestamp_minutes)*60 + int(timestamp_secondes)
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la lecture du fichier Excel", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path})
        return

def modify_html(podcast_filename):
    global spreadsheet_title
    global spreadsheet_date
    global audio_path
    global chroniques
    global app

    try :
        # Ouverture du fichier HTML et conversion en objet BeautifulSoup
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "r", encoding="utf-8") as f :
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        Errors.raise_error(app, "Erreur dans l'ouverture du fichier HTML (page web)", "AjouterÉmission.py", mail=True, specific_error=e)
        return
    
    try :
        # Récupération du numéro ID de la nouvelle émission
        if soup.find("div", {"class": "infos"}) != None :
            max_id_number = 1
            for div in soup.find_all("div", {"class": "infos"}) :
                id_number = int(div["id"].split("Infos")[-1])
                if id_number > max_id_number :
                    max_id_number = id_number
            id_number = max_id_number + 1
        else :
            id_number = 1

        # Création du nouveau code HTML
        html_ajout = f"""

                <div class="div-émission-background">
                    <div class="div-émission">
                        <div class="infos-émission">
                            <h2 class="titre-émission">{spreadsheet_title}</h2>
                            <h3 class="date-émission">{spreadsheet_date}</h3>
                        </div>

                        <div class="infos" id="Infos{id_number}"><img class="icone-infos" src="Images/Programme.svg" alt="" height="45px"></div>

                        <br>

                        <div class="div-audio">
                            <audio controls class="audio" id="Audio{id_number}">
                                <source src="Émissions/{os.path.basename(audio_path)}" type="audio/mpeg">
                                Votre navigateur ne supporte pas l'élément audio.
                            </audio>
                        </div>
                    </div>
                </div>

            <div class="div-programme-background" id="Programme-background{id_number}">
                <div class="div-programme-ensemble">
                    <div class="div-programme">
                        <h2 class="programme">Programme de l'émission :</h2>
        """

        # Ajout du code pour chaque élément du programme
        for chronique in chroniques :
            id_chronique =  f"Chronique{id_number}-{chronique.index+1}"
            html_ajout += f"""
                            <h3 class="programme" id="{id_chronique}">• {chronique.timestamp} - {chronique.type}</h3><script>document.getElementById("{id_chronique}").onclick = function ()""" + "{" + f"""document.getElementById("Audio{id_number}").currentTime = {chronique.timestamp_réel}; document.getElementById("Audio{id_number}").play();""" + "}" + """</script>
            """
        html_ajout += f"""
                    </div>
                    <div class="fermer" id="Close{id_number}"><img class="icone-fermer" src="Images/Fermer.svg" alt="" height="45px"></div>
                </div>
            </div>
        """
        # Insertion dans le code existant
        soup_ajout = BeautifulSoup(html_ajout, "html.parser")
        dates_émissions = soup.find_all("h3", {"class" : "date-émission"})
            # ╚> Placement de la nouvelle émission dans l'ordre chronologique
        spreadsheet_date_formatted = datetime.strptime(spreadsheet_date, "%d/%m/%Y")
        written = False
        if dates_émissions :
            for date in dates_émissions :
                if datetime.strptime(date.text, '%d/%m/%Y') > spreadsheet_date_formatted :
                    soup.find("div", {"class" : "conteneur-émissions"}).insert(dates_émissions.index(date) + 1, soup_ajout)
                    written = True
                    break
        if written == False :
            soup.find("div", {"class" : "conteneur-émissions"}).insert(0, soup_ajout)
        # Écriture dans le fichier HTML
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "w", encoding="utf-8") as f :
            f.write(str(soup))
            f.close()
    except Exception as e :
        Errors.raise_error(app, "Erreur dans la modification du fichier HTML (page web)", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Spreadsheet date" : spreadsheet_date})
        return

    try :
        for chronique in chroniques :
            if chronique.podcast == True :
                # Ouverture du fichier HTML du podcast te conversion en objet BeautifulSoup
                with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[chronique.type]}", "r", encoding="utf-8") as f :
                    soup = BeautifulSoup(f, "html.parser")
                # Création du code pour la nouvelle chronique du podcast
                html_ajout_chroniques = f"""
                <div class="div-émission-background">
                    <div class="div-émission">
                        <div class="infos-émission">
                            <h2 class="titre-émission">{chronique.nom}</h2>
                            <h3 class="date-émission">{spreadsheet_title} - {spreadsheet_date}</h3>
                        </div>

                        <div class="div-audio-podcasts">
                            <audio controls class="audio" id="Audio{id_number}">
                                <source src="Émissions/{os.path.basename(audio_path)[:-4]}/{chronique.fichier}" type="audio/mpeg">
                                Votre navigateur ne supporte pas l'élément audio.
                            </audio>
                        </div>
                    </div>
                </div>
            """
                soup_ajout_chroniques = BeautifulSoup(html_ajout_chroniques, "html.parser")
                # Placement du podcast dans l'ordre chronologique
                dates_émissions = soup.find_all("h3", {"class" : "date-émission"})
                spreadsheet_date_formatted = datetime.strptime(spreadsheet_date, "%d/%m/%Y")
                written = False
                if dates_émissions :
                    for date in dates_émissions :
                        if datetime.strptime(date.text.split(" - ")[-1], '%d/%m/%Y') > spreadsheet_date_formatted :
                            soup.find("div", {"class" : "conteneur-podcasts"}).insert(dates_émissions.index(date) + 1, soup_ajout_chroniques)
                            break
                if written == False :
                    soup.find("div", {"class" : "conteneur-podcasts"}).insert(0, soup_ajout_chroniques)
                # Écriture dans le fichier HTML
                with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[chronique.type]}", "w", encoding="utf-8") as f :
                    f.write(str(soup))
                    f.close()
    except Exception as e :
        Errors.raise_error(app, "Erreur dans la modification du fichier HTML (page web)", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Spreadsheet date" : spreadsheet_date})
        return

    # Vérifie comment s'est passé la synchronisation avec GitHub
    if WebsiteManager.commit_changes(app) == "error" :
        SupprimerEmission.delete_program(spreadsheet_title)
    else :
        WebsiteManager.finish_window(app)

def process_info():
    global spreadsheet_title
    global spreadsheet_date
    global audio_path
    global chroniques

    # Vérification des informations données par l'utilisateur
    if not audio_path or not spreadsheet_title :
        Errors.raise_error(app, "Veuillez remplir tous les champs", "GérerPodcasts.py")
        return

    print(chroniques)
    for chronique in chroniques :
        if chronique.podcast == True :
            podcast_filename = f"{chronique.type} - "
            invalid_chars = '<>:"/\\|?*'
            for char in chronique.nom.strip() :
                if char not in invalid_chars :
                    if char == " " :
                        char = "-"
                    podcast_filename += char
            podcast_filename += ".mp3"
            chronique.fichier = podcast_filename
            try :
                # Découpage des podcasts depuis l'émission
                audio_chronique = AudioSegment.from_file(audio_path)
                print(chronique.index)
                audio_chronique = audio_chronique[int(chronique.timestamp_réel*1000):int(chroniques[chronique.index].timestamp_réel*1000)]
                audio_chronique = audio_chronique.fade_in(1500)
                audio_chronique = audio_chronique.fade_out(1500)
                audio_chronique.export(podcast_filename, format="MP3")
            # Déplacement des audios des podcasts vers le dossier adapté
            except Exception as e :
                Errors.raise_error(app, "Erreur lors du découpage des podcasts", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path, "Filename" : podcast_filename, "Timestamp chronique" : chronique.timestamp})
                return
            try :
                shutil.move(podcast_filename, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}")
            except shutil.SameFileError :
                try :
                    # Si le fichier est déjà présent dans la destination, on le supprime et le remplace par le nouveau fichier
                    os.remove(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}/{podcast_filename}")
                    shutil.move(podcast_filename, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}")
                except Exception as e :
                    Errors.raise_error(app, "Erreur lors de l'enregistrement des podcasts", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path, "Filename" : podcast_filename})
                    return
            except shutil.Error :
                Errors.raise_error(app, "Erreur lors de l'enregistrement des podcasts", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path, "Filename" : podcast_filename})
                return

    modify_html(podcast_filename)

def select_spreadsheet(app):
    global spreadsheet_path
    global spreadsheet_title
    global spreadsheet_date
    try :
        # Demande à l'utilisateur de sélectionner le fichier Excel pour les informations
        spreadsheet_path = tk.filedialog.askopenfilename(title="Sélectionner le fichier infos",
                                                        filetypes=(("Fichiers Excel", ".xlsx"), ("Tous les fichiers", ".*")))
        # Vérification du format de fichier
        if spreadsheet_path.split(".")[-1] != "xlsx" :
            Errors.raise_error(app, "Format de fichier invalide ! Fichier Excel (.xlsx) nécessaire", "AjouterÉmission.py")
            return
        else :
            # Récupération des informations contenues dans le nom du fichier
            spreadsheet_title = spreadsheet_path.split("/")[-1].split(" - ")[0]
            spreadsheet_date = spreadsheet_path.split("/")[-1].split(" - ")[1].replace("_","/")[:-5]
            if len(spreadsheet_date.split("/")) == 3 and len(spreadsheet_date.split("/")[0]) == 2 and spreadsheet_date.split("/")[0].isdigit() == True and len(spreadsheet_date.split("/")[1]) == 2 and spreadsheet_date.split("/")[1].isdigit() == True and len(spreadsheet_date.split("/")[2]) == 4 and spreadsheet_date.split("/")[2].isdigit() == True : # Vérification du format de la date
                # Si tout est correct, affichage des informations dans la fenêtre
                label_spreadsheet_path = ctk.CTkLabel(master=app, text=f"Fichier sélectionné : {spreadsheet_path}", width=165)
                label_spreadsheet_title = ctk.CTkLabel(master=app, text=f"Nom enregistré : {spreadsheet_title}", width=165)
                label_spreadsheet_date = ctk.CTkLabel(master=app, text=f"Date enregistrée : {spreadsheet_date}", width=165)
                label_spreadsheet_path.pack(pady=5)
                label_spreadsheet_title.pack(pady=0)
                label_spreadsheet_date.pack(pady=0)
            else :
                Errors.raise_error(app, "Date du fichier invcalide (format JJ/MM/AAAA nécessaire) !", "AjouterÉmission.py")
                return
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la lecture du fichier Excel", "AjouterÉmission.py", mail=True, specific_error=e)
        return

    read_spreadsheet(spreadsheet_path)

def select_audio():
    global audio_path
    # Demande à l'utilisateur de sélectionner le fichier audio de l'émission
    audio_path = tk.filedialog.askopenfilename(title="Sélectionner le fichier audio",
                                                     filetypes=(("Fichiers MP3", ".mp3"), ("Tous les fichiers", ".*")))
    # Vérification du format de fichier
    if audio_path.split(".")[-1] != "mp3" :
            Errors.raise_error(app, "Format de fichier invalide ! Fichier MP3 (.mp3) nécessaire", "AjouterÉmission.py")
            return
    # Affichage du chemin du fichier sélectionné
    label_audio_path = ctk.CTkLabel(master=app, text=f"Fichier audio sélectionné : {audio_path}", width=165)
    label_audio_path.pack(pady=5)
    # SI ce n'est pas déjà fait, création d'un dossier pour l'émission
    if audio_path != f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}/{os.path.basename(audio_path)}" :
        os.mkdir(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}")
        # Copie de l'émission dans le nouveau dossier
        try :
            try :
                shutil.copy(audio_path, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}")
            except shutil.SameFileError :
                try :
                    # Si un fichier du même nom s'y trouve déjà, on le supprime et le remplace par le nouveau
                        # (Ce n'est normalement pas nécessaire étant donné la condition ci-dessus mais permet d'éviter toute erreur)
                    os.remove(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}/{os.path.basename(audio_path)}")
                    shutil.copy(audio_path, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}")
                except Exception as e :
                    Errors.raise_error(app, "Erreur lors de la copie du fichier audio", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path})
                    return
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de la copie du fichier audio", "AjouterÉmission.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path})
            return

def main():
    # Création et affichage des éléments dans la fenêtre
    bouton_tableur = ctk.CTkButton(master=app, text="Sélectionner le fichier infos", command=lambda : select_spreadsheet(app))
    bouton_tableur.pack(pady=5)

    bouton_audio = ctk.CTkButton(master=app, text="Sélectionner le fichier audio", command=select_audio)
    bouton_audio.pack(pady=10)

    bouton_validation = ctk.CTkButton(master=app, text="Valider les informations", command=process_info, fg_color="white", text_color="black", hover_color="grey")
    bouton_validation.pack(pady=10)

    app.mainloop()

if __name__ == "__main__" :
    main()