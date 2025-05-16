from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


class Kanjiinpdf(str):
    """Configure et génère un pdf"""
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Tsukuhou', 'TsukuhouMincho-Regular.ttf'))
        self.c = canvas.Canvas('kanji.pdf', pagesize=A4)
        self.width, self.height = A4
    
    def draw_bar(self, frequency):
        try:
            frequency = int(frequency)
        except ValueError:
            frequency = 2500
        x = 150
        y = 659
        width = 100
        height = 12
        max_rank = 2500
        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(0.5)
        self.c.rect(x, y, width, height, stroke=1, fill=0)
        pos = width * (1 - frequency / max_rank)
        pos = max(0, min(width, pos))

        self.c.setFillColor(colors.red)
        self.c.rect(x + pos - 1.5, y, 3, height, fill=1, stroke=0)
        self.c.setFillColor(colors.black)
    
        ratio = frequency / max_rank
        if ratio <= 0.1:
            freq_label = "とてもよく使う"
        elif ratio <= 0.3:
            freq_label = "よく使う"
        elif ratio <= 0.6:
            freq_label = "普通"
        elif ratio <= 0.9:
            freq_label = "ときどき使う"
        else:
            freq_label = "めずらしい"
        self.c.drawString(x + width + 6, y - 1, freq_label)
    

    def create_kanji_pdf(self, kanji, kunyomi, onyomi, jlptlevel, frequency, samplewords):
        self.c.setFont('Tsukuhou', 100)
        self.c.drawString(50, 720, f'{kanji}')
        self.c.setFont('Tsukuhou', 16)
        self.c.drawString(170, 740, f'訓読み(くんよみ): {'/'.join(kunyomi)}')
        self.c.drawString(170, 720, f'音読み(おんよみ): {'/'.join(onyomi)}')
        self.c.drawString(50, 680, f'JLPTレベル: {''.join(jlptlevel)}')
        
        self.c.drawString(50, 660, f'頻度(ひんど):')
        self.draw_bar(''.join(frequency))

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
    frequency = ["400"]
    pdf.create_kanji_pdf(kanji, kunyomi, onyomi, jlptlevel, frequency, samplewords)
    pdf.savedocument()
    print("Test terminé!")
    os.startfile("kanji.pdf")
