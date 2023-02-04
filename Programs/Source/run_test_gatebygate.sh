#!/bin/bash

# Parameters
BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=4
threshold=1

# Compile the programs
for i in test_gatebygate; do
    ./compile.py $i || exit 1
done

# Setup the network authentication
#Scripts/setup-ssl.sh 4

# Set up the player inputs
mkdir Player-Data
echo "5 -40" > Player-Data/Input-P0-0
echo "100 100 500 1000" > Player-Data/Input-P1-0


progs="./malicious-shamir-party.x"
# Run online
for prog in $progs; do
    echo "Combined Offline/Online Experiment $prog"
    for i in 0 1 2 3; do
	$prog -N 4 -T 1 -p $i -P $BLS_PRIME test_gatebygate  & pids[${i}]=$!
    done
    for pid in ${pids[*]}; do
	wait $pid
    done
done
