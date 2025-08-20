#  »»» GérerPodcasts.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import tkinter as tk
import customtkinter as ctk
from bs4 import BeautifulSoup
import json
import os
import ctypes
from PIL import Image
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY
from lxml import etree as ET
import shutil
import datetime
import Errors
from datetime import datetime

# Création de la fenêtre CustomTkinter
app = ctk.CTk()
app.geometry("775x400")
app.title("AjouterÉmission")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
scrollable_frame = ""
# Définition des variables
podcast_name = ""
icon_path = ""
audio_path = ""

# Récupération des podcasts depuis le fichier podcasts.json
noms_chroniques_podcasts = {}
try :
    with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'r', encoding='utf8') as f :
        data = json.load(f)
    for podcast in data :
        noms_chroniques_podcasts[podcast["nom_chronique"]] = podcast["fichier_html"]
except Exception as e :
    Errors.raise_error(app, "Erreur lors du chargement des podcasts", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"JSON content" : data})

def delete_podcast(frame, podcast) :
    global noms_chroniques_podcasts
    global scrollable_frame

    try :
        # Affichage de la fenêtre d'alerte Windows
        style = 0x00000001 | 0x00000030 # Codes pour le type de fenêtre
        result = ctypes.windll.user32.MessageBoxW(0, "Voulez-vous vraiment supprimer ce podcast définitivement ?", "SupprimerPodcast", style)
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'affichage de la fenêtre d'alerte Windows", "GérerPodcasts.py", mail=True, specific_error=e)
    if result == 1 : # L'utilisateur clique sur "OK"
        try :
            # Suppression du podcast de l'affichage
            frame.destroy()
            os.remove(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[podcast]}")
            del(noms_chroniques_podcasts[podcast])
            # Suppression du podcast du fichier de stockage JSON
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'r', encoding='utf8') as f :
                data = json.load(f)
            new_data = [podcast_dictionnary for podcast_dictionnary in data if podcast_dictionnary.get("nom_chronique") != podcast]
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
            # Suppression du podcast du fichier HTML (site web)
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.html", "r", encoding="utf-8") as f :
                soup = BeautifulSoup(f, "html.parser")
            boutons_podcasts = soup.find_all("h2", {"class" : "texte-bouton-podcast"})
            for bouton_podcast in boutons_podcasts :
                if bouton_podcast.text == podcast :
                    bouton_podcast.find_parent('div', class_ = "div-bouton-podcast-background").decompose()
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.html", "w", encoding="utf-8") as f :
                    f.write(str(soup))
                    f.close()
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de la suppression des podcasts", "GérerPodcasts.py", mail=True, specific_error=e)
    else : # Sinon, arrêt de la procédure de suppression
        return
    
def select_icon() :
    global icon_path
    try :
        # Demande à l'utilisateur de sélectionner le fichier PNG de l'icône
        icon_path = tk.filedialog.askopenfilename(title="Sélectionner l'icône'",
                                                filetypes=(("Fichiers PNG", ".png"), ("Fichiers JPG", ".JPG"), ("Tous les fichiers", ".*")))
        if icon_path.split(".")[-1] != "png" and icon_path.split(".")[-1] != "jpg" :
                Errors.raise_error(app, "Format de fichier invalide ! Fichier PNG ou JPG nécessaires", "GérerPodcasts.py")
                return
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la sélection de la nouvelle icône", "GérerPodcasts.py", mail=True, specific_error=e)

