import os

from dotenv import load_dotenv

from src.app import create_app

load_dotenv('.flaskenv')

app = create_app(os.environ.get('FLASK_ENV'))

if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_HOST'),
        port=os.environ.get('FLASK_PORT')
    )
