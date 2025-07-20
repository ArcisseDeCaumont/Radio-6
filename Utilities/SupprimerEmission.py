from bs4 import BeautifulSoup
import tkinter as tk
import customtkinter as ctk
import os
from datetime import datetime

noms_fichiers_podcasts = ["podcasts-chroniques-scientifiques.html", "podcasts-chroniques-touristiques.html", "podcasts-chroniques-culturelles.html", "podcasts-portraits.html"]

app = ctk.CTk()
app.geometry("775x400")
app.title("ModifierSiteWeb")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def delete_program(nom_émission) :
    print(nom_émission)

    with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "r", encoding="utf-8") as f :
        soup = BeautifulSoup(f, "html.parser")
    noms_émissions = soup.find_all("h2", {"class" : "titre-émission"})
    for nom_émission in noms_émissions :
        if nom_émission.text == nom_émission :
            nom_émission.find_parent('div', class_ = "div-émission-background").decompose()
            break

    for fichier_podcast in noms_fichiers_podcasts :
        with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/{fichier_podcast}", "r", encoding="utf-8") as f :
            soup = BeautifulSoup(f, "html.parser")
        dates_podcasts = soup.find_all("h3", {"class" : "date-émission"})
        for date_podcast in dates_podcasts :
            if date_podcast.text.split(" - ")[0] == nom_émission :
                date_podcast.find_parent('div', class_ = "div-émission-background").decompose()
                break

with open(f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/émissions.html", "r", encoding="utf-8") as f :
    soup = BeautifulSoup(f, "html.parser")

émissions = soup.find_all("h2", {"class" : "titre-émission"})
noms_émissions = []
for émission in émissions :
    noms_émissions.append(émission.text)

label_émission_à_supprimer = ctk.CTkLabel(master=app, text="Sélectionnez l'émission à supprimer")
label_émission_à_supprimer.pack(pady=5)

dropdown = ctk.CTkOptionMenu(master=app, values=noms_émissions, command=delete_program)
dropdown.pack(pady=0)

app.mainloop()