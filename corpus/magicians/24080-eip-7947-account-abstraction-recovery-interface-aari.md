---
source: magicians
topic_id: 24080
title: "EIP-7947: Account Abstraction Recovery Interface (AARI)"
author: Arvolear
date: "2025-05-07"
category: ERCs
tags: [wallet, account-abstraction, recovery]
url: https://ethereum-magicians.org/t/eip-7947-account-abstraction-recovery-interface-aari/24080
views: 742
likes: 14
posts_count: 13
---

# EIP-7947: Account Abstraction Recovery Interface (AARI)

UPDATE:

The [ERC-7947](https://eips.ethereum.org/EIPS/eip-7947) has been merged as a draft.

---

Hello magicians! Would love to hear what you think about this!

Check out the account abstraction recovery [demo](https://x.com/dr_zircuit/status/1918642455810871315) to understand where the initial EIP idea came from.

---

## Abstract

Introduce a universal account abstraction recovery mechanism `recoverAccess(subject, provider, proof)` along with recovery provider management functions for smart accounts to securely update their access subject.

## Motivation

Account abstraction and the “contractization” of EOAs are important Ethereum milestones for improving on-chain UX and off-chain security. A wide range of smart accounts emerge daily, aiming to simplify the steep onboarding curve for new users. The ultimate smart account experience is to never ask them to deal with private keys, yet still allow for full account control and access recovery. With the developments in the Zero-Knowledge Artificial Intelligence (ZKAI) and Zero-Knowledge Two Factor Authentication (ZK2FA) fields, settling on a common mechanism may even open the doors for “account recovery provider marketplaces” to emerge.

The account recovery approach described in this proposal allows for multiple recovery providers to coexist and provide a wide variety of unique recovery services. In simple terms, smart accounts become “recovery provider aggregators”, making it possible for the users to never rely on centralized services or projects.

The Account Abstraction Recovery Interface (AARI) aims to define a flexible interface for *any* smart account to implement, allowing users to actively manage their account recovery providers and restore the access of an account in case of a private key loss.

## Specification

Check out the full specification on GitHub:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1046)














####


      `master` ← `Arvolear:master`




          opened 02:04PM - 15 May 25 UTC



          [![](https://avatars.githubusercontent.com/u/47551140?v=4)
            Arvolear](https://github.com/Arvolear)



          [+171
            -0](https://github.com/ethereum/ERCs/pull/1046/files)







A quick one. Would love to hear your thoughts about this!












Check out the complete minimal reference implementation [here](https://github.com/rarimo/aari-contracts).

## Replies

**ivanmmurcia** (2025-05-07):

Hey,

IMO EIP-7702 must trigger the option to start getting rid of centralized MPCs that have the option to perform address-identity matching. This is where passkeys and proposals like this one that delegate recovery in a decentralized way come in. Looking forward to seeing how this proposal grows!

---

**Arvolear** (2025-05-15):

### It would be cool to discuss this one

I am still swinging between the current design and an option to define a common interface for the recovery providers to implement. Probably something like:

```solidity
interface IRecoveryProvider {
    /**
     * This function MUST be called from the `recoverOwnership` function on a smart account.
     */
    function checkRecovery(bytes memory proof) external view returns (bool);
}
```

This would mitigate several security concerns (the ERC20 example) while still maintaining the same level of compatibility.

---

**julianor** (2025-05-17):

Your original design is already lean, and I especially like the second option you outlined.

We can shave off the last bit of complexity by letting the recovery-provider contract handle *all* proof parsing and validation:

```auto
function recoverOwnership(address newOwner)
    external
    onlyRecoveryProvider   // modifier: require(recoveryProviderExists(msg.sender), "unauthorised")
    returns (bytes4 magic)
{
    // provider has already verified the proof off-chain or via `checkRecovery`
    _owner = newOwner;
    emit OwnershipRecovered(msg.sender, newOwner);
    return MAGIC;          // 0x3cfb167d
}
```

Questions:

1. What is the main reason to use the MAGIC?
2. Why not base the flow on a pre-signed message verified with ecrecover() (or contract signature validation) instead of keeping a provider list on-chain? Advantages:

- No on-chain whitelist until it’s needed.
- Safer backup: the owner can store a single, purpose-bound “recover to X” signature offline.

---

**Arvolear** (2025-05-19):

Hey, thanks for taking a look! I will probably update the spec to include the `IRecoveryProvider` interface for security reasons.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/julianor/48/13633_2.png) julianor:

> What is the main reason to use the MAGIC?

The idea here is just an additional sanity check like the one used in [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271). However, it may be beneficial to simplify the design to a mere `true/false`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/julianor/48/13633_2.png) julianor:

> Why not base the flow on a pre-signed message verified with ecrecover() (or contract signature validation) instead of keeping a provider list on-chain?

There are several advantages to doing it fully on-chain:

1. If we take a wallet that wants to support (integrate) several recovery providers, it could have a user onboarding page showing “Optionally add one of these providers to increase the security of your account”. Then we can implement an indexing service to properly present the user-added providers (no need for a wallet to store anything on-device).
2. Storing this “provider choice” signature off-chain may have its benefits, however it would probably get lost if a user decides to uninstall the app. With the current design, it is still possible to add a recovery prover via a signature and a sponsored multicall.

---

**Arvolear** (2025-06-02):

UPDATE:

1. Removed MAGIC from the recoverOwnership function and simplified the return value to be a bool.
2. Updated the specification section with the IRecoveryProvider interface that must be implemented by all the recovery providers.
3. Cleaned up the IAccountRecovery functions and outlined the full flow of the account recovery.
4. Started working on the reference implementation, will provide one soon.

Please check it out!

---

**Arvolear** (2025-06-05):

UPDATE:

The minimal reference implementation leveraging ERC-4337 `SimpleAccount` and a `RecoveryProvider` that verifies the knowledge of some hash preimage via a Groth16 proof is ready and available [here](https://github.com/rarimo/aari-contracts).

---

**ivanmmurcia** (2025-06-05):

Do you have some kind of diagram to understand more the EIP? I mean, I want to understand more about the “Account Recovery Provider Marketplaces” and how this EIP could work for a recovering of funds if I lose my device and I’m using, for example, passkeys to generate my SW with SimpleAccount.

Nvm, this work is cool, maybe a zkproof of my face and requesting the control of the previous SW and keep the funds safu moving to another? Could I do it if I lose the previous device to sign the recover transaction?

Thanks!

---

**Arvolear** (2025-06-19):

About the “Recovery Provider Marketplace”. I envision this as either a page inside a wallet or as a standalone dapp. A user will be asked if they want to add a new recovery method to their account, and then call `addRecoveryProvider()` under the hood.

If you lose your device, you can still download the wallet and recover the account via the previously added recovery providers. You will still remember your account address, won’t you?

In the simplest form, the recovery can be a password as shown in the [reference implementation](https://github.com/rarimo/aari-contracts). In a more complex scenario, it can be a ZKML face recognition neural net, but maintaining backward compatibility may be challenging for the wallet.

---

**SamWilsn** (2025-06-19):

Some non-editorial comments:

- The name recoveryProviderExists is a bit odd, since the recovery provider exists regardless of whether it has been added to the account. Perhaps recoveryProviderEnabled, recoveryProviderActive, or recoveryProviderAdded?
- Have you considered ERC-165?
- Should this standard depend on ERC-173?
- In your motivation, you should explain why someone would want this standard over, say, setting the recovery provider as the owner (and having it proxy function calls). There’s probably an obvious downside, but it is the de facto approach that works today.

[Corresponding editorial comments](https://github.com/ethereum/ERCs/pull/1046#pullrequestreview-2943422207).

---

**Arvolear** (2025-06-21):

Thanks for a comprehensive review. Appreciate it very much!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> The name recoveryProviderExists is a bit odd, since the recovery provider exists regardless of whether it has been added to the account.

Agree. Renamed the function to `recoveryProviderAdded`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Have you considered ERC-165?

Actually, I have thought about adding it to the recovery provider interface, but currently I see no obvious upside for this requirement. Wallets and dapps would probably support recovery providers on an individual integration basis. And adding ERC-165 to an account looks like unnecessary complexity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Should this standard depend on ERC-173?

That’s a good question. Implicitly, the standard requires some kind of ownership, but I don’t want to restrict it solely to EIP-173. For example, a smart account may support some kind of 2FA or ZK2FA upon every `execute` action. In case of a private key compromise, a user could still recover the account ownership using EIP-7947. However, if an account inherited EIP-173, the `transferOwnership` function would not allow that, and a hacker would gain full control over the account.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> In your motivation, you should explain why someone would want this standard over, say, setting the recovery provider as the owner (and having it proxy function calls). There’s probably an obvious downside, but it is the de facto approach that works today.

Extended the motivation section a bit.

---

**Joachim-Lebrun** (2025-08-07):

Interesting ERC, thanks for your work on this !

I was wondering, wouldn’t it make sense to even abstract further the role that is being recovered? Some contracts don’t use ERC-173 to manage ownership over a contract, instead they have some different access control implemented.

However if the standard doesn’t change it should say that ERC-173 interfaces are expected for the account ownership, don’t you think?

EDIT : I didn’t read that this question was already answered above, great minds think alike ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

I get your point about the ownership being potentially something else [@Arvolear](/u/arvolear) and it makes sense, but the term Owner in the context of solidity contracts is deeply tied to ERC-173 after years and years of using it everywhere, so i still believe it would make sense to rename the functions if you want to make it agnostic on that side. Could be `recoverAccess` and event `AccessRecovered` or something similar.

---

**Arvolear** (2025-08-11):

Hey, thanks for checking out the proposal. The ERC-173 echoes hard, so updated the interface to be more general-purpose. Now the recovery function signature is the following:

```auto
function recoverAccess(
    bytes memory subject,
    address provider,
    bytes memory proof
) external returns (bool);
```

Changed the previously used owner `address` to an arbitrary `bytes` to enable recovery of a wider range of access options.

