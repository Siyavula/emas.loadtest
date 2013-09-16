#! /bin/bash

mkdir 1cus
cd 1cus
ab -e varnish_ab_test_1_100.csv -g varnish_ab_test_1_100.gnuplot -c 1 -n 100 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_100.txt
ab -e varnish_ab_test_1_1000.csv -g varnish_ab_test_1_1000.gnuplot -c 1 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_1000.txt
ab -e varnish_ab_test_1_10000.csv -g varnish_ab_test_1_10000.gnuplot -c 1 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_10000.txt
ab -e varnish_ab_test_1_20000.csv -g varnish_ab_test_1_20000.gnuplot -c 1 -n 20000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_20000.txt
ab -e varnish_ab_test_1_30000.csv -g varnish_ab_test_1_30000.gnuplot -c 1 -n 30000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_30000.txt
ab -e varnish_ab_test_1_40000.csv -g varnish_ab_test_1_40000.gnuplot -c 1 -n 40000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_40000.txt
ab -e varnish_ab_test_1_50000.csv -g varnish_ab_test_1_50000.gnuplot -c 1 -n 50000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_50000.txt
ab -e varnish_ab_test_1_100000.csv -g varnish_ab_test_1_100000.gnuplot -c 1 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_100000.txt
ab -e varnish_ab_test_1_1000000.csv -g varnish_ab_test_1_1000000.gnuplot -c 1 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_1000000.txt

cd ..
mkdir 10cus
cd 10cus
ab -e varnish_ab_test_10_10.csv -g varnish_ab_test_10_10.gnuplot -c 10 -n 10 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_10_10.txt
ab -e varnish_ab_test_10_100.csv -g varnish_ab_test_10_100.gnuplot -c 10 -n 100 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_10_100.txt
ab -e varnish_ab_test_10_1000.csv -g varnish_ab_test_10_1000.gnuplot -c 10 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_10_1000.txt
ab -e varnish_ab_test_10_10000.csv -g varnish_ab_test_10_10000.gnuplot -c 10 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_10_10000.txt
ab -e varnish_ab_test_10_100000.csv -g varnish_ab_test_10_100000.gnuplot -c 10 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_10_100000.txt
ab -e varnish_ab_test_10_1000000.csv -g varnish_ab_test_10_1000000.gnuplot -c 10 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_10_1000000.txt

cd ..
mkdir 100cus
cd 100cus
ab -e varnish_ab_test_1_100.csv -g varnish_ab_test_1_100.gnuplot -c 1 -n 100 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1_100.txt
ab -e varnish_ab_test_100_1000.csv -g varnish_ab_test_100_1000.gnuplot -c 100 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_100_1000.txt
ab -e varnish_ab_test_100_10000.csv -g varnish_ab_test_100_10000.gnuplot -c 100 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_100_10000.txt
ab -e varnish_ab_test_100_100000.csv -g varnish_ab_test_100_100000.gnuplot -c 100 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_100_100000.txt
ab -e varnish_ab_test_100_1000000.csv -g varnish_ab_test_100_1000000.gnuplot -c 100 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_100_1000000.txt

cd ..
mkdir 250cus
cd 250cus/
ab -e varnish_ab_test_250_100.csv -g varnish_ab_test_250_100.gnuplot -c 250 -n 100 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_100.txt
ab -e varnish_ab_test_250_250.csv -g varnish_ab_test_250_250.gnuplot -c 250 -n 250 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_250.txt
ab -e varnish_ab_test_250_250.csv -g varnish_ab_test_250_1000.gnuplot -c 250 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_1000.txt
ab -e varnish_ab_test_250_250.csv -g varnish_ab_test_250_10000.gnuplot -c 250 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_10000.txt
ab -e varnish_ab_test_250_250.csv -g varnish_ab_test_250_250.gnuplot -c 250 -n 250 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_250.txt
ab -e varnish_ab_test_250_1000.csv -g varnish_ab_test_250_1000.gnuplot -c 250 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_1000.txt
ab -e varnish_ab_test_250_10000.csv -g varnish_ab_test_250_10000.gnuplot -c 250 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_10000.txt
ab -e varnish_ab_test_250_100000.csv -g varnish_ab_test_250_100000.gnuplot -c 250 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_100000.txt
ab -e varnish_ab_test_250_1000000.csv -g varnish_ab_test_250_1000000.gnuplot -c 250 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_250_1000000.txt

cd ..
mkdir 500cus
cd 500cus/
ab -e varnish_ab_test_500_500.csv -g varnish_ab_test_500_500.gnuplot -c 500 -n 500 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_500_500.txt
ab -e varnish_ab_test_500_1000.csv -g varnish_ab_test_500_1000.gnuplot -c 500 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_500_1000.txt
ab -e varnish_ab_test_500_10000.csv -g varnish_ab_test_500_10000.gnuplot -c 500 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_500_10000.txt
ab -e varnish_ab_test_500_100000.csv -g varnish_ab_test_500_100000.gnuplot -c 500 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_500_100000.txt
ab -e varnish_ab_test_500_1000000.csv -g varnish_ab_test_500_1000000.gnuplot -c 500 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_500_1000000.txt

cd ..
mkdir 750cus
cd 750
cd 750cus/
ab -e varnish_ab_test_750_750.csv -g varnish_ab_test_750_750.gnuplot -c 750 -n 750 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_750_750.txt
ab -e varnish_ab_test_750_1000.csv -g varnish_ab_test_750_1000.gnuplot -c 750 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_750_1000.txt
ab -e varnish_ab_test_750_10000.csv -g varnish_ab_test_750_10000.gnuplot -c 750 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_750_10000.txt
ab -e varnish_ab_test_750_100000.csv -g varnish_ab_test_750_100000.gnuplot -c 750 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_750_100000.txt
ab -e varnish_ab_test_750_1000000.csv -g varnish_ab_test_750_1000000.gnuplot -c 750 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_750_1000000.txt

cd ..
mkdir 1000cus
cd 1000cus/
ab -e varnish_ab_test_1000_1000.csv -g varnish_ab_test_1000_1000.gnuplot -c 1000 -n 1000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1000_1000.txt
ab -e varnish_ab_test_1000_10000.csv -g varnish_ab_test_1000_10000.gnuplot -c 1000 -n 10000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1000_10000.txt
ab -e varnish_ab_test_1000_100000.csv -g varnish_ab_test_1000_100000.gnuplot -c 1000 -n 100000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1000_100000.txt
ab -e varnish_ab_test_1000_1000000.csv -g varnish_ab_test_1000_1000000.gnuplot -c 1000 -n 1000000 http://qap.everythingscience.co.za/portal_css/Sunburst%20Theme/public-cachekey-4fff4ed932d766e26813993d85f43eea.css|cat > varnish_ab_test_1000_1000000.txt

cd ..
ls -lha
