import day
import month

THEMES = {
    "default": ["default", "default"],
    "patchouli": ["default", "patchouli"],
    "fox": ["default", "fox"],

}
MONTHS = {
    "default": month.Month,
    "color": month.ColorMonth,
}
DAYS = {
    "default": day.Day,
    "alternate": day.AlternateColor,
    "patchouli": day.PatchouliDay,
    "fox": day.FoxDay,
    "choupette": day.ChoupetteDay,
}


def from_theme(theme_name: str):
    """
    :type theme_name: str
    """
    if theme_name not in THEMES:
        return None, None
    return MONTHS[THEMES[theme_name][0]], DAYS[THEMES[theme_name][1]]
