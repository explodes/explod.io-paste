from distutils.core import setup


setup(
    name='explod.io',
    version='1.0',
    packages=['explodio'],
    url='http://explod.io/',
    license='MIT',
    author='Evan Leis',
    author_email='evan.explodes@gmail.com',
    description='explod.io',
    requires=[
        'django==1.5.1',
        'pygments==1.6',
    ]
)
