---
source: magicians
topic_id: 15456
title: "EIP-7503: Zero-Knowledge Wormholes - Private Proof of Burn (PPoB)"
author: keyvank
date: "2023-08-16"
category: EIPs
tags: [zkp, privacy, cryptography, burn, proof-of-burn]
url: https://ethereum-magicians.org/t/eip-7503-zero-knowledge-wormholes-private-proof-of-burn-ppob/15456
views: 8085
likes: 68
posts_count: 36
---

# EIP-7503: Zero-Knowledge Wormholes - Private Proof of Burn (PPoB)

## Abstract

While researching on privacy solutions and applications of ZKP, we discovered a technique,

by which people can burn their digital asset (E.g ETH) by sending it to an unspendable address,

and later build a ZK proof showing that some amount of tokens reside in an account that are

unspendable, without revealing the account.

The EIP proposes to add a minting functionality to Ethereum, so that people can re-mint

Ethers they have purposefully burnt. The mentioned privacy solution will bring strong levels of

***plausible deniability*** for the sender, since there is no way one can prove that the sender

has been participating in a privacy protocol. This will also make an anonymity pool that includes

all of the Ethereum accounts with zero outgoing transactions by default.

## Specification

In Elliptic-Curve based digital signatures, normally there is a secret scalar `s`, from which

a public-key is calculated (By multiplying the generator point with the scalar: `s * G`). An

Ethereum EOA-address is the keccak hash of a public-key.

Also, the funds in an Ethereum address might be spendable by a smart-contract, if the keccak hash

of the smart-contract’s parameters is equal with that address.

Therefore, an Ethereum address `A` is spendable if and only if:

1. A private-key s exists. such that A = keccak(s * G).
2. There exists a smart-contract c, such that A = keccak(c_params).

The preimage resistance property of hash functions implies that, you can’t find `x` where `keccak(x)=r`,

in case `r` is a random value. So the funds sent to a random Ethereum address `r` is unspendable, but

how can other people be sure that `r` is indeed random and not the result of calculating `s * G`?

A great source of randomness is a hash function. If the address is equal with the hash of a secret preimage

`s`, we can conclude that the address is unspendable, since there isn’t a polynomially bounded algorithm

to find `x` where `keccak(x)=h(s)`. This is only true if the second hash function is a different hash

function, and it assumes it is impossible to find `x_1` and `x_2` such that `h_1(x_1)=h_2(x_2)` in case

`h_1` and `h_2` are different hash functions.

Using the help of Zero-Knowledge proofs, we can hide the value of `s`! We just need to prove that

we know a secret value `s` where the address is `h(s)`. We can go even further. We can prove

that an Ethereum accounts exists in the state-root, which holds some amount of ETH and is unspendable.

By revealing this to the Ethereum blockchain and providing something like a nullifier

(E.g. `h(s | 123)` so that double minting of same burnt tokens are not possible), we can add a new

***minting*** functionality for ETH so that people can migrate their secretly burnt tokens to a

completely new address, without any trace on the blockchain. The target addresses can also be burn

addresses, keeping the re-minted funds in the anonymity pool.

## Rationale

Cryptocurrency mixers like TornadoCash can successfully obfuscate Ethereum transactions, but it’s

easy for the governments to ban usage of them. Anybody who has interactions with a mixer contract,

whether the sender or receiver, can get marked. However this EIP tries to minimize the privacy leakage

of the senders, by requiring zero smart-contract interactions in order to send money, so

we only use plain EOA-to-EOA transfers. In order to have a “teleportation” mechanism we divide

the set of all Secp256k1 points `E(K)` into two subsets/address-spaces:

- The spendable address-space: {p \in {0,1}^160 | \exists s : keccak(s * G)=p OR \exists c : keccak(c_params)=p }
- The unspendable address-space: {p \in {0,1}^160 | \nexists s : keccak(s * G)=p AND \nexists c : keccak(c_params)=p }

The spendable/unspendable addresses are not distinguishable, so we can exploit this fact and define

a spendability rule for the money sent to addresses that can’t be spent using regular elliptic-curve

signatures. Using the help of Zero-Knowledge proofs, we can hide the transaction trace and design

