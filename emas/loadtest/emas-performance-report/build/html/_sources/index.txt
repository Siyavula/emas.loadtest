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
    Funkload bench tests were configured not to follow external links, since
    we are attempting to benchmark the EMAS software and hardware cluster
    not external CDNs or external network access.
    
    When viewing the data in the following report one must bear in mind that the
    load generation machine (SP4) accesses the load balancing server (SP1) via
    a 100 Mbits/s network (cf. `Network topology`_).  This leads to a very
    real constraint on the maximum transfer rates.  Consider the following best 
    case scenario:

        A 100 Mbit/s network can transfer about 12800 kilobytes per second at
        the maximum.  This means a resource of 30 kilobytes can be transferred 
        ~426 times per second.  Using the `iperf`_ utility we measured a 
        throughput of 12352 kilobytes/s (~96.5 Mbits/s) on the 100 Mbits/s 
        network, which lowers the count for our 30 kilobyte resource to 
        ~411 requests/ s.
        
        For a page with 31 resources, like the EMAS home page, we can
        theoretically project a serve rate of:

            (411 requests/s) / 31 resources ~ 13 pages/s.

        If we start working at higher levels of concurrency, say 100 concurrent 
        users, this picture changes.  Now the network can only serve 
        (411 requests/ s)/100 = 4.11 requests per concurrent user per second.  
        In effect each user now waits more than 7.29 seconds per page.

        Given this we can say that the best this network can do for our
        described page, if all concurrent users are treated equitably, is:

            13 pages/s * 60 s * 60 min = 46800 pages per hour


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


2. An overview of the set-up we benchmarked
===========================================

    Four distinct servers were used in the benchmarking process.  Any further
    mention of 'test cluster' in this document refers to the following set-up:

Siyavula Performance 1 (aka. SP1)
---------------------------------
        
        - `Varnish`_ caching proxy
        - `HAProxy`_ load balancing server

Siyavula Performance 2 (aka. SP2)
---------------------------------

        - 4 `EMAS`_ application server instances
        - 1 `ZEO`_ server with `Zope Replication Service`_
        - 1 `Redis`_ analytics queue
        - 1 `PostgreSQL`_ cluster (initial primary database server)
        - 4 `Monassis`_ instances

Siyavula Performance 3 (aka. SP3)
---------------------------------

        - 4 EMAS application server instances
        - 1 ZEO server with Zope Replication Service
        - 1 Redis analytics queue
        - 1 PostgreSQL cluster (initial secondary database server)
        - 4 Monassis instances

Siyavula Performance 4 (aka. SP4)
---------------------------------

        - Load generation server
        - Host for the `Funkload`_ benchmark tests

    As load generating infrastructure we chose Funkload, since it is written in
    Python, tests are very easy to record, customise and run and the reporting
    functions are excellent.

.. _Network topology:

Network topology
----------------

    The public side of the network is 100 Mbits/sec. The private subnet is
    1000 Mbits/sec.  Currently SP1, SP2 and SP3 are on the public network and the
    private subnet.  Subsequently all internal communication between these 3
    servers run at 1000 Mbits/sec.  SP4 is not on the private 1000 Mbits/ sec
    network.  It is only on the 100 Mbits/sec public network.

    In order to validate the above set-up we ran a series of iperf tests
    between the servers.


Observations on network test results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    The `iperf data`_ shows throughput of more than 900 Mbits/s between
    SP1, SP2 and SP3.  When one keeps in mind that iperf does actual data
    transfer and that each of the packets sent and received have a protocol
    related overhead, the results for all tested servers are consistent with
    those of a 1000 Mbits/s network.

    The same test run between SP1 and SP4 shows a throughput of around 
    96,5 Mbits/sec which seems reasonable for a 100 Mbits/s network.


.. _Testing authenticated reads:

3. Testing authenticated reads
==============================
    
    Reading all the possible URLs in the site authenticated was deemed
    impractical due to the amount of time potentially required to do one
    test cycle.  In order to decide which URLs to use for the authenticated
    read tests we created a Funkload test that reads all the content
    unauthenticated (results available here: `Science unauthenticated read`_).
    This test was run with only 1 user and 1 cycle.

    Unauthenticated read set-up:

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
    
    The criterion we used to choose the above URLs is simply the performance
    in the unauthenticated reading tests.  The pages that are slow during
    unauthenticated reading will be even slower during authenticated reading.

    We also chose some URLs that seemed to serve quite fast.  This we did to get
    some balance to the overall statistics for the reading experience.

    The resultant Funkload test was run with 5 test cycles ranging from 100
    to 1000 concurrent users.

    Authenticated read set-up:

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
    
    Funkload bench report here: `Authenticated read`_ and
    `Authenticated read (with errors)`_
    

