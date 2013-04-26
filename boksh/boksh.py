#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
import argparse
import subprocess
import json

import urwid


class SshBookMark(urwid.WidgetPlaceholder):
    """
    """
    max_box_levels = 4

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
        super(SshBookMark, self).__init__(urwid.SolidFill(u'/'))
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
            body = [urwid.Text("Boksh"), urwid.Divider()]
            for choice in self.menu:
                choices.append(self.menu_button(choice,
                                                self.select_menu))
        else:
            body = [urwid.Text(lvl1_choice), urwid.Divider()]
            for choice in self.menu[lvl1_choice]:
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
            template = self.templates[template_name]
        except KeyError:
            # todo change this with an error box
            print("Unable to find template: %s" % template_name)
        else:
            self.urwd.screen.stop()
            self._runcmds(template['before'])
            self._runcmds(command, echo=True)
            self._runcmds(template['after'])
            self.urwd.screen.start()

    def menu_button(self, caption, callback):
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')

    def open_box(self, box):
        self.original_widget = urwid.Overlay(
            urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
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

    def _runcmds(self, commands, echo=False):
        """ launch command """
        if type(commands) == str or type(commands) == unicode:
            commands = [commands, ]
        for cmd in commands:
            if echo:
                subprocess.call("echo '" + cmd + "'", shell=True)
            subprocess.call(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version="%(prog)s " + 'v0.1alpha')  # todo versionning
    parser.add_argument('-f', '--file',
                        default="~/.bokshrc.json",
                        help="rc file, json format (default: ~/.bokshrc.json")

    args = parser.parse_args()

    file_d = open(args.file)
    bokshrc = json.load(file_d)
    file_d.close()
    top = SshBookMark(bokshrc)
    urwd = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
    top.urwd = urwd
    urwd.run()


if __name__ == "__main__":
    main()