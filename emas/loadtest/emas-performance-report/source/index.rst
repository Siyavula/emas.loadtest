.. EMAS Performance Tuning Report documentation master file, created by
   sphinx-quickstart on Wed Sep  4 10:29:43 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################################
Siyavula performance tuning report
##################################


Introduction
============
    
    In order to test the current configuration, hardware and software, against
    the published `performance goals`_, a series of benchmark tests were 
    undertaken.  The results of these tests were used to do optimisation changes.
    
    This document tries to summarise the data that was gathered, the conclusions
    that were reached and the remedial steps that were taken.
    
    Each section has a link to the specific `Funkload bench reports`_.  The
    Funkload bench tests were configure not to follow external links, since
    we are attempting to benchmark the EMAS software and hardware cluster
    not external CDNs or external network access.


1. Pre-test optimisation
========================
    
    We started the optimisation process by identifying those folders that have
    too many objects.  During this investigation we found that MemberServices 
    and Orders are potential problems.

    As a first-pass optimisation MemberServices were moved to a PostgreSQL
    implementation and completely removed from the ZODB.  
    
    Orders, on the other hand, were not moved out of the ZODB, since the volumes
    involved and the amount of times each Order is accessed are well within the
    ZODB's capacity to handle.  In order to stop bloating of the portal
    catalogue we did move orders to their own smaller catalogue though.


2. An overview of the setup we benchmarked
==========================================

    Four distinct servers were used in the benchmarking process.  Any further
    mention of 'test cluster' in this document refers to the following setup:

    Siyavula Performance 1 (aka. SP1)
        
        - Varnish caching proxy
        - HAProxy load balancing server

    Siyavula Performance 2 (aka. SP2)

        - 4 EMAS application server instances
        - 1 ZEO server with Zope Replication Service
        - 1 Redis analytics queue
        - 1 PostgreSQL cluster (initial primary database server)
        - 4 Monassis instances

    Siyavula Performance 3 (aka. SP3)

        - 4 EMAS application server instances
        - 1 ZEO server with Zope Replication Service
        - 1 Redis analytics queue
        - 1 PostgreSQL cluster (initial secondary database server)
        - 4 Monassis instances

    Siyavula Performance 4 (aka. sp4)

        - Load generation server
        - Host for the `Funkload`_ benchmark tests

    As load generating infrastructure we chose Funkload, since it is written in
    Python, tests are very easy to record, customise and run and the reporting
    functions are excellent.

    Network topology:

    The public side of the network is 100mbit/sec. The private subnet is
    1000mbit/sec.  Currently SP1, SP2 and SP3 are on the public network and the
    private subnet.  Subsequently all internal communication between these 3
    servers run at 1000mbit/sec.  SP4 is not on the private 1000mbit/ sec
    network.  It is only on the 100mbit/sec public network.


.. _Testing authenticated reads:

