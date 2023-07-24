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

# Register the fonts
registerFont(TTFont("Noto Sans Bold", "C:\\Users\\ws_justin.perkins3\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSansJP-Bold.ttf"))
registerFont(TTFont("Noto Sarif", "C:\\Users\\ws_justin.perkins3\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSerif-Regular.ttf"))

# Create card objects
card1 = Card()
card2 = Card()
card3 = Card()
card4 = Card()
card5 = Card()

# Set the text and subtext attributes and define the boder
#Card 1
card1.front.text = "駅"
card1.front.subtext = "(eki)"
card1.front.border = RoundedRectangle(15, 609, 276, 168, 10)

card1.back.text = "Train Station"
card1.back.subtext = ""
card1.back.border = RoundedRectangle(321, 609, 276, 168, 10)

#Card 2
card2.front.text = "郵便局"
card2.front.subtext = "(yūbin kyoku)"
card2.front.border = RoundedRectangle(15, 411, 276, 168, 10)

card2.back.text = "Post Office"
card2.back.subtext = ""
card2.back.border = RoundedRectangle(321, 411, 276, 168, 10)

#Card 3
card3.front.text = "雑誌"
card3.front.subtext = "(zasshi)"
card3.front.border = RoundedRectangle(15, 213, 276, 168, 10)

card3.back.text = "Magazine"
card3.back.subtext = ""
card3.back.border = RoundedRectangle(321, 213, 276, 168, 10)

#Card 4
card4.front.text = "新聞"
card4.front.subtext = "(shinbun)"
card4.front.border = RoundedRectangle(15, 15, 276, 168, 10)

card4.back.text = "Newspaper"
card4.back.subtext = ""
card4.back.border = RoundedRectangle(321, 15, 276, 168, 10)

#Card 5
card5.front.text = "テレビ"
card5.front.subtext = "(terebi)"
card5.front.border = RoundedRectangle(15, 609, 276, 168, 10)

card5.back.text = "Tv"
card5.back.subtext = ""
card5.back.border = RoundedRectangle(321, 609, 276, 168, 10)

# Create the canvas
my_canvas = canvas.Canvas('Flashcards.pdf', pagesize=letter)

cards = [card1, card2, card3, card4, card5]  # Add more cards to this list as needed

cards_per_page = 4
card_count = 0

# Draw the rounded rectangles for each card in two columns and handle page breaks
for card in cards:
    if card_count % cards_per_page == 0 and card_count != 0:
        my_canvas.showPage()  # Create a new page if the card_count is a multiple of cards_per_page
    card.drawCard(my_canvas)
    card_count += 1

# Save the canvas
my_canvas.save()
