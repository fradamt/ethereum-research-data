---
source: magicians
topic_id: 23259
title: "EIP-7917: Deterministic proposer lookahead"
author: linoscope
date: "2025-03-25"
category: EIPs > EIPs core
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/eip-7917-deterministic-proposer-lookahead/23259
views: 624
likes: 16
posts_count: 14
---

# EIP-7917: Deterministic proposer lookahead

Discussion topic for [EIP-7917: Deterministic proposer lookahead](https://eips.ethereum.org/EIPS/eip-7917)


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7917)





###



Pre-calculate and store a deterministic proposer lookahead in the beacon state at the start of every epoch










#### Summary

This EIP ensures that the proposer schedule for upcoming epochs is determined and stored in the beacon root at the start of each epoch. By introducing a deterministic proposer lookahead, it eliminates unpredictable changes to the next epoch’s lookahead stemming from effective balance fluctuations (e.g., due to slashings, penalties, or increased validator balances)—an issue exacerbated by [EIP-7251](https://eips.ethereum.org/EIPS/eip-7251)’s MaxEB increase. As a result, preconfirmation protocols reliant on a stable, predictable proposer schedule can operate more securely and with less complexity. It also enables straightforward on-chain access to the proposer lookahead via the beacon root, which highly simplifies the on-chain component of preconfirmation protocols. Furthermore, it removes a potential source of grinding attacks via effective balance changes, and potentially simplifies client implementations for lookahead handling.

For more details, refer to the [EIP](https://github.com/ethereum/EIPs/pull/9530) or the [consensus-spec changes](https://github.com/ethereum/consensus-specs/pull/4190).

#### Update Log

- 2025-03-20: Issue around lookahead instability through MaxEB and it’s impact to preconfs discussed: Fabric Call #001
- 2025-03-23: Consensus spec change PR opened: consensus-specs/pull/4190
- 2025-03-24: EIP PR opened: EIPs/pull/9530
- 2025-03-24: EIP presented: Fabric call #002
- 2025-03-24: Thread by author summarizing the EIP: Post
- 2025-03-25: Thread by author answering frequently asked questions: Post
- 2025-04-15: PEEPanEIP EIP-7917: Deterministic proposer lookahead: Video
- 2025-05-29: EIP-7917 SFI’d for Fusaka with target of fusaka-devnet-1 in ACDC #158: Summary

#### External Reviews

- 2025-03-23: Discussion around the feature starting in consensus-specs/pull/4190

#### Outstanding Issues

None as of 2025-03-25.

## Replies

**dantaik** (2025-03-27):

Thanks to Lin and Justin for authoring this EIP. It’s a critical piece for enabling based preconfirmation. Let’s support its inclusion in the Pectra upgrade.

---

**linoscope** (2025-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dantaik/48/14663_2.png) dantaik:

> Let’s support its inclusion in the Pectra upgrade.

Thanks for the support! (I guess you meant Fusaka, which is the earliest this could be in ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12))

---

**dapplion** (2025-04-02):

Hey! Neat proposal. I strongly support modifying the protocol to best support based and native rollups. Offering fast and **reliable** pre-confirmations is a key part of that. However, it appears that the chance the function `compute_proposer_index` (Electra spec) returns distinct proposers is extremely low (less than once per year).

I ran the numbers here and got very low probabilities of the effective balance change causing issues.


      ![image](https://hackmd.io/favicon.png)

      [HackMD](https://hackmd.io/@dapplion/eip7917_statistics)



    ![image](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Beacon proposers are selected with this function










Some questions:

- How much lookahead do you estimate pre-conf users would need? Giving
- Is a failure rate of 0.0001% acceptable?
- Another source of instability, how will you handle missed slots?
- Quoting from the EIP “This highly simplifies the implementation of on-chain components for based preconfirmation protocols.” can you detail how?

---

**linoscope** (2025-04-03):

Hi [@dapplion](/u/dapplion) , thanks a lot for the detailed writeup! Good to have these concrete numbers, it really helps. However, even if the possibility of lookahead change is *very rare*, as long as the possibility is non-zero it remains problematic for preconf protocols, at least in our current design. To explain, some context around lookahead handling in preconf protocols is needed, so wrote this document to provide that:


      ![image](https://hackmd.io/favicon.png)

      [HackMD](https://hackmd.io/@linoscope/eip-7917-from-preconf-protocol)



    ![image](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



What happens if we don't have a

---

**poojaranjan** (2025-04-30):

**PEEPanEIP-7917: Deterministic proposer lookahead with [@linoscope](/u/linoscope) & [@JustinDrake](/u/justindrake)**

  [![image](https://img.youtube.com/vi/oFSUU91BMOg/maxresdefault.jpg)](https://www.youtube.com/watch?v=oFSUU91BMOg)

---

**taxmeifyoucan** (2025-05-30):

Does this EIP imply that implementation of Whisk/SSLE is not going to be possible?

Attack on proposers is considered in the EIP from RANDAO perspective but DoS is also a potential issue

---

**linoscope** (2025-05-30):

Thanks for the questions! Both good points worth clarifying here.

> Does this EIP imply that implementation of Whisk/SSLE is not going to be possible?

Not really. Many SSLE constructs do not remove the lookahead but rather replace it with an encrypted one. This EIP will be fully compatible with this, as it can just be a “deterministic encrypted lookahead.” There’s also a deeper question about combining preconfirmations with SSLE, though. Technically, they can coexist—for instance, by having the SSLE proposer reveal themselves with a ZK proof (as suggested by Justin in the [original preconf post](https://ethresear.ch/t/based-preconfirmations/17353)). It is also worth noting that APS envisions more sophisticated (i.e., more DDoS‑resistant) execution proposers, reducing the need for SSLE.

> Attack on proposers is considered in the EIP from RANDAO perspective but DoS is also a potential issue

Is this about SSLE being important for DoS prevention and concern that this EIP will block it? If so, it is answered above.

If it’s about the concern of having a more deterministic lookahead leading to more DoS vectors (a common question we get), this EIP doesn’t really “increase” the DDoS attack surface. A very high approximation of the next epoch lookahead is already visible in current-day Ethereum, as EB usually doesn’t change during epochs. This EIP simply makes this “very high approximation” to “deterministic”.

---

**taxmeifyoucan** (2025-05-30):

Thank you very much for the quick and thorough answer!

I see it doesn’t make such a difference in practice compared to current situation, got it. There haven’t been much work on Whisk recently so I see the SSLE should to be updated to accommodate preconfs

---

**daniel_web3** (2025-06-02):

If deterministic look-ahead lets a builder know—or at least strongly expect—that it will win several consecutive payloads, could it game the fee-adjustment logic (base-fee or blob-fee) by nudging the values up or down over that streak to boost its own revenue at users’ expense?

---

**linoscope** (2025-06-02):

I belive this answer above is also relevant to your question:

> If it’s about the concern of having a more deterministic lookahead leading to more DoS vectors (a common question we get), this EIP doesn’t really “increase” the DDoS attack surface. A very high approximation of the next epoch lookahead is already visible in current-day Ethereum, as EB usually doesn’t change during epochs. This EIP simply makes this “very high approximation” to “deterministic”.

So right now, in current-day Ethereum, we *already* have an “almost” deterministic lookahead, this EIP just changes that to “completely” deterministic. So whatever exploitation vector exists with having a visible and public lookahead existed before this EIP and will continue to exist after this EIP. There are discussions about mitigating the exploitation vector via public lookaheads (e.g., SSLE, shorter lookahead, etc) but those are independent discussions from this EIP I would say.

---

**daniel_web3** (2025-06-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/linoscope/48/14642_2.png) linoscope:

> So whatever exploitation vector exists with having a visible and public lookahead existed before this EIP and will continue to exist after this EIP.

This makes a lot of sense - thanks!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/linoscope/48/14642_2.png) linoscope:

> but those are independent discussions from this EIP I would say

… absolutely. This EIP just made me think about it again ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**Uliana** (2025-10-21):

I have some questions about phrasing.

## 1: Epoch Reference

The document switches between epoch reference conventions:

**In Motivation:**

- Uses “epoch N” as current, “epoch N+1” as target
- “the beacon proposer schedule of epoch N + 1 is not fully predictable from the beacon state during epoch N”

**In Security Considerations:**

- Uses “epoch N” as the target directly
- “the lookahead of epoch N is still determined by the RANDAO of epoch N - MIN_SEED_LOOKAHEAD - 1”

Both are technically correct but use different reference points, which can be confusing when understanding the timing relationships.

## 2: “Next MIN_SEED_LOOKAHEAD + 1” Ambiguity

The Abstract states: “pre-calculate and store…for the next MIN_SEED_LOOKAHEAD + 1 epochs”

This phrasing suggests looking MIN_SEED_LOOKAHEAD + 1 epochs into the future, but the implementation actually stores:

- Current epoch (already started)
- Plus MIN_SEED_LOOKAHEAD future epochs
- Total coverage = MIN_SEED_LOOKAHEAD + 1 epochs

---

**SamWilsn** (2026-01-19):

Someone opened [a bug](https://github.com/ethereum/EIPs/issues/10447) instead of commenting here:

> ## Overview
>
>
>
> I noticed some phrasing inconsistencies that could benefit from clarification.
>
>
>
> ## Issue 1: Epoch Reference Inconsistency
>
>
>
> The document switches between epoch reference conventions:
>
>
> In Motivation:
>
>
> Uses “epoch N” as current, “epoch N+1” as target
> “the beacon proposer schedule of epoch N + 1 is not fully predictable from the beacon state during epoch N”
>
>
> In Security Considerations:
>
>
> Uses “epoch N” as the target directly
> “the lookahead of epoch N is still determined by the RANDAO of epoch N - MIN_SEED_LOOKAHEAD - 1”
>
>
> Both are technically correct but use different reference points, which can be confusing when understanding the timing relationships.
>
>
>
> ## Issue 2: “Next MIN_SEED_LOOKAHEAD + 1” Ambiguity
>
>
>
> The Abstract states: “pre-calculate and store…for the next MIN_SEED_LOOKAHEAD + 1 epochs”
>
>
> This phrasing suggests looking MIN_SEED_LOOKAHEAD + 1 epochs into the future, but the implementation actually stores:
>
>
> Current epoch (already started)
> Plus MIN_SEED_LOOKAHEAD future epochs
> Total coverage = MIN_SEED_LOOKAHEAD + 1 epochs
>
>
>
> ## Suggestion
>
>
>
> Would the authors be open to clarifying these phrasings for consistency? Happy to submit a PR if that would be helpful.
>
>
> Thanks.
> Cc @linoscope

