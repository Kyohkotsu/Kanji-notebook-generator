from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4


class Kanjiinpdf(str):
    """Configure et génère un pdf"""
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Tsukuhou', 'TsukuhouMincho-Regular.ttf'))
        self.c = canvas.Canvas('kanji.pdf', pagesize=A4)
        self.width, self.height = A4

    def create_kanji_pdf(self, kanji, kunyomi, onyomi, jlptlevel, frequency, samplewords):
        self.c.setFont('Tsukuhou', 100)
        self.c.drawString(50, 720, f'{kanji}')
        self.c.setFont('Tsukuhou', 16)
        self.c.drawString(170, 740, f'訓読み(くんよみ): {'/'.join(kunyomi)}')
        self.c.drawString(170, 720, f'音読み(おんよみ): {'/'.join(onyomi)}')
        self.c.drawString(50, 680, f'JLPTレベル: {''.join(jlptlevel)}')
        self.c.drawString(50, 660, f'頻度(ひんど): {''.join(frequency)}')
        self.c.drawString(50, 600, "言葉(ことば):")
        place = 580
        n = 1
        for word in samplewords:
            line = f"{''.join(word[0])}({''.join(word[1])}): {''.join(word[2])}"
            self.c.drawString(70, place, f"{n}. {line}")
            place -= 20
            n += 1

        try:
            image_url = f'https://kakijun.com/kanjiphoto/worksheet/2/kanji-kakijun-worksheet-2-{hex(ord(kanji))[2:6]}.png'
            self.c.drawImage(image_url, 50, self.height-700, width=510, height=340)
        except IOError:
            pass
        self.c.showPage()

    def savedocument(self):
        self.c.save()

# test
if __name__ == '__main__':
    import os
    print("Test. Création de kanji.pdf en cours...")
    pdf = Kanjiinpdf()
    kanji = '山'
    kunyomi = ['yama']
    onyomi = ['san','zan']
    samplewords =  [('火山', 'かざん', 'volcano'), ('富士山', 'ふじさん','Mount Fuji')]
    jlptlevel = ["N5"]
    frequency = ["400 sur 2500"]
    pdf.create_kanji_pdf(kanji, kunyomi, onyomi, jlptlevel, frequency, samplewords)
    pdf.savedocument()
    print("Test terminé!")
    os.startfile("kanji.pdf")
