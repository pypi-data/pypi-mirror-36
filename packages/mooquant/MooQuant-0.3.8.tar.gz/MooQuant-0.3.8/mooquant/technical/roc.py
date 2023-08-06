# -*- coding: utf-8 -*-
# MooQuant
#
# Copyright 2017 bopo.wang<ibopo@126.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: bopo.wang <ibopo@126.com>
"""

from mooquant import technical


class ROCEventWindow(technical.EventWindow):
    def __init__(self, windowSize):
        super().__init__(windowSize)

    def getValue(self):
        ret = None

        if self.windowFull():
            prev = self.getValues()[0]
            actual = self.getValues()[-1]

            if actual is not None and prev is not None:
                diff = float(actual - prev)

                if diff == 0:
                    ret = float(0)
                elif prev != 0:
                    ret = diff / prev

        return ret


class RateOfChange(technical.EventBasedFilter):
    """Rate of change filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:rate_of_change_roc_and_momentum.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`mooquant.dataseries.DataSeries`.
    :param valuesAgo: The number of values back that a given value will compare to. Must be > 0.
    :type valuesAgo: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, valuesAgo, maxLen=None):
        assert (valuesAgo > 0)
        super().__init__(dataSeries, ROCEventWindow(valuesAgo + 1), maxLen)
