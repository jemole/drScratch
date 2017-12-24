"""Package setup script suitable for the cheeseshop."""
import os
import re
from setuptools import setup


PACKAGE_NAME = 'hairball'

HERE = os.path.abspath(os.path.dirname(__file__))
INIT = open(os.path.join(HERE, PACKAGE_NAME, '__init__.py')).read()
README = open(os.path.join(HERE, 'README.md')).read()
VERSION = re.search("__version__ = '([^']+)'", INIT).group(1)


setup(name=PACKAGE_NAME,
      author='Bryce Boe',
      author_email='bbzbryce@gmail.com',
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.2',
                   'Topic :: Utilities'],
      description=('Hairball is a plugin-able framework useful for static '
                   'analysis of Scratch projects.'),
      entry_points={'console_scripts': ['hairball = hairball:main']},
      install_requires=['kurt>=2.0.2'],
      keywords='scratch static-analysis',
      license='Simplified BSD License',
      long_description=README,
      packages=[PACKAGE_NAME, '{0}.plugins'.format(PACKAGE_NAME)],
      test_suite=PACKAGE_NAME,
      url='https://github.com/ucsb-cs-education/hairball',
      version=VERSION)
