import datetime

from PIL import Image, ImageDraw

from constants import *


class Day:
    mark = Image.open("static/mark.png").convert("RGBA").resize((int(DAY_SIZE / 8), int(DAY_SIZE / 8)))

    def __init__(self, number):
        """
            Class qui s'occupe de generer tout ce qui est en rapport avec un jour
            :param number: le numero du jour
            :type number: int
        """
        self.num = number
        self.valid = False
        self.text = ""
        self.has_text = False

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
        img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color=DAY_BG_COLOR)
        draw = ImageDraw.Draw(img)
        fill = DAY_INNER_BG_BY_DAY[self.get_own_day(month, year)[0]]
        draw.rectangle(pts, outline=LINE_COLOR, fill=fill, width=LINE_SIZE)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill=DAY_NUM_COLOR, font=FONT)

        if self.has_text:
            img.alpha_composite(self.mark,
                                (int(pts[1][0] - DAY_SIZE / 8 - DAY_SIZE * TEXT_OFFSET),
                                 int(pts[0][0] + DAY_SIZE * TEXT_OFFSET)))
        return img

    def set_text(self, text):
        if text is None:
            self.has_text = False
            self.text = ""
        else:
            self.has_text = True
            self.text = text

    def generate_text(self, month, year):
        img = Image.new("RGBA", (DAY_SIZE * 7, DAY_SIZE * 2), color=DAY_BG_COLOR)
        draw = ImageDraw.Draw(img)
        font = FONT.font_variant(size=int(FONT.size / 3))
        size_text = "a" * 150
        while font.getsize(size_text)[0] > DAY_SIZE * 7:
            size_text = size_text[:-1]
        words = self.text.split(" ")
        new_text = [""]
        for word in words:
            if len(new_text[-1]) + len(word) + 1 > len(size_text):
                new_text.append(word)
            else:
                new_text[-1] += word + " "
        n_lines = len(new_text)
        new_text = "\n".join(new_text)
        draw.text(xy=(0, 0), text="{} {} {}".format(self.num, MONTH_NAME[LANG][month - 1], year), font=font,
                  fill=TEXT_COLOR)
        draw.text(xy=(0, int((img.size[1] / 2) - ((font.getsize(new_text)[1] * n_lines) / 2))), text=new_text,
                  font=font,
                  fill=TEXT_COLOR)
        return img


class AlternateColor(Day):
    ALTERNATE_COLOR = ["#FFFAF0", "#CD5C5C", "#32CD32", "#FFFFE0", "#F0F8FF", "#663399", "#800000"]

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
        img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color=DAY_BG_COLOR)
        draw = ImageDraw.Draw(img)
        fill = self.ALTERNATE_COLOR[self.get_own_day(month, year)[0]]
        draw.rectangle(pts, outline=LINE_COLOR, fill=fill, width=LINE_SIZE)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill=DAY_NUM_COLOR, font=FONT)

        if self.has_text:
            img.alpha_composite(self.mark,
                                (int(pts[1][0] - DAY_SIZE / 8 - DAY_SIZE * TEXT_OFFSET),
                                 int(pts[0][0] + DAY_SIZE * TEXT_OFFSET)))
        return img


class PatchouliDay(Day):
    """
        Une class example pour montrer comment changer la logic de l'affichage
    """
    patchouli = Image.open("./static/patchouli.png")
    resized = False

    def generate_image(self, month, year):
        pts = [(int(DAY_SIZE * BORDER_TOP_LEFT), int(DAY_SIZE * BORDER_TOP_LEFT)),
               (int(DAY_SIZE * BORDER_BOTTOM_LEFT), int(DAY_SIZE * BORDER_BOTTOM_LEFT))]
        if not self.resized:
            self.patchouli = self.patchouli.resize((int(pts[1][0] - pts[0][0]), int(pts[1][1] - pts[0][1])))
            self.resized = True
        img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color=MONTH_BG_COLOR)
        color_img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color=MONTH_BG_COLOR)
        img.paste(self.patchouli, pts[0])

        col_img_draw = ImageDraw.Draw(color_img)
        col_img_draw.rectangle(pts, outline=LINE_COLOR, fill=DAY_INNER_BG_BY_DAY[self.get_own_day(month, year)[0]],
                               width=LINE_SIZE)

        draw = ImageDraw.Draw(img)
        draw.rectangle(pts, outline=LINE_COLOR, width=LINE_SIZE)
        color_img.putalpha(128)
        img.alpha_composite(color_img)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill=DAY_NUM_COLOR, font=FONT)
        if self.has_text:
            img.alpha_composite(self.mark,
                                (int(pts[1][0] - DAY_SIZE / 8 - DAY_SIZE * TEXT_OFFSET),
                                 int(pts[0][0] + DAY_SIZE * TEXT_OFFSET)))
        return img


