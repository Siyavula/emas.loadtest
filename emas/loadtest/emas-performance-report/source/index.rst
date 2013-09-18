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
    
    Each section has a link to the specific `Funkload bench reports`_.  When
    statistics from the `Funkload bench reports`_ are used in this document
    we chose to use the 'P95' values.  They represent what happened 95% of the
    time in the test.

    The `Funkload bench reports`_ were configure not to follow external links,
    since we are attempting to benchmark the EMAS software and hardware cluster
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

    As load generating infrastructure we chose `Funkload`_, since it is written in
    Python, tests are very easy to record, customise and run and the reporting
    functions are excellent.


.. _Testing authenticated reads:

3. Testing authenticated reads
==============================
    
    Reading all the possible URLs in the site authenticated was deemed
    impractical due to the amount of time potentially required to do one
    `Funkload`_ cycle.  In order to decide which URLs to use for the authenticated
    read tests we created a `Funkload`_ test that reads all the content
    unauthenticated (results available here: `Science unauthenticated read`_).  This
    test was run with only 1 user and 1 cycle.

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

Page analysis
-------------
  
Home page
^^^^^^^^^

    The unauthenticated home page load at **100 concurrent users** looks like this:
    
    ====================================================================================================================    ============
    URL                                                                                                                     Request time
    ====================================================================================================================    ============
    /                                                                                                                       1.337 s
    /css?family=Montserrat                                                                                                  1.124 s
    /                                                                                                                       1.245 s
    /portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css                                       1.120 s
    /portal_css/Sunburst%20Theme/dropdown-menu-cachekey-18dee82342b75f2c7bc0fa7b017feb61.css                                1.119 s
    /portal_css/Sunburst%20Theme/resourcetinymce.stylesheetstinymce-cachekey-ca7f99b34a27033d846be95c8de69be2.css           1.073 s
    /portal_css/Sunburst%20Theme/resourceplone.app.dexterity.overlays-cachekey-7ac1852449e6cb2ff27111e1cd7c4665.css         1.226 s
    /portal_css/Sunburst%20Theme/resourcecollective.topictreetopictree-cachekey-2a473052fae56de9ea0cbbec5dfaa63d.css        1.130 s
    /portal_css/Sunburst%20Theme/resourcethemesapplestyle-cachekey-902306361fbd1b097cea265775a7f6da.css                     1.137 s
    /portal_css/Sunburst%20Theme/themeemas.appcssstyles-cachekey-c58e347e4c0ca6ab98d3a4104c40af46.css                       1.177 s
    /portal_css/Sunburst%20Theme/themeemas.themecssstyles-cachekey-987e0b9963b14f5de16733ce5a566073.css                     1.269 s
    /portal_css/Sunburst%20Theme/ploneCustom-cachekey-74895962889ac3a836dba1b4b8323474.css                                  1.166 s
    /portal_kss/Sunburst%20Theme/at-cachekey-9d4065eabe538900e9c3dd6fa55b6acc.kss                                           1.229 s
    /favicon.ico                                                                                                            1.157 s
    /touch_icon.png                                                                                                         1.045 s
    /++theme++emas.theme/images/logo.png                                                                                    1.054 s
    /++theme++emas.theme/images/howitworks.png                                                                              1.108 s
    /++theme++emas.theme/images/graph.png                                                                                   1.179 s
    /++theme++emas.theme/images/answer_correct.png                                                                          1.035 s
    /++theme++emas.theme/images/answer_incorrect.png                                                                        1.161 s
    /++theme++emas.theme/images/dashboard.png                                                                               1.106 s
    /++theme++emas.theme/images/learnersdashboard.png                                                                       1.250 s
    /++theme++emas.theme/images/teachersdashboard.png                                                                       1.145 s
    /++theme++emas.theme/images/media.png                                                                                   1.176 s
    /++theme++emas.theme/images/textbooks.png                                                                               1.167 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png                                                         1.081 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg                                                                  1.047 s
    /++theme++emas.theme/images/psggroup.jpg                                                                                0.992 s
    /++theme++emas.theme/images/FaceBook-icon-small.png                                                                     1.069 s
    /++theme++emas.theme/images/Twitter-icon-small.png                                                                      1.019 s
    /++theme++emas.theme/images/cc_by.png                                                                                   1.071 s
    ====================================================================================================================    ============
   
    Thus we get a **total load time of 35.214 seconds**.  Bear in mind that this
    is for an initial load.  On initial load all the CSS and javascript will be
    fetched over the netword and cached by the browser.
    
    Subsequent unauthenticated loads look like this:

    =================================================================    ============
    URL                                                                  Request time
    =================================================================    ============
    /                                                                    1.337 s
    /                                                                    1.245 s
    /touch_icon.png                                                      1.045 s
    /++theme++emas.theme/images/logo.png                                 1.054 s
    /++theme++emas.theme/images/howitworks.png                           1.108 s
    /++theme++emas.theme/images/graph.png                                1.179 s
    /++theme++emas.theme/images/answer_correct.png                       1.035 s
    /++theme++emas.theme/images/answer_incorrect.png                     1.161 s
    /++theme++emas.theme/images/dashboard.png                            1.106 s
    /++theme++emas.theme/images/learnersdashboard.png                    1.250 s
    /++theme++emas.theme/images/teachersdashboard.png                    1.145 s
    /++theme++emas.theme/images/media.png                                1.176 s
    /++theme++emas.theme/images/textbooks.png                            1.167 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png      1.081 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg               1.047 s
    /++theme++emas.theme/images/psggroup.jpg                             0.992 s
    /++theme++emas.theme/images/FaceBook-icon-small.png                  1.069 s
    /++theme++emas.theme/images/Twitter-icon-small.png                   1.019 s
    /++theme++emas.theme/images/cc_by.png                                1.071 s
    =================================================================    ============

    Thus a load time of **21.287 seconds.**

Projected serve rates
"""""""""""""""""""""

    Working with these 2 figures we can project the following:

    Initial home pages per hour:
    (60 / 35.214) * 60 = **102.232**

    Subsequent home pages per hour:
    (60 / 21.287) * 60 = **169.117**

Higher concurrencies
"""""""""""""""""""""
    
250 concurrent users

    =================================================================    ============
    URL                                                                  Request time
    =================================================================    ============
    /                                                                    1.969 s
    /                                                                    2.200 s
    /touch_icon.png                                                      1.755 s
    /++theme++emas.theme/images/logo.png                                 1.542 s
    /++theme++emas.theme/images/howitworks.png                           1.409 s
    /++theme++emas.theme/images/graph.png                                1.510 s
    /++theme++emas.theme/images/answer_correct.png                       1.573 s
    /++theme++emas.theme/images/answer_incorrect.png                     1.884 s
    /++theme++emas.theme/images/dashboard.png                            1.512 s
    /++theme++emas.theme/images/learnersdashboard.png                    1.536 s
    /++theme++emas.theme/images/teachersdashboard.png                    1.453 s
    /++theme++emas.theme/images/media.png                                1.689 s
    /++theme++emas.theme/images/textbooks.png                            1.592 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png      1.603 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg               1.595 s
    /++theme++emas.theme/images/psggroup.jpg                             1.601 s
    /++theme++emas.theme/images/FaceBook-icon-small.png                  1.511 s
    /++theme++emas.theme/images/Twitter-icon-small.png                   1.584 s
    /++theme++emas.theme/images/cc_by.png                                1.434 s
    =================================================================    ============

    Load time per page:
    
    **30.952 seconds**

    Projected serve rate:

    (60 / 30.952) * 60 = **116.30 pages per hour.**

