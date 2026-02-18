---
source: ethresearch
topic_id: 14944
title: Decentralized L2 Sequencing w/ Native IBC Interoperability
author: shakeshack
date: "2023-03-02"
category: Layer 2
tags: []
url: https://ethresear.ch/t/decentralized-l2-sequencing-w-native-ibc-interoperability/14944
views: 5667
likes: 16
posts_count: 14
---

# Decentralized L2 Sequencing w/ Native IBC Interoperability

*Authors: [Bo Du](https://twitter.com/0xshake) ([Polymer Labs](https://www.polymerlabs.org/))*

There are three core issues that could be solved using a cosmos sdk (PoS) based shared or single rollup sequencer for Ethereum rollups. The solution gets us both native IBC interoperability and decentralized sequencing at the same time!

The first issue is not well defined and incompatible transport layers across rollups and chains. An interoperability protocol has three layers - application (e.g. HTTP, gRPC), transport (e.g. TCP/UDP) and state (e.g. physical network links). The transport layer produces the commitment of chain A to some messages intended to be sent to chain B. This commitment is generally in the form of some merkle root.

[Inter-Blockchain Communication Protocol or IBC](https://ibcprotocol.org/) has an extremely well defined transport layer that is analogous to TCP/UDP in the OSI model. IBC transport layer commitments would be understandable by any IBC enabled chain as well. This would **effectively merge Ethereum and the Cosmos (and more because the IBC network is growing)**.

Seamless interoperability between chains requires a standardized transport layer otherwise packet commitments made by one chain would not be understood by another chain. IBC is already the standard transport protocol in the Cosmos and can be the standard transport protocol in Ethereum as well.

The second issue is the problem of centralized canonical bridges in the L1 → L2 direction. Currently these bridges are both centralized and maintained by the rollup teams themselves. Using cosmos sdk based sequencers would allow rollups to communicate with one another via light clients and IBC instead of using a centralized canonical bridge.

The third issue is the problem of centralized sequencers. Currently L2 protocols like Arbitrum and Optimism run their own sequencer internally. While this is a great business for them, this is not great for decentralization. A PoS sequencer means that anyone can acquire tokens to join the network as a block proposer. It becomes a free and dynamic market with an easy MEV integration (it’s easy to add MEV logic to a cosmos sdk chain).

In summary, there are three core issues a cosmos sdk based sequencer would solve:

- Incompatible and not well defined transport layers for interoperability
- Centralized canonical bridges in the L1 → L2 direction
- Centralized sequencers

This solution solves for the centralized sequencer, canonical bridge and interoperability problems at the same time.

Implementation wise a few things would need to happen for L2 <> L2 IBC communication. Let’s take a high level look at this.

On the sending side rollup:

- Bindings between the rollup VM → IBC transport logic on the sequencer would need to be made
- IBC transport logic on the sequencer would commit to all of the IBC related messages produced by the rollup
- The IBC transport commitment needs to be posted on chain on Ethereum (in addition to the rollup state commitment)

On the receiving side rollup:

- Run an ethereum light client on chain or run a tendermint light client (use the PoS validators of the sequencer of the L2 as an attester to an Ethereum block)
- Relayers prove the transport commitment made by the sending L2 exists in the Ethereum state commitment
- Relayers can query for and supply merkle proofs for packets within the transport commitment

There’s some additional exploration that can be done here around the sequencer sharing security from Ethereum re-stakers on a solution like EigenLayer. This would provide additional security for receiving L2s that opt to use the PoS validators of the sequencer of the L2 as an attester to an Ethereum block.

For those coming from the web2 space, the solution w.r.t. interoperability can be thought of as **introducing a networking sidecar**. Think Sidecar by Istio or Envoy by Lyft.

Let’s bring all ecosystems together through IBC and decentralized sequencers!

## Replies

**0xapriori** (2023-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/shakeshack/48/7531_2.png) shakeshack:

> A PoS sequencer means that anyone can acquire tokens to join the network as a block proposer.

What do you think about the arguments [against POS](https://ethresear.ch/t/against-proof-of-stake-for-zk-op-rollup-leader-election/7698)?

---

**ao98** (2023-03-02):

hey! thanks for the post. excited to have someone who has thought about, and is actively implementing IBC on other chains thinking about this.

![](https://ethresear.ch/user_avatar/ethresear.ch/shakeshack/48/7531_2.png) shakeshack:

> This would effectively merge Ethereum and the Cosmos

what do you mean by this? i have a lot of thoughts on the topic ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12) would love to discuss further / maybe elaborate here after you first answer. I think we can start from first principles:

ie. if multiple L2s share the same sequencing protocol, where the sequencing protocol is a chain running Tendermint consensus & [proposer selection](https://github.com/tendermint/tendermint/blob/936221e0a8d9d9b7e334df3fb67c745d7cda7c5e/spec/consensus/proposer-selection.md), what are the implications of the chain being IBC-enabled?

---

**shakeshack** (2023-03-02):

Hmm my rough thoughts:

- The cosmos SDK is fairly flexible w/ adding custom module logic. Perhaps we can turn proposer selection at the application layer into a public auction and allow for open participation perhaps using Eth directly.
- In terms of security, I think this is a great case for borrowing security from eth validators via EigenLayer.
- There’s an IBC app spec for cross chain validation which can replace the sequencer PoS validators with ethereum validators (there’s some missing pieces here but trying to motivate the idea).
- Perhaps its possible for PoS sequencer to be token-less (only uses Eth) and consist completely of Eth validators and stake with a public auction market that is also Eth based.

---

**shakeshack** (2023-03-02):

Ah so the idea here is that cosmos sdk already has a [native IBC transport implementation](https://github.com/cosmos/ibc-go). The rollup VM can call into the IBC transport logic on the sequencer. This step can be converted in the future to a zk circuit to remove trust on the sequencer.

The sequencer is essentially producing a transport commitment on behalf of the rollup in an IBC compliant way. This means the sequencer is a networking sidecar to the rollup.

The sequencers could be shared but do not need to be shared.

---

**edfelten** (2023-03-02):

I’m not clear on this part:

`* IBC transport logic on the sequencer would commit to all of the IBC related messages produced by the rollup`

Typically rollup sequencers don’t commit to the *results* of rollup transactions, they only commit to the transaction data (i.e., the input to the transaction).  The sequencer isn’t trusted to provide definitive information on the results of transactions.

In other words, the rollup security model would not trust the sequencer to vouch for the messages produced by the rollup.

---

**0xjim** (2023-03-02):

You raise some interesting points, but I don’t quite agree with your second point:

> The second issue is the problem of centralized canonical bridges in the L1 → L2 direction. Currently these bridges are both centralized and maintained by the rollup teams themselves.

While they are centralised, I don’t that it’s an issue because smart contract rollups derive their state from L1 itself and effectively run an Ethereum light client. Adding in a third-party for L1 → L2 bridging will needlessly add another trust assumption (e.g., SNARKing Ethereum consensus and using multi-hop IBC in order to pass the message to L2).

---

**kelemeno** (2023-03-03):

I concur with [@edfelten](/u/edfelten) and [@0xjim](/u/0xjim), the main issue is security. I am not sure [@shakeshack](/u/shakeshack)  realises the trust assumptions behind rollups, and their trustless nature (as viewed from L1).

- Given this, the L1<>L2 bridge has to be “centralised” (a more accurate word is canonical, as the operators (=L2 validators) can be decentralised). This is because there can only be a zk/fraud proof verifier contract of the L2, and bridging happens via this contract.
- “The IBC transport commitment needs to be posted on-chain on Ethereum (in addition to the rollup state commitment)”. For a rollup posting both is redundant, the rollup state commitment (with proof), is enough to prove the state transition of the rollup. For this very reason, IBC is not needed between rollups (verifying the consensus of the other chain is not needed as the execution is already checked via the zk/fraud proof).

In conclusion, the main difference is that IBC checks consensus, wheres rollups checks execution. For this reason, simply porting IBC is not really suitable.

---

**shakeshack** (2023-03-03):

Yes that is correct. This is not a traditional sequencer workload. The transport logic introduces a trust assumption on the sequencer but does not affect the state commitment.

However, the state → transport commitment mapping can be converted into circuit with an on chain verifier to remove the trust assumption.

---

**shakeshack** (2023-03-03):

I think you’re missing the point here. Adding IBC transport in this way has nothing to do with proving the state transition of the rollup or verifying consensus for that matter.

A standardized transport commitment via the IBC standard is important for all IBC enabled chains to speak the same language at the transport layer.

You inherently don’t want to conform the state commitment data structure of the execution environment you’re producing this transport commitment for.

Also, consensus is a state layer concern and not a transport layer concern. It’s a common misconception to think of the state layer when thinking about IBC.

---

**dpbmaverick98** (2023-03-04):

Really interesting convo, it is amazing to see that people are also thinking about a common transport layer for L2s, something I feel is really important for web3 to provide a web2 level of user and developer experience.

So far the discussion has been around L1->L2 canonical bridging but I actually want to explore the possibilities of " * **Well defined transport layers for interoperability**" and what all properties this transport layer should have.

This is how my doubt also emerged, what will be the flow of a message from let’s say a Cosmos Appchain to an OP Chain and what all trust assumptions will be introduced?

![](https://ethresear.ch/user_avatar/ethresear.ch/shakeshack/48/7531_2.png) shakeshack:

> chains requires a standardized transport layer otherwise packet commitments made by one chain would not be understood by another chain

---

**edfelten** (2023-03-04):

Maybe I’m missing something, but when you said in the original post that “The transport layer produces the commitment of chain A to some messages intended to be sent to chain B.” I thought this meant that the messages in the transport layer are known to have been produced by Chain A.

If so, there is no point in having the sequencer produce such messages, because the sequencer is not trusted to make claims about what has happened on the rollup chain. This is not just a small point that can be redefined away–it is fundamental to the security model of rollups.

The sequencer’s role is only to establish an ordering on incoming messages; beyond that it is no more trusted than anyone else.

---

**4rgon4ut** (2023-05-31):

Agree. Also situation with IBC Relayers is not differs much as they are not incentivized enough and also hosted by appchain teams/affilated third parties (It was impossible to gain profit by running Relayer in near past, idk maybe something changed).

The big plus about IBC is that it is unified across the network and Relayers responsibility is narrowed to passing messages only.

---

**realkeliang** (2024-03-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/shakeshack/48/7531_2.png) shakeshack:

> ncompatible and not well defined transport layers for interoperability
> Centralized canonical brid

I believe blockchains are inherently designed without native interoperability, as each upholds its sovereignty by maintaining a unique state and ledger independently.

Native interoperability indeed implies that validators or nodes from one blockchain (Chain A) would need to communicate directly with another blockchain (Chain B) through specific protocols. This process introduces significant security challenges for Chain B, as it would be required to trust external data or commands outside its own set of validators, which inherently goes against the principle of trustlessness that blockchains strive to maintain. Each blockchain is designed to operate within its secure and sovereign environment, relying on its validators to maintain consensus and integrity, making direct and native interoperability complex and fraught with potential security risks.

Regarding Layer 2 solutions, achieving ‘native’ interoperability seems highly ambitious without a dedicated blockchain underpinning each L2. This feature remains more an ideal than a readily achievable reality

