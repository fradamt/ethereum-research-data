---
source: ethresearch
topic_id: 23395
title: "The Future of State, Part 1: OOPSIE - A new type of Snap Sync-based wallet/lightclient"
author: CPerezz
date: "2025-11-03"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/the-future-of-state-part-1-oopsie-a-new-type-of-snap-sync-based-wallet-lightclient/23395
views: 526
likes: 9
posts_count: 9
---

# The Future of State, Part 1: OOPSIE - A new type of Snap Sync-based wallet/lightclient

Thanks [@gballet](/u/gballet) [@ihagopian](/u/ihagopian)  and [@weiihann](/u/weiihann) for the reviews and discussions

# (O.o)psie

OOPSIE (Opt-in Ownership of Partial State of Interest, Exclusively) turns wallets into tiny, proof-aware state clients: snap-sync-first-first reads, user-owned range sets, authenticity badges (data marked as authenticated via MPT proof), and finalized pre-sign checks—faster UX, better privacy, and fewer RPC crutches.

> This article will showcase what we could do with this new snap-based client/wallet and the major issues that it showcases. From there, this will serve us as an introduction for the article that will touch on the deep state-related problems that ZKEVM and Partial Statefulness entail.

# Why OOPSIE? - The Hidden Crisis in Ethereum’s Architecture

Today’s Ethereum faces a paradox. While we celebrate decentralization, the reality is starkly different: RPC endpoints are scarce, expensive, and centralized. Users don’t hold their own data. Bootnodes are hammered with snap sync requests. Wallets are mere proxies to centralized services. And with ZKEVMs evolving rapidly, fewer nodes will be incentivized to hold and serve syncing of Ethereum’s ever-growing state.

The consequences are already visible:

- Builder centralization: Builders produce 80-90% of Ethereum’s blocks, becoming the only entities holding full state after ZKEVMs.
- RPC dependency: Almost no full nodes serve public RPC. Users are entirely dependent on centralized providers
- Privacy leakage: Every wallet query broadcasts user addresses to centralized services linking it to the user’s IP and behaviour patterns
- Fragility: When major RPC providers go down, users lose access to their own assets

Any state expiry proposal must confront this reality: **no one holds their own data**. This makes discussions about expired state academically interesting but practically painful.

Not only that, with ZKEVMs further evolving, we will eventually get to a point, where less and less nodes will be incentivized to hold Ethereum’s *ever-growing* state. Thus arriving to a critical point where we might have a really hard time retrieving data.

# A change of paradigm - Let’s tackle the problem step by step

Instead of trying to solve a massive problem with a single solution. Incurring into massive changes and involving never-ending discussions. We should adopt a smarter strategy.

**Let’s take a first small step towards changing the storage paradigm**. What could happen if users stored the subset of state they’re interested on?

Think about it. Nowadays, wallets are a mere RPC proxy. They don’t hold any data. And, thus, they’re just not participants of the network on any way or shape. They’re completelly dependent on centralized RPCs and wallet providers.

Without them, they’re merciless and lack any sovereignty over their data/wallet. Most of them only have their seed phrase. But without holding any data, they’re just a part of the problem of expiring state. Rather than a solution or at least, not an impediment.

Even I’ve faced the issue of trying to pay a friend back for a dinnner with my wallet, and the RPC being down actually made it impossible for me to even know my balance or transact.

Besides the philosophical aspect of it, users holding their data locally would cause quite some changes for several actors:

## Renewed wallet providers

