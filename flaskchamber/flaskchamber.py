from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DecimalRangeField
from wtforms import HiddenField
from werkzeug.urls import url_encode
import logging
import midi


class FlaskGoGo():
    """run a flask webserver
    """
    def __init__(self):
        self.r=midi.EchoChamber(midi.in_device, midi.out_device)
        self.r.start()
        self.app = Flask(__name__)
        if __name__ != '__main__':
            gunicorn_logger = logging.getLogger('gunicorn.error')
            self.app.logger.handlers = gunicorn_logger.handlers
            self.app.logger.setLevel(gunicorn_logger.level)


        Bootstrap(self.app)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.app.add_url_rule('/', 'index', self.index)
        self.socketio = SocketIO(self.app)
        self.socketio.on_event('update', self.update)
        self.socketio.on_event('add', self.add)
        self.socketio.on_event('delete', self.delete)
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
        #forms=[]
        #for e in self.r.echos:
        #    form=EchoForm()
        #    form.note_offset=e[0]
        #    form.velocity_factor=e[1]
        #    form.delay=e[2]
        #    forms.append(form)
        return render_template('index.html', data=self.r.echos) 

    def delete(self,data):
        id = int(data['data'].split('_')[-1])
        self.app.logger.info("data is {}, id found is{}".format(data,id))
        del self.r.echos[id]
        self.app.logger.info("deleting {}".format(data))

    def add(self,data):
        self.r.echos.append([0,1,0])
        self.app.logger.info("adding {}".format(data))

    def update(self,data):
        type = (data['data'].split('_')[1])
        id = int(data['data'].split('_')[-1])
        value = float(data['value'])
        if type=='offset':
            cell=0
            value=int(value)
        if type=='velfact': cell=1
        if type=='delay': cell=2
        self.r.echos[id][cell]=value
        self.app.logger.info("updating {} {} {} {}".format(data, type, id, value))



if __name__=='__main__':
    f=FlaskGoGo()
    f.run()
