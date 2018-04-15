#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os


if __name__ == "__main__":

    builder = build_template_default.get_builder()
    if os.name == 'nt':
        builder.items = filter(lambda build: build.options["mosquitto:shared"] == True, builder.items)
    builder.run()
