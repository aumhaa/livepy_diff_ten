from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as DrumGroupComponentBase
from ...base import add_scroll_encoder, const, depends, listens_group, liveobj_valid, skin_scroll_buttons
from ..controls import ButtonControl, PlayableControl, control_matrix
DEFAULT_DRUM_TRANSLATION_CHANNEL = 15

class DrumGroupComponent(DrumGroupComponentBase):
    matrix = control_matrix(PlayableControl, color=None)
    select_button = ButtonControl(color=None)
    mute_button = ButtonControl(color=None)
    solo_button = ButtonControl(color=None)
    delete_button = ButtonControl(color=None)
    quantize_button = ButtonControl(color=None)

    @depends(full_velocity=None, color_for_liveobj_function=(const(None)))
    def __init__(self, name='Drum_Group', translation_channel=DEFAULT_DRUM_TRANSLATION_CHANNEL, full_velocity=None, color_for_liveobj_function=None, is_private=True, *a, **k):
        (super().__init__)(a, name=name, translation_channel=translation_channel, **k)
        self.is_private = is_private
        self._accent_component.is_private = is_private
        self._color_for_liveobj_function = color_for_liveobj_function
        add_scroll_encoder(self._position_scroll)
        for scroll in (self._position_scroll, self._page_scroll):
            skin_scroll_buttons(scroll, 'DrumGroup.Scroll', 'DrumGroup.ScrollPressed')

        self.set_full_velocity(full_velocity)

    def set_matrix(self, matrix):
        self.matrix.set_control_element(matrix)
        self._reset_selected_pads()
        self._update_led_feedback()
        self._update_assigned_drum_pads()
        self._create_and_set_pad_translations()

    def set_scroll_encoder(self, encoder):
        self._position_scroll.scroll_encoder.set_control_element(encoder)

    def set_drum_group_device(self, drum_group_device):
        super().set_drum_group_device(drum_group_device)
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

    @matrix.pressed
    def matrix(self, button):
        self._on_matrix_pressed(button)

    @matrix.released
    def matrix(self, button):
        self._on_matrix_released(button)

    @select_button.value
    def select_button(self, value, _):
        self._set_control_pads_from_script(bool(value))

    @mute_button.value
    def mute_button(self, value, _):
        self._set_control_pads_from_script(bool(value))

    @solo_button.value
    def solo_button(self, value, _):
        self._set_control_pads_from_script(bool(value))

    @delete_button.value
    def delete_button(self, value, _):
        self._set_control_pads_from_script(bool(value))

    @quantize_button.value
    def quantize_button(self, value, _):
        self._set_control_pads_from_script(bool(value))

    def quantize_pitch(self, note):
        pass

    def delete_pitch(self, drum_pad):
        pass

    def select_drum_pad(self, drum_pad):
        pass

    def _on_matrix_pressed(self, button):
        if liveobj_valid(self._drum_group_device):
            super()._on_matrix_pressed(button)

    @listens_group('color')
    def __on_color_changed(self, _):
        self._update_led_feedback()

    def _update_drum_pad_listeners(self):
        super()._update_drum_pad_listeners()
        if liveobj_valid(self._drum_group_device):
            visible_drum_pads = self._drum_group_device.visible_drum_pads
            self._DrumGroupComponent__on_color_changed.replace_subjects((pad.chains[0] for pad in visible_drum_pads if pad.chains))

    def _update_led_feedback(self):
        for button in self.matrix:
            self._update_button_color(button)

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
            if pad.mute:
                button_color = 'DrumGroup.PadMuted'
            elif pad.solo:
                button_color = 'DrumGroup.PadSoloed'
            else:
                button_color = self._filled_color(pad)
        return button_color

    def _filled_color(self, pad):
        color = None
        if self._color_for_liveobj_function:
            color = self._color_for_liveobj_function(pad.chains[0])
        if color is not None:
            return color
        return 'DrumGroup.PadFilled'

    def _button_coordinates_to_pad_index(self, first_note, coordinates):
        y, x = coordinates
        inverted_y = self.height - y - 1
        index = first_note + 4 * inverted_y + x
        if x >= 4:
            index += y * 4 + inverted_y * 4
        return index