================  =================== ================== ================== ==================  ==================
Concurrent users  Successful pages/s  Total pages served Fastest pages      Slowest pages       95th percentile 
================  =================== ================== ================== ==================  ==================
            100            11.317               2037        0.198 s             44.309 s              27.128 s 
            250            10.350               1863        0.475 s             68.065 s              44.851 s
            500            10.717               1929        0.428 s             64.953 s              33.854 s
            750            11.022               1984        0.439 s             43.599 s              20.745 s
           1000            10.489               1888        0.374 s             34.843 s              18.969 s
================  =================== ================== ================== ==================  ==================

Observations
------------
    
    At the top tested concurrency of 1000 users the cluster will serve most
    pages in about 18.969 seconds (95th percentile).  This gives the cluster an
    Apdex rating of 'Good' (0.916) which means most users should be satisfied
    with their experience.

    The longest a user ever waited for a page across all tested concurrencies
    was 68.065 seconds which occurred at 250 concurrent users.  In subsequent
    cycles the slowest pages where all served faster than this.  
    
    The test results show a small decline in performance at 250 concurrent
    users.  From 500 concurrent users, this changes.  The tests show marked
    improvement in performance up to and including the maximum concurrency of
    1000 users.  When one considers the complete test and the fact that all the
    error-free cycles serve around 10 pages per second, this appears to be
    irrelevant for the current discussion.

    The error rate stays at 0% throughout all the testing cycles up to 1000.
    This means the cluster continued to serve even at high concurrencies.  At a
    concurrency of 1500 users we started to see errors which leads us to think
    that 1000 concurrent users is the current safe maximum for this cluster.

    Across all tested concurrencies, for simple authenticated reading, the
    cluster serves more than 10 pages per second.  Given this number we can
    project that the cluster should be able to serve around:

    10 pages/ second * 60 seconds * 60 minutes = **36000 pages / hour**


Optimisations done
------------------
    
    During the testing process we realised that some content pages were not
    cached in Varnish.  This is due to elements like user name and personal links
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

    We also tested the practice proxy in the Plone application.  This was done
    in order to establish if any processing in this proxy is more of a
    performance issue than processing in the external system.  Here are the
    `Practice proxy`_ results.  To test this we recorded a Funkload  bench test
    that logs in to the site and then navigates to a simple view in Monassis.  
    This view does no processing beyond returning basic headers and the string
    literal 'OK'.

    For the full practise service test we recorded a Funkload test that logs in
    to the site, browses to the practise service and then does 10 questions.
    The answers to these questions are fetched from the 'oracle' HTTP server.  
    This test we then ran with user concurrencies of 100, 150 and 200.  We
    stopped at 200 concurrent users, because tests started failing at 250
    concurrent users. 
    
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

================== =================== ================== ================== ================== ==================
Concurrent users   Successful pages/s  Total pages served Fastest pages      Slowest pages      95th percentile   
================== =================== ================== ================== ================== ==================
            100             32.133               7712             0.144             22.775              5.919
            150             34.852               8358             0.223             51.181              7.492 
            200             26.583               6380             1.862             89.483             14.193 
================== =================== ================== ================== ================== ==================

