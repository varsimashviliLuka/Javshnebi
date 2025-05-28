from src import create_app
from src.config import DevConfig

flask_app = create_app(config=DevConfig)

# flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(debug=True, host='0.0.0.0', use_reloader=False)