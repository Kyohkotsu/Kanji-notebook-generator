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

    def create_kanji_pdf(self, kanji, kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords):
        self.c.setFont('Tsukuhou', 100)
        self.c.drawString(100, 720, f'{kanji}')
        self.c.setFont('Tsukuhou', 16)
        self.c.drawString(220, 740, f'訓読み(Kunyomi): {' / '.join(kunyomi)}')
        self.c.drawString(220, 720, f'音読み(Onyomi): {' / '.join(onyomi)}')
        self.c.drawString(100, 680, f'JLPTレベル: {', '.join(jlptlevel)}')
        self.c.drawString(100, 660, f'頻度(Fréquence): {', '.join(frequency)}')
        self.c.drawString(100, 620, "言葉(Vocabulaire):")
        place = 600
        for word in kunwords:
            self.c.drawString(105, place, f' {word}')
            place -= 20
        for word in onwords:
            self.c.drawString(105, place, f' {word}')
            place -= 20

        try:
            image_url = f'https://kakijun.com/kanjiphoto/worksheet/2/kanji-kakijun-worksheet-2-{hex(ord(kanji))[2:6]}.png'
            self.c.drawImage(image_url, 50, self.height-700, width=510, height=340)
        except IOError:
            pass
        self.c.showPage()

    def savedocument(self):
        self.c.save()


# if __name__ == '__main__':
#     import os
#     print("Test Initié. Création de kanji.pdf en cours...")
#     pdf = Kanjiinpdf()
#     kanji = '山'
#     kunyomi = ['yama']
#     onyomi = ['san','zan']
#     kunwords = []
#     onwords =  ['火山','富士山']
#     jlptlevel = ["N5"]
#     frequency = ["400 sur 2500"]
#     image_url = f'https://kakijun.com/kanjiphoto/worksheet/2/kanji-kakijun-worksheet-2-{hex(ord(kanji))[2:6]}.png'
#     pdf.create_kanji_pdf(kanji, kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords, image_url)
#     pdf.savedocument()
#     print("Test terminé!")
#     os.startfile("kanji.pdf")
