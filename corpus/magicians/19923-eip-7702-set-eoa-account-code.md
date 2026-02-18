---
source: magicians
topic_id: 19923
title: "EIP-7702: Set EOA account code"
author: vbuterin
date: "2024-05-07"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7702-set-eoa-account-code/19923
views: 21604
likes: 330
posts_count: 404
---

# EIP-7702: Set EOA account code

Add a new transaction type that adds a `contract_code` field and a signature, and converts the signing account (not necessarily the same as the `tx.origin`) into a smart contract wallet for the duration of that transaction. Intended to offer similar functionality to EIP-3074.

https://github.com/ethereum/EIPs/pull/8527

## Replies

**SamWilsn** (2024-05-07):

> Set the contract code of signer to contract_code.

Does this mean that calls back into the EOA during the transaction execute `contract_code`?

---

Should `contract_code` actually be initcode for more flexibility?

---

**vbuterin** (2024-05-07):

Some variations:

1. Should the contract_code signature also sign over the account’s nonce?
2. Should the contract_code signature also sign over the CHAINID?
3. Should the contract_code instead be an address? This would save calldata, though only a little bit of calldata because ERC-1167 proxies only take 44 bytes.
4. Should SSTORE inside the “temporarily contract-ified EOAs” be prohibited, like it is in EIP-5806?
5. Should we have initcode and not just contract_code?
6. Should we just add a flag to NOT set the code back to zero at the end? Thereby making this EIP also supersede EIP-5003.

---

