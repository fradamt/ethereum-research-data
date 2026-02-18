---
source: magicians
topic_id: 13327
title: The ERC-XXXX standard for cross chain compatibility
author: ATD007
date: "2023-03-15"
category: EIPs
tags: [erc, erc-20, cross-chain, bridge]
url: https://ethereum-magicians.org/t/the-erc-xxxx-standard-for-cross-chain-compatibility/13327
views: 2772
likes: 14
posts_count: 13
---

# The ERC-XXXX standard for cross chain compatibility

Recently I bought some tokens for a new project on polygon. This project essentially deployed it’s token contract with the same address across polygon, ethereum, bsc and avalanche. So in my ignorance I just assumed that I could simply “bridge” my polygon tokens over to ethereum by pressing a few buttons. However, I soon realized that the process of bridging involves:

1. Locking up my tokens in a polygon smart contract
2. Receiving a “wrapped” version of those tokens on ethereum (which is basically tokens made out of thin air to represent a fictitious 1-to-1 correlation to the original ones since they are locked up on polygon) and then
3. Find a liquidity pool in Ethereum where I can “unwrap them”, ie, swap them for the original token that I wanted on the Ethereum chain! The people on the other end of this trade should be able to unwrap them on polygon, ie, give them back to the smart contract of the wrapping service on ethereum and then receive the locked up tokens from the smart contract of the same wrapping service on polygon.

However since these tokens belonged to a brand new project there was no liquidity on Ethereum for the wrapped version and in the process of wrapping and unwrapping them I lost $40! Also to my surprise I was hit with the realization that the total supply of this token is actually 4X its total supply since its listed in 4 blockchains and the creators just assume different ecosystems to emerge between them which has already resulted in a great disparity between the price of the tokens across it’s 4 chains. Also, what’s there to stop me from publishing their token contract with the same address in a 5th EVM compatible blockchain and then secretly owning 90% of it’s total supply there?

As such, an elegant solution would be to have a feature in the ERC-20 contract itself where I could lock my tokens on Polygon, receive a deposit hash, move over to Ethereum and then use the hash to mint these tokens out on the new blockchain. In this way cross chain operability will become seamless in addition to other benefits like a true total supply, easy of arbitrage between chains and of course more integrity of the project as rouge actors cannot go about deploying the same token contracts on different chains to perform a rug-pull on the participants of that chain.

## Replies

**xtools-at** (2023-03-16):

i like the idea, any thoughts on how you could accomplish something like that? i might not see the big picture but i think a smart contract alone is not enough, you’d need a bridge or oracles to transfer the “deposit hash” from one chain to another

---

**ATD007** (2023-03-16):

Given that the smart contract has the same address and total supply across chains I think there is a possibility for it.

Let’s assume a contract with a total supply of 10,000 has been deployed onto Ethereum and Polygon with the same address. Now the ERC-21 standard will require the number of instances to be specified before cross chain deployment. So in our example this will be 2 so that both the contracts know that the *true total supply* is 20,000. Now lets assume a full mint in both ecosystems. During each mint the tokens can be identified uniquely as SA+1, SA+2, SA+3… SA+n, where SA is the smart contract address and n is the total supply.

Now post mint let’s say a user in Polygon want’s to bridge their tokens to Ethereum. They first lock their tokens in Polygon, at which point their tokens get represented as the collection (SA+x, SA+y, SA+z… , where x, y & z are arbitrary numbers). The first deposit and the users wallet address then get  fed into a hash function to get an output. This output and the second deposit get fed into the same function to get a new output until we arrive at the final hash.

Now the user can feed this hash over to the entereum contract, which since it’s running the same hash function can run the problem in reverse and get the unique token id’s and the original depositors address. It then mints these new tokens with the id’s SA+10000+x, SA+10000+y, SA+10000+z… from it’s reserve pool.

Then if the user wants to redeem their polygon tokens they can perform the same bridging on Ethereum and feed the hash over to Polygon which when it observes a reserve token id releases the locked tokens instead of minting new ones.

Let me know your thoughts on this ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**bawtman** (2023-03-16):

[@ATD007](/u/atd007) This is a great idea I feel, across two chains. If a third chain is added would there be any potential for a double spend situation? Not sure I would want to leave this up to the user, but I tend to think of the worst possible scenario.

---

**xtools-at** (2023-03-16):

could you do a draft of the deposit and withdrawal functions in solidity? it could help identifying gaps in the concept

---

**ATD007** (2023-03-17):

Hey [@bawtman](/u/bawtman), yup I noticed the double spend issue after publishing my answer yesterday so thanks for pointing it out.

One solution that I could think of would be to have an {chain:nonce} dictionary where each chain is assigned a unique id. If the smart contract can somehow read the chain id directly then we can bypass this step. Then in the token identifier function we can add the nonce in to identify each token as SA+n+1, SA+n+2 … SA+n+T, where T is the total supply, after which we can also factor in the nonce when minting from the reserve supply of each contract, then the algorithm can run as specified.

Let me know what you think? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ATD007** (2023-03-17):

Hmm, well my solidity isn’t really all that strong just yet so I was hoping to get some help from this forum ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

