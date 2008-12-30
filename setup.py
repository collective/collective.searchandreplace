from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.searchandreplace',
      version=version,
      description="Batch Search and Replace",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='batch regex search replace',
      author='enPraxis',
      author_email='info@enpraxis.net',
      url='https://svn.plone.org/svn/collective/collective.searchandreplace',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
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
