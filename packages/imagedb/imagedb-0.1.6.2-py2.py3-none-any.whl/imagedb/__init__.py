from flask import Flask

app = Flask(__name__)

from .views import index, get_image
from .api import create_image, rename_image
from .main import ImageDB
