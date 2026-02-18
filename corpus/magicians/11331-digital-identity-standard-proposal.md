---
source: magicians
topic_id: 11331
title: Digital identity Standard proposal
author: peersky
date: "2022-10-16"
category: EIPs
tags: [identity, soul]
url: https://ethereum-magicians.org/t/digital-identity-standard-proposal/11331
views: 895
likes: 2
posts_count: 5
---

# Digital identity Standard proposal

Hey magician fellows!

This topic is a place to discuss improvement proposal I’m working on:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5787)














####


      `master` ← `peersky:digital-identity-standard`




          opened 10:00AM - 16 Oct 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8765a90a3657d8cfe9be0466ecc6cf8dc827d4f2.jpeg)
            peersky](https://github.com/peersky)



          [+156
            -0](https://github.com/ethereum/EIPs/pull/5787/files)







Discussions to:
https://ethereum-magicians.org/t/digital-identity-standard-prop[…](https://github.com/ethereum/EIPs/pull/5787)osal/11331












Loudly stated as digital identity is a standard that would allow us to abstract away from a address/private key paradigm in to more secure way of communicating, where each identity (person or organisation) can register their name and obtain some address that is a smart contract proxy, able to represent any identities actions on chain, while also having decentralised social recovery mechanism that would allow one to secure his identity with support of ones family, friends and other people one trusts.

Basic idea is that we create a smart contract factory and registry that allows anyone to

1. Mint a special tokens (identity tokens) that are fungible ERC20 tokens with extra methods:

Burn tokens in another wallet by burning equal amount of own tokens
2. Delegate tokens to someone to use on a behalf, except for burning and transferring
3. Special methods that allows to calculate token amount on wallet relative to total circulating supply of tokens
4. Special method that allows majority of token holders to dump whole circulating supply and reissue whole supply back to those who signed under such execution in proportion.

Such token mechanism would allow one to send them to family members, collegues etc. And In case if any of wallets gets compromised others can attack compromised wallet and burn those tokens, or gather together signatures and re-issue whole supply of tokens in case if multiple wallets are compromised.

That way digital identity (soul) would be in a way immortal because tokens can always be replenished back to maximum capacity, no matter how many attacks happened, as long as true holders keep majority of power.

Such token also would allow interesting new mechanics where one that has tokens or has them delegated to can act on behalf of identity to some level of certainty.

1. Deploy a diamond proxy contract that is being owned by a majority of identity tokens from #1. This contract as a diamond proxy can be cut to represent whatever one wants it to be and can act as public address of the person.
2. Make an entry in registry allowing to register human readable identity name and link it to the diamond proxy contract and identity tokens

Such standard I believe would be greatly beneficial in order to create more reliable and robust systems and contracts. And ability for social recovery would increase speed of mass adoption.

So far proposal is a total draft and I am open for a discussion on everying

Looking forward your comments!

## Replies

**cylon56** (2022-10-18):

Hi [@peersky](/u/peersky) -

Better identity standards is a lot-standing need for the Ethereum ecosystem so glad you’re exploring this.

The implementation you’ve described with ERC20 tokens seems overly-complex though. It might be useful to review through prior identity EIPs and better understand what could be borrowed and improved upon from them. Specifically, I’d look at:

1. EIP1056
2. EIP1484
3. EIP2844

I would also recommend exploring how this might overlap with Soulbound Tokens as well as the W3C DID/VC standards. There’s a lot of existing chatter on identity standards but it will give you better context to understand how the space is approaching it today.

---

**peersky** (2022-10-23):

Hey [@cylon56](/u/cylon56) good to see you here!

To be honest main part I’m not sure right now whether I should call it a Digital Identity standard at all.

After all this is loud name and there are already plenty of US / EU standard procedures around Digital identities which brings allot of pre-assumptions right away, however,  the term “Identity” must be somehow defined within the more abstract blockchain space as well.

That definition is a main goal of a proposal here.

Firstly

I propose to abstract away identity from a concrete wallet. That’s makes a big difference with all three listed by you: they are still bounded to an address. At best a recovery address is proposed, however such straight forward recovery can be reduced to a schema *Identity = Recovery PK Holder* (even if one uses multisig, there is still single address as an owner and abstraction is not reached )

Secondly,

I seek to define what **Identity** is at all in context of a blockchain and this is what brings in difference from a DAOs which similarly are abstracted away from any single holder.

In DAOs there is assumption that token holders can disagree and act in trust-less manner, hence must proceed trough voting procedures.

Similarly as we agree that **truth** in context of a blockchain is what a majority of voting power agrees on, the proposal is to agree on that **identity** is a set of addresses that demonstrate that they have mutual trust.

The simplest implementation of such trust designation is a having revocable tokens, that each address could grant and then revoke in case if trust is undermined.

However such pattern would be highly computationally ineffective as it would involve a token per address.

My proposal is to define one single token per “identity” instance instead. This is computationally very similar to ERC20, and reduces down to idea of symmetric burn - if one revokes your tokens, you automatically revoke his tokens as well, which results that both of you loose same amount of “identity”.

And similarly, it means that if two addresses hold same amount of tokens, they have a mutual trust that can be quantised as MIN(Addr1, Addr2)

At this point I d like to keep on working on this EIP as I see some unique offering in this so far. However I’m eager for suggestions and discussion. Particular question is how to split it best in to pieces, potentially symmetrically burnable tokens could be an EIP on it own. What do you think?

---

**tahpot** (2023-01-24):

Identity is definitely an important issue to address.

Do you have some concrete user stories that relate to the problem(s) your hoping to solve.

---

**peersky** (2023-01-25):

Hi [@Tahpot](/u/tahpot)

Yes I do.

Right now though I 've decided and am working to split this in two lesser proposals.

1. Social recovery token standard
2. Digital identity high level abstraction

First one is a token standard that would allow to extend ERC20 standard that way that full token supply can be recovered in order to represent same majority group.

Second is an idea that there could be a contract that has a special logic of ownership that always follows such socially recoverable token circulating supply majority as it’s owner. Hence can be used as “Identities Address” where identity can be defined as some group of people agreeing on something with full trust.

Right now the question for me is should I close this thread and open a new 2x PRs with EIPs, or should I re-work this in to one?