**rmeissner** (2024-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should we have initcode and not just contract_code?

While this might add some complexity (i.e. it is not just copying code, instead it first needs to execute it) it also has the advantage that it might be “cleaner” to implement signature invalidation. I.e. in my init code I could check that this action was done within a specific timeframe, otherwise reverse, therefore invalidating the code setting signature.

Additionally this might add “out of the box” compatibility with existing tooling.

---

**rmeissner** (2024-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should the contract_code signature also sign over the account’s nonce?
> Should the contract_code signature also sign over the CHAINID?

For these I assume the argumentation would be the same as for EIP-3074.

Slight difference might be on the CHAINID, as code could be seen as more “universal” (which might be a misconception tbh). Removing the dependency on the CHAINID (or making it optional), might allow for interesting use cases related to account migration.

In general I believe that this approach would allow a more complete testing of the account migration use cases, as you set the code on an address similar to 5003 and 7377.

---

**nlordell** (2024-05-07):

> Should the contract_code signature also sign over the account’s nonce?

I personally felt like this was a nice feature of 3074 as it adds a “get out of jail free” card to invalidate all 7702 signatures. This can mostly be helpful in cases where the signed code has a bug and doesn’t provide functionality for disabling the code.

> Should the contract_code instead be an address? This would save calldata, though only a little bit of calldata because ERC-1167 proxies only take 44 bytes.

I think if the signature is over a contract address, then you would have to also sign over a chain ID. Personally, I slightly lean towards signing code as it could allow chain ID agnostic signatures (although whether or not that is a good idea, I don’t know yet) especially given min-proxies are quite small and comparable in size to an address.

> Should SSTORE inside the “temporarily contract-ified EOAs” be prohibited, like it is in EIP-5806?

It could also behave like TSTORE (in that it gets removed at the end of the transaction along with the code). But if it does behave like TSTORE, then it isn’t really any benefit to allowing SSTORE (besides maybe allowing for simpler execution code)

---

**SamWilsn** (2024-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should the contract_code signature also sign over the account’s nonce?

No. Let the `contract_code` handle replay protection.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should the contract_code signature also sign over the CHAINID?

No, can check that in the bytecode.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should SSTORE inside the “temporarily contract-ified EOAs” be prohibited, like it is in EIP-5806?

Alternatively, can the end of the transaction step be “At the end of the transaction, set the `contract_code` and storage of each `signer` back to empty.”?

---

**SamWilsn** (2024-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should we have initcode and not just contract_code?

Another argument in favour of initcode over `contract_code` that came up on the breakout is bypassing dumb EOA checks using extcodesize.

---

**shemnon** (2024-05-07):

What if instead of using EOA addresses, what if 7702 used a “salted” address? i.e. instead of just `keccak(public_key)[-20:]` it’s `keccak(AUTH_MAGIC | public_key)[-20:]` - that way existing EOAs won’t be impacted

That address, from its very first use, has the risks associated with eternal authorization.  That way we don’t increase the risk footprint of EOAs.

---

**taek.eth** (2024-05-07):

Might have a small DoS vector that can make a `<address>.transfer()`(i know this is anti-pattern, but still some contracts use this) being reverted when recipient has signed contract code that does not have `receive()` function

This will be up to tx.origin to post the contract code or not, but if .transfer() is being done on the execution phase of 4337, then attacker can snatch the bundle and post the bundle with recipient’s contract code, thus making the validation valid but revert on execution phase, ending up sender paying the gas but it does not achieve the behavior that sender paid for,

Also, if we look into the erc721.safeTransferFrom(), if recipient has signed the contract code before and if safeTransferFrom() is done through 4337, execution of erc721.safeTransferFrom() might fail if the recipient’s code does not have `onERC721Received`

---

**Ivshti** (2024-05-07):

this sounds good but how would that work if the entryPoint wants to call account.validateUserOp()?

---

**greg** (2024-05-07):

As a 3074 advocate, my first gut check is this is a really nice solution. I’d argue this is better for 5003 and 7377, which have irreversible side-effects and I would argue could lead us to another Parity wallet dilemma.

If this gets pushed through, then I’d strongly urge a standardization around which contracts are used (similar to 4337 entrypoints and 3074 invokers).

> Should the contract_code instead be an address? This would save calldata, though only a little bit of calldata because ERC-1167 proxies only take 44 bytes.

Personally from a safety perspective I think this actually makes more sense, since you can have very easily verifiable ABIs/Code to sanity check against your local wallet.

–

I want to point out one thing from line 27:

> at the least because eventually quantum computers will break the ECDSA that EOAs use)

(happy to move this conversation elsewhere)

I don’t think this is an overly sound argument. If ECDSA breaks we’re doomed beyond belief, and realistically before we start using this as a counter-point we need to actually have a plan (or the research) showing how were moving towards quantum safe curves ASAP. I’d assume most smart accounts are using ECDSA as a majority set of the signers, so that doesn’t save us either.

---

**ch4r10t33r** (2024-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Should we just add a flag to NOT set the code back to zero at the end? Thereby making this EIP also supersede EIP-5003.

If the code is not reset, would the private key controlling the account become ineffective (similar to 7377)? If so, how would one initiate transactions from that smart account? Always with the new transaction type?

---

**Arachnid** (2024-05-07):

I proposed something similar in 2020; the comments from then may provide some useful food for thought: ["Rich transactions" via EVM bytecode execution from externally owned accounts](https://ethereum-magicians.org/t/rich-transactions-via-evm-bytecode-execution-from-externally-owned-accounts/4025)

---

**derek** (2024-05-07):

Regarding whether to sign over the account’s nonce:

- As I argued in the 3074 call, signing over the account’s nonce would invalidate most of the popular use cases of AA that we are seeing in the 4337 ecosystem today, particularly alternative singers (e.g. attaching a passkey to your EOA) and transaction delegation (creating a session key for a DApp).
- @yoavw had a proposal for signing over a user-picked maxNonce instead.  I think this proposal is impractical from a UX perspective, since it’s not clear how the user is supposed to pick a sensible maxNonce.  However, I like how it basically gives the user a way to opt out of in-protocol revocation.  So the user could just set maxNonce to 2^64 if they don’t want to accidentally revoke the signature, and then they’d rely exclusively on the contract code for revocation.
- I do think there’s another proposal worth considering: nonceManager.  This was first described here and here.  Basically, we let the user pick a nonceManager, and it’s the nonceManager’s nonce that we sign over.

Notably, the `nonceManager` can be a counterfactually deployed smart account owned by the user’s EOA, so that when the user does want to revoke, they’d send a transaction with the smart account.  And they don’t actually have to pay gas to deploy the smart account unless they want to revoke, since the account could be counterfactually deployed.

Personally, I think it’s OK to just ignore nonce altogether in the sig, but if people are not comfortable with that (for the same reason that made people add nonce to 3074), then I think either the `maxNonce` proposal or the `nonceManager` proposal could work, though I prefer `nonceManager` since, unlike the `maxNonce` proposal:

- It gives the user a way to selectively revoke signatures without accidentally revoking anything.  With maxNonce, you always have to revoke everything within the range.
- Unlike the maxNonce proposal, there’s no UX issue of picking a max nonce.

---

**protolambda** (2024-05-07):

I support this EIP wholeheartedly. This is incredibly useful, as it looks like it essentially supports atomic bundling / composability of user-ops in protocol. This allows a lot of block-building policy protocols to really improve user-experience and support things like just-in-time data without changing the state trie in-between transactions.

Clarifying in the EIP when the `TSTORE`/`TLOAD` is shared during tx execution would be great. Setting it globally for the transaction, rather than per user-op, avoids the need to rely on account-code presence to persist data between user-ops. The 3074 comparison hints at it, but it is not entirely clear.

---

**adamegyed** (2024-05-07):

I am generally in favor of this approach to gradually introducing AA features to EOAs. I have one point I’d like to make, and a suggested implementation path.

I think it is important for this proposal to support both:

1. Re-using the signature from an EOA across multiple transactions, using the contract code to enforce signature checks and uniqueness.
2. Allow EOAs to revoke existing signatures over code.

Point 1 is critical for AA use cases around alternative transaction validity conditions, which includes other cryptographic schemes like passkeys, multisig capabilities, and permissions. Point 2 is critical to allow for “upgrading” account’s code implementation, without simultaneously allowing the old code to also be assumed. It is to prevent the “perpetual signature” risk that was identified with EIP-3074.

My proposal for how to accomplish this is to introduce a new, parallel nonce field for accounts, distinct from the existing transaction nonce. Name TBD, calling it “code assumption nonce” for now.

EIP-7702 transactions could require the EOA signature to be over the “code assumption nonce”, rather than their transaction nonce, to start an EOA assuming code. Of course, each transaction using this format would still increment the respective account nonces, ensuring unique transaction hashes.

Multiple outstanding signatures could be placed over the same “code delegation nonce”, allowing different pieces of code to be assumed in different transactions.

Accounts could opt to invalidate outstanding “code delegation nonces” by signing a 7702 signature over a magic value, such as empty code or code only containing `0xFE` (invalid opcode), indicating they intend to increment the nonce and invalidate all outstanding 7702-enabling signatures.

I see there are two other proposals for how to accomplish this (or something similar), and I want to address why I don’t think they are the best choice forward.

- One idea is to sign over a max nonce. I believe this provides a clumsy user experience for any form of AA-based transaction automation, forcing the user to guess how many times contract automation would happen, and having to either sign very far in advance or regularly re-sign to bump the nonce. Additionally, it would require more control over how to bump nonces to invalidate signatures, likely requiring the protocol to allow bumping the nonce by more than one at a time. This introduces unneeded complexity into nonce management that the EVM must bear, rather than contracts themselves.
- Another idea is to fully delegate nonce control to an external contract (the “nonce manager”), and introduce either code or an address to the contract into the 7702 transaction type as a field. I believe this to be too far in the other direction, enshrining too much application-specific logic into the transaction type than what is needed, thus making it unnecessarily complex. A “code assumption nonce” still allows for implementation-dependent nonce control, such as to track nonces for session keys or secondary signers to the account, within the code the EOA is assuming.

By keeping 7702 code assumption tracked in a separate nonce from individual transaction nonces, we can provide both customizable nonce behavior, and the ability for EOAs to manually exit and/or upgrade their code assumption behavior.

EDIT: I previously misunderstood how the max nonce field would work. If the EOA nonce is not incremented when used to assume code in a transaction while not being `tx.origin`, then using max nonce fields for the purposes of allowing alternate txn validity conditions is sufficient and doesn’t have the UX pitfalls I previously imagined. I’m keeping the proposed idea up here for posterity.

---

**wjmelements** (2024-05-07):

Instead of setting a constant for the code size costs, it should be equal to the calldata cost plus the eip-3860 gas adjustment used for `create` txs, to account for the jumpdest validation.

---

**Michaels** (2024-05-07):

I think another valid question is if selfdestruct opcode should be prohibited. If not, would it mean a gas refund  or incur more gas? Also that mean that the signers eth balance is drained to the selfdestruct argument?

---

**Michaels** (2024-05-07):

1. Taking the bytecode would be better imo as it doesn’t require the contract (if an address is required) to already be deployed in a previous tx. In most cases, a proxy to an existing 4337 code would be used but flexibility would be good too and not needing the code to be predeploted to an address beforehand is helpful
2. No, storage opcodes should not be prohibited. It (all written storage slots) should however be cleared at the end of the transaction and its gas costs be the same as TLOAD and TSTORE since they’d then behave similarly.
3. Yes. Init code rather than runtime code would be helpful for more specific and custom instances

---

**dror** (2024-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> that way existing EOAs won’t be impacted

The idea of this EIP is to let existing EOA accounts run “as if” they have code.

Mapping to different addresses doesn’t let you work with existing accounts, which defeats the purpose


*(383 more replies not shown)*
