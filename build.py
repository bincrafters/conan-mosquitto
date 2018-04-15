#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import os


if __name__ == "__main__":

    shared_option_name = False if os.name == 'nt' else None
    builder = build_template_default.get_builder(shared_option_name=shared_option_name)
    builder.run()
