import datetime

from PIL import Image, ImageDraw

from constants import *


class Day:
    def __init__(self, number):
        """
            Class qui s'occupe de generer tout ce qui est en rapport avec un jour
            :param number: le numero du jour
        """
        self.num = number
        self.valid = False

    @staticmethod
    def is_valid(num, month, year):
        """
            Retourne le jour de la semaine correspondant au arguments donnés
            :param num: le numero du jour
            :param month: le mois associer
            :param year: l'année associer
            :return: un boolean qui indique si le jour donnée est valid
        """
        correct_date = None
        try:
            datetime.datetime(year, month, num)
            correct_date = True
        except ValueError:
            correct_date = False
        return correct_date
        # if month == 2:
        #    if isleap(year):
        #        return num <= 29
        # return num <= MAX_DAY[month - 1]

    @staticmethod
    def get_day_to_string(day, month, year):
        """
            :param day: le numero du jour
            :param month: le mois associer
            :param year: l'année associer
            :return: le nom du jour
        """
        return ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][
            datetime.date(year, month, day).weekday()]

    def get_own_day(self, month, year):
        """
            :param month: le mois associer au jour
            :param year: l'année associer au jour
            :return: le numero du jour dans la semaine (0-6) et son nom
        """
        return datetime.date(year, month, self.num).weekday(), self.get_day_to_string(self.num, month, year)

    def set_validity(self, month, year):
        """
            Change la variable `valid`
            :param month: le mois associer au jour
            :param year: l'année associer au jour
        """
        self.valid = Day.is_valid(self.num, month, year)

    def generate_image(self, month, year):
        """
            Retourne une image qui reprsente le jour.
            Cette fonction pourra etre réimplementer par des classe pour changer l'apparance.
            :param month: le mois associer au jour
            :param year: l'année associer au jour
            :return: Image qui represente le jour.
        """
        pts = [(DAY_SIZE * BORDER_TOP_LEFT, DAY_SIZE * BORDER_TOP_LEFT),
               (DAY_SIZE * BORDER_BOTTOM_LEFT, DAY_SIZE * BORDER_BOTTOM_LEFT)]
        img = Image.new("RGB", size=(DAY_SIZE, DAY_SIZE), color=DAY_BG_COLOR)
        draw = ImageDraw.Draw(img)
        fill = DAY_INNER_BG_BY_DAY[self.get_own_day(month, year)[0]]
        draw.rectangle(pts, outline=LINE_COLOR, fill=fill, width=LINE_SIZE)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill=DAY_NUM_COLOR, font=FONT)
        return img


class PatchouliDay(Day):
    """
        Une class example pour montrer comment changer la logic de l'affichage
    """
    patchouli = Image.open("./patchouli.png")

    def generate_image(self, month, year):
        PatchouliDay.patchouli.resize((DAY_SIZE, DAY_SIZE))
        pts = [(DAY_SIZE * BORDER_TOP_LEFT, DAY_SIZE * BORDER_TOP_LEFT),
               (DAY_SIZE * BORDER_BOTTOM_LEFT, DAY_SIZE * BORDER_BOTTOM_LEFT)]
        img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color="white")
        color_img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE),
                              color=DAY_INNER_BG_BY_DAY[self.get_own_day(month, year)[0]])
        color_img.putalpha(150)
        img.paste(PatchouliDay.patchouli, (0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle(pts, outline=LINE_COLOR, width=LINE_SIZE)
        img.alpha_composite(color_img)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill=DAY_NUM_COLOR, font=FONT)
        return img
