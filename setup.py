from setuptools import setup, find_packages, Command
from os import path, system, remove, rename, removedirs
import re

package_name = "pytblocklib"

root_dir = path.abspath(path.dirname(__file__))

def _requirements():
    return [name.rstrip() 
        for name in open(path.join(
            root_dir, 'requirements.txt')).readlines()]

with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    version = re.search(
        r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    license = re.search(
        r'__license__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author = re.search(
        r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(
        r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(
        r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

assert version
assert license
assert author
assert author_email
assert url


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    author=author,
    author_email=author_email,
    classifiers=[
        'Natural Language :: Japanese',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',        
        'Programming Language :: Python :: 3.8',        
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
    ],
    description="a python library for youtube blocking function.",
    install_requires=_requirements(),
    keywords='youtube livechat antispam',
    license=license,
    long_description=long_description,
    long_description_content_type='text/markdown',
    name=package_name,
    packages=find_packages(exclude=['*log.txt','*testrun']),
    url=url,
    version=version,
)