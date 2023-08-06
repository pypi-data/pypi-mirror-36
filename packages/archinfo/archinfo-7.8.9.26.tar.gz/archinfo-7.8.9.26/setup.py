try:
    from setuptools import setup
    from setuptools import find_packages
    packages = find_packages()
except ImportError:
    from distutils.core import setup
    import os
    packages = [x.strip('./').replace('/','.') for x in os.popen('find -name "__init__.py" | xargs -n1 dirname').read().strip().split('\n')]

setup(
    name='archinfo',
    version='7.8.9.26',
    python_requires='<3.0',
    packages=packages,
    install_requires=['future==0.16.0'],
)
