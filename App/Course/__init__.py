from flask import Blueprint

course_blueprint = Blueprint("course", __name__, url_prefix="/course")

from .views import *
