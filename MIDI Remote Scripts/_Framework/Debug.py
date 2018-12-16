from __future__ import absolute_import, print_function, unicode_literals
enable_debug_output = True

def debug_print(*a):
    u""" Special function for debug output """
    if enable_debug_output:
        print(u' '.join(map(str, a)))
