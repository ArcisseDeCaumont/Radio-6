#  »»» ModifierInfos.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import tkinter as tk
import customtkinter as ctk
from bs4 import BeautifulSoup
import os
import shutil
import WebsiteManager
import SupprimerEmission
import Errors

# Création de la fenêtre CustomTkinter
app = ctk.CTk()
app.geometry("775x420")
app.title("EditCalendar")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Définition des variables
label_info1 = ""
label_info2 = ""
bouton_confirmer1 = ""
soup_accueil_sauvegarde = ""
soup_a_propos_sauvegarde = ""

def commit():
    global soup_accueil_sauvegarde
    global soup_a_propos_sauvegarde
    # Vérifie comment s'est passé la synchronisation avec GitHub
    if WebsiteManager.commit_changes(app) == "error" :
        try :
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/index.html", 'r', encoding='utf8') as f :
                f.write(str(soup_accueil_sauvegarde))
            with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/a-propos.html", 'r', encoding='utf8') as f :
                f.write(str(soup_a_propos_sauvegarde))
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de la synchronisation puis restauration des fichiers HTML", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"State" : "Failed to restore HTML files after GitHub commit error"})
    else :
        WebsiteManager.finish_window(app)

def changer_image(image_id, path):
    # Demande à l'utilisateur de choisir l'image
    new_image = tk.filedialog.askopenfilename(title="Sélectionnez la nouvelle image",
                                                        filetypes=(("Fichiers PNG", ".png"), ("Fichiers JPG", ".jpg"), ("Tous les fichiers", ".*")))
    if new_image.split(".")[-1] != "png" and new_image.split(".")[-1] != "jpg" :
            Errors.raise_error(app, "Format de fichier invalide ! Fichier PNG ou JPG nécessaires", "AjouterÉmission.py")
            return
    # Vérification du format de l'image
    try :
        shutil.move(new_image, f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/")
    except shutil.SameFileError :
        try :
            # Si le fichier est déjà présent dans la destination, on le supprime et le remplace par le nouveau fichier
            os.remove(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/{os.path.basename(new_image)}")
            shutil.move(new_image, f"C:/Users/{os.getlogin()}/Documents/Git Hub/Radio-6/Images/")
        except Exception as e :
            Errors.raise_error(app, "Erreur lors de la copie de l'image", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Image path" : new_image})
            return
    except shutil.Error :
        Errors.raise_error(app, "Erreur lors de la copie de l'image", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Image path" : new_image})
        return

    try :
        # Ouverture du fichier HTML (page Web) et conversion en objet BeautifulSoup
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{image_id[0]}.html", 'r', encoding='utf8') as f :
            soup = BeautifulSoup(f, "html.parser")

        # Changement du chemin ("src") de l'image sélectionnée
        soup.find_all("img", {"class" : "images-accueil"})[image_id[1]]['src'] = f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/Images/{os.path.basename(new_image)}"

        # Ouverture du fichier HTML et écriture
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{image_id[0]}.html", 'r', encoding='utf8') as f :
            f.write(soup.prettify())
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la modification du fichier page web", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Image path" : new_image, "Image ID" : image_id})
        return

def demander_images():
    # Suppression des éléments de la fenêtre
    global app
    global label_info1
    global label_info2
    global bouton_confirmer1
    label_info1.destroy()
    label_info2.destroy()
    bouton_confirmer1.destroy()

    try :
        # Ouverture des fichiers HTMLs (pages web) et conversion en objets BeautifulSoup
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/index.html", 'r', encoding='utf8') as f :
            soup = BeautifulSoup(f, "html.parser")
        # Récupération des chemins des images de la page web
        images_accueil = []
        for image in soup.find_all("img", {"class" : "images-accueil"}) :
            images_accueil.append(image.get('src'))
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/a-propos.html", 'r', encoding='utf8') as f :
            soup = BeautifulSoup(f, "html.parser")
        images_a_propos = []
        for image in soup.find_all("img", {"class" : "images-accueil"}) :
            images_a_propos.append(image.get('src'))
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la récupération des images", "ModifierInfos.py", mail=True, specific_error=e)

    # Création et affichage des éléments sur la fenêtre
    label_accueil = ctk.CTkLabel(master=app, text=f"Accueil", width=165)
    label_accueil.pack(pady=0)

    label_image1 = ctk.CTkLabel(master=app, text=f"Image 1 : {images_accueil[0]}", width=165)
    label_image1.pack(pady=0)
    bouton_changer1 = ctk.CTkButton(master=app, text="Changer", command=lambda: changer_image(["index", 0], images_accueil[0]))
    bouton_changer1.pack(pady=0)

    label_image2 = ctk.CTkLabel(master=app, text=f"Image 2 : {images_accueil[1]}", width=165)
    label_image2.pack(pady=0)
    bouton_changer2 = ctk.CTkButton(master=app, text="Changer", command=lambda: changer_image(["index", 1], images_accueil[1]))
    bouton_changer2.pack(pady=0)

    label_image3 = ctk.CTkLabel(master=app, text=f"Image 3 : {images_accueil[2]}", width=165)
    label_image3.pack(pady=0)
    bouton_changer3 = ctk.CTkButton(master=app, text="Changer", command=lambda: changer_image(["index", 2], images_accueil[2]))
    bouton_changer3.pack(pady=0)

    label_a_propos = ctk.CTkLabel(master=app, text=f"À propos", width=165)
    label_a_propos.pack(pady=5)

    label_image4 = ctk.CTkLabel(master=app, text=f"Image 1 : {images_a_propos[0]}", width=165)
    label_image4.pack(pady=0)
    bouton_changer4 = ctk.CTkButton(master=app, text="Changer", command=lambda: changer_image(["a-propos", 0], images_a_propos[0]))
    bouton_changer4.pack(pady=0)

    label_image5 = ctk.CTkLabel(master=app, text=f"Image 2 : {images_a_propos[1]}", width=165)
    label_image5.pack(pady=0)
    bouton_changer5 = ctk.CTkButton(master=app, text="Changer", command=lambda: changer_image(["a-propos", 1], images_a_propos[1]))
    bouton_changer5.pack(pady=0)

    label_image6 = ctk.CTkLabel(master=app, text=f"Image 3 : {images_a_propos[2]}", width=165)
    label_image6.pack(pady=0)
    bouton_changer6 = ctk.CTkButton(master=app, text="Changer", command=lambda: changer_image(["a-propos", 2], images_a_propos[2]))
    bouton_changer6.pack(pady=0)

    bouton_validation = ctk.CTkButton(master=app, text="Valider", command=commit(), fg_color="white", text_color="black", hover_color="grey")
    bouton_validation.pack(pady=10)

def lire_txt():
    global app
    try :
        # Ouverture du fichier txt
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/ModifierInfos.txt", 'r', encoding='utf8') as f :
            # Chargement du contenu du fichier en remplaçant les "*" par la mise en forme de soulignage
            content = f.read().replace(' *', '<a href="#" class="underlined">').replace('* ', '</a>')
            if content[-1] == "\n" :
                content = content[:-1]
            if content[-1] == "\n" :
                content = content[:-1]

            # Vérification de la mise en forme du fichier infos
            if content.count("\n\n\n\n") != 1 :
                Errors.raise_error(app, "Le fichier ModifierInfos.txt doit contenir 2 sections séparées par 4 sauts de ligne", "ModifierInfos.py")
                return

        # Transformation du contenu txt en éléments HTML
        html_accueil = ""
        for div_accueil in content.split("\n\n\n\n")[0].split("\n\n")[1:] :
            html_accueil += """<div class="div-accueil-background">
                <div class="div-accueil">"""
            titre = div_accueil.split("\n")[0]
            html_accueil += f"""<h2 class="titre-accueil">{titre}</h2>"""
            for ajout_contenu in div_accueil.split("\n")[1:] :
                html_accueil += f"""<h3 class="contenu-accueil">{ajout_contenu}</h3>"""
            html_accueil += """</div>
            </div>"""

        html_a_propos = ""
        for div_accueil in content.split("\n\n\n\n")[1].split("\n\n")[1:] :
            html_a_propos += """<div class="div-accueil-background">
                <div class="div-accueil">"""
            titre = div_accueil.split("\n")[0]
            html_a_propos += f"""<h2 class="titre-accueil">{titre}</h2>"""
            for ajout_contenu in div_accueil.split("\n")[1:] :
                html_a_propos += f"""<h3 class="contenu-accueil">{ajout_contenu}</h3>"""
            html_a_propos += """</div>
            </div>"""
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la lecture du fichier txtx", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Contenu txt" : content})

    try :
        # Ouverture des fichiers HTML et écriture du contenu
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/index.html", 'r', encoding='utf8') as f :
            soup_accueil = BeautifulSoup(f, "html.parser")
            soup_accueil_sauvegarde = soup_accueil
            # ╚> Suppression du contenu précédent
        for div_accueil in soup_accueil.find_all("div", {"class" : "div-accueil-background"})[2:] :
            div_accueil.decompose()
            # ╚> Remplacement par le nouveau contenu
        soup_ajout_accueil = BeautifulSoup(html_accueil, "html.parser")
        soup_accueil.find("div", {"class" : "conteneur"}).insert(4, soup_ajout_accueil)
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/index.html", 'w', encoding='utf8') as f :
            f.write(str(soup_accueil))
            f.close()

        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/a-propos.html", 'r', encoding='utf8') as f :
            soup_a_propos = BeautifulSoup(f, "html.parser")
            soup_a_propos_sauvegarde = soup_a_propos
        for div_accueil in soup_a_propos.find_all("div", {"class" : "div-accueil-background"}) :
            div_accueil.decompose()
        soup_ajout_a_propos = BeautifulSoup(html_a_propos, "html.parser")
        soup_a_propos.find("div", {"class" : "conteneur"}).insert(5, soup_ajout_a_propos)
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/a-propos.html", 'w', encoding='utf8') as f :
            f.write(str(soup_a_propos))
            f.close
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'écriture des nouvelles informations", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Contenu txt" : content})

    demander_images()

