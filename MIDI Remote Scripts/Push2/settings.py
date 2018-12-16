from __future__ import absolute_import, print_function, unicode_literals
from pushbase.setting import OnOffSetting

def create_settings(preferences = None):
    preferences = preferences if preferences is not None else {}
    return {u'workflow': OnOffSetting(name=u'Workflow', value_labels=[u'Scene', u'Clip'], default_value=True, preferences=preferences)}
