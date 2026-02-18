---
source: magicians
topic_id: 5480
title: MEDGASPRICE opcode EIP
author: j_chance
date: "2021-03-05"
category: EIPs
tags: [opcodes, eth1x]
url: https://ethereum-magicians.org/t/medgasprice-opcode-eip/5480
views: 2298
likes: 1
posts_count: 8
---

# MEDGASPRICE opcode EIP

This thread is for discussing the EIP adding a MEDGASPRICE opcode as described [here](https://github.com/ethereum/EIPs/pull/3332).

This opcode is designed to allow contracts to avoid the competitive nature of the gas price market by setting an upper bound on acceptable gas prices. This can be used (primarily) to prevent front-running, but could also be used for first come first serve sales, pseudo-serial queues in decentralized exchanges, etc.

## Replies

**matt** (2021-03-05):

`MEDGASPRICE` may be a valuable opcode to include, but the current motivation doesn’t convince me. It is really a crutch to attempt to stop front-running, but miners have complete control over that. If there is the economic incentive for them order transactions a certain way, they most likely will. I would like to see other valuable use cases for this opcode. Also note, the EIP-1559 BASEFEE opcode will provide contracts a mechanism to roughly gauge the current gas economy.

---

**vbuterin** (2021-03-06):

It would be easy to get around; eg. see https://ethresear.ch/t/flashbots-frontrunning-the-mev-crisis/8251

---

**j_chance** (2021-03-08):

Hey guys, I appreciate the feedback.

The way I saw it there were two groups of people that could potentially front-run, everyone and miners. The everyone group could front-run using a very simple bot that submits transactions while miners would have a more difficult time due to the fact that they would need to find the block in question in order to re-order the transactions in a favorable way. My thinking was stopping the larger group would at least be a step in the right direction and then the odds of front-running become a function of the ratio of miners participating in front-running.

That logic is a bit naive though, especially as mining fees decrease with EIP-1559 miners will be more incentivized than ever to extract value wherever possible.

I still think a median gas price operator would be useful from a contract programming perspective but I don’t know if it’s different enough from the basefee operator to justify adding it. I also assumed that there would be inclusion fee competition after EIP-1559 but that would only happen if the economics don’t work as expected - which seems unlikely to me now after thinking about it more.

So, I agree this change is probably unnecessary. Also, thanks [@MicahZoltu](/u/micahzoltu)  for suggesting a commit reveal system for fraud proofs. Such a system is still vulnerable to front-running but could *probably* be tweaked to work well.

I’m not sure what to do with this EIP, I can edit it to be withdrawn or the PR can simply be closed. I’m in favor of finishing the changes and marking it withdrawn so the discussion is preserved.

---

**MicahZoltu** (2021-03-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/j_chance/48/3417_2.png) j_chance:

> commit reveal system for fraud proofs. Such a system is still vulnerable to front-running but could probably be tweaked to work well.

If done right there shouldn’t be a way to frontrun.  Check out ENS for an example of an “un-frontrunnable” commit-reveal scheme.

---

**MicahZoltu** (2021-03-08):

I would *personally* prefer the PR was just closed, but I would not block a proposal to just merge it as withdrawn so the history is retained.

---

**j_chance** (2021-03-08):

> If done right there shouldn’t be a way to frontrun. Check out ENS for an example of an “un-frontrunnable” commit-reveal scheme.

Thanks for the tip! Their implementation is what I was thinking. The problem is, just by committing any hash you’ve alerted the network that some fraud may have occurred. Anyone attempting to front-run could then quickly look at the rollup in question, find the fraud themselves and commit their own hash. One way I’m thinking of avoiding this is having the commit stage occur separately from the rollup. e.g. an ephemeral contract is created with some appropriate methods then the reveal stage verifies and selfdestructs the contract.

> I would personally prefer the PR was just closed, but I would not block a proposal to just merge it as withdrawn so the history is retained.

Yea, I’m biased but I think preserving the discussion/idea is useful in case someone considers it in the future.

---

**MicahZoltu** (2021-03-08):

You can mask the commit in that case, so it isn’t obviously a commit until the reveal.  I suspect you can do something with a CREATE2 contract where you send ETH to the address in advance and then the reveal would contain a proof of that transaction occurring.  Not terribly gas cheap, but there may be more gas efficient solutions as well (that is just what pops into my head).

