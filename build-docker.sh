#!/bin/bash
mkdir -p src
cp -r amfi bin LICENSE MANIFEST.in README.md RELEASE-VERSION setup.py version.py src/
docker -D build -t datadownload . 
rm -rf src
