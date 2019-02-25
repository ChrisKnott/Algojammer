TEMPLATE = app
CONFIG += no_keywords # avoid clash with slots in Python.h
CONFIG += console force_debug_info
QT += widgets

include(pyside2.pri)

WRAPPED_HEADER = wrappedclasses.h
WRAPPER_DIR = $$OUT_PWD/AppLib
TYPESYSTEM_FILE = scriptableapplication.xml

QT_INCLUDEPATHS = -I"$$[QT_INSTALL_HEADERS]" -I"$$[QT_INSTALL_HEADERS]/QtCore" \
    -I"$$[QT_INSTALL_HEADERS]/QtGui" -I"$$[QT_INSTALL_HEADERS]/QtWidgets"

# On macOS, check if Qt is a framework build. This affects how include paths should be handled.
qtConfig(framework): QT_INCLUDEPATHS += --framework-include-paths=$$[QT_INSTALL_LIBS]

SHIBOKEN_OPTIONS = --generator-set=shiboken --enable-parent-ctor-heuristic \
    --enable-pyside-extensions --enable-return-value-heuristic --use-isnull-as-nb_nonzero \
    $$QT_INCLUDEPATHS -I$$PWD -T$$PWD -T$$PYSIDE2/typesystems --output-directory=$$OUT_PWD

# MSVC does not honor #define protected public...
win32:SHIBOKEN_OPTIONS += --avoid-protected-hack

# Prepare the shiboken tool
QT_TOOL.shiboken.binary = $$system_path($$PYSIDE2/shiboken2)
qtPrepareTool(SHIBOKEN, shiboken)

# Shiboken run that adds the module wrapper to GENERATED_SOURCES
shiboken.output = $$WRAPPER_DIR/applib_module_wrapper.cpp
shiboken.commands = $$SHIBOKEN $$SHIBOKEN_OPTIONS $$PWD/wrappedclasses.h ${QMAKE_FILE_IN}
shiboken.input = TYPESYSTEM_FILE
shiboken.dependency_type = TYPE_C
shiboken.variable_out = GENERATED_SOURCES

# A dummy command that pretends to produce the class wrappers from the headers
# depending on the module wrapper
WRAPPED_CLASSES = mainwindow.h
module_wrapper_dummy_command.output = $$WRAPPER_DIR/${QMAKE_FILE_BASE}_wrapper.cpp
module_wrapper_dummy_command.commands = echo ${QMAKE_FILE_IN}
module_wrapper_dummy_command.depends = $$WRAPPER_DIR/applib_module_wrapper.cpp
module_wrapper_dummy_command.input = WRAPPED_CLASSES
module_wrapper_dummy_command.dependency_type = TYPE_C
module_wrapper_dummy_command.variable_out = GENERATED_SOURCES

# Get the path component to the active config build folder
defineReplace(getOutDir) {
  out_dir = $$OUT_PWD
  CONFIG(release, debug|release): out_dir = $$out_dir/release
  else:out_dir = $$out_dir/debug
  return($$out_dir)
}

# Create hardlinks to the PySide2 shared libraries, so the example can be executed without manually
# setting the PATH.
win32 {
    out_dir = $$getOutDir()
    # no_link tell not to link to the output files, target_predeps forces the command to actually
    # execute, explicit_dependencies is a magic value that tells qmake not to run the commands
    # if the output files already exist.
    hard_link_libraries.CONFIG = no_link target_predeps explicit_dependencies
    hard_link_libraries.output = $$out_dir/${QMAKE_FILE_BASE}${QMAKE_FILE_EXT}
    hard_link_libraries.commands = mklink /H $$shell_path($$out_dir/${QMAKE_FILE_BASE}${QMAKE_FILE_EXT}) $$shell_path(${QMAKE_FILE_IN})
    hard_link_libraries.input = PYSIDE2_SHARED_LIBRARIES
}

QMAKE_EXTRA_COMPILERS += shiboken module_wrapper_dummy_command
win32:QMAKE_EXTRA_COMPILERS += hard_link_libraries

INCLUDEPATH += $$WRAPPER_DIR

for(i, PYSIDE2_INCLUDE) {
    INCLUDEPATH += $$i/QtWidgets $$i/QtGui $$i/QtCore
}

SOURCES += \
    main.cpp \
    mainwindow.cpp \
    pythonutils.cpp

HEADERS += \
    mainwindow.h \
    pythonutils.h

OTHER_FILES += $$TYPESYSTEM_FILE $$WRAPPED_HEADER pyside2_config.py README.md
