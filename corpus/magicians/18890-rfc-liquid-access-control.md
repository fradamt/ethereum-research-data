---
source: magicians
topic_id: 18890
title: "RFC: Liquid access control"
author: peersky
date: "2024-02-22"
category: ERCs
tags: [nft, token, erc-721, security, erc-20, erc1155]
url: https://ethereum-magicians.org/t/rfc-liquid-access-control/18890
views: 784
likes: 3
posts_count: 1
---

# RFC: Liquid access control

# Abstract

Token concept is widely used in Web2 environment for granting some access permissions, such as authentication.

Web3 added a concept of tokenomics where we can make assets and write business logic based on liquid, non fixed assets that can grant us some privileges (DAO voting being simple example of that).

The goal of this post is to get the comments, particularly the developer and ux expectations of discussed way to treat privileged access in a liquid form rather than statically allocated.

## Introduction

I am big fan of combining those together as I can see large potential for using standards such as 20/1155/721 for application and role base security.

There are few concepts available in that regard.

One being ability to define liquid, per method-signature access permissions as described in [method-signature-as-token-identificator](https://ethereum-magicians.org/t/method-signature-as-token-identificator/13632)

Similarly this could be utilized to produce nearly-unbreakable social recovery mechanism which I will elaborate in separate article.

Another use case for such would be to allowing minting competence tokens for DAO participation, like in https://rankify.it

Some other use-cases I’m listing below as examples of what approaches can be taken:

### Method+Account Precise RBAC use case

Building access permission module based on such principle would in theory allow to counter security vulnerabilities such as [thirdweb erc2771 multicall](https://blog.openzeppelin.com/arbitrary-address-spoofing-vulnerability-erc2771context-multicall-public-disclosure) with ease, by any semi-trusted security actor.

To do so the only requirement would be to wrap each method in to modifier requiring condition on token to fulfil. Example of such would be

```auto
// accessToken is ERC1155
modifier tokenizedRBAC() {
  uint whiteListedLiquidity = accessToken.balanceOf(msg.sender,msg.sig+WHITELISTED_OFFSET);
  uint blacklistedLiquidity = accessToken.balanceOf(msg.sender,msg.sig+BLACKLISTED_OFFSET);
  require(whiteListedLiquidity > blacklistedLiquidity)
}
function multicall(...) override public tokenizedRBAC {...}
```

Then the owner of the contract could pre-allocate whitelisting and blacklisting tokens to securiy providers, audit companies or his SecOps team and whitelist `TrustedForwarder` contract by sendign there 1 whitelisting token.

Whenever one of those security players would find the vulnerability, in order to stop the exploit it would be sufficient to send the blacklisting token id to the TrustedForwarder contact, hence breaking vulnerable circuit with “laser” precision.

If whitelisting tokens would be also allocated or possible to mint, that would give ability to change `TrustedForwarder` without need of running upgrade.

### Permission-less pause

Since tokens are liquid asset, they can be rather allocated as intent.

For example intent to give ability quickly stop protocol yet stay DoS resilient can be expressed as whitelist  pause and unpause access allocation to security council. Such allows council member to immediately pause protocol, but any counterparty can immediately unlock without requiring multi signatures as an objection for faulty decision.

If such access tokens are limited and are subject of burning during activity, principal inability to cause DoS can he designed in token allocation strategy itself.

What’s also great about this is that security council members can freely design their off and on chain logic and automated protocol which can reproduce traditional multisig systems to full extend and further.

### “Phoenix” token recovery

Another such tokenisation use case is for social recovery protocols. This serves as logical continuation of previous example.

Imagine we have a token that has generic ERC20 protocol extended with abilities to (i) burn other account tokens at expense of own 1:1, (ii) Resurrect all burned tokens to the aligned majority by submitting a multi-sig transaction and re-allocate it to signers according to their proportional balances.

If then a smart contract wallet holder who wants to secure himself, he might allocate his tokens across different EOAs, friends, family, security providers etc.

Then a simple delegation back to owners wallet could give him full power of his smart account. Alternatively uint256 level resolution of supply level could be used as depth of permissioning.

It is a simple DAO voting case so far. For simple example, one could allocate 1/3-1 to his social recovery and 2/3+1 between his multiple wallets (N>>1)

The two additional methods add functionality however.

- Purging: If some of accounts are compromised, there is no need to wait for a consensus, each individual holder can purge non-aligned account at own expense. This implies that such token holder account set is very easy to treat as aligned group, since any conflicts can be basically atomically settle.
- Resurrecting:  Recovery for any lost permissions as long as there is aligned majority with low time delay requirements in case of majority alignment. Setting time-lock delay as exponential delay  can further increase security guarantees.

### Streamlined integration with access quotas and conditions

With tokenized access model, the access issuer is able in theory not just permit someone doing something, but also in a very generalised and industry  known way define rules how the access token state must me mutated.

In example, one could be required to Lock his balance during tx, meaning that transaction that dumps tokens as side effect fails. Similarly reentrancy guard could be implemented by locking access asset. Another way for some sensitive methods could make simple rate/quota limiting by requiring to burn or transfer tokens, hence allowing to implement automatic control loops in the blockchain system without need to interact externally.

## Rationale for liquid approach

### Control issuance risks

In examples above assuming that security players or owner might have have some balance or mint access to whitelisting token for a specific method, this is a risk on it own. Such whitelisting transfers can be time-locked allowing other security “council” members to front-run such issue with allocating blacklist tokens to block such an activity.

This means that careful system and incident response planing still allows to have enough of security guarantees by simply ensuring that whitelisting capacity is below blacklisting. Worst case scenario for such would be security “council” members throwing “tokens on a fan”, which still would give enough time for community to react.

Furthermore, using “Phoenix” proposed pattern it would allow to rollup such gaming the system to consensus question, with misalignment immediate settlement.

### Liquid approach is not a requirement

One can argue that most of examples above can be implemented without liquid tokens, by using more conventional RBAC modules.

In fact our latest [Access Manager](https://docs.openzeppelin.com/contracts/5.x/access-control#access-management) module is indeed a masterpiece which I encourage to use.

However, this approach is in principle taking “solid ground” approach which implies that

- issuing permissions is central to the administrator and can be less versatile.
- grantees are not able to easily pass their permissions to another account.
- handling in block or in tx rate limiting becomes more sophisticated.
- It is less generalisable to anything approach
- It can be well standardised. Ex: msg.sig is bytes4, so there is large overhead to define conditions (bet/stake/lock/pay/burn) or transferability (souldbound/transferrable) with simply offsets.
- It can stimulate market economy in general adding intrinsic values to the assets.
- We don’t impose in best practices a requirement to wrap every method, even public in access module wrapper anticipating possible zero-days.

On other hand, there are concerns in such approach, particularly:

- If tokens are allowed to be transferred, especially NFTs create a permission marketplace. It is not rather clear how it can play out, but someone in theory could just go and sell his permissions on open Auction. It is less prominent in case of Pheonix example, as community would be able to counter that, but more actual in case of such permissions defined as erc721.
- There is generally more “mess and phishing” around well established token standards. Using more explicit access modules is believed to reduce risks of accidental transactions
- Holders account compromise can lead to some unique permissions (especially if erc721 used) to be stolen or rug pulled and potentially unrecoverable
- It might be daunting to understand for those who are more used to enterprise kind-of security models

## Request for comments

As outlined, there are pros and cons of such an approach.

I would like to understand what are community thoughts on such liquid approach proposal when it comes to access and role management.
