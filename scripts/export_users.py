"""Simple admin/export script to dump users as JSON."""
import json
from code.backend import db

if __name__ == '__main__':
    users = db.get_all_users()
    print(json.dumps(users, indent=2))
