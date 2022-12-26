from __future__ import absolute_import, print_function, unicode_literals
from ...base import MultiSlot
from .. import Component
from ..controls import ToggleButtonControl

class ViewToggleComponent(Component):
    main_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.SessionOff',
      toggled_color='ViewToggle.SessionOn')
    detail_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.DetailOff',
      toggled_color='ViewToggle.DetailOn')
    clip_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.ClipOff',
      toggled_color='ViewToggle.ClipOn')
    browser_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.BrowserOff',
      toggled_color='ViewToggle.BrowserOn')

    def __init__(self, name='View_Toggle', *a, **k):
        (super().__init__)(a, name=name, **k)
        for view_name in ('Session', 'Detail', 'Detail/Clip', 'Browser'):
            self.register_slot(MultiSlot(subject=(self.application.view),
              listener=(self._ViewToggleComponent__update_view_toggle_buttons),
              event_name_list=('is_view_visible', ),
              extra_args=(
             view_name,)))

        self._ViewToggleComponent__update_view_toggle_buttons()

    @main_view_toggle_button.toggled
    def main_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Session')

    @detail_view_toggle_button.toggled
    def detail_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail')

    @clip_view_toggle_button.toggled
    def clip_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail/Clip')

    @browser_view_toggle_button.toggled
    def browser_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Browser')

    def _show_or_hide_view(self, show_view, view_name):
        if show_view:
            self.application.view.show_view(view_name)
        else:
            self.application.view.hide_view(view_name)

    def __update_view_toggle_buttons(self):
        view = self.application.view
        self.main_view_toggle_button.is_toggled = view.is_view_visible('Session')
        self.detail_view_toggle_button.is_toggled = view.is_view_visible('Detail')
        self.clip_view_toggle_button.is_toggled = view.is_view_visible('Detail/Clip')
        self.browser_view_toggle_button.is_toggled = view.is_view_visible('Browser')