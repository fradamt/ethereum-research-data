---
source: magicians
topic_id: 6751
title: "ERC-3722 -- Poster: A ridiculously simple general purpose social media smart contract"
author: auryn
date: "2021-07-31"
category: EIPs
tags: [social-media]
url: https://ethereum-magicians.org/t/erc-3722-poster-a-ridiculously-simple-general-purpose-social-media-smart-contract/6751
views: 8119
likes: 61
posts_count: 81
---

# ERC-3722 -- Poster: A ridiculously simple general purpose social media smart contract

| Author | Auryn Macmillan |
| --- | --- |
| EIP Link | Github |
| Discussions | Various twitter threads |
| Status | Draft |
| Type | Standards Track |
| Category | ERC |
| Created | 2021-07-31 |

#

## Simple Summary

A ridiculously simple general purpose social media smart contract.

It takes a string as a parameter and emits that string, along with msg.sender, as an event. That’s it.

## Motivation

Poster is intended to be used as a base layer for decentralized social media. It can be deployed to the same address (via the singleton factory) on just about any EVM compatible network. Any Ethereum account can make posts to the deployement of Poster on its local network.

## Specification

### Contract

```solidity
contract Poster {
    event NewPost(address indexed account, string content);

    function post(string calldata content) public {
        emit NewPost(msg.send, content);
    }
}
```

### ABI

```json
[
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "user",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "content",
          "type": "string"
        }
      ],
      "name": "NewPost",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "content",
          "type": "string"
        }
      ],
      "name": "post",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
]
```

### Standard json format for Twitter-like posts

```json
{
  "content": [
    {
      "type": "microblog",
      "text": "this is the first post in a thread"
    },
    {
      "type": "microblog",
      "text": "this is the second post in a thread",
      "replyTo": "this[0]"
    },
    {
      "type": "microblog",
      "text": "this is a reply to some other post",
      "replyTo": "some_post_id"
    },
    {
      "type": "microblog",
      "text": "this is a post with an image",
      "image": "ipfs://ipfs_hash"
    },
    {
      "type": "microblog",
      "text": "this post replaces a previously posted post",
      "edit": "some_post_id"
    },
    {
      "type": "delete",
      "target": "some_post_id"
    },
    {
      "type": "like",
      "target": "some_post_id"
    },
    {
      "type": "repost",
      "target": "some_post_id"
    },
    {
      "type": "follow",
      "target": "some_account"
    },
    {
      "type": "unfollow",
      "target": "some_account"
    },
    {
      "type": "block",
      "target": "some_account"
    },
    {
      "type": "report",
      "target": "some_account or some_post_id"
    },    {
      "type": "permissions",
      "account": "",
      "permissions": {
        "post": true,
        "delete": true,
        "like": true,
        "follow": true,
        "block": true,
        "report": true,
        "permissions": true
      }
    },
    {
      "type": "microblog",
      "text": "This is a post from an account with permissions to post on behalf of another account.",
      "from": ""
    }
  ]
}

```

## Implementation