a new privacy protocol, which is what this EIP is proposing.

### Scalability Implications

In case the circuits are able to simultanously re-mint the sum of multiple burns in a single-proof,

merchants and CEXs will be able to accept their payments in burn-addresses and accumulate their funds

in a single address by storing a single proof (And a bunch of nullifiers) on the blockchain, which

significantly reduces the transaction count on the blockchain. The people who will use this EIP as a

scalability solution, will also increase the privacy guarantees of the protocol.

## Backwards Compatibility

The Ethers generated using the mint function should not have any difference with original Ethers.

People should be able to use those minted Ethers for paying the gas fees.

## Reference Implementation

A reference implementation is not ready yet, but here is a design:

- We will need to track all of the ETH transfers that are happening on the blockchain (Including those initiated by smart-contracts), and add them to a ZK-friendly Sparse-Merkle-Tree. The amount sent should also be included in the leaves.
- We will need a new transaction type responsible for minting Ethers. The initiator should provide a proof (Along with a nullifier) that proves he owns one of the leaves in the merkle-tree that has specific amount of ETHers

Alternatively, we can use the already maintained state-trie and provide merkle-patricia-trie proofs, showing

that there exists some amount of ETH in an unspendable account, and mint them.

## Security Considerations

In case of faulty implementation of this EIP, people may mint infinite amount of ETH, collapsing the price of Ethereum.

## Replies

**Mani-T** (2023-08-17):

This approach could lead to increased trust in stablecoins, as it provides a means of verifiable backing without relying on a centralized authority. This is brilliant.

---

**keyvank** (2023-08-17):

Exactly, but unfortunately, it’s a one-way cryptographic wormhole. The secondary token can never be converted back to the original token. (It’s like privately moving your asset to another universe, and there is no way back)

---

**Jamasp** (2023-09-03):

I think the applications are yet to be fully contemplated, but IMO the USDT-BUSDT example is not a good one; since the BUSDTs are not redeemable, and also can not be transferred back to USDT (so that again be redeemable), and this renders them worthless.

---

**MicahZoltu** (2023-09-11):

While I would rather see this as part of the base layer, one could create a WETH contract where withdraws required a proof of WETH burn to redeem for ETH, rather than returning the original WETH token(s).

This would be far less useful though as it is quite uncommon for people to send anything other than ETH to an otherwise empty account.  Since you need gas to do anything, ETH is always the first (and sometimes only) thing sent to a new address.

---

**JXRow** (2023-09-18):

“we can prove that some EOA-to-EOA transaction has happened in the previous blocks”

How to prove ? Using EOA’s signature ?

---

**keyvank** (2023-09-18):

Given that we have the block-hashes of the previous blocks in EVM, we can feed it as a public-input to a ZK circuit, which verifies a Merkle-Patricia-Trie proof (Of the transaction-tree), convincing us that a specific transaction has been included in a block (Without showing the TX). We can additionally check the Tx’s signature but that’s not necessarily needed, since a transaction is only included when its signature is valid.

---

**JXRow** (2023-09-19):

But how do ChainB know the previous block of ChainA, you can prove the tx is included in the block, but how to prove in ChainB that the block of ChianA exist indeed?

---

**MicahZoltu** (2023-09-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/keyvank/48/10268_2.png) keyvank:

> Given that we have the block-hashes of the previous blocks in EVM

We currently only have the last 128 blockhashes in the EVM.  There is a stagnant EIP somewhere that proposes storing all blockhashes in state, which would be necessary for this to work.  Presumably if this went through then that EIP also would go through as a dependency.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jxrow/48/11743_2.png) JXRow:

> But how do ChainB know the previous block of ChainA, you can prove the tx is included in the block, but how to prove in ChainB that the block of ChianA exist indeed?

This proposal is for within Ethereum only, not for cross-chain transfers.  You burn some ETH on Ethereum, and then later you can mint an equivalent amount of ETH on Ethereum.  The cleverness of this solution is that all accounts with ETH in them and no transactions are part of the anonymity set until the ETH moves.

---

**MicahZoltu** (2023-09-20):