Observations
------------
    
    As the concurrency rises the cluster serves fewer pages second.  This is 
    clear from the amount of successful pages per second and the total pages 
    served.  Pages also take longer to serve.  Above 250 concurrent users we 
    start to notice errors.

    At a concurrency level of 200, most pages are served within 12 seconds (95th
    percentile).  This along with the fact that errors start to occur at 250
    concurrent users makes it clear that 200 users should be considered the safe
    maximum concurrency for the practice service on this cluster.

    The cluster can server 26 pages per second at 200 concurrent users.  This
    means it can potentially serve:

    26 pages * 60 seconds * 60 minutes = **93600 practice service pages per hour.**

    
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

    We used exactly the same set of pages for the mobile authenticated read tests
    as those in :ref:`Testing authenticated reads` above.  The tests were run in
    2 batches.  The only things different between the 2 batches are the number
    of cycles and concurrencies in those cycles.  This test makes no attempt at
    modelling the nature of a mobile connection and as such does not necessarily
    accurately mirror the mobile end-user experience.  It does give one a
    reasonable idea of how the cluster scales under load when using the mobile
    theme though.

    First batch:

        Funkload bench report here: `authenticated mobile read (batch 1)`_

        Test set-up:

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
 
        Test set-up:

        Funkload bench report here: `authenticated mobile read (batch 2)`_

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

================== =================== ================== ================== ================== ==================
Concurrent users   Successful pages/s  Total pages served Fastest pages      Slowest pages      95th percentile   
================== =================== ================== ================== ================== ==================
            100              5.222                940             0.322             56.810             51.439
            250              3.317                597             0.524             75.697             68.783
            500              3.439                619             0.516             50.441             41.022
            750              4.072                733             0.255             37.729             26.844
           1000              4.178                752             0.471             33.915             26.374
================== =================== ================== ================== ================== ==================

In order to verify that the mobile theme resources are cached we gathered
Varnish statistics via `Munin`_.  The are included here as 
`Varnish statistics for authenticated mobile reads`_

