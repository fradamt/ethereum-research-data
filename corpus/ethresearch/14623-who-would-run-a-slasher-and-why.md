---
source: ethresearch
topic_id: 14623
title: Who would run a slasher and why?
author: builderbenny
date: "2023-01-16"
category: Security
tags: []
url: https://ethresear.ch/t/who-would-run-a-slasher-and-why/14623
views: 2179
likes: 1
posts_count: 3
---

# Who would run a slasher and why?

As far as I can see there is no incentive to run a slasher; i.e., whistleblower_index is set to ‘none’ [here](https://github.com/ethereum/consensus-specs/blob/496e1d86c9e251a1b1d5b0eb785b0381ce553751/specs/altair/beacon-chain.md#modified-slash_validator) - hasn’t changed since Altair as far as i can see.

That said, slashable offences have been caught (looks like about 224 so far - [Validator Slashings - Open Source Ethereum Blockchain Explorer - beaconcha.in - 2023](https://beaconcha.in/validators/slashings)) - so folks are running slashers in spite of this (*assuming slashers are needed to catch slashable offences, but I could be wrong here).

So my best guess is that some entities are performing this as a kind of public service.

Wondering if there is a way to determine how many slashers are being run and if there has been any thinking done on this, i.e., what happens if everyone decided to stop running them?

## Replies

**seunlanlege** (2023-01-22):

I have a few thoughts on this, as the security of bridges will also eventually rest on the slashing protocol.

Slashers shouldn’t be limited to the active validator set allowing anyone report a slashable offence.

Slashable offence reports should also be rewarded thereby strengthening the security of cross-domain bridges

See linked post: [Byzantine Fault Tolerant Bridges](https://ethresear.ch/t/byzantine-fault-tolerant-bridges/13841)

---

**builderbenny** (2023-02-17):

I am not sure that running a slasher is limited to validators - I think all you need is a Beacon node (see [here](https://docs.prylabs.network/docs/prysm-usage/slasher) for instance).

That said, the computational resources are intensive.

As of right now the proposer that includes the evidence of a slashable offence gets the whistleblower rewards, see:

whistleblower_index = proposer_index

([here](https://github.com/ethereum/consensus-specs/blob/270a66e36cc13787495d133ffcc909b377beefb5/specs/bellatrix/beacon-chain.md#modified-slash_validator)).

But even if the whistleblower did receive the rewards, there are two other key problems.

Given the relatively low frequency of slashable offences committed (so far) and the low payout - looks like about 0.05 to 0.07 ETH (depending on the slashed validator’s effective balance) - running a slasher does not appear to be economically feasible. Note also that that reward is, in theory, meant to be split between the whistleblower and the proposer (even though current implementations give 100% of that reward to the proposer).

The other, arguably, more important problem is that reports of slashable offences can be stolen as soon as they are propagated (as far as I understand). Some implementations (like Prysm’s) allow you to disable the propagation. I guess the idea could be that if you run a slasher and validator - you would disable propagation and send the slashable offence to your own validator when it is chosen to propose a block.

Not sure what the solution is here. From what I can see (slash_validator - in Bellatrix specs - link above), the amount slashed is “burnt”- maybe taking a higher proportion of this and giving it to whistleblower would help. That said, I don’t think that’s enough on its own to make running a slasher economical.

Things seem to be working fine right now, but if this were something to be remedied in the future, maybe it would be worth considering minting new ETH to compensate folks running slashers. Again, given the low frequency of slashable offences to date, it would require a very small amount of ETH (on a network-wide basis) be minted to make running a slasher economical.

Perhaps a hybrid approach would work best - set a threshold for whistleblower rewards to make running a slasher economical. The whistleblower would receive a higher proportion of the slashed rewards (including a portion of the proportional slashing penalty), but if the total reward to the whistleblower is below the threshold then an additional amount of ETH would be minted to reach the threshold. This would ensure that the whistleblower is adequately compensated and, in the case of a large attack on the network, where the rewards are more than sufficient to meet the threshold, no new ETH would need to be minted.

