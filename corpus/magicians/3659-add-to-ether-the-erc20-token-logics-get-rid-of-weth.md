---
source: magicians
topic_id: 3659
title: Add to ether the ERC20 token logics (get rid of WETH)
author: PaoloRebuffo
date: "2019-09-18"
category: EIPs > EIPs core
tags: [defi, scaling, weth]
url: https://ethereum-magicians.org/t/add-to-ether-the-erc20-token-logics-get-rid-of-weth/3659
views: 2653
likes: 4
posts_count: 4
---

# Add to ether the ERC20 token logics (get rid of WETH)

**Premise**

The nascent DeFi and DeX industries are almost entirely based on the ethereum blockchain and represent a fundamental and growing part of the value and the reasons for adopting this fantastic blockchain.

One of the cornerstones on which this part of the ecosystem is based is the smartcontract WETH which allows ether to obtain some properties (methods) typical of erc20 contracts, for example:

transferFrom

approve

allowance

The use of WETH instead of eth produces an over-cost both in terms of gas spent and in terms of code complexity and protocols for the DeFi sector and for decentralized exchanges with respect to the use of eth.

**Proposal**

For this reason, I propose to include the ERC20 token logic directly in the EVM, in order to make WETH use useless.

If we could handle eth as we do for WETH, wrapping and unwrapping operations would not be necessary and transfers between accounts and smartcontracts would have the typical gas cost of a transfer of eth (21,000) and not of an erc20 token (about 60,000)

In addition to this, DeFi protocols and DeX protocols would be simplified by reducing attack surfaces.

This possible EIP (still to be opened) goes in the direction of a clear market demand, today WETH, on average 7000 tx / day occur with peaks of 18,000 tx / day and a consequent waste of gas and resources for the creation of Dapp that need ether with the properties of an ERC20.

**Disclaimer**

I am a designer not a coder. I do not have the skills to make a proposal in terms of implementation, I ask you in advance for an opinion on the technical feasibility and on the problems that such a proposal has.

## Replies

**wjmelements** (2019-10-02):

I can see where you are coming from as a designer. In some other blockchains, the native token has the same privileges as the dominant fungible token standard. Here is an engineering perspective against it in the context of Ethereum.

- WETH/ERC20 is more work than ETH, so it should cost more gas to use.
- ETH isn’t a smart contract with an address; it is the low-level value that can be passed with CALL.
- ERC20 may be standardized, but it is not optimized. We do not know how to write an optimal ERC20 contract. Nobody knows exactly how much a built-in ERC20 contract should cost.
- WETH can do everything ERC20 ETH wants to do, and already exists.

---

**PaoloRebuffo** (2019-10-02):

Hi wjmelements, thanks for the reply. I go with order:

**WETH/ERC20 is more work than ETH, so it should cost more gas to use.**

1- weth / erc20 needs more gas than eth because it is an erc20, this is exactly THE problem that I would like to be solved. I find it a waste of gas to transfer weth instead of eth, and I find it a waste to be forced to wrap and unwrap to get some properties that could possibly be included as native to EVM.

**ETH isn’t a smart contract with an address; it is the low-level value that can be passed with CALL.**

2 - my goal is to allow the replacement of the WETH smart contract with ETH, which involves rewriting the DAPPs that use WETH so that they directly use ETH.

**ERC20 may be standardized, but it is not optimized. We do not know how to write an optimal ERC20 contract. Nobody knows exactly how much a built-in ERC20 contract should cost.**

3- I agree, that’s why I ask for collaboration and research in this field. There is a risk that in the end it is not worth it (I Know).

**WETH can do everything ERC20 ETH wants to do, and already exists.**

4- True, however the Wrap, Unwrap and transfer oprations have a cost that could be reduced to zero and reduced if the properties of ERC20 were added natively to ether.

---

**ZuluNatal** (2020-07-27):

Well consider the high fees to wrap eth. The high fees to unwrap ether. The high fees to send ether. The award for best day light robbers goes to the miners, forget us the users actually trying to use these erc tokens. We pay the high gas fees.

In a real world example it would be okay to for my bank to charge a high fee for a transfer to other bank. What would not be okay is my bank charging high fees to send to another account with my bank. If you geeks cant wrap (sic) your head around that logic then I dont see why I should contributeto your erc tokens and ethereum. Rather trade these tokens on exchanges

