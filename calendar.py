from math import ceil

from PIL import Image, ImageDraw

from constants import *
from month import Month


class Calendar:

    def __init__(self, year):
        """
            Une representation d'un calendrier
            :param year: l'année du calendrier
        """
        self.year = year
        self.months = [Month(x, year) for x in range(1, 13)]

    def set_custom_day(self, custom_day):
        """
            Change la classe qui s'occupe des jours
            :param custom_day: Class qui herite de Day
            :return:
        """
        self.months = list(map(lambda m: m.set_custom_day(custom_day), self.months))

    def set_custom_month(self, m):
        """
            Change la classe qui s'occupe des mois
            :param m: Class qui herite de Month
            :return:
        """
        tmp_month = self.months
        self.months = [m(x, self.year) for x in range(1, 13)]
        for (n, b) in zip(self.months, tmp_month):
            n.days = b.days

    def generate(self):
        """
            Genere une image qui montre tout le calendrier
            :return: Image du calendrier.
        """
        m_x, m_y = self.months[0].generate().size
        im = Image.new("RGB", size=(m_x * MONTH_PER_LINE, m_y * ceil(12 / MONTH_PER_LINE) + HEADER_SIZE),
                       color=CALENDAR_BG_COLOR)
        x, y = -1, HEADER_SIZE
        for month in self.months:
            if x == -1:
                x = 0
            else:
                x += m_x
            if x > m_x * (MONTH_PER_LINE - 1):
                x = 0
                y += m_y
            m_img = month.generate()
            im.paste(m_img, (x, y))
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), str(self.year), fill=TEXT_COLOR, font=FONT)
        return im
