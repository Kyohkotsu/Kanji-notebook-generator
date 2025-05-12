import requests
from bs4 import BeautifulSoup

def get_data(kanji):
    """Reçoit un kanji, recherche la page dans jisho.org et retourne les variables onyomi et kunyomi"""
    url = f"https://jisho.org/search/{kanji}%20%23kanji"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    errormessages = []

    if response.status_code != 200:
        errormessages.append("Erreur de connexion. Vérifiez la connexion internet.")
        return [], []

    soup = BeautifulSoup(response.text, "html.parser")

    readings_section = soup.select_one(".kanji-details__main-readings")
    if not readings_section:
        errormessages.append(f"Le caractère '{kanji}' n'a pas été trouvé...")

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
        
    compounds_sections = soup.find_all("div", class_="small-12 large-6 columns")
    onwords = []
    kunwords = []
    for section in compounds_sections:
        header = section.find("h2")
        if not header:
            continue
        title = header.text.strip().lower()
        li = section.find_all("li")
        if "on reading" in title:
            for word in li:
                onwords.append(word.text.strip())
        elif "kun reading" in title:
                kunwords.append(word.text.strip())    
        else:
            continue

    if len(kunwords)>= 3:
        kunwords = kunwords[1:3]
    if len(onwords) >= 3:
        onwords = onwords[1:3]

    frequency = ["Inconnu"]
    frequency_section = soup.select_one(".frequency strong")
    if frequency_section:
        frequency = [frequency_section.get_text()+"/2500"]

    return kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords, errormessages
