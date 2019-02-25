/****************************************************************************
**
** Copyright (C) 2017 The Qt Company Ltd.
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

#include "mainwindow.h"
#include "pythonutils.h"

#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>

#include <QtGui/QFontDatabase>
#include <QtGui/QIcon>

#include <QtCore/QDebug>
#include <QtCore/QTextStream>

static const char defaultScript[] =
    "print(\"Hello, world\")\n"
    "mainWindow.testFunction1()\n";

MainWindow::MainWindow()
    : m_scriptEdit(new QPlainTextEdit(QLatin1String(defaultScript), this))
{
    setWindowTitle(tr("Scriptable Application"));

    QMenu *fileMenu = menuBar()->addMenu(tr("&File"));
    const QIcon runIcon = QIcon::fromTheme(QStringLiteral("system-run"));
    QAction *runAction = fileMenu->addAction(runIcon, tr("&Run..."), this, &MainWindow::slotRunScript);
    runAction->setShortcut(Qt::CTRL + Qt::Key_R);
    QAction *diagnosticAction = fileMenu->addAction(tr("&Print Diagnostics"), this, &MainWindow::slotPrintDiagnostics);
    diagnosticAction->setShortcut(Qt::CTRL + Qt::Key_D);
    fileMenu->addAction(tr("&Invoke testFunction1()"), this, &MainWindow::testFunction1);
    const QIcon quitIcon = QIcon::fromTheme(QStringLiteral("application-exit"));
    QAction *quitAction = fileMenu->addAction(quitIcon, tr("&Quit"), qApp, &QCoreApplication::quit);
    quitAction->setShortcut(Qt::CTRL + Qt::Key_Q);

    QMenu *editMenu = menuBar()->addMenu(tr("&Edit"));
    const QIcon clearIcon = QIcon::fromTheme(QStringLiteral("edit-clear"));
    QAction *clearAction = editMenu->addAction(clearIcon, tr("&Clear"), m_scriptEdit, &QPlainTextEdit::clear);

    QMenu *helpMenu = menuBar()->addMenu(tr("&Help"));
    const QIcon aboutIcon = QIcon::fromTheme(QStringLiteral("help-about"));
    QAction *aboutAction = helpMenu->addAction(aboutIcon, tr("&About Qt"), qApp, &QApplication::aboutQt);

    QToolBar *toolBar = new QToolBar;
    addToolBar(toolBar);
    toolBar->addAction(quitAction);
    toolBar->addSeparator();
    toolBar->addAction(clearAction);
    toolBar->addSeparator();
    toolBar->addAction(runAction);
    toolBar->addSeparator();
    toolBar->addAction(aboutAction);

    m_scriptEdit->setFont(QFontDatabase::systemFont(QFontDatabase::FixedFont));
    setCentralWidget(m_scriptEdit);

    if (!PythonUtils::bindAppObject("__main__", "mainWindow", PythonUtils::MainWindowType, this))
       statusBar()->showMessage(tr("Error loading the application module"));
}

void MainWindow::slotRunScript()
{
    const QStringList script = m_scriptEdit->toPlainText().trimmed().split(QLatin1Char('\n'), QString::SkipEmptyParts);
    if (!script.isEmpty())
        runScript(script);
}

void MainWindow::slotPrintDiagnostics()
{
    const QStringList script = QStringList()
            << "import sys" << "print('Path=', sys.path)" << "print('Executable=', sys.executable)";
    runScript(script);
}

void MainWindow::runScript(const QStringList &script)
{
    if (!::PythonUtils::runScript(script))
        statusBar()->showMessage(tr("Error running script"));
}

void MainWindow::testFunction1()
{
    static int n = 1;
    QString message;
    QTextStream(&message) << __FUNCTION__ << " called #" << n++;
    qDebug().noquote() << message;
    statusBar()->showMessage(message);
}