def add_podcast(new_podcast, frame) :
    global noms_chroniques_podcasts
    global scrollable_frame
    global icon_path

    # Vidage du champ d'entrée
    new_podcast.delete(0, ctk.END)
    new_podcast = new_podcast.get()

    # Vérification des champs d'entrée
    if not new_podcast or not icon_path :
        Errors.raise_error(app, "Veuillez remplir tous les champs", "GérerPodcasts.py")
        return

    try :
        # Suppression des caractères non autorisés pour les noms de fichiers
        invalid_chars = '<>:"/\\|?*'
        filename = "podcasts"
        for char in new_podcast.lower().strip() :
            if char not in invalid_chars :
                if char == " " :
                    char = "-"
                filename += char
        filename += ".html"
        noms_chroniques_podcasts[new_podcast] = filename

        # Ajout du nouveau podcast dans le fichier de stockage JSON
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'r', encoding='utf8') as f :
            data = json.load(f)
        new_podcast_dictionnary = {"nom_chronique" : new_podcast, "fichier_html" : noms_chroniques_podcasts[new_podcast]}
        data.append(new_podcast_dictionnary)
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Création du nouveau fichier HTML du podcast
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[new_podcast]}", 'w', encoding='utf-8') as f:
            f.write(f"""
    <!DOCTYPE html>

    <html>
    <head>
    <title>{new_podcast} - Radio 6</title>
    <link href="styles.css" rel="stylesheet"/>
    <link href="Images/Logo icone.svg" rel="icon" sizes="48x48" type="image/svg"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    </head>
    <body>
    <div class="div-nav">
    <div class="div-menu">
    <a href="index.html"><h2>Accueil</h2></a>
    </div>
    <div class="div-menu">
    <a href="émissions.html"><h2>Émissions</h2></a>
    </div>
    <div class="div-menu">
    <h2 class="fleche-menu">▶</h2>
    <a href="podcasts.html"><h2>Podcasts</h2></a>
    </div>
    <div class="div-menu">
    <a href="a-propos.html"><h2>À propos</h2></a>
    </div>
    <br/>
    <div id="Niveau-sonore">
    <div id="Slider"><img alt="" src="Images/Slider.svg"/></div>
    <div id="Volume-icone"><img alt="" height="65px" id="Volume-icone-img" src="Images/Volume ON.svg"/></div>
    <div id="Curseur"></div>
    </div>
    </div>
    <div class="div-nav-téléphone" id="Div-nav-téléphone">
    <div class="div-menu-téléphone" id="Div-menu-téléphone#">
    <a href="#"><h2 class="contenu-menu-téléphone"></h2></a>
    </div>
    <div class="div-menu-téléphone" id="Div-menu-téléphone1">
    <a href="index.html"><h2 class="contenu-menu-téléphone">Accueil</h2></a>
    </div>
    <div class="div-menu-téléphone" id="Div-menu-téléphone2">
    <a href="émissions.html"><h2 class="contenu-menu-téléphone">Émissions</h2></a>
    </div>
    <div class="div-menu-téléphone" id="Div-menu-téléphone3">
    <a href="podcasts.html"><h2 class="contenu-menu-téléphone">Podcasts</h2></a>
    </div>
    <div class="div-menu-téléphone" id="Div-menu-téléphone4">
    <a href="a-propos.html"><h2 class="contenu-menu-téléphone">À propos</h2></a>
    </div>
    </div>
    <div class="div-bouton-nav-téléphone" id="Bouton-nav-téléphone">
    <img alt="" height="50px" id="Image-bouton-nav-téléphone" src="Images/Ouvrir menu.svg"/>
    </div>
    <img class="bouton-thème" height="42px" id="Bouton-thème" src="Images/Thème clair.png"/>
    <div class="conteneur" id="Conteneur">
    <img alt="" class="logo-header" id="Logo-header" src="Images/Logo header.png" width="425px"/>
                    

    </div>
    <script src="script-podcasts.js"></script>
    </div></body></html>

    """)

        # Ajout du podcast à la liste sur la fenêtre
        item_frame = ctk.CTkFrame(scrollable_frame)
        item_frame.pack(fill="x", pady=2, padx=5)
        item_label = ctk.CTkLabel(item_frame, text=new_podcast, anchor="w")
        item_label.pack(side="left", padx=5, expand=True, fill="x")
        delete_button = ctk.CTkButton(item_frame, text="Supprimer", command=lambda frame=item_frame: delete_podcast(frame, podcast), width=80)
        delete_button.pack(side="right", padx=5)

    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la création du nouveau podcast", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Filename" : filename, "Nom du podcast" : new_podcast})
        return

    try :
        # Transformation de l'image PNG en SVG
            # ╚> Ouverture de l'image au format adapté
        img = Image.open(icon_path)
        bm = Bitmap(img, blacklevel=0.5)
            # ╚> Vectorisation par Potracer
        plist = bm.trace(
            turdsize=2,
            turnpolicy=POTRACE_TURNPOLICY_MINORITY,
            alphamax=1,
            opticurve=False,
            opttolerance=0.2,
        )
            # ╚> Création d'un nouveau fichier SVG
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/Icone {new_podcast.lower()}.svg", "w") as fp:
            # ╚> Écriture des données dans le nouveau fichier
            fp.write(
                f'''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{img.width}" height="{img.height}" viewBox="0 0 {img.width} {img.height}">''')
            parts = []
            for curve in plist:
                fs = curve.start_point
                parts.append(f"M{fs.x},{fs.y}")
                for segment in curve.segments:
                    if segment.is_corner:
                        a = segment.c
                        b = segment.end_point
                        parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
                    else:
                        a = segment.c1
                        b = segment.c2
                        c = segment.end_point
                        parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
                parts.append("z")
            fp.write(f'<path stroke="none" fill="black" fill-rule="evenodd" d="{"".join(parts)}"/>')
            fp.write("</svg>")

            # ╚> Copie du fichier pour le thème sombre
        shutil.copy(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/Icone {new_podcast.lower()}.svg", f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/Icone {new_podcast.lower()} dark.svg")

            # ╚> Changement des couleurs pour le thème sombre
        tree = ET.parse(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/Icone {new_podcast.lower()} dark.svg")
        root = tree.getroot()
        for elem in root.iter():
            if 'fill' in elem.attrib and elem.attrib['fill'].lower() == "black  ".lower():
                elem.attrib['fill'] = "#FBFBFB"
            tree.write(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/Icone {new_podcast.lower()} dark.svg", encoding="utf-8", xml_declaration=True)
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la création/modification de la nouvelle icône", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Icon path" : icon_path})
        return

    try :
        # Ajout du bouton sur la page web de sélection du podcast
            # ╚> Ouverture du fichier HTML
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.html", "r", encoding="utf-8") as f :
            soup = BeautifulSoup(f, "html.parser")

            # ╚> Définition du code HTML pour le bouton
        soup_ajout = f"""
                    <div class="div-bouton-podcast-background">
                        <div class="div-bouton-podcast" onclick="window.location.href='podcasts-{new_podcast.lower().strip().replace(' ', '-')}.html';">
                            <div class="div-contenu-bouton-podcast">
                                <img class="image-bouton-podcast" id="Icone-{new_podcast.lower().strip().replace(' ', '-')}" src="Images/Icone {new_podcast.lower()}.svg" alt="" height="50px">
                                <h2 class="texte-bouton-podcast">{new_podcast}</h2>
                            </div>
                        </div>
                    </div>
    """

            # ╚> Insertion dans le code existant et écriture dans le fichier
        soup.find("div", {"class" : "conteneur-boutons-podcasts"}).insert(0, soup_ajout)
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/podcasts.html", "w", encoding="utf-8") as f :
                f.write(str(soup))
                f.close()
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la création du nouveau podcast", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Filename" : filename, "Nom du podcast" : new_podcast})
        return

