#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask

from blueprints.admin import admin_blueprint
from blueprints.student_front import student_front_blueprint
from spreadsheet_data_mapper import DataMapper

from config import AppConfig

app_config = AppConfig()

# App configuration
app = flask.Flask(__name__)
app.config["title"] = app_config.title
app.secret_key = app_config.secret_key
app.template_folder = app_config.template_folder

DataMapper.repository.get_data()

# Register jinja templates helpers in `app.jinja_env`

# Endpoints
app.register_blueprint(student_front_blueprint)
app.register_blueprint(admin_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
