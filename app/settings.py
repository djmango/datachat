import os

DEBUG = True if os.getenv('DEBUG') == 1 else False
if DEBUG:
    API_URL = 'https://dev.api.gambitengine.com'
else:
    API_URL = 'https://api.gambitengine.com'