500 concurrent users

    =================================================================    ============
    URL                                                                  Request time
    =================================================================    ============
    /                                                                    6.978 s
    /                                                                    3.301 s
    /touch_icon.png                                                      6.399 s
    /++theme++emas.theme/images/logo.png                                 3.583 s
    /++theme++emas.theme/images/howitworks.png                           4.255 s
    /++theme++emas.theme/images/graph.png                                2.345 s
    /++theme++emas.theme/images/answer_correct.png                       2.344 s
    /++theme++emas.theme/images/answer_incorrect.png                     3.769 s
    /++theme++emas.theme/images/dashboard.png                            5.999 s
    /++theme++emas.theme/images/learnersdashboard.png                    3.485 s
    /++theme++emas.theme/images/teachersdashboard.png                    2.750 s
    /++theme++emas.theme/images/media.png                                1.944 s
    /++theme++emas.theme/images/textbooks.png                            2.506 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png      2.848 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg               3.320 s
    /++theme++emas.theme/images/psggroup.jpg                             2.667 s
    /++theme++emas.theme/images/FaceBook-icon-small.png                  1.665 s
    /++theme++emas.theme/images/Twitter-icon-small.png                   2.019 s
    /++theme++emas.theme/images/cc_by.png                                2.423 s
    =================================================================    ============

    Load time per page:
    
    **64.6 seconds**

    Projected serve rate:

    (60 / 64.6) * 60 = **55.72 pages per hour.**

750 concurrent users

    =================================================================    ============
    URL                                                                  Request time
    =================================================================    ============
    /                                                                    6.107 s
    /                                                                    7.159 s
    /touch_icon.png                                                      2.978 s
    /++theme++emas.theme/images/logo.png                                 5.180 s
    /++theme++emas.theme/images/howitworks.png                           5.429 s
    /++theme++emas.theme/images/graph.png                                5.712 s
    /++theme++emas.theme/images/answer_correct.png                       5.406 s
    /++theme++emas.theme/images/answer_incorrect.png                     3.615 s
    /++theme++emas.theme/images/dashboard.png                            6.164 s
    /++theme++emas.theme/images/learnersdashboard.png                    4.241 s
    /++theme++emas.theme/images/teachersdashboard.png                    2.094 s
    /++theme++emas.theme/images/media.png                                2.532 s
    /++theme++emas.theme/images/textbooks.png                            5.995 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png      3.456 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg               2.977 s
    /++theme++emas.theme/images/psggroup.jpg                             2.973 s
    /++theme++emas.theme/images/FaceBook-icon-small.png                  3.509 s
    /++theme++emas.theme/images/Twitter-icon-small.png                   3.960 s
    /++theme++emas.theme/images/cc_by.png                                1.655 s
    =================================================================    ============

    Load time per page:
    
    **81.142 seconds**

    Projected serve rate:

    (60 / 81.142) * 60 = **44.36 pages per hour.**

1000 concurrent users

    =================================================================    ============
    URL                                                                  Request time
    =================================================================    ============
    /                                                                    7.710 s
    /                                                                    1.807 s
    /touch_icon.png                                                      2.185 s
    /++theme++emas.theme/images/logo.png                                 2.001 s
    /++theme++emas.theme/images/howitworks.png                           4.991 s
    /++theme++emas.theme/images/graph.png                                2.312 s
    /++theme++emas.theme/images/answer_correct.png                       4.129 s
    /++theme++emas.theme/images/answer_incorrect.png                     7.016 s
    /++theme++emas.theme/images/dashboard.png                            3.769 s
    /++theme++emas.theme/images/learnersdashboard.png                    2.536 s
    /++theme++emas.theme/images/teachersdashboard.png                    2.102 s
    /++theme++emas.theme/images/media.png                                4.330 s
    /++theme++emas.theme/images/textbooks.png                            6.296 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png      3.881 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg               6.484 s
    /++theme++emas.theme/images/psggroup.jpg                             2.454 s
    /++theme++emas.theme/images/FaceBook-icon-small.png                  2.743 s
    /++theme++emas.theme/images/Twitter-icon-small.png                   5.625 s
    /++theme++emas.theme/images/cc_by.png                                6.470 s
    =================================================================    ============

    Load time per page:
    
    **78.841 seconds**

    Projected serve rate:

    (60 / 78.841) * 60 = **45.66 pages per hour.**

    It is quite clear that as the concurrency rises the cluster serves less-
    and-less pages per second, but never completely stops working.


Content pages
^^^^^^^^^^^^^

    Let's look at one of the `slow science pages`_ like we did with the home
    page.

    ===================================================================================    ============
    URL                                                                                    Request time
    ===================================================================================    ============
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus               0.990 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus/              1.086 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-02.cnxmlplus               4.221 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-04.cnxmlplus               1.842 s
    /grade-12/08-work-energy-and-power/pspictures/f70fc7e8583786ef8c496e4861d8f2b7.png     1.382 s
    /grade-12/08-work-energy-and-power/pspictures/24707967fddfb273f965a0cf7224ac0a.png     1.501 s
    /grade-12/08-work-energy-and-power/pspictures/22fc66e880fffb15853e6873faa1aa2b.png     1.152 s
    /grade-12/08-work-energy-and-power/++theme++emas.theme/images/cc_by.png                1.028 s
    ===================================================================================    ============

Projected serve rates
"""""""""""""""""""""

    It is clear that the javascript and CSS is not fetched again.  Given the
    above times we know that each page will take **13.202 seconds** to fetch at
    a load of **100 concurrent users**.

    This in turn means we can potentially serve:

    (60 / 13.202) * 60 = **272.68 pages per hour.**

Higher concurrencies
"""""""""""""""""""""

250 concurrent users

    ===================================================================================    ============
    URL                                                                                    Request time
    ===================================================================================    ============
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus               1.659 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus/              1.500 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-02.cnxmlplus               1.658 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-04.cnxmlplus               1.853 s
    /grade-12/08-work-energy-and-power/pspictures/f70fc7e8583786ef8c496e4861d8f2b7.png     1.875 s
    /grade-12/08-work-energy-and-power/pspictures/24707967fddfb273f965a0cf7224ac0a.png     1.809 s
    /grade-12/08-work-energy-and-power/pspictures/22fc66e880fffb15853e6873faa1aa2b.png     1.896 s
    /grade-12/08-work-energy-and-power/++theme++emas.theme/images/cc_by.png                1.624 s
    ===================================================================================    ============

    Page load time: **12.25 seconds**

    (60 / 12.25) * 60 = **293.87 pages per hour.**

500 concurrent users

    ===================================================================================    ============
    URL                                                                                    Request time
    ===================================================================================    ============
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus               2.010 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus/              6.123 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-02.cnxmlplus               1.787 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-04.cnxmlplus               1.891 s
    /grade-12/08-work-energy-and-power/pspictures/f70fc7e8583786ef8c496e4861d8f2b7.png     2.944 s
    /grade-12/08-work-energy-and-power/pspictures/24707967fddfb273f965a0cf7224ac0a.png     6.484 s
    /grade-12/08-work-energy-and-power/pspictures/22fc66e880fffb15853e6873faa1aa2b.png     2.117 s
    /grade-12/08-work-energy-and-power/++theme++emas.theme/images/cc_by.png                5.994 s
    ===================================================================================    ============

    Page load time: **29.35 seconds**

    (60 / 29.35) * 60 = **122.65 pages per hour.**

750 concurrent users

    ===================================================================================    ============
    URL                                                                                    Request time
    ===================================================================================    ============
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus               1.569 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus/              6.385 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-02.cnxmlplus               4.795 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-04.cnxmlplus               5.794 s
    /grade-12/08-work-energy-and-power/pspictures/f70fc7e8583786ef8c496e4861d8f2b7.png     4.397 s
    /grade-12/08-work-energy-and-power/pspictures/24707967fddfb273f965a0cf7224ac0a.png     5.453 s
    /grade-12/08-work-energy-and-power/pspictures/22fc66e880fffb15853e6873faa1aa2b.png     2.007 s
    /grade-12/08-work-energy-and-power/++theme++emas.theme/images/cc_by.png                4.610 s
    ===================================================================================    ============

    Page load time: **35.01 seconds**

    (60 / 35.01) * 60 = **102.82 pages per hour.**

