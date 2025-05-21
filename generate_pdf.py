from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import get_data


class Kanjiinpdf(str):
    """Configure et génère un pdf"""
    def __init__(self, nomFichier):
        pdfmetrics.registerFont(TTFont('Noto', 'NotoSansJP-VF.ttf'))
        pdfmetrics.registerFont(TTFont('Kyokasho', 'HGRKK.TTC'))
        self.c = canvas.Canvas(f'{nomFichier}.pdf', pagesize=A4)
        self.width, self.height = A4
        self.page = 0

    def show_page_with_grid(self, kanji, translation, kunyomi, onyomi, jlptlevel, frequency, samplewords):
        """Guide pour le design"""
        self.c.setStrokeColor(colors.blue)
        self.c.setFillColor(colors.blue)

        self.c.setLineWidth(0.3)
        self.c.setFont('Noto',5)
        for a in range(1,40):
            for b in range(1,40):
                self.c.line(a*25,b*25, a*25, 0)
                self.c.line(0,b*25, a*25, b*25)
                if a%2==0:
                    self.c.drawString(a*25,835,str(a*25))
                if b%2==0:
                    self.c.drawString(0,b*25,str(b*25))
        self.create_kanji_pdf(kanji, translation, kunyomi, onyomi, jlptlevel, frequency, samplewords)

    def draw_rectangle(self,X1,Y1,X2,Y2):
        """Dessine un rectangle de coordonnées A(X1,Y1), B(X2,Y1), C(X2,Y2), D(X1,Y2)"""
        self.c.line(X1,Y1,X2,Y1)
        self.c.line(X1,Y2,X2,Y2)
        self.c.line(X1,Y2,X1,Y1)
        self.c.line(X2,Y2,X2,Y1)

    def draw_arrow(self,X1,Y1,X2,Y2):
        """Dessine une flèche des points A(X1,Y1) à B(X2,Y2)"""
        self.c.line(X1,Y1,X2,Y2)
        self.c.line(X2-7,Y2+5,X2,Y2)
        self.c.line(X2-7,Y2-5,X2,Y2)

    def draw_bar(self, frequency):
        """Représente graphiquement la fréquence d'utilisation du kanji"""
        try:
            frequency = int(frequency)
        except ValueError:
            frequency = 2500
        x = 150
        y = 619
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

        self.c.setFont('Noto', 12)
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
        self.c.drawString(x + width + 4, y + 2, freq_label)

    def make_title_page(self,kanji_list):
        """Crée une page titre : avec le titre, l'index, un guide d'utilisation et les crédits"""
        self.c.setStrokeColor(colors.black)
        self.c.setFillColor(colors.black)
        self.c.setLineWidth(1)
        self.c.setFillAlpha(1)
        self.c.setFont('Kyokasho', 100)
        self.c.drawString(50, 725, '漢字ノート') 
        self.c.setFont('Noto', 15)

        kanji_count = len(kanji_list)
        if kanji_count <= 104:
            self.c.drawString(50, 690, "Ce cahier contient les kanjis suivant:")
            i = 1
            j = 1
            n = 1
            for k in kanji_list:
                    self.c.drawString(10+i*45, 690-j*20, f'{n}.'+''.join(k))
                    i+=1
                    if n%10 == 0:
                        j+=1
                        i=1
                    n+=1
        else:
            self.c.drawString(50, 690, f"Ce cahier contient {len(kanji_list)} kanjis [{''.join(kanji_list[0])} à {''.join(kanji_list[kanji_count-1])}]")

        imageX = 270
        imageY = 50
        self.c.drawImage('samplekanji.png', imageX, imageY, width=280, height=400)
        # encadrement: lignes horizontales
        self.c.line(imageX,imageY,imageX+280,imageY)
        self.c.line(imageX,imageY+400,imageX+280,imageY+400)
        # lignes verticales
        self.c.line(imageX,imageY,imageX,imageY+400)
        self.c.line(imageX+280,imageY,imageX+280,imageY+400)
                
        # légende sur l'image
        self.c.setFont('Noto', 12)
        self.c.setFillColor(colors.brown)
        self.c.setStrokeColor(colors.brown)

        self.c.drawString(imageX-175, imageY+340, "kunyomi (lecture usuelle)")
        self.c.drawString(imageX-175, imageY+327, "onyomi (lecture 'chinoise')")
        self.draw_arrow(imageX-30,imageY+330,imageX+19,imageY+330)
        self.draw_rectangle(imageX+20,imageY+340,imageX+100,imageY+320)

        self.c.drawString(imageX-235, imageY+297, "Niveau JLPT et fréquence d'utilisation")
        self.draw_arrow(imageX-30,imageY+300,imageX+19,imageY+300)
        self.draw_rectangle(imageX+20,imageY+313,imageX+165,imageY+290)

        self.c.drawString(imageX-95, imageY+257, "Vocabulaire")
        self.draw_arrow(imageX-30,imageY+260,imageX+19,imageY+260)
        self.draw_rectangle(imageX+20,imageY+285,imageX+183,imageY+240)

        self.c.drawString(imageX-115, imageY+197, "Ordre des traits")
        self.draw_arrow(imageX-30,imageY+200,imageX+19,imageY+200)
        self.draw_rectangle(imageX+20,imageY+235,imageX+120,imageY+165)

        self.c.drawString(imageX-130, imageY+137, "Pratiquer l'écriture")
        self.draw_arrow(imageX-30,imageY+140,imageX+161,imageY+140)
        self.draw_rectangle(imageX+162,imageY+18,imageX+265,imageY+215)

        # crédits
        self.c.setFont('Noto', 10)
        self.c.setFillColor(colors.gray)
        self.c.drawString(50, 120, "Réservé à un usage éducatif et personnel.")
        self.c.drawString(50, 100, "Sources d'informations et d'images :")
        self.c.drawString(60, 80, "-www.nihongo-pro.com")
        self.c.drawString(60, 60, "-www.writechinese.com")
        self.c.drawString(60, 40, "-kakijun.com")

        # saut de page
        self.c.showPage()
    
    def create_kanji_pdf(self, kanji, translation, kunyomi, onyomi, jlptlevel, frequency, samplewords):
        """Dessine une page de kanji"""
        self.c.setStrokeColor(colors.black)
        self.c.setFillColor(colors.black)
        self.c.setLineWidth(1)
        self.c.setFillAlpha(1)
        self.c.setFont('Kyokasho', 100)
        self.c.drawString(50, 725, f'{kanji}')
        self.c.setFont('Noto', 16)
        self.c.drawString(150, 725, translation)
        self.c.drawString(50, 700, f'訓読み(くんよみ): {'/'.join(kunyomi)}')
        self.c.drawString(50, 680, f'音読み(おんよみ): {'/'.join(onyomi)}')

        self.c.drawString(50, 640, f'JLPTレベル :  {''.join(jlptlevel)}')
        self.c.drawString(50, 620, f'頻度(ひんど):')
        self.draw_bar(''.join(frequency))
        self.c.setFont('Noto', 16)

        self.c.drawString(50, 580, "言葉(ことば):")
        place = 560
        n = 1
        for word in samplewords:
            line = f"{''.join(word[0])}({''.join(word[1])}) - {''.join(word[2])}"
            self.c.drawString(70, place, f"{n}. {line}")
            place -= 20
            n += 1
        self.c.drawString(300, 480, "書いて練習しましょう！")
        self.c.setFont('Kyokasho', 100)
        self.c.setFillColor(colors.gray)
        self.c.setFillAlpha(0.3)
        self.c.drawString(450, 362, f'{kanji}')
        
        self.c.setFont('Noto', 16)
        self.c.setFillColor(colors.black)

        self.c.setDash(2, 4)
        self.c.line(280, 50, 280, 500)
        # lignes verticales
        for x in range(1,3):
            self.c.line(x*100+300, 50, x*100+300, 450)

        # lignes horizontales
        for y in range(1,5):
            self.c.line(350, y*100, 550, y*100)
        
        self.c.setDash()
        self.c.setLineWidth(1.3)
        # lignes verticales
        for x in range(1,4):
            self.c.line(x*100+250, 50, x*100+250, 450)
            
            # lignes horizontales
        for y in range(1,6):
            self.c.line(350, y*100-50, 550, y*100-50)
        
        image_url, img_width, img_height = get_data.define_image(kanji)
        if img_height <= 3072:
            adjusted_width = 200
            adjusted_height = img_height/img_width*200
        else:
            adjusted_height = 480
            adjusted_width = img_width/img_height*480
        self.c.drawImage(image_url, 50, 470-adjusted_height, adjusted_width, adjusted_height)
        self.c.drawString(50, 480, "書き順（かきじゅん）：")

        self.page += 1
        self.c.drawString(550, 20, f'{self.page}')
        self.c.showPage()

    def savedocument(self):
        self.c.save()


# test
if __name__ == '__main__':
    import os
    print("Test. Création de kanji.pdf en cours...")
    pdf = Kanjiinpdf("kanji_sample")
    pdf.make_title_page(['山'])
    kanji = '山'
    translation = 'Mountain'
    kunyomi = ['やま']
    onyomi = ['サン','ザン']
    samplewords =  [('火山', 'かざん', 'volcano'), ('富士山', 'ふじさん','Mount Fuji')]
    jlptlevel = ["N5"]
    frequency = ["400"]
    pdf.show_page_with_grid(kanji, translation, kunyomi, onyomi, jlptlevel, frequency, samplewords)
    try:
        pdf.savedocument()
        print("Test terminé!")
        os.startfile("kanji_sample.pdf")
    except Exception as e:
        print(e)
