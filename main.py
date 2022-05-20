import os
from src.app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=os.environ.get('FLASK_DEBUG'),
        host=os.environ.get('FLASK_HOST'),
        port=os.environ.get('FLASK_PORT')
    )
