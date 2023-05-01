import os

from starlette.config import Config

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)
BUILD_PATH = os.path.join(os.getcwd(), config('BUILD_PATH', default='builds'))

