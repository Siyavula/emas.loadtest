Introduction
============

Load testing package for Everything Maths & Science

Preparation
===========

    ./bin/pip install funkload

Generate user names and passwords
=================================

    emas.loadtest.createusers

Generate the paths txt files
============================

    ./bin/instance run src/emas.loadtest/emas/loadtest/generate_paths.py

Recording tests
===============

    ./bin/fl-record [testname]

Running tests
=============
    
    cd to directory where test module is.

    [virtualenv]/bin/fl-run-test [test_module_name]

    e.g. ../../../../bin/fl-run-test test_wholesite.py

    OR

    to run against different server url to that in WholeSite.conf

    [virtualenv]/bin/fl-run-test [test_module_name] -u [server url] 

    e.g. ../../../../bin/fl-run-test test_wholesite.py -u http://localhost:8080

Compiling reports
=================
