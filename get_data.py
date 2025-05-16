import requests
from bs4 import BeautifulSoup

def connection(kanji):
    errormessages = []
    url1 = f"https://jisho.org/search/{kanji}%20%23kanji"
    url2 = f"https://www.nihongo-pro.com/jp/kanji-pal/kanji/{kanji}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response1 = requests.get(url1, headers=headers)
    response2 = requests.get(url2, headers=headers)

    if response1.status_code != 200:
        errormessages.append("Erreur de connexion sur {url1}. Vérifiez la connexion internet.")
        return [], []
    if response2.status_code != 200:
        errormessages.append("Erreur de connexion sur {url2}. Vérifiez la connexion internet.")
        return [], []

    return response1, response2, errormessages

def get_data(kanji):
    """Reçoit un kanji, recherche la page dans jisho.org et retourne les variables onyomi et kunyomi"""
    response1, response2, errormessages = connection(kanji)

    soup1 = BeautifulSoup(response1.text, "html.parser")
    soup2 = BeautifulSoup(response2.text, "html.parser")

    readings_section = soup1.select_one(".kanji-details__main-readings")
    if not readings_section:
        errormessages.append(f"Le caractère '{kanji}' n'a pas été trouvé...")

    kunyomi = []
    kun_section = soup1.select_one(".kanji-details__main-readings dl.kun_yomi")
    if kun_section:
        kunyomi = [a.get_text() for a in kun_section.select("a")]
        if len(kunyomi)>=4:
            kunyomi = kunyomi[:4]
    onyomi = []
    on_section = soup1.select_one(".kanji-details__main-readings dl.on_yomi")
    if on_section:
        onyomi = [a.get_text() for a in on_section.find_all("a")]

    jlptlevel = ["Ne fait pas partie du JLPT"]
    jlpt_section = soup1.select_one(".jlpt strong")
    if jlpt_section:
        jlptlevel= [jlpt_section.get_text()]
    
    samplewords = []

    for row in soup2.find_all("tr", class_=["sampleWord_row0", "sampleWord_row1"]):
        ruby_div = row.find("div", class_="sampleWord_ruby")   
        meaning = row.find("div", class_="sampleWord_meaning")
        
        if ruby_div and meaning:
            ruby = ruby_div.find("ruby")
            meaning = meaning.text.strip()
            reading_sect = ruby_div.find("rt")
            okurigana = reading_sect.find_parent("ruby").next_sibling
            okurigana = okurigana.strip() if okurigana else ""
            reading = reading_sect.text.strip() + okurigana
            word = "".join(ruby_div.stripped_strings)        
            samplewords.append((word, reading, meaning))

    if len(samplewords) >= 3:
        samplewords = samplewords[:3]

    frequency = ["Inconnu"]
    frequency_section = soup1.select_one(".frequency strong")
    if frequency_section:
        frequency = [frequency_section.get_text()+"/2500"]
    return kunyomi, onyomi, jlptlevel, frequency, samplewords, errormessages

if __name__ == "__main__":
    print("Test")
    samplekanji = "猿"
    kunyomi, onyomi, jlptlevel, frequency, samplewords, errormessages = get_data(samplekanji)
    print("Sample kanji = ", samplekanji) 
    print("onyomi and jlpt level = ", onyomi, jlptlevel)
    print("samplewords = ", samplewords)
    print("Error messages = ", errormessages)