def add_category() :
    global scrollable_frame
    global app

    # Création de la liste déroulante
    scrollable_frame = ctk.CTkScrollableFrame(app, width=380, height=200)
    scrollable_frame.pack(pady=10)

    # Ajout des podcasts stockés dans la liste déroulant
    for podcast in noms_chroniques_podcasts :
        item_frame = ctk.CTkFrame(scrollable_frame)
        item_frame.pack(fill="x", pady=2, padx=5)
        item_label = ctk.CTkLabel(item_frame, text=podcast, anchor="w")
        item_label.pack(side="left", padx=5, expand=True, fill="x")
        delete_button = ctk.CTkButton(item_frame, text="Supprimer", command=lambda frame=item_frame: delete_podcast(frame, podcast), width=80)
        delete_button.pack(side="right", padx=5)

    # Création des différents éléments de la fenêtre
    add_podcast_entry = ctk.CTkEntry(app, placeholder_text="Nouveau podcast")
    add_podcast_entry.pack(pady=5)

    icon_button = ctk.CTkButton(app, text="Sélectionner une icône", command=select_icon, width=80)
    icon_button.pack(pady=5)

    delete_button = ctk.CTkButton(app, text="Ajouter le podcast", command=lambda : add_podcast(add_podcast_entry, scrollable_frame), width=80, fg_color="white", text_color="black", hover_color="grey")
    delete_button.pack(pady=5)



