from setuptools import setup, Extension

algorecord = Extension(
    'algorecord',
    sources=['algorecord.cpp', 'recorder.cpp', 'hacks.cpp'],
    extra_compile_args=['-std=c++11', '-O3']
)

setup(
    name='Algorecord',
    version='0.1.0',
    description='This is the C++ extension that records the interpreter',
    ext_modules=[algorecord]
)
