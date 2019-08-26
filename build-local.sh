#!/bin/bash
mkdir -p src/egg-info
cp -r amfi bin LICENSE MANIFEST.in README.md RELEASE-VERSION setup.py version.py src/
python src/setup.py build --build-base src/build egg_info --egg-base src/egg-info install
rm -rf src
