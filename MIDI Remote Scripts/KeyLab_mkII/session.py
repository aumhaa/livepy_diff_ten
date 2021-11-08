from __future__ import absolute_import, print_function, unicode_literals
import KeyLab_Essential.session as SceneComponentBase
import KeyLab_Essential.session as SessionComponentBase
from .clip_slot import ClipSlotComponent

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent