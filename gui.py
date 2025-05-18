import tkinter as tk
from tkinter import scrolledtext
from generate_pdf import Kanjiinpdf
import os
from get_data import get_data
import re


class KanjiScrapingApp(tk.Frame):
    """Ce programme fait du scraping web et génère un fichier pdf de pratique de kanji"""
    def __init__(self, master: tk):
        super().__init__(master)
        master.title("漢字スクレイピング")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.kanjiInput_label = tk.Label(self, text="Saisir les kanjis: ")
        self.kanjiInput_label.pack(pady=(5, 0), padx=5, anchor=tk.W)

        self.kanjiInput_entry = tk.Entry(self, width=50)
        self.kanjiInput_entry.pack(pady=5, padx=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.get_reply_button = tk.Button(self.button_frame, bg="skyblue", text="Générer", command=self.get_request, cursor="hand2")
        self.get_reply_button.pack(side=tk.LEFT, pady=5)

        self.response_label = tk.Label(self, text="Log: ")
        self.response_label.pack(pady=(5, 0), padx=5, anchor=tk.W)

        self.response_text = scrolledtext.ScrolledText(self, width=50)
        self.response_text.pack(pady=5, padx=5)

    def clean_data(self, user_input):
        """Elimine  les autres caractères et les kanjis redondants"""
        kanji_list = re.findall(r'[\u4e00-\u9faf]', user_input)
        seen = set()
        seen_add = seen.add
        return [x for x in kanji_list if not (x in seen or seen_add(x))]

    def get_request(self):
        """Convertit le texte saisi en une liste de kanjis. Pour chaque kanji, il émet une requête de recherche."""
        kanji_list = self.clean_data(self.kanjiInput_entry.get().strip())

        if not kanji_list:
            self.response_text.insert(tk.END, "Veuillez saisir une liste de kanjis.\n")
            return
        else:
            self.response_text.insert(tk.END, f"Traitement de {kanji_list}:\n")
            kanji_list = list(kanji_list)
            pdf = Kanjiinpdf()
            pdf.make_title_page(kanji_list)
            i = 1
            for c in kanji_list:
                kunyomi, onyomi, jlptlevel, frequency, samplewords, errormessages = get_data(c)
                self.response_text.insert(tk.END, f"{i}. {c}\n")
                self.response_text.insert(tk.END, f"訓読み (Kunyomi): {str(kunyomi)}\n")
                self.response_text.insert(tk.END, f"音読み (Onyomi) : {str(onyomi)} \n")
                for message in errormessages:
                    self.response_text.insert(tk.END, f"Attention : {message}\n")
                
                pdf.create_kanji_pdf(c, kunyomi, onyomi, jlptlevel, frequency, samplewords)
                self.response_text.insert(tk.END, f"{c} a été ajouté dans le pdf.\n\n")
                i += 1
            
            try:
                pdf.savedocument()
                self.response_text.insert(tk.END, f"\nDocument sauvegardé dans {os.getcwd()}.\n")
                os.startfile("kanji.pdf")
            except PermissionError:
                self.response_text.insert(tk.END, "\033[31mLe fichier pdf est déjà ouvert. Veuillez fermer ce fichier et refaire.\033[0m\n")

