from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as DrumGroupComponentBase
from ...base import add_scroll_encoder, depends, liveobj_valid, skin_scroll_buttons
from .playable import PlayableComponent
DEFAULT_TRANSLATION_CHANNEL = 15

class DrumGroupComponent(DrumGroupComponentBase):

    @depends(full_velocity=None)
    def __init__(self, name='Drum_Group', translation_channel=DEFAULT_TRANSLATION_CHANNEL, full_velocity=None, is_private=True, *a, **k):
        (super().__init__)(a, name=name, translation_channel=translation_channel, **k)
        self.is_private = is_private
        self._accent_component.is_private = is_private
        self.mute_button.color = 'DrumGroup.Mute'
        self.mute_button.pressed_color = 'DrumGroup.MutePressed'
        self.solo_button.color = 'DrumGroup.Solo'
        self.solo_button.pressed_color = 'DrumGroup.SoloPressed'
        add_scroll_encoder(self._position_scroll)
        for scroll in (self._position_scroll, self._page_scroll):
            skin_scroll_buttons(scroll, 'DrumGroup.Scroll', 'DrumGroup.ScrollPressed')

        self.set_full_velocity(full_velocity)

    def set_scroll_encoder(self, encoder):
        self._position_scroll.scroll_encoder.set_control_element(encoder)

    def set_drum_group_device(self, drum_group_device):
        super().set_drum_group_device(drum_group_device)
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

    def _update_led_feedback(self):
        PlayableComponent._update_led_feedback(self)

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        button.color = self._color_for_pad(pad) if pad else 'DrumGroup.PadEmpty'

    def _color_for_pad(self, pad):
        button_color = 'DrumGroup.PadEmpty'
        if pad == self._selected_drum_pad:
            button_color = 'DrumGroup.PadSelected'
            if pad.mute:
                button_color = 'DrumGroup.PadMutedSelected'
            elif pad.solo:
                button_color = 'DrumGroup.PadSoloedSelected'
        elif pad.chains:
            button_color = 'DrumGroup.PadFilled'
            if pad.mute:
                button_color = 'DrumGroup.PadMuted'
            elif pad.solo:
                button_color = 'DrumGroup.PadSoloed'
        return button_color

    def _button_coordinates_to_pad_index(self, first_note, coordinates):
        y, x = coordinates
        inverted_y = self.height - y - 1
        index = first_note + 4 * inverted_y + x
        if x >= 4:
            index += y * 4 + inverted_y * 4
        return index