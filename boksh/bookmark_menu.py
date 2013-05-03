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
import subprocess

import urwid
import six

import boksh


class SshBookMark(urwid.WidgetPlaceholder):
    """
    """
    max_box_levels = 2

    def __init__(self, bokshrc):
        """bokshrc is a json file in the form:

        {'templates':
            {'tpl_name':
                {'before': ['shellcommand',
                            'shellcommand'],
                 'after': ['shellcommand',
                            'shellcommand'],
                },
            }
         'menu': {}
        }
        """
        super(SshBookMark, self).__init__(urwid.SolidFill(u'\N{DARK SHADE}'))
        self.urwd = None
        self.box_level = 0
        self.lvl1 = []

        self.templates = bokshrc['templates']
        # todo: change self.menu name
        self.menu = bokshrc['menu']
        self.open_box(self.urwd_menu())

    def urwd_menu(self, lvl1_choice=None):
        choices = []
        if lvl1_choice is None:
            body = [urwid.Text("Boksh %s" % boksh.__version__),
                    urwid.Divider()]
            for choice in sorted(self.menu):
                choices.append(self.menu_button(choice,
                                                self.select_menu))
        else:
            body = [urwid.Text(lvl1_choice), urwid.Divider()]
            for choice in sorted(self.menu[lvl1_choice]):
                choices.append(self.menu_button(choice,
                                                self.select_item))
        body.extend(choices)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def select_menu(self, button, choice=None):
        self.lvl1.append(button.label)
        self.open_box(self.urwd_menu(button.label))

    def select_item(self, button, choice=None):
        print("select item: %s" % button.label)
        command = self.menu[self.lvl1[-1]][button.label]['command']
        template_name = self.menu[self.lvl1[-1]][button.label]['template']
        try:
            name = self.menu[self.lvl1[-1]][button.label]['name']
        except KeyError:
            name = command.split(' ')[-1]
        try:
            template = self.templates[template_name]
        except KeyError:
            # todo change this with an error box
            print("Unable to find template: %s" % template_name)
        else:
            self.urwd.screen.stop()
            self._runcmds(template['before'], name=name)
            self._runcmds(command, name=name, echo=True)
            self._runcmds(template['after'], name=name)
            self.urwd.screen.start()

    def menu_button(self, caption, callback):
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')

    def open_box(self, box):
        self.original_widget = urwid.Overlay(
            urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 90),
            valign='middle', height=('relative', 90),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
            self.lvl1.pop()
            return
        if (key == 'esc' and self.box_level == 1) or key in ['Q', 'q']:
            self.exit_program()
            return

        else:
            return super(SshBookMark, self).keypress(size, key)

    def exit_program(self, button=None):
        raise urwid.ExitMainLoop()

    def _runcmds(self, commands, name=None, echo=False):
        """ launch command """
        if isinstance(commands, six.text_type):
            commands = [commands, ]
        for cmd in commands:
            cmd = cmd.format(name=name)
            if echo:
                subprocess.call("echo '" + cmd + "'", shell=True)
            subprocess.call(cmd, shell=True)
