# The MIT License (MIT)
#
# Copyright (c) <2022-Present> <Alex Huszagh>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
    slider
    ======

    Example showing how to add ticks to a QSlider. Note that this does
    not work with stylesheets, so it's merely an example of how to
    get customized styling behavior with a QSlider.
'''

import os
import sys

EXAMPLE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(EXAMPLE))

import shared  # noqa  # pylint: disable=wrong-import-position,import-error

parser = shared.create_parser()
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)


class Slider(QtWidgets.QSlider):
    '''QSlider with a custom paint event.'''

    def __init__(self, *args, **kwds):  # pylint: disable=useless-parent-delegation,redefined-outer-name
        super().__init__(*args, **kwds)

    def paintEvent(self, event):  # pylint: disable=unused-argument,(too-many-locals
        '''Override the paint event to ensure the ticks are painted.'''

        painter = QtWidgets.QStylePainter(self)
        options = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(options)

        style = self.style()
        handle = style.subControlRect(
            compat.CC_Slider,
            options,
            compat.SC_SliderHandle,
            self,
        )

        interval = self.tickInterval() or self.pageStep()
        position = self.tickPosition()
        if position != compat.NoTicks and interval != 0:
            minimum = self.minimum()
            maximum = self.maximum()
            painter.setPen(colors.TickColor)
            for i in range(minimum, maximum + interval, interval):
                percent = (i - minimum) / (maximum - minimum + 1) + 0.005
                width = (self.width() - handle.width()) + handle.width() / 2
                x = int(percent * width)
                h = 4
                if position in (compat.TicksBothSides, compat.TicksAbove):
                    y = self.rect().top()
                    painter.drawLine(x, y, x, y + h)
                if position in (compat.TicksBothSides, compat.TicksBelow):
                    y = self.rect().bottom()
                    painter.drawLine(x, y, x, y - h)

        options.subControls = compat.SC_SliderGroove
        painter.drawComplexControl(compat.CC_Slider, options)

        options.subControls = compat.SC_SliderHandle
        painter.drawComplexControl(compat.CC_Slider, options)
