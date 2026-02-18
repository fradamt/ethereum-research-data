---
source: ethresearch
topic_id: 4279
title: Anyone working on Solidity-verifiable VDF?
author: kladkogex
date: "2018-11-16"
category: Cryptography
tags: []
url: https://ethresear.ch/t/anyone-working-on-solidity-verifiable-vdf/4279
views: 5099
likes: 4
posts_count: 16
---

# Anyone working on Solidity-verifiable VDF?

I wonder if any one at this message board is looking on a VDF (verifiable delay function) which is efficiently verifiable in Solidity? We need random numbers in our project, and are looking on implementing such a VDF.  The question is, how much gas would it take to verify a VDF in Solidity, and is it practical to do it ?

## Replies

**JustinDrake** (2018-11-16):

In Ethereum 2.0 you should to get unbiasable random numbers almost for free via an EVM2.0 opcode. If you want a custom randomness scheme or a custom VDF at the application layer then the costs will depend on which VDF you use, the specifics of the prover, and potentially also the time parameter.

If you’re happy using SNARKs then the verification costs will be no larger than one SNARK verification as you can encapsulate the VDF verification steps in a SNARK. The proof sizes for the RSA VDFs we are considering for Ethereum 2.0 have proof sizes ranging  the order of 0.5kB to 10kB, and verification times are on the order of 0.5ms to 10ms where the bulk is modular multiplications. (The Wesolowski scheme also has about 0.1ms of primality testing.)

---

**kladkogex** (2018-11-16):

Justin - thank you.  We need it in ETH 1.0 since our network is going to go live before ETH 2.0 …

Now I understand that we can not do Weselowski since we cant do primality testing in Solidity …

I think using SNARKS is a great idea.  Do you mean like doing lots of SHA sequential hashes and doing a SNARK proof for it, which is verified in Solidity ?)) In your opinion, what would be the optimal function to do inside the SNARK?

---

**JustinDrake** (2018-11-16):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> We need it in ETH 1.0 since our network is going to go live before ETH 2.0 …

An important consideration is what commodity hardware you intend to use. Anything less than a top-of-the-range FPGA is probably a non-starter, unless you only need randomness very infrequently and use a large A_max.

> Do you mean like doing lots of SHA sequential hashes and doing a SNARK proof for it, which is verified in Solidity