3. Testing authenticated reads
==============================
    
    Reading all the possible URLs in the site authenticated was deemed
    impractical due to the amount of time potentially required to do one
    test cycle.  In order to decide which URLs to use for the authenticated
    read tests we created a Funkload test that reads all the content
    unauthenticated (results available here: `Science unauthenticated read`_).
    This test was run with only 1 user and 1 cycle.

    Unauthenticated read setup:

    - Launched: 2013-07-26 15:54:29
    - Test: test_wholesite.py WholeSite.test_WholeSite
    - Target server: http://qap.everythingscience.co.za
    - Cycles of concurrent users: [1]
    - Cycle duration: 800s
    - `Apdex`_: 1.5

    From this list of URLs we chose to benchmark the following in the 
    authenticated read test:

    - /
    - /login
    - /login_form
    - grade-12/01-organic-molecules/01-organic-molecules-07.cnxmlplus
    - grade-10/19-quantitative-aspects-of-chemical-change/19-quantitative-aspects-of-chemical-change-01.cnxmlplus
    - grade-10/19-quantitative-aspects-of-chemical-change/19-quantitative-aspects-of-chemical-change-06.cnxmlplus
    - grade-11/04-intermolecular-forces/04-intermolecular-forces-02.cnxmlplus Get grade-11/04-intermolecular-forces/04-intermolecular-forces-02.cnxmlplus
    - grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus Get grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus
    - grade-10/22-mechanical-energy/22-mechanical-energy-01.cnxmlplus
    - grade-10/24-units-used-in-the-book/24-units-used-in-the-book-01.cnxmlplus
    - grade-12/02-organic-macromolecules/02-organic-macromolecules-01.cnxmlplus
    - grade-12/05-the-chemical-industry/05-the-chemical-industry-02.cnxmlplus
    - grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus
    - grade-12/10-colour/10-colour-06.cnxmlplus
    - grade-12/11-2d-and-3d-wavefronts/11-2d-and-3d-wavefronts-08.cnxmlplus
    - grade-12/12-wave-nature-of-matter/12-wave-nature-of-matter-01.cnxmlplus
    - grade-11/13-types-of-reactions/13-types-of-reactions-01.cnxmlplus
    - grade-11/14-lithosphere/14-lithosphere-01.cnxmlplus    
    
    The criterium we used to choose the above URLs is simply the performance
    in the unauthenticated reading tests.  The pages that are slow during
    unauthenticated reading will be even slower during authenticated reading.

    We also chose some URLs that seemed to serve quite fast.  This we did to get
    some balance to the overall stats for the reading experience.

    The resultant Funkload test was run with 4 test cycles ranging from 100
    to 1000 concurrent users.

    Authenticated read setup:

    - Launched: 2013-08-22 14:35:07
    - From: siyavulap04
    - Test: test_AuthenticatedRead.py AuthenticatedRead.test_AuthenticatedRead
    - Target server: http://qap.everythingscience.co.za
    - Cycles of concurrent users: [100, 250, 500, 750, 1000]
    - Apdex: 1.5
    
    The results of each test cycle contains:

    - 18 pages
    - 59 links
    - 99 images

    The benchmark test as a whole (all cycles and users) contains:

    - 381 tests
    - 9701 pages
    - 100343 requests


4. Authenticated read test results
==================================
    
    Funkload bench report here: `Authenticated read`_


100 concurrent users
--------------------

    - Total pages served:             2037 pages
    - Successfull pages per second:   11.317 pages/ second
    - Errors:                         0.00% errors             
    - Fastest page:                   0.198 seconds       
    - Slowest page:                   44.309 second  
    - 95th percentile:                27.128 seconds

250 concurrent users
--------------------

    - Total pages served:             1863 pages
    - Successfull pages per second:   10.350 pages/ second
    - Errors:                         0.00% errors             
    - Fastest page:                   0.475 seconds       
    - Slowest page:                   68.065 second  
    - 95th percentile:                44. 851 seconds

500 concurrent users
--------------------

    - Total pages served:             1929 pages
    - Successfull pages per second:   10.717 pages/ second
    - Errors:                         0.00% errors             
    - Fastest page:                   0.428 seconds       
    - Slowest page:                   64.953 second  
    - 95th percentile:                33.854 seconds

750 concurrent users
--------------------

    - Total pages served:             1984 pages
    - Successfull pages per second:   11.022 pages/ second
    - Errors:                         0.00% errors             
    - Fastest page:                   0.439 seconds       
    - Slowest page:                   43.599 second  
    - 95th percentile:                20.745 seconds

1000 concurrent users
--------------------

    - Total pages served:             1888 pages
    - Successfull pages per second:   10.489 pages/ second
    - Errors:                         0.00% errors             
    - Fastest page:                   0.374 seconds       
    - Slowest page:                   34.843 second  
    - 95th percentile:                18.969 seconds

Summary
-------


================  =================== ================== ================== ==================  ==================
Concurrent users  Successfull pages/s Total pages served Fastest pages      Slowest pages       95th percentile 
================  =================== ================== ================== ==================  ==================
            100            11.317               2037        0.198 s             44.309 s              27.128 s 
            250            10.350               1863        0.475 s             68.065 s              44.851 s
            500            10.717               1929        0.428 s             64.953 s              33.854 s
            750            11.022               1984        0.439 s             43.599 s              20.745 s
           1000            10.489               1888        0.374 s             34.843 s              18.969 s
================  =================== ================== ================== ==================  ==================

