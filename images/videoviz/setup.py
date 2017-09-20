from setuptools import setup

setup(
    name='VideoViz',
    version='0.2.0',
    py_modules=['videoviz'],
    include_package_data=True,
    install_requires=[
        'snakebite',
        'flask',
        'click',
        'cassandra-driver',
    ],
    entry_points='''
        [console_scripts]
        videoviz=videoviz:main
    ''',
)