1000 concurrent users

    ===================================================================================    ============
    URL                                                                                    Request time
    ===================================================================================    ============
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus               3.421 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-03.cnxmlplus/              1.985 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-02.cnxmlplus               1.886 s
    /grade-12/08-work-energy-and-power/08-work-energy-and-power-04.cnxmlplus               3.537 s
    /grade-12/08-work-energy-and-power/pspictures/f70fc7e8583786ef8c496e4861d8f2b7.png     7.234 s
    /grade-12/08-work-energy-and-power/pspictures/24707967fddfb273f965a0cf7224ac0a.png     6.397 s
    /grade-12/08-work-energy-and-power/pspictures/22fc66e880fffb15853e6873faa1aa2b.png     6.973 s
    /grade-12/08-work-energy-and-power/++theme++emas.theme/images/cc_by.png                3.309 s
    ===================================================================================    ============

    Page load time: **34.742 seconds**

    (60 / 34.742) * 60 = **103.62 pages per hour.**


Optimisations done
------------------
    
    During the testing process we realised that some elements in the pages are
    causing sub-optimal caching in Varnish.  This is due to elements like
    username and personal links which are unique to each authenticated user.
    These elements cause Varnish to view pages as different although very little
    actually differ between them.

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
    - `Apdex`_: 1.5


6. Results for testing practice service
=======================================

    Funkload bench report here: `Practise service test`_

Page analysis
-------------
  
Dashboard
^^^^^^^^^
    
    Authenticated read of the dashboard at 100 concurrent users:

    =================================================       ============
    URL                                                     Request time
    =================================================       ============
    /@@practice/grade-10                                    3.805 s
    /@@practice/dashboard                                   5.386 s
    /@@practice/static/practice.css                         4.291 s
    /@@practice/static/practice-ie8.css                     3.457 s
    /@@practice/static/jqplot/jquery.jqplot.min.css         1.873 s
    /@@practice/static/help-icon-no-shadow-16.png           1.553 s
    /@@practice/image/mastery_progress_3_115_0              1.421 s
    /@@practice/image/mastery_progress_3_115_115            1.400 s
    /@@practice/static/progress-up.png                      1.222 s
    /@@practice/static/gold-star-16.png                     1.135 s
    /@@practice/static/please_wait_24.gif                   0.875 s
    /@@practice/static/tick.png                             1.096 s
    /@@practice/static/gray-star-16.png                     0.819 s
    /@@practice/image/mastery_progress_4_0_0                0.961 s
    /@@practice/image/mastery_progress_3_0_0                0.906 s
    /@@practice/image/mastery_progress_1_0_0                0.980 s
    /@@practice/image/mastery_progress_2_0_0                0.912 s 
    /@@practice/image/mastery_progress_2_120_0              0.924 s
    /@@practice/image/mastery_progress_3_120_0              0.965 s
    /@@practice/image/mastery_progress_3_111_0              1.063 s
    /@@practice/image/mastery_progress_3_108_0              1.405 s
    /++theme++emas.theme/images/copyright.png               1.623 s
    /++theme++emas.theme/images/copyright.png               2.379 s
    =================================================       ============

Projected serve rates
"""""""""""""""""""""

    This gives us a  load time of **40.451 seconds per page at 100 
    concurrent users.**
    
    At this rate we can serve:

    (60 / 40.451) * 60 = **88.99 pages per hour.**

Higher concurrencies
"""""""""""""""""""""
    
150 concurrent users

    =================================================       ============
    URL                                                     Request time
    =================================================       ============
    /@@practice/grade-10                                    2.502 s
    /@@practice/dashboard                                   4.077 s
    /@@practice/static/practice.css                         2.601 s
    /@@practice/static/practice-ie8.css                     2.439 s
    /@@practice/static/jqplot/jquery.jqplot.min.css         2.383 s
    /@@practice/static/help-icon-no-shadow-16.png           2.432 s
    /@@practice/image/mastery_progress_3_115_0              2.282 s
    /@@practice/image/mastery_progress_3_115_115            2.516 s
    /@@practice/static/progress-up.png                      2.334 s
    /@@practice/static/gold-star-16.png                     2.420 s
    /@@practice/static/please_wait_24.gif                   2.432 s
    /@@practice/static/tick.png                             2.380 s
    /@@practice/static/gray-star-16.png                     2.377 s
    /@@practice/image/mastery_progress_4_0_0                2.309 s
    /@@practice/image/mastery_progress_3_0_0                2.305 s
    /@@practice/image/mastery_progress_1_0_0                2.411 s
    /@@practice/image/mastery_progress_2_0_0                2.417 s 
    /@@practice/image/mastery_progress_2_120_0              2.469 s
    /@@practice/image/mastery_progress_3_120_0              2.406 s
    /@@practice/image/mastery_progress_3_111_0              2.538 s
    /@@practice/image/mastery_progress_3_108_0              5.071 s
    /++theme++emas.theme/images/copyright.png               5.021 s
    /++theme++emas.theme/images/copyright.png               2.467 s
    =================================================       ============

    Page load time: **62.589 seconds**

    (60 / 62.589) * 60 = **57.51 pages per hour.**

200 concurrent users

    =================================================       ============
    URL                                                     Request time
    =================================================       ============
    /@@practice/grade-10                                    4.775 s
    /@@practice/dashboard                                   8.039 s
    /@@practice/static/practice.css                         5.130 s
    /@@practice/static/practice-ie8.css                     4.949 s
    /@@practice/static/jqplot/jquery.jqplot.min.css         4.692 s
    /@@practice/static/help-icon-no-shadow-16.png           4.743 s
    /@@practice/image/mastery_progress_3_115_0              5.308 s
    /@@practice/image/mastery_progress_3_115_115            4.980 s
    /@@practice/static/progress-up.png                      4.621 s
    /@@practice/static/gold-star-16.png                     4.873 s
    /@@practice/static/please_wait_24.gif                   4.716 s
    /@@practice/static/tick.png                             4.512 s
    /@@practice/static/gray-star-16.png                     4.862 s
    /@@practice/image/mastery_progress_4_0_0                4.720 s
    /@@practice/image/mastery_progress_3_0_0                4.853 s
    /@@practice/image/mastery_progress_1_0_0                4.706 s
    /@@practice/image/mastery_progress_2_0_0                4.683 s 
    /@@practice/image/mastery_progress_2_120_0              4.644 s
    /@@practice/image/mastery_progress_3_120_0              4.723 s
    /@@practice/image/mastery_progress_3_111_0              4.871 s
    /@@practice/image/mastery_progress_3_108_0              4.543 s
    /++theme++emas.theme/images/copyright.png               0.307 s
    /++theme++emas.theme/images/copyright.png               0.000 s
    =================================================       ============

    Page load time: **104.25 seconds**

    (60 / 104.25) * 60 = **34.532 pages per hour.**

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
        - `Apdex`_: 1.5

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
        - `Apdex`_: 1.5

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

Page analysis
-------------
  
Home page
^^^^^^^^^

    The unauthenticated mobile home page load at **100 concurrent users**:

    ===============================================================    ============
    URL                                                                Request time
    ===============================================================    ============
    /                                                                  0.650 s
    /++resource++gomobiletheme.basic/apple-touch-icon.png              0.547 s
    /++resource++gomobiletheme.basic/favicon.ico                       0.466 s
    /++resource++gomobiletheme.basic/common.css                        0.503 s
    /++resource++gomobiletheme.basic/lowend.css                        0.492 s
    /++resource++emas.mobiletheme/common.css                           0.475 s
    /++resource++emas.mobiletheme/lowend.css                           0.471 s
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png    0.468 s
    /++theme++emas.theme/images/shuttleworthfoundation.jpg             0.492 s
    /++theme++emas.theme/images/psggroup.jpg                           0.467 s
    /@@tracking_image?referer=                                         0.399 s
    ===============================================================    ============
    
    The page load time:
    
    **5.43 seconds per page**.

    Projected serve rate for initial mobile home pages load:
    
    (60 / 5.43) * 60 = **662.98 per hour**

Higher concurrencies
^^^^^^^^^^^^^^^^^^^^
    
