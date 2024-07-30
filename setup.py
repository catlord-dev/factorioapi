from setuptools import setup, find_packages

setup(
    name='factorioapi',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your library's dependencies here
    ],
    # entry_points={
    #     'console_scripts': [
    #         'your-command=your_library.module:function',
    #     ],
    # },
    author='Cat Lord',
    author_email='catlord03012012151804@gmail.com',
    description='A Python library to interact with the Factorio API and related files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/catlord-dev/factorioapi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: GNU AGPL v3',
        'Operating System :: OS Independent',
    ],
)
