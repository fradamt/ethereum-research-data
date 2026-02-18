---
source: magicians
topic_id: 20569
title: "ERC-7744: Code Index"
author: peersky
date: "2024-07-16"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7744-code-index/20569
views: 614
likes: 5
posts_count: 21
---

# ERC-7744: Code Index

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7744)





###



Global repository of bytecode, enabling developers, auditors, and researchers to find, analyze, and reuse bytecode efficiently.










Currently contract discovery relies on addresses, which are non-deterministic and can be obfuscated through proxies. Indexing by bytecode hash provides a deterministic and tamper-proof way to identify and verify contract code, enhancing security and trust in the Ethereum ecosystem.

Global bytecode identification is a requirement to build efficient at high scale global factories for future software distribution, that may want to rely on extensive re-use of same codebase as own dependencies, such as [Ethereum Distribution System](https://github.com/peersky/eds/tree/main)  that creates a simple, global index that maps already deployed bytecode to it’s location via `address.codehash`

## Replies

**peersky** (2024-07-16):

Pull request:

https://github.com/ethereum/ERCs/pull/542

---

**radek** (2024-07-22):

Interesting.

What are your thoughts on potential contract CREATE precompile, that would enable to etch runtime bytecode onto the address derived from the that runtime code (runtimecode hash)?

I have been playing with that idea, since making the CREATE3 factory experiencing issues on deterministic deployments on different chains (where Nick’s factory is not deployed).

---

**peersky** (2024-07-23):

Can you share any resources on your experiments?

In a way I understand CREATE precompile would enable runtime bytecode to be intrinsically linked to its address. This seems could potentially simplify contract verification and improve security.

If I get it right, It could be incorporated within EDS as `distribution` base class, currently in the repository there is only minimal proxy clone, others are welcome to be added.

---

**radek** (2024-07-23):

I made some conclusions here: [GitHub - radeksvarz/yac3f: Yet Another CREATE3 Factory](https://github.com/radeksvarz/yac3f?tab=readme-ov-file#there-are-other-create3-factories-why-another-one)

Here is the discussion we had over CreateX deployment: [📖 Private Key Management of `CreateX` Deployer · pcaversaccio/createx · Discussion #61 · GitHub](https://github.com/pcaversaccio/createx/discussions/61)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/peersky/48/6246_2.png) peersky:

> CREATE precompile would enable runtime bytecode to be intrinsically linked to its address. This seems could potentially simplify contract verification and improve security.

Exactly. Unfortunately, when I was presenting the Deterministic crosschain deployments during Eth Prague, I did not see the audience would consider the security behind the deterministic address to be of significant value. So I question whether the issue is valid for the broader community.

---

**peersky** (2024-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> nfortunately, when I was presenting the Deterministic crosschain deployments during Eth Prague, I did not see the audience would consider the security behind the deterministic address to be of significant value. So I question whether the issue is valid for the broader community.

It looks very cool tbh.  Im certainly open to adding such functionality to EDS if you wish to make a contribution.

Would you also think it may be used within the ERC7744 as well, or impact any parts of the proposed standard?

---

**radek** (2024-09-04):

Wrt 7744 mapping I assume no impact there.

However it could favor the deployment of EDS registry itself among chains (esp. those without that deployer) - it would be a perfect use case candidate.

---

**peersky** (2024-09-04):

Speaking from in-standard deployment procedure:  being independent from factory deployment would be amazing, yet I don’t see if this is achievable without making thing centralized (sender dependent)

---

**jochem-brouwer** (2024-10-06):

I just stumbled upon this EIP. Did you consider the following situation:

- A transaction creates a contract
- During this transaction, after deploying the contract (this thus has to deployed from another contract, since it has post-CREATE logic), call into the registry. This will lookup the code hash of the address, and if it does not exist in the mapping, it will set the hash of that address to that address.
- Now, call into the just-created contract and SELFDESTRUCT it (we need to do this at the same tx, the goal is to delete all code)
- The registry now has a pointer of the just-deployed-but-selfdestructed hash to the selfdestructed address
- Thus, upon looking up this specific hash in the registry, it will actually point to an account with no code at all

---

**peersky** (2024-10-07):

That’s a great question!

Since you would register a contract  that contains selfdestruct functionality with a clear means to destroy a contract code it may be seen as expected behavior.

The more complex scenario is if the implementation contract operator calls selfdestruct via delegatecall. Could be done down the road, when infrastructure relies on this.

This can be done intentionally and would cause a major disruption for dependent infrastructure.

Since it’s quite an edge case, I do think that this could be just mentioned in security considerations section: code index users MUST make sure that indexed contract has no ability to freely call self destruct via delegatecall. (Ownership renounced or no  embedded)

Perhaps, this might be a serious reason to consider moving this into EIP section, afaik SELFDESTRUCT doesn’t actually delete the contract’s storage from the Ethereum state. It just marks it as “empty,” hence if implemented on EVM level itself shouldn’t be a problem.

Also, the 7702 would raise similar concerns for  this standard btw.

[@SamWilsn](/u/samwilsn) perhaps eip editors have opinions on such cases?

---

**ownerlessinc** (2024-10-07):

Codehash / bytecode is already indexable by scanners such as Etherscan (although not perfect with some proxy mismatches), therefore I wonder who would be paying to index contracts and for what reason? I highly doubt contract deployers will willingly maintain the 7744 indexers updated with their deployments.

As you mentioned, there are easier ways to maintain track of bytecodes via EIPs but this would probably require a permanent gas increase for each deployment.  Also 7702 - with the directions EOAs working as CA is going this standard needs to include a way to map them as well.

It’s still unclear to me why this should be a standard by increasing the global deployment cost to track bytecode in an index with the final purpose of having the on-chain knowledge of who deployed what and when. I feel that this should be an optionality for protocols that want versioning tracking rather than a standard. Could you help me understand better the usage of the indexer [@peersky](/u/peersky) ?

---

**peersky** (2024-10-07):

Why do we use hashes in content addressing instead of location specifics? E.g in git?

Code index intention is to have reusable bytecode database, addresses are intrinsically flawed for that because of proxy patterns

---

**jochem-brouwer** (2024-10-07):

SELFDESTRUCT destroys the entire account, so it will destroy code, set the nonce to 0, the balance to 0, and it will also clear the storage. I am not entirely sure what scenario via delegatecall you have in mind.

Note, that since [EIP-6780: SELFDESTRUCT only in same transaction](https://eips.ethereum.org/EIPS/eip-6780) which got introduced in the Cancun hardfork, the behavior of SELFDESTRUCT is now changed. It is only possible to destroy the account in the same transaction where it got created. Thus, if the transaction is done, then if SELFDESTRUCT is called it will not destroy the code, reset the nonce, and clear the storage. (However, it will send the entire balance of the account to whatever argument is invoked to SELFDESTRUCT).

So only the pattern where in the tx a contract is created, it is added to the registry, and then (in same tx) the contract SELFDESTRUCTs allows to end up with a code pointer in the registry, but the code it points to is actually empty.

(So one way to mitigate this could be (but this is rather bad UX) is to ensure that the registry needs to register it “twice”, the first transaction adds it to the pending registry and registers what block number we are on. Then the second transaction confirms the registry by checking that the code hash of the account has not changed and the current block number is higher than the previously registered number. If that’s the case, then register the hash → address in the registry. This obviously will cost more gas, and users have to sign two txs (and they also have to ensure these two txs are mined in two different blocks)

---

**peersky** (2024-10-07):

Can older deployments on chain still use out of that rule selfdestruct?

---

**jochem-brouwer** (2024-10-07):

No, they behave the same: if they run into a SELFDESTRUCT then they will only send the balance to the target, but it will not destroy the account. So the only way to destroy a created contract is to do it in the same transaction as it was created. If it thus runs in SELFDESTRUCT and the contract was not created in that transaction, it will not destroy the contract and it will only send all funds of that contract to the target.

---

**peersky** (2024-10-07):

If that is just a constructor case, the attack vector would be to create such a contract, that mimics someones future deployment and therefore DoS dependent infrastructure.

I think could be done with better UX and without increasing gas for normal operations:

- During register function call:

IF contract is already indexed,

before reverting add another check:

query the reference

if it returns zero bytecode length:

re-index it with a newly specified address.

This would anyone who has a functional byte code to index it.

---

**jochem-brouwer** (2024-10-08):

Yes, this works too. However this means the current contract (which is pointed to by the EIP) should be changed (and thus gets a new address). I assumed this was not possible (but I als don’t know how popular this contract is / if it is being used in production). If it is not used in production, I suggest upgrading the contract to mitigate this issue.

EDIT: just checked, the contract is not deployed yet on mainnet. Together with the post below I think the contract logic (bytecode) plus the EIP will need a revamp regarding EIP7702.

---

**jochem-brouwer** (2024-10-08):

Oh, interesting, just saw your comment on the 7702 EIP. I had not thought of this case. This actually makes this hash → address registry even more nasty, because EOAs can now update their delegation (and therefore also their hash). EIP 7702 might actually completely break this EIP:

If you call EXTCODEHASH on a 7702-delegated EOA, it will actually **return the hash of the contract it was delegated to**.

So, if an “attacker” (in this case, this could also be a honest mistake), creates a contract and delegate their EOA to it, and then register the **EOA** (not the contract), then initially the hash mapping is correct. It will point to the EOA. Relevant code inspections via EVM will now be correct (these will **not** be correct over RPC, since RPC will report the 7702-delegated code (`0xef0100<address>`).

Now, to break the lookup, if the EOA delegates to another account the hash of the EOA will not be the same as in the registry. Also, the aforementioned check in registry to see if the code length is now zero could now not be the case (it could delegate to another contract).

I am not sure how to handle this, but 7702 will definitely break things.

---

**peersky** (2024-10-08):

I have it on arbitrum for testing purposes meanwhile, requesting community comments before doing any mainnet deployments :))

---

**peersky** (2025-01-18):

While this ERC is now proposed as EIP ([EIP7784](https://ethereum-magicians.org/t/eip-7784-getcontract-code/21325)) I still proceeded and implemented discussion feedback to move this on to review stage.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/855)














####


      `ethereum:master` ← `peersky:move-erc-7744-to-review`




          opened 05:48AM - 18 Jan 25 UTC



          [![peersky](https://avatars.githubusercontent.com/u/61459744?v=4)
            peersky](https://github.com/peersky)



          [+43
            -20](https://github.com/ethereum/ERCs/pull/855/files)







This PR concludes discussion that was facilitated on the Magician forums, partic[…](https://github.com/ethereum/ERCs/pull/855)ularly:

- Addresses self-destruct concerns
- Addresses EIP7702 delegated address concern
- Changes solidity file names according to standard number
- Changes salt and deployment address to accommodate bytecode changes
- New artifact was compiled with no metadata included to avoid bytecode changes if somone tries to re-compile it locally












- Addresses self-destruct concerns
- Addresses EIP7702 delegated address concern
- Changes solidity file names according to standard number
- Changes salt and deployment address to accommodate bytecode changes
- New artifact was compiled with no metadata included to avoid bytecode changes if somone tries to re-compile it locally

---

**peersky** (2025-04-25):

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1026/files)














####


      `master` ← `peersky:ERC7704-modify-erc7702-detection`




          opened 01:56AM - 25 Apr 25 UTC



          [![](https://avatars.githubusercontent.com/u/61459744?v=4)
            peersky](https://github.com/peersky)



          [+36
            -27](https://github.com/ethereum/ERCs/pull/1026/files)







- Renamed assets in directory to have corresponding names.
- Added latest 7702 […](https://github.com/ethereum/ERCs/pull/1026)changes to delegated EOA contract detection.
- Added more explicit compilation instructions to ensure nothing is hidden in my sleeve.












- Renamed assets in directory to have corresponding names.
- Added latest 7702 changes to delegated EOA contract detection.
- Added more explicit compilation instructions to ensure nothing is hidden in my sleeve.

