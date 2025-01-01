from flask import Flask
from sql_blueprint import sql_app
from phishing_app import phishing_app
from dos_app import dos_app
from crypto_blueprint import crypto_blueprint
from diffie_hellman import diffie_hellman_blueprint

app = Flask(__name__)

# Register blueprints with URL prefixes
app.register_blueprint(sql_app, url_prefix='/sql')
app.register_blueprint(phishing_app, url_prefix='/phishing')
app.register_blueprint(dos_app, url_prefix='/dos')
app.register_blueprint(crypto_blueprint)  # No url_prefix here
app.register_blueprint(diffie_hellman_blueprint, url_prefix='/diffie_hellman')
# Home route
@app.route('/')
def home():
    return "Welcome to the Combined Flask Application!"

# Custom error handler
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(debug=True)
