import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from generate_pdf import Kanjiinpdf
import os
from get_data import get_data, sort_data
import re


class KanjiScrapingApp(tk.Frame):
    """Ce programme fait du scraping web et génère un fichier pdf de pratique de kanji"""
    def __init__(self, master: tk):
        super().__init__(master)
        master.title("漢字スクレイピング")
        master.iconbitmap("./manabu_transparent.ico")
        master.geometry("420x360")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.fileName_label = tk.Label(self, text="Nom du fichier: ")
        self.fileName_label.pack(pady=(5, 0), padx=5, anchor=tk.W)
        self.ligne2 = tk.Frame(self)
        self.ligne2.pack(anchor=tk.W)
        self.fileName_entry = tk.Entry(self.ligne2, width=40)
        self.fileName_entry.pack(pady=5, padx=5, side=tk.LEFT)
        ToolTip(self.fileName_entry, 'Champ optionnel')
        self.dotpdf_label = tk.Label(self.ligne2, text=".pdf")
        self.dotpdf_label.pack(pady=(5, 0), anchor=tk.W, side=tk.RIGHT)

        self.kanjiDescription_label = tk.Label(self, text="Description: ")
        self.kanjiDescription_label.pack(pady=(5, 0), padx=5, anchor=tk.W)
        self.kanjiDescription_entry = tk.Entry(self, width=50)
        self.kanjiDescription_entry.pack(pady=5, padx=5, anchor=tk.W)
        ToolTip(self.kanjiDescription_entry, 'Champ optionnel. Entrez une description pour la liste de kanji qui figurera sur la page titre du fichier pdf.\ni.e. "Kanjis de niveau JLPT N5"')

        self.kanjiInput_label = tk.Label(self, text="Saisir les kanjis: ")
        self.kanjiInput_label.pack(pady=(5, 0), padx=5, anchor=tk.W)
        self.kanjiInput_entry = scrolledtext.ScrolledText(self, width=50, height=11)
        self.kanjiInput_entry.pack(pady=5, padx=5, anchor=tk.W)
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.get_reply_button = tk.Button(self.button_frame, bg="skyblue", text="Générer", command=self.get_request, cursor="hand2")
        self.get_reply_button.pack(side=tk.LEFT, pady=5)
        self.sort_button = tk.Button(self.button_frame, text="Classer par radical", command=self.sort_kanji, cursor="hand2")
        self.sort_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.clear_button = tk.Button(self.button_frame, text="Effacer", command=self.clear_entry, cursor="hand2")
        self.clear_button.pack(side=tk.LEFT, pady=5)

    def clean_data(self, user_input):
        """Elimine  les autres caractères et les kanjis redondants"""
        kanji_list = re.findall(r'[\u4e00-\u9faf]', user_input)
        seen = set()
        seen_add = seen.add
        return [x for x in kanji_list if not (x in seen or seen_add(x))]

    def clear_entry(self):
        self.kanjiInput_entry.delete('1.0', tk.END)

    def sort_kanji(self):
        kanji_list = self.clean_data(self.kanjiInput_entry.get('1.0',tk.END).strip())
        if not kanji_list:
            messagebox.showerror("Erreur", "Veuillez entrer un kanji.")
            return
        sorted_kanji_list = sort_data(kanji_list)
        self.kanjiInput_entry.delete('1.0', tk.END)
        for kanji in dict(sorted_kanji_list).items():
            self.kanjiInput_entry.insert(tk.END, kanji)
            self.kanjiInput_entry.insert(tk.END, "\n")

    def get_request(self):
        """Convertit le texte saisi en une liste de kanjis. Pour chaque kanji, il émet une requête de recherche."""        
        kanji_list = self.clean_data(self.kanjiInput_entry.get('1.0',tk.END).strip())
        if not kanji_list:
            messagebox.showerror("Erreur", "Veuillez entrer un kanji.")
            return
        self.kanjiInput_entry.delete('1.0', tk.END)
        self.kanjiInput_entry.insert(tk.END, f"Traitement de: \n{', '.join(kanji_list)}\n")
        nomFichier = self.fileName_entry.get().strip()

        if len(kanji_list)>=10:
            if action(self, kanji_list) == False:
                return
        
        # Vérifier si le fichier est déjà ouvert et si le nom est valide
        if not nomFichier:
            nomFichier="kanji"
        try:
            pdf = Kanjiinpdf(nomFichier)
            pdf.savedocument()
        except PermissionError:
            messagebox.showwarning('Fichier inaccessible', f"Le fichier {nomFichier}.pdf est déjà ouvert. Veuillez fermer ce fichier et refaire.")
            return
        except FileNotFoundError:
            messagebox.showwarning('Fichier inaccessible', f"Vérifiez si ce nom du fichier est valide dans votre OS.")
            return

        pdf = Kanjiinpdf(nomFichier)
        pdf.make_title_page(kanji_list,self.kanjiDescription_entry.get().strip())
        i = 1
        for kanji in kanji_list:
            try:
                translation, kunyomi, onyomi, jlptlevel, frequency, samplewords = get_data(kanji)
            
            except Exception as e:
                print(e)
                messagebox.showerror('Erreur', f'Erreur de traitement survenue avec le kanji {kanji} :\n {str(e)}')
                
            pdf.create_kanji_pdf(kanji, translation, kunyomi, onyomi, jlptlevel, frequency, samplewords)
            i += 1
        
        pdf.savedocument()
        messagebox.showinfo('Terminé', f"Document sauvegardé dans {os.getcwd()}\n")
        os.startfile(f"{nomFichier}.pdf")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Pas de bordure/fenêtre
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="lightyellow",
                         relief="solid", borderwidth=1,
                         font=("Arial", 10))
        label.pack(ipadx=5, ipady=2)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def boite_confirmation(parent, message):
    # Crée une fenêtre secondaire modale
    confirmation = tk.Toplevel(parent)
    confirmation.title("Cette action peut nécessiter du temps")
    confirmation.iconbitmap("./Timer-alert.ico")
    confirmation.transient(parent)
    confirmation.grab_set()  # Rend la fenêtre modale

    resultat = {"valeur": None}  # Dictionnaire pour stocker le choix

    # Message
    label = tk.Label(confirmation, text=message, padx=20, pady=10)
    label.pack()

    def proceder():
        resultat["valeur"] = True
        confirmation.destroy()

    def annuler():
        resultat["valeur"] = False
        confirmation.destroy()
        

    # Boutons personnalisés
    bouton_proc = tk.Button(confirmation, text="Procéder", command=proceder)
    bouton_annul = tk.Button(confirmation, text="Annuler", command=annuler)

    bouton_proc.pack(side="left", padx=20, pady=10)
    bouton_annul.pack(side="right", padx=20, pady=10)
    parent.wait_window(confirmation)

    return resultat["valeur"]

def action(self, kanji_list):
    resultat = boite_confirmation(self, f"La recherche peut nécessiter jusqu'à {len(kanji_list)*1.2} secondes. \nVoulez-vous continuer?")
    return resultat

if __name__ == "__main__":
    kanjiList = ["水", "火", "木", "金"]  # Exemple
    root = tk.Tk()
    tk.Button(root, text="Lancer une action", command=lambda:action(kanjiList)).pack(padx=20, pady=20)
    root.mainloop()
