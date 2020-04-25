import colors
from calendar import Calendar

print("Please enter a number between {0}1{1} and {0}9999{1}".format(colors.GREEN, colors.RESET))
print("Any other number will terminate the program")
while True:
    year = int(input("What year > "))
    if year < 1 or year > 9999:
        break
    c = Calendar(year)
    c.generate().show()
