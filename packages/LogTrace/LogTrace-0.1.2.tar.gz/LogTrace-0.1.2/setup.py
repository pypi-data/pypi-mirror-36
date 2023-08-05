#!python
from distutils.core import setup

description = 'Aggregate Python log messages into a single log entry.'

with open('README.txt') as file:
    long_description = file.read()

setup(name='LogTrace',
      description=description,
      url='https://github.com/paul-wolf/logtrace',
      author='Paul Wolf',
      author_email='paul.wolf@yewleaf.com',
      version='0.1.2',
      #version = module.__version__,
      packages=['logtrace', ],
      license='BSD',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          # 'Programming Language :: Python :: 2.6',
          # 'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
