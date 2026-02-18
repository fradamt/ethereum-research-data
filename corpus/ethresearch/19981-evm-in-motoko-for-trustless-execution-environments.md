---
source: ethresearch
topic_id: 19981
title: EVM in Motoko for Trustless Execution Environments
author: skilesare
date: "2024-07-05"
category: EVM
tags: []
url: https://ethresear.ch/t/evm-in-motoko-for-trustless-execution-environments/19981
views: 2114
likes: 0
posts_count: 4
---

# EVM in Motoko for Trustless Execution Environments

Hello ethResearch ![:waving_hand:](https://ethresear.ch/images/emoji/facebook_messenger/waving_hand.png?v=14) it has been a while since I posted. Thanks for your patience as I wade back into the eth universe.

An organization that I’m running called https://icdevs.org is funding an evm built in Motoko that is targeted to run on the Internet Computer(and that we think will slide well into the AO universe as well). We should have started this 3 years ago, but there is no time like the present. To date this work has been funded through #GG19 and #GG20. The eventuality of this project is trustless execution and consensus agents and the ability to monitor and relay messages between EVMs(and other chains) in a trustless manner.

The bounty has reached its first milestone and we’re looking for experienced EVM implementors to tell us what we’ve missed and how to make it better. I realize this forum seems to have moved on to bigger and harder scaling challenges, but I’m hoping you all can point me in the right direction to find the right audience. It is a bit too technical for r/ethereum but may be too basic for this forum and not quite an EIP.

Why we are looking to build out an EVM execution layer for the Intenet computer(from our thread at [Closed - ICDevs.org Bounty #63 - EVM OpCodes - Motoko - 1.9 ckETH - Bounties & RFPs - Internet Computer Developer Forum](https://forum.dfinity.org/t/open-icdevs-org-bounty-63-evm-opcodes-motoko-1-9-cketh/27592?u=skilesare) )

1. The obvious - we can’t build an EVM in motoko without the op-codes. Now building an evm in motoko isn’t particularly a priority at the moment, but long term the Ethereum Foundation has made it a priority to have EVMs in as many languages as possible as a security feature. Would it make sense to have IC canisters as evm nodes for other chains? Probably depends on network config and a few other things, but I could certainly see it being of value long term. Having the op-codes defined separates the execution concerns from any future project that might want to wire up the rest of the EVM machinery. From building from the ground up you get an EVM that takes the IC’s compute pattern and restrictions into account in ways that existing EVMs written in other languages would need significant rewrites to support.
2. General education - These opcodes are an awesome way to learn about stacks, memories, and crypto primitives. Education is the primary goal of ICDevs.org  and we feel like Motoko versions of these libraries would make a really interesting set of examples for people learning about how EVMs work, why they work, and what concepts mirror over into the IC(and which ones don’t).
3. Libraries and Integrations - these libraries build on top of a number of other Bounties that we’ve funded that could use some burn-in and integration testing to improve them and make sure they are working properly. GitHub - f0i/merkle-patricia-trie.mo: A Merkle Patricia Trie implementation in Motoko  GitHub - relaxed04/rlp-motoko: RLP implementation on motoko. In addition, some of the op codes implement core functionality that we’ll need to do cross-chain like ecrecover which would be important for a motoko canister trying to verify a signature from the evm universe.
4. Micro EVMs - In one universe bitfinity EVMs proliferate and we end up with a garden of highly specialized evms on the IC that interact and interoperate in unique ways. These libraries would allow you to pull in the memory, storage, etc from those EVMs and run transaction simulations to check for opportunities or to automate actions against them using things like the event logs. The always-on nature of IC canisters makes them ideal for writing bots/agents that seek opportunities and execute on them by signing tecdsa messages and relaying them.

Our bounty hunter has completed the first milestone, arithmetic functions.

project file:



      [github.com](https://github.com/icdevsorg/evm.mo)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/e/2/e2f71ef3abfbeafde4920333bbfae654c2dc7917_2_690x344.png)



###



EVM Based Libraries for Motoko










main code file:



      [github.com/icdevsorg/evm.mo](https://github.com/icdevsorg/evm.mo/blob/5b3870c2454caf5cb1506010c8ab6796214ff307/src/evm_mo_backend/main.mo)





####

  [5b3870c24](https://github.com/icdevsorg/evm.mo/blob/5b3870c2454caf5cb1506010c8ab6796214ff307/src/evm_mo_backend/main.mo)



```mo
import Array "mo:base/Array";
import Nat "mo:base/Nat";
import Nat8 "mo:base/Nat8";
import Nat64 "mo:base/Nat64";
import Int "mo:base/Int";
import Trie "mo:base/Trie";
import Iter "mo:base/Iter";
import Debug "mo:base/Debug";
import Vec "mo:vector"; // see https://github.com/research-ag/vector
import Map "mo:map/Map"; // see https://mops.one/map
import EVMStack "evmStack";
import T "types";

module {

  type Result = { #ok: Ok; #err: Err};
  type Engine = [(T.ExecutionContext, T.ExecutionVariables) -> Result];
  type Vec = Vec.Vector;
  type Map = Map.Map;
  type Trie = Trie.Trie;
```

  This file has been truncated. [show original](https://github.com/icdevsorg/evm.mo/blob/5b3870c2454caf5cb1506010c8ab6796214ff307/src/evm_mo_backend/main.mo)










tests:



      [github.com/icdevsorg/evm.mo](https://github.com/icdevsorg/evm.mo/blob/5b3870c2454caf5cb1506010c8ab6796214ff307/test/main.test.mo)





####

  [5b3870c24](https://github.com/icdevsorg/evm.mo/blob/5b3870c2454caf5cb1506010c8ab6796214ff307/test/main.test.mo)



```mo
import { test; skip } "mo:test/async"; // see https://mops.one/test

import { stateTransition } "../src/evm_mo_backend/main";

import Array "mo:base/Array";
import Nat "mo:base/Nat";
import Nat8 "mo:base/Nat8";
import Nat64 "mo:base/Nat64";
import Int "mo:base/Int";
import Trie "mo:base/Trie";
import Debug "mo:base/Debug";
import Vec "mo:vector";
import Map "mo:map/Map";
import EVMStack "../src/evm_mo_backend/evmStack";
import T "../src/evm_mo_backend/types";

let dummyTransaction: T.Transaction = {
    caller = "\00\aa\00\aa\00\aa\00\aa\00\aa\00\aa\00\aa\00\aa\00\aa\00\aa";
    nonce = 2;
    gasPriceTx = 5;
```

  This file has been truncated. [show original](https://github.com/icdevsorg/evm.mo/blob/5b3870c2454caf5cb1506010c8ab6796214ff307/test/main.test.mo)

## Replies

**skilesare** (2025-01-21):

We are getting closer and closer to being “done”. We have two more precompiles that are giving us a bit of trouble.

Project:



      [github.com](https://github.com/icdevsorg/evm.mo)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/e/2/e2f71ef3abfbeafde4920333bbfae654c2dc7917_2_690x344.png)



###



EVM Based Libraries for Motoko










Blake:



      [github.com/icdevsorg/evm.mo](https://github.com/icdevsorg/evm.mo/blob/a6f07fad333d730bd2134aa3d1a677aacae51831/src/evm_mo_backend/blake2.mo)





####

  [a6f07fad3](https://github.com/icdevsorg/evm.mo/blob/a6f07fad333d730bd2134aa3d1a677aacae51831/src/evm_mo_backend/blake2.mo)



```mo
// Modified from https://github.com/keep-network/blake2b/blob/master/compression/f.go
// See https://github.com/keep-network/blake2b/blob/master/LICENSE for licence and conditions

import Nat64 "mo:base/Nat64";
import Iter "mo:base/Iter";
import Debug "mo:base/Debug";

module{

    // F is a compression function for BLAKE2b. It takes as an argument the state
    // vector `h`, message block vector `m`, offset counter `t`, final
    // block indicator flag `f`, and number of rounds `rounds`. The state vector
    // provided as the first parameter is modified by the function.
    public func F(rounds: Nat, h: [Nat64], m: [Nat64], t: [Nat64], f: Nat8) : [Nat64] {

        // IV is an initialization vector for BLAKE2b
        let IV: [Nat64] = [
            0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
            0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
        ];
```

  This file has been truncated. [show original](https://github.com/icdevsorg/evm.mo/blob/a6f07fad333d730bd2134aa3d1a677aacae51831/src/evm_mo_backend/blake2.mo)










ecPairing:



      [github.com/icdevsorg/evm.mo](https://github.com/icdevsorg/evm.mo/blob/a6f07fad333d730bd2134aa3d1a677aacae51831/src/evm_mo_backend/precompiles.mo#L502)





####

  [a6f07fad3](https://github.com/icdevsorg/evm.mo/blob/a6f07fad333d730bd2134aa3d1a677aacae51831/src/evm_mo_backend/precompiles.mo#L502)



```mo


1. resultBuffer.add(Nat8.fromNat((x % (256 ** Int.abs(i+1))) / (256 ** Int.abs(i))));
2. };
3. for (i in Iter.revRange(31, 0)) {
4. resultBuffer.add(Nat8.fromNat((y % (256 ** Int.abs(i+1))) / (256 ** Int.abs(i))));
5. };
6. let result = Blob.fromArray(Buffer.toArray(resultBuffer));
7. exVar.returnData := Option.make(result);
8. exVar
9. };
10.
11. let pc_08_ecPairing = func (exCon: T.ExecutionContext, exVar: T.ExecutionVariables, engineInstance: T.Engine) : T.ExecutionVariables {
12. // Get input data from calldata
13. let inputArray = Blob.toArray(exCon.calldata);
14. let inputLength = inputArray.size();
15. if (inputLength % 192 != 0) {
16. return ecPairingError(exCon, exVar);
17. };
18. // Calculate gas
19. let dynamic_gas = (inputLength / 192) * 34000;
20. let newGas: Int = exVar.totalGas - 45000 - dynamic_gas;
21. if (newGas  Debugging is taking a little longer than I’d hoped. I’ve modified the test output so that it shows exactly where I’m up to with all of this even if the tests don’t pass. I now only have the last 2 precompiles (ecPairing and blake2f) left to debug. I’m just hoping I haven’t created a needle-in-a-haystack situation here!

> With ecPairing and its related module I modified this from Python code (the source is linked in comments), or rather I got ChatGPT to translate it into Motoko and then went through and corrected ChatGPT’s mistakes. I’ve verified that the test values are indeed correct and that the evm.codes Playground example from which I took them works in Remix. I’ve now started sifting through the code to make sure that the Motoko code matches the Python logic at every point. I’ll come back to it on Friday but I’ll see if I can figure out a more systematic way to do it.

---

**skilesare** (2025-01-28):

Update: We have now reached the Shanghai upgrade in OpCodes.  I hope to get things up to Paris with the Cancun-Deneb opcodes asap, but hopefully, we have a functioning execution pipeline here soon enough that works with real world contracts.

---

**skilesare** (2025-04-09):

I could certainly use some advice from folks who’ve gone before me and raised funds to build out core infrastructure.  We’ve done a few rounds of Gitcoin Grants and just never had much success.  We have one going right now, but as this is a research forum, I’ll avoid posting it directly. I’m sure you can find it if you’d like.  I’m just not sure how to reach the right people.  Those in our little IC corner of the world just don’t want to bridge eth to arbitrum and have been absolutely battered by the market over the last 4 years and thus giving is not at the top of their agenda.

Are there any grants for this kind of thing in places I’m not looking?  We tried for a grant from the Ethereum Foundation and it was just denied with a stock email stating that the application didn’t meet the mission of ethereum despite the fact that I thought having multiple clients was part of the mission of ethereum. We’ve done a good bit of work, and I don’t want it to get lost in the shuffle, but ultimately, we have to fund it somehow.  Feel free to DM me if you have any advice.

