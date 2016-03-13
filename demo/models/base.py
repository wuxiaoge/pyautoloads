#!usr/bin/env python
# coding: utf-8

from autoloads import Entity, EntityHelper


class BaseModel(Entity, EntityHelper):
    def __init__(self, **kargs):
        Entity.__init__(self, **kargs)
