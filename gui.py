import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
from generate_pdf import Kanjiinpdf
import os

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

        self.get_reply_button = tk.Button(self.button_frame, bg="skyblue", text="作成", command=self.get_request, cursor="hand2")
        self.get_reply_button.pack(side=tk.LEFT, pady=5)

        self.response_label = tk.Label(self, text="Log: ")
        self.response_label.pack(pady=(5, 0), padx=5, anchor=tk.W)

        self.response_text = scrolledtext.ScrolledText(self, width=50)
        self.response_text.pack(pady=5, padx=5)

    def get_request(self):
        """Convertit le texte saisi en une liste de kanjis. Pour chaque kanji, il émet une requête de recherche."""
        kanji_list = self.kanjiInput_entry.get().strip()
        self.response_text.insert(tk.END, f"Recherche {kanji_list}\n")
        if not kanji_list:
            self.response_text.insert(tk.END, "Erreur, veuillez saisir des kanjis.\n")
            return
        else:
            kanji_list = list(kanji_list)
            pdf = Kanjiinpdf()
            i = 1
            for c in kanji_list:
                kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords = self.get_data(c)
                self.response_text.insert(tk.END, f"{i}. {c}")
                self.response_text.insert(tk.END, f"\n訓読み (Kunyomi): {str(kunyomi)}")
                self.response_text.insert(tk.END, f"\n音読み (Onyomi) : {str(onyomi)} \n")
                image_url = f'https://kakijun.com/kanjiphoto/worksheet/2/kanji-kakijun-worksheet-2-{hex(ord(c))[2:6]}.png'
                pdf.create_kanji_pdf(c, kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords, image_url)
                i += 1
            pdf.savedocument()
            os.startfile("kanji.pdf")



    def get_data(self, kanji):
        """Reçoit un kanji, recherche la page dans jisho.org et retourne les variables onyomi et kunyomi"""
        url = f"https://jisho.org/search/{kanji}%20%23kanji"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            self.response_text.insert(tk.END, "Erreur de connexion. Vérifiez la connexion internet.\n")
            return [], []

        soup = BeautifulSoup(response.text, "html.parser")

        readings_section = soup.select_one(".kanji-details__main-readings")
        if not readings_section:
            self.response_text.insert(tk.END, "***Erreur : Ce kanji n'existe pas***\n")

        kunyomi = []
        kun_section = soup.select_one(".kanji-details__main-readings dl.kun_yomi")
        if kun_section:
            kunyomi = [a.get_text() for a in kun_section.select("a")]

        onyomi = []
        on_section = soup.select_one(".kanji-details__main-readings dl.on_yomi")
        if on_section:
            onyomi = [a.get_text() for a in on_section.find_all("a")]

        jlptlevel = ["Ne fait pas partie du JLPT"]
        jlpt_section = soup.select_one(".jlpt strong")
        if jlpt_section:
            jlptlevel= [jlpt_section.get_text()]

        kunwords = []
        kunwords_section = soup.select_one(".kanji-details__main-readings dl.on_yomi")
        if kunwords_section:
            kunwords = [a.get_text() for a in on_section.find_all("li")]
            if len(kunwords) >= 3:
                kunwords = kunwords[:3]
        
        onwords = []
        onwords_section = soup.select_one(".kanji-details__main-readings dl.on_yomi")
        if onwords_section:
            onwords = [a.get_text() for a in onwords_section.find_all("li")]
            if len(onwords) >= 3:
                onwords = onwords[:3]

        frequency = []
        frequency_section = soup.select_one(".frequency")
        if frequency_section:
            frequency = [frequency_section.get_text()]

        return kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords

