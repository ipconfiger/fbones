# coding=utf8


from setuptools import setup

setup(name='fbones',
      version='0.0.1',
      description='A bootstrap toolkit to kickoff a flask project',
      url='https://github.com/ipconfiger/fbones',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=['fbones'],
      install_requires=[
          'flask',
          'click',
          'alembic'
      ],
      entry_points={
        'console_scripts': ['fbones=fbones.fbones:main'],
      },
      zip_safe=False)