As far as I can tell I will essentially need to code in the following functions into the already existing ERC-20 contract code:

1. The reserve tokens function that accounts for the true total supply across all chain deployments
2. The deposit function that goes over the entire chain hashing sequence
3. The redeem function that takes in a hash and does the data unwrapping
4. The withdraw function that allows the user to reclaim their previously deposited tokens on one chain after they have deposited their newly minted tokens on the other chain.

I just haven’t yet found the time to dive deep into encoding them so any leads/help will be greatly appreciated ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**bawtman** (2023-03-18):

Hi @[ATD007](https://ethereum-magicians.org/u/ATD007), While I still love this idea I have a lot of skepticism about the safty of it I am sorry to say. First being that cross chain bridges are a favorite target for hackers. Last year alone in February Wormhole cross chain service was hit for about $320 million, and in October Binance lost $570 million from such attacks. Chainalyis has estimated that 69% of cryptocurrency funds stolen in 2022 have been attributed to attacks on cross-chain bridges. Without a service in place, as much as I hate to say it could be an open target. There are several services that bridge from chain to chain as listed in the link at the bottom. Fiat bridging may actually be the safest and possibly the least expensive, depending on what service you use in moving your funds. I would love to see a contract for both ends of this as it may change my mind. I still have some thought’s running through my mind on a way to accomplish this. I will leave that for another time. Here is the link to the info I cited.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/6/61af8433f8669ac081cb990b3c90bc1c30756c85.png)

      [WhatIs](https://www.techtarget.com/whatis/feature/The-best-cross-chain-bridges)



    ![](https://www.techtarget.com/rms/onlineimages/money_g932729776.jpg)

###



Here are some of the best cross-chain bridges people can use to swap one cryptocurrency for another.

---

**ATD007** (2023-03-18):

Hey [@bawtman](/u/bawtman) thanks for sharing the article, it was a fascinating read.

After digging deeper into the attacks I can see that the Wormhole one was caused by the attacker tricking the guardian system for this protocol while the Binance hack was cause by the attacker tricking the relay system of the BSC. In both cases, and I’m sure that in all of the 69% cases of cross-chain bridge hacks, the attacker exploited one of the moving parts with which they bought down the entire system.

The place where my approach is different is that I have just one moving part. It’s just the same smart contract deployed across chains and the bridging is done based on the mathematical soundness (unhackability) of the hash function.

Of course, there can be exploits if there are vulnerabilities present within the underlying code that makes up the EVM and therefore Solidity, but given a fair playing field I think we have a chance at being able to pull this off using a standard ERC-20 contract with a few extra functions.

You mentioned that you had a few thoughts running in your mind regarding how to accomplish this, I would love to hear them because you never know what might spark the breakthrough for someone else ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**bawtman** (2023-03-19):

Hi [@ATD007](/u/atd007), The article was more or less showing how much of a target this could be. If this is possible it will be great. It could save a bunch of money in fee’s and make a transfer truly decentralized. I do agree that a mathematical formula could be the key, but every road I go down ends in a roadblock.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atd007/48/8881_2.png) ATD007:

> Now the user can feed this hash over to the entereum contract, which since it’s running the same hash function can run the problem in reverse and get the unique token id’s and the original depositors address. It then mints these new tokens with the id’s SA+10000+x, SA+10000+y, SA+10000+z… from it’s reserve pool.

I am not sure reversing a hash is plausible, It is the essence of what a hash is and why it is so secure. If you have a contract that was able to accomplish this, then anybody would be able to replicate it. Also depending on the formula it may cost a very large amount if fee’s for processing. While I still feel it would be unique and useful I am not sure it’s possible. Maybe one of the Cypherpunks here would have a a method but I am at a loss for a way to safely preform this.

---

**abcoathup** (2023-03-19):

Before you get too far using the name ERC21.  EIP editors assign an EIP number (generally the PR number, but the decision is with the editors) (from: [EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1#eip-numbers)).  The latest PR is 6726 so likely to be higher than that.

Suggest reading: [Guidelines on How to write EIP. Do’s and Don’ts including examples | by Anett | The Fellowship of Ethereum Magicians | Medium](https://medium.com/ethereum-magicians/guide-on-how-to-write-perfect-eip-70488ad70bec)

---

**ATD007** (2023-03-21):

Hey [@bawtman](/u/bawtman) thank you for your comment and warnings, they really made me think deeply about this topic. However, my intuition is telling me that that an optimum solution does exist using hash and keyed-hash functions primarily because the problem boils down to:

1. Proving that a user has deposited x number of core-mint tokens in the y instance of the contract against which reserve-mints can be issued.
2. Proving that a user has deposited a number of reserve-mint tokens in the b instance of the contract against which core-mints can be unlocked.

Both these problems are “trust-issues”, and the hash/key-hash functions were made to eliminate trust from the equation.

I’m currently working on the code to test this hypothesis and would love to hear your as well as the communities feedback on it once it’s done ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ATD007** (2023-03-21):

Hey [@abcoathup](/u/abcoathup) thank you for the heads up and the links! I have updated the heading of this thread to reflect this discussion/proposal more accurately ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

