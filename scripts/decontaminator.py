#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Launch the Decontaminator GUI"""

import multiprocessing

from itaxotools.decontaminator_gui import run


if __name__ == '__main__':
    multiprocessing.freeze_support()
    run()
