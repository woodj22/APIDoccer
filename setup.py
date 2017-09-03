from setuptools import setup

setup(name='apidoccer',
      version='0.1',
      description='Used for documenting PHP.',
      url='http://github.com/woodj22/apidoccer.',
      author='woodj22',
      author_email='joe.wood@bbc.co.uk',
      package_data={'apidoccer': ['*.txt', 'data/*.txt']},
      include_package_data=True,
      license='MIT',
      packages=['funniest'],
      zip_safe=False)