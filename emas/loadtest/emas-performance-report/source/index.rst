.. EMAS Performance Tuning Report documentation master file, created by
   sphinx-quickstart on Wed Sep  4 10:29:43 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
Siyavula performance tuning report
==================================


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

    Four distinct servers were used in the benchmarking process. They are:

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
        - Host for the Funkload benchmark tests

    As load generating infrastructure we chose `Funkload`_, since it is written in
    Python, tests are very easy to record, customise and run and the reporting
    functions are excellent.


3. Testing authenticated reads
==============================
    
    Reading all the possible URLs in the site authenticated was deemed
    impractical due to the amount of time potentially required to do one
    Funkload cycle.  In order to decide which URLs to use for the authenticated
    read tests we created a Funkload test that reads all the content
    unauthenticated (results available here: `Science unauthed read`_).

    Unauthed read setup:

    - Launched: 2013-07-26 15:54:29
    - Test: test_wholesite.py WholeSite.test_WholeSite
    - Target server: http://qap.everythingscience.co.za
    - Cycles of concurrent users: [1]
    - Cycle duration: 800s
    - Apdex: 1.5

    From this list of URLs we chose the following to benchmark in our
    authenticated read:

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
    
    The criterium we used to chose the above URLs is simply the performance
    in the unauthenticated reading tests.  The pages that are slow during
    unauthenticated reading will be even slower during authenticated reading.
    Since we are trying to establish a worst-case read scenario this seemed
    a pragmatic approach.

    We also chose some URLs that seemed to be served quite fast.  This we did
    to get some balance to the overall stats for the reading experience.

    Authenticated read setup:

    - Launched: 2013-08-22 14:35:07
    - From: siyavulap04
    - Test: test_AuthenticatedRead.py AuthenticatedRead.test_AuthenticatedRead
    - Target server: http://qap.everythingscience.co.za
    - Cycles of concurrent users: [100, 250, 500, 750, 1000]
    - Apdex: 1.5


4. Authenticated read test results
==================================

    Raw results here: `Authenticated read`_

    Login is slow

    ESI for portal personal toolbar

    Point where service delivery degrades badly

    What we did about it


5. Testing practice service
===========================

    In order to test the Intelligent Practise service fully, Carl Scheffler
    implemented an 'oracle' for answers generated from the Monassis data.
    This 'oracle' we then wrapped in an HTTP server when we found that opening
    the pickle of all the saved answers to be a huge performance hit in our
    Funkload tests.

    During the testing we also tested the practice proxy in the Plone
    application.  This was done in order to establish if any processing in this
    proxy is possibly more of a performance issue than processing in the
    external system.  Here are the `Practice proxy`_ results.  To test this we
    recorded a Funkload test that logs in to the site and then navigates to a
    simple view in Monassis.  This view does no processing beyond returning
    basic headers and 'OK'.

    For the full practise service test we recorded a Funkload test that logs in
    to the site, browses to the practise service and then does 10 questions.
    The answers to these questions are fetched from the 'oracle' HTTP server.

    We used the following test configuration:

    - Launched: 2013-08-23 12:10:13
    - From: siyavulap04
    - Test: test_Practice.py Practice.test_practice
    - Target server: http://qap.everythingmaths.co.za
    - Cycles of concurrent users: [100, 150, 200]
    - Apdex: 1.5


6. Results for testing practice service
=======================================

    Raw results here: `Practise service test`_


7. Testing mobile reads
=======================

    Raw results here: `Mobile test`_

8. Results for testing mobile reads
===================================

9. Recommendation for scaling / Conclusion
==========================================


.. _All test results: http://197.221.50.101/stats/
.. _Science unauthed read: http://197.221.50.101/stats/test_WholeSite-20130726T155429/
.. _Funkload: http://funkload.nuxeo.org
.. _Authenticated read: http://197.221.50.101/stats/test_AuthenticatedRead-20130822T143507/
.. _Practise service test: http://197.221.50.101/stats/test_practice-20130823T121013/
.. _Practice proxy: http://197.221.50.101/stats/test_practiceproxy-20130819T124350/
.. _Mobile test: http://197.221.50.101/stats/
