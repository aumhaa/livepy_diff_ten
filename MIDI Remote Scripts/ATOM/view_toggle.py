from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ToggleButtonControl

class ViewToggleComponent(Component):
    detail_view_toggle_button = ToggleButtonControl()
    main_view_toggle_button = ToggleButtonControl()

    def __init__(self, *a, **k):
        (super(ViewToggleComponent, self).__init__)(*a, **k)
        self._ViewToggleComponent__on_detail_view_visibility_changed.subject = self.application.view
        self._ViewToggleComponent__on_main_view_visibility_changed.subject = self.application.view
        self._ViewToggleComponent__on_detail_view_visibility_changed()
        self._ViewToggleComponent__on_main_view_visibility_changed()

    @detail_view_toggle_button.toggled
    def detail_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail')

    @main_view_toggle_button.toggled
    def main_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Session')

    def _show_or_hide_view(self, show_view, view_name):
        if show_view:
            self.application.view.show_view(view_name)
        else:
            self.application.view.hide_view(view_name)

    @listens('is_view_visible', 'Detail')
    def __on_detail_view_visibility_changed(self):
        self.detail_view_toggle_button.is_toggled = self.application.view.is_view_visible('Detail')

    @listens('is_view_visible', 'Session')
    def __on_main_view_visibility_changed(self):
        self.main_view_toggle_button.is_toggled = self.application.view.is_view_visible('Session')