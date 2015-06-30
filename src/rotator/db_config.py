import rotatordb


def load_config():
    session = rotatordb.db_session
    cur = session.query(rotatordb.Config).all()
    config = {}
    for conf in cur:
        config[conf.name] = conf.value

    return config
