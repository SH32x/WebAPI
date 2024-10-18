# Application runpoint file

from flask import Flask
app = Flask(__name__)


# Placeholder test function
@app.route('/')
def init_run():
    return 'Testing output...'