from api import app
from api import config

app.config['MONGO_HOST'] = config.MONGO_HOST
app.config['MONGO_PORT'] = config.MONGO_PORT
app.config['MONGO_DB'] = config.MONGO_DB

app.run(port=config.PORT, debug=config.DEBUG, host='0.0.0.0', threaded=False, processes=1, use_reloader=False, use_debugger=False)