250 concurrent users

    ===============================================================     ============
    URL                                                                 Request time
    ===============================================================     ============
    /                                                                   1.400                                                    
    /++resource++gomobiletheme.basic/apple-touch-icon.png               1.075                
    /++resource++gomobiletheme.basic/favicon.ico                        0.817
    /++resource++gomobiletheme.basic/common.css                         1.035
    /++resource++gomobiletheme.basic/lowend.css                         1.163
    /++resource++emas.mobiletheme/common.css                            0.815
    /++resource++emas.mobiletheme/lowend.css                            1.008
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png     1.221
    /++theme++emas.theme/images/shuttleworthfoundation.jpg              1.002
    /++theme++emas.theme/images/psggroup.jpg                            0.860
    /@@tracking_image?referer=                                          0.563
    ===============================================================     ============

    Load time per page:
    
    **10.959 seconds**

    Projected serve rate:

    (60 / 10.959) * 60 = **328.49 pages per hour.**

500 concurrent users

    ===============================================================     ============
    URL                                                                 Request time
    ===============================================================     ============
    /                                                                   2.924
    /++resource++gomobiletheme.basic/apple-touch-icon.png               2.914
    /++resource++gomobiletheme.basic/favicon.ico                        2.411
    /++resource++gomobiletheme.basic/common.css                         2.206
    /++resource++gomobiletheme.basic/lowend.css                         2.136
    /++resource++emas.mobiletheme/common.css                            2.136
    /++resource++emas.mobiletheme/lowend.css                            1.756
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png     0.794
    /++theme++emas.theme/images/shuttleworthfoundation.jpg              0.627
    /++theme++emas.theme/images/psggroup.jpg                            2.174
    /@@tracking_image?referer=                                          0.517
    ===============================================================     ============

    Load time per page:
    
    **20.595 seconds**

    Projected serve rate:

    (60 / 20.595) * 60 = **174.79 pages per hour.**

750 concurrent users

    ===============================================================     ============
    URL                                                                 Request time
    ===============================================================     ============
    /                                                                   4.701
    /++resource++gomobiletheme.basic/apple-touch-icon.png               3.063
    /++resource++gomobiletheme.basic/favicon.ico                        3.297
    /++resource++gomobiletheme.basic/common.css                         3.225
    /++resource++gomobiletheme.basic/lowend.css                         1.433
    /++resource++emas.mobiletheme/common.css                            3.162 
    /++resource++emas.mobiletheme/lowend.css                            2.130
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png     3.296
    /++theme++emas.theme/images/shuttleworthfoundation.jpg              3.241
    /++theme++emas.theme/images/psggroup.jpg                            3.510
    /@@tracking_image?referer=                                          1.967
    ===============================================================     ============

    Load time per page:
    
    **33.025 seconds**

    Projected serve rate:

    (60 / 33.025) * 60 = **109.00 pages per hour.**

1000 concurrent users

    ===============================================================     ============
    URL                                                                 Request time
    ===============================================================     ============
    /                                                                   5.841
    /++resource++gomobiletheme.basic/apple-touch-icon.png               4.649
    /++resource++gomobiletheme.basic/favicon.ico                        5.419
    /++resource++gomobiletheme.basic/common.css                         4.620
    /++resource++gomobiletheme.basic/lowend.css                         7.447 
    /++resource++emas.mobiletheme/common.css                            7.627
    /++resource++emas.mobiletheme/lowend.css                            7.533
    /++theme++emas.theme/images/Logo_transparentBackground-tiny.png     6.943
    /++theme++emas.theme/images/shuttleworthfoundation.jpg              7.573
    /++theme++emas.theme/images/psggroup.jpg                            4.350
    /@@tracking_image?referer=                                          7.125
    ===============================================================     ============

    Load time per page:
    
    **69.127 seconds**

    Projected serve rate:

    (60 / 69.127) * 60 = **52.07 pages per hour.**


Content pages
-------------

    This section is based on the `slowest authenticated mobile read page`_.

    ==================================================================  ============
    URL                                                                 Request time
    ==================================================================  ============
    /grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus  0.525
    /@@shortimageurl/AD510                                              0.423
    /@@shortimageurl/AD511                                              0.393
    /@@mobile_image?key=8b0bd8e3345bc429a3f636e3e07a04b2.png            0.533
    /@@shortimageurl/AD512                                              0.391
    /@@mobile_image?key=7b4be31b46722cd43d1015f116b7e3f1.png            0.545
    /@@mobile_image?key=2544b965c153fae51f6ac177de34b986.png            0.535
    /@@mobile_image?key=4ef3bf468cb48070148dd217b034f6fb.png            0.572
    /@@mobile_image?key=25ff2ae319e6ba28f424d0f3ec2b35ef.png            0.559
    /@@mobile_image?key=17ad0d1adc7278d5f3e157641fa0b2f4.png            0.542
    /@@mobile_image?key=9bd096913bfd88c059698f9ba8b048f1.png            0.527
    /@@mobile_image?key=459ea8be55b6b79c61c99e05997b9e51.png            0.533
    /@@mobile_image?key=6b720d16b7857a81b0d819ec3eac9c22.png            0.541
    /@@mobile_image?key=66a94ac3fd51ac936dbc297958d81b42.png            0.563
    /@@mobile_image?key=f8c53946f5e89a5ae16e7b52c94e96d8.png            0.563
    /@@mobile_image?key=feec6c6188f2085b8a4ef86211c90186.png            0.541
    /@@mobile_image?key=5bc4bd1f5144391739a4d4182410316b.png            0.544
    /@@mobile_image?key=8cd33db7801b1911c840342ec94d5ea8.png            0.539
    /@@mobile_image?key=7d907101d4391f5cc801a24951620ae8.png            0.566
    /@@mobile_image?key=49e1207917564b80288d171709bff3fe.png            0.530
    /@@mobile_image?key=4d4ea0f18c98b9e4f5d7093e58ef77c0.png            0.543
    /@@mobile_image?key=bc09066d6104bb4fbab0111d53bb0016.png            0.562
    /@@mobile_image?key=e73b83c8b7c167019c593db770184cae.png            0.556
    /@@mobile_image?key=b2c70956388cc07422c14767c28d74c5.png            0.566
    /@@mobile_image?key=3880dd8f0fe610278c12be30c42aee55.png            0.568
    /@@mobile_image?key=36ac7e4e5bb463b3cb64ea19bb31d7dc.png            0.523
    /@@mobile_image?key=3a514f9ebde121ec7d03284d4fb4422c.png            0.551
    /@@mobile_image?key=4b4b7c48f32657f30a6a772b218fb1a3.png            0.553
    /@@mobile_image?key=caf1848ad50defe990ea86337eab9233.png            0.545
    /@@mobile_image?key=1c87b254d6a03ccd80f634f5de8eafb3.png            0.540
    /@@mobile_image?key=afd7fbf97328485b45980cc6d9f78cca.png            0.543
    /@@mobile_image?key=6eb5016e88ad606a49030715e634f562.png            0.557
    /@@mobile_image?key=684344c5d30d01fa23632bca5018d909.png            0.575
    /@@mobile_image?key=90408fe81acaa6a987db7b19f69e845b.png            0.556
    /@@mobile_image?key=07f8b53830e827cc02010c031c122018.png            0.567
    /@@mobile_image?key=2ede975866d71d01a12b3a8c739fdd3b.png            0.553
    /@@mobile_image?key=1f56771a9c381b7011b68c754e7e999a.png            0.562
    /@@mobile_image?key=67d91b87621708c628b359ceb4981ab2.png            0.557
    /@@mobile_image?key=373e5902295de703a8d15ba2925b39a9.png            0.551
    /@@mobile_image?key=c481ece79b8392fdd694abac94373bb7.png            0.563
    /@@mobile_image?key=ee4eef421be8f235b8c0329c9e4dde65.png            0.525
    /@@mobile_image?key=331350c3e262bf7389b396bfffb626c2.png            0.526
    /@@mobile_image?key=6631e14cdf53d54a9d9924dd38c89558.png            0.554
    /@@mobile_image?key=978a5b8cef208724511317ae1502bffe.png            0.577
    /@@mobile_image?key=a2a25f6080dd8f9f9bd8d9690d76f395.png            0.568
    /@@mobile_image?key=6d71d5f52935a25d0f056ad5c8353135.png            0.552
    /@@mobile_image?key=e0115a83f9bc84e13d4ad902c70108c8.png            0.551
    /@@mobile_image?key=cb33acfe03c34e9dd056393ff3f7db6c.png            0.561
    /@@mobile_image?key=c9639e5974ddebc4b44b8f094c1ff1ee.png            0.582
    /@@mobile_image?key=c580ddcfdbd65c68d283e5d44b381983.png            0.550
    /@@mobile_image?key=aa920e645e3b49e93ef08208dee18d65.png            0.569
    /@@mobile_image?key=2be66372650893e9801a30d442a824a4.png            0.563
    /@@mobile_image?key=08a047ebe0b9a8343c6609d97d3f5b15.png            0.532
    /@@mobile_image?key=7eee7698552130868caf27f039e83f4f.png            0.558
    /@@mobile_image?key=24830c7d3309a812abbf432067034f00.png            0.563
    /@@mobile_image?key=d0cdb3ab8b7aa9bf07b6e31c805f1975.png            0.533
    /@@mobile_image?key=aac7a0d3c40b9d74083a6cd02769ca2b.png            0.553
    /@@mobile_image?key=9a8a89de6adeeff0c8368ea595d14a19.png            0.561
    /@@mobile_image?key=82ec43195a695b25afe09a0e577810e8.png            0.575
    /@@mobile_image?key=ad08b3b82e7745f1d181e6c9fe0fd47d.png            0.530
    /@@mobile_image?key=67b52a61dc6643e4fdf284e5aed9c8fa.png            0.547
    /@@mobile_image?key=679404c6ed73389212cb9b08cabf738d.png            0.517
    /@@mobile_image?key=8b4a7468255d9bb893a88be1123534aa.png            0.538
    /@@mobile_image?key=0e6f5ac561d3141863c38a6cd9fbb515.png            0.545
    /@@mobile_image?key=20039428e194368ece3c88967fd033f3.png            0.594
    /@@mobile_image?key=79d58bb3af55d24126228287f69b28ad.png            0.552
    /@@mobile_image?key=7eac6588f5c34d23d60b3f5d1a93bb31.png            0.540
    /@@mobile_image?key=0b32c74b52648019180ffcf0bea280b2.png            0.571
    /@@mobile_image?key=60ff5fa9f0ffe0b7b4bad3a9f9b2d6ea.png            0.548
    /@@shortimageurl/AD513                                              0.398
    /grade-10/05-the-periodic-table/@@tracking_image?referer=           0.421
    http://m.qap.everythingscience.co.za/grade-10/04-the-atom/
    04-the-atom-08.cnxmlplus                                            
    ==================================================================  ============

    Load time per page:
    
    **38.41 seconds**

    Projected serve rate:

    (60 / 38.41 seconds) * 60 = **93.7255922937 pages per hour.**

