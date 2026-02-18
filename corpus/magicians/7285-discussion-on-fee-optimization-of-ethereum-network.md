---
source: magicians
topic_id: 7285
title: Discussion on fee optimization of Ethereum network
author: PHPJourney
date: "2021-10-17"
category: EIPs > EIPs core
tags: [gas, core-eips, live-data, chat]
url: https://ethereum-magicians.org/t/discussion-on-fee-optimization-of-ethereum-network/7285
views: 1690
likes: 1
posts_count: 7
---

# Discussion on fee optimization of Ethereum network

With the high transaction fees caused by the rise in the overall price of Ethereum, Ethereum network applications are gradually transferred to other such as binance smart chain, Tron and heco. I propose to focus on optimizing the smart contract fees in the subsequent upgrading process

To solve this problem, my optimization idea is

1. The Ethereum main network compensates the gas usage fees involved in contract transactions. The fixed rate of client handling fees has been realized, and eth can be returned in proportion to the actual usage rate
2. In the smart contract interface, the block function provides the actual use parameters of the current transaction. The DAPP application team can make token compensation according to the user’s actual use of gas
For example:
Bob deploys a smart contract. According to the gasused cost of the block function, the main network outputs 80% eth from the 0x0 address and returns it to Bob’s wallet address
Alice initiates a transaction with Bob’s contract address, and Bob’s contract address returns the corresponding service charge to Alice according to the calculated service charge proportion
If this scheme can be passed, Ethereum’s ecological application will be steadily improved. From the advent of bitcoin to the subsequent emergence of various main chains, many application teams are deterred by the high handling fees and switch to other places. Now Ethereum is facing this problem, which I think needs to be solved urgently
Second question
The wisper project in Ethereum network seems to be at a standstill and is not supported by most providers. On the premise of decentralization, I think we should provide users with a fee free contract interface method for users to share real-time chat data
This method only does data transmission without storage. If the contract administrator requires storage, a certain gas fee will be charged.
I hope to receive the latest message from the chain in a getter like manner, and then wait for the next message to load

## Replies

**mightypenguin** (2021-10-18):

I do not believe that this proposal will reduce fees paid by users.

But if you believe it can reduce ethereum network fees, please describe fewer ideas in your proposal and also be more technical with how you would implement them.

There are too many ideas currently listed in your proposal and not enough details.

---

**PHPJourney** (2021-10-19):

I’m not talking about reducing the network service charge directly from the chain link. It’s just a compensation measure,

Compensation measures include two aspects, which I have mentioned in the article

The first way is to realize compensation through the main chain. In order to stabilize the use of network fees, the main chain can verify the actual use fees when the transaction is packaged on the chain, and then wake up the compensation mechanism for fee conversion. It creates a compensation fee from the “0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000” address to msg.sender

A simple code verification, the actual expansion should be much more complex

```auto
if(block.gasUsed > fixedPoint || block.GasUsed.mul(fixedPoint.div(100))){
super._mint(msg.sender, block.gasUsed.sub(fixedPoint));
// or
super._mint(msg.sender, block.gasUsed.mul(fixedPoint.div(100)));
}
```

The second scheme is to open the service charge field to the block for the contract. At present, the block structure is as follows

```auto
{
blockHash: "0x0",
coinbase: "0x0",
difficulty: "0x0",
gaslimit: "0x0",
number: "0x0",
timestamp: "0x0"
}
```

I think we should add an extra field to the block that actually consumes eth. The contract creator can provide service fee compensation according to this field, which can be selected by the contract creator and sent to msg.sender

According to the actual operation needs of the project party, Ethereum can be returned directly or compensated to the user in token or other forms

**About the second scheme**

I just saw someone *tx.gasPrice* And *gasleft()* Two functions provide support, but how to use them remains to be verified

---

**imkharn** (2021-10-21):

It is already possible for contract creators to partially reimburse gas costs and some do

---

**PHPJourney** (2021-10-22):

How？

Is it through fixed compensation, or can we get the actual gas cost calculation proportional compensation

---

**PHPJourney** (2021-10-22):

I think the best compensation mechanism comes from the production on the chain, and the compensation of the contract creator is only the second scheme.

We should not be kidnapped by miners. The whole network belongs to everyone. If there is a solution to keep the handling fee constant, I believe it is more conducive to development

---

**imkharn** (2021-11-16):

Query either basefee or chainlink gas price to reimburse traders

