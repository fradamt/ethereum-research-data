---
source: magicians
topic_id: 4187
title: EIP-2537 (BLS12 precompile) discussion thread
author: shamatar
date: "2020-04-07"
category: EIPs > EIPs core
tags: [core-eips, precompile, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187
views: 42555
likes: 94
posts_count: 90
---

# EIP-2537 (BLS12 precompile) discussion thread

Reference thread from the EIP itself.

Resources:

- spec until it’s accepted from PR
- test vectors

## Replies

**shemnon** (2020-04-11):

Doing a testing pass:

- First, can you provide a test vector for pairings where in the pairing contract “Any of G1 or G2 points are not in the correct subgroup” is triggered?  All the test vectors are happy path.  Not on G1 or G2 is trivial to produce, subgroup is a bit more involved.  This will be needed for reference tests.
- Second, does the padded space need to be zeros only?  i.e. is ff00000000000000000000000000000012196c5a43d69224d8713389285f26b98f86ee910ab3dd668e413738282003cc5b7357af9a7af54bb713d62255e80f560000000000000000000000000000000006ba8102bfbeea4416b710c73e8cce3032c31c6269c44906f8ac4f7874ce99fb17559992486528963884ce429a992fee a valid G1 point for the contract? (the first set of zeros has junk data in it)

---

**holiman** (2020-06-22):

Just saw that the EIP now has a section about " Prevention of DDoS on error handling" . Can someone explain what distributed denial of service attack can be carried out if we blow all gas on a subroutine error (like we do on all other types of errors, always?)

---

**shamatar** (2020-06-23):

Hello Martin.

EIP text actually will be updated because now (in latest commit in master) it reflects a “desired” behavior for calls to the precompile (only nominal cost is burned), but such desired behavior will not be implemented.

In any case, there is no DDoS vector if precompile burns all the gas of the current frame (what was sent along with a staticcall) and supplied gas is more than a gas cost from the schedule.

---

**shamatar** (2020-06-23):

Negative vectors are also available in 1962 repo (in “negative” folder), there are cases with invalid subgroup there.

Padding with zeroes should be enforced with ABI because field element is required to be “in the field”, so it must be strictly less than modulus, and if leading bytes are non-zero (and we use BE encoding) the element will be not “in a field”.

---

**jochem-brouwer** (2020-07-01):

Hey, we are implementing the multiExp precompiles at EthereumJS. The gas used is not very clear to me.

In the pairing precompile it is clear that if the input length is 0, or the length of the input is not of an expected length, then we use the base gas. However, what should this be if I input an empty byte to multiExp? 0 gas (this is what Geth does)? What if I input 1 byte (i.e. the length is not a multiple of 160 bytes). Should I also use 0 gas here? What if I input 161 bytes? Should I deduct the “corresponding gas” (1 pair) or also 0 gas? Geth seems to floor the division of the input (i.e. `floor(len(input)/160)`), calculate the gas, and then deduct this if the `len(input) % 160 != 0`. (To be clear: in this case thus more than 0 gas is deducted)

---

**shamatar** (2020-07-05):

Hello [@jochem-brouwer](/u/jochem-brouwer)

A PR with the clarification and explicit formulas for variable length cases is pending the bot approval at the moment, but you can still access the document [here](https://github.com/ethereum/EIPs/pull/2693).

Sincerely, Alexander

---

**jochem-brouwer** (2020-07-09):

Thanks Alexander for the update!

I have a question about the encoding of Fp points. Sorry for my ignorance about this. Is the only check necessary for a Fp point to be on the curve that it is strictly less than the base field modulus? (I.e. `< 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab`).

Does the same apply for Fp2 points (`c0` is less than the base field modulus)? Is there any requirement for the `c1` point of Fp2?

Kind regards,

Jochem

---

**shamatar** (2020-07-09):

Field elements (either Fp or Fp2) in pairs for the affine coordinates (x, y) of the curve point. They must satisfy the equation like `y^2 = x^3 + b` for the BLS12-381 curve (`b` coefficient can be found in the EIP itself). Then point is “on curve” and this check is always performed during deserialization. `c0` and `c1` elements of Fp2 element are just Fp elements, so all corresponding encoding rules apply.

---

**jochem-brouwer** (2020-07-15):

The input to the `mapToG1` precompile takes 64 bytes (top 16 bytes are zero). This is a single number. I don’t see how I can then check if they satisfy that equation? Shouldn’t this strictly less check as mentioned before be the sole check?

---

**shamatar** (2020-07-16):

`mapToG1` takes as an input a single Fp element (not a curve point) and outputs a valid curve point. So the only check here is that input element must be “in the field” (properly encoded).

---

**jochem-brouwer** (2020-07-28):

Hey [@shamatar](/u/shamatar), I just had a discussion with [@MariusVanDerWijden](/u/mariusvanderwijden) on discord about [this particular test](https://github.com/matter-labs/eip1962/blob/master/src/test/test_vectors/eip2537/extras/g2_multiexp.csv).

Geth currently outputs a zero point of this multiexp call. However, to me it seems that per the EIP, these zero points are “not on curve” and thus should throw an error instead of returning the zero point (infinity point (?)) as output. See the pic below from the EIP which is the part which confuses me. Should thus the precompile yield an output and thus make the call succeed (current implementation) or should it throw? I think by the EIP it should throw?

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/2/298deac61a817cedf23abc566da753098e1a3311_2_690x115.png)image789×132 15.5 KB](https://ethereum-magicians.org/uploads/default/298deac61a817cedf23abc566da753098e1a3311)

---

**shamatar** (2020-07-28):

Hey [@jochem-brouwer](/u/jochem-brouwer)

Well, it’s only a wording problem, that’s why I’ve called it “convention”. On BLS12-381 point of infinity is “virtual”, in a sense that there is no point `O` with some coordinates `(x,y)` that is on curve and that for any point `P` one has `P + O = P`. Do achieve necessary functionality nevertheless this EIP follows the BN254 one where “point of infinity” is encoded as `(0,0)` for both input and output purposes (it’s not that hardly needed for inputs cause it can be filtered out in Solidity if really necessary, but valid outputs can be points of infinity).

---

**jannikluhn** (2020-10-27):

Both this EIP and the existing BN254 precompile only allow performing pairing checks, not evaluations (get the result `C = e(A, B)` for further processing). What’s the reason for this?

---

**shamatar** (2020-10-27):

It’s kind of no point to output Gt (Fp12) element in plain text we also don’t give the Fp12 arithmetic operations. But such addition would make this (already quite large) proposal really enormous.

---

**poojaranjan** (2021-01-20):

EIP-2537 explained in five slides by Alex Vlasov - https://youtu.be/al4YpfDVmS4

---

**wbl** (2022-01-06):

I’m interested in seeing this proposal move forward, and I’m rather new to the community. Right now it is listed as stagnant despite being implemented in go-ethereum.

---

**ralexstokes** (2022-01-06):

me (and many others) are also interested in BLS precompiles in the EVM!

we made a lot of good progress but there was some hesitation around this EIP as it adds a lot of very complex functionality to the EVM (in the form of BLS arithmetic) and it wasn’t super clear at the time it delivered enough value to justify going into a crowded upgrade schedule.

so activity around it has slowed and we are in a bit of limbo as development resources at the moment are nearly exclusively focused on the merge.

this EIP could conceivably go into the upcoming execution layer upgrade Shanghai but this will likely be the second half of 2022 at the earliest. this being said it facilitates a lot of use cases around scaling rollups with sharding so should become very important very quickly once we deploy the merge.

it is on my personal bucket list to track post-merge so hopefully we see BLS precompiles sometime soon ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

edit: may see some progress here: [Proposal to add EIP-2537 (BLS Precompile) to Shanghai · Issue #343 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/343)

---

**kladkogex** (2022-01-17):

We have been waiting for this for sooo long … It is amazing it is taking so much time.

---

**ralexstokes** (2022-01-18):

patience is rewarded ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

---

**PeterCCLiu** (2022-05-25):

**Quick update in May 2022:**

**Summary:** The implementation of EIP-2537 has been completed and is now in go-ethereum codebase— it is only pending activation of this functionality.

**Next steps:** Enable the precompiles by editing /core/vm/contracts.go, similar to what is done for Byzantine/Istanbul/Berlin:

1. Create a new default set of pre-compiled Ethereum contracts used in the next release, including the new precompiles of EIP-2537.
2. Modify init() and ActivePrecompiles() functions to activate the new precompiles.

**Other points to mention:** There exist another implementation that is marginally more performant regards to gas consumption and running time (blst utilizing wasm). But the workload to move on to the other implementation is high and discarding the past hard work is unworthy.


*(69 more replies not shown)*
