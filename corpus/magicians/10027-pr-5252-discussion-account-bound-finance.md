---
source: magicians
topic_id: 10027
title: "PR-5252 Discussion: Account-Bound Finance"
author: hskang9
date: "2022-07-21"
category: EIPs
tags: [nft, wallet, defi, identity, soul-bound]
url: https://ethereum-magicians.org/t/pr-5252-discussion-account-bound-finance/10027
views: 2978
likes: 1
posts_count: 11
---

# PR-5252 Discussion: Account-Bound Finance

---

eip: 5252

title: Account-bound Finance

description: An EIP-5114 extension to remove insolvency and arbitrary loss of funds

author: Hyungsuk Kang ([@hskang9](/u/hskang9))

status: Draft

type: Standards Track

category: ERC

created: 2022-06-29

requires: 721, 1155, 5114

---

## Abstract

This EIP proposes a form of smart contract design pattern and a new type of account abstraction on how one’s finance should be managed in web3.0, ensuring transparency of managing investments and protection with self-sovereignty even from its financial operators.

This EIP also extends EIP-5114, but the difference is that it can be transferred to other accounts for mobility between managing multiple wallets.

## Motivation

Finance in the crypto ecosystem is facing a huge trust issue. Smart contracts are often proxies, with the actual logic of the contract hidden away in a separate logic contract. Many projects include a multi-signature “wallet” with unnecessarily-powerful permissions. And it is not possible to independently verify that stablecoins have enough real-world assets to continue maintaining their peg, creating a large loss of funds (such as happened in the official bankruptcy announcement of Celsius and UST de-pegging and anchor protocol failure). One should not trust exchanges or other third parties with one’s own investments.

The pattern empowers more self-sovereignty and gives more credentials(obviously with an Account-bound token) than locking financial data in the operating team’s contract.

Segregation between investor’s fund and operation fee is clearly specified in the smart contract, so investors can ensure safety from arbitrary loss of funds by the operating team’s control.

## Specification

The pattern consists of 5 components, manager, factory, finance, account-bound token, and extension.

### Diagram

![Trulli](https://raw.githubusercontent.com/hskang9/EIPs/eip-5190/assets/eip-5252/diagram.svg)

**Fig 1 - Component Diagram of EIP-5252**

**`Manager`**: **`Manager`** contract acts as an entry point to interact with the investor. The contract also stores parameters for **`Finance`** contract.

**`Factory`**: **`Factory`** contract manages contract bytecode to create for managing investor’s fund and clones **`Finance`** contract on **`Manager`** contract’s approval. It also mints account-bound tokens to interact with the `Finance` contract.

**`Finance`**: **`Finance`** contract specifies all rules on managing an investor’s fund. The contract is only accessible with an account that has an Account-bound token. When an investor deposits a fund to **`Manager`** contract, the contract sends the fund to **`Finance`** contract account after separating fees for operation.

**`Account-bound token`**: **`Account-bound token`** contract in this EIP can bring the **`Finance`** contract’s data and add metadata. For example, if there is a money market lending **`Finance`** contract, its **`Account-bound token`** can show how much balance is in agreement using SVG.

**`Extension`**: **`Extension`** contract is another contract that can utilize locked funds in **`Finance`** contract. The contract can access with **`Finance`** contract on operator’s approval managed in **`Manager`** contract.

## Backwards Compatibility

This EIP has no known backward compatibility issues.

## Reference Implementation

Reference implementation is a CDP-lending stablecoin project [here](https://github.com/digitalnativeinc/standard-evm/tree/master/contracts/vaults/meter).

## Copyright

Copyright and related rights waived via CC0.

## Replies

**SamWilsn** (2022-12-13):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@stoicdev0](/u/stoicdev0)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@stoicdev0](/u/stoicdev0) please take a look through [EIP-5252](https://eips.ethereum.org/EIPS/eip-5252) and comment here with any feedback or questions. Thanks!

---

**stoicdev0** (2022-12-19):

Sorry for the delay, I’ll review today.

---

**stoicdev0** (2022-12-21):

There are a lot of components which makes this very difficult to review. I don’t think I’ll be able do it in the next couple of weeks, apologies.

---

**hskang9** (2023-01-21):

[@stoicdev0](/u/stoicdev0) any updates

---

**SamWilsn** (2023-01-23):

[@stoicdev0](/u/stoicdev0) is a volunteer reviewer. There are no criteria to become a reviewer, and there are no qualifications required. These reviews are informal, and are **not required** before progressing your EIP.

That said, calling a community member a “moron” is unacceptable behaviour. Please treat everyone here with respect and follow the [rules in the FAQ](https://ethereum-magicians.org/faq#civilized).

---

**hskang9** (2023-01-23):

With that said, EIP is just being a proposal platform in disguise with one arbiter changing the rule even if one makes a contradiction for what it has been built for. Stop running circus being Do Kwon in your organization and do your assigned job.

---

**hskang9** (2023-01-23):

If there are not reviewers who cannot give technical in-depth review as they are all volunteering with no reward, what is this platform other than [@vbuterin](/u/vbuterin)’s echo chamber who can just make things without thorough peer review and publicize?

---

**hskang9** (2023-01-23):

Solidity was supposed to be universal programming language where everyone should be able to join and verify whether it should work. Now the code here is reviewed by the people who is only “interested”. How in the world does the code determine technical validity based on the “interest of the reviewer”?

---

**stoicdev0** (2023-01-26):

Hey there, sorry for lack of feedback. I’ve been trying to wrap my head around it but it’s not simple since there are 7 actors there.

With that said, that gives you no right for being disrespectful.

[@SamWilsn](/u/samwilsn) for obvious reasons I’d like to be removed as reviewer for this. Thanks.

---

**hskang9** (2023-03-30):

For actor, do you mean the contract or account to interact? Not only you haven’t managed to read the whole contracts’ architecture, you can’t even elaborate yourself. With that insolvency and disintegrity, that gives you no right for having respect as a reviewer, and you deserve to be criticized. I wouldn’t even have a single word about you if you didn’t take responsibility to review this, but you did, and you messed up.