250 concurrent users

    ==================================================================  ============
    URL                                                                 Request time
    ==================================================================  ============
    /grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus  0.699
    /@@shortimageurl/AD510                                              0.484
    /@@shortimageurl/AD511                                              0.515
    /@@mobile_image?key=8b0bd8e3345bc429a3f636e3e07a04b2.png            0.759
    /@@shortimageurl/AD512                                              0.543
    /@@mobile_image?key=7b4be31b46722cd43d1015f116b7e3f1.png            0.747
    /@@mobile_image?key=2544b965c153fae51f6ac177de34b986.png            0.722
    /@@mobile_image?key=4ef3bf468cb48070148dd217b034f6fb.png            0.743
    /@@mobile_image?key=25ff2ae319e6ba28f424d0f3ec2b35ef.png            0.699
    /@@mobile_image?key=17ad0d1adc7278d5f3e157641fa0b2f4.png            0.716
    /@@mobile_image?key=9bd096913bfd88c059698f9ba8b048f1.png            0.755
    /@@mobile_image?key=459ea8be55b6b79c61c99e05997b9e51.png            0.724
    /@@mobile_image?key=6b720d16b7857a81b0d819ec3eac9c22.png            0.725
    /@@mobile_image?key=66a94ac3fd51ac936dbc297958d81b42.png            0.699
    /@@mobile_image?key=f8c53946f5e89a5ae16e7b52c94e96d8.png            0.728
    /@@mobile_image?key=feec6c6188f2085b8a4ef86211c90186.png            0.778
    /@@mobile_image?key=5bc4bd1f5144391739a4d4182410316b.png            0.757
    /@@mobile_image?key=8cd33db7801b1911c840342ec94d5ea8.png            0.702
    /@@mobile_image?key=7d907101d4391f5cc801a24951620ae8.png            0.689
    /@@mobile_image?key=49e1207917564b80288d171709bff3fe.png            0.722
    /@@mobile_image?key=4d4ea0f18c98b9e4f5d7093e58ef77c0.png            0.696
    /@@mobile_image?key=bc09066d6104bb4fbab0111d53bb0016.png            0.731
    /@@mobile_image?key=e73b83c8b7c167019c593db770184cae.png            0.722
    /@@mobile_image?key=b2c70956388cc07422c14767c28d74c5.png            0.748
    /@@mobile_image?key=3880dd8f0fe610278c12be30c42aee55.png            0.722
    /@@mobile_image?key=36ac7e4e5bb463b3cb64ea19bb31d7dc.png            0.879
    /@@mobile_image?key=3a514f9ebde121ec7d03284d4fb4422c.png            0.889
    /@@mobile_image?key=4b4b7c48f32657f30a6a772b218fb1a3.png            0.819
    /@@mobile_image?key=caf1848ad50defe990ea86337eab9233.png            1.084
    /@@mobile_image?key=1c87b254d6a03ccd80f634f5de8eafb3.png            0.718
    /@@mobile_image?key=afd7fbf97328485b45980cc6d9f78cca.png            0.793
    /@@mobile_image?key=6eb5016e88ad606a49030715e634f562.png            0.795
    /@@mobile_image?key=684344c5d30d01fa23632bca5018d909.png            0.698
    /@@mobile_image?key=90408fe81acaa6a987db7b19f69e845b.png            0.739
    /@@mobile_image?key=07f8b53830e827cc02010c031c122018.png            0.937
    /@@mobile_image?key=2ede975866d71d01a12b3a8c739fdd3b.png            0.817
    /@@mobile_image?key=1f56771a9c381b7011b68c754e7e999a.png            0.845
    /@@mobile_image?key=67d91b87621708c628b359ceb4981ab2.png            1.089
    /@@mobile_image?key=373e5902295de703a8d15ba2925b39a9.png            0.700
    /@@mobile_image?key=c481ece79b8392fdd694abac94373bb7.png            0.715
    /@@mobile_image?key=ee4eef421be8f235b8c0329c9e4dde65.png            0.755
    /@@mobile_image?key=331350c3e262bf7389b396bfffb626c2.png            0.802
    /@@mobile_image?key=6631e14cdf53d54a9d9924dd38c89558.png            0.772
    /@@mobile_image?key=978a5b8cef208724511317ae1502bffe.png            0.688
    /@@mobile_image?key=a2a25f6080dd8f9f9bd8d9690d76f395.png            0.895
    /@@mobile_image?key=6d71d5f52935a25d0f056ad5c8353135.png            0.833
    /@@mobile_image?key=e0115a83f9bc84e13d4ad902c70108c8.png            0.750
    /@@mobile_image?key=cb33acfe03c34e9dd056393ff3f7db6c.png            0.729
    /@@mobile_image?key=c9639e5974ddebc4b44b8f094c1ff1ee.png            0.695
    /@@mobile_image?key=c580ddcfdbd65c68d283e5d44b381983.png            0.729
    /@@mobile_image?key=aa920e645e3b49e93ef08208dee18d65.png            0.800
    /@@mobile_image?key=2be66372650893e9801a30d442a824a4.png            0.738
    /@@mobile_image?key=08a047ebe0b9a8343c6609d97d3f5b15.png            0.740
    /@@mobile_image?key=7eee7698552130868caf27f039e83f4f.png            0.697
    /@@mobile_image?key=24830c7d3309a812abbf432067034f00.png            0.747
    /@@mobile_image?key=d0cdb3ab8b7aa9bf07b6e31c805f1975.png            0.937
    /@@mobile_image?key=aac7a0d3c40b9d74083a6cd02769ca2b.png            0.736
    /@@mobile_image?key=9a8a89de6adeeff0c8368ea595d14a19.png            0.761
    /@@mobile_image?key=82ec43195a695b25afe09a0e577810e8.png            0.683
    /@@mobile_image?key=ad08b3b82e7745f1d181e6c9fe0fd47d.png            0.729
    /@@mobile_image?key=67b52a61dc6643e4fdf284e5aed9c8fa.png            0.691
    /@@mobile_image?key=679404c6ed73389212cb9b08cabf738d.png            0.979
    /@@mobile_image?key=8b4a7468255d9bb893a88be1123534aa.png            0.846
    /@@mobile_image?key=0e6f5ac561d3141863c38a6cd9fbb515.png            0.828
    /@@mobile_image?key=20039428e194368ece3c88967fd033f3.png            0.945
    /@@mobile_image?key=79d58bb3af55d24126228287f69b28ad.png            0.680
    /@@mobile_image?key=7eac6588f5c34d23d60b3f5d1a93bb31.png            0.650
    /@@mobile_image?key=0b32c74b52648019180ffcf0bea280b2.png            0.697
    /@@mobile_image?key=60ff5fa9f0ffe0b7b4bad3a9f9b2d6ea.png            0.749
    /@@shortimageurl/AD513                                              1.492
    /grade-10/05-the-periodic-table/@@tracking_image?referer=           0.526
    http://m.qap.everythingscience.co.za/grade-10/04-the-atom/
    04-the-atom-08.cnxmlplus                                            
    ==================================================================  ============

    Load time per page:
    
    **54.341 seconds**

    Projected serve rate:

    (60 / 54.341 seconds) * 60 = **66.24 pages per hour.**


