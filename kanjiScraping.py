# from docx import Document
import requests
import tkinter as tk
from bs4 import BeautifulSoup

def jisho_search(kanji):
    url = f"https://jisho.org/search/{kanji}%20%23kanji"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erreur de connexion")
        return [], []

    soup = BeautifulSoup(response.text, "html.parser")

    readings_section = soup.select_one(".kanji-details__main-readings")
    if not readings_section:
        print("***Erreur : Ce kanji n'existe pas***")

    kunyomi = []
    kun_section = soup.select_one(".kanji-details__main-readings dl.kun_yomi")
    if kun_section:
        kunyomi = [a.get_text() for a in kun_section.select("a")]

    onyomi = []
    on_section = soup.select_one(".kanji-details__main-readings dl.on_yomi")
    if on_section:
        onyomi = [a.get_text() for a in on_section.find_all("a")]

    return kunyomi, onyomi

def read_kanji():
    kanji = kanjiEntry.get()
    kanji = list(kanji)
    n = 1
    for c in kanji:
        kunyomi, onyomi = jisho_search(c)
        answerbox.insert(tk.END, f"漢字{n}: {c}\n")
        answerbox.insert(tk.END, f"訓読み (Kunyomi): {kunyomi}\n")
        answerbox.insert(tk.END, f"音読み (Onyomi): {onyomi}\n")
        n += 1

# Créer l'instance fenetre
fenetre = tk.Tk()

# Donner un titre à la fenêtre
fenetre.title("Trouver la prononciation de tes kanjis")

# Configurer dex labels, deux textbox, un bouton de confirmation
entryLabel = tk.Label(fenetre, text="Saisir tes kanjis:")
kanjiEntry = tk.Entry(fenetre)
buttonFrame = tk.Frame(fenetre)
confirmButton = tk.Button(buttonFrame, text="Rechercher", command=read_kanji)
answerLabel = tk.Label(fenetre, text="Saisir tes kanjis:")
answerbox = tk.Entry(fenetre)

# Placer les éléments dans fenetre
entryLabel.pack(anchor=tk.W)
kanjiEntry.pack()
buttonFrame.pack()
confirmButton.pack(pady=5, padx=5)
answerLabel.pack(anchor=tk.W)
answerbox.pack()

# Lancer fenetre
fenetre.mainloop()
