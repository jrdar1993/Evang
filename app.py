from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from controllers.tipo_validacion_controller import tipo_validacion_bp
    from controllers.lugar_conversion_controller import lugar_conversion_bp
    from controllers.convertido_controller import convertido_bp

    app.register_blueprint(tipo_validacion_bp)
    app.register_blueprint(lugar_conversion_bp)
    app.register_blueprint(convertido_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
