import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler
import readline
import re


class Dialogs:
    def __init__(
            self, 
            pad_right                 = 0,
            indent                    = 0,
            align                     = 0,
            margin                    = 0,
            shift                     = 0,
            bullet                    = '>', 
            check                     = '#', 
            word_color                = colors.foreground["default"],
            word_on_switch            = colors.REVERSE,
            background_color          = colors.background["default"],
            background_on_switch      = colors.REVERSE,
            bullet_color              = colors.foreground["default"],
            check_color               = colors.foreground["default"],
            check_on_switch           = colors.REVERSE,
        ):

        if indent < 0:
            raise ValueError("Indent must be > 0!")
        if margin < 0:
            raise ValueError("Margin must be > 0!")

        self.indent = indent
        self.align = align
        self.margin = margin
        self.shift = shift
        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.pad_right = pad_right
        self.bullet = bullet
        self.bullet_color = bullet_color
        self.check = check
        self.check_color = check_color
        self.check_on_switch = check_on_switch

    def optone(self, prompt='', choices=[], default=None):
        if not choices:
            raise ValueError('Choices can not be empty!')
        if prompt:
            utils.forceWrite(' ' * self.indent + prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if default is None:
            default = choices[0]
        else:
            if not default in choices:
                raise ValueError('`default` should be an element of `choices`!')
        return OptOne(self, choices, default).launch()

    def optany(self, prompt='', choices=[], default=None):
        if not choices:
            raise ValueError("Choices can not be empty!")
        if prompt:
            utils.forceWrite(' ' * self.indent + prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if default is None:
            default = []
        else:
            if not type(default).__name__ == 'list':
                raise TypeError('`default` should be a list!')
            if not all([i in choices for i in default]):
                raise ValueError('`default` should be a subset of `choices`!')
        return OptAny(self, choices, default).launch()


@keyhandler.init
class OptOne:
    def __init__(self, itself, choices, default):
        self.indent = itself.indent
        self.align = itself.align
        self.margin = itself.margin
        self.shift = itself.shift
        self.bullet = itself.bullet
        self.bullet_color = itself.bullet_color
        self.word_color = itself.word_color
        self.word_on_switch = itself.word_on_switch
        self.background_color = itself.background_color
        self.background_on_switch = itself.background_on_switch
        self.max_width = len(max(choices, key = len)) + itself.pad_right
        self.choices = choices
        self.pos = choices.index(default)

    def renderBullets(self):
        for i in range(len(self.choices)):
            self.printBullet(i)
            utils.forceWrite('\n')
            
    def printBullet(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        if idx == self.pos:
            utils.cprint("{}".format(self.bullet) + " " * self.margin, self.bullet_color, back_color, end = '')
        else:
            utils.cprint(" " * (len(self.bullet) + self.margin), self.bullet_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()

    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos - 1 < 0:
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            self.printBullet(old_pos)
            utils.moveCursorUp(1)
            self.printBullet(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.choices):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.printBullet(old_pos)
            utils.moveCursorDown(1)
            self.printBullet(self.pos)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        ret = self.choices[self.pos]
        self.pos = 0
        return ret

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        raise KeyboardInterrupt

    def launch(self):
        self.renderBullets()
        utils.moveCursorUp(len(self.choices) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret


@keyhandler.init
class OptAny:
    def __init__(self, itself, choices, default):
        self.indent = itself.indent
        self.align = itself.align
        self.margin = itself.margin
        self.shift = itself.shift
        self.check = itself.check
        self.check_color = itself.check_color
        self.check_on_switch = itself.check_on_switch
        self.word_color = itself.word_color
        self.word_on_switch = itself.word_on_switch
        self.background_color = itself.background_color
        self.background_on_switch = itself.background_on_switch
        self.max_width = len(max(choices, key = len)) + itself.pad_right
        self.checked = [ True if i in default else False for i in choices ]
        self.choices = choices
        self.pos = 0

    def renderRows(self):
        for i in range(len(self.choices)):
            self.printRow(i)
            utils.forceWrite('\n')
            
    def printRow(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        check_color = self.check_on_switch if idx == self.pos else self.check_color
        if self.checked[idx]:
            utils.cprint("{}".format(self.check) + " " * self.margin, check_color, back_color, end = '')
        else:
            utils.cprint(" " * (len(self.check) + self.margin), check_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()

    @keyhandler.register(SPACE_CHAR)
    def toggleRow(self):
        self.checked[self.pos] = not self.checked[self.pos]
        self.printRow(self.pos)

    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos - 1 < 0:
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            self.printRow(old_pos)
            utils.moveCursorUp(1)
            self.printRow(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.choices):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.printRow(old_pos)
            utils.moveCursorDown(1)
            self.printRow(self.pos)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        ret = [self.choices[i] for i in range(len(self.choices)) if self.checked[i]]
        self.pos = 0
        self.checked = [False] * len(self.choices)
        return ret

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        raise KeyboardInterrupt

    def launch(self):
        self.renderRows()
        utils.moveCursorUp(len(self.choices))
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret
