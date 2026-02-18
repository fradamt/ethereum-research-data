---
source: magicians
topic_id: 14849
title: "ERC-7246 - Encumber: Extending the ERC-20 token interface to allow pledging tokens without giving up ownership"
author: coburncoburn
date: "2023-06-27"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-7246-encumber-extending-the-erc-20-token-interface-to-allow-pledging-tokens-without-giving-up-ownership/14849
views: 2761
likes: 8
posts_count: 9
---

# ERC-7246 - Encumber: Extending the ERC-20 token interface to allow pledging tokens without giving up ownership

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/7246)














####


      `master` ← `compound-finance:encumber`




          opened 08:06PM - 27 Jun 23 UTC



          [![](https://avatars.githubusercontent.com/u/32463466?v=4)
            coburncoburn](https://github.com/coburncoburn)



          [+223
            -0](https://github.com/ethereum/EIPs/pull/7246/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/7246)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












## Abstract

This ERC proposes an extension to the ERC-20 token standard by adding Encumber — the ability for an account to grant another account exclusive right to move some portion of their balance. Encumber is a stronger version of ERC-20 allowances. While ERC-20 approve grants another account the permission to transfer a specified token amount, encumber grants the same permission while ensuring that the tokens will be available when needed.

## Motivation

Token holders commonly transfer their tokens to smart contracts which will return the tokens under specific conditions. In some cases, smart contracts do not actually need to hold the tokens, but need to guarantee they will be available if necessary. Since allowances do not provide a strong enough guarantee, the only way to do guarantee token availability presently is to transfer the token to the smart contract. Locking tokens without moving them gives more clear indication of the rights and ownership of the tokens. This allows for airdrops and other ancillary benefits of ownership to reach the true owner. It also adds another layer of safety, where draining a pool of ERC-20 tokens can be done in a single transfer, iterating accounts to transfer encumbered tokens would be significantly more prohibitive in gas usage.

For some sample implementations & toy use cases, see [this example repo](https://github.com/compound-finance/encumber_samples).

## Replies

**crazyrabbitLTC** (2023-07-10):

This is a pretty interesting idea, my first thought would be, “Could we just ask the user move the tokens to a lockup?”, encumbering would be difficult for indexers and parses to handle because a user might have a certain balance, but that balance might not actually be available. Also, how would the process of removing an encumbrance work? If it requires the recipient of the token to agree, then users could find there tokens locked up forever if the recipient doesn’t agree to release it.

In theory I do like the idea though.

---

**coburncoburn** (2023-07-11):

Thanks for these questions! Allow me to attempt to clarify

re Lockup:

A lockup could be purpose built to give ownership benefits e.g. governance votes back to the original owner, but those contracts would need to be generally re-implemented or re-deployed by whatever protocol was requiring the lockup, introducing complexity and risk. In some cases it would require deploying a smart contract vault for each user, which is costly.

Another side-benefit, which was not the purpose but a happy discovery, is that while a pool can be drained with a single `ERC20.transfer`, an Encumber based protocol would require iterating all encumbered accounts and transferring tokens out of individual wallets. This would be more expensive to accomplish, requiring first indexing positions to attack and then to pay the additional gas cost of iterating them all.

Additionally, in the off chain world there are schools of thought that are aided by Encumber. For example, a party may not being wish to mingle tokens in a pool with unknown parties. A party so resolved could participate in a protocol by encumbering tokens with a clear conscience, since the tokens are never commingled by being transferred to a shared pool.

Re indexers: Yes, wallets and indexers relying heavily on `balanceOf` would need to adapt for 7246 tokens. Interpretations of `balanceOf` would need to adapt to account for encumberedBalanceOf. There is a benefit though, as reading `encumberedBalanceOf` in one slot of the token would be easier than iterating known defi positions to discover additional token balances.

Re removing encumbrances/bricking tokens: the removal process is simply `ERC7246.release(owner, amount)`. This is drop-in replacement of `ERC20.transferFrom(address(this), owner, amount)` in the most ordinary case. Encumber has practically the same risk surface area as `ERC20.transfer` with respect to sending your coins into the oblivion or locking them for eternity. The traditional “pull” pattern of `ERC20.approve` followed by `ERC7246.encumberFrom` is the safer route.

---

**ash2cash** (2023-07-14):

[@coburncoburn](/u/coburncoburn) very nice idea you offer. Nice that we are thinking same way , previously Envelop DAO realized such a concept where we split up right of ownership and usage for in-game mechanics of non-pledge rental. Mainly we focused on NFTs and realized the concept via wrapped NFT. Had thoughts to use it for DeFi use cases you described - like rental of liquidity with the right of call back. Inside wNFT you can wrap FTs, NFTs, LPs - and set-up rules of behavior: time, actors, events of execution, transfer locks and multiple others. Think we got what to discuss, especially taking in account that this year we are focusing on bridgeless cross-chain, decentralized cross-chain liquidity, tradable index and much stuff more.  Feel free to reach out alex@envelop.is.

---

**DrakeEvans** (2023-10-02):

To be clear, release can only be called by the taker? So unlike approvals this cannot be revoked by the user.  This opens a lot of use cases and IMO is the way debt markets should work (and how they work in real life). This allows the use of an asset as both collateral and for the holder to retain ownership.  Similar to a mortgage or a car note.  Ownership remains with user however, 3rd party has rights on the asset.

---

**coburncoburn** (2023-10-27):

yes, this is precisely the goal

---

**SamWilsn** (2023-12-22):

Might I suggest `Unencumber` instead of `Release` as an event name? It’s more unique to this proposal.

---

**arr00** (2025-12-19):

Agree with sam here–may be a bit too intrenched at this point though.

---

**arr00** (2025-12-19):

> ```auto
> /**
> * @dev Emitted when the encumbrance of a `taker` to an `owner` is reduced by `amount`.
> */
> event Release(address indexed owner, address indexed taker, uint amount);
> ```

The docs for the `Release` event seem to infer that any time the value of `encumbrances(owner, taker)` decreases, this event should be trigged. The reference impl should be changed to follow this.

