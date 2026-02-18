---
source: magicians
topic_id: 5292
title: Chargeback Tokens
author: bradleat
date: "2021-02-04"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/chargeback-tokens/5292
views: 1570
likes: 0
posts_count: 1
---

# Chargeback Tokens

Awhile ago I submitted an [EIP for a Recoverable Token Standard](https://ethereum-magicians.org/t/erc-1080-recoverabletoken-standard/364), but it appears that since then this issue has been better addressed by wallets such as Argent or Gnosis Safe.

Building on this work, I was motivated to solve the other part of the EIP which was dealing with a standard for chargebacks. This concept will be important for users who wish to spend their tokens (such as DAI) in exchange for goods or services that they fear may not be delivered.

The basic concept is that we create a virtual “check” which includes a default remedy if a chargeback is requested. Here we can send tokens to the sender, recipient and also another address (such as one for a counterfactual contract which can deal with a recovery process). Transfers also have a blockCount that must pass before they can be finalized. During this waiting period they can be disputed. Either party then may trigger the defaultResolution or may propose other remedies to the situation.

As an aside the method of signing the various hashes needed by this system is delegated to a contract signing method wherein someone in control of a contract can publish a signature that can be consumed by the chargeback token contract.

Besides this the proposal is essentially an escrow for tokens.

Remedies (especially the default Remedy) should allow for a satisfactory recovery of the situation for both parties. This may mean triggering a decentralized justice process for the recovery of the funds, splitting the funds, or (for account with KYC or other incentives to be kept in good standing and uniquely identifying a user) we maybe choose to lookup the account’s history to compute a risk score and use that information to proceed with a chargeback.

As a other option for a good default remedy is to allow the sender to recover a small amount of funds with each future such transfer if they continue to use a system without asking for further remedies. Then after N blocks, the intended recipient can recover the rest of the funds. The idea being that the locking of the funds (to be recovered by future transfers), forces the user to continue using this account if they want to receive their remedy. However, it also allows recipients to understand the risk that the sending account carries. On the other side, if the recipient account is a popular account (for a retailer perhaps), then we can use this information to see if the sender account is requesting more or less remedies than average for a given recipient. This idea in particular needs some work.

You can find a draft implementation for this idea [here](https://github.com/inKibra/chargeback-token/blob/main/contracts/chargeback-token.sol).

If you have any feedback on this idea, I would very much welcome it! Thanks.
