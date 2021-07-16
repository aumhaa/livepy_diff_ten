from __future__ import absolute_import, print_function, unicode_literals
import _Arturia.SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):

    def set_selected_scene_launch_button(self, button):
        self.selected_scene().set_launch_button(button)