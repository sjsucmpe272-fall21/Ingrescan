from flask_sqlalchemy import SQLAlchemy

db_obj = SQLAlchemy()


# Function that initializes the db and creates the tables
def db_init(app):
    db_obj.init_app(app)

    # Creates the tables if the db doesnt already exist
    with app.app_context():
        db_obj.create_all()
