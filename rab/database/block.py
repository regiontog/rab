from rab.database import _get
from rab.database import blocks_con as blocks
import mmh3

def reset():
    """Delete all blocks stored and initialize empty tabels
       WARNING: Will cause loss of data"""

    with blocks as con:
        con.execute("DROP TABLE IF EXISTS hashmap")
        con.execute("CREATE TABLE hashmap(key INT, size INT, value BLOB)")


class Block():
    def __init__(self, blob, size, hash):
        self.blob = blob
        self.size = size
        self._hash = hash

    @classmethod
    def with_blob(cls, blob, size):
        return cls(blob, size, None)

    @classmethod
    def from_key(cls, key):
        print "Getting block", hex(key)
        with blocks as con:
            blob = _get(con, key, select="value", frm="hashmap", where="key")
            size = _get(con, key, select="size" , frm="hashmap", where="key")

        return cls(blob, size, key)

    def __hash__(self):
        if self._hash == None:
            self._hash = mmh3.hash(self.blob)

        return self._hash

    def __str__(self):
        return hex(hash(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def _store(self):
        tuple = hash(self), self.size, buffer(self.blob)

        with blocks as con:
            con.execute("INSERT INTO hashmap VALUES(?, ?, ?)", tuple)

    def store(self):
        if self.exists():
            print "-----> Block", self, "already exists"
        else:
            print "Inserting", self
            self._store()

    def exists(self):
        key = hash(self),
        sql = "SELECT * FROM hashmap WHERE key=?"

        with blocks as con:
            return [row for row in con.execute(sql, key)]
