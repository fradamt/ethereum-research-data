---
source: magicians
topic_id: 12179
title: "Discussion: A token standard for Authentication/Authorization"
author: 3braheem
date: "2022-12-17"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/discussion-a-token-standard-for-authentication-authorization/12179
views: 715
likes: 2
posts_count: 2
---

# Discussion: A token standard for Authentication/Authorization

Related: [ERC-644 Proposal](https://ethereum-magicians.org/t/eip-644-a-standard-for-permission-token/9105/3)

I wanted to bring up a discussion on proposing a standard for a token with properties specific to use as a tool for authentication/authorization, because in my opinion, this could be key to integrating web3 into the greater internet further.

There are benefits to the use of on-chain assets for auth, namely streamlining the onboarding process for access permissions by associating a wallet with those permissions. Companies/organizations could benefit from a faster, reliable process to hand out permissions through company wallets, which would likely see more use as web3 protocols develop further and offer more productivity value.

An issue I see with trying to implement something like this is the nature of our current ERC token standards, they are simply not made for this type of functionality. ERC20/721/1155 etc. do not have the features necessary to implement this well, for example, I think its pretty clear a company wouldn’t want its employees to be able to trade permissions online.

Let me know what you think on the usefulness of a standard like this, because I see many possible applications for web3 auth tokens that could have a lasting impact on software.

## Replies

**vaumoney** (2022-12-17):

Think of an **(a) open source service token** and *an (b) ISP wallet*, authority.

I think `upgradeContract` `permissionToken` `permission` `balance` is useful for an `RLP NodeList` Open Source ***Authority*** for (A) programmatic ***minting*** (“gateway”…) *or (B) wallet recovery and generation*. *The **custody differs for the service, like Digital Ocean, who does provision (a) deployment logs for their buildpack apps** (i.e. ex-droplet).* *[Phone Authentication, the app developer](https://ethereum-magicians.org/t/nonce-minter-bot-for-erc20mintable-open-source-wallet-supply-recovery/11930), and the Identity Provider can (b) begin the chain track implementation, or recover any publicId balances (using a dashboard like Firebase/Identity Platform, and setting allowed domains)*, not ***mint***.

*This recoverable open source layer I want to use in front of USDC tbills or even better, capital currency stock; I’m not sure why **ACH reconciliation and card issuers won’t allow nonfinancial banks unless we use blockchain** (i.e. Mastercard, potentially non-U.S.), but the Ummah can only take introspectively equal and full measure, as ability makes need and takes from market, and I agree bond-purchases are stolen from an in balanced market towards the right to ownership. So here is either a coincidental or compelled use case need, but I’m not forfeiting my desire to use ACH even without Ethereum in this statement; this use case is important - as we likely all know - for **wallet custody recovery**, generally.*

