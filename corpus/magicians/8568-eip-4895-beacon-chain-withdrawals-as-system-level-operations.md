---
source: magicians
topic_id: 8568
title: "EIP-4895: Beacon chain withdrawals as system-level operations"
author: ralexstokes
date: "2022-03-10"
category: EIPs > EIPs core
tags: [shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-4895-beacon-chain-withdrawals-as-system-level-operations/8568
views: 11258
likes: 13
posts_count: 52
---

# EIP-4895: Beacon chain withdrawals as system-level operations

Discussions for [Beacon chain withdrawals as system-level operations by ralexstokes · Pull Request #4895 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4895) follow:

## Replies

**jochem-brouwer** (2022-03-21):

On execution layer, the ETH comes “out of thin air” I assume? We can’t withdraw from the ETH2 deposit contract since if a lot of addresses withdraw we can get negative balance?

---

**ralexstokes** (2022-03-21):

Yeah, this EIP specifies an unconditional balance increase with no source, just like how the coinbase reward works.

While it could be nice from an accounting standpoint to try to match withdrawals to deposits in the deposit contract, we would run into an issue as we (likely) end up with more ETH on the beacon chain than started in the deposit contract (due to validation rewards). So you could end up with some kind of negative balance in the deposit contract in the limit. I’d also push back against addressing the deposit contract balance in this EIP to keep the scope smaller.

I know [@axic](/u/axic) has thought some about the accounting here and he may have more to say.

---

**OisinKyne** (2022-03-24):

Hey all, I have an ask about this specific requirement:

> The withdrawals in a block are processed after any user-level transactions are applied.

Is there a definitive reason why these withdrawals need to be processed after the normal transactions?

The reason I highlight it is cross-slot MEV. There are already serious concerns about BLS withdrawal keys that have been compromised, and best-effort out of protocol methods to mitigate this are being [worked on](https://eips.ethereum.org/EIPS/eip-4736), specifically focusing on the [0x00 to 0x01 change](https://github.com/ethereum/consensus-specs/pull/2855) message feature being added.

My concern relates to an EVM EOA being compromised, which is probably a smaller impact than the number of BLS keys that have been compromised, but still should be considered all the same.

If an 0x01 recipient is compromised, and two actors hold the private key. They can be expected to bribe block producers for inclusion to sweep the rewards to a secure address. This bribe could theoretically approach 100% of the exited validator rewards, which at 16 exits per block could reach 512+ ether.

My concern is, if we process this balance change after all of the regular transactions, the funds cannot be swept until the next block, and could leave 500+ ether in limbo, which I fear could encourage bad behaviour like DoS’ing block producers.

However, if we process these withdrawals before we process the standard transactions, the funds can be swept the same block that they become accessible. I think this could be cleaner, and might reduce the stress that would be put on the network/BPs versus spreading this unfortunate situation across multiple slots.

What do people think?

---

**ralexstokes** (2022-03-24):

Hi [@OisinKyne](/u/oisinkyne), this is an interesting scenario… there is currently not any principled reason to choose processing withdrawals *before* vs. *after* the other transactions in a block and a strong argument one way or the other could change the route we go here.

Prior versions of this work had the withdrawals *before* and I wrote 4895 to say *after* as it felt a bit more right; but, only for keeping w/ the symmetry of the block subsidy paid to the block’s coinbase which is applied *after* the other transactions. It also seems to make MEV searching a bit easier as you don’t also need to bother with withdrawal simulation on top of all the other things you want to do when searching (as you can just use the prior block’s post-state as your starting state, without having to get some intermediate state of post-state + withdrawals.) Now, I definitely don’t think we should cater to searchers if we can think of a good argument one way or the other, but I do personally find weight to the “symmetry” argument, if only to reduce the complexity of what you have to remember when reasoning about the protocol.

This all being said, I have some questions about your specific scenario:

> However, if we process these withdrawals before we process the standard transactions, the funds can be swept the same block that they become accessible.

If I can DoS proposers to capture the ether “in limbo” via *after* execution (by waiting until we get to a “malicious” proposer I control), can’t I also DoS them if we move to *before* execution and wait until we get to the same proposer under my control?

It seems that this decision doesn’t really change the outcome here, so I would still argue for *after* execution via the symmetry arguments I made at the start.

Do you see it differently?

---

**OisinKyne** (2022-03-24):

Thanks for a quick response ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

So I do agree that there can be DoSing in both scenarios, but if balances are updated before, I believe the situation can be over and done with in one slot. If its after, it is at least two slots.

As for whether either approach would result in a meaningfully different outcome, I have no idea, I also agree that at the end is more ‘natural’ for a tidy up system operation, and feels sensible.

The reason I am averse to spreading MEV across slots is because I have a fear that that can be centralising. Obviously in this case I hope what I am describing is an extremely rare phenomenon, and won’t ever meaningfully impact returns, but previously I have been concerned that contiguous block production being in the hands of one party can allow them to cause harm to systems that were built with assumptions from the PoW era, where no one could reliably control consecutive blocks. (Uniswap TWAPs being the obvious target imo)

I wrote [this blog post](https://blog.obol.tech/p/19797f97-18dd-4dbb-bfdd-0151f2099f7c/#the-stakes-are-raised-with-proof-of-stake) nearly a year ago that I never ended up publishing, and it is not 100% accurate anymore considering 0x01 and PBS, but I guess I just want to highlight where my concern is coming from and why I am chewing on whether withdrawal processing before or after normal transactions could mitigate or exacerbate the situation.

---

**ralexstokes** (2022-03-25):

> previously I have been concerned that contiguous block production being in the hands of one party can allow them to cause harm to systems that were built with assumptions from the PoW era

I think with the existence of mining pools, the situation here is not that different moving from PoW to PoS and in fact may improve as the barrier to entry as a “solo staker” is much  lower than being a “solo miner”.

---

**MicahZoltu** (2022-04-02):

Usually we separate consensus change EIPs from networking change EIPs.  In this case, the consensus change is the addition of the withdrawal root to the header.  The networking change is the addition of the withdraw data to the block body.

---

**MicahZoltu** (2022-04-02):

This EIP shouldn’t reference EIPs that won’t make it to final, and the motivation isn’t the right section for describing alternative options.

In the motivation, remove the references to “alternative EIPs” and instead in the rationale very briefly describe the other options (a sentence or two is usually fine) and why they weren’t chosen.

---

**MicahZoltu** (2022-04-02):

Recommend removing the reference to EIP-3675 and the empty ommers list.  This EIP could be implemented even if the ommers list isn’t empty, so there is no dependency and if we change our minds on emptying the ommers list for some reason then we would want this EIP to not suddenly become incorrect.

Also, it is unnecessary information to readers of this EIP and shorter is better where possible.

---

**poojaranjan** (2022-04-12):

EIP-4895: Beacon chain push withdrawals as operations with [@ralexstokes](/u/ralexstokes)

  [![image](https://i.ytimg.com/vi/CcL9RJBljUs/hqdefault.jpg)](https://www.youtube.com/watch?v=CcL9RJBljUs)

---

**bbuddha** (2022-06-03):

Are there any resources on how the withdrawal flow works and the plans to trigger withdrawals from contracts?

In this model, if contracts want to do accounting based on withdrawals, are they expected do delayed accounting by proving withdrawals against the withdrawal root of a previous block header?

---

**jochem-brouwer** (2022-08-31):

I have some questions and remarks regarding this EIP, especially now it is CFI’d for Shanghai.

> Beginning with the execution timestamp FORK_TIMESTAMP

Should I read this as `>` or `>=`?

```auto
def compute_trie_root_from_indexed_data(data):
    trie = Trie.from([(i, obj) for i, obj in enumerate(data)])
    return trie.root

block_header.withdrawals_root = compute_trie_root_from_indexed_data(block.withdrawals)
```

For clarification, is this a trie where the keys are hashed, or not?

```auto
block_header_rlp = RLP([
  parent_hash,
  ommers_hash,
  coinbase,
  state_root,
  txs_root,
  receipts_root,
  bloom,
  difficulty,
  number,
  gas_limit,
  gas_used,
  time,
  extradata,
  mix_hash,
  nonce,
  withdrawals_root,
])
```

Base fee field is missing.

> The withdrawals in a block are processed after any user-level transactions are applied.

~~What if there’s a `SELFDESTRUCT`? Does the clearing of the destructed account happen before or after processing the withdrawals? (So: if it is after the withdrawals, one could blackhole the withdrawn ETH)~~ → I just realized that selfdestruct clearing happens after each tx, so this is part of the spec already.

---

**ralexstokes** (2022-08-31):

> Should I read this as > or >= ?

`>=`

> For clarification, is this a trie where the keys are hashed, or not?

as written I’d say there is no additional hashing layer, I don’t see a reason to add it; e.g. the transactions trie doesn’t have hashing like the main state trie

> Base fee field is missing.

nice catch, I’ll make a note to update this

---

**jochem-brouwer** (2022-08-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> as written I’d say there is no additional hashing layer, I don’t see a reason to add it; e.g. the transactions trie doesn’t have hashing like the main state trie

I completely agree, but it would make the EIP more self contained (also with the timestamp clearly defined as `>=`)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> nice catch, I’ll make a note to update this

Great ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12) Thanks for the quick reply!

---

**MicahZoltu** (2022-09-01):

`mixhash` should also be changed to `prevRandao` I think, since this will almost certainly land after [EIP-4399: Supplant DIFFICULTY opcode with PREVRANDAO](https://eips.ethereum.org/EIPS/eip-4399).

---

**MicahZoltu** (2022-09-19):

> NOTE: refer to EIP-3675 as some of the values in the header RLP have fixed values that MUST* be used.

Can we get this line removed and instead just have the block header contain the fixed values?  This PR was written prior to The Merge, so I can appreciate why it was this way originally, but I think things would be more clear if we just put the fixed values inline.

---

**ralexstokes** (2022-09-19):

agree, I intend to address the feedback in this thread some time this week

---

**ralexstokes** (2022-09-20):

I have addressed all of the feedback to date in this PR:

https://github.com/ethereum/EIPs/pull/5697

---

**jochem-brouwer** (2022-10-10):

I have a question regarding this EIP.

The `index` items of the withdrawals are “monotonically increasing” and “uniquely identify each withdrawal”. The `index` is of type `uint64`.

Is this “monotonically increasing” verified at block-level or does it uniquely identify each withdrawal? I.e. if block `A` has withdrawals with indices [0,1,2] and block `B` (`B.number > A.number`) has [0,1] as indices, is this invalid? So should `B` at least start with index 3?

The “monotonically increasing”  also sounds a bit problematic to me if the monotonically increasing is enforced system-wide (so spanning multiple blocks), I am not sure if this is enforced at CL, but what if I create a valid block with a withdrawal ID of `uint64.maxNumber - 1` and the next block should have a withdrawal where the index is also larger than the last one, then it will not fit into the `uint64` anymore?

---

**ralexstokes** (2022-10-10):

the `index` starts at `0` and increments by `1` for each withdrawal.

the withdrawals are automatically made at the consensus layer where the logic to do this is enforced.

withdrawal indices will never duplicate – so you couldn’t get into the `[0,1,2]` then `[0,1]` situation you describe.

you have no (direct) control over the index so we will never see `uint64.maxNumber - 1`


*(31 more replies not shown)*
