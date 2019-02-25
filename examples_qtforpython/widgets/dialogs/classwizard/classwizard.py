#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2016 The Qt Company Ltd.
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
#############################################################################

from PySide2 import QtCore, QtGui, QtWidgets

import classwizard_rc


class ClassWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(ClassWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(ClassInfoPage())
        self.addPage(CodeStylePage())
        self.addPage(OutputFilesPage())
        self.addPage(ConclusionPage())

        self.setPixmap(QtWidgets.QWizard.BannerPixmap,
                QtGui.QPixmap(':/images/banner.png'))
        self.setPixmap(QtWidgets.QWizard.BackgroundPixmap,
                QtGui.QPixmap(':/images/background.png'))

        self.setWindowTitle("Class Wizard")

    def accept(self):
        className = self.field('className')
        baseClass = self.field('baseClass')
        macroName = self.field('macroName')
        baseInclude = self.field('baseInclude')

        outputDir = self.field('outputDir')
        header = self.field('header')
        implementation = self.field('implementation')

        block = ''

        if self.field('comment'):
            block += '/*\n'
            block += '    ' + header + '\n'
            block += '*/\n'
            block += '\n'

        if self.field('protect'):
            block += '#ifndef ' + macroName + '\n'
            block += '#define ' + macroName + '\n'
            block += '\n'

        if self.field('includeBase'):
            block += '#include ' + baseInclude + '\n'
            block += '\n'

        block += 'class ' + className
        if baseClass:
            block += ' : public ' + baseClass

        block += '\n'
        block += '{\n'

        if self.field('qobjectMacro'):
            block += '    Q_OBJECT\n'
            block += '\n'

        block += 'public:\n'

        if self.field('qobjectCtor'):
            block += '    ' + className + '(QObject *parent = 0);\n'
        elif self.field('qwidgetCtor'):
            block += '    ' + className + '(QWidget *parent = 0);\n'
        elif self.field('defaultCtor'):
            block += '    ' + className + '();\n'

            if self.field('copyCtor'):
                block += '    ' + className + '(const ' + className + ' &other);\n'
                block += '\n'
                block += '    ' + className + ' &operator=' + '(const ' + className + ' &other);\n'

        block += '};\n'

        if self.field('protect'):
            block += '\n'
            block += '#endif\n'

        headerFile = QtCore.QFile(outputDir + '/' + header)

        if not headerFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(None, "Class Wizard",
                    "Cannot write file %s:\n%s" % (headerFile.fileName(), headerFile.errorString()))
            return

        headerFile.write(str(block))

        block = ''

        if self.field('comment'):
            block += '/*\n'
            block += '    ' + implementation + '\n'
            block += '*/\n'
            block += '\n'

        block += '#include "' + header + '"\n'
        block += '\n'

        if self.field('qobjectCtor'):
            block += className + '::' + className + '(QObject *parent)\n'
            block += '    : ' + baseClass + '(parent)\n'
            block += '{\n'
            block += '}\n'
        elif self.field('qwidgetCtor'):
            block += className + '::' + className + '(QWidget *parent)\n'
            block += '    : ' + baseClass + '(parent)\n'
            block += '{\n'
            block += '}\n'
        elif self.field('defaultCtor'):
            block += className + '::' + className + '()\n'
            block += '{\n'
            block += '    // missing code\n'
            block += '}\n'

            if self.field('copyCtor'):
                block += '\n'
                block += className + '::' + className + '(const ' + className + ' &other)\n'
                block += '{\n'
                block += '    *this = other;\n'
                block += '}\n'
                block += '\n'
                block += className + ' &' + className + '::operator=(const ' + className + ' &other)\n'
                block += '{\n'

                if baseClass:
                    block += '    ' + baseClass + '::operator=(other);\n'

                block += '    // missing code\n'
                block += '    return *this;\n'
                block += '}\n'

        implementationFile = QtCore.QFile(outputDir + '/' + implementation)

        if not implementationFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(None, "Class Wizard",
                    "Cannot write file %s:\n%s" % (implementationFile.fileName(), implementationFile.errorString()))
            return

        implementationFile.write(str(block))

        super(ClassWizard, self).accept()


class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                QtGui.QPixmap(':/images/watermark1.png'))

        label = QtWidgets.QLabel("This wizard will generate a skeleton C++ class "
                "definition, including a few functions. You simply need to "
                "specify the class name and set a few options to produce a "
                "header file and an implementation file for your new C++ "
                "class.")
        label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ClassInfoPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ClassInfoPage, self).__init__(parent)

        self.setTitle("Class Information")
        self.setSubTitle("Specify basic information about the class for "
                "which you want to generate skeleton source code files.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo1.png'))

        classNameLabel = QtWidgets.QLabel("&Class name:")
        classNameLineEdit = QtWidgets.QLineEdit()
        classNameLabel.setBuddy(classNameLineEdit)

        baseClassLabel = QtWidgets.QLabel("B&ase class:")
        baseClassLineEdit = QtWidgets.QLineEdit()
        baseClassLabel.setBuddy(baseClassLineEdit)

        qobjectMacroCheckBox = QtWidgets.QCheckBox("Generate Q_OBJECT &macro")

        groupBox = QtWidgets.QGroupBox("C&onstructor")

        qobjectCtorRadioButton = QtWidgets.QRadioButton("&QObject-style constructor")
        qwidgetCtorRadioButton = QtWidgets.QRadioButton("Q&Widget-style constructor")
        defaultCtorRadioButton = QtWidgets.QRadioButton("&Default constructor")
        copyCtorCheckBox = QtWidgets.QCheckBox("&Generate copy constructor and operator=")

        defaultCtorRadioButton.setChecked(True)

        defaultCtorRadioButton.toggled.connect(copyCtorCheckBox.setEnabled)

        self.registerField('className*', classNameLineEdit)
        self.registerField('baseClass', baseClassLineEdit)
        self.registerField('qobjectMacro', qobjectMacroCheckBox)
        self.registerField('qobjectCtor', qobjectCtorRadioButton)
        self.registerField('qwidgetCtor', qwidgetCtorRadioButton)
        self.registerField('defaultCtor', defaultCtorRadioButton)
        self.registerField('copyCtor', copyCtorCheckBox)

        groupBoxLayout = QtWidgets.QVBoxLayout()
        groupBoxLayout.addWidget(qobjectCtorRadioButton)
        groupBoxLayout.addWidget(qwidgetCtorRadioButton)
        groupBoxLayout.addWidget(defaultCtorRadioButton)
        groupBoxLayout.addWidget(copyCtorCheckBox)
        groupBox.setLayout(groupBoxLayout)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(classNameLabel, 0, 0)
        layout.addWidget(classNameLineEdit, 0, 1)
        layout.addWidget(baseClassLabel, 1, 0)
        layout.addWidget(baseClassLineEdit, 1, 1)
        layout.addWidget(qobjectMacroCheckBox, 2, 0, 1, 2)
        layout.addWidget(groupBox, 3, 0, 1, 2)
        self.setLayout(layout)


class CodeStylePage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(CodeStylePage, self).__init__(parent)

        self.setTitle("Code Style Options")
        self.setSubTitle("Choose the formatting of the generated code.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo2.png'))

        commentCheckBox = QtWidgets.QCheckBox("&Start generated files with a "
                "comment")
        commentCheckBox.setChecked(True)

        protectCheckBox = QtWidgets.QCheckBox("&Protect header file against "
                "multiple inclusions")
        protectCheckBox.setChecked(True)

        macroNameLabel = QtWidgets.QLabel("&Macro name:")
        self.macroNameLineEdit = QtWidgets.QLineEdit()
        macroNameLabel.setBuddy(self.macroNameLineEdit)

        self.includeBaseCheckBox = QtWidgets.QCheckBox("&Include base class "
                "definition")
        self.baseIncludeLabel = QtWidgets.QLabel("Base class include:")
        self.baseIncludeLineEdit = QtWidgets.QLineEdit()
        self.baseIncludeLabel.setBuddy(self.baseIncludeLineEdit)

        protectCheckBox.toggled.connect(macroNameLabel.setEnabled)
        protectCheckBox.toggled.connect(self.macroNameLineEdit.setEnabled)
        self.includeBaseCheckBox.toggled.connect(self.baseIncludeLabel.setEnabled)
        self.includeBaseCheckBox.toggled.connect(self.baseIncludeLineEdit.setEnabled)

        self.registerField('comment', commentCheckBox)
        self.registerField('protect', protectCheckBox)
        self.registerField('macroName', self.macroNameLineEdit)
        self.registerField('includeBase', self.includeBaseCheckBox)
        self.registerField('baseInclude', self.baseIncludeLineEdit)

        layout = QtWidgets.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(commentCheckBox, 0, 0, 1, 3)
        layout.addWidget(protectCheckBox, 1, 0, 1, 3)
        layout.addWidget(macroNameLabel, 2, 1)
        layout.addWidget(self.macroNameLineEdit, 2, 2)
        layout.addWidget(self.includeBaseCheckBox, 3, 0, 1, 3)
        layout.addWidget(self.baseIncludeLabel, 4, 1)
        layout.addWidget(self.baseIncludeLineEdit, 4, 2)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field('className')
        self.macroNameLineEdit.setText(className.upper() + "_H")

        baseClass = self.field('baseClass')
        is_baseClass = bool(baseClass)

        self.includeBaseCheckBox.setChecked(is_baseClass)
        self.includeBaseCheckBox.setEnabled(is_baseClass)
        self.baseIncludeLabel.setEnabled(is_baseClass)
        self.baseIncludeLineEdit.setEnabled(is_baseClass)

        if not is_baseClass:
            self.baseIncludeLineEdit.clear()
        elif QtCore.QRegExp('Q[A-Z].*').exactMatch(baseClass):
            self.baseIncludeLineEdit.setText('<' + baseClass + '>')
        else:
            self.baseIncludeLineEdit.setText('"' + baseClass.lower() + '.h"')


class OutputFilesPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(OutputFilesPage, self).__init__(parent)

        self.setTitle("Output Files")
        self.setSubTitle("Specify where you want the wizard to put the "
                "generated skeleton code.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo3.png'))

        outputDirLabel = QtWidgets.QLabel("&Output directory:")
        self.outputDirLineEdit = QtWidgets.QLineEdit()
        outputDirLabel.setBuddy(self.outputDirLineEdit)

        headerLabel = QtWidgets.QLabel("&Header file name:")
        self.headerLineEdit = QtWidgets.QLineEdit()
        headerLabel.setBuddy(self.headerLineEdit)

        implementationLabel = QtWidgets.QLabel("&Implementation file name:")
        self.implementationLineEdit = QtWidgets.QLineEdit()
        implementationLabel.setBuddy(self.implementationLineEdit)

        self.registerField('outputDir*', self.outputDirLineEdit)
        self.registerField('header*', self.headerLineEdit)
        self.registerField('implementation*', self.implementationLineEdit)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(outputDirLabel, 0, 0)
        layout.addWidget(self.outputDirLineEdit, 0, 1)
        layout.addWidget(headerLabel, 1, 0)
        layout.addWidget(self.headerLineEdit, 1, 1)
        layout.addWidget(implementationLabel, 2, 0)
        layout.addWidget(self.implementationLineEdit, 2, 1)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field('className')
        self.headerLineEdit.setText(className.lower() + '.h')
        self.implementationLineEdit.setText(className.lower() + '.cpp')
        self.outputDirLineEdit.setText(QtCore.QDir.toNativeSeparators(QtCore.QDir.tempPath()))


class ConclusionPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("Conclusion")
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                QtGui.QPixmap(':/images/watermark2.png'))

        self.label = QtWidgets.QLabel()
        self.label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QtWidgets.QWizard.FinishButton)
        finishText.replace('&', '')
        self.label.setText("Click %s to generate the class skeleton." % finishText)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    wizard = ClassWizard()
    wizard.show()
    sys.exit(app.exec_())
