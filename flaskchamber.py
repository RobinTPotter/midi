from flask import Flask, render_template, request
from flask_socketio import SocketIO

import midi

class FlaskGoGo():
    """run a flask webserver
    """
    def __init__(self):
        self.r=midi.EchoChamber(midi.in_device, midi.out_device)
        self.r.start()
        self.app = Flask(__name__)
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
        data = ['{}'.format(e) for e in self.r.echos]
        return """<html onselectstart='return false;'>
<script src=\"/static/socketio.js\" crossorigin=\"anonymous\"></script>
<script type="text/javascript" charset="utf-8">
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', function() {{
    socket.emit('hello', {{data: 'I\\'m connected!'}});
}});
</script>
<body>
{}
<script>
socket.emit('update', {{data: "dickheads!" }})
</script>
</body>
</html>""".format(data)

    def update(self,data):
        print("updating {}".format(data))

if __name__=='__main__':
    f=FlaskGoGo()
    f.run()
