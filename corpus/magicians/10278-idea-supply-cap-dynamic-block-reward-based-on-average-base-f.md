---
source: magicians
topic_id: 10278
title: "IDEA: Supply cap & dynamic block reward based on average base fees"
author: SoundMoney
date: "2022-08-07"
category: EIPs
tags: [burn, issuance-rate, cap, supply]
url: https://ethereum-magicians.org/t/idea-supply-cap-dynamic-block-reward-based-on-average-base-fees/10278
views: 711
likes: 0
posts_count: 2
---

# IDEA: Supply cap & dynamic block reward based on average base fees

There is a lot of excitement around the “ultra sound money” meme, the idea that Ethereum might become deflationary after the issuance reduction that will coincide with the merge (aka the “triple halvening”). Based on my research, Ethereum will be deflationary if gas prices stay at or below 7 gwei.

While I understand the excitement, I believe that Ethereum would be a better form of money if it had a predictable (net) issuance like Bitcoin. Personally I’d prefer holding a currency with an absolute supply cap over a currency that will probably have a net negative issuance but that does not have an explicit supply cap. In other words, I’d prefer holding an asset that is definitely not inflationary over an asset that will probably be deflationary. The fact that only 21 million Bitcoin can ever exist is an incredibly strong meme. In my opinion, the most sound money would have an issuance of zero, neither negative, nor positive. Moreover, it is difficult to denominate debt in a currency with negative expected issuance.

I propose the following:

- Reduce issuance to 0
- Compensate miners using the current EIP-1559 burns (I’ll refer to them as base fees), in addition to priority fees
- Stabilize the block reward by allocating base fees to a base fee reserve, and assign 1/N of the reserve to the validators of the block

Example:

`N = 1000` (this could also be much larger to smoothen out base fee rewards even more)

Assume base fee reserve is `2000` ETH at block `T`

Block `T+1`:

Total base fees in that block: `2`

Validator base fee rewards: `(2000 + 2)/1000 = 2.002`

New base fee reserve: `2000 + 2 - 2.002 = 1999.998`

Block `T+2`:

Total base fees in that block: `3`

Validator base fee rewards: `(1999.998 + 3)/1000 = 2.003`

New base fee reserve: `1999.998 + 3 - 2.003 = 2000.995`

Block `T+3`:

Total base fees in that block: `0`

Validator base fee rewards: `2000.995/1000 = 2.001`

New base fee reserve: `2000.995 - 2.001 = 1998.994`

I would probably also allocate slashing penalties to honest validators, but I left those out for now to keep the proposal simple.

Would love to hear your thoughts on the general idea of a supply cap and this mechanism.

## Replies

**phi1** (2024-12-27):

I love this because I had a similar thought and wondered if anyone had started this idea yet.

In a nutshell…

- Create a Max Supply of either where we’re at at the moment (roughly 120M Ether) or 126M Ether, which is equal to 6x Bitcoins 21M.
- Reward the validators with all of the fees, so nothing is burnt.

