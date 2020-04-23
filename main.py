# imports
import datetime

from PIL import Image, ImageDraw

# Constants
# *_SIZE = <INT> in pixel;
# *_COLOR = r,g,b int tuple;
DAY_SIZE = 40
MAX_DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
HEADER_SIZE = 25
BORDER_TOP_LEFT = .05
BORDER_BOTTOM_LEFT = .95
TEXT_OFFSET = .04


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
        fill = ["yellow", "blue", "cyan", "orange", "purple", "green", "grey"][self.get_own_day(month, year)[0]]
        draw.rectangle(pts, outline="black", fill=fill)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill="red")
        return img


class Month:
    def __init__(self, number, year):
        self.number = number
        self.year = year
        self.days = [Day(num) for num in range(1, 31)]

    @staticmethod
    def get_month(month):
        month_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
                      "Novembre", "Décembre"]
        return month_list[month - 1]

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
        draw.text((0, 0), "{} {}".format(self.get_month(self.number), self.year), fill="black")
        return im


m = Month(4, 2020)
m.generate().show()