def add_episode(category, episode_name, episode_date) :
    global audio_path
    try :
        # Vérification des champs
        if not category or not episode_name or not episode_date or not audio_path :
            Errors.raise_error(app, "Veuillez remplir tous les champs", "GérerPodcasts.py")
            return
        # Vérification du format de la date
        if not (len(episode_date.split("/")) == 3 and
                len(episode_date.split("/")[0]) == 2 and episode_date.split("/")[0].isdigit() and
                len(episode_date.split("/")[1]) == 2 and episode_date.split("/")[1].isdigit() and
                len(episode_date.split("/")[2]) == 2 and episode_date.split("/")[2].isdigit()):
            Errors.raise_error(app, "Format de date invalide ! Format attendu : JJ/MM/AA", "GérerPodcasts.py")
            return
        episode_date = datetime.strptime(episode_date, "%d/%m/%Y")
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la vérification et formatage des informations", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Category" : category, "Episode name" : episode_name, "Episode date" : episode_date})
        return

    try :
        # Ouverture du fichier HTML du podcast
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[category]}", 'r', encoding='utf8') as f :
            soup = BeautifulSoup(f, "html.parser")
        # Récupération du numéro ID du nouvel épisode
            if soup.find("div", {"class": "audio"}) != None :
                max_id_number = 1
                for div in soup.find_all("div", {"class": "audio"}) :
                    id_number = int(div["id"].split("Audio$")[-1]) # Utilisation d'un symbole $ pour séparer les épisodes individuels et ceux des émissions
                    if id_number > max_id_number :
                        max_id_number = id_number
                id_number = max_id_number + 1
            else :
                id_number = 1
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'ouverture du fichier HTML du podcast", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Category" : category, "Podcasts filenames" : noms_chroniques_podcasts, "Episode name" : episode_name, "Episode date" : episode_date})
        return
    # Nouveau code HTML de l'épisode
    html_ajout = f"""
            <div class="div-émission-background">
            <div class="div-émission">
            <div class="infos-émission">
            <h2 class="titre-émission">{episode_name}</h2>
            <h3 class="date-émission">{episode_date}</h3>
            </div>v
            <div class="div-audio-podcasts">
            <audio class="audio" controls="" id="Audio${id_number}">
            <source src="{audio_path}" type="audio/mpeg"/>
                                        Votre navigateur ne supporte pas l'élément audio.
                                    </audio>
            </div>
            </div>
            </div>
    """

    try :
        # Insertion dans le code existant
        soup_ajout = BeautifulSoup(html_ajout, "html.parser")
        dates_émissions = soup.find_all("h3", {"class" : "date-émission"})
            # ╚> Placement de la nouvelle émission dans l'ordre chronologique
        for date in dates_émissions :
            if datetime.strptime(date.text, '%d/%m/%Y') < episode_date :
                soup.find("div", {"class" : "conteneur-émissions"}).insert(dates_émissions.index(date), soup_ajout)
                break
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[category]}", "w", encoding="utf-8") as f :
                f.write(str(soup))
                f.close()
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'ajout de l'épisode", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Category" : category, "Podcasts filenames" : noms_chroniques_podcasts, "Episode name" : episode_name, "Episode date" : episode_date, "Audio path" : audio_path})
        return

