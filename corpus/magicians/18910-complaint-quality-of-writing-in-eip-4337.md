---
source: magicians
topic_id: 18910
title: Complaint - quality of writing in EIP-4337
author: luke
date: "2024-02-23"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/complaint-quality-of-writing-in-eip-4337/18910
views: 790
likes: 6
posts_count: 6
---

# Complaint - quality of writing in EIP-4337

Hello all,

Firstly, I’m sorry that my first engagement with the community is to whinge. However, I sincerely feel that my moaning is in the very best interests of Ethereum. It’s also possible that I’m wrong or shouldn’t be poking around this deep.

As part of learning Ethereum, I’ve been picking the most well known EIPs, reading them and making notes. All has been fine until I reached 4337.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4337)





###



An account abstraction proposal which completely avoids consensus-layer protocol changes, instead relying on higher-layer infrastructure.










The quality of writing is very poor, to the point of me either failing to comprehend large parts of it, or making guesses in my notes. I’m new to Ethereum but I have fully read and made notes on Mastering Ethereum, O’Reilly, and I’ve been coding almost daily for 39 years.

This particular EIP is long and complicated, and so I suspect the collaborators are a) time-poor b) experts with tacit knowledge who subconsciously infer what’s meant by vague terms (Curse of Knowledge) c) are being extemporaneous, i.e. working it out, as they type.

I won’t list all its problems but there are faults in almost every sentence, and concepts and terms are mixed or ill-defined, not meticulously stuck to.

At points, there aren’t even capital letters starting some of the sentences, which demonstrates extreme lack of care or time. Even the code has sloppy use of whitespace.

When someone saves a minute in writing clearly, they steal that minute from thousands of other readers. Harsh, but true.

I can’t fix it or suggest edits or rewrite it for other’s benefit because I can’t grasp what it’s saying with any confidence.

Anyway, I’m drawing attention to this, at risk of looking rude and demanding, because I strongly believe that adoption follows documentation and developer experience (think of Cuda vs. ROCm in AI and its impact on Nvidia’s sales).

The ultimate worry is that those companies that make something hard, much simpler for the early majority, tend to become tomorrows big centres of influence and control, which I think runs contra to Ethereum’s values. In a sense, this is how regulatory capture works.

In other words, documentation quality is critical to decentralisation.

Thank you

Luke Puplett

## Replies

**abcoathup** (2024-02-23):

ERC-4337 is still draft.  You could make suggestions to improve the language, reach out to some of the authors.

---

**luke** (2024-02-23):

Thanks for your quick reply.

**Can I mention the authors or will they get notified if I tag my message properly? Should I retag this one?**

-

I got the impression that AA was done, to the extent that it’s being implemented by all kinds of companies providing APIs and stuff, and it’s labeled “Standards Track: ERC”.

To be honest, I don’t even know where to start with this one. It’s so long and so badly written, it’d take me a week to compile all the issues and I’d just upset everyone.

I feel like this one is a lost cause, but in general, would everyone please raise their expectations from each other around quality, think about Curse of Knowledge, and the importance of documentation on democracy and fair participation.

Much appreciated.

---

**abcoathup** (2024-02-25):

The ERC is still in draft.

You can offer to help the authors improve the language, which may be ignored or appreciated.  Try DMing them on social media.

---

**ZWJKFLC** (2024-02-26):

This is the simplest EIP-4337, and the rest are in-depth supplements.

```plaintext
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/access/Ownable.sol";
contract MyContract is Ownable {
    constructor(address initialOwner) Ownable(initialOwner) {}
    function all(address add,bytes calldata a,uint256 _gas,uint256 _value)payable public {
        unchecked {
            (bool success,) = add.call{gas: _gas,value: _value}(a);
            require(success,"error call");
        }
    }
}
```

---

**robertgenito** (2024-02-27):

I hope you look at the ERC I will soon post for discussion…definitely want to hear people’s thoughts and constructive criticism!  Good post, Luke, and good point.  It’s beneficial to all incoming developers–and there will be many of them in the smart contract ecosystem!–for even ERCs to be written clearly and understood.  Why?  Because it’s the application layer; the layer that most incoming smart contract developers will want to know about.

