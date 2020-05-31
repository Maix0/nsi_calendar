import constants
import web

if __name__ == "__main__":  # ceci permet d'executer ce code seulement si invoquer directement avec `python main.py`
    print("The web server will be served at http://localhost:{}/".format(constants.WEB_PORT))
    web.run(handler_class=web.CalendarWeb, port=constants.WEB_PORT)
