import sqlite3
import os

home_dir     = os.path.expanduser("~")
config_dir   = os.path.join(home_dir  , ".rab")
data_dir     = os.path.join(config_dir, "data")
snapshot_dir = os.path.join(config_dir, "snapshots")

blocks_con = sqlite3.connect(os.path.join(data_dir, "blocks.db"))
snapshot_con = sqlite3.connect(os.path.join(snapshot_dir, "default"))

def _get(con, val, **kwargs):
    sql = "SELECT %(select)s FROM %(frm)s WHERE %(where)s=?" % kwargs
    try:
        return con.execute(sql, (val,)).fetchone()[0]
    except TypeError as e:
        print "TypeError: %s with %s returned None" % (sql, val)
        return None
