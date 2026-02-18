---
source: magicians
topic_id: 19668
title: EIP-7685 General purpose execution layer requests
author: matt
date: "2024-04-15"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7685-general-purpose-execution-layer-requests/19668
views: 2552
likes: 11
posts_count: 24
---

# EIP-7685 General purpose execution layer requests

Discussion for [Add EIP: General purpose execution layer requests by lightclient · Pull Request #8432 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8432)

## Replies

**acolytec3** (2024-04-25):

I’ve started a [draft implementation](https://github.com/ethereumjs/ethereumjs-monorepo/pull/3372) of this EIP for ethereumjs and have a question regarding the Intra-type ordering.

The EIP states:

> Within the same type, order is not defined. This is because the data of the request is opaque as far as this EIP is concerned. The only valid ordering scheme would be lexicographical ordering of the opaque byte data.

If we don’t define any intratype order and make it exogenous to this EIP, doesn’t that make the `requestsRoot` non-deterministic where we have multiple requests of the same type since you could reorder them arbitrarily?  I suppose we can just create arbitrary test vectors and say we’re assuming the order of requests within a type is lexicographical for now?

---

**matt** (2024-04-25):

My perspective is that if a EIP uses 7685 and doesn’t define it’s intra-type ordering, it’s incomplete. Therefore I’m not sure how the ordering would be non-deterministic. Do you have an example maybe?

---

**acolytec3** (2024-04-25):

Ah, ok, that makes more sense.  It might be clearer in the EIP to say something like

> Within the same type, order is not defined. This is because the data of the request is opaque as far as this EIP is concerned.  Intra-type order should be determined by each request type.

instead of the comment about lexicographical ordering since that made me thing we needed to code that as a fallback in case an order was not otherwise defined.

I’ll create a simple request type and ordering mechanism in my work to use as a proof of concept.

---

**matt** (2024-04-25):

I made the clarification in the EIP [Update EIP-7685: clarify intra-type ordering by lightclient · Pull Request #8501 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8501)

---

**jochem-brouwer** (2024-04-25):

Then at this point, 7002 and 6110 are incomplete, right? They define the encoding of the request but not the ordering ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**matt** (2024-04-25):

Hmm 6110 does specifically say the ordering:

> Each deposit accumulated in the block must appear in the EIP-7685 requests list in the order they appear in the logs

However it isn’t said explicitly in 7002. It should be in the order it is pulled out of the queue (FIFO). I can make that explicit.

---

**jochem-brouwer** (2024-04-25):

Ah right, sorry, I did not see that part of 6110. Thanks ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

If you could make the order for 7002 more explicit that would be great! ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**etan-status** (2024-04-29):

About “Opaque byte array rather than an RLP array” rationale, it also means that it becomes challenging to upgrade existing schemes later on.

For example, EIP-6110 adds more RLP cruft, if it uses EIP-7685 it means that that RLP component cannot easily be replaced with SSZ or a SNARK friendly representation later on.

Also, the proposal attempts to be generic, but is not completely generic. For example, some operations may be desirable to execute at start of the block, some at end of the block, and so on.

It’s also a bit weird, to have deposits follow a completely different scheme than withdrawals. What’s the advantage of mixing different concepts into one tree, instead of continuing the existing scheme of simply using separate lists for separate operations? How many operations do we expect there to be? Is it more than 2-3? Do they thematically overlap, as in, would something as in EIP-6493 work out for these validator dependent operations?

---

**matt** (2024-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> For example, EIP-6110 adds more RLP cruft, if it uses EIP-7685 it means that that RLP component cannot easily be replaced with SSZ or a SNARK friendly representation later on.

I’m not sure why it is harder to replace. It seems equally as challenging as replacing, say, the withdrawals root with a hash tree root.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> It’s also a bit weird, to have deposits follow a completely different scheme than withdrawals.

Withdrawals are CL → EL communication, whereas deposits, exits, and partial withdrawals are EL → CL communication (a request).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> How many operations do we expect there to be? Is it more than 2-3?

My understanding is that there are many more possibilities for EL → CL requests to manage validators. We’re even discussing another one potentially for Prague: consolidations.

---

**etan-status** (2024-04-29):

> Withdrawals are CL → EL communication, whereas deposits, exits, and partial withdrawals are EL → CL communication (a request).

Makes sense, thanks for the clarification.

Considering that it gets transformed to a `deposit_receipts` list in the CL `ExecutionPayload`, maybe still simpler to just match that in the EL block header, as in, make it a `deposit_receipts` list there as well, instead of the list of prefixed opaque blocks.

How would JSON-RPC look for these? Would it return the prefixed opaque data, or something sensible (as is the case for withdrawals/receipts/transactions atm)?

---

**potuz** (2024-05-10):

I have a couple of questions regarding the statement about processing the requests in `process_execution_payload`.  I want to make sure that this EIP does not block completely ePBS.

1. The outcome of processing these requests can affect the beacon state right? (Eg deposits, withdrawals etc).
2. are the requests located in the CL ExecutionPayloadHeader or within the ExecutionPayload?

In ePBS these are processed at different times and the header may be present and processed with the full payload never be revealed. A situation that becomes difficult and even impossible in ePBS would be if some request that is forced to be processed during header processing (with the CL block) then forces the payload to have specific information. An example of this is withdrawals, which can be processed with the header in the CL block, and then the next payload is forced to fulfill them in the EL or it’s not valid. This doesn’t break ePBS because withdrawals are completely beacon state deterministic but if these requests require knowledge of the EL state that would be quite difficult.

If on the other hand the requests can be processed in the CL side when the payload is processed, this won’t be any problem.

---

**matt** (2024-05-10):

Hey you might be reading an old version. I ended up removing the wording around when / where the CL should process requests.

The EIP defines how requests should be saved in the EL. It is agnostic to how the CL stores requests.

---

**poojaranjan** (2024-07-11):

An overview of [EIP#132: EIP-7685:General purpose execution layer requests](https://youtu.be/3g71BGZFASE) with [@matt](/u/matt)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/d/d70560ba1113d9cad9d7a7063b0316507a710826.jpeg)](https://www.youtube.com/watch?v=3g71BGZFASE)

---

**SamWilsn** (2024-10-18):

Why does this proposal use `sha256` instead of `keccak256`?

---

**SamWilsn** (2024-10-18):

It’s SHA2-256 for compatibility with the CL (via [ethereum/consensus-specs#612](https://github.com/ethereum/consensus-specs/issues/612).)

---

**gumb0** (2024-12-02):

> A requests object consists of a request_type prepended to an opaque byte array request_data. The request_data contains zero or more encoded request objects.
>
>
>
> ```auto
> requests = request_type ++ request_data
> ```

I would like to know the size of `request_type`, I cannot find it in the EIP.

---

**eawosika** (2024-12-04):

Hi Ethereum magicians! The team at [2077 Research](https://research.2077.xyz/) recently published a deep dive on EIP-7685 for interested readers: [EIP-7685: General Purpose Execution Requests](https://research.2077.xyz/eip-7685-general-purpose-execution-requests). All feedback and comments are welcome.

---

**gumb0** (2024-12-12):

Requests root is not longer computed as merkle tree root, but just hash of a list of hashes, so this part of the article is outdated.

---

**gumb0** (2024-12-12):

[@matt](/u/matt) What is the rationale for the root being hash of hashes instead of just a hash of concatenation of requests? Seems like unnecessary extra work for double-hashing.

---

**eawosika** (2024-12-17):

Thanks for letting me know! We’ll update that part of the article.


*(3 more replies not shown)*
