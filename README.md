
# BMR Escape Hatch Demo

This repo contains an MP-SPDZ proof of concept that allows for the use of extensive precomputation in order to later execute a boolean circuit in a constant number of rounds.

It proceeds in four steps which are sequentially dependent. The first step is input-independent precomputation while steps 2-4 are input-dependent and would be run in quick succession.

1) Circuit Generation: Generates a garbled circuit independent of program inputs, which can be evaluated later
2) Input Mapping: Convert secret-shared program inputs into wire labels
3) Local Evaluation: Use the wire labels to locally evaluate the garbled circuit
4) Output Mapping: Convert the GC outputs back into shared secrets

The boolean circuit used is an implementation of the HoneyBadgerSwap Trade function from this blog post: https://medium.com/initc3org/honeybadgerswap-making-mpc-as-a-sidechain-364bebdb10a5

The inputs are specified in the "input mapping" script (`Programs/Source/run_test_bmrmimc_2.sh`). Here P0 inputs the desired swap amounts for token A and token B, while P1 inputs the system data: the user's balances of both tokens and the pool's balances of both tokens.

#### Prerequisites
Clone the repo and run `make shamir` in the root directory. If that doesn't work then have fun figuring out docker :)

#### Running the demo 
From the root directory, run the following four scripts corresponding to the four program steps specified above

`./Programs/Source/run_test_bmrmimc_1.sh`
`./Programs/Source/run_test_bmrmimc_2.sh`
`./Programs/Source/run_test_bmrmimc_3.sh`
`./Programs/Source/run_test_bmrmimc_4.sh`

The program outputs are those following the "Output on next line" in the printout of the fourth scripts

Note that any of these steps can be rerun provided the previous step has been completed and its output isn't expected to change. So to change the inputs, modify the second script and rerun it (then run scripts 3 and 4). There is no need to rerun the first script (and running it is quite expensive)

#### Caution
This is research code. It also modifies MP-SPDZ itself, and so the programs contained herein will not work in other versions of MP-SPDZ.