500 concurrent users

    ==================================================================  ============
    URL                                                                 Request time
    ==================================================================  ============
    /grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus  0.768
    /@@shortimageurl/AD510                                              0.523
    /@@shortimageurl/AD511                                              0.546
    /@@mobile_image?key=8b0bd8e3345bc429a3f636e3e07a04b2.png            0.677
    /@@shortimageurl/AD512                                              0.513
    /@@mobile_image?key=7b4be31b46722cd43d1015f116b7e3f1.png            0.735
    /@@mobile_image?key=2544b965c153fae51f6ac177de34b986.png            0.685
    /@@mobile_image?key=4ef3bf468cb48070148dd217b034f6fb.png            0.718
    /@@mobile_image?key=25ff2ae319e6ba28f424d0f3ec2b35ef.png            0.686
    /@@mobile_image?key=17ad0d1adc7278d5f3e157641fa0b2f4.png            0.786
    /@@mobile_image?key=9bd096913bfd88c059698f9ba8b048f1.png            0.685
    /@@mobile_image?key=459ea8be55b6b79c61c99e05997b9e51.png            0.688
    /@@mobile_image?key=6b720d16b7857a81b0d819ec3eac9c22.png            0.788
    /@@mobile_image?key=66a94ac3fd51ac936dbc297958d81b42.png            1.105
    /@@mobile_image?key=f8c53946f5e89a5ae16e7b52c94e96d8.png            0.754
    /@@mobile_image?key=feec6c6188f2085b8a4ef86211c90186.png            0.775
    /@@mobile_image?key=5bc4bd1f5144391739a4d4182410316b.png            0.724
    /@@mobile_image?key=8cd33db7801b1911c840342ec94d5ea8.png            0.799
    /@@mobile_image?key=7d907101d4391f5cc801a24951620ae8.png            0.727
    /@@mobile_image?key=49e1207917564b80288d171709bff3fe.png            0.717
    /@@mobile_image?key=4d4ea0f18c98b9e4f5d7093e58ef77c0.png            0.718
    /@@mobile_image?key=bc09066d6104bb4fbab0111d53bb0016.png            0.704
    /@@mobile_image?key=e73b83c8b7c167019c593db770184cae.png            1.901
    /@@mobile_image?key=b2c70956388cc07422c14767c28d74c5.png            0.784
    /@@mobile_image?key=3880dd8f0fe610278c12be30c42aee55.png            0.694
    /@@mobile_image?key=36ac7e4e5bb463b3cb64ea19bb31d7dc.png            0.699
    /@@mobile_image?key=3a514f9ebde121ec7d03284d4fb4422c.png            0.729
    /@@mobile_image?key=4b4b7c48f32657f30a6a772b218fb1a3.png            0.706
    /@@mobile_image?key=caf1848ad50defe990ea86337eab9233.png            0.694
    /@@mobile_image?key=1c87b254d6a03ccd80f634f5de8eafb3.png            0.723
    /@@mobile_image?key=afd7fbf97328485b45980cc6d9f78cca.png            1.054
    /@@mobile_image?key=6eb5016e88ad606a49030715e634f562.png            0.722
    /@@mobile_image?key=684344c5d30d01fa23632bca5018d909.png            0.736
    /@@mobile_image?key=90408fe81acaa6a987db7b19f69e845b.png            0.777
    /@@mobile_image?key=07f8b53830e827cc02010c031c122018.png            0.658
    /@@mobile_image?key=2ede975866d71d01a12b3a8c739fdd3b.png            0.781
    /@@mobile_image?key=1f56771a9c381b7011b68c754e7e999a.png            1.012
    /@@mobile_image?key=67d91b87621708c628b359ceb4981ab2.png            0.775
    /@@mobile_image?key=373e5902295de703a8d15ba2925b39a9.png            0.704
    /@@mobile_image?key=c481ece79b8392fdd694abac94373bb7.png            0.692
    /@@mobile_image?key=ee4eef421be8f235b8c0329c9e4dde65.png            0.716
    /@@mobile_image?key=331350c3e262bf7389b396bfffb626c2.png            0.706
    /@@mobile_image?key=6631e14cdf53d54a9d9924dd38c89558.png            0.675
    /@@mobile_image?key=978a5b8cef208724511317ae1502bffe.png            0.689
    /@@mobile_image?key=a2a25f6080dd8f9f9bd8d9690d76f395.png            1.239
    /@@mobile_image?key=6d71d5f52935a25d0f056ad5c8353135.png            0.766
    /@@mobile_image?key=e0115a83f9bc84e13d4ad902c70108c8.png            0.738
    /@@mobile_image?key=cb33acfe03c34e9dd056393ff3f7db6c.png            0.778
    /@@mobile_image?key=c9639e5974ddebc4b44b8f094c1ff1ee.png            0.746
    /@@mobile_image?key=c580ddcfdbd65c68d283e5d44b381983.png            1.721
    /@@mobile_image?key=aa920e645e3b49e93ef08208dee18d65.png            0.736
    /@@mobile_image?key=2be66372650893e9801a30d442a824a4.png            0.670
    /@@mobile_image?key=08a047ebe0b9a8343c6609d97d3f5b15.png            1.164
    /@@mobile_image?key=7eee7698552130868caf27f039e83f4f.png            0.674
    /@@mobile_image?key=24830c7d3309a812abbf432067034f00.png            0.800
    /@@mobile_image?key=d0cdb3ab8b7aa9bf07b6e31c805f1975.png            0.701
    /@@mobile_image?key=aac7a0d3c40b9d74083a6cd02769ca2b.png            0.676
    /@@mobile_image?key=9a8a89de6adeeff0c8368ea595d14a19.png            1.033
    /@@mobile_image?key=82ec43195a695b25afe09a0e577810e8.png            0.698
    /@@mobile_image?key=ad08b3b82e7745f1d181e6c9fe0fd47d.png            0.768
    /@@mobile_image?key=67b52a61dc6643e4fdf284e5aed9c8fa.png            0.662
    /@@mobile_image?key=679404c6ed73389212cb9b08cabf738d.png            0.795
    /@@mobile_image?key=8b4a7468255d9bb893a88be1123534aa.png            0.894
    /@@mobile_image?key=0e6f5ac561d3141863c38a6cd9fbb515.png            0.714
    /@@mobile_image?key=20039428e194368ece3c88967fd033f3.png            0.730
    /@@mobile_image?key=79d58bb3af55d24126228287f69b28ad.png            0.750
    /@@mobile_image?key=7eac6588f5c34d23d60b3f5d1a93bb31.png            0.743
    /@@mobile_image?key=0b32c74b52648019180ffcf0bea280b2.png            0.806
    /@@mobile_image?key=60ff5fa9f0ffe0b7b4bad3a9f9b2d6ea.png            0.671
    /@@shortimageurl/AD513                                              1.091
    /grade-10/05-the-periodic-table/@@tracking_image?referer=           0.560
    http://m.qap.everythingscience.co.za/grade-10/04-the-atom/
    04-the-atom-08.cnxmlplus                                            
    ==================================================================  ============

    Load time per page:
    
    **55.772 seconds**

    Projected serve rate:

    (60 / 55.772 seconds) * 60 = **64.5485189701 pages per hour.**


