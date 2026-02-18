---
source: magicians
topic_id: 21271
title: "EIP-7782: Reduce Block Latency"
author: benaadams
date: "2024-10-05"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7782-reduce-block-latency/21271
views: 745
likes: 11
posts_count: 6
---

# EIP-7782: Reduce Block Latency

Discussion topic for EIP-7781

https://github.com/ethereum/EIPs/pull/8931

Reduce Ethereum’s slot time from 12 seconds to 8 seconds

1. reduce based rollup latency
2. increase transaction throughput by approximately 33% without increasing individual block or blob counts
3. distributing bandwidth usage over time to lower peak bandwidth requirements and maintain network efficiency.

This would be equivalent to increasing blob count from 6 to 8 or gas limit from 30M to 40M; however this approach does not increase peak bandwidth.

## Replies

**daniellehrner** (2024-10-06):

I think one thing that is currently missing is decreasing the validator rewards accordingly.

Validators will propose more blocks per year and and will attest to more epochs. If we keep the current rewards, more ETH will be issued than is today.

IMO changing the issuance should not be mixed together with performance increases, but should rather be a separate discussion.

The reward decrease should be a simple enough and not add much complexity to the EIP

---

**shashi0x00** (2024-10-07):

- Is there a way to determine the expected bandwidth and hardware requirements for solo stakers like myself?
- I understand the goal of increasing throughput, but how do we quantify the impact this will have on solo stakers? Specifically, how many solo stakers might be adversely affected or forced out?
- I came across a post on X where Vitalik mentioned another sensible approach that involves increasing throughput while also reducing the minimum staking requirement (e.g., to 16 ETH or 8 ETH). Will this idea be part of this EIP, or is it even being considered at the moment?

---

**Iceblue** (2024-10-07):

As Layer1, the slot time should be slightly longer rather than shorter while ensuring the goal of supporting enough and diverse validators. Increasing it from 12s to 16s~32s is a more correct choice. How do you ensure geographic diversity among validators?

---

**catwith1hat** (2024-10-09):

A thought experiment:

Assume there is EIP-X that wants to cut slot times in half to 6 seconds, and also cuts max gas in half to half the block size. Assume that before EIP-X your uplink/downlink bandwidth is barely able to receive all the required data within 11 second. You need the extra 1 second to verify and execute the block, so you just hit the 12 second mark before you need to start downloading data for the next slot.

After EIP-X is implemented, you will not be able to participate in the network anymore. Why? Because the block verification and execution time is not going to get cut in half. There is a fixed cost in that process that is not dependent on the block size. Let’s say the fixed cost is only 10% out of your 1 second processing time, i.e. 0.1 sec. Then post-EIP-X, you still have a harder bandwidth requirement than before as (11/2+0.9/2+0.1) > 12/2.

I have ignored attestation data and attestation timing in the thought experiment above. I believe that attestation data requirements within a slot wouldn’t change. You still need to send/receive the same amount per slot independent of the fact that the execution payload size post-EIP-X is half. So you have another fixed cost.

You can take the whole thought experiment further. Just keep cutting slot times in half, while also cutting block size in half. I argue that you will all those cuts adverse effect low bandwidth participants. It increases their (peak) bandwidth requirement, where “peak” means in the first half of the slot for them to be ready to attest to the new HEAD.

Frankly, an increase in the gas limit doesn’t seem very pressing giving the success of the L2s. By the same argument, EIP-7782 as an alternative means to increase block space expansion should be equally considered low priority. While faster confirmations are nice, based preconfirmations look more promising.

---

**MicahZoltu** (2025-04-28):

It seems like it would be best to separate `gas_per_second` and `minutes_per_epoch` into independent variables first, before making changes like this.  That would allow us to make changes to things like slot time without having to simultaneously touch state growth, average bandwidth, or finality times.  Each of those variables could be changed/updated in their own respective EIPs and discussed independently from a change like this.

The advantage of such an approach is that concerns like average bandwidth use, finality time, and state growth can be ignored and instead discussion can focus on things like propagation time between stakers, attestation collection timing, etc. which are all directly related to slot times.

---

This change would increase the max state growth rate by 50%.  While there are steps being taken to limit non-state storage growth requirements, state growth is permanent and perpetual at the moment with no way to cap it.  Until this unbounded growth problem is addressed, it seems prudent to avoid any significant gas limit increases.

At Ethereum’s current growth rate, it has already pushed many (I believe almost all) home node operators out of the market, and as storage requirements continue to grow more and more home operators are pushed out.  Even running in a datacenter is getting more challenging as large-disk servers tend to be much more rare and much more expensive than high CPU servers.

