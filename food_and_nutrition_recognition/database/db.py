from scripts.utils import db_connect

db_obj = None


def connect_to_db(app):
    global db_obj
    db_obj = db_connect(app)
    return db_obj
