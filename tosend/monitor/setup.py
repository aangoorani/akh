from monitor import db,util


def run():
    db.setup_database()
    util.register_server("www.aut.ac.ir")
    util.register_server("www.google.com")
    util.health_check()
