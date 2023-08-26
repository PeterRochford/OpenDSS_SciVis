'''
A script to create a pip release of the OpenDSS_SciVis package.

Description of the package can be found in the wiki:
https://github.com/PeterRochford/OpenDSS_SciVis/wiki

Created on Aug 11, 2023

@author: Kevin Wu
'''
from setuptools import setup, find_packages

setup(
    name='OpenDSS_SciVis',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'SkillMetrics'
    ],
    author='Peter Rochford',
    author_email='peter.rochford@xatorcorp.com',
    description='A Python package for analysis and visualization of data produced by the OpenDSS software application.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PeterRochford/OpenDSS_SciVis/tree/main',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
