#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

####################### Licensing #######################################################
#
#   Copyright 2018 @ Evandro Coan
#   Helper functions and classes
#
#  Redistributions of source code must retain the above
#  copyright notice, this list of conditions and the
#  following disclaimer.
#
#  Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials
#  provided with the distribution.
#
#  Neither the name Evandro Coan nor the names of any
#  contributors may be used to endorse or promote products
#  derived from this software without specific prior written
#  permission.
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or ( at
#  your option ) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################
#

import sys
import threading
import textwrap

if sys.version_info[0] < 3:
    Event = threading._Event

else:
    Event = threading.Event


class SleepEvent(Event):

    def __init__(self):
        super( SleepEvent, self ).__init__()

    def sleep(self, timeout=None):
        """
            If blockOnSleepCall() was called before, this will sleep the current thread for ever if
            not arguments are passed. Otherwise, it accepts a positive floating point number for
            seconds in which this thread will sleep.

            If disableSleepCall() is called before the timeout has passed, it will immediately get
            out of sleep and this thread will wake up.
        """
        self.wait( timeout )

    def blockOnSleepCall(self):
        self.clear()

    def disableSleepCall(self):
        self.set()


def wrap_text(text):
    return textwrap.dedent( text ).strip( " " ).strip( "\n" )


