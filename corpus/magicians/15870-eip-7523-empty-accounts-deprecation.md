---
source: magicians
topic_id: 15870
title: "EIP-7523: Empty accounts deprecation"
author: SamWilsn
date: "2023-09-21"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7523-empty-accounts-deprecation/15870
views: 2698
likes: 7
posts_count: 11
---

# EIP-7523: Empty accounts deprecation

https://github.com/ethereum/EIPs/pull/7744/files

## Replies

**chfast** (2023-09-26):

Thanks for working on cleaning up and simplifying the Ethereum spec. And props for adding Undefined Behavior to the spec!

---

**PaulRBerg** (2023-09-26):

Big time in favor of this EIP.

I always get lost when looking at REVM and seeing code like [this](https://github.com/bluealloy/revm/blob/8206193e65ad199a1dde1e79e38bf9ffe38118c9/crates/revm/src/db/states/account_status.rs#L9):

```rust
pub enum AccountStatus {
    LoadedNotExisting,
    Loaded,
    LoadedEmptyEIP161,
```

And this:

```rust
/// Account got touched and before EIP161 state clear this account is considered created.
    pub fn touch_create_pre_eip161(
        &mut self,
        storage: StorageWithOriginalValues,
    ) -> Option {
        // ...
    }
```

Seems like much ado about nothing.

---

**PaulRBerg** (2023-09-26):

Does this EIP purport to replace [EIP-4747](https://eips.ethereum.org/EIPS/eip-4747)?

---

**SamWilsn** (2023-09-26):

[@petertdavies](/u/petertdavies) this is a question for you!

---

**petertdavies** (2023-09-27):

Yes, I decided EIP-4747 was excessively complicated for minimal benefit.

---

**petertdavies** (2023-09-27):

> Seems like much ado about nothing.

This is an understatement. The EELS team reckon about half of the weird edgecases in the EVM are related to empty account clearing. The spec contains a permanent kludge just to deal with the time every client implemented an edgecase wrong and the wrong behavior got permanently embedded in the chain. Far too much time has been expended on pointless historical legacy.

As my favourite example I present this line from REVM:

```auto
// Set all storages to default value. They need to be present to act as accessed slots in access list.
// it shouldn't be possible for them to have different values then zero as code is not existing for this account,
// but because tests can change that assumption we are doing it.
let empty = StorageSlot::default();
account
    .storage
    .iter_mut()
    .for_each(|(_, slot)| *slot = empty.clone());
```

This is handling the case were a pre-Spurious Dragon `CREATE` leaves and empty account with storage and someone `CREATE`s a different account at the same address (requires a full KECCAK collision) after Spurious Dragon. The only reason we know what happens in this case is because someone wrote a test. Both EELS and REVM now have special case code just for that test.

---

**PaulRBerg** (2023-09-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/p/4bbf92/48.png) petertdavies:

> I decided EIP-4747 was excessively complicated for minimal benefit.

It might be worth mentioning this in the EIP

---

**jochem-brouwer** (2023-10-25):

I was not aware of this EIP and I got aware of this just now, thanks [@shemnon](/u/shemnon) for putting this on an ACDE agenda ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

I completely agree with this EIP. I am just wondering, can this EIP also be extended to testing suites? I do not find explicit lines of this at the EIP. We at EthereumJS have had many cases where this entire touch-and-delete logic has triggered state test failures. If we can “just” agree that a final state trie (i.e. when one reports `stateRoot`) does not contain empty-but-existing accounts are not accepted (they are deleted) then this would help a lot ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**winsvega** (2024-01-08):

what about L2 networks that has totally different genesis and chain state.

we won’t have empty account scenarios covered for them?

---

**MariusVanDerWijden** (2024-02-21):

I have verified that ethereum mainnet does not contain these accounts

