from setuptools import setup

setup(
    name='VideoPub',
    version='0.1.0',
    py_modules=['videopub'],
    install_requires=[
        'click',
        'kafka-python',
    ],
    entry_points='''
        [console_scripts]
        videopub=videopub:main
    ''',
)
