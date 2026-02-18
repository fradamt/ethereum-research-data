---
source: ethresearch
topic_id: 5455
title: Solidity AI demo
author: kladkogex
date: "2019-05-15"
category: Data Science
tags: []
url: https://ethresear.ch/t/solidity-ai-demo/5455
views: 6259
likes: 17
posts_count: 16
---

# Solidity AI demo

A demo of first-ever AI-enabled in a Solidity smart contract running on ETH side chain.  An image is being uploaded into a decentralized social network running on a blockchain.  Once the image is uploaded into the blockchain file storage, a precompiled SmartContract analyzes it using Resnet50 neural network, and rejects it if it contains an image of a cat.

## Replies

**rumkin** (2019-05-17):

Exciting. Wondering how much gas was spent by the call? And what size the image has?

---

**Econymous** (2019-05-17):

Very promising.  I have the same questions,  how expensive is this operation?

---

**wanghs09** (2019-05-31):

seems one way to filter out illegal information, but too expensive I guess

---

**kladkogex** (2019-06-04):

Thank you guys - the operation is not expensive. It is the same order of magnitude as crypto algorithms (e.g. ECDSA signature verification) . We did not decide on the gas value yet, but we are able to do several hundred AI predictions per second in EVM …

---

**wanghs09** (2019-06-10):

interesting, what about the transaction size and parameter size for the AI model?

---

**burrrata** (2019-06-15):

This is awesome! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

What kind of sidechain are you using?

---

**demisstif** (2019-06-17):

Interesting:laughing:，want more detail

---

**kashishkhullar** (2019-06-23):

Is the image processing off chain? It certainly cannot be on chain. Did you use a their party server to delegate the expensive computation?

---

**kladkogex** (2019-08-14):

Yep - in our case image processing is precompiled smartcontract on chain.

We are using SKALE chains.

https://github.com/skalenetwork/skaled

---

**nollied** (2022-04-02):

where are the inferences displayed? i couldn’t tell from the video, i only saw how the image was uploaded.

also, could you share the code you wrote for this?

---

**sametcodes** (2022-04-17):

Is the code available or could you mention any open-source projects that demonstrate a similar idea? I would like to read and learn more.

---

**wangtsiao** (2022-04-19):

Awesome! It’s hard to believe that this is an idea which has been realized in 2019.

since I’m newbie to SKALE sidechain, so some questions here.

- According to the large number of user requests in the past, we need to update the recognition model to improve the accuracy. Whether the model can still be updated after the contract is deployed?
- Is SKALE sidechain based on zero-knowledge proofs and how does it achieve correctness?

---

**iswarm** (2022-05-04):

Running precompiled some AI inference is Very interesting.  Is there any advancement? and what is your idea?

---

**christiankesslers** (2022-05-24):

I could see this being useful to prevent the verification and injection of any known malicious smart contract Solidity action. Do away with being able to hide operations, set others’ permissions by blocking such things as msg.sender == newOwner and could also help limit or learn if the actin is being done too many times and I’d imagine built in wad calculation could work.

Just some thoughts.

---

**hemedex.eth** (2022-06-16):

Would also love to see the relevant code open sourced. However, especially interested in optimize performance for using AI model in smart contract.

