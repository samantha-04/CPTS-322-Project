import os
import tempfile
import sqlite3
from code.backend import db


def test_create_user_and_verify_password(tmp_path):
    db_file = str(tmp_path / 'test_users.db')
    # ensure DB initialized
    db.init_db(db_file)

    username = 'tester'
    email = 'tester@example.com'
    password = 'S3cureP@ssw0rd'

    user = db.create_user_with_password_plain(username, email, password, path=db_file)
    assert user['email'] == email

    fetched = db.get_user_by_email(email, path=db_file)
    assert fetched is not None
    assert 'salt' in fetched and 'pwd_hash' in fetched

    assert db.verify_password(fetched['salt'], fetched['pwd_hash'], password)

    # sessions
    token = 'tokentest123'
    db.create_session(token, fetched['id'], path=db_file)
    sessions = db.get_all_sessions(path=db_file)
    assert token in sessions and sessions[token] == fetched['id']

    # cleanup
    os.remove(db_file)
