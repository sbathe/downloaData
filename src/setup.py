import setuptools
major_version='0.1.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='amfi',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url='https://github.com/sbathe/downloadData',
    license='GPLv3',
    author='Saurabh Bathe',
    author_email='sbathe@gmail.com',
    packages=setuptools.find_packages(),
    description='put something good here',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
)
