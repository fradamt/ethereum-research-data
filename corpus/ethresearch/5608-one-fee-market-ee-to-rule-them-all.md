---
source: ethresearch
topic_id: 5608
title: One fee market EE to rule them all
author: vbuterin
date: "2019-06-12"
category: Sharded Execution
tags: [fee-market, execution-environment]
url: https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608
views: 7051
likes: 3
posts_count: 11
---

# One fee market EE to rule them all

One of the challenges of the current phase 2 spec is as follows. The abstraction model has ensured that it’s possible for dozens of different kinds of environments (eth1-like, eth1-like-improved, ZEXE, UTXO-based…) to be run on top of the chain, but keeping the consensus code that validators need to run very small. A node only needs to have knowledge of one of these environments if it is personally interested in it. But this only solves the problem of validation; it does not solve another large problem that validators have, which is optimal fee collection: how do validators know what to include that will pay them the most fees, when there are 74 different environments with 33 different ways of representing currency, which the validator does not understand? **A highly abstracted spec that makes validation universal and simple is of limited value if the code needed to run to effectively propose blocks and collect fees still requires knowledge of 74 different sub-protocols**.

One proposed mitigation in the earlier spec design was *relayer markets*. Essentially, there would be a category of intermediaries that each understand one more more of the different environments and aggregate transactions for them and collect them into packages that pay fees using some standard method that the validators understand. These relayers could also perform tasks like adding or aggregating Merkle branches or other witnesses. Alternatively, transaction senders that do not want to go through relayers could simply “self-package” their transactions, making a package with only their transaction included (potentially, transaction senders could create packages containing both their transaction *and* other transactions that they have seen). But what is the universal fee payment medium that these systems would use?

### The basic universal fee market

Here is one proposal. For each transaction package, it would be standard for an EE to create a Merkle branch that is verifiable against the state root in a standard position that contains a receipt with the fee to be paid (eg. `state = SSZContainer(real_state: RealState, fee: uint64)` would make `fee` easy to verify with an SSZPartial). It would be the EE’s responsibility to charge the fees to the actual transaction senders; the `fee` specified in this `fee` value would be charged *to the execution environment* itself.

There would be one EE called the “fee market EE”, where *other* EEs (as well as block proposers) could hold accounts with balances. If anyone submits a Merkle branch showing that some EE issued a receipt paying some fee then the fee market would deduct that fee from that EE’s account and add it to the account of the proposer address of that block. The fee market EE could require branches to be submitted in slot order for each EE, removing the need for any more complicated replay protection.

