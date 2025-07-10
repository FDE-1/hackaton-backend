from flask import Flask
from src.routes.scrapperRoutes import scrapper
from src.routes.iaRoutes import ia_routes

app = Flask(__name__)
app.register_blueprint(scrapper)
app.register_blueprint(ia_routes)

if __name__ == '__main__':
    app.run(debug=True)