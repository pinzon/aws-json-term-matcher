
from setuptools import setup, find_packages

setup(
    name='aws_json_term_matcher',
    version='0.1.0',
    description='A parser for AWS log JSON term matching filters.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cristopher Pinzon',
    author_email='cristopher.pinzon@gmail.com',
    url='https://github.com/pinzon/aws-logs-parser',
    packages=find_packages(),
    install_requires=[
        'lark>=1.2.2',
        'pytest>=8.3.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