Observations
------------
    
    The successful pages per second for the mobile theme is a concern.  We 
    analysed some of the content pages and found that several have very high 
    numbers of resources, some over a 100.  
    (cf.  http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T183506/#id11 and
    http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T183506/#id12).  
    Each of these resource are requested individually.  This high level of
    resources per page is due to the way the page is structured and not the 
    current cluster set-up.  Including the way mathml is converted to images.
    It is a concern though, since high levels of
    requests for small resources creates a situation where the connection
    overhead to actually data throughput ratio becomes a problem.  The system
    spends progressively more time on connection, transport, etc. handling and
    this reduces the effective throughput of data.

    The cluster exhibits a gradual decline in successful pages served across the
    tested concurrencies.  We observed the same degrade in the performance for
    250 concurrent users as we did for the normal web theme.  In this case we
    also consider it irrelevant for the goal of determining performance and
    scalability under load where mobile authenticated reading is concerned.
    
    The fastest page is served in 0.322 seconds at 100 concurrent users.  The
    slowest page is served in 75.697 seconds at a concurrency of 250. After this
    point the minimum page load times increase steadily.  The fact that pages
    individually load faster under higher concurrencies is likely due to the 
    caching proxy.

    The `Varnish statistics for authenticated mobile reads`_ verify that at
    least 80% of all requests for resources in the mobile authenticated read
    test is being served by Varnish from its cache.

    The results indicate that this cluster can serve 4.178 pages per second at
    a concurrency of 1000 users and can manage around 4 pages per second across
    the tested concurrencies.  This means we can potentially serve:

    4 pages * 60 seconds * 60 minutes ~ **14400 pages per hour.**
    

9. Testing Varnish
==================
    
    As background to this test consider the following.  The application servers
    SP2 and SP3 are connected via a private subnet in the 10.0.0.* range. In
    the current cluster set-up they are accessed over this private subnet via
    the HAProxy and Varnish servers on SP1.  This means any latency or
    throughput issues on the subnet will adversely affect the total scalability.

    Varnish serves all our cachable resources (CSS, javascript, images, etc.).  
    In order to understand the total scalability we decided to checked Varnish's 
    scalability in our current cluster set-up.

    We used `Apache Benchmark`_ to test Varnish from our load generating server
    and the Varnish/ HAProxy server.  This was done with a script that starts
    off with 1 user and 10 requests all the way up to 1000 concurrent users and
    1000000 requests.


10. Results of Varnish
======================

1 user
------

    =================   ===============
    Complete requests   SP4 requests/s
    =================   ===============
    100                 242.94
    1000                242.47  
    10000               242.78
    100000              243.10
    1000000             242.91
    =================   ===============

10 concurrent users
-------------------

    =================   ===============
    Complete requests   SP4 requests/s
    =================   ===============
    100                 356.05 
    1000                356.20
    10000               358.07
    100000              358.09
    1000000             358.04
    =================   ===============

100 concurrent users
--------------------

    =================   ===============
    Complete requests   SP4 requests/s
    =================   ===============
    100                 242.86 
    1000                357.70
    10000               358.10
    100000              358.13
    1000000             358.13
    =================   ===============

1000 concurrent users
---------------------

    =================   ===============
    Complete requests   SP4 requests/s
    =================   ===============
    100                 no data
    1000                129.72
    10000               no data
    100000              no data
    1000000             no data
    =================   ===============
    
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
=======================================
    
    The Hetzner data centre provides a 100 Mbits/s link to our test cluster.   
    This observation is supported by the `Hetzner network information`_ and 
    our own iperf tests.

    Comparing the Funkload tests with the maximum stated network throughput 
    points to the fact that the network itself will be the  limiting factor in 
    most of our typical usage scenarios (cf. tested scenarios in this document).

    A second point of import is the Google analytics information for August and 
    September 2013.  It shows maximum usage of ~5000 hits per hour for 
    everthingmaths and ~5000 for everythingscience.  This leaves us with a 
    combined peak load of ~11000 page requests per hour.

    The network itself and the tested cluster can handle this load.  We suggest 
    that the production environment be monitored closely.  When the combined 
    peak load reaches ~80% of the tested maximum, Siyavula should invest in 
    another similar cluster.


Referenced images and data
==========================

.. _iperf data:

Network test from SP1 to SP2
----------------------------
    
    SP1 server::

        iperf -s -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        [  4] local 10.0.0.11 port 5001 connected with 10.0.0.12 port 45482
        ------------------------------------------------------------
        Client connecting to 10.0.0.12, TCP port 5001
        TCP window size: 0.11 MByte (default)
        ------------------------------------------------------------
        [  6] local 10.0.0.11 port 51005 connected with 10.0.0.12 port 5001
        [ ID] Interval       Transfer     Bandwidth
        [  6]  0.0-10.0 sec  1097 MBytes   920 Mbits/sec
        [  4]  0.0-10.0 sec  1112 MBytes   930 Mbits/sec
    
    SP2 client::

        iperf -c 10.0.0.11 -d -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        ------------------------------------------------------------
        Client connecting to 10.0.0.11, TCP port 5001
        TCP window size: 0.14 MByte (default)
        ------------------------------------------------------------
        [  5] local 10.0.0.12 port 45482 connected with 10.0.0.11 port 5001
        [  4] local 10.0.0.12 port 5001 connected with 10.0.0.11 port 51005
        [ ID] Interval       Transfer     Bandwidth
        [  5]  0.0-10.0 sec  1112 MBytes   932 Mbits/sec
        [  4]  0.0-10.0 sec  1097 MBytes   918 Mbits/sec
    
Network test from SP1 to SP3
----------------------------
    
    SP1 server::

        iperf -s -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        [  4] local 10.0.0.11 port 5001 connected with 10.0.0.13 port 49089
        ------------------------------------------------------------
        Client connecting to 10.0.0.13, TCP port 5001
        TCP window size: 0.11 MByte (default)
        ------------------------------------------------------------
        [  6] local 10.0.0.11 port 51450 connected with 10.0.0.13 port 5001
        [ ID] Interval       Transfer     Bandwidth
        [  4]  0.0-10.0 sec  1110 MBytes   929 Mbits/sec
        [  6]  0.0-10.0 sec  1098 MBytes   920 Mbits/se
        
    SP3 client::

        iperf -c 10.0.0.11 -d -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        ------------------------------------------------------------
        Client connecting to 10.0.0.11, TCP port 5001
        TCP window size: 0.14 MByte (default)
        ------------------------------------------------------------
        [  5] local 10.0.0.13 port 49089 connected with 10.0.0.11 port 5001
        [  4] local 10.0.0.13 port 5001 connected with 10.0.0.11 port 51450
        [ ID] Interval       Transfer     Bandwidth
        [  5]  0.0-10.0 sec  1110 MBytes   930 Mbits/sec
        [  4]  0.0-10.0 sec  1098 MBytes   919 Mbits/sec

Network test between SP2 and SP3
--------------------------------

    SP2 server::

        iperf -s -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        [  4] local 10.0.0.12 port 5001 connected with 10.0.0.13 port 58467
        ------------------------------------------------------------
        Client connecting to 10.0.0.13, TCP port 5001
        TCP window size: 0.11 MByte (default)
        ------------------------------------------------------------
        [  6] local 10.0.0.12 port 42910 connected with 10.0.0.13 port 5001
        [ ID] Interval       Transfer     Bandwidth
        [  6]  0.0-10.0 sec  1090 MBytes   914 Mbits/sec
        [  4]  0.0-10.0 sec  1111 MBytes   930 Mbits/sec

    SP3 bidirectional test::

        iperf -c 10.0.0.12 -d -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        ------------------------------------------------------------
        Client connecting to 10.0.0.12, TCP port 5001
        TCP window size: 0.15 MByte (default)
        ------------------------------------------------------------
        [  5] local 10.0.0.13 port 58467 connected with 10.0.0.12 port 5001
        [  4] local 10.0.0.13 port 5001 connected with 10.0.0.12 port 42910
        [ ID] Interval       Transfer     Bandwidth
        [  5]  0.0-10.0 sec  1111 MBytes   931 Mbits/sec
        [  4]  0.0-10.0 sec  1090 MBytes   913 Mbits/sec

Network test from SP1 to SP4
----------------------------
    
    SP1 server::

        iperf -s -f m
        ------------------------------------------------------------
        Server listening on TCP port 5001
        TCP window size: 0.08 MByte (default)
        ------------------------------------------------------------
        [  4] local 197.221.50.98 port 5001 connected with 197.221.50.101 port 35371
        [ ID] Interval       Transfer     Bandwidth
        [  4]  0.0-10.3 sec   116 MBytes  94.1 Mbits/sec

    SP4 bidirectional test::

        iperf -c 197.221.50.98 -f m
        ------------------------------------------------------------
        Client connecting to 197.221.50.98, TCP port 5001
        TCP window size: 0.02 MByte (default)
        ------------------------------------------------------------
        [  3] local 197.221.50.101 port 35371 connected with 197.221.50.98 port 5001
        [ ID] Interval       Transfer     Bandwidth
        [  3]  0.0-10.1 sec   116 MBytes  96.5 Mbits/sec

Varnish cache statistics
------------------------

    .. _Varnish statistics for authenticated mobile reads:

    .. image:: ./images/varnish_backend_traffic-day.png

    .. image:: ./images/varnish_hit_rate-day.png


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
.. _performance goals: https://docs.google.com/a/upfrontsystems.co.za/document/d/1GUjwcpHBpLILQozouukxVQBLB1-GQvdUa6UXfpv75-M/edit#
.. _Funkload bench reports: http://197.221.50.101/stats/
.. _Edge-side include: http://en.wikipedia.org/wiki/Edge_Side_Includes
.. _slow science pages: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/#page-013-get-grade-12-08-work-energy-and-power-08-work-energy-and-power-03-cnxmlplus
.. _Apache Benchmark: https://httpd.apache.org/docs/2.2/programs/ab.html
.. _Science authenticated mobile read: http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T193836/
.. _authenticated mobile read (batch 1): http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T183506/
.. _authenticated mobile read (batch 2): http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T193836/
.. _slowest authenticated mobile read page: http://197.221.50.101/stats/test_AuthenticatedMobileRead-20130916T183506/#id15
.. _Authenticated read (with errors): http://197.221.50.101/stats/test_AuthenticatedRead-20130730T203634
.. _iperf: http://iperf.sourceforge.net/
.. _Varnish: https://www.varnish-cache.org/
.. _Munin: http://munin-monitoring.org/
.. _EMAS: http://projects.siyavula.com/technology-driven-learning/
.. _ZEO: http://docs.zope.org/zope2/zope2book/ZEO.html
.. _PostgreSQL: http://www.postgresql.org
.. _Redis: http://redis.io/
.. _Monassis: http://projects.siyavula.com/about-intelligent-practice/
.. _ZRS: http://www.zope.com/products/x1752814276/Zope-Replication-Services
.. _Zope Replication Service: http://www.zope.com/products/x1752814276/Zope-Replication-Services
.. _HAProxy: http://haproxy.1wt.eu/
.. _Hetzner network information: http://www.hetzner.co.za/helpcentre/index.php/articles/content/category/our_network_and_servers/hetzners_network_115
