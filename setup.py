import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'geoalchemy',
    'gevent-socketio',
	 'pyodbc',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'sqlalchemy',
    'transaction',
    'zope.sqlalchemy',
    ]

setup(name='ecoReleve-Sensor',
      version='0.0',
      description='ecoReleve-Sensor',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Natural Solutions (Thomas Peel)',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ecorelevesensor',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = ecorelevesensor:main
      [console_scripts]
      """,
      )