One downside of this strategy is that the anonymity set shrinks over time.  If you mint at block 20,000,000, then your anonymity set is all accounts with ETH and no transactions where the ETH was transferred into the account after this change goes live and before block 20,000,000.  However, over time the set of accounts where the ETH doesn’t move will trend towards only those which were actual burns, thus your anonymity set ends up (eventually) being similar to contract layer tools like Tornado.

The one exception is ETH that is *mistakenly* sent to a wrong address (e.g., typo).  This ETH will stay in your anonymity set forever.  Unfortunately for this protocol (and fortunately for everyone else) the number people who accidentally burn their ETH by sending to a non-existent account is quite small.  Losing private keys is slightly more common, but still pretty rare and such accounts usually have transactions.

That being said, this protocol still provides some amount of plausible deniability in that you can claim that ETH you burned was either sent to a wrong address, you lost the keys, or you have the keys but are unwilling to share them.  Unlike Tornado, burning your ETH through this protocol doesn’t give away that you used the protocol at all.  Only withdrawing proves that you used the protocol in the past.

---

**keyvank** (2023-09-21):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> We currently only have the last 128 blockhashes in the EVM. There is a stagnant EIP somewhere that proposes storing all blockhashes in state, which would be necessary for this to work. Presumably if this went through then that EIP also would go through as a dependency.

If this is going to be implemented on the base layer, then I think the best option is to not rely on EVM-providen roots, and build and maintain an additional tree with a ZK-friendly hash function on Ethereum clients.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> One downside of this strategy is that the anonymity set shrinks over time. If you mint at block 20,000,000, then your anonymity set is all accounts with ETH and no transactions where the ETH was transferred into the account after this change goes live and before block 20,000,000. However, over time the set of accounts where the ETH doesn’t move will trend towards only those which were actual burns, thus your anonymity set ends up (eventually) being similar to contract layer tools like Tornado.

This is actually very convincing and sad, I thought the anonymity set would be bigger.

---

**MicahZoltu** (2023-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/keyvank/48/10268_2.png) keyvank:

> This is actually very convincing and sad, I thought the anonymity set would be bigger.

I agree it is unfortunate.  The plausible deniability is still incredibly valuable though.  You don’t get that with tools like Tornado.

---

**MicahZoltu** (2023-09-28):

The scalability idea from the slide deck presented at ACD should be added to the EIP, or perhaps a second EIP that depends on this one could “extend” it.

> A CEX can accept deposits in burn-addresses and re-mint the sum of them in a single proof.
> This way, a single nullifier will be stored on Ethereum client’s database instead of a complete TX.

Of note, this isn’t just for CEXs.  This would potentially be useful for anyone who sets up a unique recipient address for each payer including payment processors, merchants, etc.

Also worth noting: it would allow a merchant to accept payments without the payer being associated with the seller on chain.  The payers would all just send to burn addresses and the merchant would be able to simply mint all of their proceeds in one shot.  The same for allowing for anonymizing donations to political causes that one may not want to be publicly associated with (e.g., Canadian Truckers donations).

The nice thing about both of these use cases is that it creates an incentive to grow the anonymity set as receiving funds this way would be cheaper than receiving at independent addresses since you can “rollup” the consolidation transaction.

---

**runatyr1** (2023-09-30):

[@keyvank](/u/keyvank) couldn’t anonymity be increased by adding functionality to retrieve the newly mint tokens using uniform amounts and random time periods?

I’m not an expert at this but I think this could help further un-link the secretly burned eth from a new wallet that is receiving newly minted eth. e.g.

wallet A burns: 0.5 eth

wallet B burns 0.7 eth

…etc

then

new wallet A sets a retrieval schedule of 0.1 eth per mint at random times in the next  6 hours to complete retrieving the new eth in 5 transfers

new wallet B also sets a retrieval schedule of 0.1 eth per mint at random times in the next  6 hours to complete retrieving the new eth in 7 transfers

(maybe initially limit this type of anonymous transaction to be of certain amounts, like 0.01, eth 0.1 eth, 1 eth or 10 eth)

So even if the  anonymity set shrinks over time like [@MicahZoltu](/u/micahzoltu) said, it would be difficult to link certain burn to a mint because wallets doing the mints would be getting the same amounts per mint and at random times, plus the added privacy of the Private Proof of Burn when requesting the minting to start.

