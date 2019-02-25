/****************************************************************************
**
** Copyright (C) 2018 The Qt Company Ltd.
** Contact: http://www.qt.io/licensing/
**
** This file is part of the Qt for Python examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
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


import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1

ApplicationWindow {
    id: page
    width: 800
    height: 400
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red

    GridLayout {
        id: grid
        columns: 2
        rows: 3

        ColumnLayout {
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 400

            Text {
                id: leftlabel
                Layout.alignment: Qt.AlignHCenter
                color: "white"
                font.pointSize: 16
                text: "Qt for Python"
                Layout.preferredHeight: 100
                Material.accent: Material.Green
            }

            RadioButton {
                id: italic
                Layout.alignment: Qt.AlignLeft
                text: "Italic"
                onToggled: {
                    leftlabel.font.italic = con.getItalic(italic.text)
                    leftlabel.font.bold = con.getBold(italic.text)
                    leftlabel.font.underline = con.getUnderline(italic.text)

                }
            }
            RadioButton {
                id: bold
                Layout.alignment: Qt.AlignLeft
                text: "Bold"
                onToggled: {
                    leftlabel.font.italic = con.getItalic(bold.text)
                    leftlabel.font.bold = con.getBold(bold.text)
                    leftlabel.font.underline = con.getUnderline(bold.text)
                }
            }
            RadioButton {
                id: underline
                Layout.alignment: Qt.AlignLeft
                text: "Underline"
                onToggled: {
                    leftlabel.font.italic = con.getItalic(underline.text)
                    leftlabel.font.bold = con.getBold(underline.text)
                    leftlabel.font.underline = con.getUnderline(underline.text)
                }
            }
            RadioButton {
                id: noneradio
                Layout.alignment: Qt.AlignLeft
                text: "None"
                checked: true
                onToggled: {
                    leftlabel.font.italic = con.getItalic(noneradio.text)
                    leftlabel.font.bold = con.getBold(noneradio.text)
                    leftlabel.font.underline = con.getUnderline(noneradio.text)
                }
            }
        }

        ColumnLayout {
            id: rightcolumn
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 400
            Layout.preferredHeight: 400
            Layout.fillWidth: true

            RowLayout {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter


                Button {
                    id: red
                    text: "Red"
                    highlighted: true
                    Material.accent: Material.Red
                    onClicked: {
                        leftlabel.color = con.getColor(red.text)
                    }
                }
                Button {
                    id: green
                    text: "Green"
                    highlighted: true
                    Material.accent: Material.Green
                    onClicked: {
                        leftlabel.color = con.getColor(green.text)
                    }
                }
                Button {
                    id: blue
                    text: "Blue"
                    highlighted: true
                    Material.accent: Material.Blue
                    onClicked: {
                        leftlabel.color = con.getColor(blue.text)
                    }
                }
                Button {
                    id: nonebutton
                    text: "None"
                    highlighted: true
                    Material.accent: Material.BlueGrey
                    onClicked: {
                        leftlabel.color = con.getColor(nonebutton.text)
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Text {
                    id: rightlabel
                    color: "white"
                    Layout.alignment: Qt.AlignLeft
                    text: "Font size"
                    Material.accent: Material.White
                }
                Slider {
                    width: rightcolumn.width*0.6
                    Layout.alignment: Qt.AlignRight
                    id: slider
                    value: 0.5
                    onValueChanged: {
                        leftlabel.font.pointSize = con.getSize(value)
                    }
                }
            }
        }
    }
}
