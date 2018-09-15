#!/bin/sh

cd ../test_site
PYTHONPATH=../b-log/pelican python3.6 -m pelican.server
