from setuptools import setup, find_packages

# https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use
setup(
    name='qiidly',
    version='0.1.0',
    packages=find_packages(),
    # scripts = ['say_hello.py'],
    install_requires=[
      'qiita-v2',
    ],

    # metadata for upload to PyPI
    author='uraxy',
    author_email='uraxy123@gmail.com',
    description='Sync following tag feeds at Qiita to Feedly.',
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
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
