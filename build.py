#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os
import platform
import copy

def is_windows():
    return platform.system() == 'Windows'

def is_linux():
    return platform.system() == 'Linux'

def add_conan_community():
    conan_remote_env = "CONAN_REMOTES"
    conan_community_address = "https://api.bintray.com/conan/conan-community/conan"
    remote = os.getenv(conan_remote_env, "")
    if remote:
        remote += ","
    remote += conan_community_address
    os.environ[conan_remote_env] = remote

if __name__ == "__main__":
    add_conan_community()
    shared_option_name = False if is_windows() else None
    builder = build_template_default.get_builder(shared_option_name=shared_option_name)
    if is_linux():
        extended_builds = copy.deepcopy(builder)
        for settings, options, env_vars, build_requires, _ in extended_builds.items:
            options['mosquitto:with_mosquittopp'] = False
            builder.add(settings=settings, options=options, env_vars=env_vars, build_requires=build_requires)
    builder.run()
