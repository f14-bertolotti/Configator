from setuptools import setup, find_packages
setup(name='configator',
version='0.1',
description='CLI changeable json configuration',
url='https://github.com/f14-bertolotti/Configator',
author='f14',
author_email='f14.bertolotti@email.com',
license='GNU',
packages=find_packages(),
install_requires=['dynamic-json','dynamic-yaml'],
zip_safe=False)
