---
source: magicians
topic_id: 3208
title: Generalised Precompile for Elliptic Curve arithmetics and pairings Working Group
author: AlexeyAkhunov
date: "2019-04-26"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, precompile]
url: https://ethereum-magicians.org/t/generalised-precompile-for-elliptic-curve-arithmetics-and-pairings-working-group/3208
views: 6564
likes: 5
posts_count: 25
---

# Generalised Precompile for Elliptic Curve arithmetics and pairings Working Group

There is discussion going on here: [Precompile for general elliptic curve linear combinations](https://ethereum-magicians.org/t/precompile-for-general-elliptic-curve-linear-combinations/2581)

Recently, [@shamatar](/u/shamatar) (Alexander Vlasov) has agreed to become the leader of this Working group with the objective of researching and making reference implementation (and test generation) for this precompile (or group of precompiles). I understand that there is also work on figuring out the formula for the gas cost estimation, which is not trivial.

Please message DM him or post here if you would like to join the group, with the thought of what you can contribute and how much of your time you would like to commit.

## Replies

**shamatar** (2019-04-26):

Thank you [@AlexeyAkhunov](/u/alexeyakhunov). Here is also a link to an existing [repo](https://github.com/matter-labs/eip1829) (with a legacy name).

---

**jpitts** (2019-04-27):

[@AlexeyAkhunov](/u/alexeyakhunov), for discussions under this WG, should they fall under the category of “Ethereum 1.x”, or can I create a new category “EC Arithmetics and Pairings WG” and then tag all topics w/ “eth1x”?

I’m aiming to make topics easily searched-for on the Forum!

I can also create an entry for this and the other 1.x WGs on the wiki: https://github.com/ethereum-magicians/scrolls/wiki#rings

---

**snaketh4x0r** (2019-06-17):

hey [@AlexeyAkhunov](/u/alexeyakhunov) [@shamatar](/u/shamatar) I would like to join the group.

---

**axic** (2019-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shamatar/48/1877_2.png) shamatar:

> Here is also a link to an existing repo  (with a legacy name).

Here is an [EVMC Precompile](https://eips.ethereum.org/EIPS/eip-2003) implementation of the EIP using repo from [@shamatar](/u/shamatar): [GitHub - axic/eip1962-evmc: EIP-1962 implementation as an EVMC precompile module](https://github.com/axic/eip1962-evmc)

---

**shamatar** (2019-06-20):

Sure, can you PM me your telegram handle? Most of the discussion happens there.

---

**axic** (2019-07-05):

Since this seems to supersedes https://eips.ethereum.org/EIPS/eip-1829 and https://eips.ethereum.org/EIPS/eip-665 (is it superseding the Ed25519 verification proposal), can you mention that in a section in the EIP? If this EIP is accepted, that it should mark those two properly “superseded”, but for now just a mention of the fact would be useful.

---

**shemnon** (2019-07-16):

I am still strugging to understand why this isn’t four separate contracts?  The first argument is a 4 way switch to 4 different logic paths, with at least two interpretations of the binary input data and multiple return value meanings.

The spec claims

> One may separate interfaces for additions, multiplications and multiexponentiations and estimate gas costs differently for every operation, but it would bring confusion for users and will make it harder to use a precompile from the smart-contract.

But my experience as a software engineer says the opposite.  Cramming too much functionality into one function call differentiated only by parameter values is what is making this hard to use.  Four distinct contracts would be much better.

---

**MicahZoltu** (2019-07-20):

Can someone drop a link to the EIP that is being discussed here?  I can’t find it.

---

**shemnon** (2019-07-20):

[EIP-1962](https://eips.ethereum.org/EIPS/eip-1962) - This is the discussion-to link for that EIP and after my comment I realized this thread is meant as a more generic working group thread.

---

**shamatar** (2019-07-20):

Few notes about the ABI:

- Merging different operations under one precompile is a design decision due to the following two reasons:

Not spam the address space of precompiles
- Most of the procedures where one will want to use pairings will require one to have do few operations in G1/G2

With this in mind large part of the ABI is reusable (e.g. one can always hardcode preamble bytes for G1 ADD/G1 MUL/G1 MULTIEXP in a contract and then just use `abi.encodePacked` to attach points or scalars encoding after)
ABI is the least troublesome part of the precompile, so I’m flexible to change it if necessary. For example one can only encode parameters as multiples of 32 byte “words”, but it does not solve the problem that for some specific cases one may want to have modular multiplications of 256+ bit integers (e.g. MNT4/6 753) that requires another degree of tricks

[@shemnon](/u/shemnon) If you have proposals to improve the ABI I’d be glad to hear them, as I told, ABI is not difficult to change

---

**shemnon** (2019-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shamatar/48/1877_2.png) shamatar:

> Not spam the address space of precompiles

This is not a problem.  Were we talking about opcodes it would be more of an issue since over half of the “space” is used.  But for precompiles the available space is quite large.

You will note that the alt_bn128 calls already have one call per operation (add, mul, and pairing check).  So splitting this into four functions would match the design of precompiles already in the mainnet definitions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shamatar/48/1877_2.png) shamatar:

> Most of the procedures where one will want to use pairings will require one to have do few operations in G1/G2

And switching to a different function for each operation will help in understanding which operation is being called.

From a client implementation perspective the merged APIs also become difficult to maintain.  The gas cost definitions hinge off of the value of the first byte, and it’s not just changes in constants but changing formula.  While gas costs have taken into account the size and for EXP one value, aside from Call and Storage operations all gas costs go into one formula.

Making the functions parametric on curve type is perfectly fine, it feels like a good design.  But putting the operation as a parameter when each operation could/should be its own call is where I think the design should be changed.

---

**shamatar** (2019-07-22):

Just for correctness, it would be 7 different precompiles (3xG1 ops, 3xG2 ops, pairing).

For gas estimates - gas estimator is part of the implementation and is not exposed to the node developers with the current design cause it allows one to re-use all the ABI parsing functionality.

As I was told, there is no solid preference for one or seven separate precompile addresses. We can discuss it on the next call briefly and here I will rely on the decision of the node developers.

---

**shemnon** (2019-07-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shamatar/48/1877_2.png) shamatar:

> Just for correctness, it would be 7 different precompiles (3xG1 ops, 3xG2 ops, pairing).

Still reasonable.  And it more accurately reflects the complexity of what is being proposed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shamatar/48/1877_2.png) shamatar:

> For gas estimates - gas estimator is part of the implementation and is not exposed to the node developers with the current design cause it allows one to re-use all the ABI parsing functionality.

My main issue is that we should not assume clients are just going to use the one provided implementation.  Multiple viable independent implementations is one of the things that differentiates Ethereum from other blockchains.  Expecting that clients will use the same implementation from a single provider chips away at that quality.

The spec needs to be written and thought of from the perspective that clients may want to make a new, clean-room implementation based strictly off the specs.  So saying that it is already implemented is not a persuasive argument.  It is a bit of a counter-indication when a question about a spec detail can be met with “look at what the reference implementation does” rater than being able to reason about it from the content of the specification.  This is the core of a lot of the pushback that I’ve seen and provided on the all core devs calls.

---

**shamatar** (2019-07-22):

Sorry for confusion, my meaning of “is provided in implementation” is that it’s my responsibility to perform a gas schedule research and provide a reference implementation bundled together with functionality itself. If client developers would want to port it - no one can stop them. Gas schedule itself is still WiP, but it’s getting close at least for Rust implementations, then I need to check what is a final performance of C++ one since it’s quite far from the Rust one, for example it uses external code for arithmetic (that is great for cross-checks).

---

**gluk64** (2019-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> The spec needs to be written and thought of from the perspective that clients may want to make a new, clean-room implementation based strictly off the specs.

Absolutely agree to this! We started with the ABI spec to define the exact scope of functionality, and will now specify formally the internal details. This is a relatively easy task once the gas metering is complete: since the operations follow simple algebraic formulas, we only need to define the format of the number representations, the edge cases, and the gas metering coefficients.

The implementation in C++ took only a week, so the workload is pretty bounded. It will be great to see implementations in further languages, we will be more than happy to assist anybody who will take on the task.

---

**gluk64** (2019-07-26):

A library is implemented to conveniently call the precompile:

https://github.com/matter-labs/eip1962_lib/

The usage will be as simple as:

```
EIP1962.G1Pair[] memory pairs = EIP1962.Pair[
        EIP1962.PairG1({
            p1: EIP1962.G1Point(1, 2),
            p2: EIP1962.G1Point(1, 3)
        })
    ];
    bytes memory result = BLS12.pairingG1(pairs);
    require(result, "Wrong inputs");
```

---

**axic** (2019-07-26):

The repo seems to be broken, I think `examples/EIP1962.sol` should be in `contracts`.

Another comment: this library uses manual byte copying. Solidity has built in support for that with much better speed: `abi.encodePacked`.

---

**axic** (2019-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Since this seems to supersedes https://eips.ethereum.org/EIPS/eip-1829  and EIP-665: Add precompiled contract for Ed25519 signature verification (is it superseding the Ed25519 verification proposal), can you mention that in a section in the EIP?

Looking at today’s version of EIP1962 it doesn’t seem to support Curve25519. [@shamatar](/u/shamatar) [@gluk64](/u/gluk64) is this the case?

---

Can you post gas calculation comparing the cost with the overlapping existing bn128/bn254 ecadd/ecmul/ecpairing precompile?

I’d assume the cost for those operations would be the same here, unless the design of this precompile can accommodate for some optimisations.

---

**shemnon** (2019-07-26):

While we are updating the spec can we get real test cases?  “Test cases are the part of the implementation with a link below.” is not a sufficient set of test cases as it blurs the line between specification and implementation.  (Insert waterfall vs agile grumblings here, but waterfall is how we need to work to maintain a billion dollar network).

I would expect (possibly in another markdown document kept in the EIP repository) a table of inputs to the precompile, and a column of outputs, and a gas cost column, and possibly a column describing if this test is for any particular corner case.  It doesn’t need to be reference test level exhaustive but given the nature of this precompile would expect at least one positive test for each operation on each supported curve for that operation.

---

**shamatar** (2019-08-20):

So far, the roadblock for me to complete the implementation including gas schedule is to generate a set of MNT4/6 curves with bit width for the base field of 256, 320, 384, etc bits up to (1024-1) to measure pairing cost on those and redo G1 and G2 operations gas metering based on the latest Monte-Carlo simulation approach (first results an the description of the procedure can be found [here](https://github.com/matter-labs/eip1962/blob/master/Gas_schedule.md)).

After that for sure there will be test vectors in a form `[curve description, points, operation, expected output, encoded input, encoded output, gas cost]`. I can already derive most part of it, but gas cost will be missing.

For BN254 price - it will not be “the lowest possible”. Due to variable field modulus some precomputations are not possible and one will have to pay substantial price for those over the run time.


*(4 more replies not shown)*
