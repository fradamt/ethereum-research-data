---
source: magicians
topic_id: 13623
title: "EIP-?: Commander Token"
author: neiman
date: "2023-03-31"
category: EIPs
tags: [erc, token]
url: https://ethereum-magicians.org/t/eip-commander-token/13623
views: 551
likes: 2
posts_count: 2
---

# EIP-?: Commander Token

Hi everyone! I’m from Esteroids and Woolball. As part of our work, we created two potential EIPs extending ERC721. What do we need to do in order to propose these as EIPs?

## TL;DR

[Commander Token](https://github.com/woolballers/commander-token-contracts/) is a set of two token standards that enhance the functionality of ERC721 tokens. These standards provide refined control options for transferring or burning tokens.

Commander Token was created for the Woolball project (an ID system with links) but can be used for many other use cases, such as Soulbound Tokens, Community-bounded Tokens, or Tokens bounded to a name.

We provide an interface and a reference implementation for both standards, see [our repository](https://github.com/woolballers/commander-token-contracts/).

## Commander Token

The first token standard in Commander Token is the eponymous Commander Token, which is an ERC721 token with partial transferability and burnability.  This token standard provides a flexible approach to token transferability that allows various levels of control.

For example, Commander Tokens can have full transferability like regular ERC721 tokens, non-transferability like Soulbound Tokens, or anything in between, including transferability controlled by a community or transferability that changes with time. The same flexibility also applies to burnability.

Commander Token provides two mechanisms for controlling transferability.

The first is a simple `setTransferable` function that marks the token as transferable or not. In the reference implementation, the token owner calls this function, but more elaborate implementations are possible that allow for control by someone else, a community, or even a smart contract.

The second mechanism is *dependence*, which allows the owner of a token to set a token to depend on another token, even from another contract. Once a token depends on another token, it is transferable only if the other token is transferable as well. Tokens can be dependent on many different tokens, and in that case, they are transferable only if all the other tokens are transferable as well.

The interface for Commander Token includes functions for managing dependencies, transferability, and burnability, as well as functions for checking the transferability and burnability properties of a token.

## Locked Tokens

The second token standard in Commander Token is Locked Tokens, which essentially binds tokens together.

If a group of tokens that belong to the same owner are locked together, it means that they will always be transferred together. As long as the locking exists, the owner cannot transfer any of the tokens separately.

Locked Tokens are particularly useful for creating a collection of tokens that should always have the same owner. An example of this is a classic name system with domains and subdomains, where each domain and subdomain is represented by a token. By locking all the subdomains to the domain, each time the domain is transferred, all its subdomains are transferred as well.

The interface for Locked Tokens simply consists of a few functions for locking and unlocking tokens.

## State of development

We implemented interface and reference implementations for both Commander Token and Locked Token . For each implementation we created plenty of tests.

However, the code has not been audited and is not suitable for use in production at this stage.

## Replies

**abcoathup** (2023-03-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neiman/48/9043_2.png) neiman:

> What do we need to do in order to propose these as EIPs?

Suggest reading: [Guidelines on How to write EIP. Do’s and Don’ts including examples | by Anett | The Fellowship of Ethereum Magicians | Medium](https://medium.com/ethereum-magicians/guide-on-how-to-write-perfect-eip-70488ad70bec)

