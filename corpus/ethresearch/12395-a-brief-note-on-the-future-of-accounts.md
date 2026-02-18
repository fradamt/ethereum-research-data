---
source: ethresearch
topic_id: 12395
title: A brief note on the future of accounts
author: SamWilsn
date: "2022-04-13"
category: Execution Layer Research
tags: [account-abstraction]
url: https://ethresear.ch/t/a-brief-note-on-the-future-of-accounts/12395
views: 7745
likes: 13
posts_count: 12
---

# A brief note on the future of accounts

Future visions for Ethereum have [included](https://vitalik.ca/general/2021/01/11/recovery.html) smart contract wallets for some time. Not only do smart contract wallets improve efficiency and user experience, they provide a general way to mitigate cryptographic weaknesses (like ECDSA being vulnerable to quantum computing.)

The future of accounts is a wide open design space. We present a few rough options to migrate existing EOAs to smart contract wallets: forcibly migrate current EOAs, assume a default contract, a new transaction type, and a newly proposed opcode (`AUTHUSURP`) plus [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074).

For the purposes of this post, deploying bytecode may refer to actually deploying bytecode in the current sense, or setting a delegate/proxy field on the account in the verkle trie.

## Approaches

### Forced Deployment

#### What is it?

Perform an irregular state transition to deploy bytecode into every account that may have been an EOA.

#### Benefits

Irregular state transitions are a one-time cost, and this change could be performed alongside another state transition (like verkle trees.)

#### Drawbacks

The first major drawback to this approach is that if you’re going to deploy bytecode, you need to have some bytecode to deploy. You’d need to implement, at minimum, a call function and some upgrade functionality.

This approach will also break any system of contracts that relies on `SELFDESTRUCT` and `CREATE2`, if the account is migrated between the `SELFDESTRUCT` and the `CREATE2`. There are, however, [plans to remove SELFDESTRUCT](https://eips.ethereum.org/EIPS/eip-4758) so these contracts may break anyway.

Counterfactual contracts, even without `SELFDESTRUCT`, would break as well.

Finally, this approach has a high cost to miners/validators, because every existing EOA has to be touched and modified.

### Assume a Default Contract

#### What is it?

If a transaction originates from an account with no code, pretend that account had some default code which behaves like an EOA.

#### Benefits

Unlike actually modifying the state above, this approach does not have a one-time cost.

Since the bytecode isn’t actually deployed anywhere, it’s possible to upgrade it and add features over time.

Counterfactual contract deployments would not be entirely broken.

#### Drawbacks

While the default bytecode can be upgraded over time, you still need an implementation to execute, which may or may not do everything users need.

### Create Transaction Type

#### What is it?

Introduce a new [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718) transaction type that deploys code at the transaction signer’s address.

#### Benefits

No one-time cost to miners/validators.

No need to create a single contract that would be deployed everywhere, instead users could choose what to deploy.

#### Drawbacks

The signing account must have a non-negligible ether balance to upgrade.

### AUTH + AUTHUSURP

Leveraging the `AUTH` opcode from [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074), create a new opcode `AUTHUSURP` that deploys code at the `authorized` address.

#### Benefits

Just like the new transaction type above, this approach has no one-time cost to miners/validators, and users can choose what to deploy.

Also works well with sponsored transactions: the account to be upgraded doesn’t need an ether balance.

#### Drawbacks

Comes with the drawbacks of EIP-3074: invokers potentially have total control over an account, it breaks some rare flash loan protections, and consumes three opcodes that might become deprecated in the future.

## Conclusion

As far as the above options go, only three are serious candidates. Deploying bytecode and permanently breaking counterfactual deployments is unacceptable.

Assuming a default contract is reasonable, but takes an opinionated stance on what a smart contract wallet will look like. Allowing users to choose their wallet—either an EOA or smart, either with a new transaction type or with `AUTHUSURP`—is more in line with the Ethereum ethos.

At the risk of letting my biases show through, I believe EIP-3074 brings a lot of benefits for users today, and—coupled with the `AUTHUSURP` migration path off of EOAs—is a great direction to pursue.

Are there other approaches to migration that aren’t listed here? If so, I’d love to know!

---

Stay tuned for a companion post on how EIP-3074 might work in a post-EOA world!

## Replies

**MicahZoltu** (2022-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/samwilsn/48/4301_2.png) SamWilsn:

> Allowing users to choose their wallet—either with a new transaction type or with AUTHUSURP—is more in line with the Ethereum ethos.

I agree that allowing users to choose their wallet is in line with the Ethereum ethos.  Perhaps what you mean is, “allowing users to choose to *not* use a wallet is in line with the Ethereum ethos”?  If we go with AUTHSURP or a new transaction type, users would be allowed to continue using pure EOAs, without any code attached.

The downside of those options is that it means dapp authors will likely continue to have “EOA only” checks and whatnot.

---

**SamWilsn** (2022-04-14):

Yes, I suppose users would get to choose not to upgrade as well. Edited to include that!

---

**danfinlay** (2022-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The downside of those options is that it means dapp authors will likely continue to have “EOA only” checks and whatnot.

Can you imagine a scenario where this isn’t true? Even the most optimistic transition plan would still involve the need to support legacy cold wallets in some cases, would it not?

---

**SamWilsn** (2022-04-15):

I think if you’re assuming a default (or forcibly deploying code), you don’t need to keep the non-smart account implemented in the client’s native language, just EVM.

---

**yoavw** (2022-04-18):

Assuming a Default Contract for all EOAs shouldn’t break the assumptions of existing wallets such as legacy cold wallets. It could be something similar to the [ECDSA contract](https://github.com/ethereum-optimism/contracts/blob/df10de974629615b8597ed9bdbcd1b5ec2c0c9b7/contracts/optimistic-ethereum/OVM/accounts/OVM_ECDSAContractAccount.sol) in OVM 1. This particular implementation had some security issues but it could be implemented safely. It’s also not opinionated about what a contract wallet should look like. All EOAs become proxies pointing by default to an ECDSA precompile with the same behavior as existing EOAs, and a setImplementation function which the user can call to switch to a different one in-place. Therefore the default implementation doesn’t need to do everything users need, just the basic functionality and an easy way to upgrade.

The default implementation could also include minimal functionality that allows trustless gas sponsorship when calling setImplementation. For example it could implement the [IWallet interface](https://github.com/eth-infinitism/account-abstraction/blob/a2f4b7be4d9996095e08d7102bacc9f13ea99ff6/contracts/IWallet.sol) of ERC 4337 and point  `validateUserOp` to the same function that handles the ECDSA signature verification and nonce. This way anyone could implement an ERC 4337 paymaster that sponsors these calls when switching to a particular implementation. The paymaster would have no power over the account at any point (unlike an EIP 3074 invoker). It would just pay the bundler for the call. The user stays in control the entire time.

AUTHUSURP achieves a similar goal, allowing the user to set the first implementation, but I think it has a couple of drawbacks compared to assuming default contract:

1. We never fully get rid of EOAs. Some users won’t call an invoker and the network will have to keep supporting EOA for them. Even if everyone calls an invoker, we’ll still need to support EOA for that first operation. By replacing all EOAs with code that emulates an EOA we can simplify Ethereum and have a single type of account.
2. The invoker now has even more power than before. My bias re invokers security is already known here  but previously the invoker could only race against the owner if a bug is discovered. The user may be able to save the assets. With AUTHUSURP the owner loses access to the account. This places an even bigger burden on the invoker to ensure that it is secure.

It would be worth it of it was the only way to achieve the goal, but let’s explore alternatives such as trustless paymasters before taking that risk. The above is a hybrid between “Assume default contract” and “AUTHUSURP” seems to have the same benefits as AUTHUSURP:

- No one-time cost (since it’s the “assume default contract” path).
- The user can choose what to deploy.  (starts with an EOA-like implementation and can change it in-place).
- Works well with sponsored transactions. An ERC 4337 paymaster can pay for switching implementation without an ETH balance (or sponsor any other operation for that matter, as long as the paymaster is willing to do so).

And it solves the drawbacks of both the “Assume default contract” option and the “AUTHUSURP” option:

- For the former: “may or may not do everything users need” - the user can choose any implementation.
- For the latter: “Comes with the drawback pf EIP-3074: invokers potentially have total control over an account” - sponsorship is decoupled from the wallet creation/modification and no trust relationship required.

What would be the drawbacks of this hybrid model?

---

**vbuterin** (2022-04-19):

> AUTHUSURP achieves a similar goal, allowing the user to set the first implementation, but I think it has a couple of drawbacks compared to assuming default contract:
>
>
> We never fully get rid of EOAs.

I think the AUTHUSURP world is not intended to be one where *every* user account starts off being an EOA and then migrates to its “real” validation mechanism. Rather, AUTHUSURP is a migration path for existing accounts that are EOAs today (or that get created later as EOAs because of old software or whatever), and the intended “normal user” flow is to just go straight into an account created via ERC-4337.

Assume default is definitely an interesting option! I do worry about the permanent complexity gain, though I guess it would work nicely in a world where we enshrine code forwarding (so the header would have a field saying “use this other address’s code for the code”), and we could even premine that code into some convenient address eg. 0x0100 or whatever (it would use the `ADDRESS` opcode together with ECRECOVER so it would verify correctly at any address without requiring any storage key to be set to contain the pubkey hash) and make that address the default forwarding destination for EOAs.

---

**imkharn** (2022-04-21):

If I understand your assessment correctly, the “lets not deploy code and say we did” default contract method appears to be the best option except the only issue being ethos (taking an opinionated stance on what a smart contract wallet will look like).

I imagine that a default contract could be voluntarily overridden at any point by a user who chooses what to deploy.

In short, assume the default contract unless a user requests something custom. It still technically has bias because the default contract is free, but its near ignorable impact.

After coming up with my suggestion I read Vitaliks comment. I couldn’t understand what he meant by “I guess it would work nicely in a world where we enshrine code forwarding”. Perhaps he was trying to communicate the same solution as me… that the best compromise might be to assume the default code unless the user forwards to different code.

---

**SamWilsn** (2022-04-21):

There are at least two independent axes for comparison: (a) how do you store the smart contract wallet, and (b) how do you set the smart contract wallet. I’d like to think this post covers (b), mostly.

For (a), we have:

- As actual contract code (that might delegatecall to a common implementation); and
- As a “code pointer” address in the account’s trie, which is what @vbuterin called “enshrine[d] code forwarding”.

For (b), we have:

- Specific transaction type;
- An upgrade function implemented in the default smart contract wallet itself; and
- AUTHUSURP.

---

**SamWilsn** (2022-04-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> a setImplementation function which the user can call to switch to a different one in-place

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> The default implementation could also include minimal functionality that allows trustless gas sponsorship when calling setImplementation.

These are pretty minimal requirements for the default smart contract wallet, and we’ve shown we can write decently secure contracts (like the deposit contract.) I wouldn’t hate a world where we took this path! I will admit that I haven’t looked at 4337 at all, but I’m sure it can handle sponsoring these upgrades easily.

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> Even if everyone calls an invoker, we’ll still need to support EOA for that first operation.

I don’t think that’s necessarily true. You’d only need to support the code for signature verification, which you’d probably need to keep for `ecrecover` anyway.

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> With AUTHUSURP the owner loses access to the account.

Losing access to the account is a funny way to say the user can rotate their ECDSA key and keep the same address ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> What would be the drawbacks of this hybrid model?

I don’t think the user gets to keep their address in this model, and has to transfer all their assets, no?

---

**yoavw** (2022-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> enshrine code forwarding (so the header would have a field saying “use this other address’s code for the code”)

Storing a code forwarding address in the account itself rather than using a storage slot would be great!  Along with an opcode to allow the user to set it to a new address, so that the current implementation’s `setImplementation` function could switch to a new one.  If we want AA to be a first class citizen, then saving SLOAD+DELEGATECALL gas for each transaction is great.

One caveat: code forwarding must not be recursive:

- If account A points to account B for code, and account B doesn’t have code, the call reverts even if account B itself has code forwarding set.
- If an account has code, its code-forwarding field should be ignored so user accounts (currently EOAs) can change implementations, but contracts can’t.

Otherwise we could have circular accounts or just long forwarding-chains, and since there’s no DELEGATECALL cost, it could become a DoS vector on miners.  And it could enable bait & switch attacks.  Code and code-forwarding should be mutually exclusive.

We also need to think about controlling the cost, so that it won’t become a free DELEGATECALL with O(n) cost to validators. Otherwise we can save on SLOAD but still must charge for a DELEGATECALL.  I’m not sure we can safely avoid that.

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> I imagine that a default contract could be voluntarily overridden at any point by a user who chooses what to deploy.

Yes, that’s what I meant.  The default implementation will be a proxy to code that behaves like a current EOA but with a `setImplementation` function that points it to a different one.

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> It still technically has bias because the default contract is free, but its near ignorable impact.

There’s a one-time fee when switching to a new implementation.  Other than that it’s supposed to cost the same in theory.  In practice there may still be a bias since the default implementation would be a precompile so its DELEGATECALL is cheaper, whereas other implementations will be cold and cost more to DELEGATECALL to.  If we make AA a first-class citizen by adding code-forwarding to the account itself, then maybe there’s no DELEGATECALL and no gas difference between implementations.  But that requires a lot more thinking as I suggested above.

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> I couldn’t understand what he meant by “I guess it would work nicely in a world where we enshrine code forwarding”.

It means having a pointer to the implementation in the account header instead of storage.  A more efficient way to support changing implementations.

---

**yoavw** (2022-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/samwilsn/48/4301_2.png) SamWilsn:

> I will admit that I haven’t looked at 4337 at all, but I’m sure it can handle sponsoring these upgrades easily.

Basically it’s an ERC to start experimenting with AA without committing to a consensus change prematurely, by introducing a new mempool. Bundlers (likely miners/validators but could be anyone) mine this pool and send operations to contract accounts through the EntryPoint contract.

Gas abstraction happens through Paymaster contracts (similar to GSN’s), so the contract wallet may or may not pay its own gas, depending on whether another contract is willing to pay on its behalf  The paymaster has no power over the operation, other than deciding whether it is willing to pay for it as-is.

I explained the ERC in [my ethamsterdam talk](https://twitter.com/yoavw/status/1522672508331245570) and happy to discuss further on our call tomorrow ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/samwilsn/48/4301_2.png) SamWilsn:

> I don’t think that’s necessarily true. You’d only need to support the code for signature verification, which you’d probably need to keep for ecrecover anyway.

I meant that we wouldn’t be able to remove the current EOA model, because initially accounts won’t have code, so they would need to call an invoker at least once in order to “become” contracts.  Therefore we still have two account types (EOA and contract).  Is that not the case?

If we go the “assume default code” route, we drop EOA altogether and Ethereum will have only one account type.

![](https://ethresear.ch/user_avatar/ethresear.ch/samwilsn/48/4301_2.png) SamWilsn:

> Losing access to the account is a funny way to say the user can rotate their ECDSA key and keep the same address

The context in which I wrote this sentence above is the case of a buggy/malicious EIP 3074 invoker.  The user gets to rotate their ECDSA key in *any* of  the methods we’re discussing.  The difference is how it’s done and what’s the risk exposure.  I’m more comfortable with having a default implementation (that uses ecrecover) and let the user `setImplementation` in the account itself, rather than signing an authorization to an invoker to do it on the user’s behalf.

![](https://ethresear.ch/user_avatar/ethresear.ch/samwilsn/48/4301_2.png) SamWilsn:

> I don’t think the user gets to keep their address in this model, and has to transfer all their assets, no?

Users do keep their addresses.  The model switches existing EOAs to have a “default code” in which the user can `setImplementation`, so the implementation can be changed anytime while the assets remain in the original address.  Hence it seems to have all the benefits and none of the drawbacks as far as I can tell (but let’s find the drawbacks if they exist, so that we can consider the trade-offs ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) )

