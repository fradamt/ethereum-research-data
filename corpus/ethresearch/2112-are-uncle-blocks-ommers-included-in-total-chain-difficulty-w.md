---
source: ethresearch
topic_id: 2112
title: Are Uncle Blocks (ommers) included in total chain difficulty / weight?
author: Chrakker
date: "2018-06-01"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/are-uncle-blocks-ommers-included-in-total-chain-difficulty-weight/2112
views: 2519
likes: 1
posts_count: 4
---

# Are Uncle Blocks (ommers) included in total chain difficulty / weight?

Hi.

My [Reddit-Post](https://www.reddit.com/r/ethereum/comments/8n705o/are_uncle_blocks_ommers_included_in_total_chain/)  that did not gain any attention

After some time researching actual papers I came across this [Stackexchange Discussion](https://ethereum.stackexchange.com/questions/13378/what-is-the-exact-longest-chain-rule-implemented-in-the-ethereum-homestead-p) which stated, that (valid and in the main chain included) uncle blocks do not contribute to the weight of the chain in total, which would in term mean that there is no added security through uncle blocks and that a 34% attack-vulnerability is possible.

-> Meaning Ethereum uses only uses **longest chain**, instead of the actual heaviest chain proposed in **GHOST**.

As I read through the yellowpaper and whitepaper, as well as actual implementation code I could not answer this question myself. Can anyone please enlighten me with the backing of a source?

Thank you guys in advance for helping me out, English is not my native tongue so please bear with me.

## Replies

**lithp** (2018-06-01):

I’m very surprised, I’ve also thought Ethereum uses GHOST but after looking through the source code I think you’re right that it doesn’t.

When picking which block to accept geth uses the fork with the highest difficulty. The difficulty of a chain is just the sum of the difficulty of all it’s blocks, and the difficulty of a block is (as of byzantium) [computed with](https://github.com/ethereum/go-ethereum/blob/v1.8.10/consensus/ethash/consensus.go?utf8=%E2%9C%93#L323):

```auto
func calcDifficultyByzantium(time uint64, parent *types.Header) *big.Int {
  // https://github.com/ethereum/EIPs/issues/100.
  // algorithm:
  // diff = (parent_diff +
  //         (parent_diff / 2048 * max((2 if len(parent.uncles) else 1) - ((timestamp - parent.timestamp) // 9), -99))
  //        ) + 2^(periodCount - 2)

  bigTime := new(big.Int).SetUint64(time)
  bigParentTime := new(big.Int).Set(parent.Time)

  // holds intermediate values to make the algo easier to read & audit
  x := new(big.Int)
  y := new(big.Int)

  // (2 if len(parent_uncles) else 1) - (block_timestamp - parent_timestamp) // 9
  x.Sub(bigTime, bigParentTime)
  x.Div(x, big9)
  if parent.UncleHash == types.EmptyUncleHash {
	x.Sub(big1, x)
  } else {
	x.Sub(big2, x)
  }
  // max((2 if len(parent_uncles) else 1) - (block_timestamp - parent_timestamp) // 9, -99)
  if x.Cmp(bigMinus99) < 0 {
	x.Set(bigMinus99)
  }
  // parent_diff + (parent_diff / 2048 * max((2 if len(parent.uncles) else 1) - ((timestamp - parent.timestamp) // 9), -99))
  y.Div(parent.Difficulty, params.DifficultyBoundDivisor)
  x.Mul(y, x)
  x.Add(parent.Difficulty, x)
}
```

This code was added in Byzantium, as [part of EIP100](https://github.com/ethereum/EIPs/issues/100), in [this PR](https://github.com/ethereum/go-ethereum/pull/3632).

It does take the existence of uncles into account, but definitely not in the way described by [the GHOST paper](https://eprint.iacr.org/2013/881.pdf). I also looked at v1.0.0 of geth, it performs similar logic but doesn’t include EIP100, so uncles aren’t taken into account at all.

---

**Chrakker** (2018-06-04):

Hey [@lithp](/u/lithp), thanks for your reply.

I’m stunned how few people actually looked into the way how Ethereum decides to select its valid chain.

Simply because I do not know enough about the sourcecode of geth/parity/eth, I can neither verify nor debunk the made claim of this paper.

Maybe this topic will get someone to answer it eventually.

Sadly, I do not know any other way to make this more visible.

Maybe [@vbuterin](/u/vbuterin) knows a definitive answer to this, as he made the EIP100 in the first place in 2016 ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Best Regards!

---

**dlubarov** (2018-06-12):

[@nickjohnson](/u/nickjohnson)’s answer on ethereum.SE seems authoritative (see his profile); uncles don’t contribute to difficulty. I guess fixing it would require a hard fork since difficulty is declared in Ethereum’s block headers, not derived.

