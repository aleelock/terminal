# -*- coding: utf-8 -*-
import os
import sys

# Python 3
if sys.version_info[0] == 3:
    string_type = str
else:
    string_type = basestring


def is_color_supported():
    "Find out if your terminal environment supports color."
    # shinx.util.console
    if not hasattr(sys.stdout, 'isatty'):
        return False

    if not sys.stdout.isatty():
        return False

    if sys.platform == 'win32':
        try:
            import colorama
            colorama.init()
            return True
        except ImportError:
            return False

    if 'COLORTERM' in os.environ:
        return True

    term = os.environ.get('TERM', 'dumb').lower()
    return term in ('xterm', 'linux') or 'color' in term


def is_256color_supported():
    "Find out if your terminal environment supports 256 color."
    if not is_color_supported():
        return False
    term = os.environ.get('TERM', 'dumb').lower()
    return '256' in term


_reset = '\x1b[0;39;49m'


class Color(object):
    def __init__(self, *items):
        self.items = items

        self.styles = []
        self.fgcolor = None
        self.bgcolor = None

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        text = ''.join(unicode(item) for item in self.items)
        if not is_color_supported():
            return text

        is256 = is_256color_supported()
        if is256:
            if self.fgcolor is not None:
                text = '\x1b[38;5;%im%s%s' % (self.fgcolor, text, _reset)
            if self.bgcolor is not None:
                text = '\x1b[48;5;%im%s%s' % (self.bgcolor, text, _reset)

        else:
            if self.fgcolor is not None and self.fgcolor < 8:
                text = '\x1b[%im%s%s' % (30 + self.fgcolor, text, _reset)
            if self.bgcolor is not None and self.bgcolor < 8:
                text = '\x1b[%im%s%s' % (40 + self.bgcolor, text, _reset)

        if self.styles:
            code = ';'.join(str(i) for i in self.styles)
            text = '\x1b[%sm%s%s' % (code, text, _reset)

        return text

    def __repr__(self):
        return repr(unicode(self))

    def __len__(self):
        return sum([len(item) for item in self.items])

    def __add__(self, s):
        if not isinstance(s, (string_type, Color)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(s), type(self)))
        return Color(self, s)

    def __radd__(self, s):
        if not isinstance(s, (string_type, Color)):
            msg = "Concatenatation failed: %r + %r (Not a ColorString or str)"
            raise TypeError(msg % (type(s), type(self)))
        return Color(s, self)


def _create_color_func(text, fgcolor=None, bgcolor=None, *styles):
    c = Color(text)
    c.fgcolor = fgcolor
    c.bgcolor = bgcolor
    c.styles = styles
    return c


def bold(text):
    """
    Bold style.
    """
    return _create_color_func(text, None, None, 1)


def faint(text):
    """
    Faint style.
    """
    return _create_color_func(text, None, None, 2)


def italic(text):
    """
    Italic style.
    """
    return _create_color_func(text, None, None, 3)


def underline(text):
    """
    Underline style.
    """
    return _create_color_func(text, None, None, 4)


def blink(text):
    """
    Blink style.
    """
    return _create_color_func(text, None, None, 5)


def overline(text):
    """
    Overline style.
    """
    return _create_color_func(text, None, None, 6)


def inverse(text):
    """
    Inverse style.
    """
    return _create_color_func(text, None, None, 7)


def conceal(text):
    """
    Conceal style.
    """
    return _create_color_func(text, None, None, 8)


def strike(text):
    """
    Strike style.
    """
    return _create_color_func(text, None, None, 9)


def black(text):
    """
    Black color.
    """
    return _create_color_func(text, fgcolor=0)


def red(text):
    """
    Red color.
    """
    return _create_color_func(text, fgcolor=1)


def green(text):
    """
    Green color.
    """
    return _create_color_func(text, fgcolor=2)


def yellow(text):
    """
    Yellow color.
    """
    return _create_color_func(text, fgcolor=3)


def blue(text):
    """
    Blue color.
    """
    return _create_color_func(text, fgcolor=4)


def magenta(text):
    """
    Magenta color.
    """
    return _create_color_func(text, fgcolor=5)


def cyan(text):
    """
    Cyan color.
    """
    return _create_color_func(text, fgcolor=6)


def white(text):
    """
    White color.
    """
    return _create_color_func(text, fgcolor=7)


def gray(text):
    """
    Gray color.
    """
    if is_256color_supported():
        return _create_color_func(text, fgcolor=8)
    return _create_color_func(text, 0, None, 8)


def grey(text):
    """
    Alias of gray.
    """
    return gray(text)


def black_bg(text):
    """
    Black background.
    """
    return _create_color_func(text, bgcolor=0)


def red_bg(text):
    """
    Red background.
    """
    return _create_color_func(text, bgcolor=1)


def green_bg(text):
    """
    Green background.
    """
    return _create_color_func(text, bgcolor=2)


def yellow_bg(text):
    """
    Yellow background.
    """
    return _create_color_func(text, bgcolor=3)


def blue_bg(text):
    """
    Blue background.
    """
    return _create_color_func(text, bgcolor=4)


def magenta_bg(text):
    """
    Magenta background.
    """
    return _create_color_func(text, bgcolor=5)


def cyan_bg(text):
    """
    Cyan background.
    """
    return _create_color_func(text, bgcolor=6)


def white_bg(text):
    """
    White background.
    """
    return _create_color_func(text, bgcolor=7)


def gray_bg(text):
    """
    Gray background.
    """
    if is_256color_supported():
        return _create_color_func(text, bgcolor=8)
    return _create_color_func(text, None, 0, 1)


def grey_bg(text):
    """
    Alias of gray_bg.
    """
    return gray_bg(text)