- Wallet providers would heavily alleviate the pressure on their RPCs (though this requires further investigation and i. Since wallets now hold data and can/will update state. Users are able to have a synced subset of ethereum’s state that is of their interest and update it themseleves.
- Wallets would snap sync their range set at every startup. Getting not only the updated values but also the proofs for the ranges they’re interested on.
- Faster, offline-first experience (instant balance + nonce display).
- Reduced privacy leakage: no need to broadcast every address to a single RPC provider.
- State marketplace participation strategies. Wallets can offload storage costs for redundancy on users in return of premium features for example.
- Reduced freemium costs: Free tier users consume minimal resources

## Better UX

- Offline-first basics: Instant balance + nonce + token holdings for recent activity. Compose transactions while offline and broadcast later.
- 2–3s faster tx building: Pre-filled nonce/balance removes a blocking RPC round trip for most common sends/swaps.
- Lower infra cost: Many read calls (balanceOf, nonce, token lists) are served locally. Your free tier goes further.
- Better privacy posture: Fewer raw address queries. Marketable as a tangible privacy upgrade.
- Resilience = fewer support tickets: Users aren’t bricked by a transient RPC outage.

# Architecture & technical dive.

Let’s be clear. We don’t need another grand rewrite. We need a small, sharp step that makes wallets faster, more private, and harder to brick when RPCs sneeze. That’s OOPSIE in **hybrid mode**: light-client for authenticity + snap synced subset state for UX. Everything else stays the same.

No forks. No heroics. No promises to “solve Ethereum.” Just a small incremental update.

## TLDR

Hybrid edge client inside the wallet:

- Block headers: keep a thin, verified view of finalized headers. Use them as the anchor of truth.
- Snap synced subset state: store only the key-values the user cares about (balances, nonces, a few token/storage slots) with proofs.
- RPC for the rest (RPC IS OPTIONAL. The wallet can function without it): raw reads if needed and with proofs if you’ve got them. Always MPT-proved.

Net effect: faster UI, offline-friendly basics, fewer blind calls, and a way to talk about state expiry without users paying the price.

### The Range Set — What do we store

A tiny list of exact keys the wallet will be stored locally with their proofs.

#### A) Account meta (per address)

- balance(address)
- nonce(address)
- codeHash(address) (If we want to be able to simulateGas for example we need the actual code too). Same if you have a smart wallet.
- (storageRoot(address) is implicit if you track any storage slots)

These come from the account leaf/commitment itself.

#### B) ERC balances (precise, verifiable)

- ERC‑20 balanceOf(owner)

Key = (token, owner) → slot = keccak(owner || baseSlot_balances) (OZ layout uses slot 0 for balances)
- Value = uint256

ERC‑721

- ownerOf(tokenId) → slot = keccak(tokenId || baseSlot_owners) (often slot 0)
- balanceOf(owner) → keccak(owner || baseSlot_balances) (often slot 1)

ERC‑1155 `balanceOf(owner, id)`

- Nested mapping → keccak( owner || keccak(id || baseSlot) )
- Value = uint256

#### C) Allowances & approvals (Probably overkill/ can be optional)

- ERC‑20 allowance(owner, spender) → commonly keccak( spender || keccak(owner || baseSlot_allowances) )
- ERC‑721

getApproved(tokenId) (per‑token)
- isApprovedForAll(owner, operator) (nested mapping)

#### D) Selective storage slots (DeFi positions)

Pin a handful of slots that matter to the user:

- Router allowances for swaps
- LP shares / staking balances
- Collateral and debt indexes

Represented as:

```ts
SelectiveSlot {
  contract: address,
  slot?: bytes32,                 // exact 32‑byte slot
  preimage?: { parts: bytes[], hash: 'keccak256', nested?: true },
  abi?: { type: string, scale?: number } // optional decode hints
}
```

#### Example range sets

- Minimal (10–15 keys): account meta for the active address, 3 token balances (USDC/WETH/DAI), 1–2 allowances, 1–2 NFT bits, maybe one lending slot.
- Active DeFi (30–50 keys): 2–3 accounts, ~10 ERC‑20s, ~10 allowances, ~10 protocol slots, a few 1155 balances.

---

## How the Pieces Fit

```auto
UI ↔ Query Router ↔ OOPSIE Engine (WASM)
                     ├─ Range Set Manager
                     ├─ Snapsync Fetcher
                     ├─ Proof Verifier
                     ├─ Block Header Pipeline

Providers (full nodes / snapshotters)
  ├─ JSON‑RPC
  └─ Proof/Multi‑proof endpoints
```

## Snap Sync — Pull What We Care About, With Proofs, Without RPCs

**Cold start:**

```auto
User picks range set
   │
   ▼
Pick target = latest finalized header H_f
   │
   ▼
Request Range with multiproof(keys, H_f) → {values, proofs} (via snap sync)
   │
   ▼
Verify vs H_f → OK → store (value, proof, H_f)
               FAIL → discard & fallback
```

**Warm path (delta refresh):**

- On new finalized header, on send, or on schedule (Wi‑Fi/charging), refresh only what matters.
- Heuristics: keys touched by user since last header + anything past an age cap.
- We can snap sync a lot more metadata related to previous txs like receiver/senders account data, past contract state-updates etc..

![oopsie_snapsync_flow_labels_above_fix4_ready (1)](https://ethresear.ch/uploads/default/original/3X/4/2/42afbb2d989ab66640ae56f0b53d85ade12513af.svg)

**Trie path (conceptual):**

```auto
stateRoot (from H_f)
   │
 [branch]
 /     \
acct   acct ...
 |        \
 meta    storageRoot
             │
           [branch]── proofs only for the exact leaves we pin
             │
           storage leaf (slot)
```

---

![multiproof_presign_final](https://ethresear.ch/uploads/default/original/3X/4/2/4258f422521faecd6acdd35df4454d2fadb685fa.svg)

> Minimal proof: only the account leaf and specific storage leaves (e.g., allowance, balanceOf) plus the branch nodes needed to recompute stateRoot@H_f.

---

## Reading Data — Router Rules

![oopsie_wallet_call_routing_legend_border](https://ethresear.ch/uploads/default/original/3X/3/0/30f79157a601365e8ff238aaad2d6b3e7b06cedc.svg)

---

**Routing matrix (what goes to Snap sync vs RPC)**

> Quick map of common wallet calls, their primary path, and fallbacks.

| Bucket | Examples | Needs known leaf key? | Mempool needed? | Primary Path | Badge | Fallback |
| --- | --- | --- | --- | --- | --- | --- |
| Account meta | balance(A), nonce(A), codeHash(A) | No (account leaf is address-keyed) | No | Snap sync (multiproof) vs safe head (UI) / finalized (pre-sign) | VERIFIED | RPC (UNVERIFIED) if Snap sync slow/unavailable |
| Known storage slot | ERC-20 balanceOf, allowance; ERC-721 ownerOf; ERC-1155 balanceOf | Yes | No | Snap sync | VERIFIED | RPC (UNVERIFIED); optional bg-verify to upgrade |
| Derived / ABI-known slot | totalSupply() when slot mapped | Often yes | No | Snap sync if slot mapped; else RPC → learn & cache slot | VERIFIED (if snap sync) / UNVERIFIED (RPC) | RPC now; snap sync later once mapped |
| Arbitrary eth_call | router.getQuote(...), complex view | No | No | RPC (needs EVM execution) | UNVERIFIED (unless provider includes proof) | Optional bg discovery of slots (advanced) |
| Gas/fee & pending | eth_feeHistory, maxPriorityFee | No | Yes | RPC | UNVERIFIED | — |
| Estimate gas / simulate | eth_estimateGas, dry-run | No | Often | RPC | UNVERIFIED | — |
| Logs & receipts | eth_getLogs, getTransactionReceipt | No | No | RPC (indexed history) | UNVERIFIED | — |
| Tracing / debug | debug_traceTx, callTracer | No | No | RPC | UNVERIFIED | — |

**Why snap sync before RPC on a miss?**

- Authenticity: you get a Merkle multiproof back and can verify against your block header, turning reads into VERIFIED without trusting the provider.
- Batchability: router can batch multiple UI asks (balance, nonce, 3 token balances) into a single multiproof tied to one header → fewer round-trips and smaller total proof than N separate proofs.
- Privacy: rotating snapshotters + header-anchored reads reduces repeated raw-address spam to a single RPC origin. Thus reducing traceability & footprint metadata.
- Offline-tolerant: cached proofs remain meaningful (badged STALE) without network.

> For the avg. case, for ≤50 keys, a well-formed multiproof is on the order of tens of KB and verify in tens of ms on mobile. That often beats a handful of RPC calls + TLS + cold caches.
>
>
> This should mean:
>
>
> Wallets are happy (less RPC reliance).
> Users are happy (Better UX and privacy).
> RPCs get alleviated (They serve only requests which need them 100% (history, mempool-related stuff, tx simulation etc..)

---

---

# The uncomfortable part — who actually serves state?

OOPSIE leans on snap sync/multiproofs for authenticity. Today, snap-serving nodes (public sync nodes, a few public Geth, Nethermind and Besu nodes) are already saturated. In a ZK-EVM world, validators don’t need full state to prove/verify, so the natural question is: **who is incentivized to hold and serve state at all?**

Not validators. Not most solo builders (they’ll be squeezed between builders and provers).

That leaves two classes with any reason to carry state:

- Block builders (especially under FOCIL-like regimes): They still need read access to build sensible blocks, but their business model is latency-sensitive, not “serve the world proofs.”
- RPC providers: Centralization pressure increases. Their bandwidth is already eaten by eth_call, logs, mempool gossip. Serving snap sync for free has negative ROI.

If that’s our future, we risk a vicious circle:

fewer state holders → proofs harder to find → wallets fall back to RPC → RPCs get even more load → less appetite to run snap servers → even fewer state holders.

And there’s a second sting: user-held leaves age into uselessness for revival if all you keep is the value. A hundred blocks later, your leaf without a decent witness (siblings/branches up to the root) can’t help rebuild anything. The user’s “local state” degenerates into a pretty cache entry with no recovery value.

## The opposite arc: when state is served, expiry becomes tractable

If we push the ecosystem so that many actors are incentivized to hold and serve authenticated slices (snap sync/multiproof), the picture flips:

- Availability scales with demand. Wallet demand for proofs turns into a predictable revenue line for anyone exposing multiproofs (dapps for their own contracts, RPCs with per-KB pricing, builder-adjacent caches).
- Witnesses become a commodity. Small, content-addressed witness bundles (account proof + storage proofs) circulate, users and apps keep witness-rich fragments (pieces of data + their proof), not just raw values.
- Expiry ≠ exile. When state is pruned, revival = fetch a bundle from multiple sources and check it against a header you already trust. No global archives needed, just enough overlapping witnesses.
- Decentralization by slicing. Nobody needs all state. Many parties can profitably hold and serve their slice (per-domain, per-contract, per-prefix). That’s real, emergent state sharding without protocol sharding.

# Conclusion

Expiry is only real if state is served. OOPSIE-like clients matter only if they can keep up-to-date & authenticated data for users. **And, only, if they can do something with that data like reviving state**!

If ZK-EVM decouples validation from holding state, the default gravity is RPC + builder centralization. In that world, state-expiry is theater: you can “expire” state on paper, but revival just means asking the same few RPCs for answers you can’t independently authenticate.

OOPSIE flips the demand curve. By making wallets ask for multiproofs of named leaves and by showing authenticity in the UI, OOPSIE turns proof-backed state into a first-class product. That creates room for many actors—not just RPC oligopolies—to profitably hold and serve slices of state, which is exactly what makes expiry tractable. When witnesses are easy to get, expiry stops being a cliff and becomes “fetch a bundle, verify against a header, move on.”

**What can help to facilitate this?**

- Partial RPC solutions where re-execution is not needed. And partial state-holding still allows for proof-serving & snapsync range-constrained serving.
- Incentive-based state-serving. Either via RPC or Snapsync.
- Snapsync needs to be updated to a design where ranges can be missing and it still finalizes.

The north star: don’t centralize re-execution; decentralize witness serving.

*Next, we will delve into the depths of partial stateful nodes and explore the broader challenges of a ZKEVM–based future for Ethereum’s state availability.*

## Replies

**MicahZoltu** (2025-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> #### B) ERC balances (precise, verifiable)
>
>
>
> ERC‑20 balanceOf(owner)
>
> Key = (token, owner) → slot = keccak(owner || baseSlot_balances) (OZ layout uses slot 0 for balances)
> Value = uint256
>
>
> ERC‑721
>
> ownerOf(tokenId) → slot = keccak(tokenId || baseSlot_owners) (often slot 0)
> balanceOf(owner) → keccak(owner || baseSlot_balances) (often slot 1)
>
>
> ERC‑1155 balanceOf(owner, id)
>
> Nested mapping → keccak( owner || keccak(id || baseSlot) )
> Value = uint256

How much disk space does the full USDC state consume?  While I very much appreciate your desire to get down to the minimum size possible, I wonder if it is worth the effort compared to just grabbing the full state of tokens of interest.  If the difference is a handful of bytes (plus all of the proofs) vs MBs (plus all of the proofs), it may make sense to just pull down the MBs since I think the proof sizes will be the same or *smaller*.  If the full state for USDC token is GBs though, then selective balances would make more sense.

---

**MicahZoltu** (2025-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Logs & receipts eth_getLogs, getTransactionReceipt No No RPC (indexed history) UNVERIFIED —

While I know no one listens to me when I shout this into the wind, events (aka “logs”) should not be used for long term storage.  They should be used to notify chain followers of interesting things that occurred in a block.  A light client that is following head *can* utilize events for this trustlessly without an RPC server.

Use case:

1. User wants to make a payment to a friend from a mobile device.
2. The recipient opens their wallet and indicates that they are expecting a payment.
3. The sender opens their wallet and initiates the payment.
4. The recipient and sender’s devices both are following head looking for payment events to/from their account.
5. When the transaction is mined, recipient is notified and balance in wallet is updated.
6. When the transaction is mined, sender is notified and balance/nonce in wallet is updated.
7. Both devices continue to follow head until finality is reached (to ensure no reorg occurred).

---

**CPerezz** (2025-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If the full state for USDC token is GBs though, then selective balances would make more sense.

Indeed is more than 1GB. You can see that in 2024 it was already 1GB in [How to Raise the Gas Limit, Part 1: State Growth - Paradigm](https://www.paradigm.xyz/2024/03/how-to-raise-the-gas-limit-1) (see Figure 2). On top of that you also should account that most revival mechanisms require proofs to revive expired data.

So if you want Oopsie to be useful, you also need to store all intermediate nodes from the root of USDC contract until the root.

This is further explored in [The Future of State, Part 2: Beyond The Myth of Partial Statefulness & The Reality Of ZKEVMs - #4 by MicahZoltu](https://ethresear.ch/t/the-future-of-state-part-2-beyond-the-myth-of-partial-statefulness-the-reality-of-zkevms/23396/4) where we get numbers of the data needed in order to serve proofs for a particular contract. (TLDR, it’s arround 10GBs).

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> While I know no one listens to me when I shout this into the wind, events (aka “logs”) should not be used for long term storage. They should be used to notify chain followers of interesting things that occurred in a block. A light client that is following head can utilize events for this trustlessly without an RPC server.

As per this, I agree we can do better. Nevertheless, it doesn’t fix or address the core issues of Oopsie within the situation where Ethereum is going to be in a couple years.

---

**Julian** (2025-12-23):

Hey Carlos, thanks for the post!

If I understand correctly the idea is that light clients store the state and proofs the user is interested in. However, proofs need to be updated continuously as other parts of state change (as the authors of this post argued [On the impossibility of stateless blockchains - a16z crypto](https://a16zcrypto.com/posts/article/on-the-impossibility-of-stateless-blockchains/)). How would light clients ensure that they create proofs against the canonical state root? Are they expected to be constantly online or do they sync to the head of the chain when a user wants to send a transaction? If the light client syncs when the user wants to send a transaction, can we say anything how much transaction inclusion latency that would add?

---

**CPerezz** (2025-12-23):

Hey! Thanks for reading this [@Julian](/u/julian) and good question BTW.

The idea here is to leverage snap-sync mechanisms that already exist today in most clients and work by default.

Instead of needing to constantly keep proofs up-to-date, we can simply query the P2P network with a snapsync-request (technically we would be requesting a leaf rangeproof for only 1 leaf (or the few of interest we have)). And the network would get back at us with it (already synced at the top of the chain).

This, combined with the [sync-commitee](https://github.com/ethereum/annotated-spec/blob/160764ac180eca2cea3581f731ee96ac7098f9f7/altair/sync-protocol.md#introduction) that lightclients use gives us P2P user-generated proofs for our data which we can verify at tip-of-the-chain height.

Latency would be  in the order of`ms` for less than 10 leaves. For arround 50 we are looking at `<1s` for sure. I can try to get you numbers on that if it’s needed ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

With that we can be sure that our data is valid at anytime and get a proof for it if ours is invalid and for some reason we need it.

Notice that with statelessness and a heavily reduced count of full nodes serving these requests, this system might eventually collapse as the few nodes that remain would be overwhelmed with requests.

---

**Julian** (2025-12-23):

Thanks [@CPerezz](/u/cperezz)! Who do you intend to be the providers of state in this model? Is the idea that regular users who also run OOPSIE wallets provide state that others can snap-sync to or are they more professional RPCs?

---

**CPerezz** (2025-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Who do you intend to be the providers of state in this model?

The whole idea is that as the network is today, any full node is a provider by default (as long as they support SnapSync (so Geth, Nethermind & Besu).

Since snapsync requests are always served by default (even some RPC providers have them on).

And the pairing is done via P2P network and enode obtention. So it’s decently well distributed (though not uniformally I’d assume).

Wallets can serve their leaves only, so they aren’t the provider on any way or shape. This is more of a way to serve RPC calls, own your data locally and also have a “TLS-like system” for data any wallet needs (RPCs don’t send proofs with the data they provide).

---

**YanAnghelp** (2025-12-25):

The shortcomings observed today are not merely implementation artifacts, but rather symptoms of a structural flaw in the consensus design.

If consensus could be achieved in a round-isolated manner—without requiring access to global state or historical data—then, in principle, nodes would only need to store block hashes in order to verify the entire chain history.

Under such a model, the resource requirements for running a full node could be reduced to an extremely low level.

Of course, this is not feasible for strongly consistent systems like monetary blockchains, but the main pressure today appears to be on the execution layer, which may not require the same level of strong consistency as money.

