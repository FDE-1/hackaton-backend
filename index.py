from flask import Flask
from src.routes.scrapperRoutes import scrapper
from src.routes.iaRoutes import ia_routes
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
app.register_blueprint(scrapper)
app.register_blueprint(ia_routes)

if __name__ == '__main__':
    app.run(debug=True)