def écrire_txt():
    global app
    try :
        content = "Accueil :\n\n"
        # Ouverture des fichiers HTML et récupération du contenu
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/index.html", 'r', encoding='utf8') as f :
            soup_accueil = BeautifulSoup(f, "html.parser")
        for div_accueil in soup_accueil.find_all("div", {"class" : "div-accueil"})[2:] :
            content += div_accueil.find("h2", {"class" : "titre-accueil"}).text + "\n"
            for contenu in div_accueil.find_all("h3", {"class" : "contenu-accueil"}) :
                content += contenu.text + "\n"
            content += "\n"
        
        content += "\n\nÀ propos :\n\n"
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/a-propos.html", 'r', encoding='utf8') as f :
            soup_a_propos = BeautifulSoup(f, "html.parser")
        for div_accueil in soup_a_propos.find_all("div", {"class" : "div-accueil"}) :
            content += div_accueil.find("h2", {"class" : "titre-accueil"}).text + "\n"
            for contenu in div_accueil.find_all("h3", {"class" : "contenu-accueil"}) :
                content += contenu.text + "\n"
            content += "\n"
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la récupération des informations depuis le fichier HTML", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Contenu txt" : content})

    try :
        # Ouverture/création du fichier txt et écriture des informations
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/ModifierInfos.txt", 'w', encoding='utf8') as f :
            f.write(content.replace('<a href="#" class="underlined">', ' *').replace('</a>', '* '))
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de l'écriture des données dans le fichier txt'", "ModifierInfos.py", mail=True, specific_error=e, additional_infos={"Contenu txt" : content})

    print(content)

def main() :
    global label_info1
    global label_info2
    global bouton_confirmer1
    écrire_txt()
    # Création et affichage des éléments dans la fenêtre
    label_info1 = ctk.CTkLabel(master=app, text=f"Vous pouvez modifier les infos dans le fichier ModifierInfos.txt", width=165)
    label_info1.pack(pady=5)
    label_info2 = ctk.CTkLabel(master=app, text=f"(Documents/GitHub/Radio-6/ModifierInfos.txt)", width=165)
    label_info2.pack(pady=0)

    bouton_confirmer1 = ctk.CTkButton(master=app, text="C'est fait !", command=lire_txt)
    bouton_confirmer1.pack(pady=5)

    try :
        # Ouverture du fichier txt dans le bloc-notes
        os.startfile(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/ModifierInfos.txt")
    except Exception as e :
        pass

    app.mainloop()

main()