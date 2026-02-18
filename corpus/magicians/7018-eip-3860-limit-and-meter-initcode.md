---
source: magicians
topic_id: 7018
title: "EIP-3860: Limit and meter initcode"
author: axic
date: "2021-09-07"
category: EIPs > EIPs core
tags: [evm, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-3860-limit-and-meter-initcode/7018
views: 29813
likes: 5
posts_count: 17
---

# EIP-3860: Limit and meter initcode

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3860)





###



Limit the maximum size of initcode to 49152 and apply extra gas cost of 2 for every 32-byte chunk of initcode

## Replies

**axic** (2021-12-10):

This has been implemented in Geth ([core/vm: implement EIP-3860: Limit and meter initcode by gumb0 · Pull Request #23847 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/23847)) and state tests have been created ([Tests for EIP-3860: Limit and meter initcode by gumb0 · Pull Request #990 · ethereum/tests · GitHub](https://github.com/ethereum/tests/pull/990)).

---

**jochem-brouwer** (2021-12-15):

If a contract uses a `CREATE/CREATE2` opcode and the resulting `initcode_size` exceeds the maximum, then there is an exceptional abort. But, in what context does it abort? Does it fail in the CREATE frame or does it fail in the context of the contract which calls the CREATE opcode? So the quesiton here is, if there is an exceptional abort, does the 0 address get put on the stack after executing CREATE/CREATE2, or does the contract which calls CREATE/CREATE2 go OOG?

---

**k06a** (2022-03-04):

What do you think about non-charging 32k or gas when returned deployment code is empty?

---

**axic** (2022-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/k06a/48/1421_2.png) k06a:

> non-charging 32k

Assuming the reasoning here would be to use creation transactions as a “poor man’s” batched transactions?

---

**k06a** (2022-03-15):

This is also safe way to have create2 factory of proxies for delegatecalls. No need to care of proxy selfdestruction if it was not even deployed.

---

**poojaranjan** (2022-04-08):

PEEPanEIP-3860: Limit and meter initcode with [@axic](/u/axic) [@chfast](/u/chfast)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/5/58f9352155559e004f559fe55b0e303bf212e86e.jpeg)](https://www.youtube.com/watch?v=PJQdhPR5BJ0)

---

**jochem-brouwer** (2022-10-24):

Hi all, since we consider this for Shanghai and we want 3540 (EOF contracts) 3670 (EOF code validation) in it, plus this EIP, we now run into a situation where the interaction between these three EIPs are not clear.

What if:

I deploy an EOF contract which has a code section of size lower than than the max initcode, but the entire container is larger than the max intitcode?

Is the 2 gas charged on the entire container per word, or only the code section?

---

**frangio** (2022-10-31):

Running into the code size limit is a very frequent problem for smart contract developers (Solidity developers, at least), and the workarounds are often not pretty. There is hope that this limit will be lifted or at least increased in the future. Does this EIP affect the chances that that will happen?

In particular, one of the things that concern me is that the EIP mentions as a motivation that EVM engines could implement the program counter as a 16 bit sized type. This would be incompatible with code size increases beyond that. Granted, that still allows for a 2x increase of today’s limit, but not for lifting the limit. I believe I’ve seen proposals in the past to lift it (sadly can’t find them), so I’d like to hear your thoughts on those prospects.

If this is accepted and engines implement this change, it would probably still be possible to later increase the allowed size of code pointers, but it would require larger code changes as opposed to a simpler parameter change. Additionally, if there is an EVM-compatible chain/rollup that decides it can support higher code size limits and increases this parameter, it would not be able to reuse the execution engine without those code changes.

A possible alternative is to instead suggest a 32 or 24 bit type for representing code pointers, to allow for potential further increases in the future, though this can’t be more than a recommendation I guess.

---

As a second question, have you looked in the history of the chain to see if there have been transactions with init code larger than 48kB, and if so how frequently? I’m wondering if this will be a new frequent annoyance for developers.

---

**gumb0** (2022-11-28):

EIP was clarified regarding nonce update and gas deduction in case of initcode size above the limit for CREATE/CREATE2: [Update EIP-3860: Clarify nonce rules by gumb0 · Pull Request #6040 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6040)

Also tests were updated accordingly: [EIP-3860: Update tests for CREATE/CREATE2 according to spec change by gumb0 · Pull Request #1105 · ethereum/tests · GitHub](https://github.com/ethereum/tests/pull/1105)

---

**axic** (2022-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> What if:
>
>
> I deploy an EOF contract which has a code section of size lower than than the max initcode, but the entire container is larger than the max intitcode?
>
>
> Is the 2 gas charged on the entire container per word, or only the code section?

There is no special rule for EOF, i.e. the entire container is counted for the EIP-3860/EIP-170 limits. Doing otherwise could quickly become overly complicated, and the “code size limit” is actually for limiting data storage, not for limiting executable code.

---

**axic** (2022-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Running into the code size limit is a very frequent problem for smart contract developers (Solidity developers, at least), and the workarounds are often not pretty. There is hope that this limit will be lifted or at least increased in the future. Does this EIP affect the chances that that will happen?

I agree it is concerning, and we considered several times to submit a proposal to increase the limit. I don’t think this particular proposal has an effect on it, especially because we have defined it to state:

> MAX_INITCODE_SIZE 2 * MAX_CODE_SIZE
>
>
> Where MAX_CODE_SIZE is defined by EIP-170 as 24576.

This is for hoping that the initcode limit is scaled when the code limit is changed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> In particular, one of the things that concern me is that the EIP mentions as a motivation that EVM engines could implement the program counter as a 16 bit sized type. This would be incompatible with code size increases beyond that.

With the “full suite of EOF” (= function sections), each function section can be 2^16 bytes big, which in practice removes any feasible limit. This is what is considered for adoption.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> As a second question, have you looked in the history of the chain to see if there have been transactions with init code larger than 48kB, and if so how frequently?

We did some investigation back in the day, but also a back of the envelope calculation: since [EIP-2028](https://eips.ethereum.org/EIPS/eip-2028) non-zero bytes are 16 gas in calldata, i.e. 768432 gas, however deploying ~48k would cost ~9.6M gas.

The likely case where problems could arise is contracts containing a significantly heavy constructor. I wonder however if even those cases where a lot of gas is used, is it because of a lot of code, or is it because of performing calculations.

---

**marioevz** (2022-12-07):

I’m implementing tests on the python tests repository, and I’m having trouble understanding this change referenced here.

It seems like the hashing costs for `CREATE2` are charged even when the initcode exceeds the max length, which doesn’t make much sense to me since there should be no hashing performed at all.

Is this the correct behavior or should the hashing costs not be charged in this case?

I’m currently testing using latest version here: [GitHub - ewasm/go-ethereum at eip-3860](https://github.com/ewasm/go-ethereum/tree/eip-3860)

---

**chfast** (2022-12-29):

Your understanding is correct, just the tests were generated from the incorrect implementation.

The implementation is fixed now: https://github.com/ethereum/go-ethereum/pull/23847

and tests are updated: [Fix tests for EIP-3860 by gumb0 · Pull Request #1125 · ethereum/tests · GitHub](https://github.com/ethereum/tests/pull/1125)

---

**chfast** (2022-12-29):

In `CREATE` and `CREATE2` we have OOG errors (terminating the current execution context) and “light” errors (instruction returns 0 address).

#### CREATE2 pre EIP-3860:

1. Memory expansion (OOG)
2. Initcode hashing cost (OOG)
3. Call depth check (light)
4. Balance check (light)

#### CREATE2 after EIP-3860:

1. Memory expansion (OOG)
2. Initcode size limit check (light)
3. Initcode hashing cost (OOG)
4. Initcode cost (OOG)
5. Call depth check (light)
6. Balance check (light)

The 3 and 4 can be combined into single one, but 3 does not exist in `CREATE`.

The light check are sensitive to the order of checks while OOG checks can happen in any order. Somehow EIP-3860 introduced a light check in between of two OOG checks. This caused a lot confusion and bugs in implementations. To the point the official ethereum/tests still contains incorrect tests as of today.

I think this design choice was a mistake and we should change the limit check to OOG one. Interpretation: the cost of initcode above the limit is infinite.

---

**holiman** (2022-12-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> I think this design choice was a mistake and we should change the limit check to OOG one. Interpretation: the cost of initcode above the limit is infinite.

I fully agree about this. It makes the semantics and implementation a lot simpler.

---

**chfast** (2023-01-05):

This change has been accepted. Please raise concerns if you have any. [EIP-3860: Change the failure to OOG by chfast · Pull Request #6249 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6249)

