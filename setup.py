from distutils.core import setup

setup(name='vlermv',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://thomaslevine.com/!/vlermv/',
      packages=['vlermv', 'vlermv.serializers', 'vlermv.transformers'],
      install_requires = [],
      tests_require = [
          'pytest>=2.6.4', 'testfixtures>=4.1.2',
          'thready>=1.4.0',
      ],
      version='1.3.4',
      license='LGPL',
      entry_points = {'console_scripts': ['dadaname = vlermv.transformers.magic:cli']},
)
