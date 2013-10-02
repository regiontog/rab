import sqlite3
import logging
import os.path
from rab.database import snapshot_con as snapshot
from rab.database import _get, snapshot_dir, block

logger = logging.getLogger(__name__)

def set(path):
    logger.debug("Setting snapshot to %s" % path)

    global snapshot
    snapshot = sqlite3.connect(path)

def create():
    with snapshot as con:
        con.execute("CREATE TABLE file(id INTEGER PRIMARY KEY, name TEXT, path TEXT UNIQUE)")
        con.execute("CREATE TABLE file_block(block_key INT, file_id INT, begin INT)")
        con.execute("CREATE TABLE metadata(name TEXT)")

def delete():
    """Delete all files in current snapshot, but not the blocks they contain"""
    with snapshot as con:
        con.execute("DROP TABLE IF EXISTS file")
        con.execute("DROP TABLE IF EXISTS file_block")
        con.execute("DROP TABLE IF EXISTS metadata")

class File():
    def __init__(self, path, id):
        self.id = id
        self.path = path

        if id is None:
            self.id = self._create_record()

    @classmethod
    def from_id(cls, id):
        with snapshot as con:
            path = _get(con, id, select="path", frm="file", where="id")

        return cls(path, id)

    @classmethod
    def from_path(cls, path):
        with snapshot as con:
            id = _get(con, path, select="id", frm="file", where="path")

        return cls(path, id)

    def _create_record(self):
        tuple = os.path.basename(self.path), self.path

        with snapshot as con:
            con.execute("REPLACE INTO file(name, path) VALUES(?, ?)", tuple)
            return _get(con, self.path, select="id", frm="file", where="path")

    def add_block(self, begin, block):
        with snapshot as con:
            tuple = hash(block), self.id, begin
            con.execute("REPLACE INTO file_block(block_key, file_id, begin) VALUES(?, ?, ?)", tuple)

    def blocks(self):
        with snapshot as con:
            for key, begin in con.execute("SELECT block_key, begin FROM file_block WHERE file_id=?", (self.id,)).fetchall():
                 yield begin, block.Block.from_key(key)

    def reconstruct(self, target):
        with open(target, 'wb') as f:
            for offset, block in self.blocks():
                logger.debug("Writing to file %s with offset %s: %s" % (target, offset, block))
                f.seek(offset)
                f.write(block.blob)
