from setuptools import setup

setup(name='kharon',
      version='0.1.5.13',
      description='Simplifying hardware/iot development with a Django style batteries-included framework',
      url='https://github.com/RedRussianBear/kharon',
      author='Mikhail Khrenov, Sahil Kochar, Shriyash Upadhyay',
      author_email='mkhrenov34@gmail.com',
      license='BSD',
      packages=['kharon'],
      package_data={'kharon': ['*', 'project_templates/*']},
      entry_points={
          'console_scripts': ['kharon=kharon.command_line:kharon'],
      },
      zip_safe=False, install_requires=['pyserial'])
