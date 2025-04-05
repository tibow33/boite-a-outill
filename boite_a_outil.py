import zipfile
import time
import random 
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests #dans invite de commande pip install requests
import cv2 #dans invite de commande pip install opencv-python
from urllib.parse import urlparse

class Application(tk.Tk):
    def __init__(window):
        super().__init__()
        # Personaliser cette fennetre
        window.title("Boîte à Outils Sécurité")
        window.geometry("600x500")
        window.resizable(False, False)
        window.iconbitmap("rickroll.ico")
        window.config(background='#41B77F')

        # Variables
        window.Listecaractere = "abcdef"
        window.lettres = string.ascii_letters
        window.chiffres = string.digits
        window.ponc = string.punctuation
        
        # Menu principal
        window.create_main_menu()
        
    def create_main_menu(window):
        # Nettoyer la fenêtre
        for widget in window.winfo_children():
            widget.destroy()
        
        # Titre
        tk.Label(window, text="BOÎTE À OUTILS SÉCURITÉ", font=("Arial", 16, "bold"),bg='#41B77F',fg='white').pack(pady=20)
        
        # Options du menu
        options = [
            ("1 - Brute Force", window.brute_force),
            ("2 - Attaque Dictionnaire", window.dictionary_attack),
            ("3 - Générateur MDP", window.password_generator),
            ("4 - Cryptage de mot de passe", window.video_player),
            ("5 - Récupération du code HTML", window.html_extractor),
            ("6 - Quitter", window.quit)
        ]
        
        for text, command in options:
            tk.Button(window, text=text, command=command, width=30,bg='#41B77F',fg='white').pack(pady=5)
    
    def brute_force(window):
        # Nettoyer la fenêtre
        for widget in window.winfo_children():
            widget.destroy()
        
        # Retour menu
        tk.Button(window, text="← Retour", command=window.create_main_menu,bg='#41B77F',fg='white').pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(window, text="BRUTE FORCE", font=("Arial", 14),bg='#41B77F',fg='white').pack(pady=10)
        
        tk.Label(window, text="Longueur des combinaisons:",bg='#41B77F',fg='white').pack()
        length_entry = tk.Entry(window)
        length_entry.pack()
        
        tk.Label(window, text="Caractères possibles:",bg='#41B77F',fg='white').pack()
        char_entry = tk.Entry(window)
        char_entry.insert(0, window.Listecaractere)
        char_entry.pack()
        
        result_label = tk.Label(window, text="",bg='#41B77F')
        result_label.pack(pady=10)
        
        def launch_brute_force():
            try:
                x = int(length_entry.get())
                window.Listecaractere = char_entry.get()
                
                datedebut = time.time()
                liste_mots = generer_mot_recursif(x)
                
                fichier = open("datas.txt","w")
                if fichier:
                    for mot in liste_mots:
                        fichier.write(mot + "\n")
                    
                    datefin = time.time()
                    result_label.config(text=f"Terminé! Temps: {datefin-datedebut:.2f}s\nFichier sauvegardé: {fichier}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
        
        tk.Button(window, text="Lancer Brute Force",bg='#41B77F',fg='white', command=launch_brute_force).pack(pady=10)
    
    def dictionary_attack(window):
        # Nettoyer la fenêtre
        for widget in window.winfo_children():
            widget.destroy()
        
        # Retour menu
        tk.Button(window, text="← Retour",bg='#41B77F',fg='white', command=window.create_main_menu).pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(window, text="Attaque par dictionnaire",bg='#41B77F',fg='white', font=("Arial", 14)).pack(pady=10)
        
        liste1 = tk.BooleanVar(value=True)
        liste2 = tk.BooleanVar(value=False)
        tk.Checkbutton(window, text="10k-most-common.txt",bg='#41B77F', width=90, variable=liste1).pack()
        tk.Checkbutton(window, text="french_passwords_20k.txt",bg='#41B77F', width=90, variable=liste2).pack()

        result_label = tk.Label(window, text="",bg='#41B77F')
        result_label.pack(pady=10)
        
        def launch_attack():
            try:
                
                datedebut = time.time()
                dict_files = []
                if liste1.get():
                    dict_files.append("10k-most-common.txt")
                if liste2.get():
                    dict_files.append("french_passwords_20k.txt")
            
                if not dict_files:
                    messagebox.showwarning("Attention", "Aucun dictionnaire sélectionné")
                    return
                
                for dict_file in dict_files:
                    with open(dict_file, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        with zipfile.ZipFile("lo.zip") as fichierZip:
                            for ligne in lines:
                                motdepasse = ligne.strip()
                                try:
                                    fichierZip.extractall("Extract", pwd=bytes(motdepasse, "utf-8"))
                                    datefin = time.time()
                                    result_label.config(text=f"Mot de passe trouvé: {motdepasse}\nTemps: {datefin-datedebut:.2f}s")
                                    return
                                except:
                                    continue
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
        
        tk.Button(window, text="Lancer l'attaque", command=launch_attack).pack(pady=10)
    
    def password_generator(window):
        # Nettoyer la fenêtre
        for widget in window.winfo_children():
            widget.destroy()
        
        # Retour menu
        tk.Button(window, text="← Retour",bg='#41B77F',fg='white', command=window.create_main_menu).pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(window, text="GÉNÉRATEUR DE MOT DE PASSE",bg='#41B77F',fg='white', font=("Arial", 14)).pack(pady=10)
        
        # Cases à cocher
        letters_var = tk.BooleanVar(value=True)
        numbers_var = tk.BooleanVar(value=False)
        symbols_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(window, text="Lettres",bg='#41B77F', variable=letters_var).pack()
        tk.Checkbutton(window, text="Chiffres",bg='#41B77F', variable=numbers_var).pack()
        tk.Checkbutton(window, text="Symboles",bg='#41B77F', variable=symbols_var).pack()
        
        tk.Label(window, text="Longueur:",bg='#41B77F').pack()
        length_entry = tk.Entry(window)
        length_entry.pack()
        
        result_label = tk.Label(window, text="",bg='#41B77F', font=("Arial", 12))
        result_label.pack(pady=10)
        
        def generate_password():
            try:
                l = int(length_entry.get())
                char = ""
                char += window.lettres if letters_var.get() else ""
                char += window.chiffres if numbers_var.get() else ""
                char += window.ponc if symbols_var.get() else ""
                
                if not char:
                    messagebox.showwarning("Attention", "Sélectionnez au moins un type de caractère")
                    return
                
                passe = "".join(random.choices(char, k=l))
                result_label.config(text=f"Mot de passe généré:\n{passe}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
        
        tk.Button(window, text="Générer", command=generate_password).pack(pady=10)
    
    def video_player(window):
        # Nettoyer la fenêtre
        for widget in window.winfo_children():
            widget.destroy()
        
        # Retour menu
        tk.Button(window, text="← Retour",bg='#41B77F',fg='white', command=window.create_main_menu).pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(window, text="Cryptage de mot de passe",bg='#41B77F',fg='white', font=("Arial", 14)).pack(pady=10)

        Symetrique = tk.BooleanVar(value=True)
        Asymetrique = tk.BooleanVar(value=False)
        Hachage = tk.BooleanVar(value=False)

        tk.Checkbutton(window, text="Chiffrement Symétrique",bg='#41B77F', variable=Symetrique).pack()
        tk.Checkbutton(window, text="Chiffrement Asymétrique",bg='#41B77F', variable=Asymetrique).pack()
        tk.Checkbutton(window, text="Hachage",bg='#41B77F', variable=Hachage).pack()
        
        tk.Label(window, text="Entrez un mot pour le Crypter",bg='#41B77F').pack()
        length_entry = tk.Entry(window)
        length_entry.pack()

        def play_video():
            video_path = "ma_video.mp4"
            
            
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                messagebox.showerror("Erreur", "Impossible d'ouvrir la vidéo")
                return
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('Video', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
        
        tk.Button(window, text="Lancer le Cryptage",bg='#41B77F',fg='white', command=play_video).pack(pady=10)
    
    def html_extractor(window):
        # Nettoyer la fenêtre
        for widget in window.winfo_children():
            widget.destroy()
        
        # Retour menu
        tk.Button(window, text="← Retour",bg='#41B77F',fg='white', command=window.create_main_menu).pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(window, text="RÉCUPÉRATION HTML",bg='#41B77F',fg='white', font=("Arial", 14)).pack(pady=10)
        
        tk.Label(window, text="URL du site (exemple:https://www.youtube.com/):",bg='#41B77F',fg='white',).pack()
        url_entry = tk.Entry(window, width=40)
        url_entry.pack()
        
        result_label = tk.Label(window, text="",bg='#41B77F')
        result_label.pack(pady=10)
        
        def extract_html():
            try:
                url = url_entry.get().strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                parsed = urlparse(url)
                if not all([parsed.scheme, parsed.netloc]):
                    messagebox.showerror("Erreur", "URL invalide")
                    return
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                datedebut = time.time()
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                
                with open("codehtml.txt", "w", encoding="utf-8") as fichier:
                        fichier.write(response.text)
                    
                datefin = time.time()
                result_label.config(text=f"HTML sauvegardé dans:\n{fichier}\nTemps: {datefin-datedebut:.2f}s")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
        
        tk.Button(window, text="Récupérer HTML", command=extract_html).pack(pady=10)

def generer_mot_recursif(x, prefixe="", Listecaractere="abcdef"):
    if x == 0:
        return [prefixe]
    mots = []
    for caractere in Listecaractere:
        mots += generer_mot_recursif(x-1, prefixe+caractere, Listecaractere)
    return mots

if __name__ == "__main__":
    app = Application()
    app.mainloop()