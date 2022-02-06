from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as UndoRedoComponentBase

class UndoRedoComponent(UndoRedoComponentBase):

    def __init__(self, name='Undo_Redo', *a, **k):
        (super().__init__)(a, name=name, **k)
        self.undo_button.color = 'UndoRedo.Undo'
        self.undo_button.pressed_color = 'UndoRedo.UndoPressed'
        self.redo_button.color = 'UndoRedo.Redo'
        self.redo_button.pressed_color = 'UndoRedo.RedoPressed'