750 concurrent users

    ==================================================================  ============
    URL                                                                 Request time
    ==================================================================  ============
    /grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus  0.683 
    /@@shortimageurl/AD510                                              0.569
    /@@shortimageurl/AD511                                              0.564
    /@@mobile_image?key=8b0bd8e3345bc429a3f636e3e07a04b2.png            0.691
    /@@shortimageurl/AD512                                              1.368
    /@@mobile_image?key=7b4be31b46722cd43d1015f116b7e3f1.png            1.591
    /@@mobile_image?key=2544b965c153fae51f6ac177de34b986.png            0.750
    /@@mobile_image?key=4ef3bf468cb48070148dd217b034f6fb.png            0.837
    /@@mobile_image?key=25ff2ae319e6ba28f424d0f3ec2b35ef.png            0.792
    /@@mobile_image?key=17ad0d1adc7278d5f3e157641fa0b2f4.png            0.715
    /@@mobile_image?key=9bd096913bfd88c059698f9ba8b048f1.png            0.785
    /@@mobile_image?key=459ea8be55b6b79c61c99e05997b9e51.png            0.761
    /@@mobile_image?key=6b720d16b7857a81b0d819ec3eac9c22.png            0.772
    /@@mobile_image?key=66a94ac3fd51ac936dbc297958d81b42.png            0.698
    /@@mobile_image?key=f8c53946f5e89a5ae16e7b52c94e96d8.png            0.732
    /@@mobile_image?key=feec6c6188f2085b8a4ef86211c90186.png            0.743
    /@@mobile_image?key=5bc4bd1f5144391739a4d4182410316b.png            0.714
    /@@mobile_image?key=8cd33db7801b1911c840342ec94d5ea8.png            0.824
    /@@mobile_image?key=7d907101d4391f5cc801a24951620ae8.png            0.750
    /@@mobile_image?key=49e1207917564b80288d171709bff3fe.png            0.680
    /@@mobile_image?key=4d4ea0f18c98b9e4f5d7093e58ef77c0.png            0.699
    /@@mobile_image?key=bc09066d6104bb4fbab0111d53bb0016.png            0.734
    /@@mobile_image?key=e73b83c8b7c167019c593db770184cae.png            2.621
    /@@mobile_image?key=b2c70956388cc07422c14767c28d74c5.png            1.531
    /@@mobile_image?key=3880dd8f0fe610278c12be30c42aee55.png            1.641
    /@@mobile_image?key=36ac7e4e5bb463b3cb64ea19bb31d7dc.png            0.696
    /@@mobile_image?key=3a514f9ebde121ec7d03284d4fb4422c.png            0.727
    /@@mobile_image?key=4b4b7c48f32657f30a6a772b218fb1a3.png            0.688
    /@@mobile_image?key=caf1848ad50defe990ea86337eab9233.png            1.517
    /@@mobile_image?key=1c87b254d6a03ccd80f634f5de8eafb3.png            3.306
    /@@mobile_image?key=afd7fbf97328485b45980cc6d9f78cca.png            1.658
    /@@mobile_image?key=6eb5016e88ad606a49030715e634f562.png            0.854
    /@@mobile_image?key=684344c5d30d01fa23632bca5018d909.png            0.737
    /@@mobile_image?key=90408fe81acaa6a987db7b19f69e845b.png            0.689
    /@@mobile_image?key=07f8b53830e827cc02010c031c122018.png            1.441
    /@@mobile_image?key=2ede975866d71d01a12b3a8c739fdd3b.png            2.192
    /@@mobile_image?key=1f56771a9c381b7011b68c754e7e999a.png            1.520
    /@@mobile_image?key=67d91b87621708c628b359ceb4981ab2.png            0.760
    /@@mobile_image?key=373e5902295de703a8d15ba2925b39a9.png            0.698
    /@@mobile_image?key=c481ece79b8392fdd694abac94373bb7.png            0.710
    /@@mobile_image?key=ee4eef421be8f235b8c0329c9e4dde65.png            3.119
    /@@mobile_image?key=331350c3e262bf7389b396bfffb626c2.png            0.742
    /@@mobile_image?key=6631e14cdf53d54a9d9924dd38c89558.png            1.497
    /@@mobile_image?key=978a5b8cef208724511317ae1502bffe.png            0.723
    /@@mobile_image?key=a2a25f6080dd8f9f9bd8d9690d76f395.png            2.794
    /@@mobile_image?key=6d71d5f52935a25d0f056ad5c8353135.png            1.952
    /@@mobile_image?key=e0115a83f9bc84e13d4ad902c70108c8.png            2.482
    /@@mobile_image?key=cb33acfe03c34e9dd056393ff3f7db6c.png            0.757
    /@@mobile_image?key=c9639e5974ddebc4b44b8f094c1ff1ee.png            0.765
    /@@mobile_image?key=c580ddcfdbd65c68d283e5d44b381983.png            0.727
    /@@mobile_image?key=aa920e645e3b49e93ef08208dee18d65.png            1.721
    /@@mobile_image?key=2be66372650893e9801a30d442a824a4.png            3.651
    /@@mobile_image?key=08a047ebe0b9a8343c6609d97d3f5b15.png            1.533
    /@@mobile_image?key=7eee7698552130868caf27f039e83f4f.png            0.693
    /@@mobile_image?key=24830c7d3309a812abbf432067034f00.png            0.823
    /@@mobile_image?key=d0cdb3ab8b7aa9bf07b6e31c805f1975.png            0.788
    /@@mobile_image?key=aac7a0d3c40b9d74083a6cd02769ca2b.png            0.780
    /@@mobile_image?key=9a8a89de6adeeff0c8368ea595d14a19.png            0.702
    /@@mobile_image?key=82ec43195a695b25afe09a0e577810e8.png            0.747
    /@@mobile_image?key=ad08b3b82e7745f1d181e6c9fe0fd47d.png            2.310
    /@@mobile_image?key=67b52a61dc6643e4fdf284e5aed9c8fa.png            0.676
    /@@mobile_image?key=679404c6ed73389212cb9b08cabf738d.png            0.778
    /@@mobile_image?key=8b4a7468255d9bb893a88be1123534aa.png            0.734
    /@@mobile_image?key=0e6f5ac561d3141863c38a6cd9fbb515.png            0.681
    /@@mobile_image?key=20039428e194368ece3c88967fd033f3.png            1.715
    /@@mobile_image?key=79d58bb3af55d24126228287f69b28ad.png            0.716
    /@@mobile_image?key=7eac6588f5c34d23d60b3f5d1a93bb31.png            1.645
    /@@mobile_image?key=0b32c74b52648019180ffcf0bea280b2.png            3.586
    /@@mobile_image?key=60ff5fa9f0ffe0b7b4bad3a9f9b2d6ea.png            0.738
    /@@shortimageurl/AD513                                              0.594
    /grade-10/05-the-periodic-table/@@tracking_image?referer=           0.559
    http://m.qap.everythingscience.co.za/grade-10/04-the-atom/
    04-the-atom-08.cnxmlplus                                            
    ==================================================================  ============

    Load time per page:
    
    **83.16 seconds**

    Projected serve rate:

    (60 / 83.166 seconds) * 60 = **43.28 pages per hour.**


