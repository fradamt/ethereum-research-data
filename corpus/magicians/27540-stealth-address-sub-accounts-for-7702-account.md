---
source: magicians
topic_id: 27540
title: Stealth Address + Sub Accounts for 7702 Account
author: 0xkoiner
date: "2026-01-20"
category: Magicians > Primordial Soup
tags: [erc, "7702", erc5564]
url: https://ethereum-magicians.org/t/stealth-address-sub-accounts-for-7702-account/27540
views: 135
likes: 4
posts_count: 1
---

# Stealth Address + Sub Accounts for 7702 Account

Hi magicians!! I’d like to present my idea (research + PoC) and get some feedback or notes.

[![Stealth Address + Sub-Accounts (3)](https://ethereum-magicians.org/uploads/default/optimized/3X/f/7/f7b309c5c1e05f0d8d8c658635eea0629809a722_2_690x403.jpeg)Stealth Address + Sub-Accounts (3)1920×1124 186 KB](https://ethereum-magicians.org/uploads/default/f7b309c5c1e05f0d8d8c658635eea0629809a722)

**Key Points:**

1. The Root Key can be an existing 7702 account.
2. The Spending Key and Viewing Key must be stored in a secure box (e.g., KMS/HSM/MPC).
3. Stealth address discovery requires storing the ERC-5564 metadata: viewTag (1 byte) and ephemeralPublicKey (33 bytes).
4. This metadata can be stored in contract storage, event logs, local/client storage, or the backend (depending on UX and privacy requirements).

**Notes:**

1. It is possible to derive N stealth addresses from a single meta-address.
2. Each derived address can represent a dedicated sub-account for subscriptions, private transactions, private payments, or payment channels.
3. The creation request may originate from a third party (via the API), be approved by the user, and then be enforced to the account implementation with spending policy on the sub-account on-chain.
4. The sub-account can be topped up in an unlinkable way using Privacy Pools or other privacy funding mechanisms available in the market.

Example On-Hand:

based on: [![](https://ethereum-magicians.org/images/external_integrations/github-icon.png)stealth/contracts/STEALTH_ARCHITECTURE.mdopenfort-xyz/stealth-addresses](https://github.com/openfort-xyz/stealth-addresses/blob/0xkoiner/stealth/contracts/STEALTH_ARCHITECTURE.md) Bob owned 7702 account. In the implementation exits:

```auto
    event Announcement(
        uint256 indexed schemeId, address indexed caller, bytes1 indexed viewTag, bytes ephemeralPubKey, bytes metadata
    );

    bytes public stealthMetaAddress;

    error InvalidEphemeralPubKeyLength();
    error EmptyMetadata();

    function announce(uint256 schemeId, bytes calldata ephemeralPubKey, bytes calldata metadata) external {
        // Validate ephemeral public key length (66)
        if (ephemeralPubKey.length != 66) {
            revert InvalidEphemeralPubKeyLength();
        }

        // Validate metadata contains at least viewTag
        if (metadata.length == 0) {
            revert EmptyMetadata();
        }

        // Extract viewTag from first byte of metadata
        bytes1 viewTag = metadata[0];

        emit Announcement(schemeId, msg.sender, viewTag, ephemeralPubKey, metadata);
    }
```

In this case, Bob can create a stealth account based on his `st:eth:0x<spendingPubKey><viewingPubKey>` and call `Stealth.announce()` to publish the data.

This will emit an event and store the data cheaply, attached to Bob’s main account.

From an external viewer’s perspective, it will look like random data. It won’t be possible to derive the stealth address or keys. An observer might infer that Bob is using stealth addresses, but they still won’t be able to link whether Bob announced for himself or for another user’s stealth address.

On the other hand, Alice can also announce to Bob that she sent a payment to the stealth address Bob requested.

In both cases, we preserve the unlinkability between the stealth address and its owner.

Additionally, the private viewing key can be delegated to a trusted monitoring system that can scan the metadata, detect whether a stealth address was created for a given spending public key, and signal it. Then, to recover the stealth address, we can do it offline (e.g., in a safe environment) and securely recover the private key to associate the stealth address with the owner of the 7702 account in our frontend.

This is the cheapest and most trustless way to store stealth address metadata without storing stealth private keys on the client or backend.

**What is ERC5564 (Stealth Address)?:** https://github.com/openfort-xyz/-stealth-addresses/tree/0xkoiner/dev/documentation

### Actors / keys

- ROOT 7702 account: the user’s main account (funding + orchestration).
- KMS: stores ERC-5564 spend/view secrets (or protects them via HSM/MPC).
- P-256 non-extractable key: the long-term signer for the subaccount implementation.
- Privacy Pools: used to fund subaccounts unlinkably.

## Phase 0 — Provision the “Stealth Meta-Address” (ERC-5564)

1. Generate Spending keypair and Viewing keypair (ERC-5564 receiver keys).
2. Store spend_sk and view_sk in KMS (preferably threshold / split-control; more below).
3. Publish the stealth meta-address (= spend_pk + view_pk) anywhere you want (user profile, app registry, QR).

**Why this matters:** you can deterministically derive *many* one-time stealth addresses without ever storing them.

Your point stands: you **don’t store derived stealth private keys**, only the *root receiver keys*.

## Phase 1 — Create a new subaccount address (ERC-5564 derivation)

For each new subaccount you want:

1. Create an ephemeral keypair.
2. Compute (stealthAddress, viewTag) from (epk, metaAddress) per ERC-5564.
3. Optionally create an announcement record/event so wallets can discover it (if you want third-party payments UX; not strictly needed for self-managed subaccounts).

At this point, you have the **fresh EOA address** that will become your 7702 subaccount.

## Phase 2 — Bootstrap the 7702 subaccount using a derived EOA key (no storage)

Goal: use the stealth address’s **ECDSA(secp256k1)** capability *exactly once* to install code + rotate authority.

1. Inside trusted service boundary, derive the stealth private key just-in-time:

 Use view_sk to scan/identify the target (or if you’re the creator you already know which one it is),
2. Use spend_sk + epk (and whatever ERC-5564 specifies for derivation) to compute the one-time private key for that stealth address.
3. Use that derived privkey only to sign the EIP-7702 authorization that sets the code for the account (your custom implementation).
4. In the same setup flow, call initialize(...) to:

 set P-256 pubkey as the primary signer (non-extractable),
5. set your limits module / permissions,
6. optionally set a “delegate / session key” policy.
7. Immediately zeroize the derived stealth privkey in memory.

**Important nuance (security):**

Even if you “wash out” the derived stealth privkey, if someone later compromises the KMS (and it can recompute spend/view secrets), they can *re-derive it* and can sign new 7702 authorizations. So your **true root-of-roots becomes KMS**. Treat it like a hardware wallet-tier asset.

## Phase 3 — Fund the subaccount privately via Privacy Pools

1. ROOT 7702 deposits ETH/USDC/etc into Privacy Pools.
2. Later, withdraw from Privacy Pools to stealthAddress (now a 7702 smart account).

**Best practice:** use Privacy Pools’ native relay/fee mechanism (or a relayer) to avoid needing the subaccount to already have ETH for gas *before it’s funded*.

## Phase 4 — Start using AA normally (4337 + paymasters)

Now the subaccount has funds and long-term control is P-256:

1. Use 4337 userOps signed by P-256.
2. If you want sponsored gas:

 either keep some ETH in the subaccount, or
3. use a paymaster that charges ERC-20 and is compatible with your execution pattern.

### Paymaster + “withdraw + approve in same userOp”

Be careful: paymaster validation happens *before* execution. So “withdraw then approve then repay paymaster” can make the paymaster eat risk unless it’s designed to tolerate it. The safer pattern is:

- PP withdrawal funds the account first, then later userOps can safely pay/approve.

## Use case: Merchant-created, unlinkable subscription sub-accounts

### Goal

Let a trusted service (Spotify/YouTube/ChatGPT) create a **dedicated sub-account** for subscriptions that:

- is unlinkable on-chain to the user’s ROOT account,
- is controlled by the merchant (so they can charge monthly),
- has hard spending limits (so the merchant can’t drain funds),
- and the user can revoke/cancel any time and recover remaining funds.

A trusted service (Spotify, YouTube, ChatGPT) can request via an API its own dedicated subscription sub-account from the user.

The user approves this request from their ROOT 7702 account, including the subscription policy (monthly cap, allowed token, allowed recipient) and the service’s P-256 public key that will control spending.

Once approved, the platform derives a fresh ERC-5564 stealth address through a KMS (so no derived private key needs to be stored, but recovery remains possible). The user’s ROOT account then deposits funds into Privacy Pools, and later those funds are withdrawn to the newly derived stealth sub-account in a way that avoids on-chain linkage between the ROOT and the sub-account.

After the sub-account receives funds, it is upgraded via an EIP-7702 authorization to a custom smart-account implementation and initialized so that the service’s P-256 key becomes the active signer, with strict spending limits and execution permissions enforced on-chain.

From that point on, the service can run recurring subscription charges within the configured constraints, while the user retains an escape hatch: Root Key can revoke the service at any time, recover control (via the KMS backed derivation/recovery path), and withdraw any remaining balance without revealing a direct on-chain connection to the main ROOT account.
