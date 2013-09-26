import sqlite3
import mmh3
import os

home_dir     = os.path.expanduser("~")
config_dir   = os.path.join(home_dir  , ".rab")
data_dir     = os.path.join(config_dir, "data")
snapshot_dir = os.path.join(config_dir, "snapshots")

snapshot_name = "test"

blocks = sqlite3.connect(os.path.join(data_dir, "blocks.db"))
snapshot = sqlite3.connect(os.path.join(snapshot_dir, snapshot_name))

class File():
    def __init__(self, path, id):
        self.id = id
        self.path = path

        if id is None:
            self.id = self._create_record()

    @classmethod
    def from_id(cls, id):
        with snapshot as con:
            path = con.execute("SELECT path FROM file WHERE id=?", (id,)).fetchone()

        return cls(path, id)

    @classmethod
    def from_path(cls, path):
        with snapshot as con:
            id = con.execute("SELECT id FROM file WHERE path=?", (path,)).fetchone()

        return cls(path, id)

    def _create_record(self):
        tuple = os.path.basename(self.path), self.path

        with snapshot as con:
            con.execute("REPLACE INTO file(name, path) VALUES(?, ?)", tuple)
            return con.execute("SELECT id FROM file WHERE path=?", (self.path,)).fetchone()

    def add_block(self, begin, block):
        with snapshot as con:
            tuple = hash(block), self.id[0], begin
            con.execute("REPLACE INTO file_block(block_key, file_id, begin) VALUES(?, ?, ?)", tuple)

    def blocks(self):
        with snapshot as con:
            for key, begin in con.execute("SELECT block_key, begin FROM file_block WHERE file_id=?", self.id).fetchall():
                 yield begin, Block.from_key(key)

    def reconstruct(self, target):
        with open(target, 'wb') as f:
            for offset, block in self.blocks():
                f.seek(offset)
                f.write(block.blob)

class Block():
    def __init__(self, blob, size, hash):
        self.blob = blob
        self.size = size
        self._hash = hash

    @classmethod
    def from_blob(cls, blob, size):
        return cls(blob, size, None)

    @classmethod
    def from_key(cls, key):
        with blocks as con:
            blob = con.execute("SELECT value FROM hashmap WHERE key=?", (key,)).fetchone()[0]
            size = con.execute("SELECT size FROM hashmap WHERE key=?", (key,)).fetchone()[0]

        return cls(blob, size, key)

    def __hash__(self):
        if self._hash == None:
            self._hash = mmh3.hash(self.blob)

        return self._hash

    def __str__(self):
        return hex(hash(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def store(self):
        tuple = hash(self), self.size, buffer(self.blob)

        with blocks as con:
            con.execute("INSERT INTO hashmap VALUES(?, ?, ?)", tuple)

    def exists(self):
        key = hash(self),
        sql = "SELECT * FROM hashmap WHERE key=?"

        with blocks as con:
            return [row for row in con.execute(sql, key)]
