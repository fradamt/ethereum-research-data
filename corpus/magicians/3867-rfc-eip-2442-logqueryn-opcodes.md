---
source: magicians
topic_id: 3867
title: "[RFC] EIP-2442 - LOGQUERYn Opcodes"
author: pinkiebell
date: "2019-12-19"
category: EIPs
tags: [opcodes, events, eip-2442]
url: https://ethereum-magicians.org/t/rfc-eip-2442-logqueryn-opcodes/3867
views: 1240
likes: 3
posts_count: 10
---

# [RFC] EIP-2442 - LOGQUERYn Opcodes

![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15) Magicians.

![:woman_mage:](https://ethereum-magicians.org/images/emoji/twitter/woman_mage.png?v=15) Let this here be the breeding ground, around all things LOGQUERY bound. ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=15)



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2442)














####


      `master` ← `pinkiebell:logquery`




          opened 04:14PM - 19 Dec 19 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a182a4c55d80ef4c9cb5ee93ab90f81199f412ec.png)
            pinkiebell](https://github.com/pinkiebell)



          [+113
            -0](https://github.com/ethereum/EIPs/pull/2442/files)







This EIP specifies new opcodes `LOGQUERY(x)`, which mirrors the semantics of the[…](https://github.com/ethereum/EIPs/pull/2442) `LOG(n)` opcodes to gain the support for querying/filtering the most recent log event of the current contract/EVM context.












To better support stateless(light)-clients, layer-2 scaling solutions and similiar applications,
gaining the ability to query the last emitted log event and having the log-data available inside a
contract has a huge benefit to an overall simpler system/application design.

In the context of optimistic-rollup solutions, one could imagine to use `LOG` events, corresponding `topics` as storage keys and log-data

as a way to signal state changes to light clients and simultaneously using it as a storage backend for the on-chain contract itself.

A rudimentary example:

```auto
// Layer-2 Bridge contract transfers AMOUNT of TOKEN from `Alice` to `Bob`.

let storageTopic = keccak256(Alice, Token)
// query Alice
let success = logquery1(memoryPtr, 0, 32, storageTopic)

// we had a past event
if (success) {
  // the data of the log contains the uint256 balance
  let aliceBalance = mload(memoryPtr)

  if (aliceBalance >= AMOUNT) {
    mstore(memoryPtr, aliceBalance - AMOUNT)
    // update Alice's new balance
    log1(memoryPtr, 32, storageTopic)

    // Bob's new (pre) balance
    mstore(memoryPtr, AMOUNT)
    let storageTopic = keccak256(Bob, Token)
    // query Bob
    success = logquery1(memoryPtr, 0, 32, storageTopic)
    if (success) {
      // update Bob's balance
      mstore(memoryPtr, mload(memoryPtr) + AMOUNT)
    }
    // log Bob's new balance
    log1(memoryPtr, 32, storageTopic)
  } else {
    // Alice has not enough AMOUNT
    revert()
  }

} else {
  // no event for (Alice, Token) emitted in the past - who is Alice?
  revert()
}
```

Other solutions like validating log events with past block-hashes are inconvienent and also of limited use.

Additionally, there is no trustless way of verifying if any given log was the latest/most recent  one.

## Replies

**MrChico** (2019-12-21):

The very nature of ethereum LOGs is that they are transient constructions that they can only reveal information about EVM execution, but never effect it.

Currently, fully verifying nodes do not need to store any logs at all, and while most implementations do anyway, there are [concrete plans on pruning historical logs](https://gist.github.com/karalabe/60be7bef184c8ec286fc7ee2b35b0b5b#theoretical-solution). This proposal would increase the storage requirements for nodes.

In addition to this, there are smart contract security properties that would need to be revisited in the context of this EIP. In discussions around reentrency vulnerabilities, or more generally the question of what possible state can be changed as a result of a CALL, the general assumption is that emitting a LOG does not effect state, and will therefore not effect further computation (cf.  [STATICCALLWITHLOGSANDVALUE](https://github.com/ethereum/pm/issues/123#issuecomment-528506546)).

---

**pinkiebell** (2019-12-21):

Thanks for the feedback!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrchico/48/1427_2.png) MrChico:

> Currently, fully verifying nodes do not need to store any logs at all, and while most implementations do anyway, there are concrete plans on pruning historical logs. This proposal would increase the storage requirements for nodes.

My initial thoughts on the implementation side of the nodes was that they only have to store the most recent log events for any given unique topic-combination `log0() log1(), log2() etc`, and are free to prune the remainder of it. So yes, it increases the state requirements somewhat that these nodes still need some kind of index + the logs itself.

My assumption is that if developers going to use this scheme, then they likely won’t make us of `SSTORE`/`SLOAD` anymore.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrchico/48/1427_2.png) MrChico:

> In addition to this, there are smart contract security properties that would need to be revisited in the context of this EIP. In discussions around reentrency vulnerabilities, or more generally the question of what possible state can be changed as a result of a CALL, the general assumption is that emitting a LOG does not effect state, and will therefore not effect further computation (cf. STATICCALLWITHLOGSANDVALUE).

![:bulb:](https://ethereum-magicians.org/images/emoji/twitter/bulb.png?v=12)Thanks for the hint. I agree, that would need to be communicated widely.

---

**jochem-brouwer** (2019-12-24):

The gas cost of this EIP does seem way too low. I would use this opcode to store data (like `SSTORE`). You can use the storage slot as the topic and then use `LOGQUERY1` to load the data. Logging (`LOG1`) is much cheaper than storing via `SSTORE`. Loading it will also be significantly cheaper than `SLOAD`. Result is probably that this is significantly underpriced.

Another problem I see is that you might need to know the length of the stored event. You can of course circumvent this by storing the length in the first bytes32 and then loading the rest, e.g. calling the opcode twice with different lengths.

What happens when this op is called on a contract which has the opcode, where this contract has been deployed before the fork block? What happens if I call the op? If it returns the last log this means at the block we should somehow query the chain to figure out the latest log data. This imposes a gigantic load on the fork block. Even if a client does not do this it still means it has to retroactively go back in blocks to figure out the latest data.

In general I think this op is severely underpriced and think it can be used to DoS the network by simply logging gigantic loads of data for a low price. In conjunction with other research topics such as state rent this would also somehow need to get implemented in the rent, to prevent massive unbounded state growth. I currently see too many practical problems with this EIP and also dont really see a practical use for it.

---

**pinkiebell** (2019-12-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Another problem I see is that you might need to know the length of the stored event. You can of course circumvent this by storing the length in the first bytes32 and then loading the rest, e.g. calling the opcode twice with different lengths.

Assuming the contract does ‘know’ what the logs represent, this should not be needed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> What happens when this op is called on a contract which has the opcode, where this contract has been deployed before the fork block? What happens if I call the op? If it returns the last log this means at the block we should somehow query the chain to figure out the latest log data. This imposes a gigantic load on the fork block. Even if a client does not do this it still means it has to retroactively go back in blocks to figure out the latest data.

If you mean the Proxy (`DELEGATECALL`) situation, this would imply that it indeed has to query for the log in history (before the `FORK_BLK`).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> In general I think this op is severely underpriced and think it can be used to DoS the network by simply logging gigantic loads of data for a low price. In conjunction with other research topics such as state rent this would also somehow need to get implemented in the rent, to prevent massive unbounded state growth. I currently see too many practical problems with this EIP and also dont really see a practical use for it.

I’m agree that it is important to reduce the state-burden for nodes, but I also think that we should not do that by limiting new capabilities/features;  and instead doing it with a good pricing model. I’m open for any gas-cost recommendations ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) .

> I currently see too many practical problems with this EIP and also dont really see a practical use for it.

The use-case I had in mind was like this:

- Light-clients rely on emitted events to store the results of any complex operations,
so that the light-clients don’t have to implement & calculate basically the same complex logic again.
- The contract needs to store the results of that computation and also emits the same results via log events. That means for a full node (with event logs), it is actually cheaper on disk and by computing time (< that’s is a guess) if it only have to deal with the log entries.

Thanks for the feedback!

---

**kladkogex** (2019-12-30):

I think the correct compromise is making a limited range of logs  (say last week of logs by timestamp) accessible to EVM.

There would be a huge benefit to that, and the costs would be tiny.

---

**pinkiebell** (2020-01-02):

Thanks for the feedback! This sounds like a good compromise. I personally did like a larger timeframe for the logs, 1 week is a bit low for certain applications that may need to handle disputes in a bigger timeframe.

I will work on some numbers to estimate the storage costs, probably in the next week.

---

**pinkiebell** (2020-01-14):

Let me propose another compromise here, how about just storing the hash of the log-data?

Additionally (as per [@kladkogex](/u/kladkogex)’s suggestion), we define `LOG_RETENTION_EPOCH = <number in blocks>` to be the time(in blocks) any unique log event needs to be stored until `<blockNumber of the block this log was emitted> + LOG_RETENTION_EPOCH` passes.

Instead of `success = logquery1(memoryPtr, 0, 32, storageTopic)`

we can do `logDataHash = logquery1(storageTopic)`.

```auto
IF logquery1(_topic_) EQUALS 0
THEN

ELSE
  returns the keccak256() hash of the data emitted from the log event
```

In the case of `log4`, the node needs to store `4 x 32 bytes (topics) and + 32 bytes for the hash = 160 bytes`. Plus any additional metadata for storing/retrieving such values (implementation specific).

---

**shemnon** (2020-01-21):

I want to echo [@MrChico](/u/mrchico)’s opinion on the matter.  Logs are write only within the context of a smart contract.  Making them queryable alters a fundamental assumption about how a smart contract works.  The intent is that logs would be useful to programs outside of the smart contract execution environment.  If a smart contract needs storage it should use storage.

---

**pinkiebell** (2020-01-24):

Thanks for the input guys!

I’m going to close the pull request and see you next time around ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

