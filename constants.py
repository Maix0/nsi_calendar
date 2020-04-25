from PIL import ImageFont

DAY_SIZE = 150
MAX_DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
HEADER_SIZE = 50
BORDER_TOP_LEFT = .05
BORDER_BOTTOM_LEFT = .95
TEXT_OFFSET = .04
MONTH_PER_LINE = 3
LINE_SIZE = 5
FONT_SIZE = 50
LINE_COLOR = "black"
TEXT_COLOR = "white"
DAY_NUM_COLOR = "black"
MONTH_BG_COLOR = "#1e1e1e"
DAY_BG_COLOR = "#1e1e1e"
CALENDAR_BG_COLOR = "#1e1e1e"
DAY_INNER_BG_BY_DAY = ["#FFCC00", "#FF32CB", "#01CC01", "#FF9209", "#0265FF", "#6600CE", "#FE0000"]
LANG = "fr"
MONTH_NAME = {"fr": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
                     "Novembre", "Décembre"],
              "en": ["January", "February", "March", "April", "May", "Jun", "July", "August", "September", "October",
                     "November", "December"]}

FONT = ImageFont.truetype("Consolas.ttf", size=FONT_SIZE)


def change_lang(new_lang):
    global LANG
    LANG = new_lang


__all__ = ["DAY_SIZE", "MAX_DAY", "HEADER_SIZE", "BORDER_TOP_LEFT", "BORDER_BOTTOM_LEFT", "TEXT_OFFSET",
           "MONTH_PER_LINE", "LINE_SIZE", "FONT_SIZE", "FONT", "LINE_COLOR", "DAY_NUM_COLOR", "DAY_BG_COLOR",
           "TEXT_COLOR", "MONTH_BG_COLOR", "DAY_INNER_BG_BY_DAY", "CALENDAR_BG_COLOR", "LANG", "MONTH_NAME",
           "change_lang"]
