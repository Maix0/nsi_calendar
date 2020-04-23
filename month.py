from PIL import Image, ImageDraw

from constants import *
from day import Day


class Month:
    """
    Classe qui reprente un mois d'une année donné
    """

    def __init__(self, number, year):
        self.number = number
        self.year = year
        self.days = [Day(num) for num in range(1, 32)]

    """
    Permet de changer la classe qui represente les jour
    """

    def set_custom_day(self, day):
        self.days = [day(num) for num in range(1, 32)]

    """
    Retourne le nom du mois donnée en string
    """

    @staticmethod
    def get_month(month):
        month_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
                      "Novembre", "Décembre"]
        return month_list[month - 1]

    """
        Retourne une image qui represente le mois.
        Cette fonction peut etre reimplementer pour changer l'apparence des mois.
    """

    def generate(self):
        im = Image.new("RGB", size=(DAY_SIZE * 7, DAY_SIZE * 5 + HEADER_SIZE), color="white")
        draw = ImageDraw.Draw(im)
        y = HEADER_SIZE
        x = -1
        for day in self.days:
            day.set_validity(self.number, self.year)
            if not day.valid:
                continue
            if x == -1:
                x = DAY_SIZE * day.get_own_day(self.number, self.year)[0]
            else:
                x += DAY_SIZE
            if x > DAY_SIZE * 6:
                x = 0
                y += DAY_SIZE
            im.paste(day.generate_image(self.number, self.year), (x, y))
        draw.text((0, 0), self.get_month(self.number), fill="black", font=FONT)
        return im
