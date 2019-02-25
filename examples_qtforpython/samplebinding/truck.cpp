/****************************************************************************
**
** Copyright (C) 2018 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt for Python examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include <iostream>
#include <random>

#include "truck.h"

Truck::Truck(bool leaveOnDestruction) : m_leaveOnDestruction(leaveOnDestruction) {}

Truck::Truck(const Truck &other)
{
    for (size_t i = 0; i < other.m_flavors.size(); ++i) {
        addIcecreamFlavor(other.m_flavors[i]->clone());
    }
}

Truck &Truck::operator=(const Truck &other)
{
    if (this != &other) {
        clearFlavors();
        for (size_t i = 0; i < other.m_flavors.size(); ++i) {
            addIcecreamFlavor(other.m_flavors[i]->clone());
        }
    }
    return *this;
}

Truck::~Truck()
{
    if (m_leaveOnDestruction)
        leave();
    clearFlavors();
}

void Truck::addIcecreamFlavor(Icecream *icecream)
{
    m_flavors.push_back(icecream);
}

void Truck::printAvailableFlavors() const
{
    std::cout << "It sells the following flavors: \n";
    for (size_t i = 0; i < m_flavors.size(); ++ i) {
        std::cout << "  * "  << m_flavors[i]->getFlavor() << '\n';
    }
    std::cout << '\n';
}

void Truck::arrive() const
{
    std::cout << m_arrivalMessage;
}

void Truck::leave() const
{
    std::cout << "The truck left the neighborhood.\n";
}

void Truck::setLeaveOnDestruction(bool value)
{
    m_leaveOnDestruction = value;
}

void Truck::setArrivalMessage(const std::string &message)
{
    m_arrivalMessage = message;
}

bool Truck::deliver() const
{
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> dist(1, 2);

    std::cout << "The truck started delivering icecream to all the kids in the neighborhood.\n";
    bool result = false;

    if (dist(mt) == 2)
        result = true;

    return result;
}

void Truck::clearFlavors()
{
    for (size_t i = 0; i < m_flavors.size(); ++i) {
        delete m_flavors[i];
    }
    m_flavors.clear();
}
