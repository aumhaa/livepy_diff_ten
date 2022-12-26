from __future__ import absolute_import, print_function, unicode_literals
from Live.Sample import SlicingStyle
from ...base import delete_notes_with_pitch, depends, listens, liveobj_changed, liveobj_valid, task
from ..controls import ButtonControl
from ..skin import LiveObjSkinEntry
from . import Pageable, PageComponent, PlayableComponent
DEFAULT_SIMPLER_TRANSLATION_CHANNEL = 14
BASE_SLICING_NOTE = 36

class SlicedSimplerComponent(PlayableComponent, PageComponent, Pageable):
    delete_button = ButtonControl(color=None)
    position_count = 16
    page_length = 4
    page_offset = 0

    @depends(target_track=None)
    def __init__(self, name='Sliced_Simpler', translation_channel=DEFAULT_SIMPLER_TRANSLATION_CHANNEL, target_track=None, *a, **k):
        self._position = 0
        self._simpler_device = None
        (super().__init__)(a, name=name, scroll_skin_name='SlicedSimpler.Scroll', **k)
        self._target_track = target_track
        self._translation_channel = translation_channel

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, index):
        self._position = index
        self.notify_position()
        self._update_led_feedback()
        self._update_note_translations()

    def can_scroll_page_up(self):
        if not liveobj_valid(self._simpler_device) or (self._position + 1) * self.page_length > len(self._slices()):
            return False
        return super().can_scroll_page_up()

    def set_scroll_encoder(self, encoder):
        self._position_scroll.set_scroll_encoder(encoder)

    def set_simpler_device(self, simpler_device):
        if liveobj_changed(simpler_device, self._simpler_device):
            self._simpler_device = simpler_device
            self._SlicedSimplerComponent__on_file_changed.subject = simpler_device
            self._SlicedSimplerComponent__on_selected_slice_changed.subject = simpler_device
            self._SlicedSimplerComponent__on_pad_slicing_changed.subject = simpler_device
            sample = simpler_device.sample if liveobj_valid(simpler_device) else None
            self._SlicedSimplerComponent__on_slices_changed.subject = sample
            self._SlicedSimplerComponent__on_slicing_style_changed.subject = sample
            self._SlicedSimplerComponent__on_track_color_changed.subject = self._target_track.target_track if simpler_device else None
            self._update_led_feedback()
            self.update()
        if not liveobj_valid(self._simpler_device):
            self._update_led_feedback()
            self.update()

    def _on_matrix_pressed(self, button):
        if self._simpler_setup_is_valid():
            slice_index = self._coordinate_to_slice_index(button.coordinate)
            if self.delete_button.is_pressed:
                button.color = 'SlicedSimpler.PadAction'
                delete_notes_with_pitch(self._target_track.target_clip, button.identifier)
            if self.select_button.is_pressed:
                self._select_slice_at_index(slice_index)
                super()._on_matrix_pressed(button)

    @delete_button.value
    def delete_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    def _select_slice_at_index(self, index):
        slices = self._slices()
        if len(slices) > index:
            try:
                self._simpler_device.view.selected_slice = slices[index]
            except RuntimeError:
                pass

    def _slices(self):
        if self._simpler_setup_is_valid():
            return self._simpler_device.sample.slices
        return []

    def _selected_slice(self):
        if self._simpler_setup_is_valid():
            return self._simpler_device.view.selected_slice
        return -1

    def _should_show_next_slice(self, index, length_of_slices):
        return self._simpler_setup_is_valid() and index == length_of_slices and self._simpler_device.pad_slicing and self._simpler_device.sample.slicing_style == SlicingStyle.manual

    def _simpler_setup_is_valid(self):
        return liveobj_valid(self._simpler_device) and liveobj_valid(self._simpler_device.sample)

    def _update_button_color(self, button):
        index = self._coordinate_to_slice_index(button.coordinate)
        slices = self._slices()
        length_of_slices = len(slices)
        color = 'SlicedSimpler.NoSlice'
        if index < length_of_slices:
            color = 'SlicedSimpler.SliceSelected' if slices[index] == self._selected_slice() else 'SlicedSimpler.SliceNotSelected'
        elif self._should_show_next_slice(index, length_of_slices):
            color = 'SlicedSimpler.NextSlice'
        button.color = LiveObjSkinEntry(color, self._target_track.target_track)

    def _note_translation_for_button(self, button):
        identifier = BASE_SLICING_NOTE + self._coordinate_to_slice_index(button.coordinate)
        return (
         identifier, self._translation_channel)

    def _coordinate_to_slice_index(self, coordinate):
        y, x = coordinate
        y = self.height - y - 1
        y += self._position
        y += self.height if x >= 4 else 0
        return x % 4 + y * 4

    @listens('sample')
    def __on_file_changed(self):
        self._SlicedSimplerComponent__on_slices_changed.subject = self._simpler_device.sample if liveobj_valid(self._simpler_device) else None
        self._update_led_feedback()

    @listens('view.selected_slice')
    def __on_selected_slice_changed(self):
        self._update_led_feedback()

    @listens('pad_slicing')
    def __on_pad_slicing_changed(self):
        self._update_led_feedback()

    @listens('slices')
    def __on_slices_changed(self):
        self._update_led_feedback()

    @listens('slicing_style')
    def __on_slicing_style_changed(self):

        def set_pad_slicing():
            self._simpler_device.pad_slicing = self._simpler_device.sample.slicing_style == SlicingStyle.manual

        self._tasks.add(task.sequence(task.delay(1), task.run(set_pad_slicing)))

    @listens('color_index')
    def __on_track_color_changed(self):
        self._update_led_feedback()