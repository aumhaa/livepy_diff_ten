from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb

class Colors:

    class DefaultButton:
        On = Rgb.GREEN
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Recording:
        On = Rgb.RED
        Off = Rgb.RED_HALF
        Transition = Rgb.RED_BLINK
        CaptureTriggered = Rgb.WHITE

    class Transport:
        PlayOff = Mono.OFF
        PlayOn = Mono.ON
        ContinueOff = Mono.OFF
        ContinueOn = Mono.HALF
        CaptureOff = Mono.OFF
        CaptureOn = Mono.HALF

    class Session:
        RecordButton = Rgb.RED_HALF
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipEmpty = Rgb.BLACK
        Scene = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF
        Navigation = Rgb.WHITE_HALF
        NavigationPressed = Rgb.WHITE

    class Mixer:
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        MuteOn = Rgb.YELLOW_HALF
        MuteOff = Rgb.YELLOW
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        EmptyTrack = Rgb.BLACK

    class DrumGroup:
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.DARK_ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        Navigation = Rgb.YELLOW_HALF
        NavigationPressed = Rgb.YELLOW

    class Mode:

        class Volume:
            On = Rgb.GREEN
            Off = Rgb.WHITE_HALF

        class Pan:
            On = Rgb.ORANGE
            Off = Rgb.WHITE_HALF

        class SendA:
            On = Rgb.VIOLET
            Off = Rgb.WHITE_HALF

        class SendB:
            On = Rgb.DARK_BLUE
            Off = Rgb.WHITE_HALF

        class Stop:
            On = Rgb.RED
            Off = Rgb.WHITE_HALF

        class Mute:
            On = Rgb.YELLOW
            Off = Rgb.WHITE_HALF

        class Solo:
            On = Rgb.BLUE
            Off = Rgb.WHITE_HALF

        class Arm:
            On = Rgb.RED
            Off = Rgb.WHITE_HALF

        class Launch:
            On = Rgb.WHITE_HALF


skin = Skin(Colors)
