import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='clabe',
    version='0.0.2',
    author='Cuenca',
    author_email='dev@cuenca.io',
    description='Validate and generate the control digit of a CLABE in Mexico',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/clabe',
    packages=setuptools.find_packages(),
    extras_require={
        'dev': [
            'pytest>=3',
            'pycodestyle'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
