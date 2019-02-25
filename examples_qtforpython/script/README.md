# About QtScript

The QtScript module is deprecated since Qt 5.5,
and hence is not being distributed through our wheels.

However, it is possible to access the module
when using a local build of PySide2 which was built
against a Qt installation containing the Qt Script module
(ALL_OPTIONAL_MODULES in `sources/pyside2/CMakeLists.txt`).
