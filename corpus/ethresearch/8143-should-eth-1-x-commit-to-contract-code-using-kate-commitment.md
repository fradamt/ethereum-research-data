---
source: ethresearch
topic_id: 8143
title: Should ETH 1.x commit to contract code using kate commitments?
author: lithp
date: "2020-10-22"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/should-eth-1-x-commit-to-contract-code-using-kate-commitments/8143
views: 3717
likes: 6
posts_count: 2
---

# Should ETH 1.x commit to contract code using kate commitments?

In the most recent All Core Devs call [@vbuterin](/u/vbuterin) again [proposed](https://youtu.be/LDSTqo0LKUM?t=1588) that we use Kate Commitments when committing to contract code. They’ve been mentioned a few times before, starting a thread to centralize the discussion of whether we want to use them.

In stateless ethereum miners will need to add proofs for all executed code to the witness. Currently our proof sizes are linear in the size of the code, we must include the entire code segment. Our plan is [code merkelization](https://ethresear.ch/t/some-quick-numbers-on-code-merkelization/7260), which will give us proofs which grow logarithmically with the size of the contract code; [@sinamahmoodi](/u/sinamahmoodi) and others have done [a lot of work](https://eips.ethereum.org/EIPS/eip-2926) in that direction.

[Kate commitments](https://dankradfeist.de/ethereum/2020/06/16/kate-polynomial-commitments.html) go further; they promise constant sized proofs. The witness for a contract’s code will need to include the executed code chunks along with a single group element (~48 bytes), this is almost no overhead at all! Given that witness size is a key factor in whether stateless ethereum is possible at all this makes Kate commitments seem quite appealing.

It has a big drawback:

- It requires a trusted setup. As far as I can tell we will only need to run the trusted setup once, we can reuse the group it generates for each commitment.

To start things off, I think there are some open questions:

- How large are code merkle proofs, by how much would moving to Kate commitments reduce witness sizes?
- How much time does it take to create a commitment, create a proof, or verify a proof? I think these are relatively fast, but if this adds an additional second to block processing that’s likely not tenable.
- Has someone (Aztec?) already gone through a trusted setup, that we might use the group they’re using?
- What does running our own trusted setup require? We will have to pick an MPC protocol, write multiple independent implementations of the setup client, then advertise it and ask many people to run it. How much will this work delay stateless ethereum?
- I can’t tell for sure, but it seems that Kate commitments are not quantum-secure. Do we want to build a system which we’ll need to replace with something else in 5-10 years.

## Replies

**vbuterin** (2020-10-22):

> It requires a trusted setup. As far as I can tell we will only need to run the trusted setup once, we can reuse the group it generates for each commitment.

Correct. That said, the size of the trusted setup would be small (\approx 2^{10} would suffice, compared to the usual \approx 2^{24} to \approx 2^{28}). This means that we could make it *extremely* easy to participate (eg. you can participate in-browser), leading to a setup with many thousands of participants.

> How much time does it take to create a commitment, create a proof, or verify a proof?

Creating a commitment requires ~1 elliptic curve addition per byte (naively it’s 1 per bit, but you can use [fast linear combination algorithms](https://ethresear.ch/t/simple-guide-to-fast-linear-combinations-aka-multiexponentiations/7238) or even just precomputation tables over the trusted setup to greatly accelerate this). A normal ECMUL operation requires ~384 EC additions. So committing to 24 kB code is equivalent to ~62 ECMULs in cost. So the gas cost equivalent of making the commitment would be much lower than the 200 gas per byte in creating a contract.

> What does running our own trusted setup require? We will have to pick an MPC protocol, write multiple independent implementations of the setup client, then advertise it and ask many people to run it. How much will this work delay stateless ethereum?

In a universal updateable setup, the MPC is trivial. It’s just “I do my processing, pass the output to you, you do your processing, pass the output to Bob, Bob does his processing, passes his output to Charlie…”. As mentioned above, for trusted setups of this size you could even make the implementation in-browser, so lots of people could participate.

> I can’t tell for sure, but it seems that Kate commitments are not quantum-secure. Do we want to build a system which we’ll need to replace with something else in 5-10 years.

Neither are ECDSA signatures, or for that matter the BLS signatures that eth2 relies on. But I think we’re all assuming that by the time quantum computers hit we’ll have STARKs over Merkle proofs running extremely smoothly and we can just upgrade to that.

