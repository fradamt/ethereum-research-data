---
source: ethresearch
topic_id: 7341
title: ETH2 commitee selection
author: kladkogex
date: "2020-04-30"
category: The Merge
tags: []
url: https://ethresear.ch/t/eth2-commitee-selection/7341
views: 1219
likes: 0
posts_count: 1
---

# ETH2 commitee selection

From reading ETH2 spec:

Can ETH committee selection fork leading to multiple concurrent committees operating? Or there is a protection mechanism against it?



      [github.com/ethereum/consensus-specs](https://github.com/ethereum/consensus-specs/issues/1776)












####



        opened 08:34AM - 30 Apr 20 UTC



          closed 01:16PM - 11 Dec 23 UTC



        [![](https://ethresear.ch/uploads/default/original/3X/8/d/8d78f8308060b15b90d9e0b771da1edca0d92c68.jpeg)
          kladkogex](https://github.com/kladkogex)










_High-level description of the bug [1 sentence]_

ETH committee selection can […]()fork leading to multiple concurrent committees operating, this needs to be at least addressed and explained in the spec.

_Attack scenario_

In ETH2 committees are selected based on the current state of the chain, which in turn depends
on the winning branch of the block tree.

The spec seems to not address the fact that since potentially Casper may not finalize for a long time, the LMD GHOST fork rule can lead to long-time reoderings in the chain.

An attacker can potentially reorder the chain, say, one day back in the past, totally changing committee  assignments.  The committee members that thought they were  validating will be invalidated.

It then seems  that new true committees will not be able to operate, since no-one can not respond to changes happening back in time, unless there is a time machine invented.

It may be that the spec actually does allow multiple alternative committees operating at the same time, that correspond to alternate branches.  If yes, this needs to be explained in the spec. The way the spec currently is written it seems to state that there is a unique committee at each moment in time, which introduces confusion.

As I already mentioned, it may be a documentation issue, but the fact that this is not discussed at all in the spec is not good.

_Impact: Describe the effect this may have in a production setting [1 to 2 sentences]_

The chain may lose consistency and irreparably stall.

_Components: Point to the files, functions, and/or specific line numbers where the bug occurs [1 to 2 sentences]_

def get_committee_assignment(state: BeaconState,
                             epoch: Epoch,
                             validator_index: ValidatorIndex
                             ) -> Optional[Tuple[Sequence[ValidatorIndex], CommitteeIndex, Slot]]:

Committee assignment depends on the state of the chain, which is not finalized

https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/validator.md#validator-assignments

_Reproduction: If used any sort of tools/simulations to find the bug, describe in detail how to reproduce the buggy behavior. Showcasing the bug using the python spec and associated test infrastructure found in the spec repo is preferred!_

1. Start the chain.
2. Turn off Casper for a while to simulate LMD Ghost only.
3. Introduce a long-term reorg by  voting to for a very old alternative previously non-winning branch.

_Details: Very specific details about the bug. What state must the system be in, what types of messages must be included and in which order, etc_

I think this is pretty generic, the only condition is a long-term reorg that changes the committees.

It may be that the spec provides some type of defense against this, but I was not able to find it after re-reading the spec several times.

If some type of protection exist, it needs to be documented. So it may be either a documentation bug or a more fundamental spec issue.

_Fix: Description of suggested fix if available_

Seems that committees need to be selected only based on Casper-finalized state.
This means, that older finalized state needs to be used if newer does not yet exist.

It may be that the spec actually does allow multiple alternative committees operating at the same time, that correspond to alternate branches.  If yes, this needs to be explained in the spec.

Note: if there is any bounty, please send it to Cancer Discovery fund

http://med.stanford.edu/cancer/about/help/make-a-gift.html
