from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap


import midi

class FlaskGoGo():
    """run a flask webserver
    """
    def __init__(self):
        self.r=midi.EchoChamber(midi.in_device, midi.out_device)
        self.r.start()
        self.app = Flask(__name__)
        Bootstrap(self.app)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.app.add_url_rule('/', 'index', self.index)
        self.socketio = SocketIO(self.app)
        self.socketio.on_event('update', self.update)
        #self.socketio.on_event('noteon', self.noteon)
        #self.socketio.on_event('noteoff', self.noteoff)
        #self.socketio.on_event('oct_up', self.oct_up)
        #self.socketio.on_event('oct_down', self.oct_down)

    def run(self, host='0.0.0.0'):
        """run the webserver

        Args:
            host (str, optional): listening host. Defaults to '0.0.0.0'.
        """
        self.socketio.run(self.app, host=host)

    def index(self):
        """the page
        """

        return render_template('index.html', data=self.r.echos) 

    def update(self,data):
        print("updating {}".format(data))

if __name__=='__main__':
    f=FlaskGoGo()
    f.run()
