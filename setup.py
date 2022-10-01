import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'greeter'
AUTHOR = 'Haley Hunter-Zinck'
URL = 'https://github.com/hhunterzinck/daily-brief'

LICENSE = 'MIT License'
DESCRIPTION = 'Send an automated, daily email'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'pandas',
      'numpy'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      entry_points ={
            'console_scripts': [
                'dailybrief = dailybrief.__main__:main'
            ]
      }
      )

