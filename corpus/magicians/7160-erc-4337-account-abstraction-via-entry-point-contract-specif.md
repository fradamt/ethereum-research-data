---
source: magicians
topic_id: 7160
title: "ERC-4337: Account Abstraction via Entry Point Contract specification"
author: vbuterin
date: "2021-09-29"
category: ERCs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/erc-4337-account-abstraction-via-entry-point-contract-specification/7160
views: 40847
likes: 177
posts_count: 147
---

# ERC-4337: Account Abstraction via Entry Point Contract specification

An account abstraction proposal which completely avoids the need for consensus-layer protocol changes, instead relying on a separate mempool of `UserOperation` objects and miners running either custom code or a bundle marketplace.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4337)














####


      `master` ← `vbuterin-patch-1`




          opened 08:57AM - 29 Sep 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/1X/882285f3628ea3784835c306639dd8f62179a6d9.png)
            vbuterin](https://github.com/vbuterin)



          [+331
            -0](https://github.com/ethereum/EIPs/pull/4337/files)







An account abstraction proposal which completely avoids the need for consensus-l[…](https://github.com/ethereum/EIPs/pull/4337)ayer protocol changes, instead relying on a separate mempool of `UserOperation` objects and miners either running custom code or connecting to a bundle marketplace.

## Replies

**Agusx1211** (2021-09-29):

The proposal looks awesome! We worked on a very similar set of contracts under the name of “Sequence”, in short is pretty much the same system, with the key difference that `handleOp` and `verifyUserOp` are bundled together on the same `execute` function. The relayer has to simulate this `execute` function with a fixed amount of gas and see if it’s going to get paid or not before sending the transaction.

The contracts are here: https://github.com/0xsequence/wallet-contracts

The cool thing is that our system could be upgraded to support this new standard, after all wallets are upgradable, and we could split our `execute` function into `verifyUserOp` and `handleOp`.

The only roadblock I see is that we already have our own “Wallet factory”, it uses CREATE2 in pretty much the exact same way ERC4337 does (https://github.com/0xsequence/wallet-contracts/blob/master/src/contracts/Factory.sol) and wallets are indeed counter-factual, but afaik ERC4337 wallets must be created using the `EntryPoint` contract as factory. Thus our wallet addresses couldn’t benefit from the `initCode` property on the relayer network, because the resulting addresses would be different.

I wonder if this is an implementation detail or something by design, because by allowing contracts as wallet factories we could allow existing smart contract wallet implementations to be retrofitted without having to re-deploy all counter-factual accounts. I imagine this issue affects not only Sequence but also Gnosis, Argent, etc.

A possible solution could be to split `initCode` into two fields: `initCode` and `initAddress`, the creation of the wallet involves calling `initAddress` with `initCode` as data, after that `EntryPoint` could validate if the account address now contains code.

The trusts assumptions are the more or less the same, and any restrictions put on `initCode` (call external contracts, use timestamp, etc) could also be applied to `initAddress`.

---

**vbuterin** (2021-09-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> ERC4337 wallets must be created using the EntryPoint contract as factory

I don’t think this is technically true; you can use ERC 4337 with wallets created in other ways, you just would not be able to create the wallet without a paymaster.

> A possible solution could be to split initCode into two fields: initCode and initAddress, the creation of the wallet involves calling initAddress with initCode as data, after that EntryPoint could validate if the account address now contains code.

Interesting! Need to think about whether or not it’s safe to call into arbitrary addresses as contract creators… or if it’s a useful idea. Perhaps instead we should just agree on a chain-wide generic factory contract that everything gets created through (this would have other use cases, eg. if users using account-abstracted wallets want to create new contracts, they could do it through the factory instead of the wallet supporting a separate creation mechanism).

---

**JamesZaki** (2021-09-30):

Great write-up ![:nerd_face:](https://ethereum-magicians.org/images/emoji/twitter/nerd_face.png?v=12)

FYI, another implementation in progress (with a previous version tested on Optimism and Arbitrum testnets) can be found [here](https://github.com/jzaki/bls-wallet-contracts), it’s focus is on using BLS signature aggregation.

“EntryPoint” is [VerificationGateway](https://github.com/jzaki/bls-wallet-contracts/blob/main/contracts/VerificationGateway.sol#L89) (cleanup in progress), the wallet contract is BLSWallet, and “Bundler” is [bls-wallet-aggregator](https://github.com/jzaki/bls-wallet-aggregator) repo.

Which will go beyond just contract wallets, introducing significant savings on L1 by reducing L2 calldata (1 instead of n BLS sigs in a “bundle”).

> Perhaps instead we should just agree on a chain-wide generic factory contract that everything gets created through

This is the current design for VerificationGateway, but the indirection through aggregators and user bls keys I think rules out deterministic wallet addresses.

---

**vbuterin** (2021-09-30):

Happy to hear there’s work being done on this! Does your BLS wallet aggregate transactions across operations? That’s a feature that, while not especially useful for regular wallets because calldata costs are not that high relative to ECPAIRING costs, is a lifesaver for optimistic rollups. Would be interesting to see how it could be incorporated into the same standard.

---

**JamesZaki** (2021-09-30):

> Happy to hear there’s work being done on this!

Thanks EF ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> across operations

I have a card in the github project: “Consider design of single signature for multiple txs (eg exchanges frequent need of `approve` then `transfer`)”, if that is what you mean?

Currently an aggregator (server) would put together bls-signed tx data for an arbitrary set of txs (from any blswallet) that fit in an L2 tx, they could be txs from the same address with consecutive nonces, each individually signed-for though (before aggregation).

---

**vbuterin** (2021-09-30):

The bundler should be able to take all the BLS signatures in the user operations, and combine them together into a single BLS aggregate signature that goes on chain. When verifying the ops, the contract would extract the entire list of (pubkey, msghash) pairs that wallet verification execution expects, and check the aggregate signature against that whole list.

Is that what you have in mind?

---

**JamesZaki** (2021-09-30):

Yes, that’s what it does → [bls-wallet-contracts/VerificationGateway.sol at main · jzaki/bls-wallet-contracts · GitHub](https://github.com/jzaki/bls-wallet-contracts/blob/main/contracts/VerificationGateway.sol#L105)

EDIT: bundling [here](https://github.com/jzaki/bls-wallet-aggregator/blob/main/src/app/WalletService.ts#L130)

---

**rmeissner** (2021-09-30):

This sounds very similar to https://docs.opengsn.org/ Did you look into this and where there are parallels and differences? Also something like this has been attempted in the past with [EIP-1077: Gas relay for contract calls](https://eips.ethereum.org/EIPS/eip-1077). I would love to see what is different from then to now.

I also think that pushing [EIP-2937: SET_INDESTRUCTIBLE opcode](https://eips.ethereum.org/EIPS/eip-2937) with that would be super helpful as it would enable more wallet to comply to this. For example the current Gnosis Safe setup would not be usable with the current proposal as it supports delegatecalls.

I would also be interested in what relation the Bundlers stand to the Miners/Validators. It sounds like these would be a complete different service. Or would you expect this to be part of a default Miner/Validator setup.

---

**vbuterin** (2021-10-03):

> I would also be interested in what relation the Bundlers stand to the Miners/Validators. It sounds like these would be a complete different service. Or would you expect this to be part of a default Miner/Validator setup.

Bundlers would either be miners/validators, or they would be actors publishing bundle txs through Flashbots.

---

**StanislavBreadless** (2022-02-02):

Excuse me if I misunderstood something, but I could not find how the `preVerificationGas` field is handled. Or is it the responsibility of the account abstraction account to handle and use these fields correctly?

Especially what’s interesting is at what step the `preVerificationGas` is paid.

---

**dror** (2022-02-02):

`preVerificationGas` covers all the gas that can’t be checked on-chain using gasleft() deltas, but is known to be paid by both the calling user and the miner.

It covers static gas cost (e.g 21000 stipend, and little more used by handleOps other), and dynamic cost which depends on actual UserOp structure (e.g calldata cost, and memory usage/copy into the inner methods of handleOps.

---

**StanislavBreadless** (2022-02-03):

But how is it charged from the user?

Do I get it right that it is the responsibility of the user account to pay for it? The same as for the actual fee? In the specification, `preVerificationGas` is a part of `UserOperation`.

That means that there is no way to enforce that the miner (or the one who submits this bundle of `UserOperation`s) will get paid.

---

**dror** (2022-02-05):

To summarize the complete transaction payment:

- The EntryPoint calculate the total cost of the UserOp, and charges the wallet (or paymaster) for that and transfer that amount to the bundler/miner.
- the payment is split into 2 parts: those we can calculate on-chain (using gasleft() wrappers), and those we can’t.
- the paymaster calculates the cost of verification, target call gas (and postOp, in case a paymaster is used to pay instead of the wallet itself.)
- to this value it adds the preVerificationGas, which should be set to the excess (calldata cost, and some static cost we can’t calculate on-chain)
- The preVerificationGas is calculated by the user who creates and signs the request.
- The bundler/miner - verifies this value before putting it on-chain, to make sure it makes profit on this transaction.

Notes:

- The UserOp contains 2 other gas values, the verificationGas and callGas. The user/paymaster must have balance to pay these values, but eventually pay only for the actual used gas. The preVerificationGas is paid in full.
- preVerificationGas name is misleading a little: most of its value indeed comes before the verification, but it covers also some static overhead that comes later.

---

**jacekv** (2022-02-09):

The ERC looks pretty good, yet I was wondering about adding a `chainId` field into the UserOperation.

Since transactions have it ([EIP-155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md)) to prevent replay attacks, I believe the same attack vector comes in play in regards the UserOperations. Or am I wrong?

---

**yoavw** (2022-02-09):

Thanks, you are right, and the [implementation](https://github.com/eth-infinitism/account-abstraction/blob/main/contracts/EntryPoint.sol#L173) actually covers `chainId` as part of the signature.  The UserOperation struct doesn’t include a chain ID field, but it is appended before signing/verifying.  The EIP should reflect that as well.

---

**jacekv** (2022-02-09):

[@yoavw](/u/yoavw) Thanks for linking it to the contract. I am not sure how this is going to prevent replay attacks. The `chainId` is taken from the block and hashed with the UserOperation. As an attacker, I still could take the UserOperation and use it on a different chain, or not?

Is there something I am overlooking?

---

**yoavw** (2022-02-09):

The user signed `userOp.hash(), address(this), block.chainid` and taht’s what the wallet will verify. This signature is a part of the the UserOperation.  If someone relays the same UserOperation on another chain with a different chainid, the wallet will revert during its `validateUserOp` because the signature won’t match  the `requestId` it receives from EntryPoint.

Do you see a way to bypass that, and successfully replay the UserOperation on a chain with a different `chainId`?

---

**jacekv** (2022-02-09):

Alright, I get the flow know and was able to follow the steps in the code ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10) Thanks for the explanation [@yoavw](/u/yoavw)

---

**tjade273** (2022-03-22):

> Note that balance cannot be read in any case because of the forbidden opcode restriction. Writing balance (via value-bearing calls) to any address is not restricted.

Doesn’t allowing value-bearing called essentially allow reading the balance of an account?

For example, if the wallet includes this in `validateUserOp`

```auto
bool success = this.send(500);
```

`success` will contain 1 iff the contract contains at least 500 wei. If we want the exact balance, we can just binary search.

Also, what happens if the wallet has all funds removed between simulation time and run time? Is the idea that this shouldn’t be possible because the `handleOps` call will always be the first transaction in a block?.

---

**yoavw** (2022-03-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjade273/48/5715_2.png) tjade273:

> Doesn’t allowing value-bearing called essentially allow reading the balance of an account?

Yes, the wallet could check its own balance this way, much like it could check its own storage. The user would be able to invalidate an op that is already in the mempool by using a non-op transaction to change the wallet’s balance.

However, the wallet can only check its own value this way, so it can only be used to invalidate the op of a single wallet at a time.  The wallet could similarly use a separate transaction to update its nonce and invalidate the op.

Your question does highlight an important point - that the client should treat the value as part of the account state, and not just the storage.  I.e. if a wallet calls a function in a 3rd party contract, which doesn’t access storage but does attempt to send value, the clients shouldn’t accept it.  Otherwise this could be used to invalidate ops of multiple wallets.

The EIP specifies this condition: `The first call does not access mutable state of any contract except the wallet itself and its deposit in the entry point contract.`

I now edited it to clarify that `mutable state` includes both value and storage. Thanks for bringing it up.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjade273/48/5715_2.png) tjade273:

> Also, what happens if the wallet has all funds removed between simulation time and run time? Is the idea that this shouldn’t be possible because the handleOps call will always be the first transaction in a block?.

The simulation is performed against the latest state while building the block. It is the block proposer’s responsibility to ensure that an earlier transaction in the block doesn’t invalidate an op.  The simplest way to do it is what you suggested - make the `handleOps` call in the first transaction in the block.  A client could simulate it against a mid-block state or use access lists to prevent conflicts, but making it first is easier.  The current client implementations already do this, but I now added a comment to the EIP to make this requirement clearer.

Thanks for highlighting these points!  Client developers need to take them into account.


*(126 more replies not shown)*
