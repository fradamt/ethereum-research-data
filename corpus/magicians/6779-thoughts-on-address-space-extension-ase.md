---
source: magicians
topic_id: 6779
title: Thoughts on Address Space Extension (ASE)
author: norswap
date: "2021-08-04"
category: Working Groups > Ethereum 1.x Ring
tags: [address-space]
url: https://ethereum-magicians.org/t/thoughts-on-address-space-extension-ase/6779
views: 9510
likes: 1
posts_count: 9
---

# Thoughts on Address Space Extension (ASE)

## Context

1. Increasing address size from 20 to 32
bytes
2. ASE (Address Space Extension) with Translation
Map
3. ASE Test
Cases
4. Issues with ASE (with a translation
map)
5. Types of Resurrection Metadata in State
Expiry
6. Address Space Extension with bridge
contracts
7. Making ASE work with an Edict

I’ve thought a bit on address space extension and I wanted to clarify a few

things, propose some ideas and get some feedback.

In what follows, unless said otherwise, I’ll assume the period-aware address ASE

scheme (ASE-PWA) (defined in links 1 & 2 above, name from link 5). This is the

scheme that uses a translation map from compressed address to long adresses.

I don’t actually think this is the best scheme — I lean towards either keeping

the translation map but moving the period (aka epoch) identifier out of the address, or using

bridge contracts only. I’ll explain below.

## Multiple Contexts