Observations
------------
    
    Accross all tested concurrencies the cluster serves more than 10 pages per
    second.  Given this number we can project that the cluster should be able to
    serve:

    10 pages/ second * 60 seconds * 60 minutes = **36000 pages / hour**

    The test results show an interesting decline in performance around 250 and
    500 concurrent users.  This trend is reversed for 750 and 1000 concurrent
    users, where the tests show marked better performance.  No errors were
    experienced by Funkload during the test cycles.  This means the cluster
    continued to work even at high concurrencies.

    At the top tested concurrency of 1000 users the cluster will serve most
    pages in about 18.969 seconds.  This gives the cluster an Apdex rating of
    'Good' (0.916) which means most users should be satisfied with their
    experience.

    The longest a user ever waited for a page across all tested concurrencies
    was 68.065 seconds which occured at 250 concurrent users.


Optimisations done
------------------
    
    During the testing process we realised that some content pages were not
    cached in Varnish.  This is due to elements like username and personal links
    which are unique to each authenticated user.  These elements cause Varnish
    to view pages as different although very little actually differ between them.

    We implemented an `Edge-side include`_ (ESI) for the personal toolbar which
    leads to Varnish caching most of the page and only fetching the ESI content.


5. Testing practice service
===========================

    In order to test the Intelligent Practise service fully, Carl Scheffler
    implemented an 'oracle' for answers generated from the Monassis data.
    This 'oracle' we then wrapped in an HTTP server when we found that opening
    the pickle of all the saved answers to be a huge performance hit in our
    `Funkload`_ tests.

    During the testing we also tested the practice proxy in the Plone
    application.  This was done in order to establish if any processing in this
    proxy is possibly more of a performance issue than processing in the
    external system.  Here are the `Practice proxy`_ results.  To test this we
    recorded a `Funkload`_ test that logs in to the site and then navigates to a
    simple view in Monassis.  This view does no processing beyond returning
    basic headers and the string literal 'OK'.

    For the full practise service test we recorded a `Funkload`_ test that logs in
    to the site, browses to the practise service and then does 10 questions.
    The answers to these questions are fetched from the 'oracle' HTTP server.  
    This test we then ran with user concurrencies of 100, 150 and 200.

    We used the following test configuration:

    - Launched: 2013-08-23 12:10:13
    - From: siyavulap04
    - Test: test_Practice.py Practice.test_practice
    - Target server: http://qap.everythingmaths.co.za
    - Cycles of concurrent users: [100, 150, 200]
    - Apdex: 1.5


6. Results for testing practice service
=======================================

    Funkload bench report here: `Practise service test`_

100 concurrent users
--------------------


150 concurrent users
--------------------


200 concurrent users
--------------------


Optimisations done
------------------
    
    When we analysed the data from the practice service test we realized that
    the Plone login process takes quite a bit of time.  Upon further
    investigation we found that the user object is updated on each login.
    This is unnecessary given that we do not require the last login time.  We
    changed that specific method and removed all unnecessary changes to the 
    user object.


7. Testing mobile authenticated reads
=====================================

    Funkload bench report here: `Mobile test`_

    We used exactly the same set of pages for the mobile authenticated read tests
    as those in :ref:`Testing authenticated reads` above.  The tests were run in
    2 batches.  The only things different between the 2 batches are the number
    of cycles and concurrencies in those cycles.

    First batch:

        Test setup:

        - Launched: 2013-09-16 18:35:06
        - Test: test_AuthenticatedMobileRead.py AuthenticatedMobileRead.test_AuthenticatedMobileRead
        - Target server: http://m.qap.everythingscience.co.za
        - Cycles of concurrent users: **[100, 250, 500]**
        - Cycle duration: 180s
        - Apdex: 1.5

        The results of each test cycle contains:

        - 18 pages
        - 6 links
        - 588 images

        The benchmark test as a whole (all cycles and users) contains:

        - 19 tests
        - 1485 pages
        - 76088 requests

    Second batch:

        Test setup:

        - Launched: 2013-09-16 19:38:36
        - Test: test_AuthenticatedMobileRead.py AuthenticatedMobileRead.test_AuthenticatedMobileRead
        - Target server: http://m.qap.everythingscience.co.za
        - Cycles of concurrent users: **[750, 1000]**
        - Cycle duration: 180s
        - Apdex: 1.5

        The results of each test cycle contains:

        - 18 page(s)
        - 6 link(s)
        - 588 image(s)

        The benchmark test as a whole (all cycles and users) contains:

        - 18 tests
        - 2156 pages
        - 116041 requests


8. Results for testing mobile authenticated reads
=================================================

100 concurrent users
--------------------


250 concurrent users
--------------------

