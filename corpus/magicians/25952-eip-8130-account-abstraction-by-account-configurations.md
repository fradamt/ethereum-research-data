---
source: magicians
topic_id: 25952
title: "EIP-8130: Account Abstraction by Account Configurations"
author: chunter
date: "2025-10-24"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8130-account-abstraction-by-account-configurations/25952
views: 164
likes: 0
posts_count: 10
---

# EIP-8130: Account Abstraction by Account Configurations

Discussion topic for EIP-XXXX [DRAFT](https://github.com/chunter-cb/EIPs/blob/enshrined-aa-validation/EIPS/eip-draft-aa-account-configuration.md)

#### Update Log

- 2025-10-24: initial draft

#### External Reviews

None as of yyyy-mm-dd.

#### Outstanding Issues

Hey all this is a work in progress draft, looking for some early feedback!

First time writing an EIP and sharing in Ethereum Magicians so please let me know if I missed anything!

Thanks

## Replies

**chunter** (2026-01-21):

Moved to an EIP here, the previous link will get more and more out of date.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/11144)














####


      `master` ← `chunter-cb:eip-8127-pr`




          opened 07:36PM - 21 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/133686793?v=4)
            chunter-cb](https://github.com/chunter-cb)



          [+608
            -0](https://github.com/ethereum/EIPs/pull/11144/files)







## Summary

This PR adds a new draft EIP proposing account abstraction via onc[…](https://github.com/ethereum/EIPs/pull/11144)hain account configurations.

**Key features:**
- Standardized validation mechanism using onchain account configurations to define accepted keys and key types
- Predefined key types (K1, R1, WebAuthn, BLS, DELEGATE) enabling protocol-level signature verification without EVM execution during validation
- New EIP-2718 transaction type with native gas abstraction support (token payments, permissioned/permissionless payers)
- Native multisig support at the protocol level
- Account Configuration Precompile for key management
- Compatibility with existing EIP-7702 and ERC-4337 infrastructure

**Motivation:**
Enable account abstraction benefits (batching, gas sponsorship, custom authentication) while allowing nodes to validate transactions via simple state checks without EVM execution. This enables highly optimizable mempool implementations and removes the need for additional reputation systems for DoS prevention.

## Discussion

Ethereum Magicians thread: https://ethereum-magicians.org/t/account-abstraction-by-account-configurations/25952

## Checklist

- [x] Followed EIP-1 formatting guidelines
- [x] Created Ethereum Magicians discussion thread
- [x] Included all required sections

---

**rmeissner** (2026-01-22):

Thanks for sharing this EIP.

After an initial read I have two questions for the start:

- Why did you chose a self-call for execution rather than a dedicated entrypoint address? This would have allowed to distinguish this from a self call in contract methods.
- Why did you chose to have the account authentication logic and gas payment logic in one EIP? From past experience I would say that this lowers the chances of adoption by the core team due to complexity. Separating this into multiple EIPs might make sense.

---

**chunter** (2026-01-22):

Thanks [@rmeissner](/u/rmeissner) !

I can split this out into two EIPs, agree that would keep it much cleaner. Initially wanted to have ~parity for the things we cared about for AA and ERC20 payments was one of them.

As for the self call:

- this allows tx.origin to be the wallet address
- enforces that the calldata must be interpreted by the wallet code
- no entrypoint overhead
- can determine if msg.sender == tx.origin && msg.sender == address(this)

Any specific use case for the self call initiated from code vs from the initial transaction frame?

---

**Helkomine** (2026-01-23):

Changes to token balances should be understood as changes in storage (e.g., ERC20) rather than turning them into a transaction format attribute, as this increases protocol complexity. Additionally, a 2D nonce structure can be simplified to a nonceBitmap, as shown here: https://ethereum-magicians.org/c/web/70

---

**rmeissner** (2026-01-28):

Hey, sorry for the late reply,

regarding the self call I was mostly thinking about the requirements to make an account like Safe compatible to it. For config changes the Safe checks on self calls. Therefore it would be directly compatible to have an “entrypoint”.

Just to note: I don’t mean that there should be an entrypoint contract, rather that tx.origin (or msg.sender) is set to a pre-defined address, to easily check that this flow is taken.

Edit:

> can determine if msg.sender == tx.origin && msg.sender == address(this)

This would would be true for the initial invocation and any follow up calls, right? At least for Safe it would be interesting to differentiate these. That being said, this is also true for EIP-7702 and the solution most likely would be transient storage.

---

**chunter** (2026-01-29):

Yes that would be true for both initial invoke and follow up calls.

Yes seems like transient storage could be a solution here, I cant right now see how that breaks.

Initial frame: works (sets transient flag)

Initial frame to another address which calls into the wallet later (not this tx type): wouldnt be triggered, caller cant be msg.sender ?

The above is true for any other as well I think but havent thought too deeply on it.

---

**chunter** (2026-01-29):

…The main tradeoff here is swapping out arbitrary code execution in validation which allows us to have no wasted/unpaid computation and performant inclusion checks (just nonce, payer balance, sig matches sig slot) and a performant mempool.

The solution is backwards compatible with ERC-4337 and allows existing smart accounts to migrate by registering their keys with the precompile.

Disabling arbitrary validation code enables us to have node optimizations for reasons mentioned above.

We believe this tradeoff is acceptable because the vast majority of wallets today verify a single key: secp256k1, P-256, or WebAuthn. These cover EOAs, hardware wallets, and passkeys. BLS enables signature aggregation where needed. Delegated keys provide subaccount functionality. The key type system is extensible—new signature schemes can be added via protocol upgrades with clearly defined verification logic.

The primary capability lost by removing arbitrary validation is custom recovery logic. However, recovery flows remain fully supported through multiple pathways:

1. ERC-4337 compatibility: Accounts can still use EntryPoint-based recovery modules alongside native AA transactions

2. Relayer-assisted recovery: Guardians sign recovery authorizations off-chain; a relayer submits the transaction and pays gas (standard pattern used by Safe, Argent today)

3. Future protocol level recovery: ie. native multisig of trusted external accounts, potential zk implementation if performant enough

