---
source: magicians
topic_id: 11772
title: EIP-5988 - Add Poseidon hash function precompile
author: abdelhamidbakhta
date: "2022-11-17"
category: EIPs > EIPs core
tags: [evm, gas, precompile]
url: https://ethereum-magicians.org/t/eip-5988-add-poseidon-hash-function-precompile/11772
views: 4829
likes: 17
posts_count: 24
---

# EIP-5988 - Add Poseidon hash function precompile

Discussion about [EIP-5988 - Add Poseidon hash function precompile](https://github.com/ethereum/EIPs/pull/5988).

This EIP introduces a new precompiled contract which implements the hash function used in the Poseidon cryptographic hashing algorithm, for the purpose of allowing interoperability between the EVM and ZK / Validity rollups, as well as introducing more flexible cryptographic hash primitives to the EVM.

## Replies

**vbuterin** (2022-11-22):

The main missing piece here seems to be the MDS matrix and the round constants. Since the precompile is intended to be arbitrary-size, we can’t just save the round constants in the precompile as we do with SHA256, RIPEMD160, etc, we have to generate them.

I see a few options:

1. Add an extra global execution context variable which stores which state sizes and round counts have been used before, and the MDS and RC values for those state sizes using some standard algorithm. When using a new (state size, round count), generate new values and charge extra gas for this.
2. Generate the values in real time.
3. Pass the values in as inputs.

### Option 1: cache constants in global context variable

(1) is in my view unlikely to pass, because it is a large increase in complexity, and it makes the precompile stateful (not a pure function), which is something that has not been done before.

### Option 2: generate constants in real time

(2) is more viable than one might think, because the constants would only need to be calculated once but would be used for calculations ~64 times.

For example, the default MDS matrix used in many implementations is `MDS[x][y] = 1/(2+x+y)`, which only requires `N` inversions (`~= 3N` field operations with Montgomery multi-inv), barely the cost of a single round. But this would require some tight coordination between the various Poseidon users, because it’s possible that some users (eg. Goldilocks field users) have very specific MDS values in mind that are well-optimized for their specific use case.

RC values are harder, because there are [width] of them per round. In existing implementations, eg. [this one](https://github.com/ingonyama-zk/poseidon-hash/blob/main/poseidon/round_constants.py), the RC values are generated with a fairly complicated pseudo random number generator. We would have to agree on an algorithm for generating RC values that is *very* efficient but also generates good values. Would something like `RC[i] = (i**3) ^ (i**5)` where `i = (round number) * width + index` and `^` is binary xor work? No idea, need to ask the cryptanalysis experts.

### Option 3: pass constants in as parameter

(3) has the challenge that there are *a lot* of constants. For the MDS matrix, it would work if we insist that the matrix must be a [Toeplitz matrix](https://en.wikipedia.org/wiki/Toeplitz_matrix), so `MDS[x][y] = D[x+y]` for some length 2n-1 `D`. For round constants, it would not work, and we would need to find easy real-time-generateable values like in the previous option.

The main benefit of allowing more arbitrary MDS values is that it would be more likely to satisfy the needs of specific teams that have specific algorithms that are highly optimized around particular prime fields. Because the round constant mixing step is relatively simpler, there is less need to optimize it, and so people would be more likely to simply accept whatever round constants we suggest as long as there is reason to believe that they are secure.

---

**elistark** (2022-11-23):

Hi! Super important initiative, thanks [@abdelhamidbakhta](/u/abdelhamidbakhta) and [@vbuterin](/u/vbuterin) for leading this.

A few comments, I’ll let David say more (and correct me where I err).

1. Definitely in support of @vbuterin’s option 2, in our Poseidon we generate the round constants using SHA2. To allow a bit of wiggle room for others, suggest to allow any of SHA2, SHA3, Keccak and Blake. And the input should probably include all the parameters of that version: p (modulus), # full rounds, # partial rounds, etc.
2. As part of our effort to include the Poseidon builtin in Cairo and StarkNet, we’ve contracted an independent expert evaluation of the security of the MDS matrices we use. David is checking efficiency compared to the MDS matrices @vbuterin mentioned. We’ll try to bring the crypto expert on board to also vet and opine on the various other constructions.
3. We’ve also contracted an independent team to work on an efficient CPU implementation of (our version of) Poseidon, will try to also loop them in to help write the precompile in a super-efficient way.
Will update on both 2, 3 once I get the relevant OKs from those teams.

Eli

---

**elistark** (2022-11-23):

Update from [@DavidLevitGurevich](/u/davidlevitgurevich) : The MDS matrix we use is

3 1 1

1 -1 1

1 1 -2

Multiplying by it requires no multiplications and only 8 additions/subtractions. According to our understanding, a single multiplication (modulo a 256 bit prime) costs ~7.5 additions, i.e., the matrix above will likely be faster to compute than anything which involves more than one multiplication and one addition.

---

**elistark** (2022-11-23):

BTW, I don’t have permissions to mention more than 2 handles in a post, because I’m new to the system. Can anyone pls grant me more permissions? [@vbuterin](/u/vbuterin) [@timbeiko](/u/timbeiko) (would add a few more names but, y’know, I’m not allowed ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) )

---

**DavidLevitGurevich** (2022-11-23):

That’s right.

Our plan for the future includes also higher dimension matrices, all of a similar form of small values on the diagonal and 1 in the other places.

The main advantage of these matrices is their CPU time, so I think they should be part of the precompile.

It’s important to mention that the independent expert advised us that these MDS matrices are secure as long as the round constants are not too small (we are fine because we use SHA256 to generate the round constants).

---

**elistark** (2022-11-23):

I’d like to address the concerns that [@CPerezz](/u/cperezz)  **[CPerezz](https://github.com/CPerezz)** raised on the **[EIP page](https://github.com/ethereum/EIPs/pull/5988)**, so will first quote him, then answer:

> I do have a couple of concerns with this EIP proposal:
>
>
> On which field is this going to be implemented? As there’s a lot of BLS and BN curves and you’ll need to have a pre-compile for each of them. Which seems unfeasible and not practical at all.
> The security parameters will change depending on the field on which you’re working with and the security of the curve, bit size etc…
> You can implement Poseidon with different Arity parameters. So basically there’s an infinite amount of permutations that can be added. And doesn’t make sense that this is enforced by a precompile as many companies or users might find the precompile worthless.

Responses:

1. Suggest a small list of common fields (up to 5 or so should cover existing use cases), and then presumably new projects will opt for one of those. A different option is that the field be a parameter, but this this is unneeded
2. Again, I’d go with a small selection of parameters that are either currently used. Notice that Poseidon, as a sponge construction, can be applied to different compression ratios
3. Right, and we’ll curate a small reasonable number.

---

**timbeiko** (2022-11-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elistark/48/7748_2.png) elistark:

> Definitely in support of @vbuterin’s option 2, in our Poseidon we generate the round constants using SHA2. To allow a bit of wiggle room for others, suggest to allow any of SHA2, SHA3, Keccak and Blake. And the input should probably include all the parameters of that version: p (modulus), # full rounds, # partial rounds, etc.

Can’t help here, sorry! [@jpitts](/u/jpitts) should be able to, though!

---

**vbuterin** (2022-11-24):

Hmm, it does feel inelegant to make the Poseidon precompile dependent on other hash functions for round constant generation. It would basically mean that a Poseidon precompile call requires calling those other hash functions, which are expensive in SNARKs, and so it would require the precompile to have a high cost in the EVM, and possibly have a complicated caching mechanic to only charge that cost once.

Do you have any thoughts [@elistark](/u/elistark) [@abdelhamidbakhta](/u/abdelhamidbakhta) on the possibility of using some simpler formula to generate round constants (like some bitwise thing as I mentioned)? Are there deep security concerns there that push strongly for round constants being fully “random”?

---

**elistark** (2022-11-25):

I don’t see the problem here: E.g., in a recursive STARK setting in all but the top (Ethereum) layer we bake the round constants into the program/builtin. That’s already done, so no need to prove SHA2/3 using the STARK. On the top layer, i.e., on Ethereum, it should be part of the pricing of using the precompile:  3 gas * number of invocations of SHA2/3/Keccak (replace 3 by the correct gas cost of those hashes).

Notice that most often you’ll have many invocations of Poseidon in a call to this precompile, so the amortized gas of computing the constants once is negligible. E.g., verifying a STARK takes ~ 2000 hash calls, but the number of round constants is ~ 100 - [@DavidLevitGurevich](/u/davidlevitgurevich) will know the exact number.

I’m not an expert on precompiles, but can’t a precompile generate constants to be stored in local memory and used by all calls to it inside a single transaction?

---

**dror** (2022-11-25):

Why not use parameter set in a contract code? cost should be equivalent to EXTCODECOPY (2600/100 for warm/cold access)

it does require eip4758 (deactivate selfdestruct)

---

**DavidLevitGurevich** (2022-11-27):

I am not an expert on precompiles either, but would it be possible to set a low price for industry common configurations? while the general case can be priced higher.

[@elistark](/u/elistark) your numbers are correct

---

**LeoPerrin** (2022-11-28):

Hello everyone,

Léo Perrin here, I am a symmetric cryptographer and I had a look at several arithmetization-oriented hash functions. The need to support a vast number of distinct sets of parameters for a primitive is something that is completely new in this field, and which we are only started to learn how to handle from a security standpoint. Until now, when doing cryptanalysis, we look at a single (or a few) well specified primitive, say the three AESs (128, 192 and 256). Here, there is a lot more variety for any given primitive (field size, number of inputs), and this of course impacts the security analysis. For example, it is well known that *some* choices of the MDS matrix can lead to significant security issues with Poseidon [1,2]. However, the matrix suggested above is, as far as I can tell, completely safe, provided that the round constants are chosen pseudo randomly.

This brings me to another point: it is in my opinion crucial that the MDS matrix and the round constants be provided as a “bundle”, i.e. implementers must *not* have the freedom to combine an MDS matrix from some set with round constants from another set. While not published yet, some colleagues and I found that some specific patterns in the combination of an MDS matrix and some round constants could be a security problem for some arithmetization-oriented permutation (not Poseidon at this stage, but still). It is nothing to worry about in practice provided that, again, matrix and constants are not allowed to be picked independently.

Feel free to ask any question you may have regarding the symmetric crypto aspects, with one obvious caveat: while I know the state-of-the-art in this area pretty well, it is a brand new area where there has been too little work on cryptanalysis in my opinion. Thus, much remains to be investigated!

[1] Out of Oddity – New Cryptanalytic Techniques Against Symmetric Primitives Optimized for Integrity Proof Systems. Beyne et al. CRYPTO’20 (also available on eprint).

[2] Mind the Middle Layer: The HADES Design Strategy Revisited. Keller and Rosemarin. EUROCRYPT’21 (also available on eprint).

---

**CPerezz** (2022-12-01):

Hey thanks for the reply!!

My concern is that the small selection of parameters in the three different points, ends up with a pretty big permutation of implementations that we need to support/implement.

I’ve even seen implementations that use a custom `x^13` S-Box and addition chains to optimize the in and out of circuit implementations at the same time. So I think will be hard to decide which are included and which excluded as it might not be fair for some projects.

Also, **and this is probably my biggest concern** is that this pre-compile would make the ZKEVM super SUPER tricky to implement. As this pre-compile for Poseidon would need to support BigInteger arithmetic in all the fields that are supported and conditionally select them. Not only that but supporting all the permutations might be directly unfeasible. I haven’t thought about it deeply TBH. But it doesn’t look promising…

And as one of the main contributors to the PSE/zkevm this is a real concern IMVHO for the project. And mainly for any other ZKEVM project that pretends to support the 100% of the EVM.

On a final note, I’d say this EIP arrives a bit late IMO. We’re at a stage where lookups are getting cheaper and cheaper. Things like [Baloo](https://eprint.iacr.org/2022/1565) or [Caulk+](https://eprint.iacr.org/2022/957.pdf) will probably enable to have reasonable fast implementations for common hashing algorithms so that we don’t need Poseidon as a precompile.

If this could have arrived some years ago, and we could have taken a concrete setup as the reference.

---

**elistark** (2022-12-01):

What’s your suggestion?

---

**elistark** (2022-12-01):

Regarding lookup tables: for STARKs, Poseidon costs ~ 200 trace cells (field elements). Pedersen costs ~ 10x more (2K trace cells) and “fast cpu hashes” like SHA2/3/Blake are 10x or more worse than Pedersen (20K-100K trace cells).

Are you claiming that with lookups you can prove a SHA2/3/Blake hash using ~200 constraints?

---

**CPerezz** (2022-12-01):

No, not claiming that. I do agree that actually it’s impossible to beat Poseidon (Indeed I know in PolygonHermez they can perform a Poseidon permutation in under 60 constraints IIRC). What I’m saying is that with PIOPs w/ lookups proving fast-cpu hashing algorithms are slowly starting to reduce this enormous performance gap.

And my intuition is that this will continue until we arrive to a point where hashing in circuits is no longer the most expensive thing. And therefore, we will have a precompile that will loose much of it’s purpose.

And to be clear, I’m not saying I have a suggestion on how to include Poseidon as a precompile. Indeed, I think that this arrives really late. And by the time is added, will no longer be that relevant IMO.

And if it was something less configurable, I’d probably haven’t even said anything in the discussion.

But:

1. Is unacceptably expensive to generate the constants at runtime. Same happens for caching them. Unless we just implement 1 or 2 curves and 1 or 2 Poseidon configs.
2. If we reduce the possibilities to a small, really small subset, which ARITY will we support? As that will be really unfair for some projects and really advantageous for others.
3. After seeing how painful it’s being now to deal with keccak in the ECDSA for example or in general in the storage. I don’t think adding another hash function to the Ethereum core is the way to go. As what now can be useful for maybe a year or two (as this is not landing soon anyway), can be a pain in the longer term.

I think it’s important to consider how challenging and tedious would be implementing all this inside a circuit. Which is what we will need to do at PSE if we want to do a proof of validity of the entire chain some day. Because a proof of validity will force us to implement everything as is in the EVM. So while zkevm projects can simply ignore the precompile on their L2’s, we can’t.

I’m sorry if I’m not being constructive Eli. But my opinion on this EIP isn’t really good TBH. Anyway, **not here to block the discussions if you want to move it forward nor trying to prevent this from being actually implemented and merged**. Just wanted to reply you and express why this is concerning in many aspects from my perspective that some projects might not be considering.

***On a sidenote***

Also, for what lookups and the future of proving systems refers, you might be interested on [this zkresear.ch thread from Barry on lookup singularity](https://zkresear.ch/t/lookup-singularity/65). This might help to clarify what I was saying about fast-cpu hash functions.

---

**mimoo** (2022-12-02):

Late to the game! But I was asked to chime in.

We use Poseidon and the Pasta curves in Mina (btw is there a similar EIP for supporting the pasta curves in the EVM?) and we already are running in production with our own parameters (yeah I know, another Poseidon variant ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12)) meaning that we can’t easily change them. I have some more information on the configuration we use here: [proof-systems/poseidon.md at ebe59f35f5cb6bb33fc0ed3c4cb5040d8cd81247 · o1-labs/proof-systems · GitHub](https://github.com/o1-labs/proof-systems/blob/ebe59f35f5cb6bb33fc0ed3c4cb5040d8cd81247/book/src/specs/poseidon.md) if that’s of interest.

My 2 cents would be: support different bundles the same way we can support different configurations for ECDSA or for SHA-2 (SHA-2-256, SHA-2-512, etc.) Perhaps the parameters used should be dictated by an argument to a poseidon function. This way it would force standardization of at least a small number of Poseidon implementations.

---

**CPerezz** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mimoo/48/7957_2.png) mimoo:

> (btw is there a similar EIP for supporting the pasta curves in the EVM?)

I think I saw something in the ethresear.ch forum. It was about forgetting about BLS precompiles and implement pasta curves directly. See: [Do not add bls12 precompile, implement Pasta curves w/o trusted setup instead - Cryptography - Ethereum Research](https://ethresear.ch/t/do-not-add-bls12-precompile-implement-pasta-curves-w-o-trusted-setup-instead/12808)

Not sure how did it evolve. Hope it helps!

---

**xzhang** (2022-12-06):

This might be a bit off-topic but I remember StarkWare did a review of zk-friendly hash functions. What are your thoughts on using the Rescue/Rescue Prime hash? [@elistark](/u/elistark)

---

**naure** (2023-02-02):

There is an important parameter missing: **the initial capacity**.

There are multiple modes of operations that set different initial states. As an example, it can be used to hold the message length in bytes. Below are some suggestions from the paper. There is also a generalization of this called [SAFE](https://hackmd.io/bHgsH6mMStCVibM_wYvb2w).

[![image](https://ethereum-magicians.org/uploads/default/original/2X/7/7d0a37e510ada5e52cf0bee4089779cb3c71041d.png)image457×455 74.4 KB](https://ethereum-magicians.org/uploads/default/7d0a37e510ada5e52cf0bee4089779cb3c71041d)

Concretely, there should be at least:

- A parameter initial_capacity, of length t - rate.
- A parameter rate (unless we force it to t - 1).
- The parameter input_rate as currently written is a misnomer, the description sounds like it is chunk_count, that is the number of absorb steps.

Alternatively, do away with the notion of input rate. Instead accept inputs of size `t` to be added to the state between each permutation. Also return the entire final state. The caller can implement all modes of operations with this.

The algorithm of the precompile is as follows (with example `t=3`):

```auto
inputs = [ [1, 2, 3], [0, 4, 5], …]    # Matrix of shape (chunk_count, t)

state = [0, 0, 0]                      # Zero vector of length t

for chunk in inputs:
    state += chunk                     # Vector add
    permute(state)

return state
```

The caller to hash a sequence of elements uses the following input, including a particular choice of initial capacity:

```auto
inputs = [
    [ initial_cap, input1, input2 ],
    [ 0,           input3, input4 ],
    [ 0,           input5, input6 ],
    …
]

final_state = poseidon_hash(inputs)
digest = final_state[0]
```

This design gives the flexibility to the caller to implement any mode of operation around the permutation.


*(3 more replies not shown)*
