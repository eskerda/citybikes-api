from flask import Flask
import config

app = Flask(__name__)

# These are default settings, please, set them
# before app.run customized to your own needs
app.config['MONGO_HOST'] = config.MONGO_HOST
app.config['MONGO_PORT'] = config.MONGO_PORT
app.config['MONGO_DB'] = config.MONGO_DB
app.config['REDIRECT'] = config.REDIRECT

import api.views
