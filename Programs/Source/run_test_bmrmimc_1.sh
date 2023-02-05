#!/bin/bash

# Parameters
BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=4
threshold=1
players_minus_1=$(($players - 1))

# Compile the programs
for i in test_bmrmimc_mult64_1; do
    #./compile.py -M -B $i || exit 1
    # -M gets rid of memory warnings but increases number of rounds
    # -l optimizes loops but causes compilation errors
    # -D removes dead code
    ./compile.py -D $i > output_step1.txt || exit 1
done

# Setup the network authentication
Scripts/setup-ssl.sh $players > /dev/null

mkdir Persistence
for i in $(eval echo "{0..$players_minus_1}"); do
    rm Persistence/Transactions-P$i-5000.data
    rm Persistence/Transactions-P$i.data
    touch Persistence/Transactions-P$i-5000.data
    touch Persistence/Transactions-P$i.data
done

progs="./malicious-shamir-party.x"
rm output_step1.err
# Run online
for prog in $progs; do
    for i in $(eval echo "{0..$players_minus_1}"); do
	$prog -N $players -T $threshold -p $i -P $BLS_PRIME test_bmrmimc_mult64_1  >> output_step1.txt 2>> output_step1.err & pids[${i}]=$! 
    done
    for pid in ${pids[*]}; do
	wait $pid
    done
done

