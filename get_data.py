import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from io import BytesIO

def connection(kanji):
    errormessages = []
    url = f"https://www.nihongo-pro.com/jp/kanji-pal/kanji/{kanji}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        errormessages.append("Erreur de connexion sur {url}. Vérifiez la connexion internet.")
        return [], []

    return response, errormessages

def get_data(kanji):
    """Reçoit un kanji, recherche la page dans jisho.org et retourne les variables onyomi et kunyomi"""
    response, errormessages = connection(kanji)

    soup = BeautifulSoup(response.text, "html.parser")

    kunyomi = []
    onyomi = []

    for table in soup.select("div.readingsTableDiv > table"):
        label_div = table.find("div", class_="kanji_readingsLabel")
        if label_div:
            reading_type = label_div.text.strip()
            values = table.find_all("div", class_="readingsValue")
            readings = [val.text.strip() for val in values]
            if "訓読み" in reading_type:
                kunyomi.extend(readings)
            elif "音読み" in reading_type:
                onyomi.extend(readings)

    # Réduire le nombre de kun-yomi à retenir pour ne pas dépasser dans la marge du pdf
    if len(kunyomi)>=4:
        kunyomi = kunyomi[:4]

    jlptlevel = ["Ne fait pas partie du JLPT"]
    frequency = "不明/Inconnu"

    for row in soup.select("table.infoTable tr"):
        label = row.find("div", class_="label")
        value = row.find("div", class_="value")

        if label and value:
            label_text = label.text.strip()

            # JLPT
            if "JLPT" in label_text:
                jlpt_match = re.search(r"N\d", value.text)
                if jlpt_match:
                    jlptlevel = jlpt_match.group()

            # Fréquence
            if "使用頻度" in label_text:
                freq_match = re.search(r"約\s*(\d+)\s*字", value.text)
                if freq_match:
                    frequency = freq_match.group(1)
                # exception avec 日 (frequency_value = "書き言葉に用いられる最も一般的な漢字です。")
                if kanji == "日":
                    frequency = "1"


    samplewords = []
    for row in soup.find_all("tr", class_=["sampleWord_row0", "sampleWord_row1"]):
        ruby = row.find("div", class_="sampleWord_ruby")   
        meaning = row.find("div", class_="sampleWord_meaning")
        
        if ruby and meaning:
            meaning = meaning.text.strip()
            reading_sect = ruby.find("rt")
            okurigana = reading_sect.find_parent("ruby").next_sibling
            okurigana = okurigana.strip() if okurigana else ""
            reading = reading_sect.text.strip() + okurigana
            word = "".join(ruby.stripped_strings)        
            samplewords.append((word, reading, meaning))

    if len(samplewords) >= 3:
        samplewords = samplewords[:3]

    return kunyomi, onyomi, jlptlevel, frequency, samplewords, errormessages

def define_image(kanji):
    """Returns image url and its width & height"""
    # old f'https://kakijun.com/kanjiphoto/worksheet/2/kanji-kakijun-worksheet-2-{hex(ord(kanji))[2:6]}.png'
    img_url = f'https://www.writechinese.com/assets/strokeorder/stroke/ja/{ord(kanji)}.png'
    try:
        response = requests.get(img_url)
        response.raise_for_status()
    except Exception as e:
        img_url = f'https://kakijun.com/kanjiphoto/frame/kanji-kakijun-kakusu-{hex(ord(kanji))[2:6]}.png'
        response = requests.get(img_url)
        response.raise_for_status()
        print(kanji, e)
    image = Image.open(BytesIO(response.content))
    width, height = image.size
        
    return img_url, width, height

# test
if __name__ == "__main__":
    print("Test")
    samplekanji = "鬱"
    kunyomi, onyomi, jlptlevel, frequency, samplewords, errormessages = get_data(samplekanji)
    print("Sample kanji = ", samplekanji) 
    print("onyomi = ", onyomi, " jlpt level = ", jlptlevel, " frequency = ", frequency)
    print("samplewords = ", samplewords)
    print("Error messages = ", errormessages)
    img_url, width, height = define_image(samplekanji)
    print(width, height)
