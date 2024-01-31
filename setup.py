from setuptools import setup, find_packages

setup(
    name='CC_Asn1',  # Replace with your package's name
    version='0.1',  # Your package's version
    description='A short description of your package',  # A brief description
    author='Your Name',  # Your name
    author_email='your.email@example.com',  # Your email
    url='https://github.com/yourusername/yourpackagename',  # URL to your package's repository
    packages=find_packages(exlude=["test", "tests"]),  # Automatically find your package
    install_requires=[
        'numpy',  # List your dependencies here
        'pandas',
        # etc.
    ],
    classifiers=[
        'Programming Language :: Python :: 3',  # Specify which Python versions you support
        'License :: OSI Approved :: MIT License',  # Your license
        'Operating System :: OS Independent',
        # etc.
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
)