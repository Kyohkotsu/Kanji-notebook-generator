# from docx import Document
import requests
from bs4 import BeautifulSoup

def get_readings(kanji):
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


kanji = input("Saisir les kanjis：\n")
kanji = list(kanji)

for c in kanji:
    kunyomi, onyomi = get_readings(c)
    print(c)
    print("訓読み (Kunyomi):", kunyomi)
    print("音読み (Onyomi) :", onyomi)

