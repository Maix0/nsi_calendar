import datetime

from PIL import Image, ImageDraw

from constants import *


class Day:
    MAX_DAY = MAX_DAY

    def __init__(self, number):
        self.num = number
        self.valid = False

    @staticmethod
    def is_valid(num, month, year):
        if month == 2:
            if (year // 4 and not year // 100) or year // 400:
                return num <= 29
        return num <= Day.MAX_DAY[month - 1]

    @staticmethod
    def get_day_to_string(day, month, year):
        return ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][
            datetime.date(year, month, day).weekday()]

    def get_own_day(self, month, year):
        return datetime.date(year, month, self.num).weekday(), self.get_day_to_string(self.num, month, year)

    def set_validity(self, month, year):
        self.valid = Day.is_valid(self.num, month, year)

    def generate_image(self, month, year):
        pts = [(DAY_SIZE * BORDER_TOP_LEFT, DAY_SIZE * BORDER_TOP_LEFT),
               (DAY_SIZE * BORDER_BOTTOM_LEFT, DAY_SIZE * BORDER_BOTTOM_LEFT)]
        img = Image.new("RGB", size=(DAY_SIZE, DAY_SIZE), color="white")
        draw = ImageDraw.Draw(img)
        print(self.get_own_day(month, year)[0])
        # fill = ["yellow", "blue", "cyan", "orange", "purple", "green", "grey"][self.get_own_day(month, year)[0]]
        fill = "white"
        draw.rectangle(pts, outline="black", fill=fill, width=LINE_SIZE)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill="red", font=FONT)
        return img
