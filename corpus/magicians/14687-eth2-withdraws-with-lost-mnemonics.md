---
source: magicians
topic_id: 14687
title: ETH2 withdraws with lost mnemonics
author: Darren-Yau
date: "2023-06-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/eth2-withdraws-with-lost-mnemonics/14687
views: 1829
likes: 5
posts_count: 10
---

# ETH2 withdraws with lost mnemonics

Staking withdraw to original sender.

I would just like some feedback on this idea, but not sure if this is possible.

**Abstract**

This is a proposal for validators an alternative way retrieve their staked eth. The Ethereum launchpad goes through great effort to inform solo validators not to lose their mnemonics as it is the only way to retrieve their funds after the Shapella upgrade, but unfortunately, it is entirely possible to lose/misplace a mnemonic. The idea is that the validator should have control of the original deposit address and would be the rightful owner, therefore returning staked eth to the depositor would allow validators access to their staked eth in the case they have lost their Eth2 mnemonics phrase and are unable to create a deposit address.

**Motivation**

Validator who have lost their Eth2 mnemonics phrase, and did not create a deposit address are unable to create a withdraw address without the mnemonic. Without an withdraw address they are unable to access their staked eth, or any rewards from attestations. That being said, there is now little to no reason for them to keep their validator up and running.

**Specification**

I am not entirely sure if this is doable, but I believe that this can be done by referencing the beacon chain deposit address to determine the original sender. I am seeking the help of the Ethereum magicians to see if this is possible.

**Rationale**

Validators are the ones that maintain the network, and those without a way to generate a deposit address have no reason to keep their validators running other then MEV. This can cause missed proposal/missed attestations and cause slight delays when validators are offline for this reason.

I am currently seeking the help of Ethereum Magicians to see if this is something that should be pursued, and I’m happy to work with anyone interested.

## Replies

**hiddenintheworld** (2023-06-15):

The original deposit address may not be under the control of the validator, especially if they have lost their mnemonic phrase. For example, the deposit address could be owned by an exchange or a third-party custodian. In such cases, returning the staked ETH to the original deposit address would not help the validator recover their funds.

Furthermore, the proposal does not address the security implications of returning staked ETH to an address that may no longer be secure. If the original deposit address has been compromised or is no longer secure, returning staked ETH to that address could result in the loss of those funds.

---

**Darren-Yau** (2023-06-15):

Thanks for the reply. I forget some users staked with third party. I was assuming that a user would send funds directly to the deposit contract and have a third party stake with their signin keys. Would you know of any other secure way to retrieve staked funds once the mnemonic phrase is lost? Thanks!

---

**hiddenintheworld** (2023-06-17):

Think from two approachs

1. Backup
2. Multi-party

---

**Darren-Yau** (2023-06-17):

How would I approach retrieving staked eth from multi party? A little bit more about my situation is that I staked eth into the deposit contract from my own personal wallet. I still have control of those keys and it has never been compromised. I’ve lost the mnemonic to my eth2 address, and never added a deposit address to those validators. I only have the sign in keys that were generated. Where should I go to learn more about multi party?

---

**Darren-Yau** (2023-06-22):

This is my final idea before I give up hope. Would it ever be considered a good idea to enable the deposit back to its original ETH1 deposit address? My suggestion is once a staking balance is 16, it is removed from the staking pool. Would it be possible in the future to allow those that to be returned to its original ETH1 address. More then likely those funds will belong to validators that have lost their keys, and want to be united with their long lost ETH again. Would that be possible or just wishful thinking?

---

**maverickandy** (2024-03-03):

Apologies for resurrecting an old topic but I would like to raise something here:

I’m a pre-genesis staker and it was impossible me to set a withdrawal address at the time so my creds are still on 0x00. I was also an active staker on the testnets but made a big, big mistake when writing down my mnemonic. I’ve seemed to have written down a mnemonic used on the testnets so I no longer have access to my actual mnemonic.

My question is this:

For people that still have creds set to 0x00, with access to the original deposit address + the actual keystores used for the deposit, should this not be enough to prove ownership?

I know have the power to exit the validators (and thus removing security of the network) but I do not have the power to access my funds. Which feels very unfair even though it was my own fault.

---

**Eth2** (2024-04-17):

Same situation here, we should be able to withdraw to the original deposit address when we have all the files for the deposit and keystore. Especially for initial staker without 0x01 address.

---

**Eth2** (2024-04-17):

Why would deposit to the initial address not be useful? Especially if the own ask for it. It’s better to provide a solution for honest people then nothing. I don’t see the arm or sending it back to the sender especially if that one is asking for it and especially if we are initial staker without the withdrawal address.

---

**maverickandy** (2025-11-24):

I’ve built a dashboard to track progress of deprecating the BLS withdrawal credentials.

Also developed a proposed mechanism for validators that are unable to migrate (e.g. due to loss of private key/ mnemonic). I will lobby for support to include these proofs into the hardfork to quantum-proof signatures.

All information can be found here: [deprecatebls.com](http://deprecatebls.com)

