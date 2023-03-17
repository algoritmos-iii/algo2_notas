#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask

from .blueprints.admin import admin_blueprint
from .blueprints.student_front import student_front_blueprint

from .jinja2_filters import markdown2HTML, as_grade_str
from .config import AppConfig

app_config = AppConfig()

# App configuration
app = flask.Flask(__name__)
app.config["title"] = app_config.title
app.secret_key = app_config.secret_key
app.template_folder = app_config.template_folder
app.static_folder = app_config.static_folder

# Register jinja templates helpers
# pylint: disable=no-member
app.jinja_env.filters["md"] = markdown2HTML
app.jinja_env.filters["as_grade_str"] = as_grade_str
# pylint: enable=no-member

# Endpoints
app.register_blueprint(student_front_blueprint)
app.register_blueprint(admin_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
