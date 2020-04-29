from setuptools import setup

setup(
        name = 'PyIntruder',
        version = '0.1.0',
        author = '@sirpsycho',
        description = 'Revised by @CasperGN - https://github.com/CasperGN/PyIntruder',
        url = 'https://github.com/sirpsycho/PyIntruder',
        include_package_data=True,
        install_requires=[
            'requests',
            'pyopenssl'
            ],        
        classifiers = [
            'Programming Language :: Python :: 3',
        ],
        python_requires = '>=3.4',
)