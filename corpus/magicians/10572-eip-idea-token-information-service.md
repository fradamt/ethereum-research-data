---
source: magicians
topic_id: 10572
title: "EIP Idea: Token Information Service"
author: peetzweg
date: "2022-08-29"
category: EIPs
tags: [erc20, onchain, chain-agnostic]
url: https://ethereum-magicians.org/t/eip-idea-token-information-service/10572
views: 824
likes: 0
posts_count: 2
---

# EIP Idea: Token Information Service

Hi, thanks for stoping by!

I want to propose a protocol and implementation of a service similar to ENS but for token information. More specifically a tokens “image”. As with ENS, we want to resolve machine addresses with user friendly names. We are doing something similar with the `name()` and `symbol()` of an ERC20 token for sure, but it’s lacking the image of the token. Images of tokens are omnipresent in every web3 app.

Since realising this I’m quite confused to not find an proposal for a ERC20 extension to include a `image()` field.

Although this extension might be handy, it’s not backward compatible. Therefore I want to suggest a registry similar to ENS. Potentially name `Token Information Service - TIS` ![:person_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/person_shrugging.png?v=12) . Which serves first and foremost humans, like ENS. In the most basic form it should just contain a `mapping(address=>string)` resolving a token address to i.e. a URI of the tokens image/logo.

The value of the mapping can be updated by the `owner` of the token via the `Ownable` interface or other  used authorisation mechanism of tokens. For tokens without any ownership left, it could be set by the maintainers or DAO proposal of the service.

Another useful addition I want to suggest is a function to resolve the whole set of information about a token in a single function call returning: `symbol`, `name`, `decimals` and `uri` (image) of given token address or for multiple addresses even.

`function info(address token) returns (string, string, uint, string)`

This would be handy for a lot of frontend applications. As normally this data is either fetched and stored in advanced by a centralised services. Or if retrieved onchain directly from the contract, it has to be done in 3 individual `eth_call` invocations for symbol, name, decimals. So clearly not ideal and cumbersome.

I think this would be a great addition to the current token landscape and would resolve inconveniences every web3 currently solves on it’s own. People store the images in repos, fetch them from coingecko or create their own for LP tokens. This would resolve all that and give them community a decentralised solution for a central service resolving an image for a token.

I think it’s valuable to create such a service via an EIP as to have an official approval for the service. I would be happy to come up a proper EIP draft and reference implementation.

What do you think about this? Would this be valuable for you or your project? Does something already exist which solves this problem?

Notes:

- should resolve data compatible with EIP-747 to directly integrate into wallets using this standard
- current solutions

Trust Wallet assets repo used by SushiSwap and Uniswap - GitHub - trustwallet/assets: A comprehensive, up-to-date collection of information about several thousands (!) of crypto tokens.
- upload manually to etherscan, “Update Token Info” -  Token Info Submission Guidelines
- coingecko - “can’t put more links, but also manual centralized process to set token logo”

## Replies

**peetzweg** (2022-08-29):

I’m also curious about opinions about extending ERC20 by an optional “logo uri” field. IMHO token logos are essential these days and should become a part of the standard. However, this is most likely a separate EIP if there is enough interest.

