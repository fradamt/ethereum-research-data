---
source: ethresearch
topic_id: 12220
title: Transactions that pay for themselves
author: vrwim
date: "2022-03-16"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/transactions-that-pay-for-themselves/12220
views: 2294
likes: 3
posts_count: 3
---

# Transactions that pay for themselves

My idea surrounds the concept of onboarding users. I organise hackathons and give out an original NFT to every competitor. These users mostly have crypto, but some don’t. I have to provide a faucet where they can request ETH (or the EVM-compatible blockchain the hackathon is sponsored by) so they have enough crypto to submit their voucher and receive their NFT. The issue I have is that this faucet needs to calculate the correct amount of ETH to dispense and then they need to submit their transaction with the correct fee to make it work.

It would be much easier if I could have some opcode or similar to describe that a certain contract invocation is paid for by the contract.

The way I envision this is that you perform a transaction giving exactly 0 gas. Then the first opcode in the function you call tells the EVM that the contract will pay for this invocation, possibly with a certain gas price and gas limit, like you do with regular transactions. If a transaction is sent with 0 gas and this opcode is not the first instruction, then the transaction is invalid.

If your transaction supplies too little gas, this may por may not supply the transaction with additional gas, but I leave that discussion to you.

I envision this as a modifier in Solidity, like this:

```auto
function functionName() public paysOwnGas(gasLimit, gasPrice) {
}
```

What do you think?

## Replies

**MicahZoltu** (2022-03-16):

I think what you want is either meta-trantsactions or account abstraction.  These are both more generalized/broad solutions to the problem of transaction signer needing to be the one who pays gas.  There have been some other proposals as well like sponsored transactions, but I think something else is likely to win out over those.

---

**nollied** (2022-04-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vrwim/48/8828_2.png) vrwim:

> I organise hackathons and give out an original NFT to every competitor.

why do you need a faucet to send people ETH, then have them pay for the gas using said ETH as a third-party to your NFT transaction, when instead you could cut out the middle-man and just send them the NFT directly?

