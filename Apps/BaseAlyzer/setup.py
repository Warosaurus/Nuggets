from setuptools import setup

setup(
    #Application name
    name='funniest',
    
    #Version number
    version='0.1',

    #Author details
    author='Warwick Brett Louw (Warosaurus)',
    author_email='WarwickBrettLouw@gmail.com',
    
    #Packages
    packages=['BaseAlyzer'],
    
    #Description *later*
    description='',
    
    #Details
    url='http://github.com/Warosaurus/Nuggets',
    
    #Dependancies
    install_requires=[
        "numpy",
        "scipy",
        "ftplib",
    ]
    
    zip_safe=False
)