1000 concurrent users

    ==================================================================  ============
    URL                                                                 Request time
    ==================================================================  ============
    /grade-10/05-the-periodic-table/05-the-periodic-table-01.cnxmlplus  2.154
    /@@shortimageurl/AD510                                              2.592
    /@@shortimageurl/AD511                                              2.078
    /@@mobile_image?key=8b0bd8e3345bc429a3f636e3e07a04b2.png            4.167
    /@@shortimageurl/AD512                                              0.886
    /@@mobile_image?key=7b4be31b46722cd43d1015f116b7e3f1.png            0.759
    /@@mobile_image?key=2544b965c153fae51f6ac177de34b986.png            0.716
    /@@mobile_image?key=4ef3bf468cb48070148dd217b034f6fb.png            1.039
    /@@mobile_image?key=25ff2ae319e6ba28f424d0f3ec2b35ef.png            4.390
    /@@mobile_image?key=17ad0d1adc7278d5f3e157641fa0b2f4.png            0.782
    /@@mobile_image?key=9bd096913bfd88c059698f9ba8b048f1.png            0.812
    /@@mobile_image?key=459ea8be55b6b79c61c99e05997b9e51.png            2.055
    /@@mobile_image?key=6b720d16b7857a81b0d819ec3eac9c22.png            2.154
    /@@mobile_image?key=66a94ac3fd51ac936dbc297958d81b42.png            1.971
    /@@mobile_image?key=f8c53946f5e89a5ae16e7b52c94e96d8.png            2.121
    /@@mobile_image?key=feec6c6188f2085b8a4ef86211c90186.png            0.676
    /@@mobile_image?key=5bc4bd1f5144391739a4d4182410316b.png            6.917
    /@@mobile_image?key=8cd33db7801b1911c840342ec94d5ea8.png            3.261
    /@@mobile_image?key=7d907101d4391f5cc801a24951620ae8.png            0.844
    /@@mobile_image?key=49e1207917564b80288d171709bff3fe.png            3.706
    /@@mobile_image?key=4d4ea0f18c98b9e4f5d7093e58ef77c0.png            0.759
    /@@mobile_image?key=bc09066d6104bb4fbab0111d53bb0016.png            2.128
    /@@mobile_image?key=e73b83c8b7c167019c593db770184cae.png            3.575
    /@@mobile_image?key=b2c70956388cc07422c14767c28d74c5.png            0.965
    /@@mobile_image?key=3880dd8f0fe610278c12be30c42aee55.png            4.933
    /@@mobile_image?key=36ac7e4e5bb463b3cb64ea19bb31d7dc.png            2.013
    /@@mobile_image?key=3a514f9ebde121ec7d03284d4fb4422c.png            1.605
    /@@mobile_image?key=4b4b7c48f32657f30a6a772b218fb1a3.png            2.167
    /@@mobile_image?key=caf1848ad50defe990ea86337eab9233.png            2.048
    /@@mobile_image?key=1c87b254d6a03ccd80f634f5de8eafb3.png            0.745
    /@@mobile_image?key=afd7fbf97328485b45980cc6d9f78cca.png            0.703
    /@@mobile_image?key=6eb5016e88ad606a49030715e634f562.png            0.957
    /@@mobile_image?key=684344c5d30d01fa23632bca5018d909.png            2.263
    /@@mobile_image?key=90408fe81acaa6a987db7b19f69e845b.png            0.738
    /@@mobile_image?key=07f8b53830e827cc02010c031c122018.png            0.681
    /@@mobile_image?key=2ede975866d71d01a12b3a8c739fdd3b.png            3.310
    /@@mobile_image?key=1f56771a9c381b7011b68c754e7e999a.png            5.699
    /@@mobile_image?key=67d91b87621708c628b359ceb4981ab2.png            4.468
    /@@mobile_image?key=373e5902295de703a8d15ba2925b39a9.png            4.395
    /@@mobile_image?key=c481ece79b8392fdd694abac94373bb7.png            3.702
    /@@mobile_image?key=ee4eef421be8f235b8c0329c9e4dde65.png            0.736
    /@@mobile_image?key=331350c3e262bf7389b396bfffb626c2.png            2.748
    /@@mobile_image?key=6631e14cdf53d54a9d9924dd38c89558.png            2.161
    /@@mobile_image?key=978a5b8cef208724511317ae1502bffe.png            7.801
    /@@mobile_image?key=a2a25f6080dd8f9f9bd8d9690d76f395.png            1.283
    /@@mobile_image?key=6d71d5f52935a25d0f056ad5c8353135.png            1.486
    /@@mobile_image?key=e0115a83f9bc84e13d4ad902c70108c8.png            0.855
    /@@mobile_image?key=cb33acfe03c34e9dd056393ff3f7db6c.png            2.089
    /@@mobile_image?key=c9639e5974ddebc4b44b8f094c1ff1ee.png            3.675
    /@@mobile_image?key=c580ddcfdbd65c68d283e5d44b381983.png            1.941
    /@@mobile_image?key=aa920e645e3b49e93ef08208dee18d65.png            2.869
    /@@mobile_image?key=2be66372650893e9801a30d442a824a4.png            0.695
    /@@mobile_image?key=08a047ebe0b9a8343c6609d97d3f5b15.png            3.190
    /@@mobile_image?key=7eee7698552130868caf27f039e83f4f.png            4.656
    /@@mobile_image?key=24830c7d3309a812abbf432067034f00.png            0.850
    /@@mobile_image?key=d0cdb3ab8b7aa9bf07b6e31c805f1975.png            6.472
    /@@mobile_image?key=aac7a0d3c40b9d74083a6cd02769ca2b.png            0.757
    /@@mobile_image?key=9a8a89de6adeeff0c8368ea595d14a19.png            2.568
    /@@mobile_image?key=82ec43195a695b25afe09a0e577810e8.png            1.964
    /@@mobile_image?key=ad08b3b82e7745f1d181e6c9fe0fd47d.png            0.772
    /@@mobile_image?key=67b52a61dc6643e4fdf284e5aed9c8fa.png            0.724
    /@@mobile_image?key=679404c6ed73389212cb9b08cabf738d.png            1.101
    /@@mobile_image?key=8b4a7468255d9bb893a88be1123534aa.png            2.848
    /@@mobile_image?key=0e6f5ac561d3141863c38a6cd9fbb515.png            2.148
    /@@mobile_image?key=20039428e194368ece3c88967fd033f3.png            0.722
    /@@mobile_image?key=79d58bb3af55d24126228287f69b28ad.png            0.895
    /@@mobile_image?key=7eac6588f5c34d23d60b3f5d1a93bb31.png            0.974
    /@@mobile_image?key=0b32c74b52648019180ffcf0bea280b2.png            1.974
    /@@mobile_image?key=60ff5fa9f0ffe0b7b4bad3a9f9b2d6ea.png            2.395
    /@@shortimageurl/AD513                                              0.653
    /grade-10/05-the-periodic-table/@@tracking_image?referer=
    http://m.qap.everythingscience.co.za/grade-10/04-the-atom/
    04-the-atom-08.cnxmlplus                                            5.730
    ==================================================================  ============

    Load time per page:
    
    **161.66 seconds**

    Projected serve rate:

    (60 / 161.666 seconds) * 60 = **22.26 pages per hour.**


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
