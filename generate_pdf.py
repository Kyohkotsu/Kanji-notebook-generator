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

    def create_kanji_pdf(self, kanji, kunyomi, onyomi, jlptlevel, frequency, kunwords, onwords, image_url):
        self.c.setFont('Tsukuhou', 100)
        self.c.drawString(100, 720, f'{kanji}')
        self.c.setFont('Tsukuhou', 16)
        self.c.drawString(100, 680, f'訓読み: {' / '.join(kunyomi)}')
        self.c.drawString(100, 660, f'音読み: {' / '.join(onyomi)}')
        self.c.drawString(100, 640, f'JLPTレベル: {', '.join(jlptlevel)}')
        self.c.drawString(100, 620, f'頻度: {', '.join(frequency)}')
        self.c.drawString(100, 600, f'訓読みをふくむ言葉: {'; '.join(kunwords)}')
        self.c.drawString(100, 580, f'音読みをふくむ言葉: {'; '.join(onwords)}')

        self.c.drawImage(image_url, 50, self.height-700, width=510, height=340)

        self.c.showPage()

    def savedocument(self):
        try:
            self.c.save()
        except PermissionError:
            print("\033[31mNous n'avons pas pu savegarder le fichier pdf car il est déjà ouvert. Veuillez fermer le fichier actuel et refaire.\033[0m")


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
