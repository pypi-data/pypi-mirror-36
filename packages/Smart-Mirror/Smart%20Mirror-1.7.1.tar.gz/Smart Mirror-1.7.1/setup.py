from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()


setup(
    name='Smart Mirror',
    version='1.7.1',
    entry_points = {
        "console_scripts": ['smart_mirror = smart_mirror.__main__:main']
        },
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['smart_mirror'],
    include_package_data=True,
    zip_safe=False,
    install_requires=required,

    # metadata to display on PyPI
    author="Kushal Katta",
    author_email="kushal@katta.xyz",
    description="Smart Mirror Project",
    keywords="smart mirror intelligent system home automation",
    url="http://katta.xyz/SmartMirror/",
    project_urls={
        # "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        # "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://github.com/KushalKatta/SmartMirror",
    }

    # could also include long_description, download_url, classifiers, etc.
)
