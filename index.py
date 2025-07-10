from flask import Flask
from src.routes.scrapperRoutes import scrapper

app = Flask(__name__)
app.register_blueprint(scrapper)

if __name__ == '__main__':
    app.run(debug=True)