def select_audio_file() :
    global audio_path
    try :
        # Demande à l'utilisateur de sélectionner le fichier audio de l'épisode
        audio_path = tk.filedialog.askopenfilename(title="Sélectionner le fichier audio de l'épisode",
                                                filetypes=(("Fichiers MP3", ".mp3"), ("Tous les fichiers", ".*")))
        if audio_path.split(".")[-1] != "mp3" :
                Errors.raise_error(app, "Format de fichier invalide ! Fichier MP3 nécessaire", "GérerPodcasts.py")
                return
        audio_path = audio_path.replace("\\", "/")
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la sélection du fichier audio", "GérerPodcasts.py", mail=True, specific_error=e)

    try :
        shutil.move(audio_path, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Émissions/{os.path.basename(audio_path)[:-4]}")
        audio_path = f"Émissions/{os.path.basename(audio_path)[:-4]}.mp3"
    except shutil.SameFileError :
        pass
    except shutil.Error as e :
        Errors.raise_error(app, "Erreur lors de la copie du fichier audio", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Audio path" : audio_path})
        return

def add_episode_selection() :
    global app

    # Création et affichage des éléments de la fenêtre
    episode_name_entry = ctk.CTkEntry(app, placeholder_text="Nom de l'épisode")
    episode_name_entry.pack(pady=5)
    
    episode_date_entry = ctk.CTkEntry(app, placeholder_text="Date de l'épisode")
    episode_date_entry.pack(pady=5)

    audio_path_selection_button = ctk.CTkButton(app, text="Sélectionner le fichier audio de l'épisode", command=select_audio_file, width=80)
    audio_path_selection_button.pack(pady=5)

    label_podcast = ctk.CTkLabel(app, text="Sélectionner la catégorie de podcasts")
    label_podcast.pack(pady=5)

    dropdown = ctk.CTkOptionMenu(app, values=list(noms_chroniques_podcasts.keys()))
    dropdown.pack(pady=5)

    confirm_button = ctk.CTkButton(app, text="Confirmer", command=lambda: add_episode(dropdown.get(), episode_name_entry.get(), episode_date_entry.get()), width=80, fg_color="white", text_color="black", hover_color="grey")
    confirm_button.pack(pady=5)



def delete_episode(category, episode_name) :
    global app

    try :
        # Ouverture du fichier HTML (page web) du podcast et conversion en objet BeautifulSoup
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[category]}", 'r', encoding='utf8') as f :
            soup = BeautifulSoup(f, "html.parser")

        # Récupération de tous les épisodes
        episodes = soup.find_all("div", {"class": "div-émission-background"})
        # Pour chaque épisode, vérifier si le nom correspond à celui de l'épisode à supprimer
        for episode in episodes :
            if episode.find("h2", {"class": "titre-émission"}).text == episode_name :
                # Suppression du de l'épisode et fin de la boucle
                episode.find_parent("div", class_ = "div-émission-background").decompose()
                break

        # Écriture des modifications dans le fichier HTML
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[category]}", "w", encoding="utf-8") as f :
            f.write(str(soup))
            f.close()
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la suppression de l'épisode", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Category" : category, "Episode name" : episode_name, "Podcasts filenames" : noms_chroniques_podcasts})
        return

def select_episode_to_delete(category) :
    global app

    try :
        # Ouverture du fichier HTML du podcast et conversion en objet BeautifulSoup
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{noms_chroniques_podcasts[category]}", 'r', encoding='utf8') as f :
            soup = BeautifulSoup(f, "html.parser")

        # Récupération de tous les épisodes
        episodes = soup.find_all("div", {"class": "div-émission-background"})
        # Récupération de chaque titre d'épisode et ajout à la liste
        episode_names = [episode.find("h2", {"class": "titre-émission"}).text for episode in episodes]
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la récupération des épisodes", "GérerPodcasts.py", mail=True, specific_error=e, additional_infos={"Category" : category, "Podcasts filenames" : noms_chroniques_podcasts, "Episodes names" : episode_names if 'episode_names' in locals() else "N/A"})
        return

    # Création et affichage de la liste déroulante
    dropdown = ctk.CTkOptionMenu(app, values=episode_names, command=lambda episode_name: select_episode_to_delete(category, episode_name))
    dropdown.pack(pady=5)

def del_episode_selection() :
    global app

    # Création et affichage des éléments de la fenêtre
    label_podcast = ctk.CTkLabel(app, text="Sélectionner la catégorie de podcasts")
    label_podcast.pack(pady=5)

    dropdown = ctk.CTkOptionMenu(app, values=list(noms_chroniques_podcasts.keys()), command=lambda category: select_episode_to_delete(category))
    dropdown.pack(pady=5)



def main() :
    global app

    # Création et affichage des boutons principaux de la fenêtre
    category_button = ctk.CTkButton(app, text="Gérer les catégorie de podcasts", command=add_category, width=80)
    category_button.pack(pady=5)

    add_episode_button = ctk.CTkButton(app, text="Ajouter un épisode de podcasts", command=add_episode_selection, width=80)
    add_episode_button.pack(pady=5)

    del_episode_button = ctk.CTkButton(app, text="Supprimer un épisode de podcasts", command=del_episode_selection, width=80)
    del_episode_button.pack(pady=5)

    # Boucle principale de la fenêtre CustomTkinter
    app.mainloop()