#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2018 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
############################################################################

from __future__ import print_function

"""An example showcasing how to use bindings for a custom non-Qt C++ library"""

from Universe import Icecream, Truck

class VanillaChocolateIcecream(Icecream):
    def __init__(self, flavor=""):
        super(VanillaChocolateIcecream, self).__init__(flavor)

    def clone(self):
        return VanillaChocolateIcecream(self.getFlavor())

    def getFlavor(self):
        return "vanilla sprinked with chocolate"

class VanillaChocolateCherryIcecream(VanillaChocolateIcecream):
    def __init__(self, flavor=""):
        super(VanillaChocolateIcecream, self).__init__(flavor)

    def clone(self):
        return VanillaChocolateCherryIcecream(self.getFlavor())

    def getFlavor(self):
        base_flavor = super(VanillaChocolateCherryIcecream, self).getFlavor()
        return base_flavor + " and a cherry"

if __name__ == '__main__':
    leave_on_destruction = True
    truck = Truck(leave_on_destruction)

    flavors = ["vanilla", "chocolate", "strawberry"]
    for f in flavors:
        icecream = Icecream(f)
        truck.addIcecreamFlavor(icecream)

    truck.addIcecreamFlavor(VanillaChocolateIcecream())
    truck.addIcecreamFlavor(VanillaChocolateCherryIcecream())

    truck.arrive()
    truck.printAvailableFlavors()
    result = truck.deliver()

    if result:
        print("All the kids got some icecream!")
    else:
        print("Aww, someone didn't get the flavor they wanted...")

    if not result:
        special_truck = Truck(truck)
        del truck

        print("")
        special_truck.setArrivalMessage("A new SPECIAL icecream truck has arrived!\n")
        special_truck.arrive()
        special_truck.addIcecreamFlavor(Icecream("SPECIAL *magical* icecream"))
        special_truck.printAvailableFlavors()
        special_truck.deliver()
        print("Now everyone got the flavor they wanted!")
        special_truck.leave()
