from setuptools import setup

setup(
    name='VideoPub',
    version='0.2.0',
    py_modules=['videopub'],
    install_requires=[
        'click',
        'kafka-python',
        'pyhdfs'
    ],
    entry_points='''
        [console_scripts]
        videopub=videopub:main
    ''',
)
