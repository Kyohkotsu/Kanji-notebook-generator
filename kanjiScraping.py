import
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext


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

        self.get_reply_button = tk.Button(self.button_frame, bg="skyblue", text="Rechercher", command=self.get_request, cursor="hand2")
        self.get_reply_button.pack(side=tk.LEFT, pady=5)

        self.response_label = tk.Label(self, text="Log: ")
        self.response_label.pack(pady=(5, 0), padx=5, anchor=tk.W)

        self.response_text = scrolledtext.ScrolledText(self, width=50)
        self.response_text.pack(pady=5, padx=5)

    def get_request(self):
        kanjiList = self.kanjiInput_entry.get().strip()
        self.response_text.insert(tk.END, f"Recherche {kanjiList}\n")
        if not kanjiList:
            self.response_text.insert(tk.END, "Erreur, veuillez saisir des kanjis.\n")
            return
        else:
            kanjiList = list(kanjiList)
            i = 1
            for c in kanjiList:
                kunyomi, onyomi = self.get_readings(c)
                self.response_text.insert(tk.END, f"{i}. {c}")
                self.response_text.insert(tk.END, f"\n訓読み (Kunyomi): {str(kunyomi)}")
                self.response_text.insert(tk.END, f"\n音読み (Onyomi) : {str(onyomi)} \n")
                i += 1

    def get_readings(self, kanji):
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

        return kunyomi, onyomi


if __name__ == "__main__":
    root = tk.Tk()
    fenetre = KanjiScrapingApp(root)
    fenetre.mainloop()

