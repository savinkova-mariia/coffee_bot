import sqlite3


class DBOrder:
    def __init__(self, dbname="db.sqlite3"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = 'CREATE TABLE IF NOT EXISTS posts_post ' \
               '(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, ' \
               'body text NOT NULL, ' \
               'person text NOT NULL, ' \
               'created default (datetime(current_timestamp)) NOT NULL, ' \
               'tables_id integer NOT NULL)'
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, tables_id, body, person, created):
        stmt = "INSERT INTO posts_post (tables_id, body, person, created) VALUES (?, ?, ?, ?)"
        args = (tables_id, body, person, created,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM posts_post WHERE body = (?)"
        args = (item_text,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT body FROM posts_post"
        return [x[0] for x in self.conn.execute(stmt)]
