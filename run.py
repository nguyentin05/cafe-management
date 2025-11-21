from app import app

if __name__ == "__main__":
    with app.app_context():
        from app.admin import *
        app.run(debug=True)