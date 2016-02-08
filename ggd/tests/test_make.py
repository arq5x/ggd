from ggd.ggd import make

import tempfile
import atexit
import shutil
import os

TMP = tempfile.mkdtemp()

atexit.register(shutil.rmtree, TMP)

def test_make():
    if os.path.exists("aaa"):
        os.unlink("aaa")

    res = make({'cmds': ['echo "abc" > aaa'], 'outfiles': ['aaa']},
               "name_test", "v0.0.1",
               TMP,
               ["03cfd743661f07975fa2f1220c5194cbaff48451"],
               overwrite=False)
    assert res == 0, res

    res = make({'cmds': ['echo "abc" > aaa'], 'outfiles': ['aaa']},
               "name_test", "v0.0.1",
               TMP,
               ["03cfd743661f07975fa2f1220c5194cbaff48451"],
               overwrite=False)
    assert res != 0, res

    res = make({'cmds': ['echo "abc" > aaa'], 'outfiles': ['aaa']},
               "name_test", "v0.0.1",
               TMP,
               ["03cfd743661f07975fa2f1220c5194cbaff48451"],
               overwrite=True)
    assert res == 0, res
