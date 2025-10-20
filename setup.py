# -*- coding: utf-8 -*-

import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="inventree-category-ipn-generator",
    version="1.0.0",
    author="InvenTree Community",
    author_email="plugins@inventree.org",
    description="InvenTree plugin for auto-generating IPNs based on category codes",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="inventree plugin ipn part-number category automation sequential",
    url="https://github.com/inventree/inventree-category-ipn",
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[
        # InvenTree is expected to be installed
    ],
    setup_requires=[
        "wheel",
    ],
    include_package_data=True,
    entry_points={
        "inventree_plugins": [
            "CategoryIPNGeneratorPlugin = cat_code_ipn_generator:CategoryIPNGeneratorPlugin"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Topic :: Office/Business",
    ],
)
