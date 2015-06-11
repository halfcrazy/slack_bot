#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class PluginBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def test(data, bot):
        pass

    @abstractmethod
    def handle(data, bot, kv, app):
        pass
