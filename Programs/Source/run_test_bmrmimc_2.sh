#!/bin/bash

# Parameters
BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=4
threshold=1
players_minus_1=$(($players - 1))


# Compile the programs
for i in test_bmrmimc_mult64_2; do
    #./compile.py -M -B $i || exit 1
    # -M gets rid of memory warnings but increases number of rounds
    # -l optimizes loops but causes compilation errors
    # -D removes dead code
    ./compile.py -D $i > output_step2.txt || exit 1
done

# Set up the player inputs
mkdir Player-Data
echo "5 -40" > Player-Data/Input-P0-0
echo "100 100 500 1000" > Player-Data/Input-P1-0

progs="./malicious-shamir-party.x"
rm output_step2.err
# Run online
for prog in $progs; do
    for i in $(eval echo "{0..$players_minus_1}"); do
	$prog -N $players -T $threshold -p $i -P $BLS_PRIME -npfs test_bmrmimc_mult64_2  >> output_step2.txt 2>> output_step2.err & pids[${i}]=$! 
    done
    for pid in ${pids[*]}; do
	wait $pid
    done
done

