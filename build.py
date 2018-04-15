#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os


if __name__ == "__main__":
    builder = build_template_default.get_builder()

    # Mosquitto doesn't support MTd for x86
    if os.name == 'nt':
        # Mosquitto only support shared lib on Windows
        builder = build_template_default.get_builder(shared_option_name=False)
        filtered_builds = []
        for settings, options, env_vars, build_requires, reference in builder.items:
            if settings["compiler.runtime"] == "MTd" and settings["arch"] == "x86":
                continue
            filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds

    builder.run()
