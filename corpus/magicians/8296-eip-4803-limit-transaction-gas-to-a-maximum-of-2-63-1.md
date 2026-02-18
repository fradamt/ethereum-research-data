---
source: magicians
topic_id: 8296
title: "EIP-4803: Limit transaction gas to a maximum of 2^63-1"
author: axic
date: "2022-02-14"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-4803-limit-transaction-gas-to-a-maximum-of-2-63-1/8296
views: 2457
likes: 7
posts_count: 17
---

# EIP-4803: Limit transaction gas to a maximum of 2^63-1

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4803)





###



Valid transactions must have a reasonable gas limit










This is a follow up of [ACD#120](https://github.com/ethereum/pm/blob/master/AllCoreDevs-Meetings/Meeting%20120.md#limiting-account-nonce-eip-2681-vs-3338) where it was agreed to follow up the EIP-2681 and split more of EIP-1985 content into individual EIPs.

## Replies

**axic** (2022-02-14):

[@chfast](/u/chfast) suggested to further reduce this limit to `2^31-1`, because it would allow removing the “call depth check” from the EVM.

The call depth is limited to 1024, but the Tangerine Whistle hardfork introduced [EIP-150](https://eips.ethereum.org/EIPS/eip-150) with the “63/64th rule”. That rule makes it not realistic to exhaust the 1024 limit with the current and historical block gas limits. However having `2^31-1` would allow removing it entirely – or in practice combine the various checks into a few branches.

A `CALL` costing 1 gas would allow 1138 call depth, while 4 gas would terminate after 1021 depth. Note that a call currently costs as at least 100 gas ([EIP-2929](https://eips.ethereum.org/EIPS/eip-2929)).

---

**axic** (2022-02-14):

For historical reference, [this proposal](https://github.com/ethereum/EIPs/issues/92) was also discussed in 2017. There was a suggestion for `2^62-1` as a limit there.

Additionally, [here](https://github.com/ethereum/EIPs/issues/106) it was suggested to explicitly enforce this on the block level too. It is unlikely to be worth it, given the strict rules about increasing the block gas limit.

---

**MicahZoltu** (2022-02-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> suggested to further reduce this limit to 2^31-1, because it would allow removing the “call depth check” from the EVM.

`2^31-1` would also fit into the integer space of a double, which means you could store this value in a JavaScript `number` without fear of running into rounding errors.

---

**axic** (2024-11-27):

Proposed discussing this on the next ACDE: [Execution Layer Meeting 201 · Issue #1197 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1197#issuecomment-2504831879)

---

**axic** (2024-11-27):

There is a somewhat related EIP being proposed: [Eip 7825: Transaction Gas Limit Cap](https://ethereum-magicians.org/t/eip-7825-transaction-gas-limit-cap/21848)

This proposes a much stricter limit (30 Mgas vs. 2^63-1 or 2^31-1) and has a different motivation, but has a similar effect. I am not sure it is applicable from genesis, but my hunch is that EIP-4803 *is applicable*.

For the EVM perspective EIP-4803 makes a lot of sense as a *hard limit*, but could make sense having EIP-7825 as a *soft limit* on the tx/block level. Perhaps these two could be discussed together on ACDE.

cc [@Giulio2002](/u/giulio2002)

---

**axic** (2024-12-05):

[@matt](/u/matt) regarding your question on ACD, from the rationale:

> 2^63-1 vs 2^64-1
>
>
> 2^63-1 is chosen because it allows representing the gas value as a signed integer, and so the out of gas check can be done as a simple “less than zero” check after subtraction.

The check can be as simple as with signed numbers:

```auto
gasAvailable -= cost
if gasAvailable < 0:
  raise OOG
```

(In theory this also allows processing multiple instructions and checking OOG once – this is not realistic given we need to stop at the exact OOG spot)

When working with unsigned numbers:

```auto
if gasAvailable < cost:
  raise OOG
gasAvailable -= cost
```

geth currently uses uint64, and with the EIP they do not need to change that, however they can, and use a check like above, which could be cheaper on most CPUs.

[@chfast](/u/chfast) since you had a strong preference for the signed version, let me know if you have anything to add.

---

**axic** (2024-12-05):

[@shemnon](/u/shemnon) gave a better terminology for the distinction:

- EIP-4803 is the parsing limit
- EIP-7825 is the configuration limit

---

**shemnon** (2024-12-09):

I think we should give strong consideration to the JavaScript limit of 2^53-1.

My reasoning is that traces are often in JSON, and ensuring that gas values will fit into a JSON number will simplify generation and consumption of those traces.

That allows for over 9 quadrillion gas (9,007,199,254,740,991) in a transaction, which at 1 MegaGas/sec would take over 285 years to execute.  At 1 TeraGas/Sec that is still 104 days.

Unless there is existential change to the model of a transaction or what amount of work 1 unit of gas provides then this amount of gas should be sufficient for any reasonable block size.

---

**sbacha** (2025-01-13):

Just pointing it out there, there are some legit use cases, such as Convex protocol global shutdown which uses ~22mil gas, see https://github.com/mds1/convex-shutdown-simulation

---

**shemnon** (2025-01-13):

Given Base’s aim for Gigagas/sec I think we need to be prepared for Gigagas (10^9) transactions.  JSON 53 bits gives us 9 Peta gas (10^15), (9 Giga Mega gas).  63 bits gives us 9 Exa gas (9,000 Peta Gas).  Barring pointless memory allocations it should be enough for the next 5-10 years.

---

**wjmelements** (2025-01-15):

Why not 2^64-1? Gas doesn’t need to be a signed integer.

---

**pdobacz** (2025-01-15):

Here is the rationale behind signed: [EIP-4803: Limit transaction gas to a maximum of 2^63-1 - #7 by axic](https://ethereum-magicians.org/t/eip-4803-limit-transaction-gas-to-a-maximum-of-2-63-1/8296/7), also mentioned in the EIP

---

**wjmelements** (2025-01-15):

This isn’t compelling to me. The signed and unsigned versions are the same number of lines of code. It sounds like this was pushed by someone (perhaps [@chfast](/u/chfast)?) without a solid rationale.

---

**MicahZoltu** (2025-01-16):

1. Not all languages have unsigned numbers (e.g., JavaScript).
2. Sometimes there are simplifications to accounting that can be done if you allow negative numbers (there is a place clients already do this in either balance or gas accounting, I forget which).
3. You may not have an unsigned value for the limit, but you may have an unsigned value that is added to it, and if the limit is unsigned you can end up with needing to do a type conversion during the algebra.

I think the biggest argument though is just that 2^64 doesn’t buy us much compared to 2^63 and even a little bit of a reason to do 2^63 is sufficient to beat that.

---

**chfast** (2025-01-16):

The only difference between signed and unsigned integers in this context currently that with signed integers you can delay the check:

```python
gas -= cost1;
gas -= cost2;
if gas < 0:
   exit();
```

On the other hand, I’m considering switching to 32-bit variant internally.

---

**wjmelements** (2025-01-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Not all languages have unsigned numbers (e.g., JavaScript).

This is the best reason I think. I think Javascript doesn’t even have integers, but java doesn’t have unsigned integers. The lack of unsigned types in some programming languages should be added to the Rationale.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> You may not have an unsigned value for the limit

I don’t understand this part. All of the gas calculations I have done use unsigned longs. Is there a calculation with a negative parameter?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Sometimes there are simplifications to accounting that can be done if you allow negative numbers

I doubt it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> with signed integers you can delay the check

Out of gas checks should be done eagerly to avoid DoS.

