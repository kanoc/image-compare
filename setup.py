from os import path

from setuptools import setup, find_packages


HERE = path.abspath(path.dirname(__file__))


with open(path.join(HERE, 'requirements.in')) as f:
    install_requires = f.read().splitlines()

setup(
    name='image-compare',
    version='0.0.1',
    description='Compare images',
    author='Csaba',
    author_email='kanocspam@gmail.com',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    python_requires='>=3.7, <4',
    classifiers=[
        'Development Status :: 4 - Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ]
)
