from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Carga tu configuración normal
    app.config.from_object(Config)

    # 1) Leemos la variable original
    orig_uri = os.environ.get("DATABASE_URL", "")
    print(">>> DEBUG: orig DATABASE_URL =", orig_uri)

    # 2) Forzamos que use pg8000 aunque llegue sin el sufijo
    if orig_uri.startswith("postgres://"):
        uri = orig_uri.replace("postgres://", "postgresql+pg8000://", 1)
    elif orig_uri.startswith("postgresql://") and "+pg8000://" not in orig_uri:
        uri = orig_uri.replace("postgresql://", "postgresql+pg8000://", 1)
    else:
        uri = orig_uri
    print(">>> DEBUG: using DATABASE_URI =", uri)

    # 3) Configuramos SQLAlchemy con el URI forzado
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    db.init_app(app)

    # Registramos los blueprints
    from controllers.tipo_validacion_controller import tipo_validacion_bp
    from controllers.lugar_conversion_controller import lugar_conversion_bp
    from controllers.convertido_controller import convertido_bp
    from controllers.dashboard_controller import dashboard_bp
    from controllers.health_controller import health_bp



    app.register_blueprint(tipo_validacion_bp)
    app.register_blueprint(lugar_conversion_bp)
    app.register_blueprint(convertido_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(health_bp)

    
    

    @app.route("/")
    def home():
        return render_template("home.html")

    return app

if __name__ == "__main__":
    app = create_app()   
    app.run(debug=True)
