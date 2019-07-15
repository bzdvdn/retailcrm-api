from setuptools import setup, find_packages

setup(
    name='retailcrm-api',
    version='0.0.1',
    packages=find_packages(),
    install_requires = [
        'requests>=2.18.2'
    ],
    description='RetailCRM api v5 wrapper',
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/retailcrm-api',
    license='MIT',
    python_requires=">=3.6",
)