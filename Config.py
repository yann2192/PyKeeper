#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2011 Yann GUIBET <yannguibet@gmail.com>
#  See LICENSE for details.

import os

home = os.getenv('USERPROFILE') or os.getenv('HOME')
#home = '' # For test

folder = os.path.join(home,'.keeper')
if os.path.exists(folder) is False:
    os.mkdir(folder)
elif os.path.isdir(folder) is False:
    raise Exception("%s already exist" % folder)

shadow = os.path.join(folder, 'shadow.db')
