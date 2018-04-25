#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import platform
import copy

def is_windows():
    return platform.system() == 'Windows'

def is_linux():
    return platform.system() == 'Linux'

if __name__ == "__main__":
    builder = build_template_default.get_builder()
    extended_builds = copy.deepcopy(builder)
    for settings, options, env_vars, build_requires, _ in extended_builds.items:
        options['mosquitto:with_mosquittopp'] = False
        builder.add(settings=settings, options=options, env_vars=env_vars, build_requires=build_requires)
    extended_builds = copy.deepcopy(builder)
    for settings, options, env_vars, build_requires, _ in extended_builds.items:
        options['mosquitto:with_mosquittopp'] = False
        options['mosquitto:with_binaries'] = False
        builder.add(settings=settings, options=options, env_vars=env_vars, build_requires=build_requires)
    builder.run()
