import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='area_weighted_join',
                 version='0.1',
                 description='Spatially join misaligned polygons',
                 url='http://github.com/azavea/area-weighted-join',
                 author='Simon Kassel',
                 author_email='skassel@azavea.com',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ])
