from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import old_hasattr

def is_real_control_surface(lom_object):
    import _Framework.ControlSurface as ControlSurface
    import ableton.v2.control_surface as ControlSurface2
    return isinstance(lom_object, (ControlSurface, ControlSurface2))


class WrapperRegistry(object):

    def __init__(self, *a, **k):
        (super(WrapperRegistry, self).__init__)(*a, **k)
        self._wrapper_registry = {}

    def wrap(self, obj):
        if is_real_control_surface(obj):
            try:
                return self._wrapper_registry[obj]
            except KeyError:
                wrapped = ControlSurfaceWrapper(control_surface=obj)
                self._wrapper_registry[obj] = wrapped
                obj.add_disconnect_listener(self._WrapperRegistry__on_control_surface_disconnected)
                return wrapped

            return obj

    def __on_control_surface_disconnected(self, unwrapped_cs):
        try:
            unwrapped_cs.remove_disconnect_listener(self._WrapperRegistry__on_control_surface_disconnected)
            self._wrapper_registry[unwrapped_cs].disconnect()
            del self._wrapper_registry[unwrapped_cs]
        except KeyError:
            pass


class ControlSurfaceWrapper(object):

    def __init__(self, control_surface=None, *a, **k):
        (super(ControlSurfaceWrapper, self).__init__)(*a, **k)
        self._control_surface = control_surface
        self._grabbed_controls = []

    @property
    def __doc__(self):
        return self._control_surface.__doc__

    def set_control_element(self, control, grabbed):
        if old_hasattr(control, 'release_parameter'):
            control.release_parameter()
        control.reset()

    def disconnect(self):
        for control in self._grabbed_controls:
            with self._control_surface.component_guard():
                control.resource.release(self)

    def __getattr__(self, name):
        return getattr(self._control_surface, name)

    def __setattr__(self, name, value):
        if name not in ('_control_surface', '_grabbed_controls'):
            setattr(self._control_surface, name, value)
        else:
            super(ControlSurfaceWrapper, self).__setattr__(name, value)

    def __eq__(self, other):
        return self._control_surface == other

    def __hash__(self):
        return hash(self._control_surface)

    @property
    def type_name(self):
        return self._control_surface.__class__.__name__

    @property
    def control_names(self):
        return [control.name for control in self._control_surface.controls if old_hasattr(control, 'name') if control.name]

    def has_control(self, control):
        return control in self._control_surface.controls

    def get_control_by_name(self, control_name):
        for control in self._control_surface.controls:
            if old_hasattr(control, 'name'):
                if control.name == control_name:
                    return control

    def grab_control(self, control):
        if control not in self._grabbed_controls:
            with self._control_surface.component_guard():
                priority = self._control_surface.mxd_grab_control_priority() if old_hasattr(self._control_surface, 'mxd_grab_control_priority') else 1
                control.resource.grab(self, priority=priority)
                if old_hasattr(control, 'suppress_script_forwarding'):
                    control.suppress_script_forwarding = False
                self._grabbed_controls.append(control)

    def release_control(self, control):
        if control in self._grabbed_controls:
            with self._control_surface.component_guard():
                self._grabbed_controls.remove(control)
                control.resource.release(self)