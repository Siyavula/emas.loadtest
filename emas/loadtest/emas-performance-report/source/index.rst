.. EMAS Performance Tuning Report documentation master file, created by
   sphinx-quickstart on Wed Sep  4 10:29:43 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
Siyavula performance tuning report
==================================


Introduction
============
    
    In order to test the current configuration, hardware and software, against
    the published `performance goals`_, a series of bencmark tests were 
    undertaken.  The results of these tests were used to do optimisation changes
    that were deemed necessary. 
    
    This document tries to summarise the data that was gathered, the conclusions
    that were reached and the remedial steps that were taken.
    
    Each section has a link to the specific `Funkload bench reports`_.


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

    Four distinct servers were used in the benchmarking process  Any further
    mention of 'test cluster' in this document refers to the following setup:

    Siyavula Performance 1
        
        - Varnish caching proxy
        - HAProxy load balancing server

    Siyavula Performance 2

        - 4 EMAS application server instances
        - 1 ZEO server with Zope Replication Service
        - 1 Redis analytics queue
        - 1 PostgreSQL cluster (initial primary database server)
        - 4 Monassis instances

    Siyavula Performance 3

        - 4 EMAS application server instances
        - 1 ZEO server with Zope Replication Service
        - 1 Redis analytics queue
        - 1 PostgreSQL cluster (initial secondary database server)
        - 4 Monassis instances

    Siyavula Performance 4

        - Load generation server
        - Host for the `Funkload`_ benchmark tests

    As load generating infrastructure we chose `Funkload`_, since it is written in
    Python, tests are very easy to record, customise and run and the reporting
    functions are excellent.


3. Testing authenticated reads
==============================
    
    Reading all the possible URLs in the site authenticated was deemed
    impractical due to the amount of time potentially required to do one
    `Funkload`_ cycle.  In order to decide which URLs to use for the authenticated
    read tests we created a `Funkload`_ test that reads all the content
    unauthenticated (results available here: `Science unauthed read`_).  This
    test was run with only 1 user and 1 cycle.

    Unauthed read setup:

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
    Since we are trying to establish a worst-case read scenario this seemed
    a pragmatic approach.

    We also chose some URLs that seemed to serve quite fast.  This we did to get
    some balance to the overall stats for the reading experience.

    The resultant `Funkload`_ test was run with 4 test cycles ranging from 100
    to 1000 concurrent users.

    Authenticated read setup:

    - Launched: 2013-08-22 14:35:07
    - From: siyavulap04
    - Test: test_AuthenticatedRead.py AuthenticatedRead.test_AuthenticatedRead
    - Target server: http://qap.everythingscience.co.za
    - Cycles of concurrent users: [100, 250, 500, 750, 1000]
    - `Apdex`_: 1.5
    
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
    
Pages served
------------

    The initial test results looked good, even though the total test cycle took
    very long to complete.  This was expected since we test at high concurrency
    levels.  The test cluster kept on serving all pages up to a maximum of **1000
    concurrent users.**  At that point it can serve **18.969 pages per second
    95% of the time.**  This means at a peak load of **1000** concurrent users
    the above test cluster can serve:

    18.969 * 60 * 60 = **67305.60 pages per hour**

    This is significantly lower than our required serve rate of **~36 000 000**
    pages per hour.

    At lower concurrencies we see the following:
    
    =====================  ================  ========================
    Concurrent users       Pages per second  Total pages per hour
    =====================  ================  ========================
             100                27.128           **68288.40** 
             250                44.851           **161463.60** 
             500                33.854           **121874.40** 
             750                20.745           **74682.00** 
    =====================  ================  ========================
    
    It is clear that even at the best serve rate of **44 pages per second** the
    test cluster will still **not reach the goal of ~36M pages per hour.**

Response time per page
----------------------

    ================    ===================     =========================
    Concurrent users    Requests per second     Response time per request
    ================    ===================     =========================
          100               111.106                 1.150
          250               105.456                 1.762
          500               113.183                 2.913
          750               113.700	                4.251
          1000              114.017                 5.317	
    ================    ===================     =========================

    The average response time per page is encouraging.  Even at the top
    concurrency of 1000 the worst response time is 12.326 seconds.  Most of the
    responses (95%) complete in less than 6 seconds though.  The current
    test cluster is degrading slowly and does not come to a complete halt even
    at the highest tested concurrency level.

Optimisations done
------------------
    
    During the testing process we realised that some elements in the pages are
    causing sub-optimal caching in Varnish.  This is due to elements like
    username and personal links which are unique to each authenticated user.
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
    basic headers and 'OK'.

    For the full practise service test we recorded a `Funkload`_ test that logs in
    to the site, browses to the practise service and then does 10 questions.
    The answers to these questions are fetched from the 'oracle' HTTP server.

    We used the following test configuration:

    - Launched: 2013-08-23 12:10:13
    - From: siyavulap04
    - Test: test_Practice.py Practice.test_practice
    - Target server: http://qap.everythingmaths.co.za
    - Cycles of concurrent users: [100, 150, 200]
    - `Apdex`_: 1.5


6. Results for testing practice service
=======================================

    Funkload bench report here: `Practise service test`_

Optimisations done
------------------
    
    When we analysed the data from the practice service read test we realized
    that the Plone login process takes quite a bit of time.  Upon further
    investigation we found that the user object was being update on each login.
    This is unnecessary given that we do not require the last login time.  We
    changed that specific method and removed all unnecessary changes to the 
    user object.


7. Testing mobile reads
=======================

    Funkload bench report here: `Mobile test`_


8. Results for testing mobile reads
===================================

1. level 1
----------

2. Level 2
----------

9. Recommendation for scaling / Conclusion
==========================================


.. _Apdex: http://apdex.org/
.. _All test results: http://197.221.50.101/stats/
.. _Science unauthed read: http://197.221.50.101/stats/test_WholeSite-20130726T155429/
.. _Funkload: http://funkload.nuxeo.org
.. _Authenticated read: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/
.. _slowest authed results: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/#slowest-requests
.. _Practise service test: http://197.221.50.101/stats/test_practice-20130823T121013/
.. _Practice proxy: http://197.221.50.101/stats/test_practiceproxy-20130819T124350/
.. _Mobile test: http://197.221.50.101/stats/
.. _performance goals: https://docs.google.com/a/upfrontsystems.co.za/document/d/1GUjwcpHBpLILQozouukxVQBLB1-GQvdUa6UXfpv75-M/edit#
.. _Funkload bench reports: http://197.221.50.101/stats/
.. _Edge-side include: http://en.wikipedia.org/wiki/Edge_Side_Includes
