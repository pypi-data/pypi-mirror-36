from setuptools import find_packages, setup

__version__ = '2018.8'

setup(
    name='q2-SCNIC',
    version=__version__,
    license='BSD-3-Clause',
    packages=find_packages(),
    author="Michael Shaffer",
    author_email="michael.shaffer@ucdenver.edu",
    description=(
        "QIIME2 plugin for using SCNIC."),
    url="https://github.com/shafferm/q2-SCNIC",
    package_data={
        'q2_SCNIC': ['citations.bib']
    },
    entry_points={
        'qiime2.plugins':
        ['q2-SCNIC=q2_SCNIC.plugin_setup:plugin']
    }
)