![image](https://ethresear.ch/uploads/default/original/3X/0/6/0622f6306840bdd8caff3bea3c162fa0b60d994f.svg)

The process for a block proposer looking to accept transaction packages would be to do two things:

1. Run the transaction package and verify that it produces a fee receipt (as an optimization, EE execution could pre-signal that it will produce a certain fee receipt as soon as it knows this, and if an EE is found to even once lie with these pre-signals then it could be automatically blacklisted)
2. Verify that the EE has an account with the fee market EE with enough funds to pay for the fee specified in the receipt.

## Replies

**djrtwo** (2019-06-12):

The receiving of the fee by the block proposer is asyncronous with the proposal of the block, correct? The fees that were transferred into the fee-EE over N blocks would have to be consumed with the N-receipts with a specific block to the EE, right?

---

**vbuterin** (2019-06-12):

Inside of the block, the fee from the transactor into the EE gets processed through some means within the EE, and the receipt saying what the total fee owed to the block producer is gets generated (if there is one transaction package containing 10 transactions then still only one receipt is generated). Some time later, that receipt gets included into the fee market EE, charging the transaction’s EE and crediting the block producer. Some time even later, someone acting on behalf of the transaction’s EE (the fee market can incentivize this) would need to deposit more ETH into the fee market EE to top it up, and also some time later the block proposer can withdraw all of the rewards that they have received.

---

**villanuevawill** (2019-06-13):

I was originally going to advocate for something similar to this in a post today (after analyzing the issues around the original relay market). Your timing is impeccable. **A few points here.**

Why not make it more simple and just use the EE as a hub by which the payment is transferred and call into the appropriately packaged EE for the transactions via a similar staticCallExecutionScript? Standards can be built around this pretty fluidly. This is **one of many** usecases for making calls into other EEs available synchronously. I’ll put a post up about this later.

**Advantages over previous relay markets**

Regardless of whether this system is facilitated via the method above or via a receipt claim, this general approach is a huge step forward. A few reasons why:

- Previous relay markets (1 or 2 relayers per block) generally converges into a cheapest hardware, cheapest computation system. It also could centralize transaction broadcasting and make it very difficult for anyone to self publish their own transaction in case a cartel runs the relay market. Other issues listed here from @benjaminion: Exploring the proposer/collator split
- Previous relay markets discouraged peering
- This separate approach of accepting many different packaged transactions does incentivize peering/sharing between validators of the packaged tx’s
- This allows for a user who is being censored by various relayers or broadcasters to send their own transaction into this “mempool” or peering mechanism
- Introduces a better monetization strategy for wallets and infrastructure providers (vs. potential hoarding between a small cartel of proposers on each shard)
- more unified payment model between all EEs
- Fragmented/multiple transaction packages would actually make self-publishing much easier. (ie. bulk transaction transmitters/relayers may offer best fee deals but packaging your own would likely be more expensive and thus discourage just one or two major relayers)

**Business Models**

I tend to think this approach opens up very strong monetization opportunities for wallet providers and nodes that manage state. Wallet providers are incentivized to keep state and witness data and attach it to each transaction. There can be an additional fee market around adding the witness data on behalf of the tx (separate from a fee differential to the block producer). A lot of different approaches here.

**Preliminary Questions**

- An approach of multiple packages can complicate the system of others wrapping around the packaged transactions and transmitting it for themselves. (although setting limits on recursive action with the call “proxied” through a fee market EE would remove this concern) - we wouldn’t need a system like this: Optimised proposal commitment scheme
- Providing the appropriate witness data would be signed by the original tx sender to accept this service and have an open market or would we encourage a flat fee and any client can add this data (possibly discouraging peering once again if we go wit the flat fee/any client can add)?
- Would the market end up converging into just a few packaged txs anyways? To elaborate, a general relay/fee cover would likely form in many EEs to avoid tx senders from having to own the pegged eth or canonical currency anyways

These are my preliminary thoughts as a whole - I’ll likely follow up with something more formal later.

---

**vbuterin** (2019-06-13):

Another set of actors to keep in mind in all of this is light client servers - nodes that store the full state of a (shard, EE) pair and serve Merkle branches to anyone who wants to read the state (as well as storing history/receipts). Clients would establish connections to these servers and ask for Merkle branches for specific history or state in exchange for payments through a channel. Because any user will be a light client in almost every shard, this class of actors becomes very important. They are also a natural class of actor to serve as a relayer, and they can charge epsilon for the service of relaying at time of receiving the transaction, so it doesn’t matter if block producers just take their packaged tx and redirect the reward to themselves.

Currently, there are few light client servers, but if we set up the infrastructure, in the eth2 world there could be many. Potentially validators could also be light client servers, though really any functionality that involves being always online and storing the chain (eg. on-chain DEX arbitrage bots) could benefit from bundling with being a light client server ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=14)

Will need to think more about this idea of sync calling between different EEs.

---

