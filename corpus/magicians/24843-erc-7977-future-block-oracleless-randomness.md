---
source: magicians
topic_id: 24843
title: "ERC-7977: Future-block oracleless randomness"
author: SamWilsn
date: "2025-07-18"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7977-future-block-oracleless-randomness/24843
views: 77
likes: 0
posts_count: 4
---

# ERC-7977: Future-block oracleless randomness

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1094/)














####


      `master` ← `angrymouse:patch-1`




          opened 08:53PM - 16 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/40735471?v=4)
            angrymouse](https://github.com/angrymouse)



          [+92
            -0](https://github.com/ethereum/ERCs/pull/1094/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/1094)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**bbjubjub** (2025-07-23):

Good news: since Prague, one can access the last 8191 block hashes using [EIP-2935: Serve historical block hashes from state](https://eips.ethereum.org/EIPS/eip-2935). That improves liveness a lot.

You that using “entropy slicing” instead of hash functions to aggregate randomness contributions prevents grinding attacks. I am not convinced by that. My mental model is that it doesn’t matter so much what aggregation function you use: the last block producer can see all the previous inputs and as a result they can keep trying values just as easily. It could be that I did not understand your proposal though, so feel free to expand on this.

I think there is an alternative scheme that is more natural and efficient: the execution layer block header includes a field called prevrandao, which already a highly bias resistant source of randomness. Why not have the following protocol:

1. at block height n, a user registers a request. The system keeps track of n.
2. starting from block height n+1 (and until n+8192), anyone can fulfill the request permissionlessly by submitting the preimage of blockhash(n+1). The system extracts prevrandao and uses it as a random seed to fulfill the request.

This requires decoding RLP on chain, which is a little bit annoying and also will be broken occasionally by hard forks, but it requires witholding a block to grind 1 bit, and uses only Ethereum. lmk what you think.

(tagging [@angrymouse](/u/angrymouse) just in case)

---

**angrymouse** (2025-07-24):

> My mental model is that it doesn’t matter so much what aggregation function you use: the last block producer can see all the previous inputs and as a result they can keep trying values just as easily.

[@bbjubjub](/u/bbjubjub)

It’s indeed true, but you missed one important piece in the proposal: It’s *future* blocks that matter, not past. Obviously we can’t access future blockhashes right away, but we can have 2 stages: 1 being entering “randomness request”. Of course individual block producers can still try to grind blockhash, but due to slicing of 1 hash into 32 bytes, grinding would have to involve actually grinding 32 MSBs (most significant bits), so block would have to be withheld for significant time to achieve any meaningful improvement to the randomness (though validators indeed can achieve some marginal improvement, with improvement increasing the more they withhold a block).

But prevrandao idea is also very interesting and might be the better solution, especially combined with the slicing idea (slice prevrandao into 32 byte array to “diversify” MSBs throughout whole prevrandao)

---

**bbjubjub** (2025-07-31):

I am aware that we use future blockhashes. I don’t get from your explanation how entropy slicing specifically fixes grinding but we can also leave that aside since we have RANDAO anyway.

Speaking of, I ended up implementing and deploying a RANDAO-based raffle if you want to take a look:



      [github.com](https://github.com/bbjubjub2494/randao-raffle)




  ![image](https://opengraph.githubassets.com/78ae01457b731b91bcbcb6150d2c377b/bbjubjub2494/randao-raffle)



###



Contribute to bbjubjub2494/randao-raffle development by creating an account on GitHub.

