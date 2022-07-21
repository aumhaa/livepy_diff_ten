from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import BasicColors, Skin, default_skin, merge_skins
from .colors import Rgb

class Colors:

    class DefaultButton:
        Disabled = Rgb.BLACK

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        Selected = Rgb.WHITE
        NotSelected = Rgb.BLACK
        Empty = Rgb.BLACK

    class Session:
        ClipEmpty = Rgb.BLACK
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipRecordButton = Rgb.RED_HALF
        Scene = Rgb.GREEN_HALF
        SceneEmpty = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF

    class Zooming:
        Selected = Rgb.WHITE
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class NotePad:
        Pressed = Rgb.RED

    class Keyboard:
        Natural = Rgb.YELLOW
        Sharp = Rgb.BLUE

    class DrumGroup:
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadQuadrant0 = Rgb.BLUE
        PadQuadrant1 = Rgb.GREEN
        PadQuadrant2 = Rgb.YELLOW
        PadQuadrant3 = Rgb.PURPLE
        PadQuadrant4 = Rgb.ORANGE
        PadQuadrant5 = Rgb.LIGHT_BLUE
        PadQuadrant6 = Rgb.PINK
        PadQuadrant7 = Rgb.PEACH

    class EncoderModes:

        class Volume:
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class Pan:
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF

        class SendA:
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF

        class SendB:
            On = Rgb.PURPLE
            Off = Rgb.PURPLE_HALF

    class SessionNavigationModes:

        class Default:
            On = BasicColors.OFF

    class TopLevelModes:

        class Default:
            On = BasicColors.OFF


skin = merge_skins(default_skin, Skin(Colors))