You could use Guralnick and Muller polynomials (see page 18 [here](https://eprint.iacr.org/2018/601.pdf)) combined with SNARKs but these polynomials haven’t really been stress tested for security.

> I think using SNARKS is a great idea.

I was thinking of doing a first round of [Pietrzak](https://eprint.iacr.org/2018/627.pdf) or Wesolowski and then shrinking the proof using a SNARK to save on gas. Unfortunately RSA doesn’t play super well with SNARKs. Benedikt Bunz pointed to [this paper](https://eprint.iacr.org/2015/1093.pdf) which brought down RSA key exchange to 435k gates (for reference a sapling Zcash transaction is about 100k gates).

---

**kladkogex** (2018-11-20):

Justin - thank you.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> An important consideration is what commodity hardware you intend to use. Anything less than a top-of-the-range FPGA is probably a non-starter, unless you only need randomness very infrequently and use a large A_max.

In our case we need RNG to pick servers for a side chain from a large server network, this needs to happen once in a life time of a side chain. It is OK for us to have three hour wait-out time, so essentially as long as the attacker is not 1000 times faster than we, we are fine …

---

**JustinDrake** (2018-11-20):

> this needs to happen once in a life time of a side chain

Oh, that’s ideal. Can you just use a massive SHA3 hash chain with collaterisation and TrueBit-style challenges? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kladkogex** (2018-11-21):

I think we can … Then we need to get the challengers … We are just a tiny startup with a tiny network - nobody would probably want to be a challenger ![:sob:](https://ethresear.ch/images/emoji/facebook_messenger/sob.png?v=9)

---

**kladkogex** (2018-11-21):

Here is an interesting paper on graphene-based transistors that can work at 100 GZ

https://pdfs.semanticscholar.org/3163/bd8eeee14ef3c0ba5962f0927df769ab0994.pdf

Theoretically using graphene you can do 25 faster VDF calculations than a custom ASIC that works at 4GZ …

And then there are DARPA programs for ultrafast GaAs transistors that can operate  at up to 1THZ



      [antena.fe.uni-lj.si](https://antena.fe.uni-lj.si/literatura/Razno/Konferenca%20midem%202015/hemt/06005329.pdf)



    https://antena.fe.uni-lj.si/literatura/Razno/Konferenca%20midem%202015/hemt/06005329.pdf

###



1571.10 KB










Also there is research that if you replace electrons with laser light, you can build transistors 1M times (!) faster than silicon ASIC


      ![](https://ethresear.ch/uploads/default/original/3X/8/1/81c7702801d8bb8f125dcd1af7fa3fae1dd0bed9.png)

      [Live Science – 14 May 18](https://www.livescience.com/62561-laser-computer-speed-quantum.html)



    ![](https://ethresear.ch/uploads/default/optimized/3X/f/b/fb5ecc978d917c2892f6f2180617dec6bf1909b4_2_690x460.jpeg)

###



Pulses of light from infrared lasers can speed up computer operations by a factor of 1 million, and may have opened the door to room-temperature quantum computing.










So it looks like doing a VDF on a PC is not really practical. And even an FPGA based VDF based on regular silicon chips may be not so secure …

---

**kilic** (2021-04-20):

I’ve implemented Wesolowski VDF verifier in solidity for 2048 bit RSA settings. Verification takes around 200k gas after eip2565.



      [github.com](https://github.com/kilic/evmvdf)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/1/a/1ac6246cb1043969157b7dc1b060038e1eddcd4d_2_690x344.png)



###



Delay Function Verification Smart Contract

---

**kladkogex** (2021-04-20):

Nice!

We will look into it

---

**kelly** (2021-04-23):

There is an RSA VDF verifier in Solidity here by [@pvienhage](/u/pvienhage) : [GitHub - 0xProject/VDF: A Solidity implementation of a VDF verifier contract](https://github.com/0xProject/VDF)

---

**pvienhage** (2021-04-23):

It’s definitely not production ready though

---

**guthlStarkware** (2021-04-26):

VeeDoo is production ready. https://github.com/starkware-libs/veedo

---

**kladkogex** (2021-05-07):

Nice!

We may use it at SKALE in the next release

---

**Mister-Meeseeks** (2021-05-07):

This might not be pure enough for your purposes, but one quick and dirty way to harvest random entropy on-chain is to leverage the Efficient Market Hypothesis.

Pick some trading pair and medium-frequency horizon, where price movements are approximately normal. Say 5 minutes on ETH/USDT. Collect one bit of entropy using the following formula:

- Price moves up by at least one sigma (and holds for 5+ blocks)        →     1
- Price moves down by at least one sigma (and holds for 5+ blocks)   →     0
- Otherwise, no entropy. Wait another period.

An attacker would have to spend very large resources to manipulate a liquid market. The reason we add 5+ blocks, is because it prevents an attacker from manipulating within a single block or a hostile miner from manipulating within a consecutive sequence of blocks that it controls. 5+ blocks requires genuine defense against speculative attacks by arbitrageurs.

You can also accelerate the entropy rate by looking at multiple markets, but you have to make sure to de-correlate the cross-sectional returns so that the bits are independent.

---

**keithc** (2023-07-24):

Hi [@kilic](/u/kilic)

I am a bit late into this conversation, but I had a look at the repository above ([GitHub - kilic/evmvdf: Delay Function Verification Smart Contract](https://github.com/kilic/evmvdf)). Great work!! However, it has 2 fundamental issues that I can see:

1. Fractional division
It is doing a division to a fractional value (0…1), and decimals are not supported in the big num library, eg const b = r2.div(challenge.l);
2. Modular exponentiation
The Wesolowski paper and other implementations (eg GitHub - poanetwork/vdf: An implementation of Verifiable Delay Functions in Rust) do not use the RSA modulus in their pow functions, instead uses GMP’s pure pow function.

Because of (1) the evaluator in vdf.ts will not work. And for (2), I am not sure the implication of using modm over pow, and since it is different from the formula in the paper, will it open the solution up to potential attacks?

