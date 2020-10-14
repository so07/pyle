"""
unit tests for pyle module
"""
import os
import glob
import random
import string


def get_random_string(length=10):
    """return random string of given length"""
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def touch_file(d, f):
    """create empty file in a given directory"""
    path = os.path.join(d, f)
    with open(path, "w") as fp:
        pass
    return path


def test_import_pyle():
    import pyle
    from pyle import add_pyle_parser
    from pyle import add_parser


def test_add_pyle_parser():
    import argparse
    from pyle import add_pyle_parser

    parser = argparse.ArgumentParser()

    add_pyle_parser(parser)


def test_add_parser_deprecated():
    import argparse
    from pyle import add_parser

    parser = argparse.ArgumentParser()

    add_parser(parser)


def test_get_files(tmpdir):
    import argparse
    import datetime
    from pyle import get_files

    l = []
    for i in range(10):
        l.append(touch_file(tmpdir, get_random_string()))

    d = argparse.Namespace()
    d.pyle_files = l
    d.from_date = datetime.datetime.strptime(
        datetime.datetime(1970, 1, 1).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
    )
    d.to_date = datetime.datetime.strptime(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
    )
    d.from_date = datetime.datetime(1970, 1, 1)
    d._to_date = datetime.datetime.now()
    d.time_type = "ctime"

    files = get_files(d)

    assert l == files


def test_filter_files():
    from pyle.pyle import _filter_files

    files = _filter_files(glob.glob("*.py"))

    assert files == ["__init__.py", "pyle.py", "test_pyle.py"]


def test_filter_files_type_time():
    from pyle.pyle import _filter_files

    for t in ["atime", "mtime", "ctime"]:
        files = _filter_files(glob.glob("*.py"), type_time=t)
        assert files == ["__init__.py", "pyle.py", "test_pyle.py"]


def test_filter_files_empty_1():
    import datetime
    from pyle.pyle import _filter_files

    files = _filter_files(
        glob.glob("*.py"),
        from_time=datetime.datetime(1970, 1, 1),
        to_time=datetime.datetime(1970, 1, 2),
    )

    assert files == []


def test_filter_files_empty_2():
    import datetime
    from pyle.pyle import _filter_files

    files = _filter_files(glob.glob("*.py"), to_time=datetime.datetime(1970, 1, 2))

    assert files == []


def test_filter_files_empty_3():
    import datetime
    from pyle.pyle import _filter_files

    for t in ["atime", "mtime", "ctime"]:
        files = _filter_files(
            glob.glob("*.py"), to_time=datetime.datetime(1970, 1, 2), type_time=t
        )
        assert files == []