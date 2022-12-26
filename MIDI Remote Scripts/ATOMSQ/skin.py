from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import BasicColors, Skin, default_skin, merge_skins
from .colors import Rgb

class Colors:

    class DefaultButton:
        On = Rgb.ON
        Off = Rgb.OFF
        Disabled = Rgb.OFF

    class Transport:
        PlayOn = Rgb.GREEN
        PlayOff = Rgb.GREEN_DIM
        LoopOn = Rgb.GREEN
        LoopOff = Rgb.GREEN_DIM

    class Mixer:
        Selected = Rgb.ON
        NotSelected = Rgb.OFF

    class Session:
        Slot = Rgb.OFF
        SlotRecordButton = Rgb.RED_HALF
        NoSlot = Rgb.OFF
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStopped = BasicColors.ON
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        Scene = Rgb.GREEN_HALF
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.OFF
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF

    class ViewToggle:
        DetailOn = Rgb.YELLOW
        DetailOff = Rgb.YELLOW_HALF
        SessionOn = Rgb.BLUE
        SessionOff = Rgb.BLUE_HALF
        ClipOn = Rgb.PURPLE
        ClipOff = Rgb.PURPLE_HALF
        BrowserOn = Rgb.GREEN
        BrowserOff = Rgb.GREEN_HALF


skin = merge_skins(default_skin, Skin(Colors))