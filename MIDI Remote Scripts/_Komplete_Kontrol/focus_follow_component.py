from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
import Live
from ableton.v2.base import listens, listens_group, liveobj_valid
from ableton.v2.control_surface import Component, find_instrument_devices, find_instrument_meeting_requirement
from ableton.v2.control_surface.control import SendValueControl
KK_NAME_PREFIX = u'Komplete Kontrol'

class FocusFollowComponent(Component):
    focus_follow_control = SendValueControl()

    def __init__(self, *a, **k):
        super(FocusFollowComponent, self).__init__(*a, **k)
        self._track = None
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        track = self.song.view.selected_track
        self._track = track if track.has_midi_input else None
        self.update()

    @listens_group(u'chains')
    def __on_chains_changed(self, _):
        self.update()

    @listens_group(u'devices')
    def __on_devices_changed(self, _):
        self.update()

    def update(self):
        super(FocusFollowComponent, self).update()
        self._update_listeners()
        self._update_komplete_kontrol_instance()

    def _update_listeners(self):
        devices = list(find_instrument_devices(self._track))
        racks = filter(lambda d: d.can_have_chains, devices)
        chains = list(chain([self._track], *[ d.chains for d in racks ]))
        self.__on_chains_changed.replace_subjects(racks)
        self.__on_devices_changed.replace_subjects(chains)

    def _update_komplete_kontrol_instance(self):
        is_kk_instance = lambda d: isinstance(d, Live.PluginDevice.PluginDevice) and d.name.startswith(KK_NAME_PREFIX)
        instance = find_instrument_meeting_requirement(is_kk_instance, self._track)
        param_name = u''
        if liveobj_valid(instance):
            param_name = instance.get_parameter_names(end=1)[0]
        self.focus_follow_control.value = tuple([ ord(n) for n in param_name ])
