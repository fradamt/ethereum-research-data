---
source: magicians
topic_id: 21975
title: "EIP-7833: Scheduled function calls"
author: keyvank
date: "2024-12-05"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7833-scheduled-function-calls/21975
views: 247
likes: 5
posts_count: 10
---

# EIP-7833: Scheduled function calls

## Abstract

Ethereum’s smart contracts enable users to delegate control of their funds to code, but these contracts require an external trigger to execute. Timing is often critical, and issues such as network delays or malicious behavior by block producers—like MEV attacks—can prevent timely execution. To address these challenges, this Ethereum Improvement Proposal (EIP) introduces a new opcode, OFFERCALL, which allows contracts to schedule function calls. When functions self-schedule, they exhibit bot-like behavior. These scheduled calls would offer ETH to block producers as an incentive to prioritize their execution over manually submitted transactions. If the offer is not fulfilled, the bot is deactivated until manually re-ignited by the owner. The EIP proposes enforcing the execution of scheduled calls as a requirement for block validity. This could help mitigate MEV attacks, as block producers would be compelled to execute bots that neutralize market manipulation within the blockchain.

## Specification

Adding bot-like behavior to an EVM function is achieved by recursively scheduling a call to the same function in the next block. We propose introducing a new EVM opcode, OFFERCALL, which, as the name implies, offers ETH to be burnt to the block producer of the next block in exchange for invoking a function. These offers are aggregated and ranked by the Ethereum node, with only the top N offers being retained; all others are discarded. Scheduled calls must be executed before any user transactions, with execution order determined by their rank in the sorted list. The offered ETH is burnt to prevent block producers from exploiting the system by scheduling calls that pay the offered amounts back to themselves.

Here is a solidity example of how the usage of OFFERCALL would look like:

```auto
contract Bot {
    uint256 offerPerCall;

    constructor(uint256 _offer) {
        offerPerCall = _offer;

        // Ignite the bot with an initial invocation offer
        offercall(update, offerPerCall);
    }

    function setOffer(uint256 _offer) external {
        offerPerCall = _offer;
    }

    function update() external {
        // Do scheduled work

        // The callee may reschedule itself in order to
        // introduce a bot-like behavior.
        // The callee has to be careful about its offer
        // otherwise it may die.
        offercall(update, offerPerCall);

        // Once an offercall fails, the contract owner
        // may have to set a new offer by calling `setOffer`
        // and then invoking the `update()` function again.
    }
}
```

Link to EIP: [Add EIP: Scheduled function calls by keyvank · Pull Request #9096 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9096)

## Replies

**wjmelements** (2024-12-06):

This isn’t necessary. You can do this already with the `TIMESTAMP` opcode, by rewriting your update like this:

```auto
uint256 after; // when to call the next update
function update() external {
   require(now > after);
   after += 1 day;
   // do scheduled work
   msg.sender.transfer(offerPerCall);
}
```

with eip 7702, even EOAs will be able to schedule activity.

---

**keyvank** (2024-12-06):

I thought broadcasting a contract-call which doesn’t meet the requirement (`require(now > after);`) leads to transaction failure (Which still is included in the block). How does that remove the need for a external entity to trigger the contract at the right time?

---

**wjmelements** (2024-12-07):

I was representing your “scheduling” that way.

> How does that remove the need for a external entity to trigger the contract at the right time?

It doesn’t. But someone needs to pay the gas. Letting anyone trigger it is as good as letting the builder trigger it. If you only want the builder to be able to trigger it you can do

```auto
require(msg.sender == block.coinbase);
```

It’s not important for there to be a separate trigger method than transactions. Better that there are fewer mechanisms because it is simpler.

---

**bbjubjub** (2024-12-07):

Personally, I think this is quite a clever solution and would like to see it fleshed out more.

On a more general level, I think having multiple pathways to access blockspace makes sense. We already have top-of-the-block which comes at a premium, and potentially the inclusion list. On L2s we also have transactions coming from the L1 which also have different properties. There could be a market fit for these types of delayed transactions that have been included by previous block builders but execute in the current block.

Compared to n+1 inclusion lists, scheduled function calls feel conceptually simpler because they stay in the EVM. They also access the top of the block. On the other hand, they would be included by *builders* instead of proposers, which is something inclusion lists want to avoid due to their tendency to centralize. For that reason I think we still need inclusion lists, but scheduled transactions could complement them.

It would be interesting to experiment with this on L2s, to see what people do with them. At the same time, keepers are well established and have distinct advantages, such as the ability to supply offchain information which scheduled transactions lack. This is also why encrypted mempools cant be built on them as far as I can tell.

On the more technical level, I would suggest that we should limit the sum of gas used by scheduled transactions instead of their number. I don’t think either design is game-theoretically unsound, but this would help price resources better. I also think `OFFERCALL` should take a byte string of arbitrary length as input for the scheduled call instead of a selector, which don’t exist at the bytecode level. This also allows passing arguments.

---

**keyvank** (2024-12-07):

Wasn’t aware of the inclusion lists EIP! Thanks ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Yes, I’m totally sure that limiting offers by count (Or even gas) isn’t the best idea (I’m not even sure if we need to put a separate limit (Apart from the limit Ethereum naturally puts on the txs in a block) on them at all ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)). What I’m sure is, there are applications that need to be somehow “alive” on the blockchain.

Invoking `OFFERCALL` should also be very similar to a DELEGATECALL for example, getting a contract-address and a bytestring as you said. (The contract to be called doesn’t need to be the same contract that offers the call)

---

**Arvolear** (2024-12-08):

Hey [@keyvank](/u/keyvank), I think this behavior can probably be implemented without the need to “hard fork” the network. Similar architecture to ERC-4337 can be taken and OFFERCALL opcode substituted to a simple EVM log (event).

The Ethereum validators may then install a special add-on that will monitor these events and do the functions execution.

WDYT?

---

**keyvank** (2024-12-08):

Hmmm, account abstraction works too! But unlike a natively scheduled call (Which is forced to be executed on the requested block), its execution is not guaranteed.

---

**theGreg** (2025-01-03):

[@keyvank](/u/keyvank), and for anyone seeking scheduled transaction capabilities, here’s a public-good contract TransferScheduler that handles this at an ERC20 smart contract level.

Essentially, relays observe the event logs for scheduled transfers, queue them offchain, and broadcast them at the specified time in exchange for the equivalent of the transactions gas fee plus tip in WETH.

Also not guaranteed but is permissionless and decentralized.

---

**theGreg** (2025-01-03):

TransferScheduler:

```auto
https://github.com/MnrGreg/TransferScheduler
```

