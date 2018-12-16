from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Control import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection

class DeviceNavigationComponent(ControlSurfaceComponent):
    device_nav_left_button = ButtonControl()
    device_nav_right_button = ButtonControl()

    @device_nav_left_button.pressed
    def device_nav_left_button(self, value):
        self._scroll_device_chain(NavDirection.left)

    @device_nav_right_button.pressed
    def device_nav_right_button(self, value):
        self._scroll_device_chain(NavDirection.right)

    def _scroll_device_chain(self, direction):
        view = self.application().view
        if not view.is_view_visible(u'Detail') or not view.is_view_visible(u'Detail/DeviceChain'):
            view.show_view(u'Detail')
            view.show_view(u'Detail/DeviceChain')
        else:
            view.scroll_view(direction, u'Detail/DeviceChain', False)
