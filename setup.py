from distutils.core import setup
import os


HERE = os.path.dirname(__file__)


def read_requirements(filename):
    filename = os.path.join(HERE, filename)
    return [line.strip() for line in open(filename) if line.strip()]


setup(
    name='jsd',
    packages=['jsd', 'jsd.tests'],
    version='0.1',
    description='Declarative JSONSchema generation.',
    author='David Stanek',
    author_email='dstanek@dstanek.com',
    url='https://github.com/dstanek/jsd',
    download_url='https://github.com/dstanek/jsd/tarball/0.1',
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt')
)
