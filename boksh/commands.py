#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
#
import argparse
import json
from os.path import expanduser
import glob

import urwid

import boksh
from boksh.bookmark_menu import SshBookMark
from boksh.tools import merge_dicts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version="%(prog)s " + boksh.__version__)
    parser.add_argument(
        '-f', '--file',
        default="~/.config/boksh/*.json",
        help="rc file, json format (default: ~/.config/boksh/*.json")

    args = parser.parse_args()

    files = glob.glob(expanduser(args.file))
    bokshrc = {}
    for file_name in files:
        file_d = open(file_name)
        bokshrc = merge_dicts(bokshrc, json.load(file_d))
        file_d.close()

    top = SshBookMark(bokshrc)
    urwd = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
    top.urwd = urwd
    urwd.run()


if __name__ == "__main__":
    main()
