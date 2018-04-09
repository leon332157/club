import flask
import uuid

class NameServer():
    def __init__(self, name):
        self.app = flask.Flask(__name__)
        self.name = str(name)
        self.id=str(uuid.uuid4().int)
        @self.app.route('/')
        def index():
            return self.name
        @self.app.route('/id')
        def id():
            #print(self.id)
            return self.id

    def start(self, debug=False):
        self.app.run(host='0.0.0.0', debug=debug)


if __name__ == '__main__':
    ns = NameServer('Test')
    ns.start(debug=True)