As mentionned in [5](https://ethereum-magicians.org/t/types-of-resurrection-metadata-in-state-expiry/6607), the PWA-ASE scheme “creates two different EVM contexts,

legacy mode and extended mode”.

I think this is unavoidable if there is going to be any address extension at

all, and we should embrace the distinction between the two contexts to clarify

the semantics.

In particular, I propose that:

- in legacy modes, all addresses are always 20 bytes
- in extended mode, all addresses are always 32 bytes

In legacy mode, all opcodes that access addresses must be changed to consult the

translation map and access data under the long address if an entry is found. No

other change is required.

In extended mode, all addresses are 32 bytes, legacy addresses are simply

0-extended.

Extended mode can call legacy mode, in which case addresses passed to calls will

automatically be compressed. This must be done by the compiler, so we can’t

automatically compress custom calldata encodings and there is a possibility of

error there, although this only concerns new (extended mode) code. This kind of

things should be caught in testing anyway.

Should legacy mode be able to call extended mode? Some possible design choices:

1. no
2. yes, with automatic address decompression for calls
3. like 2, but only if calling a bridge contract (somewaht similar to those of 6),
which is just an extended mode contract with a special flag set to accept
such calls.

`1` might be too restrictive if we want to enable callbacks when an

extended-mode caller calls an legacy-mode contract. In `2`, it would again be

the compiler’s job to properly decompress the received 20 bytes addresses, while

it leaves 32 bytes addresses alone. Again, this is not compatible with custom

calldata encoding. `3` is just `2` but forcing the contract developer to consider the

problem and say “yes I know what I’m doing”.

## Multiple Addresses

Under the new scheme, each key pair is associated to (at least) three addresses.

These are referred as “personas” in 4.

- one 20 byte legacy (“short”) address
- one (or more?) 32 byte long address(es)
- one (or more?) 20 byte compressed address(es)

A very important thing to remember here is that transactions never identify the

sender’s address, instead the signature can be used to recover the public key.

Something to contend with is that a key pair can potentially be associated with

an infinite amount of long addresses (corresponding to different periods). I

think there was some mention of whether a key should be allowed to control

multiple addresses like that of whether it should be locked to a single period.

I haven’t seen any discussion of how that would work and what it would entail,

tell me if I’m wrong.

The major related to multiple addresses stems from the “state transition” that

occurs whenever the long address becomes active (by receiving funds, or in the

future, maybe through some account abstraction mechanism).

### Short + Long Address

(Here “short address” is not the compressed address but rather the last 20 bytes

of the long address.)

Unlike sending a transaction, receiving funds does mention the address

explicitly.

This means that we can have the following situation:

1. I generate a new key pair
2. I communicate the short address to Alice
3. Alice sends funds to the short address
4. (I can know move these funds using my private key, but I do not)
5. I communite the long address to Bob
6. Bob sends funds to the long address
7. ?? can I still move funds on the short address ??

You can’t answer “yes” to that last question if you value the security goal of

address extension. To quote Vitalik in [1](https://ethereum-magicians.org/t/increasing-address-size-from-20-to-32-bytes/5485):

> current 20 byte (160 bit) addresses only provide 80 bits of collision
> resistance, meaning that someone can spend 2^80 computing work to generate
> two pieces of contract init code (or (sender, ID) pairs, or one piece of
> contract code and one EOA private key) that have the same address. 2^80 will
> soon be within reach of sophisticated attackers; the bitcoin blockchain has
> already made more than 2^90 hashes.

> you can trust an address if either (i) it is on chain, or (ii) you personally
> created it; for example, an organization cannot safely receive funds at a
> multisig unless that multisig has already been published on-chain, because
> whoever was the last to provide their public key could have chosen their
> private key in such a way as to make the address also a valid EOA controlled
> by themselves.

The security guarantee that address extension should provide is that if you

receive a 32 byte address, you know the above scenario is not possible. If you

answer “yes” to the question above (moving funds on the short address) then it

means you can still find a collision (between the short address and a legacy

EOA).

By the way, I don’t really understand why an address being on-chain would

preclude the attack described in the quote above. What prevents someone to

create a multisig that is also an EOA, then let the multisig be used “as

intended”, only to use the EOA to siphon off the funds afterwards? Please, let

me know!

So it looks like we’re forced to lose any funds left on the short address.

In fact things are even much worse than that. Say I generate a new keypair and

intend to use the short address only. I receive funds on it. Then Bob can just

make up a long address that ends with the short address, send one wei to it, and

lock me out of my funds.

The solution is relatively simple: mandate that once an address is used as a

legacy address (i.e. marked as `LEGACY` as in [7](https://hackmd.io/@yokPKswWQlu93Y10pQBj2Q/By5FXqLkt)), it is not possible to

enter an extended address that ends with that short address into the translation

map. **A bad consequence of this** is that we can’t expire account state anymore

(we can still expire account storage).

UX-wise, users should choose in advance whether a keypair will be mapped to a

long or short address, and wallets should always show that address — never the

other address. For recovery from a BIP-39 seed phrase, the wallet must consult

the chain to determine whether the recover the short or long address.

### Compressed + Long Addresses

Peter did a great job thinking through this case in [7](https://hackmd.io/@yokPKswWQlu93Y10pQBj2Q/By5FXqLkt).

To summarize briefly, problems can occur if you communicate the compressed

address before the compressed/long pair has been entered in the translation map.

Hence Peter proposes “the edict”, a set of conditions that ensures that this

entry will have been created, and thus avoids problematic scenarios if

respected.

There are two problematic scenarios.

In the first scenario is essentially the one in Vitalik’s quote from above, but

using a compressed address. An attacker generates a collision such that

`compressed(long_address_a) == short_address_b` (imagine that for instance

`long_address_a` is a multisig). If you send funds (e.g. ERC20 tokens) to

`compressed(long_address_a)` before it has been entered to the translation map,

then the attacker can make out with the funds.

If the compressed address had been in the translation map, then we could have

rejected a transaction with a signature for the compressed address.

As Peter says on the Discord:

> There are two types of problems:
> a) You violate The Edict sending and send something to the contract that has a collision and Chuck steals your funds.
> b) You violate The Edict and you funds end up in long address land at encode(compress(long_address)) and you can’t get them back.
> I (and most other people) aren’t very worried about a), because Chuck has to spend billions of dollars to generate the collision and then cross his fingers and hope you screw up. The attack isn’t even viable unless Chuck targets the richest whales anyway.

In the second scenario (the worrisome one), you make a mistake and pass

`compressed(long_address)` to an extended-mode contract, instead of simply

`long_address`.

For Ethereum transfers, this is easily avoided. If sending before the

translation map entry is established, we can merge the balances when the entry

is created. If after, we can simply look in the translation map for the correct

address.

For other use cases, things are more complicated. For instance, sending tokens

to `compressed(long_address)` with a extended-mode ERC20 contract will cause a

mapping from that compressed address to the balance to be created, whereas

normally the balance should be mapped to `long_address` directly.

Here are some ideas of how to fix this:

1. automatic “address normalization”
2. having contracts check both long_address and compressed(long_address)
3. including a recovery function (devised by Peter in 7) in the contract

Automatic address normalization would cost gas, and would fail on custom

calldata parsing. Solution `2` would also cost gas, and relies on ERC20

implementation to actually do it. Solution `3` also relies on inclusion in

implementations, but only costs gas at contract deployment time. Including `2`

or `3` int the OpenZeppelin implementations (and maybe a few frequently forked

repos) could help a lot.

Note that this may seem similar to the short address issue. But this time there

is a good reason for being able to see the compressed address: it will show up

in transaction data (and hence on etherscan & co, which people do use to check

up on their transactions).

## ECRECOVER

Currently, the ECRECOVER precompile returns the (20-byte) address associated

with a signature (last 20 bytes of hash of the public key).

With period-aware addresses however, we can’t get the address from the public

key. We need to know the epoch (and potentially version, shard id, …).

For use in extended mode (for which there is no code written yet) we can just

change the precompile to take the epoch (& co) as parameter. Or change it to

return the public key.

The thorny problem is what to do with signatures generated by long addresses in

legacy mode.

There is only one way I can think to get this to work backward-compatibly under

PWA. And that is stuff the epoch (& co) in the signature itself (e.g. in `v`, just like

EIP-155 did for the chain ID. I don’t think `v` is limited to a certain size, so

this is certainly possible.

I don’t see any other way, but let me know otherwise.

If we decide to break ECRECOVER (bad idea imho), the question is: how much is

ECRECOVER used. How much would break if we change it?

Another concern is that we can’t “break it neatly”. Ideally, if we identify

that a signature was signed with long address public key, we would revert.

However, we cannot make this determination, because it would require compressing

the address, **including the epoch** which we do not know.

## Do we need PWA?

I don’t think so? If we’re going to have the translation map stick around

forever, I don’t think it’s a big deal to add an epoch field in there.

If the address can stay purely derived from the public key, this keeps ECRECOVER

backward compatible: We can verify that a signature was generated by a long

address by compressed it and looking in the map, in which case we can return the

compressed address in legacy mode.

Additionally we don’t have to worry about having multiple addresses with

different epochs for the same public key. Now the epoch is metadata of the

address, just like the nonce. We’re also able to change the epoch associated

with an address easily.

## Translation Map: Expirable? Size?

Can the translation map be expired? I don’t think so.

Many problem mitigations outlined above wrt compressed addresses relies being

able to tell that a public key matches a long address, or that a short address

is a compressed address. I’m not sure it’s feasible to do all that when that

information is missing.

To give you just an example, to avoid collision attacks on compressed addresses,

we must forbid transactions signed by a public key whose hash ends with an

existing compressed address.

If the translation map can’t be expired, we should worry about its size. Ipsilon

[reports](https://notes.ethereum.org/@ipsilon/address-space-extension-exploration) 150M addresses in June, and estimates 150M over two years.

Over on Discord, potus did an exponential fitting on [the address data](https://etherscan.io/chart/address) starting

July 2018 and predicts about twice more (~300M) over two years.

Ipsilon estimates ~9GB for 150M addresses.

The obvious question is whether it’s worth it in terms of state expiry (though

of course that’s not the only goal of ASE).

It might be interesting to see what the numbers would have been if address

extension had been introduced two years ago, although that might be

unrepresentative given both high growth + the big push in DeFi only happening

only a year ago.

Nevertheless the current state size is about 30-40GB. How much of that has been

inactive for more than 1 year? Two years?

## Bridge-Only

One alternative to the translation map approach is to simply forbid long

addresses to interact with legacy contracts.

Legacy contracts could be allowed to call extended contracts, but that is not

strictly required.

We need a way to bridge over between the two worlds. Those are the [bridge
contracts](https://ethereum-magicians.org/t/address-space-extension-with-bridge-contracts/6660) proposed by Alex. Bridge contracts are essentially

extended-mode contracts that can call legacy contracts, and have a legacy address.

Let’s take the example of an ERC20 token. Initially, the token is handled by a

legacy, and so a long address can’t own the token. Say we want to update to an

extended contract. A possible implementation is that the extended contract will

transfer the balance of the caller to itself in the legacy contract, then credit

the caller in the extended contract.

As far as I understand, the idea of a bridge contract is that (a) it lets an

extended-mode contract have a legacy address and (b) acts as a marker for the

developer to acknowledge that legacy-extended mode communication is tricky and

should be handled with care.

This proposal has the advantage of being much simpler.

The downside is that adoption of long addresses may be sluggish. People don’t

want to make long addresses because contracts are not compatible. Because people

don’t have long addresses, project are in no hurry to upgrade.

Only the extra cost of state resurrection is a foolproof incentive to migrate.

But in the proposed scheme this only kicks in after two years, at which point

creating new state becomes costlier because a proof of absence needs to be

provided. Two years is a long time in blockchains, so most important projects

might have updated by then, but it stays likely that in the meantime, most new

addresses will continue being legacy addresses.

## More

Something I’d like to see if we want to adopt state expiry with ASE-PWA is how

we could help long-lived contracts handle storage over many epochs (without

incurring undue proof costs when writing new state).

## Recap

This was long, so let me summarize the main points & questions:

Points:

- Let’s think of legacy mode as “addresses are always 20 bytes” and extended mode as
“addresses are always 32 bytes”.
- Avoiding an attack that locks people out of their funds requires never
expiring account state (!= account storage).
- The annoying gotcha of PWA-ASE is losing funds when accidentally interpreting
a compressed address as a long address. This can be avoided by following the
edict. Some in-code mitigations are possible.
- To make ECRECOVER work with PWA, we need to stuff the epoch in the signature.
- ECRECOVER cannot be broken neatly.
- If the translation map is non-expirable, we might as well store the epoch in
there.
- I don’t see how we possibly can exipre the translation map.
- The space requirement for the translation map is significant (10-20GB in two years).
- If we’re not in a hurry for people to adopt long addresses, the bridge method
is much simpler.

Questions:

- In PWA-ASE, should legacy contracts be able to call extended contracts, and
how?
- In PWA-ASE, how to contend with the fact that a public key could be associated
with multiple addresses with different periods?
- In the quote from Vitalik, why does the address being on-chain preclude an attack?
- How much/importantly is ECRECOVER used in practice? Will horrible things
result if it returns bogus legacy when passed a signature signed by a long address?
- How much space does PWA-ASE save using state expiry (given that the
translation map is persisted forever)?
- In state expiry, with PWA-ASE, how would long-lived contracts handle storage
over many epochs?

## Replies

**axic** (2021-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> The downside is that adoption of long addresses may be sluggish. People don’t
> want to make long addresses because contracts are not compatible. Because people
> don’t have long addresses, project are in no hurry to upgrade.
>
>
> Only the extra cost of state resurrection is a foolproof incentive to migrate.
> But in the proposed scheme this only kicks in after two years, at which point
> creating new state becomes costlier because a proof of absence needs to be
> provided. Two years is a long time in blockchains, so most important projects
> might have updated by then, but it stays likely that in the meantime, most new
> addresses will continue being legacy addresses.

Depending on what option is chosen for bridge contracts, the existence of them may be more widespread than not.  I could imagine that basically any new EOF-style (EIP-3540) contract is a “bridge contract” (i.e. is expected to understand long addresses), but it would remain possible to create EOF-style contracts under both legacy (which in effect is the bridge contract) and long addresses.

This means most contracts during those 2 years likely would be long address compatible already.

One general problem with long addresses is that we need to introduce new types in the contract ABI (what was called `address32` in the bridge writeup), which in turn means new types in Solidity and tooling, *and most importantly*, brand new (token) standards.  The creation and maturity of these standards may take quite a bit of time.

Unless we want to be stuck with the translation map forever, these long address-capable standards are needed no matter which ASE method is chosen.

Hence, the longer ramp up time with bridge contracts may actually be a blessing in disguise: it gives a longer transition period during which these problems can be figured out, without forcing a brittle scheme (=translation) in one go.

---

**norswap** (2021-08-04):

> This means most contracts during those 2 years likely would be long address compatible already.

I agree. And even in PWA-ASE, is there any reason not to make new contracts in extended space (besides marginally higher memory requirement), given that legacy addresses can interact with them?

> One general problem with long addresses is that we need to introduce new types in the contract ABI (what was called address32 in the bridge writeup), which in turn means new types in Solidity and tooling, and most importantly, brand new (token) standards. The creation and maturity of these standards may take quite a bit of time.

Doesn’t feel overwhelming to me, but it’s just a feeling. Standard-wise, isn’t this as simple as `s/address20/address32` in the existing standard?

---

**axic** (2021-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> One general problem with long addresses is that we need to introduce new types in the contract ABI (what was called address32 in the bridge writeup), which in turn means new types in Solidity and tooling, and most importantly, brand new (token) standards. The creation and maturity of these standards may take quite a bit of time.

Doesn’t feel overwhelming to me, but it’s just a feeling. Standard-wise, isn’t this as simple as `s/address20/address32` in the existing standard?

It is simple to change code, but there are already many competing token standards, each took a lot of deliberation and trying to improve various aspects of the preceding ones. Someone needs to create a new one, and likely there would be new competing ones or people seizing the opportunity to improve other aspects of existing standards.

In any case, it won’t happen overnight, and therefore any migration will happen over a period of time.  Unless deploying legacy contracts is disallowed soon, which likely would cause a lot of hassle for everyone.

---

**axic** (2021-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> This means most contracts during those 2 years likely would be long address compatible already.

I agree. And even in PWA-ASE, is there any reason not to make new contracts in extended space (besides marginally higher memory requirement), given that legacy addresses can interact with them?

The main difference with the bridge one is that one can create long address aware contracts in both namespaces.  It becomes possible for new projects to support token standards of both worlds, making the eventual transition smoother.

With the translation map the incentive to start supporting new token standards is simply not there. It kind of kicks the can down the road.

---

**illuzen** (2021-12-07):

Since full pubkey can be recovered from a signature, any EOA that has ever sent funds could be autoconverted to an address32, right? And contract addresses aren’t derived from pubkeys anyways so we could automatically convert them to address32 as well.

This makes the problem much smaller, doesn’t it? Just EOAs that have received funds but never spent them, and these could be autoconverted upon first use, effectively retiring legacy addresses completely.

I’m probably missing something important here.

---

**illuzen** (2021-12-07):

I definitely think it was a mistake to shorten addresses to 20 bytes in the first place and it would also be a mistake to make contract developers deal with this issue.

The issue of old state hashes being based on legacy addresses does seem to require a translation table… But if we swap in address32 moving forward, it seems we could slowly remove things from the translation table, since the extended->legacy translation is computable…still not sure at what layer this swap would happen…

So there’s a fork at time h, before h all addresses are legacy, after h all addresses input to the system must be extended with some internal check to match extended to legacy if necessary.

Ex: before h, Bob sends Alice 1 token, all 3 addresses are legacy. After h, Alice sends it back, sending from her equivalent extended address to Bob’s equivalent extended address, sending the tx to the extended version of the token contract address.

Can we make it so users never know any different except for the addresses got longer?

---

**norswap** (2021-12-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/illuzen/48/1408_2.png) illuzen:

> The issue of old state hashes being based on legacy addresses does seem to require a translation table… But if we swap in address32 moving forward, it seems we could slowly remove things from the translation table, since the extended->legacy translation is computable…still not sure at what layer this swap would happen…

That’s the issue right here: you need the translation to call from legacy mode to extended mode (unless you use bridges). The translation map will keep growing as long as new (long) addresses interact with old legacy mode (20 bytes) contracts.

---

**illuzen** (2021-12-09):

I guess what I’m proposing is using interactions with legacy contracts as an opportunity to upgrade them to extended mode. Is this possible?

