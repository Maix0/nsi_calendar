import json
import mimetypes
import posixpath
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4

import calendar
import themes

CAL_ID = r"(?P<cal_id>[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab][0-9A-Za-z]{3}-[0-9A-Za-z]{12})"


class CalendarWeb(BaseHTTPRequestHandler):
    pages = {
        "index": re.compile(r"^/$", re.MULTILINE),
        "assets": re.compile(r"^/assets/(?P<Filename>[a-z]+\.[a-z]+)$", re.MULTILINE),
        "get_month": re.compile(
            r"^/image/{cal_id}/(?P<month>[1-9]|[1][0-2]?)(?:/(?P<text>[0-9]{{1,2}}))?\?\d{{5}}".format(cal_id=CAL_ID),
            re.MULTILINE),
        "get_id": re.compile(r"^/get_id/(?P<year>\d{1,4})", re.MULTILINE),
        "set_theme": re.compile(r"^/set_theme/{cal_id}/(?P<theme_name>[a-z]*)".format(cal_id=CAL_ID), re.MULTILINE),
        "set_month": re.compile(r"^/set_theme/month/{cal_id}/(?P<theme_month>[a-z]*)".format(cal_id=CAL_ID),
                                re.MULTILINE),
        "set_day": re.compile(r"^/set_theme/day/{cal_id}/(?P<theme_day>[a-z]*)".format(cal_id=CAL_ID), re.MULTILINE),
        "get_themes": re.compile(r"^/get_themes/(?P<query>day|month|theme)", re.MULTILINE),
        "get_days": re.compile(r"^/get_days/{cal_id}/(?P<month>[1-9]|[1][0-2]?)".format(cal_id=CAL_ID), re.MULTILINE),
        "set_text": re.compile(
            r"^/set_text/{cal_id}/(?P<month>[1-9]|[1][0-2]?)/(?P<day>\d{{1,2}})".format(cal_id=CAL_ID), re.MULTILINE),
        "get_text": re.compile(
            r"^/get_text/{cal_id}/(?P<month>[1-9]|[1][0-2]?)/(?P<day>\d{{1,2}})".format(cal_id=CAL_ID), re.MULTILINE),
        "test": re.compile(r"^/test/", re.MULTILINE)
    }
    calendars = {}

    extensions_map = _encodings_map_default = {
        '.gz': 'application/gzip',
        '.Z': 'application/octet-stream',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
    }

    def __init__(self, *args, **kwargs):
        self.body = None
        super().__init__(*args, **kwargs)

    # noinspection PyPep8Naming
    def do_GET(self) -> None:
        valid_route = self.check_route("index", self.serve_index) or \
                      self.check_route("assets", self.serve_assets) or \
                      self.check_route("get_month", self.serve_get_month) or \
                      self.check_route("get_id", self.serve_get_id) or \
                      self.check_route("set_theme", self.serve_set_theme) or \
                      self.check_route("set_month", self.serve_set_month) or \
                      self.check_route("set_day", self.serve_set_day) or \
                      self.check_route("get_themes", self.serve_get_themes) or \
                      self.check_route("get_days", self.serve_days_location) or \
                      self.check_route("get_text", self.serve_get_text) or \
                      self.check_route("test", self.serve_test) or \
                      False

        if not valid_route:
            self.not_found()

    # noinspection PyPep8Naming
    def do_POST(self) -> None:
        self.body = self.rfile.read(int(self.headers.get('content-length', 0)))
        valid_route = self.check_route("set_text", self.serve_set_text) or False
        if not valid_route:
            self.not_found()
        self.body = None

    def check_route(self, route, handler) -> None:
        m = self.pages[route].fullmatch(self.path)
        if m:
            handler(m)
            return True
        return False

    def serve_index(self, match: re.Match) -> None:
        """
        :type match: re.Match
        la fonction qui gere l'adresse "/"
        """
        self.send_file("index.html")

    def serve_assets(self, match: re.Match) -> None:
        """
        :type match: re.Match
        la fonction qui gere l'adresse "/"
        """
        self.send_file(match.groupdict()["Filename"])

    def serve_get_month(self, match: re.Match) -> None:
        """4
        :type match: re.Match
        la fonction qui gere l'adresse "/image/<id>/<mois>"
        """
        cal_id = match.groupdict()["cal_id"]
        month = int(match.groupdict()["month"])
        has_text = match.groupdict()["text"]
        if not self.has_id(cal_id):
            return self.not_found()
        self.ok()
        self.calendars[cal_id].months[month - 1].generate(
            focus=int(has_text) if type(has_text) == str else None).save(self.wfile, "PNG")

    def serve_get_id(self, match: re.Match) -> None:
        """
        :type match: re.Match
        la fonction qui gere l'adresse "/get_id/<année>"
        """
        year = int(match.groupdict()["year"])
        if year < 1 or year > 9999:
            return self.not_found()
        u = uuid4()
        self.calendars[str(u)] = calendar.Calendar(year)
        self.ok()
        self.wfile.write(bytes(str(u), 'utf-8'))

    def serve_set_theme(self, match: re.Match):
        """
        :type match: re.Match
        la fonction qui gere l'adresse "/set_theme/<cal_id>/<theme>"
        """
        cal_id = match.groupdict()["cal_id"]
        theme = match.groupdict()["theme_name"]
        if not self.has_id(cal_id):
            return self.not_found()
        month, day = themes.from_theme(theme)
        self.ok()
        if month is not None:
            self.calendars[cal_id].set_custom_month(month)
            self.wfile.write(bytes("{}".format(theme), 'utf-8'))
        if day is not None:
            self.calendars[cal_id].set_custom_day(day)
            self.wfile.write(bytes("{}".format(theme), 'utf-8'))

    def serve_set_month(self, match: re.Match):
        """
        :type match: re.Match
        :param match: regex match
        :return: None
        """
        cal_id = match.groupdict()["cal_id"]
        theme = match.groupdict()["theme_month"]
        if not self.has_id(cal_id):
            return self.not_found()
        month = themes.MONTHS.get(theme)
        self.ok()
        if month is not None:
            self.calendars[cal_id].set_custom_month(month)
            self.wfile.write(bytes("{}".format(theme), 'utf-8'))

    def serve_set_day(self, match: re.Match):
        """
        :type match: re.Match
        :param match: regex match
        :return: None
        """
        cal_id = match.groupdict()["cal_id"]
        theme = match.groupdict()["theme_day"]
        if not self.has_id(cal_id):
            return self.not_found()
        day = themes.DAYS.get(theme)
        self.ok()
        if day is not None:
            self.calendars[cal_id].set_custom_day(day)
            self.wfile.write(bytes("{}".format(theme), 'utf-8'))

    def serve_get_themes(self, match: re.Match):
        """
        :type match: re.Match
        :param match: regex match
        :return: None
        """
        query = match.groupdict()["query"]
        self.ok()
        data = None
        if query == "day":
            data = json.dumps(list(themes.DAYS.keys()))
        elif query == "month":
            data = json.dumps(list(themes.MONTHS.keys()))
        elif query == "theme":
            data = json.dumps(themes.THEMES)
        self.wfile.write(bytes(data, "utf-8"))

    def serve_days_location(self, match):
        """
        :type match: re.Match
        :param match: regex match
        :return: None
        """
        cal_id = match.groupdict()["cal_id"]
        month = int(match.groupdict()["month"])
        if not self.has_id(cal_id):
            self.not_found()
        data = json.dumps(self.calendars[cal_id].months[month - 1].get_day_location())
        self.wfile.write(bytes(data, "utf-8"))

    def serve_test(self, match):
        self.ok()
        calendar.Calendar(2020).months[0].days[0].generate_text(12, 2020).save(self.wfile, "PNG")

    def serve_get_text(self, match):
        cal_id = match.groupdict()["cal_id"]
        month = int(match.groupdict()["month"])
        day = int(match.groupdict()["day"])
        if not self.has_id(cal_id):
            self.not_found()
            return
        if themes.day.Day.is_valid(day, month, self.calendars[cal_id].year):
            self.ok()
            data = json.dumps({"message":
                                   self.calendars[cal_id].months[month - 1].days[day - 1].text if
                                   self.calendars[cal_id].months[month - 1].days[day - 1].has_text else None})
            self.wfile.write(bytes(data, "utf-8"))
        else:
            self.not_found()

    def serve_set_text(self, match):
        data = json.loads(self.body)
        if not "message" in data:
            self.not_found()
            return
        cal_id = match.groupdict()["cal_id"]
        month = int(match.groupdict()["month"])
        day = int(match.groupdict()["day"])
        if not self.has_id(cal_id):
            self.not_found()
            return
        if themes.day.Day.is_valid(day, month, self.calendars[cal_id].year):
            self.ok()
            self.calendars[cal_id].set_text(day, month, data["message"])
        else:
            self.not_found()

    def guess_type(self, path):
        """Guess the type of a file.
        Argument is a PATH (a filename).
        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.
        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.
        """
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        guess, _ = mimetypes.guess_type(path)
        if guess:
            return guess
        return 'application/octet-stream'

    def has_id(self, cal_id: str):
        return cal_id in self.calendars

    def send_file(self, filename: str):
        try:
            file = open("./pages/" + filename, "rb")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", self.guess_type(filename))
            self.end_headers()
            self.wfile.write(file.read())
        except OSError as e:
            print(e)
            self.not_found()

    def ok(self) -> None:
        """
        Send an "200 OK" to the client
        :rtype:
        """
        self.send_response(HTTPStatus.OK)
        self.end_headers()

    def not_found(self) -> None:
        """
        Send a "404 Not Found" to the client
        :rtype:
        """
        self.send_response(HTTPStatus.NOT_FOUND)
        self.end_headers()
        self.wfile.write(bytes("{} \nNot Found".format(self.path), 'utf-8'))


def run(server_class=ThreadingHTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run(handler_class=CalendarWeb)