Poster has been deployed at `0x0000000000A84Fe7f5d858c8A22121c975Ff0b42` on multiple networks using the [Singleton Factory](https://eips.ethereum.org/EIPS/eip-2470). If it is not yet deployed on your chosen network, you can use the Singleton Factory to deploy an instance of Poster at the same address on just about any EVM compatible network using these parameters:

> initCode: 0x608060405234801561001057600080fd5b50610189806100206000396000f3fe608060405234801561001057600080fd5b506004361061002b5760003560e01c80638ee93cf314610030575b600080fd5b61004361003e366004610099565b610045565b005b3373ffffffffffffffffffffffffffffffffffffffff167f6babe127d1599cad37c523a2dd29c5d02acd7132a883e378a2d9b42ec75a1fa9838360405161008d929190610106565b60405180910390a25050565b600080602083850312156100ab578182fd5b823567ffffffffffffffff808211156100c2578384fd5b818501915085601f8301126100d5578384fd5b8135818111156100e3578485fd5b8660208285010111156100f4578485fd5b60209290920196919550909350505050565b60006020825282602083015282846040840137818301604090810191909152601f9092017fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe016010191905056fea264697066735822122091369fb6f397ae303a741fb470a163a0384d9152cd15b5887f5f0b68e5a3c8e964736f6c63430008000033
>
>
> salt: 0x51a9566bdb2664f8cb31cd79d50e2c10ea34f765e27bc8e3ff3c60175ad4cb6c

The source code is available in the [Poster contract repo](https://github.com/ETHPoster/contract/blob/master/contracts/Poster.sol).

When verifying on the source code on a block explorer, make sure to set the optimizer to `yes` and the runs to `10000000`.

## Replies

**auryn** (2021-07-31):

Given that this is intended for use as the base layer for decentralized social media, minimizing gas costs is crucial. However, this could come at the cost of increasing infrastructure requirements for services / clients indexing posts. There have been several suggestions on the best balance of gas cost and utility for this contract. They seem to boil down to these options, in order of gas cost from highest to lowest; easiest to hardest to index.

Emit both msg.sender and content

```auto
contract Poster {
    event NewPost(address account, string content);

    function post(string memory content) public {
        emit NewPost(msg.send, content);
    }
}
```

Emit content only

```auto
contract Poster {
    event NewPost(string content);

    function post(string memory content) public {
        emit NewPost(content);
    }
}
```

Emit msg.sender only

```auto
contract Poster {
    event NewPost(address account);

    function post(string memory content) public {
        emit NewPost(msg.send);
    }
}
```

Emit an empty event

```auto
contract Poster {
    event NewPost();

    function post(string memory content) public {
        emit NewPost();
    }
}
```

Emit no event

```auto
contract Poster {
    function post(string memory content) public {}
}
```

---

**dekanbro** (2021-07-31):

Awesome.

I think you could use calldata instead of memory for ‘content’. might save a couple wei



      [github.com/onPoster/contract](https://github.com/onPoster/contract/pull/13)














####


      `master` ← `dekanbro:patch-1`




          opened 01:34PM - 31 Jul 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/a/ae7e58ab05a9b60164085e330cf98f65d2820b35.png)
            dekanbro](https://github.com/dekanbro)



          [+1
            -1](https://github.com/onPoster/contract/pull/13/files)













Also what do you think about adding another field for referencing another index? could be used for ‘retweet/like’

---

**auryn** (2021-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dekanbro/48/4354_2.png) dekanbro:

> Also what do you think about adding another field for referencing another index? could be used for ‘retweet/like’

I think that could be achieved just as well by encoding into the `content` string, see the example json format above.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dekanbro/48/4354_2.png) dekanbro:

> I think you could use calldata instead of memory for ‘content’. might save a couple wei

Are there any trade-offs to using calldata rather than memory?

---

**dekanbro** (2021-07-31):

encoding into the string might save a tiny bit but also could get some misformated entries.

putting it into another field would also allow you to index it.

calldata should be fine because we are not changing the value in any logic.

Will have to do some profiling though to see if it matters.

---

**dekanbro** (2021-07-31):

I guess another option would be to just store a content hash and put it on ipfs or something, but that might defeat the purpose.

---

**auryn** (2021-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dekanbro/48/4354_2.png) dekanbro:

> but also could get some misformated entries

I don’t think adding another field meaningfully reduced the likelihood of malformed information. Someone could just as easily put malformed information into that field.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dekanbro/48/4354_2.png) dekanbro:

> I guess another option would be to just store a content hash

Yeah, this is how [@bonustrack](/u/bonustrack) is thinking about using it.

---

**bonustrack** (2021-07-31):

Yes i prefer with a hash, it makes a light and constant gas cost and remove the content size limit, without a content size limit we can imagine anything like posting large content, use signed messages or batch actions. On Twitter even if the size limit is “just” 280 chars it doesn’t include things like long URLs and metadata. I’d rather use the chain as a trust layer rather than for storage. The tradeoff is just that if you store the data on IPFS it’s not immutable, maybe the question is what threat(s) you want to avoid.

---

**bonustrack** (2021-07-31):

The current design assume the author of the action is the same that broadcasting the tx. If this live in a L2 or another EVM L1 chain it would force users to have fund in their wallet for that chain. It would be more convenient if the design support meta-transaction. This could be done with the idea from Dennison, by broadcasting the content and signature and verify it with a contract function within a subgraph. The issue is just that this would not work for contract signatures (unless the contract is on the same chain than the protocol).

---

**auryn** (2021-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bonustrack/48/4352_2.png) bonustrack:

> It would be more convenient if the design support meta-transaction

I’ve thought more about this. For Snapshot, the real issue is trustless time-stamping and data availability, right?

There’s no reason that votes couldn’t be signed messages just like they are now, the IPFS hash can be posted on-chain by any account. The subgraph would return the timestamp of the block where the IPFS hash was first posted. That way Snapshot can post messages on behalf of users, but users can opt to post their votes themselves and don’t **have** to rely on Snapshot.

---

**bonustrack** (2021-07-31):

Yes, but the subgraph wont help so much cuz we wont be able to valid a message there, we would still need to replay/stream the data offchain to check what is valid and build our own API.

---

**auryn** (2021-07-31):

Assuming that the data is pinned/available, there is no reason that a subgraph couldn’t validate the data. From what I understand, subgraphs that incorporated IPFS data are simply not eligible for indexer rewards.

---

**bonustrack** (2021-07-31):

I mean within the subgraph we can not validate signatures from smart contract, so the only way i see would be to store all messages on the subgraph even if the signature is wrong, and do validation offchain. I can not really store a list of valid messages from the subgraph directly, i could do that only if there is only EOAs signatures.

---

**auryn** (2021-07-31):

Oh, you mean EIP-1271 signatures?

---

**bonustrack** (2021-07-31):

Yes exactly, the problem is only with these signature, but I can’t imagine not having them.

---

**auryn** (2021-08-01):

A response from the graph’s discord server.

> Yes, you can make eth calls. (Note: these are quite “expensive” in terms of indexing performance. Subgraphs with an excessive amount of calls can take a long time to sync)
>
>
> An example call to an ERC-20 contract
> let contract = ERC20Contract.bind(event.address)
> let erc20Symbol = contract.symbol()

So it seems you could call  `isValidSignature()` from within the subgraph.

---

**bonustrack** (2021-08-01):

Yes but it’s only useful if the contract who signed the message is on the same chain where you index data. Which is most of the time not the case.

---

**auryn** (2021-08-01):

Happy to be proven setting, but I’d guess most of the time you’d be indexing mainnet and most of the contacts that would want to sign messages would be deployed to mainnet. No?

So this may not work for every scenario, but it probably covers the majority.

---

**bonustrack** (2021-08-01):

If we publish the data on mainnet the cost to cover the fee would be way too high. Imagine posting 5K messages per day onchain on mainnet. That’s why i assume it must be on another chain, with low gas fee.

---

**auryn** (2021-08-02):

Perhaps you could periodically post an IPFS hash to a json document for a batch of votes?

Users can either submit their vote via your service, in which case it might take a few hours before there are enough votes to justify it going on chain, or they can vote directly by submitting a transaction themselves.

Your service would just need to guarantee that votes would be submitted on-chain before the poll closes.

Maybe if there is less than x amount of time to go, users must submit their own TX. Just so you can’t get blossomed for a user’s cute but being counted if it is submitted late on-chain.

With this setup, you’d have a fixed gas cost for submitting any number of votes each day and still be able to index mainnet.

---

**auryn** (2021-08-02):

[@LefterisJP](/u/lefterisjp), [@Arachnid](/u/arachnid), and [@tjayrush](/u/tjayrush) , I’m keen to hear your feedback on the best of these options.

I’d like to come to a concrete decision on which of these options we should use so we can deploy a final version and start coordinating around one specific instance of it.


*(60 more replies not shown)*
