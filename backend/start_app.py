import os

from config import DevelopmentConfig
from config import ProductionConfig

from application import create_app

# set environment auto
if os.environ.get('ENV') == 'development':
    CONFIG = DevelopmentConfig()
else:
    CONFIG = ProductionConfig()

app = create_app(CONFIG)