**cdetrio** (2019-06-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Why not make it more simple and just use the EE as a hub by which the payment is transferred and call into the appropriately packaged EE for the transactions via a similar staticCallExecutionScript? Standards can be built around this pretty fluidly. This is one of many usecases for making calls into other EEs available synchronously.

Even if EEs can do synchronous same-shard calls, that doesn’t mean they can do synchronous ETH transfers during those same-shard calls. As I understand the phase2 proposal2 spec (fwiw, may be mistaken), EE balances are on the beacon state `BigState`, which can only be updated on cross-links (in contrast, EE state roots are on shards and are updated on shard blocks).

Maintaining an ETH balance field in the BeaconState keeps the “minimal execution” spec close to the phase0/phase1 specs, as EE’s are basically the same as validator accounts (with the addition of a code field and a state root field). The state root field can be viewed as existing on a shard, and is updated on shard blocks, in the same way that shard block hashes (in the phase1 spec without execution) are maintained on shards.

It might be a good idea to maintain EE balances as state local to shards, just like the EE state roots, so that same-shard EE calls can do synchronous balance transfers. But let’s be clear in distinguishing “synchronous same-shard EE calls and stateroot updates” versus “synchronous same-shard EE calls and balance transfers” while talking about what the minimal execution spec permits.

I like the idea of a universal/standard fee market EE, btw.

---

**villanuevawill** (2019-06-15):

You’re correct that moving the balance of beacon eth between EEs on the beacon chain would not be a synchronous call and requires a crosslink to form and a receipt to absorb from a shard/EE that pegs to it. Even if we assume this proposed design pegs all fees to beacon eth, this would still simplify the proposal by just generating one account balance per EE/slot for the proposer vs. multiple receipts generated for each submitted transaction package on each EE. I also am on board with agreeing on the right terminology here as well to distinguish balance transfers of beacon eth and stateroot updates for shard eth.

However, I would challenge the assumption that fees would only be paid in beacon eth. I’d also challenge the assumption that pegged beacon eth even needs to be tied to an EE at all. It’s difficult to predict the general trajectory/future of how EEs will form, but here are a few scenarios that could arise:

**1. We peg/bind beacon eth through a shared EE or even token EE (think ERC-20 implementation)**

This scenario is interesting. We could have a token EE that manages deposits/withdrawals of beacon eth and also supports generating other tokens. If we move in this direction and synchronous EE calls are supported within a shard, then beacon eth and other tokens can be bound/shared collectively between other EEs. For example, the eth 1 EE and the community supported eth 2 EE can now transfer value between each other fluidly and synchronously. There would be no need to move pegged eth between the two EEs since the token/shared EE already pegs everything and can be withdrawn directly to the validator account on the beacon chain.

**2. An EE doesn’t peg itself to beacon eth**

Of course, pegging/backing to beacon eth make sense for the eth 1 EE and the subsequent EE the community/ecosystem stands behind. However, we can’t be sure that the canonical/main store of value in addition to fee market in other EEs will be centered around beacon eth.

Anyways, it sounds like we’re likely on the same page, but wanted to clarify the various scenarios. If we do not enforce EE fees to beacon eth, then using the fee market EE to synchronously call into each of the EEs can be pretty powerful here.

---

**villanuevawill** (2019-06-15):

I meant to respond to this sooner. I’m actually very happy with this direction and think the channel method to pay for Merkle branches is quite clean. It will be interesting to see how dex or dapps might provide this service for their users vs. wallets and the monetization opps it provides.

---

**vbuterin** (2019-06-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> 1. We peg/bind beacon eth through a shared EE or even token EE (think ERC-20 implementation)
> This scenario is interesting. We could have a token EE that manages deposits/withdrawals of beacon eth

This is what I was thinking. So the thing that other EEs would be using to pay fees is balance stored in the fee market EE.

> and also supports generating other tokens. If we move in this direction and synchronous EE calls are supported within a shard, then beacon eth and other tokens can be bound/shared collectively between other EEs.

I didn’t get this far, but great idea! Seems potentially really good to me.

---

**cdetrio** (2019-06-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> villanuevawill:
>
>
> 1. We peg/bind beacon eth through a shared EE or even token EE (think ERC-20 implementation)
> This scenario is interesting. We could have a token EE that manages deposits/withdrawals of beacon eth

This is what I was thinking. So the thing that other EEs would be using to pay fees is balance stored in the fee market EE.

Good point that fees can be paid in FeeMarketTokens (erc2000 wrapped BETH). That would be a workaround for “synchronous same-shard EE calls and state root updates” to enable synchronous fee payments, without synchronous same-shard BETH transfers.

---

**matt** (2019-06-15):

There are a couple attributes of a generic asset EE that I think are desirable:

- The EE can be rigorously tested and formally verified, allowing anyone to deploy an asset with full confidence that the implementation is secure
- Allows for upgrades to all assets if need be
- Simplifies the transfer of value between EEs
- No need to for approve -> transferFrom as assets are first class

I’m imagining this execution environment looking something like the following (just trying to get the broad strokes out, feedback is obviously more than welcome):

### GenericAssetEnvState

```python
{
  "assets": [[AssetState, 2**256], MAX_NUM_EE]
}
```

### AssetState

```python
{
  "balances": [u64, 2**256],
  "states": [bytes, 2**256],
  "operations": [OperationCode]
}
```

`OperationCode` would represent wasm code that describes how to perform an operation on the token. I imagine the most generic interface would at least support a `transfer(to, amount)` function which could be defined directly in the EE, but additional functionality (e.g. `authorizeOperator(operator)`) could be stored as wasm modules that are dynamically linked in during runtime. I believe this kind of linking functionality is something that [@axic](/u/axic) is working on.

In this world, ShardEther™ could be premined to some address (`0x000...0000™`) and new tokens could be generated by sending a create transaction to the generic asset EE. These addresses would be valid across all EEs, but each EE, like a fee market EE, would have its own set of balances for each token. Since all / most assets would live within one domain with a consistent addressing scheme, it should be possible to extend the concept of `msg.value` in the Ethereum EE similarly to how I described in [this](https://ethereum-magicians.org/t/brainstorming-the-token-standard-in-eth2/3135/15) post:

### msg.value

```python
{
  "amount": uint256,
  "asset_address": uint256
  # the EE is implicitly known as the origination EE
}
```

Now imagine user A wants to send tokens to contract B. User A crafts a transaction using the new `msg.value` definition and sends it to contract B’s `deposit` function:

```auto
contract B {
  mapping(address => mapping(address => uint256)) deposits;

  function deposit() payable {
    deposits[msg.sender][msg.value.token] += msg.value.amount;
    get_msg_value();
  }
}
```

The `deposit` function updates its records and calls `get_msg_value()`, which is defined as an opcode or EEI host function.

```auto
function get_msg_value() {
  token = GenericTransferableTokenInterface(msg.value.token)
  execEnvCall(token.transfer(self, msg.value.amount))
}
```

The `msg.sender` and `msg.value` of the call to contract B is forwarded to the token contract using a delegate call and `self` is the address of the current execution context, contract B in this example. By nature of signing and sending the original transaction, user A approved the transfer to contract B.

