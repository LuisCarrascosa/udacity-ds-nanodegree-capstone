from flaskr.db import get_db


def select_user_byName(username):
    print(username)
    return get_db().execute(
        'SELECT id, username, password \
            FROM user WHERE username = ?', (username,)
    ).fetchone()


def select_user_byId(user_id):
    return get_db().execute(
        'SELECT id, username, password \
                FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def insert_user(username, hash_password):
    get_db().execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, hash_password)
    )

    get_db().commit()