class FoxDay(Day):
    bgs = [Image.open(path) for path in ["./static/fox/fox{}.png".format(i) for i in range(1, 8)]]
    resized = [False] * 7

    def generate_image(self, month, year):
        pts = [[DAY_SIZE * BORDER_TOP_LEFT, DAY_SIZE * BORDER_TOP_LEFT],
               [DAY_SIZE * BORDER_BOTTOM_LEFT, DAY_SIZE * BORDER_BOTTOM_LEFT]]
        for i, r in enumerate(FoxDay.resized):
            if not r:
                FoxDay.bgs[i] = FoxDay.bgs[i].resize((int(pts[1][0] - pts[0][0]), int(pts[1][1] - pts[0][1])))
                FoxDay.resized[i] = True
        img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color=MONTH_BG_COLOR)
        img.paste(FoxDay.bgs[self.get_own_day(month, year)[0]], (int(pts[0][0]), int(pts[0][1])))
        draw = ImageDraw.Draw(img)
        draw.rectangle(list(map(tuple, pts)), outline=LINE_COLOR, width=LINE_SIZE)
        pts[0] = [DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)]
        pts[1][0] = pts[0][0] + FONT.getsize(str(self.num))[0] * 1.05
        pts[1][1] = pts[0][1] + FONT.getsize(str(self.num))[1] * 1.05
        draw.rectangle(list(map(tuple, pts)), fill=MONTH_BG_COLOR, outline=None)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill="white", font=FONT)
        if self.has_text:
            img.alpha_composite(self.mark,
                                (int(pts[1][0] - DAY_SIZE / 8 - DAY_SIZE * TEXT_OFFSET),
                                 int(pts[0][0] + DAY_SIZE * TEXT_OFFSET)))
        return img


class ChoupetteDay(Day):
    bgs = [Image.open(path) for path in ["./static/choupette/choupette{}.png".format(i) for i in range(1, 8)]]
    resized = [False] * 7

    def generate_image(self, month, year):
        pts = [[DAY_SIZE * BORDER_TOP_LEFT, DAY_SIZE * BORDER_TOP_LEFT],
               [DAY_SIZE * BORDER_BOTTOM_LEFT, DAY_SIZE * BORDER_BOTTOM_LEFT]]
        for i, r in enumerate(FoxDay.resized):
            if not self.resized[i]:
                self.bgs[i] = self.bgs[i].resize((int(pts[1][0] - pts[0][0]), int(pts[1][1] - pts[0][1])))
                self.resized[i] = True
        img = Image.new("RGBA", size=(DAY_SIZE, DAY_SIZE), color=MONTH_BG_COLOR)
        img.paste(self.bgs[self.get_own_day(month, year)[0]], (int(pts[0][0]), int(pts[0][1])))
        draw = ImageDraw.Draw(img)
        draw.rectangle(list(map(tuple, pts)), outline=LINE_COLOR, width=LINE_SIZE)
        pts[0] = [DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)]
        pts[1][0] = pts[0][0] + FONT.getsize(str(self.num))[0] * 1.05
        pts[1][1] = pts[0][1] + FONT.getsize(str(self.num))[1] * 1.05
        draw.rectangle(list(map(tuple, pts)), fill=MONTH_BG_COLOR, outline=None)
        draw.text((DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET), DAY_SIZE * (BORDER_TOP_LEFT + TEXT_OFFSET)),
                  str(self.num), fill="white", font=FONT)
        if self.has_text:
            img.alpha_composite(self.mark,
                                (int(pts[1][0] - DAY_SIZE / 8 - DAY_SIZE * TEXT_OFFSET),
                                 int(pts[0][0] + DAY_SIZE * TEXT_OFFSET)))
        return img
