# Application runpoint file

from flask import Flask
from app import app
app = Flask(__name__)


# Placeholder test function
@app.route('/')
def init_run():
    return 'Testing output...'

@app.route('/page/<int:page_num>')
def content(page_num):
    return f'<h1>Welcome to page {page_num} of this webapp!</h1>'

if __name__ == '__main__':
    app.run()