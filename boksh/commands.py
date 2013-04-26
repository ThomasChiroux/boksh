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

import urwid

import boksh
from boksh.bookmark_menu import SshBookMark


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version="%(prog)s " + boksh.__version__)
    parser.add_argument('-f', '--file',
                        default="~/.bokshrc.json",
                        help="rc file, json format (default: ~/.bokshrc.json")

    args = parser.parse_args()

    file_d = open(args.file)
    bokshrc = json.load(expanduser(file_d))
    file_d.close()
    top = SshBookMark(bokshrc)
    urwd = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
    top.urwd = urwd
    urwd.run()


if __name__ == "__main__":
    main()
