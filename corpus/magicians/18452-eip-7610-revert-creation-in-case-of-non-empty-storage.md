---
source: magicians
topic_id: 18452
title: "EIP-7610: Revert creation in case of non-empty storage"
author: rjl493456442
date: "2024-02-02"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7610-revert-creation-in-case-of-non-empty-storage/18452
views: 3291
likes: 10
posts_count: 23
---

# EIP-7610: Revert creation in case of non-empty storage

EIP: [Add EIP: Revert creation in case of non-empty storage by rjl493456442 · Pull Request #8161 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8161/files)

## Replies

**holiman** (2024-02-02):

Related discussion can be found here, on a PR which preceded this EIP: [core/state: remove account reset operation by rjl493456442 · Pull Request #28666 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/28666#issuecomment-1891997143)

cc [@shemnon](/u/shemnon) [@petertdavies](/u/petertdavies) [@LukaszRozmej](/u/lukaszrozmej) [@rakita](/u/rakita)

---

**shemnon** (2024-02-05):

I support this.  Reverting on non-empty storage is the cleanest fix that doesn’t require fiddling with state.

---

**rakita** (2024-02-07):

In revm presently we are just checking the nonce and code and not storage. As the list of accounts is limited and hash collision is very very unlikely I am fine with having undefined behaviour here.

What I would like to see in future is the removal of those storages from the state as they are dead data. A good time for that would be verkle transition (cc [@gballet](/u/gballet) for visibility on this edge case).

---

**holiman** (2024-02-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rakita/48/2822_2.png) rakita:

> In revm presently we are just checking the nonce and code and not storage.

Right, that is the correct behaviour for now. However, [@petertdavies](/u/petertdavies) wrote ([core/state: remove account reset operation by rjl493456442 · Pull Request #28666 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/28666#issuecomment-1895871101)):

> Reth and EELS both intentionally implement a version of the account reset solely to pass the tests.

What does that mean? Sounds to me like EIP-7610 would make it possible to remove some “code that exists only to pass a few quirky tests”.

---

**rjl493456442** (2024-02-08):

I think there is no conflict between the two. In this EIP, the deployment on non-empty storage is rejected to prevent something bad happens. In the future, if we really think it’s necessary to remove these “dead accounts”, we can have another EIP.

Personally I think defining the extra restriction for deployment is easy and conforms to the basic concept of code immutability. Removing the existent accounts is another story, as we do have more “dead” contracts with zero-length runtime code(the only difference is these accounts have non-zero nonce). It’s not that reasonable to only delete the ones listed in the EIP.

---

**shemnon** (2024-02-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> What does that mean? Sounds to me like EIP-7610 would make it possible to remove some “code that exists only to pass a few quirky tests”.

Reth replays transactions from genesis as a core feature, so it’s not just to pass a few quirky tests in their case.  If pre-merge replay was not a feature then the code could be dropped, such as what Besu does with their journaled execution flag.

---

**holiman** (2024-02-12):

> If pre-merge replay was not a feature then the code could be dropped, such as what Besu does with their journaled execution flag.

No, code can “just be dropped”. The “deploy contract despite existing storage” is something that has never happened, nor can ever happen.

To expand a bit on why I want to remove it, is that it makes the journalling more complicated than it needs to be. If a creation happens, then, in order to be strictly according to specification, the journal-event needs to contain a list of slots-that-were-deleted. And if the scope is reverted, these slots needs to be un-deleted (In practice, geth internally makes it even more complex than that, but that is the bare minimum)

---

**Aadi** (2024-02-12):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/3/309bcbb1acad15ac8e8773ec46a792cc3c8e83e3_2_230x500.png)image720×1560 95 KB](https://ethereum-magicians.org/uploads/default/309bcbb1acad15ac8e8773ec46a792cc3c8e83e3)

---

**chfast** (2024-02-12):

I’m in favor. [Implementation draft in evmone](https://github.com/ethereum/evmone/pull/816).

```diff
diff --git a/test/state/host.cpp b/test/state/host.cpp
index e05001357..e3bb850d1 100644
--- a/test/state/host.cpp
+++ b/test/state/host.cpp
@@ -208,7 +208,8 @@ evmc::Result Host::create(const evmc_message& msg) noexcept
     // All combinations of conditions (nonce, code, storage) are tested.
     // TODO(EVMC): Add specific error codes for creation failures.
     if (const auto collision_acc = m_state.find(msg.recipient);
-        collision_acc != nullptr && (collision_acc->nonce != 0 || !collision_acc->code.empty()))
+        collision_acc != nullptr && (collision_acc->nonce != 0 || !collision_acc->code.empty() ||
+                                        !collision_acc->storage.empty()))
         return evmc::Result{EVMC_FAILURE};

     // TODO: msg.recipient lookup is done 3x here.
@@ -221,14 +222,6 @@ evmc::Result Host::create(const evmc_message& msg) noexcept

     new_acc.just_created = true;

-    // Clear the new account storage, but keep the access status (from tx access list).
-    // This is only needed for tests and cannot happen in real networks.
-    for (auto& [k, v] : new_acc.storage) [[unlikely]]
-    {
-        m_state.journal_storage_change(msg.recipient, k, v);
-        v = StorageValue{.access_status = v.access_status};
-    }
-
     auto& sender_acc = m_state.get(msg.sender);  // TODO: Duplicated account lookup.
     const auto value = intx::be::load(msg.value);
     assert(sender_acc.balance >= value && "EVM must guarantee balance");
```

The change makes the following state tests to fail:

```auto
[  FAILED  ] 7 tests, listed below:
[  FAILED  ] stCreate2.RevertInCreateInInitCreate2
[  FAILED  ] stCreate2.create2collisionStorage
[  FAILED  ] stEIP2930.manualCreate
[  FAILED  ] stEIP2930.variedContext
[  FAILED  ] stExtCodeHash.dynamicAccountOverwriteEmpty
[  FAILED  ] stRevertTest.RevertInCreateInInit
[  FAILED  ] stSStoreTest.InitCollision
```

---

**kladkogex** (2024-02-12):

The description has a small inconsistency. I suggest to change

*If a contract creation is attempted due to a creation transaction, the `CREATE` opcode, the `CREATE2` opcode, or any other reason, and the destination address already has either a nonzero nonce,*

To

*If a contract creation is attempted due to a creation transaction, the  `CREATE2`, and the destination address already has either a nonzero nonce,*

It is not possible to use the CREATE to with the same contract address, and there is no way create a contract except CREATE and CREATE2. So “any other reason” does not seem necessary here

---

**holiman** (2024-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> It is not possible to use the CREATE to with the same contract address, and there is no way create a contract except CREATE and CREATE2. So “any other reason” does not seem necessary here

> It is not possible to use the CREATE to with the same contract address

Yes it is, if there’s a hash collision. Alternatively, a contract deployed via genesis allocation, which is then “collided” by a normal deployment.

> So “any other reason” does not seem necessary here

I think the original intent is to signal “even if future deployment methods are added”, For example, there’s been talk of `CREATE3`.

---

**kladkogex** (2024-02-13):

> Yes it is, if there’s a hash collision.

Well ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) I assume this is a  joke since this would take time more than the future existence time of this universe ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)  From the philosophical why should the EIP care what happens after the universe dies?

Also, if one assumes possibility of finding a hash collisions, then the entire Ethereum blockchain will be compromised.

> Alternatively, a contract deployed via genesis allocation, which is then “collided” by a normal deployment.

I feel predeploying contracts in the way is an insecure configuration, since the attacker would be able to do lots of bad thngs.  ETH yellowpaper does not specifically address the issue of predeploying contracts on collision-addresses, but it is definitely something that should never be done for a secure configuration.  In addition, to my knowlege many EVM implementations simply do not check for such collisions during execution, since they presume the collisions will never happen, so they will simply crash.

Also Ethereum spec does not provide a guarantee that the system is secure in case attackers are allowed to predeploy contracts that could collide with regular contracts.  So EIPs should not IMO consider possibility of such deployments.

> So “any other reason” does not seem necessary here
>
>
>
> I think the original intent is to signal “even if future deployment methods are added”, For example, there’s been talk of CREATE3 .

Do not want to sound  too much of a nasty guy, but I think if CREATE3 is created in the future, then the EIP need to be amended. IMO The EIP needs to precise and state things as to the current version of ETH.

---

**shemnon** (2024-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> Do not want to sound too much of a nasty guy, but I think if CREATE3 is created in the future, then the EIP need to be amended. IMO The EIP needs to precise and state things as to the current version of ETH.

EOF has a CREATE3 (and CREATE4) as both CREATE and CREATE2 won’t work with banning code introspection.  Aside from where it gets the bytecode and address generation it follows all exisiting CREATE semantics.  And it would honor this EIP.

---

**shemnon** (2024-02-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> To expand a bit on why I want to remove it, is that it makes the journalling more complicated than it needs to be. If a creation happens, then, in order to be strictly according to specification, the journal-event needs to contain a list of slots-that-were-deleted. And if the scope is reverted, these slots needs to be un-deleted (In practice, geth internally makes it even more complex than that, but that is the bare minimum)

This is quite literally the code I didn’t write in Besu for our jornaled exectuion mode, and instead made it a user flag and told the users “don’t use this pre merge.”  With the enshrinement of this EIP we can make it the default for post-merge networks.

---

**gballet** (2024-02-16):

> What I would like to see in future is the removal of those storages from the state as they are dead data. A good time for that would be verkle transition (cc @gballet for visibility on this edge case).

That would be very easy to implement!

The only question is, what does it break? I will try it when we run the next shadowfork, to at least collect the addresses that are affected so that we can see if there is anything obvious.

---

**chfast** (2024-02-19):

I’m coincidentally working on a new transaction execution API that tracks what state elements are modified during execution and produces “state diff” in the end. The access to the current state is provided by the view-only simple API (e.g. `get_storage(key)`).

In this model, I’m not able to implement the current `CREATE`’s “delete all storage” unrealistic case because there is no way to iterate over all storage keys.

So the EIP-7610 helps a lot in this context. Moreover, it restores nice boundary between transaction execution and state’s trie structure.

---

**SamWilsn** (2024-02-19):

[@MariusVanDerWijden](/u/mariusvanderwijden) wants me to say:

> We should independently verify that this has never happened on mainnet.

---

**rjl493456442** (2024-02-28):

It’s verified! I did run a full sync with new additional rule, chain can be synced with no error.

---

**rjl493456442** (2024-02-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rakita/48/2822_2.png) rakita:

> What I would like to see in future is the removal of those storages from the state as they are dead data. A good time for that would be verkle transition (cc @gballet for visibility on this edge case).

I think we are aligned. Martin and I think we can go with EIP first (it will hurt nothing) and then discard the storage of the accounts on the list during the verkle transition(or we can do it in the Prague fork if we find it’s still over-complicated to discard storage during transition).

---

**chfast** (2024-05-08):

This has been implemented in evmone: [Implement EIP-7610 (non-empty storage create collision) and upgrade execution-tests by chfast · Pull Request #816 · ethereum/evmone · GitHub](https://github.com/ethereum/evmone/pull/816)


*(2 more replies not shown)*