500 concurrent users
--------------------


750 concurrent users
--------------------


1000 concurrent users
---------------------


9. Testing Varnish
==================
    
    As background to this test consider the following.  The application servers
    SP2 and SP3 are connected via a non-routable private subnet in the 10.0.0.*
    range. In the current cluster setup they are accessed over this private
    subnet via the HAProxy and Varnish servers on SP1.  This means any latency 
    or throughput issues on the subnet will adversly affect the total 
    scalability.

    Varnish serves all our cachable resources (CSS, javascript, images, etc.).  
    In order to understand the total scalability we decided to checked Varnish's 
    scalability in our current cluster setup.

    We used `Apache Benchmark`_ to test Varnish from our load generating server
    and the Varnish/ HAProxy server.  This was done with a script that starts
    off with 1 user and 10 requests all the way up to 1000 concurrent users and
    1000000 requests.


10. Results of Varnish
======================

1 user
------

    =================   ==============    ===============
    Complete requests   SP1 requests/s    SP4 requests/s
    =================   ==============    ===============
    100                 3799.39           242.94
    1000                4672.11           242.47  
    10000               4271.39           242.78
    100000              4457.42           243.10
    1000000             4828.27           242.91
    =================   ==============    ===============

10 concurrent users
-------------------

    =================   ==============    ===============
    Complete requests   SP1 requests/s    SP4 requests/s
    =================   ==============    ===============
    100                 11041.18          356.05 
    1000                20597.32          356.20
    10000               21980.24          358.07
    100000              18690.17          358.09
    1000000             20729.00          358.04
    =================   ==============    ===============

100 concurrent users
--------------------

    =================   ==============    ===============
    Complete requests   SP1 requests/s    SP4 requests/s
    =================   ==============    ===============
    100                 9004.95           242.86 
    1000                17513.13          357.70
    10000               18031.14          358.10
    100000              18753.04          358.13
    1000000             18552.96          358.13
    =================   ==============    ===============

1000 concurrent users
---------------------

    =================   ==============    ===============
    Complete requests   SP1 requests/s    SP4 requests/s
    =================   ==============    ===============
    100                 no data (1)       no data
    1000                10249.79          129.72
    10000               12786.09          no data
    100000              15860.49          no data
    1000000             16436.69          no data
    =================   ==============    ===============
    
    (1) An entry of 'no data' indicates that the test cycle could not complete
    successfully and therefore `Apache Benchmark`_ did not record the statistics.

    Both SP1 and SP4 show relatively linear changes in performance.  The important
    thing is the marked difference in the amount of requests per second between
    the 2 servers.  After more investigation we found that the back-end network
    between the servers in the cluster is not running at its full capacity.  This
    has been changed and a second set of tests will be run to validate the
    assumption that network throughput is responsible for the difference in 
    performance between the 2 mentioned servers.


Recommendation for scaling / Conclusion
==========================================


.. _Apdex: http://apdex.org/
.. _All test results: http://197.221.50.101/stats/
.. _Science unauthenticated read: http://197.221.50.101/stats/test_WholeSite-20130726T155429/
.. _unauthenticated read: http://197.221.50.101/stats/test_WholeSite-20130726T155429/
.. _Funkload: http://funkload.nuxeo.org
.. _Science authenticated read: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/
.. _Authenticated read: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/
.. _slowest authenticated results: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/#slowest-requests
.. _Practise service test: http://197.221.50.101/stats/test_practice-20130823T121013/
.. _Practice proxy: http://197.221.50.101/stats/test_practiceproxy-20130819T124350/
.. _Mobile test: http://197.221.50.101/stats/
.. _performance goals: https://docs.google.com/a/upfrontsystems.co.za/document/d/1GUjwcpHBpLILQozouukxVQBLB1-GQvdUa6UXfpv75-M/edit#
.. _Funkload bench reports: http://197.221.50.101/stats/
.. _Edge-side include: http://en.wikipedia.org/wiki/Edge_Side_Includes
.. _slow science pages: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/#page-013-get-grade-12-08-work-energy-and-power-08-work-energy-and-power-03-cnxmlplus
.. _Apache Benchmark: https://httpd.apache.org/docs/2.2/programs/ab.html
.. _Science authenticated mobile read: http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T193836/
.. _authenticated mobile read: http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T193836/
.. _slowest authenticated mobile read page: http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T183506/#id15
