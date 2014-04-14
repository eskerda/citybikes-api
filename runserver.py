from api import app
from api import config

app.config['MONGO_HOST'] = config.MONGO_HOST
app.config['MONGO_PORT'] = config.MONGO_PORT
app.config['MONGO_DB'] = config.MONGO_DB

app.run(port = config.PORT, debug=config.DEBUG)
