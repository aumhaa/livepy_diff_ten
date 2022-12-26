from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from typing import NamedTuple
from . import BasicColors
ON_SUFFIXES = ('enabled', 'on', 'pressed', 'selected')

class OptionalSkinEntry(NamedTuple):
    name: str
    fallback_name: str


class Skin:

    def __init__(self, colors=None, *a, **k):
        (super().__init__)(*a, **k)
        self.colors = {}
        if colors is not None:
            self._fill_colors(colors)

    def _fill_colors(self, colors, pathname=''):
        if getattr(colors, '__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base, pathname=pathname)

        for k, v in vars(colors).items():
            if k[:1] != '_':
                if callable(v):
                    self._fill_colors(v, '{}{}.'.format(pathname, k))
                else:
                    self.colors['{}{}'.format(pathname, k)] = v

    def __getitem__(self, key):
        if isinstance(key, OptionalSkinEntry):
            key = key.name if key.name in self.colors else key.fallback_name
        if key not in self.colors:
            if key.lower().endswith(ON_SUFFIXES):
                return BasicColors.ON
            return BasicColors.OFF
        return self.colors[key]


def merge_skins(*skins):
    skin = Skin()
    skin.colors = dict(chain(*map(lambda s: s.colors.items(), skins)))
    return skin