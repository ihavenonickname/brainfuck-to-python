from setuptools import setup

def tests():
    import unittest
    loader = unittest.TestLoader()
    return loader.discover('brainfuck_to_python/tests')

setup(
    name='brainfuck_to_python',
    version='1.0.0',
    description='Translate brainfuck code to Python code',
    author='Gabriel Blank Stift Mousquer',
    author_email='gabrielblanksm@gmail.com',
    url='https://github.com/ihavenonickname/brainfuck-to-python',
    py_modules=['brainfuck_to_python'],
    license='GPL 3.0',
    test_suite='setup.tests',
    keywords='brainfuck esolang compiler transpiler',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
