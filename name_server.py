import flask


class NameServer():
    def __init__(self, name):
        self.app = flask.Flask(__name__)
        self.name = str(name)

        @self.app.route('/')
        def index():
            return self.name

    def start(self, debug=False):
        self.app.run(host='0.0.0.0', debug=debug)


if __name__ == '__main__':
    ns = NameServer('Test')
    ns.start(debug=True)
