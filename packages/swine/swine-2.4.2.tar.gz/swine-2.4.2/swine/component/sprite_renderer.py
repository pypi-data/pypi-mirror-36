#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

import pymunk
import pyglet.sprite

from swine.component.physics import RigidBody
from swine.object.component import Component
import swine.graphics


class SpriteRenderer(Component):
    def __init__(self, image: swine.graphics.Sprite, scale: int = 1):
        Component.__init__(self)
        self.image = image
        self.scale = scale

        self.sprite: swine.graphics.Sprite = None

    def start(self):
        self.sprite = pyglet.sprite.Sprite(self.image.sprite, batch=self.parent.scene.batch)
        self.sprite.scale = self.scale

    def physics_update(self, dt):
        rigid = self.parent.get_component(RigidBody)

        if rigid is not None:
            body = rigid.body
            self.sprite.rotation = math.degrees(-body.angle)
            self.sprite.position = pymunk.Vec2d(body.position.x, body.position.y)