This could be optimized to avoid it from being too many transactions and resulting in expensive gas fees but still keeping it anonymous.

Because, otherwise, even if private proof of burn are used to anonymously mint new eth, i think the amount and timing would give away the identity. If wallet A burned 1.7598 ETH and other wallet B suddenly mints 1.7598 ETH then its easy to know that the owner is very likely the same.

---

**MicahZoltu** (2023-09-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/runatyr1/48/10608_2.png) runatyr1:

> @keyvank couldn’t anonymity be increased by adding functionality to retrieve the newly mint tokens using uniform amounts and random time periods?

A big part of having a functionally large anonymity set is proper operational security and practices for people using the protocol.  I would argue that this problem is orthogonal to the technical problem being addressed by this proposal.

On the technical side, it is necessary to have at least one of the follow:

1. Allow partial withdraws, where you deposit 5 and then withdraw 3 and later withdraw 2.
2. Have fixed note sizes, where everyone deposits/withdraws the same amount.
3. Allow internal consolidation, where you can deposit 2 and later deposit 3 and then withdraw 5.

Having both (1) and (2) is ideal IMO, and hopefully if this goes through it would include both.  From there, it is up to tooling authors to build tools that make it easy to use this underlying platform in a way that doesn’t create correlation between depositors and withdrawers.

---

**keyvank** (2023-09-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Of note, this isn’t just for CEXs. This would potentially be useful for anyone who sets up a unique recipient address for each payer including payment processors, merchants, etc.

Makes sense! I like the fact that it economically encourages more users to enter the anonymity set! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Will add to the current EIP soon.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/runatyr1/48/10608_2.png) runatyr1:

> Because, otherwise, even if private proof of burn are used to anonymously mint new eth, i think the amount and timing would give away the identity. If wallet A burned 1.7598 ETH and other wallet B suddenly mints 1.7598 ETH then its easy to know that the owner is very likely the same.

Definitely, but as [@MicahZoltu](/u/micahzoltu) mentioned, we still have plausible deniability ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) You can just claim that someone else has minted exactly 1.7598ETH to fake your identity and you have nothing to do with that transaction. Nobody can 100% prove that you are connected with that TX, nor can they prove that you are involved in any privacy protocol!

---

**jftavira** (2023-10-19):

Are you aware of that could be used for circumventing AML regulations and may lead to ETH being banned in most of the exchanges?

---

**keyvank** (2023-10-19):

It’s not that simple imo, if this was for a new/less-popular cryptocurrency, then yes, exchanges would ban it. But for a major crypto like ETH, I’m not really sure what will happen ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**jftavira** (2023-10-19):

The decision is not in the exchanges, it is in the countries and AML regulations are quite rigid: no tracking of the money (whatever the kind) no money. TornadoCash accounts have been banned, Monero is also affected because its annonymity.

---

**lovely-necromancer** (2023-11-01):

Aren’t we reaching to a point that AML becomes just something from the past? I mean they just try to control something, which is not controllable at all. They wanted to ban Bitcoin in early years and as a result, they couldn’t. Sometimes newer tech forces governments to reshape. Will they be able to stand against the biggest web3 foundation?

This all reminds me of the same historic events happened between email and post industry: They tried to regulate emails with E-COM, the program allowed users to send electronic mail to a post office branch. From there, it was printed and hand-delivered ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

**eawosika** (2024-03-27):

Hi Ethereum Magicians. I recently published a deep dive on EIP-7503: Zero-Knowledge Wormholes as part of [2077 Research](https://research.2077.xyz/)’s coverage of Ethereum Improvement Proposals (EIPs).  [Read the full article](https://research.2077.xyz/eip-7503-zero-knowledge-wormholes-for-private-ethereum-transactions) to understand how EIP-7503 enables privacy-preserving transfers on Ethereum with zero-knowledge proofs and why we need a protocol-layer privacy solution like EIP-7503 (vs. relying on privacy tools like Tornado Cash).

All feedback and comments on the article are welcome.


*(15 more replies not shown)*
