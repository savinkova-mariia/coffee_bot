import sqlite3


class DBMenu:
    def __init__(self, dbname="menu.sqlite3"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (beverages text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT beverages FROM items"
        return [x[0] for x in self.conn.execute(stmt)]
