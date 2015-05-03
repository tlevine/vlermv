from distutils.core import setup

setup(name='vlermv',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://thomaslevine.com/!/vlermv/',
      packages=['vlermv', 'vlermv.serializers', 'vlermv.transformers'],
      install_requires = [],
      tests_require = ['pytest>=2.6.4'],
      version='1.1.0',
      license='AGPL',
)
