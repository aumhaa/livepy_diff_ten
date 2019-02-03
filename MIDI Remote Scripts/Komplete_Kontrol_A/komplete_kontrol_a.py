from __future__ import absolute_import, print_function, unicode_literals
from _Komplete_Kontrol.komplete_kontrol_base import NUM_TRACKS, KompleteKontrolBase, ButtonMatrixElement, Layer, create_button, create_display_line, sysex

class Komplete_Kontrol_A(KompleteKontrolBase):

    def _create_controls(self):
        super(Komplete_Kontrol_A, self)._create_controls()
        self._mute_button = create_button(67, u'Mute_Button')
        self._solo_button = create_button(68, u'Solo_Button')
        self._track_volume_displays = ButtonMatrixElement(rows=[[ create_display_line(sysex.TRACK_VOLUME_DISPLAY_HEADER, index, u'Track_Volume_Display_{}'.format(index), width=12) for index in xrange(NUM_TRACKS) ]], name=u'Track_Volume_Displays')
        self._track_panning_displays = ButtonMatrixElement(rows=[[ create_display_line(sysex.TRACK_PANNING_DISPLAY_HEADER, index, u'Track_Panning_Display_{}'.format(index), width=12) for index in xrange(NUM_TRACKS) ]], name=u'Track_Panning_Displays')

    def _create_mixer_component_layer(self):
        return super(Komplete_Kontrol_A, self)._create_mixer_component_layer() + Layer(mute_button=self._mute_button, solo_button=self._solo_button, track_volume_displays=self._track_volume_displays, track_panning_displays=self._track_panning_displays)
