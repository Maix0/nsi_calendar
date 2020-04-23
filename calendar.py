from math import ceil

from PIL import Image

from constants import *
from month import Month


class Calendar:
    """
    Class qui reprensete le calendrier.
    """

    def __init__(self, year):
        self.year = year
        self.months = [Month(x, year) for x in range(1, 13)]

    """
    Change la classe qui represente les jours
    """

    def set_custom_day(self, day):
        map(lambda d: d.set_custom_days(day), self.months)

    """
    genere l'image du calendrier. cette fonction peut etre reimplementer pour changer l'apparence
    """

    def generate(self):
        m_x, m_y = self.months[0].generate().size
        im = Image.new("RGB", size=(m_x * MONTH_PER_LINE, m_y * ceil(12 / MONTH_PER_LINE) + HEADER_SIZE), color="white")
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

        return im
