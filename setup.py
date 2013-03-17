from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='adhocracy.nrw_gruene_theme',
      version=version,
      description="Adhocracy theme for beteiligung.gruene-nrw.de, diazo based, merges in wordpress.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Benjamin Jopen'
      author_email='ben@kre8tiv.de',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adhocracy'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
