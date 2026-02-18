---
source: ethresearch
topic_id: 5434
title: Eth1.0 as shard 0 of the Beacon chain
author: josojo
date: "2019-05-10"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/eth1-0-as-shard-0-of-the-beacon-chain/5434
views: 2210
likes: 3
posts_count: 5
---

# Eth1.0 as shard 0 of the Beacon chain

As the Eth1.0 finalization working group is forming, I would like to investigate the technical pro and cons of introducing full POS to Eth1.0 by making Eth1.0 a shard of the Beacon chain.

**Architecture description**

In this section I am description the infrastructure and changes needed to make Eth1.0 the shard 0:

- The Beacon chain can stay like it is currently specified. It will assign randomly validators to all shards, especially also validators to shard 0.
- These validators of shard 0 will be in charge of proposing blocks for the Eth1.0, instead of blocks for shard 0.
- The Eth1.0 clients have to implement the “latest message driven GHOST” fork choice rule, such that they follow the proposed blocks of the beacon chain validators.
- In order to fully verify the correctness of the state of the validators, the Eth1.0 clients also would have to follow the Beacon chain and its finalization.
- While the shard 1-1023 would support - after phase 2 - complicated receipt creations for inter-shard communication, the shard 0 would only generate the receipts for becoming a validator, as the Eth1.0 chain is planned to do anyways.

**Analysis**

Pros:

- This approach would unify the two different chains eth1.0 and eth2.0
- It would introduce full POS to the Eth1.0 chain with relatively small effort. POS would offer better security and finalization to the Eth1.0 chain
- As Beacon chain clients anyways need to be aware of the eth1.0 chain, there is no substantial additional load on the clients.
- Compared to the proposals of the current working group of eth1.0 finalization, the shard 0 approach seems cleaner, as it is introducing pure POS, instead of mixtures of POS and POW.

Cons

- The introduction of full POS bears a lot of potential risks, especially as the new fork choice rule has not yet been tested.
- Shards are no longer homogenous

**Personal conclusion**

Personally, I think that the benefits outweigh the involved risks. Ending this wasteful and insecure POW period should have one of the highest priorities. I suggest to start the implementation of such solutions or similar ones early and do substantial testing to migrate the risks. These fork choices rules and this POS system is the result of 4 years research and I am convinced that it is much better than the status quo.

I am really looking forward to getting the involved challenges of this proposal highlighted in this thread.

## Replies

**vbuterin** (2019-05-10):

The main challenge I see with doing this “naively” is that the eth1 state size is very large, compared to the planned state sizes of eth2 chains, so it will be difficult for validators to rotate in and out.

Now [@AlexeyAkhunov](/u/alexeyakhunov)’s stateless client research pans out well, one thing we *could* do is create an execution environment (in the sense in https://notes.ethereum.org/s/HylpjAWsE) that processes Merkle proofs of eth1 transactions. Then we could just seed that execution environment with ETH and let it run. This would require zero modifications to eth2, just a dedicated team to write the code of the execution environment.

So far this is my favorite approach for where eth1 “fits in” long term.

---

**dankrad** (2019-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Then we could just seed that execution environment with ETH and let it run. This would require zero modifications to eth2, just a dedicated team to write the code of the execution environment.

Do I understand it correctly that you do not want to emulate the full eth1 chain, but only be able to access its transactions? I wonder if this would ever allow tight integration?

I think the proposal here is one that’s worth considering. Somehow compatibility will have to be achieved; it’s no accident Intel kept compability all the way down to 16 bit in its newest processors ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I wonder if there are ways to solve the state problem. Obviously eth1 in its current form cannot be integrated. So either a reasonable state rent would have to be integrated first that will lead to a sufficiently decrease in state size. Alternatively, maybe there is a way of integrating it that just gradually makes gas very expensive. So while the state is still there, it will be accessed less and less, allowing nodes to keep it in higher latency storage or eventually even remotely.

---

**vbuterin** (2019-05-14):

> Do I understand it correctly that you do not want to emulate the full eth1 chain, but only be able to access its transactions?

No the idea will definitely be to emulate the full eth1 chain. The only difference is that transactions will need to be packaged along with merkle proofs.

---

**dankrad** (2019-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> No the idea will definitely be to emulate the full eth1 chain. The only difference is that transactions will need to be packaged along with merkle proofs.

Aha, yes that makes sense. So then that is basically “making gas very expensive”

