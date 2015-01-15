from setuptools import setup, find_packages

setup(
    # Application name
    name='BaseAlyzer',
    
    # Version number
    version='0.1',

    # Author details
    author='Warwick Brett Louw (Warosaurus)',
    author_email='WarwickBrettLouw@gmail.com',
    
    # Description
    description='Code for project big data',

    # Packages
    packages=find_packages(),

    # Details
    url='http://github.com/Warosaurus/Nuggets',
    
    # Dependancies
    install_requires=[
        "numpy",
    ],

    # Package data
    package_data={
        '': [".py"],
    }
)
