from distutils.core import setup

setup(name='vlermv',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://github.com/tlevine/vlermv',
      packages=['vlermv'],
      install_requires = [],
      tests_require = ['nose'],
      version='0.2.3',
      license='AGPL',
)
