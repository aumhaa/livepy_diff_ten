from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from .Colors import Rgb

class Colors:

    class Session:
        ClipEmpty = Rgb.BLACK
        ClipStopped = Rgb.GREEN_HALF
        ClipStarted = Rgb.GREEN
        ClipRecording = Rgb.RED
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        NoScene = Rgb.BLACK
        Scene = Rgb.BLUE_HALF
        SceneTriggered = Rgb.BLUE_BLINK
        ScenePlaying = Rgb.BLUE
        StopClip = Rgb.RED
        StopClipTriggered = Rgb.RED_BLINK


def make_default_skin():
    return Skin(Colors)
