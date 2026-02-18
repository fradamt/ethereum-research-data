---
source: magicians
topic_id: 21763
title: "EIP-7819: setdelegate"
author: Amxx
date: "2024-11-19"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7819-setdelegate/21763
views: 352
likes: 14
posts_count: 17
---

# EIP-7819: setdelegate

# Discussion topic for EIP-7819

### Update Log

2024-11-18: initial draft https://github.com/ethereum/EIPs/pull/9042

2024-11-21: [EIP merged and available here](https://eips.ethereum.org/EIPS/eip-7819)

2025-05-01: rename opcode, and move from EOF to legacy EVM.

2025-07-17: [Implementation in “execution-specs”](https://github.com/ethereum/execution-specs/pull/1332)

### External Reviews

None as of 2024-11-18.

### Outstanding Issues

2024-11-19: Which magic value to use? (`0xef0100` vs `0xef0101`)

## Replies

**wjmelements** (2024-11-20):

> This instruction is NOT added to legacy EVM.

Why not?

---

**wjmelements** (2024-11-20):

A better way to specify this than a `CREATEDELEGATE` opcode might be to allow `CREATE`, `CREATE2`, `EOFCREATE`/`RETURNCONTRACT` to return a delegate contract.

I don’t think every kind of special contract should have its own opcode.

---

**Amxx** (2024-11-20):

> This instruction is NOT added to legacy EVM.
> Why not?

This is up to debate. I think I did not want to focus on pushing more stuff to the legacy EVM now that we are in a transition to EOF. IMO, there is no way this EIP makes it into a fork before EOF, so I though it would be simpler to only have that in EOF.

> better way to specify this than a CREATEDELEGATE opcode might be to allow CREATE , CREATE2 , EOFCREATE /RETURNCONTRACT to return a delegate contract.

That is an interresting idea, but it would not provide a mechanism for upgradeability of the delegate:

- CREATE uses a different nonce everytime
- CREATE2 would target a different address if the bytecode (of the delegate) changes
- in any cases, both CREATE and CREATE2 fail is the target as non empty code

IMO, this proposal loses a lot of its value if upgrades are not possible.

---

**wjmelements** (2024-11-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> IMO you lose a lot of the value of the proposal if upgrades are not possible.

Upgrades could still be possible via `SETCODE`/`RECREATE` or any of the other mutable code proposals. I think mutable code is important enough that it should be available to everyone, not only delegators.

---

**Amxx** (2024-11-20):

That is a very different path that will take a very long time to get accepted (if it ever is).

Delegations already have this reconfiguration by design, which made me thing this proposal would be more easily accepted than a combo “`CREATE`/`CREATE2`/`EOFCREATE` can create delegations” + “`SETCODE`/`RECREATE`” that may takes multiple years to be available.

---

**shemnon** (2025-03-12):

I think we should make explicit the visibility and effectiveness of the deligation in the spec. We also need to think through what the implications of a rapidly changing delegation could be.  For example, the code in question could take an address, update the delegation, execute that address, update the delegation again, execute that address again, and then remove that delegation.  This would have, in the same transaction without reverts, an address that has three or four possible different codes associated with it, two of which are executed.

We should call this out in security consideraions, namely that end users whose business is forensics and reconciliation, will need to make sure their tooling can handle this scenario.

I propose this note in Specification, after the enumeration of the behavior

> Note: The delegation is effective immediately upon the completion of the operation.  Calls to the address as soon as the next operation will execute the newly delegated code.

---

**Amxx** (2025-03-17):

An account executing differnt logic within the same transaction is already possible with “tranditional” upgradeable contracts.

Still adding that to the EIP document

---

**axic** (2025-04-10):

Since this not only creates, but updates existing delegations, I think a better opcode name would be appropriate. I suggest `SETDELEGATE` or `UPDATEDELEGATE` as a better option.

Side-note: traditionally we do not have opcodes with an underscore in them.

---

**JhChoy** (2025-05-26):

It seems like EOF might be significantly delayed.

What are your thoughts on introducing this opcode to the current EVM in the meantime?

---

**Amxx** (2025-06-18):

The EIP document has been updated to target inclusion in the current EVM !

Note: I’m willing to work on this EIP (implement it in clients, write test cases, champion it during ACD calls) … but I havent seen much enthousiasm outside of my own. If you (or anyone) think it would be a valuable addition to the EVM, please say it publicly (here, or during ACD)

---

**shemnon** (2025-08-21):

I see value in it, and would be willing to help advance it.

My specific use case is 4337 wallets set up via code-cloning intstead of deployment, and deployed in such a way that the ECDSA key cannot un-do the delegation. Rather than burning the key it never had a key.

---

**Amxx** (2025-09-19):

[This X/twitter thread](https://x.com/ngweihan_eth/status/1968583066391040384) describes how contracts are deployed and use chain space.

An interesting statistic is

> There are ~99k factory contracts on mainnet, and they deploy ~89% of all contracts.

If it was available, they could use EIP-7819 to create delegations instead of ERC-1167 clones or ERC1-1967 proxies. This would reduce state usage by ~50% compared to ERC-1167 clones and ~96% compared to ERC-1967 proxies.

---

**Amxx** (2025-09-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> My specific use case is 4337 wallets set up via code-cloning intstead of deployment, and deployed in such a way that the ECDSA key cannot un-do the delegation. Rather than burning the key it never had a key.

The factory could even give the account the ability to self-upgrade. This is something you could never do with key burning.

---

**jochem-brouwer** (2025-11-27):

Hiya, great EIP, some minor comments:

> There parameters are the same ones as used in EIP-7702.

(There → These). The `MAGIC` constant is `0xef0100` but the `MAGIC` constant in EIP-7702 is `0x05` (`0xef0100` is the delegation designator).

I think the way the `location` is derived works, but we should check if there are ways to create collissions with e.g. `CREATE` or `CREATE2` opcode.

The `target` stack item should I think be limited to 20 bytes: e.g. left filll (big-endian notation) it with zeros if it is smaller than 20 bytes and otherwise trim of the highest bytes if it is larger than 20 bytes. If we don’t do this then if someone sets target to a value of `32` bytes then this would be an invalid EIP-7702 designator as the designator should be exactly 23 bytes.

It notes if `target` is `0x0000000000000000000000000000000000000000` then reset the codeHash to the emptyHash, however in EVM we use numbers so the correct way would be to write “if `target` is `0x0`” to avoid ambiguity.

The `location` does not increase the nonce of `location` if it sets the delegate. It should do so because otherwise one can `SETDELEGATE(salt, A)`, then call `location` (which calls A), then `SETDELEGATE(salt, 0)` (this removes the code). We now end up with an EIP-161 empty account and since this is deprecated by EIP-7523 we should not do this.

I think for clarity it should be mentioned that `SETDELEGATE` does not “create a contract” just like how 7702 also does not create contracts. So if we `SELFDESTRUCT` in the transaction where the `SETDELEGATE` was called, `SELFDESTRUCT` should thus behave as if it would be used in a contract created in a different transaction.

---

**Amxx** (2025-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> It notes if target is 0x0000000000000000000000000000000000000000 then reset the codeHash to the emptyHash, however in EVM we use numbers so the correct way would be to write “if target is 0x0” to avoid ambiguity.

If we force the target to be either left padded with zeros or trimed, to always be 20 bytes, is that comment still relevant ?

---

**Amxx** (2025-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> The location does not increase the nonce of location if it sets the delegate. It should do so because otherwise one can SETDELEGATE(salt, A), then call location (which calls A), then SETDELEGATE(salt, 0) (this removes the code). We now end up with an EIP-161 empty account and since this is deprecated by EIP-7523 we should not do this.

Would it be ok to only increment the nonce if target is not 0, or should we do it regardless of target.

Basically, if the is nothing (and never was anything) at `location`, and if the first `SETDELEGATE` uses a zero target, we are not creating the delegation. Technically we are asked to clear the code of an account that doesn’t exist in the trie. In that case is it ok to leave the account empty, or is this seen as an operation that change the code from “undefined” to “0x” … which creates the account, and which thus require setting the nonce to 1 ?

