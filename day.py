import datetime

from PIL import Image, ImageDraw

from constants import *


class Day:
    """
        Class qui s'occupe de generer tout ce qui est en rapport avec un jour
    """

    """
    :param number: test
    :return Day
    """

    def __init__(self, number):
        self.num = number
        self.valid = False

    """
    Permet de savoir si le jour est valid, cette fonction n'est pas attacher a une instance de la classe,
    elle peut etre utiliser comme ceci :
        Day.is_valid(arguments)
    """

    @staticmethod
    def is_valid(num, month, year):
        if month == 2:
            if (year // 4 and not year // 100) or year // 400:
                return num <= 29
        return num <= MAX_DAY[month - 1]

    """
    Retourne le jour de la semaine correspondant au arguments donnés
    """

    @staticmethod
    def get_day_to_string(day, month, year):
        return ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][
            datetime.date(year, month, day).weekday()]

    """
        Retourne le jour de la semaine associer a l'instance de cette classe
    """

    def get_own_day(self, month, year):
        return datetime.date(year, month, self.num).weekday(), self.get_day_to_string(self.num, month, year)

    """
        Mets a jour une valeur de la classe qui permet de savoir si le jour existe
    """

    def set_validity(self, month, year):
        self.valid = Day.is_valid(self.num, month, year)

    """
            Retourne une image qui reprsente le jour.
            Cette fonction pourra etre réimplementer par des classe pour changer l'apparance.
    """

    def generate_image(self, month, year):
        pts = [(DAY_SIZE * BORDER_TOP_LEFT, DAY_SIZE * BORDER_TOP_LEFT),
               (DAY_SIZE * BORDER_BOTTOM_LEFT, DAY_SIZE * BORDER_BOTTOM_LEFT)]
        img = Image.new("RGB", size=(DAY_SIZE, DAY_SIZE), color=DAY_BG_COLOR)
        draw = ImageDraw.Draw(img)
        fill = DAY_INNER_BG_BY_DAY[self.get_own_day(month, year)[0]]
        draw.rectangle(pts, outline=LINE_COLOR, fill=fill, width=LINE_SIZE)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill=DAY_NUM_COLOR, font=FONT)
        return img
