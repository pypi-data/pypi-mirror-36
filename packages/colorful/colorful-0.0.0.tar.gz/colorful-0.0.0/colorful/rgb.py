# -*- coding: utf-8 -*-

"""
    colorful
    ~~~~~~~~

    Terminal string styling done right, in Python.

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

# This module provides the X11 rgb.txt as python dictionary.
# See https://en.wikipedia.org/wiki/X11_color_names for more information


def parse_rgb_txt_file(path):
    """
    Parse the given rgb.txt file into a Python dict.

    :param str path: the path to the X11 rgb.txt file
    """
    #: Holds the generated color dict
    color_dict = {}

    def __make_valid_color_name(name):
        """
        Convert the given name into a valid colorname
        """
        if len(name) == 1:
            name = name[0]
            return name[:1].lower() + name[1:]

        return name[0].lower() + ''.join(word.capitalize() for word in name[1:])


    with open(path, 'r') as rgb_txt:
        for line in rgb_txt:
            if line.startswith('!'):
                continue  # skip comments

            line = line.strip()
            parts = line.split()
            color_dict[__make_valid_color_name(parts[3:])] = (parts[0], parts[1], parts[2])

    return color_dict
