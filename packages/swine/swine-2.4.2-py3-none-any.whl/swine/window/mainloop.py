#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyglet
from pyglet.app.base import EventLoop


class Mainloop(EventLoop):
    def __init__(self):
        EventLoop.__init__(self)

    def idle(self):
        dt = self.clock.update_time()
        self.clock.call_scheduled_functions(dt)

        try:
            for window in pyglet.app.windows:
                try:
                    window.switch_to()
                    window.dispatch_events()
                    window.dispatch_event('on_draw')
                    window.flip()

                except AttributeError:
                    pass

        except RuntimeError:
            pass

        return self.clock.get_sleep_time(True)
