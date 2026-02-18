---
source: magicians
topic_id: 21237
title: "ERC-7779: Interoperable Delegated Account"
author: DavidKim
date: "2024-10-01"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-7779-interoperable-delegated-account/21237
views: 672
likes: 11
posts_count: 13
---

# ERC-7779: Interoperable Delegated Account

## Abstract

This proposal outlines the interfaces to make delegated EOAs interoperable after the merge of EIP-7702. With EIP-7702, EOAs will be able to enable execution abstraction, which leads to a more feature-rich account, including gas sponsorship, batch execution, and more.

However, there is a need to help facilitate storage management for redelegation, as invalid management of storage may incur storage collisions that can lead to unexpected behavior of accounts (e.g., account getting locked, security vulnerabilities, etc)

The interface `InteroperableDelegatedAccount` suggests the interfaces for delegated EOAs to be interoperable and facilitate a better environment for redelegation.

## Motivation

After the merge of EIP-7702, it is expected that a considerable number of EOA wallets will migrate from pure EOA accounts to delegated EOA accounts.

This is to enable a more appealing wallet UX, including a 1-step swap, automated subscription, gas sponsorship, and more.

However, considering the fact that delegated EOAs will utilize its own storage bound to their Smart Account implementation, the storage management is essential to foster migration between wallets to better ensure sovereignty of users to freely migrate their wallet app whenever they want.

EOA (Externally Owned Account) is currently comprised of cryptographic key pair that is mostly managed in the form of mnemonic phrase.

This simplicity provided frictionless interoperability between wallets that gave users the freedom to freely migrate between different wallet applications.

However, after the merge of EIP-7702, each EOA will be given the ability to delegate itself to a smart account which will impact migration as storage remains in the continuous context while EOA can be delegated to diverse smart accounts if the user migrates their wallet.

Account Abstraction Wallets, given the wallet-specific validation and execution logic, also have the interoperability issue to be considered but its importance in EOA is much more significant as EOA users are already familiar with wallet migration and its a common action to migrate wallets.

This spec provides a standard approach for fetching the storage base used in the delegated account together with an optional mechanism to clean up the storage.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

```solidity
interface IInteroperableDelegatedAccount {
	/*
	 * @dev    Provides the namespace of the account.
	 *         namespace of accounts can possibly include, account version, account name, wallet vendor name, etc
	 * @notice this standard does not standardize the namespace format
	 * e.g.,   "v0.1.2.7702Account.WalletProjectA"
	 */
	function accountId() external view returns (string);

	/*
	 * @dev    Externally shares the storage bases that has been used throughout the account.
	 *         Majority of 7702 accounts will have their distinctive storage base to reduce the chance of storage collision.
	 *         This allows the external entities to know what the storage base is of the account.
	 *         Wallets willing to redelegate already-delegated accounts should call accountStorageBase() to check if it confirms with the account it plans to redelegate.
	 *
	 *         The bytes32 array should be stored at the storage slot: keccak(keccak('InteroperableDelegatedAccount.ERC.Storage')-1) & ~0xff
	 *         This is an append-only array so newly redelegated accounts should not overwrite the storage at this slot, but just append their base to the array.
	 *         This append operation should be done during the initialization of the account.
	 */
	function accountStorageBases() external view returns (bytes32[]);
}
```

```solidity
interface IRedelegableDelegatedAccount {
	/*
	 * @dev    Function called before redelegation.
	 *         This function should prepare the account for a delegation to a different implementation.
	 *         This function could be triggered by the new wallet that wants to redelegate an already delegated EOA.
	 *         It should uninitialize storages if needed and execute wallet-specific logic to prepare for redelegation.
	 *         msg.sender should be the owner of the account.
	 */
	function onRedelegation() external returns (bool);
}
```

Accounts MUST implement the `IInteroperableDelegatedAccount` to be compliant with the standard.

Accounts MAY implement the `IRedelegableDelegatedAccount`.

### accountId()

This function is a view function to fetch the account information.

