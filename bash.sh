#!/bin/bash

mkdir -p tmp
PYTHONPATH=. python django_hello_world/manage.py print_models >/dev/null 2> tmp/$(date +%F).dat
