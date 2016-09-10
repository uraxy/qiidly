from setuptools import setup, find_packages
from qiidly import __version__, __description__

# https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use
setup(
    name='qiidly',
    version=__version__,
    packages=find_packages(),
    # scripts = ['say_hello.py'],
    install_requires=[
      'qiita-v2',
    ],

    # metadata for upload to PyPI
    author='uraxy',
    author_email='uraxy123@gmail.com',
    description=__description__,
    license='MIT',
    keywords=['Qiita', 'Feedly', 'feed', 'rss', 'atom'],
    url='https://github.com/uraxy/qiidly',
    entry_points={
        'console_scripts': ['qiidly=qiidly.command_line:main'],
    },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ],
)
