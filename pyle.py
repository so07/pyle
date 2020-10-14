#!/usr/bin/env python3
#
# Copyright 2015 so07
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = "so07"
__version__ = "0.1.1"

import os
import glob
import datetime
import time
import argparse


fmt_day = "%Y-%m-%d"
fmt_time = "%H:%M:%S"
fmt_daytime = fmt_day + " " + fmt_time


def _date(s):
    for fmt in fmt_day, fmt_time, fmt_daytime:
        try:
            return datetime.datetime.strptime(s, fmt)
        except:
            pass
    else:
        raise ValueError("invalid date {}".format(s))


def _filter_files(
    files,
    from_time=datetime.datetime(1970, 1, 1),
    to_time=datetime.datetime.now(),
    type_time="ctime",
):
    """return list of files in the data range"""
    list_files = []
    for f in files:
        l = sorted(
            glob.glob(f), key=lambda filename: getattr(os.stat(filename), "st_ctime")
        )
        for file in l:
            file_time = getattr(os.stat(file), "st_" + type_time)
            file_date = datetime.datetime(*time.localtime(file_time)[:6])
            if from_time <= file_date <= to_time:
                list_files.append(file)
    return list_files


def get_files(args):

    if isinstance(args, argparse.Namespace):
        _files = args.pyle_files
        _from_date = args.from_date
        _to_date = args.to_date
        _time_type = args.time_type

    if isinstance(args, dict):
        _files = args["pyle_files"]
        _from_date = args["from_date"]
        _to_date = args["to_date"]
        _time_type = args["time_type"]

    return _filter_files(_files, _from_date, _to_date, _time_type)


def add_pyle_parser(parser, name="File", help=None):

    pyle_parser = parser.add_argument_group(name + " options")

    pyle_parser.add_argument(
        "--from-date",
        type=_date,
        default=datetime.datetime(1970, 1, 1).strftime(fmt_daytime),
        metavar="YYYY-MM-DD HH:MM:SS",
        help="select files after YYYY-MM-DD HH:MM:SS",
    )

    pyle_parser.add_argument(
        "--to-date",
        type=_date,
        default=datetime.datetime.now().strftime(fmt_daytime),
        metavar="YYYY-MM-DD HH:MM:SS",
        help="select files before YYYY-MM-DD HH:MM:SS",
    )

    default_time_type = "ctime"

    pyle_parser.add_argument(
        "--mtime",
        dest="time_type",
        action="store_const",
        const="mtime",
        default=default_time_type,
        help="use modification time",
    )

    pyle_parser.add_argument(
        "--atime",
        dest="time_type",
        action="store_const",
        const="atime",
        default=default_time_type,
        help="use access time",
    )

    pyle_parser.add_argument(
        "--ctime",
        dest="time_type",
        action="store_const",
        const="ctime",
        default=default_time_type,
        help="use status change time",
    )

    if help:
        files_help = help
    else:
        files_help = "List of " + name

    # Positional parameters
    parser.add_argument(
        "pyle_files", default=[], nargs="+", metavar=name, help=files_help
    )


def add_parser(parser, name="File", help=None):
    add_pyle_parser(parser, name, help)


def main(args):
    print("Files:", get_files(args))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="pyle",
        description="files management",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    add_parser(parser)

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="show version and exit",
    )

    args = parser.parse_args()

    main(args)
