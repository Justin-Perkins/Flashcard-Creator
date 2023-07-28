from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

class RoundedRectangle:
    def __init__(self, x, y, width, height, radius, line_thickness = 5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.line_thickness = line_thickness

    def drawRectangle(self, c):
        c.setLineWidth(self.line_thickness)
        c.roundRect(self.x, self.y, self.width, self.height, self.radius)

class Face:
    def __init__(self):
        self.text = ""
        self.text_font = "Noto Sans Bold"
        self.text_font_size = 50
        
        self.subtext = ""
        self.subtext_font = "Noto Sarif"
        self.subtext_font_size = 14
        
        self.border = None

    def drawFace(self, c):
        # Draw the card border
        self.border.drawRectangle(c)

        # Set font for text
        c.setFont(self.text_font, self.text_font_size)

        # Calculate the dimensions of the text
        text_width = c.stringWidth(self.text, self.text_font, self.text_font_size)
        text_height = pdfmetrics.getAscent(self.text_font, self.text_font_size)

        # Reduce font size if text is too big
        while text_width > (self.border.width * 0.9):
            self.text_font_size -= 1
            text_width = c.stringWidth(self.text, self.text_font, self.text_font_size)

        # Change the font to the new font size
        c.setFont(self.text_font, self.text_font_size)

        # Recalculate the dimensions and coordinates after adjusting font size
        text_height = pdfmetrics.getAscent(self.text_font, self.text_font_size)
        x_centered = self.border.x + (self.border.width - text_width) / 2
        y_centered = self.border.y + (self.border.height - text_height) / 2 + (pdfmetrics.getAscent(self.text_font, self.text_font_size) / 5)

        # Add text to canvas
        c.drawString(x_centered, y_centered, self.text)

        # Add the subtext
        c.setFont(self.subtext_font, self.subtext_font_size)

        # Calculate the dimensions of the subtext
        subtext_width = c.stringWidth(self.subtext, self.subtext_font, self.subtext_font_size)
        subtext_height = pdfmetrics.getAscent(self.subtext_font, self.subtext_font_size)

        # Reduce font size if text is too big
        while subtext_width > (self.border.width * 0.9):
            self.subtext_font_size -= 1
            subtext_width = c.stringWidth(self.subtext, self.subtext_font, self.subtext_font_size)

        # Change the font to the new font size
        c.setFont(self.subtext_font, self.subtext_font_size)

        # Calculate the coordinates for center the subtext inside the rectangle
        x_subtext_centered = self.border.x + (self.border.width - subtext_width) / 2
        
        # Add subtext to canvas
        c.drawString(x_subtext_centered, y_centered - (subtext_height * 1.5), self.subtext)  

class Card:
    def __init__(self):
        self.front = Face()
        self.back = Face()

    def drawCard(self, c):
        self.front.drawFace(c)
        self.back.drawFace(c)

class Pdf:
    def __init__(self, filename):
        # Register the fonts
        registerFont(TTFont("Noto Sans Bold", "C:\\Users\\ws_justin.perkins3\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSansJP-Bold.ttf"))
        registerFont(TTFont("Noto Sarif", "C:\\Users\\ws_justin.perkins3\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSerif-Regular.ttf"))

        # Create the canvas
        self.my_canvas = canvas.Canvas(f"{filename}.pdf", pagesize=letter)

        self.list_cards = []
        self.cards_per_page = 4
        self.card_count = 0

    def addCard(self, front_text, front_subtext, back_text, back_subtext):
        # Create card objects
        new_card = Card()

        # Calculate the y-coordinate based on self.card_count
        y_coordinate = 609 - self.card_count * 198

        
        # Set the text and subtext attributes and define the boder
        new_card.front.text = front_text
        new_card.front.subtext = front_subtext
        new_card.front.border = RoundedRectangle(15, y_coordinate, 276, 168, 10)

        new_card.back.text = back_text
        new_card.back.subtext = back_subtext
        new_card.back.border = RoundedRectangle(321, y_coordinate, 276, 168, 10)

        # Increment the card_count variable for the next card
        self.card_count += 1

        self.list_cards.append(new_card)


    def exportPdf(self):
        for card in self.list_cards:
            if self.card_count % self.cards_per_page == 0 and self.card_count != 0:
                self.my_canvas.showPage()  # Create a new page if the card_count is a multiple of cards_per_page
            card.drawCard(self.my_canvas)
            self.card_count += 1
        # Save the canvas
        self.my_canvas.save()
