import StringIO
import os

from rab import __file__ as mod_path
from rab.database import snapshot, block
from rab.parse import Parse
from rab.rab import _setup

root = os.path.dirname(mod_path) + "/tests/"

_setup()
snapshot.set(root + "testing.db")
snapshot.delete()
snapshot.create()
block.reset()


def test_parser_and_reconstruct():
    import filecmp

    Parse.parser(root + "test_file")
    file = snapshot.File.from_path(root + "test_file")
    file.reconstruct(root + "recon")

    res = filecmp.cmp(root + "test_file", root + "recon")
    os.remove(root + "recon")
    assert res
