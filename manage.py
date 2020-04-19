#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager

from app import app

manager = Manager(app)

@manager.command
def runserver():
    app.run(port=30090, host='0.0.0.0')


if __name__ == '__main__':
    manager.run()
