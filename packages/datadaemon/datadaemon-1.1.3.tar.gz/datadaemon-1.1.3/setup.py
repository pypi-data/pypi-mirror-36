from setuptools import setup

setup(
    name='datadaemon',
    version='V1.1.3',
    packages=['datadaemon', 'datadaemon.base',  'datadaemon.utilities'],
    url='',
    license='MIT',
    author='Ghost',
    author_email='',
    description='An cryptocurrency kline data collecting tool.',
    keywords=["cryptocurrency", "data collecting"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Console'
    ],
    install_requires=[
        "ccxt == 1.11.89",
        "alertover >= 1.0.0",
        "pandas >= 0.10.0",
        "sqlalchemy >= 1.1.0"
    ],
    entry_points="""
    [console_scripts]
    datadaemon = datadaemon.datadaemon:main
    """
)
