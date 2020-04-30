from calendar import Calendar
from day import PatchouliDay
from month import ColorMonth

if __name__ == "__main__":  # ceci permet d'executer ce code seulement si invoquer directement avec `python main.py`
    print("Please enter a number between 1 and 9999")
    print("Any other number will terminate the program")
    while True:
        year = int(input("What year > "))
        if year < 1 or year > 9999:
            break
        c = Calendar(year)
        c.set_custom_day(PatchouliDay)
        c.set_custom_month(ColorMonth)
        c.generate().show()
        # c.generate().save("calendar.png")
