from flask import Flask

app = Flask(__name__)

# These are default settings, please, set them
# before app.run customized to your own needs
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DB'] = 'citybikes'

import api.views