A use case for this could be wallet showing the redelegation process e.g., Are you willing to migrate your account `“Wallet A” → “Wallet B”`.

Wallet A information could be extracted from `accountId()`.

### accountStorageBases()

This function returns the list of base storage slots of that account has used.

7702 Accounts do plan to use a custom non-zero storage slot to avoid storage collision as much as possible, however, there hasn’t been a standardized approach on how to fetch them.

This function provides a standardized approach for wallets and other applications to check the base storage slots of an account, and verify if the base storage slots are far enough from the newly to-be-redelegated account’s base storage slot.

Note that there could be some exceptions for mappings, etc depending on how account manages storage.

This provides Wallets and applications a standard approach to fetch the base storage slots for verification rather than just relying on the probability of hash.

If the account uses external storage, it should return ERC Number prefixed slot with the external storage contract address concatenated.

```solidity
..N...
```

For example, if the storage contract address is `0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` the returned value should be

```auto
0x777977797779777977797779AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

When the account is delegated(e.g., during the account initialization stage), the account implementation should append the base storage slot of the account to the following slot position: `keccak(keccak('InteroperableDelegatedAccount.ERC.Storage')-1) & ~0xff` .

The storage variable would be using the `bytes32[]` type and is an append-only variable which newly delegated accounts append its storage slot hash. The account may choose to not append its storage base to an array if there is an identical entry that already exist.

In case the account identifies that there are colliding storage bases, the account can perform further storage verification either off-chain or on-chain and decide whether the delegation would happen.

Wallet may revert the delegation if the colliding storage includes a suspicious storage values that may target the user(e.g., shadow signer, etc).

### onRedelegation()

This function is to prepare for the redelegation to a new account.

When this function is called, the existing delegated account should perform actions to not limit or impact the user when the user redelegates to a new account as much as possible.

For example, the account could uninitialize the storage variables as much as it can to provide clean storage for new wallet.

This standard, however, does not explicitly state the behavior to be done during this function call as wallet implementations have very distinctive architecture and details.

**The standard expect the wallet implementation to revert it back to a clean storage state *as much as possible*** with this function.

`onRedelegation()` should validate if the caller is indeed the authorized user by checking the `msg.sender` value.

This could also be done through a `self-call` if a custom validation scheme is implemented or at the wallet’s discretion as a side case.

[![diagram showing the flow of onredelegation](https://ethereum-magicians.org/uploads/default/original/2X/e/e14d32eb7745b4e88a147c6de935318b3f9775b8.png)diagram showing the flow of onredelegation639×208 15.5 KB](https://ethereum-magicians.org/uploads/default/e14d32eb7745b4e88a147c6de935318b3f9775b8)

## Rationale

### Storage base checks

This standard is designed with the need of wallets to validate the storage of the EOA, even if some may consider that the probability of hash is already big that the account doesn’t have to check, assuming that each wallet uses a different storage base slot.

In fact, this standard thinks exactly the opposite. It is worth scanning the storage, or at least the storage that the delegated account will use, which the wallet wants to delegate to. E.g., Just like developers validating the storage of Facets in Diamond (ERC-2535) to prevent storage collision and not just relying on hash probability.

In line with this, the `accountStorageBases()` was designed to not only return the storage base of the current wallet implementation, but return the full historical storage slots that the account has used.

This could provide valuable information for the storage scanning of the EOA before delegation.

### Optional onRedelegation()

`onRedelegation()` was designed to be optional to lower the barrier of being compliant with this standard. Also, there could be accounts that does not functionally require a hook-logic to be in place before redelegation, or accounts that does not suite with the design principle of the `onRedelegation()` e.g., excessive use of mapping or data types that’s hard to uninitialize.

It is worth noting that, `onRedelegation()` does not obligate the account to completely whipe out it’s storage. It’s more of a best effort function to leave the cleanest stage for the future use of the EOA in a new wallet. Or to execute a function to prepare for redelegation.

## Backwards Compatibility

Existing smart accounts that was built prior to the EIP-7702 discussion will need changes to support this standard.

This standard was specifically for Smart Accounts for EOA, but this could be applied further to diverse cases and architecture.

## Security Considerations

1. Calling onRedelegation() should include security mechanism to properly authentication the owner.
2. This standard enforces the accounts to

provide proper Base Storage Slot when accountStorageBase() is called
3. perform proper actions to make account storage to a clean state as much as possible (e.g., uninitialization of storage variables, etc) IF the account supports onRedelegation()

However, whether the account follows the above three enforcements with behavioral actions is dependant of the account.

If needed, accounts may check the authenticity of the information through off-chain approaches.

Wiping out the storage completely may not be an adaptable action depending on how account implementation manages storage.

This standard recommends the account to completely wipe out its storage, however, exceptions apply if the account is incapable of doing that.

In the case when the account cannot completely wipe out its storage, the standard expect the account to perform the best degree of action it can do to support the redelegation operation for the user.

Also, the account should make sure the initializer cannot be triggered by an arbitrary entity after `onRedelegation()` is called.

`onRedelegation()` should not reset the replay protection considering that it could incur a vulnerability(e.g., signature reply attack).

It is worth noting that this standard is an ERC, which means that even if the ERC enforces it, the actual implementation may not be compliant with it. e.g., accounts pretending to support this standard which is not, in fact. So it is recommend to validate if the account is a know implementation that is secure and compliant with the standard.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**dror** (2024-10-08):

I’m trying to understand when “accountStorageBases” are needed?

each wallet is required to have a unique storage base.

Since this value is derived from a keccak (over a string), these values are randomly distributed on the 2**256 range, and roughy 2**128 apart.

That’s “far enough” for any practical reason, so the above arrays are not in real use.

I think that an upgrade should be an “upgradeAccountFromAtoB”, which reads “A” configuration (from A’s storage map) and put values into B’s storage map.

Obviously, the wallet supports both “A” and “B”, and thus also this upgrade method.

I don’t think that a “generic” interface can help in this case.

even the “accountId” generic function doesn’t help much: unless the wallet knows both implementations (and method to upgrade between), it can’t do anything, and the “title” of the account implementation doesn’t help much.

There is a case for wallets which don’t use storage properly, but this interface doesn’t help to detect them either.

---

**DavidKim** (2024-11-02):

The use case of AccountStorageBases is shared in the ERC.

To elaborate it further:

> I’m trying to understand when “accountStorageBases” are needed?

1. Before delegation, the wallet software can take this as a reference to scan the storage of the account and make sure the new account implementation that it will delegate to is indeed not affected by previous storage.

> Since this value is derived from a keccak (over a string), these values are randomly distributed on the 2256 range, and roughy 2 128 apart.

1. The probability of the hash being large does not justify that validating the storage beforehand is useless. Note that it’s a security best practice to check if storage hash is indeed far from each other in Diamond Storage for Facets, according to your argument this shouldn’t be the case, which is not in reality.

> There is a case for wallets which don’t use storage properly, but this interface doesn’t help to detect them either.

1. As all ERCs are, there is nothing we can enforce. Because developing a smart contract is totally up to the developer. However, this is a social consensus between wallets/accounts to adhere and comply with this standard, just like any other ERC.
2. Actually, regarding the real use case, numerous wallet vendors(e.g., Safe, Alchemy, etc) already agreed on the use case and need for this ERC. It’s better to have a way to identify storage in an easier way to take it as a reference rather than having nothing at all.

> even the “accountId” generic function doesn’t help much

1. The use case of accountId has already been shared in numerous ERCs, including ERC-6900 & ERC-7579.

Regarding your point here:

> I think that an upgrade should be an “upgradeAccountFromAtoB”, which reads “A” configuration (from A’s storage map) and put values into B’s storage map.

I don’t think this would be the case in reality, upgrade from Wallet A → Wallet B will happen through 7702 redelegation, not through a contract function call.

It’s much more complicated to do it through contract function call, and even the proxy implementation can be completely different e.g., some using UUPS, some using Diamond, etc.

Moreover, it means each wallet should be aware of how others implement and implement the `upgradeAccountFromAtoB` function, which is far from reality.

---

**dror** (2024-11-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> The probability of the hash being large does not justify that validating the storage beforehand is useless

If your argument is correct, then having a single contract with multiple maps couldn’t be treated as secure.

e.g. each token has a map of balances, and a second map of approvals. It is implicitly assumed that there could be no collisions between these maps, and nobody check for it (and in fact, it is impossible to check for collisions, since there is no way to enumerate all values)

---

**DavidKim** (2024-11-06):

So are you insisting that not doing checks is better than performing checks?

Also, I don’t think your analogy makes much sense.

For mappings, the compiler/evm sets a different slot/hash value by itself with different values. But for this case, developers manually set them.

---

**dror** (2024-11-20):

There is a standard of using namespaced stroage, ERC-7201

If a contract is compliant (that is, all its storage is done within this namespace), and you upgrade to another compliant contract, then there can’t be any conflict.

So as you don’t expect to have balance/approvals overlaps in tokens (even in highly used ones, like USDC/WETH/etc), there is unlikely chance for overlap between such two audited namedpsaced contracts.

If the contracts are not namespaced and audited, then you shouldn’t trust them even with a storage-scanning technique.

---

**wjmelements** (2024-11-20):

Instead of having the contracts list out their storage, it would be better to build up a registry to document backwards compatibility for common wallet contracts, so that wallet software can easily identify that compatibility. With this standard it isn’t possible to know whether an overlap indicates compatibility or not. I would prefer a solution that does not require the account code to implement any specific ABI.

---

**DavidKim** (2024-11-29):

This contract also leverages the ERC 7201 namespace storage to append the storage slots.

I think the point is that performing no checks at all and only relying on this is not recommended.

For instance,

> If the contracts are not namespaced and audited, then you shouldn’t trust them even with a storage-scanning technique.

The above you mentioned above requires the scanning of the EOA and performing diverse checks.(e.g., Tx of the EOA, previous delegation designation, etc).

So from a wallet perspective, it requires a check either way. (including what you mentioned)

If the account previously delegated to trusted 7702 account implementation(s), this ERC helps them to check the storage in a better fashion.

---

**DavidKim** (2024-11-29):

I’m not very sure if a Registry type of approach could be a good solution in reality.

The storage of the EOA is very address specific, meaning that a registry outlining the storage it uses does not fully dictate the storage of EOA.

Also, registry may incur the issue of the authority of who can register in the registry and who can not.

> it would be better to build up a registry to document backwards compatibility for common wallet contracts

Who and what defines the “common wallet contracts” creates layers of complexity and it may be sensitive to centralization risk, because if this registry gets commonly used between wallet software as the “trusted common wallets” then it creates politics which then requires much attention to how we(the ecosystem) manage it fairly.

---

**wjmelements** (2024-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> Also, registry may incur the issue of the authority of who can register in the registry and who can not.

Generally the software developers are interested in noting the compatibility of their software. It’s possible to identify who is the developer and let them document their own code. There could even be competing attestations and authorities, eg auditors.

An ideal solution would do on-chain static analysis either directly or by validating some ZK proof, but that likely wouldn’t be sufficiently flexible. I don’t think compatibility can be proven in the general case.

---

**fmc** (2024-12-24):

Have you guys considered accepting `bytes calldata data` param in `onRedelegation()` ?

It can be useful, for example for ERC-7579 accounts, to call `onUnistall` methods on modules.

---

**marcelomorgado** (2025-02-25):

FYI there is this interesting proposal here [Prototype external storage contract for 7702 CoinbaseSmartWallets by amiecorso · Pull Request #108 · coinbase/smart-wallet · GitHub](https://github.com/coinbase/smart-wallet/pull/108) that try to address the storage issue. The approach is basically to having EXTCODEHASH as part of the namespacing calculation to ensure no conflicts. The caveat is that requires storage migration when upgrading the wallet to a new version.

---

**livingrockrises** (2025-05-07):

Can we finalise this?

