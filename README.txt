Introduction
============

Load testing package for Everything Maths & Science

Preparation
===========

    ./bin/pip install funkload

Generate user names and passwords
=================================

    ./bin/instance run src/emas.loadtest/emas/loadtest.createusers.py emas

Generate the paths txt files
============================

    ./bin/instance run src/emas.loadtest/emas/loadtest/create_paths_files.py \
    emas maths

    ./bin/instance run src/emas.loadtest/emas/loadtest/create_paths_files.py \
    emas science

Recording tests
===============

    ./bin/fl-record [testname]

Set up the monitoring server
============================
    
    Do a basic funkload install in a virtualenv on the monitoring server.

        cf. http://funkload.nuxeo.org/monitoring.html
    
    If you are not running the load generation and the monitoring servers on 
    the same IP, you will have to set up the monitoring server like this:

    Get the config files

        git clone https://github.com/Siyavula/emas.loadtest.git emas.loadtest

        Change emas/loadtest/monitor.conf

            host = 0.0.0.0 (or whatever IP/FQDN you prefer)

    Caveat

        Looks like there are some bugs in funkload/MonitorPlugins.py.
        You might have to add an 'import sys' and change the bit that checks
        for kernel versions, around line 81, to allow kernels newer than 2.6.

    Change the benchmark test's configuration file too. The [monitor] section
    has to be updated to point to the IP address or fully qualified domain
    name of the monitoring server. Have a look at emas/loadtest/WholeSite.conf.

    Start the monitoring server before you start the bench marking.

        [virtualenv]/bin/fl-monitor-ctl emas.loadtest/emas/loadtest/monitor.conf startd
    
    You should now have a monitoring server running and attached to the
    current terminal.

    The monitoring log should be in the same folder you started from, look for
    'monitor.log'.

Set up the credentials server
=============================

Running tests
=============
    
    Start the monitoring server
    ---------------------------

    cd to directory where test module is.

    [virtualenv]/bin/fl-run-test [test_module_name]

    e.g. ../../../../bin/fl-run-test test_wholesite.py

    OR

    to run against different server url to that in WholeSite.conf

    [virtualenv]/bin/fl-run-test [test_module_name] -u [server url] 

    e.g. ../../../../bin/fl-run-test test_wholesite.py -u http://localhost:8080

Compiling reports
=================


Open issues
===========

    sleep_time_min
    sleep_time_max
    cycles
    duration


