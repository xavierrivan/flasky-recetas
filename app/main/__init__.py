from flask import Blueprint

main = Blueprint('main', __name__)


def linebreaksbr_filter(text):
    """Converts newlines to <br> tags."""
    return text.replace('\n', '<br>')


main.app_template_filter('linebreaksbr')(linebreaksbr_filter)

from . import views, errors
