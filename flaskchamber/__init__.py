from .flaskchamber import *

def create_app():
    f=FlaskGoGo()
    return f.app

app = create_app()

