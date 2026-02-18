---
source: magicians
topic_id: 4497
title: Should there be a standard algorithm for calculating ETH supply?
author: jpitts
date: "2020-08-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/should-there-be-a-standard-algorithm-for-calculating-eth-supply/4497
views: 863
likes: 3
posts_count: 4
---

# Should there be a standard algorithm for calculating ETH supply?

Setting aside the (kind of made-up) controversy, I ask the following questions:

- Should there be a standard algo for calculating ETH supply in clients?
- What would be the best approach to deal with the generation and storage of this measure?
- Who are the users of a supply measurement?
- Are there different kinds of supply which would be useful or relevant?

---

A response by JΞFF to “Crypto’s Weirdest Cognitive Dissonance” on Twitter https://twitter.com/jeffehh/status/1294289745292546049:

> It’s not as dry cut as it may seem. BTC for example allow for a simple algorithm to calculate the current amount of coins. For ethereum it’s slightly different because it allows for ether to be burned (as in it doesn’t exists anymore). Without iterating over all of the accounts
> in the trie you’ll never have a definitive answer. I’m not saying it’s impossible, but it would take an insane amount of time. The other solution is to create a separate log that records changes to the total supply (I.e. block rewards, suicide calls + pre-minted coins). Bear in
> mind that this will only ever be possible when running a full node (I.e. start execution from genesis) and I have no idea what kind of overhead this may cause plus it’s slightly tricky because you’d need to record only SUICIDE ADDRESS
> and SUICIDE . Also I wouldn’t want to mess with the VM unless absolutely necessary and certainly not, imo, for a nice gimmick.

## Replies

**jpitts** (2020-08-16):

Posted by [@tjayrush](/u/tjayrush) on [reddit](https://www.reddit.com/r/ethereum/comments/ialcf0/ethereums_issuance_two_articles_and_some_code_to/):

> Here’s two articles I wrote:
>
>
> Ethereum’s Issuance: blockReward | Coinmonks
>
>
> Ethereum’s Issuance: uncleReward. This the second in a series of two… | by Thomas Jay Rush | Coinmonks | Medium
>
>
> and a code base implementing the discussion in the articles:
>
>
> https://github.com/Great-Hill-Corporation/trueblocks-core/blob/develop/src/other/issuance/README.md
>
>
> I’d love feedback on them if anyone’s interested.

---

**CryptoBlockchainTech** (2020-08-16):

Confusing article, can’t tell which is original and which is new code. You talk about how confusing the yellow paper is, but when you write the article it is confusing as well as to which lines of code you are wanting to change. Maybe you can put them side by side?

---

**jpitts** (2020-08-19):

Jordan Last has created scripts for the “total issued ETH” methodology.



      [github.com](https://github.com/lastmjs/eth-total-supply#methodology)




  ![image](https://opengraph.githubassets.com/9657486ab6da641fae94a35d0c94a471/lastmjs/eth-total-supply#methodology)



###



Information and some implementation for calculating the total supply of ETH










Twitter discussion:



      [twitter.com](https://twitter.com/lastmjs/status/1295913937192415232)



    ![image](https://pbs.twimg.com/profile_images/1905052599348494336/04wJ-luR_200x200.jpg)

####

[@lastmjs](https://twitter.com/lastmjs/status/1295913937192415232)

  1/ #supplygate

I can say beyond reasonable doubt, that the total amount of ETH issued up to and including block 9193265 (the last block in 2019) is 109,094,014.21823.

Three independent scripts attest to this number: https://t.co/SK0CWhwLGI

  https://twitter.com/lastmjs/status/1295913937192415232

