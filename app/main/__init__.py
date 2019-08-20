from flask import Blueprint

main = Blueprint('main', __name__)  # noqa isort:skip

from app.main.views import ( # noqa isort:skip
  index,
  set_lang,
)
