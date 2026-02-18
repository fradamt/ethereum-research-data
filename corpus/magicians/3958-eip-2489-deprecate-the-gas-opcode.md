---
source: magicians
topic_id: 3958
title: "EIP-2489: Deprecate the GAS opcode"
author: axic
date: "2020-01-24"
category: EIPs > EIPs core
tags: [opcodes, eip-2489]
url: https://ethereum-magicians.org/t/eip-2489-deprecate-the-gas-opcode/3958
views: 1471
likes: 6
posts_count: 12
---

# EIP-2489: Deprecate the GAS opcode

Discussion topic for https://github.com/ethereum/EIPs/pull/2489

## Replies

**Amxx** (2020-01-24):

> This is a breaking change and has a potential to break contracts. The author expects no contracts of any value should be affected.

I’m feeling unconfortable with that kind of claims … particularly while we are activelly discussing meta-transansaction repayment (which implies gas usage monitoring).

Do you have stats/analysis to back this claim?

---

**axic** (2020-01-24):

The EIP is not even merged as a draft (which would signal it is somewhat complete), so I would defer from arguing before it is merged. Only created this thread because it is a requirement for the EIP.

---

**3esmit** (2020-01-27):

I don’t understand the motivation of deprecating the GAS opcode. Can you explain it better? Seems like its related to UNGAS discussion.

Perhaps this EIP should deal with all aspects of UNGAS, not just with the GAS opcode?

---

**3esmit** (2020-01-27):

Regarding [EIP 1077](https://eips.ethereum.org/EIPS/eip-1077) this affect it’s design, and if there is plans on getting this approved on mainnet I can simply change the architecture to don’t use this opcode, however this will imply extra processing in the gas relayer side.

---

**sohkai** (2020-01-29):

aragonOS has a few places where we use the `gas` opcode to save gas to ensure we can return revert errors, including every user-controlled organization contracts (all proxies):

- DelegateProxy
- CallsScript

While this particular change would not *really* negatively affect them, outside of potentially confusing error messages that make debugging more difficult, I am also interested in the rationale and what patterns we should expect to be reliable where we’d like to ensure at least some measure of gas to handle error cases.

---

**wighawag** (2020-01-31):

If that change is made alone, this will break some contract for sure. We for example use the gas opcode to ensure a meta-tx receive the proper amount of gas. If the gas opcode always return 2**156-1 then our contract will always assume the meta-tx received enough amount of gas while it might not be the case. Relayer could thus maliciously make the meta-tx fails while getting the reward, if any.

I have been pushing for an EIP for quite some time that would remove the need for the gas opcode for taht particular use case (metatx)

So if we could get this first  : [ERC-1930 Allows specification of a strict amount of gas for calls](https://ethereum-magicians.org/t/erc-1930-allows-specification-of-a-strict-amount-of-gas-for-calls/3132)

Then maybe we could deprecate the GAS opcode

But the problem still remain that existing contracts will be affected

---

**wighawag** (2020-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> Perhaps this EIP should deal with all aspects of UNGAS, not just with the GAS opcode?

Same thoughts here.

For those not aware of the UNGAS proposal see the following video: https://youtu.be/0-Vld7GTRhQ?t=490

From what I gathered, the idea is that contract would not have access to gas anymore AND that an “out of gas” call will make the whole transaction revert, even if that call is at a lower depth.

If so, I think if we started ethereum from scratch, it would be an interesting approach to gas, as this would remove the ambiguity we currently get when contracts call other contract and the call fails.

But we would also need to support meta-transaction natively somehow because if an exception occurs down a chain of call as a result of a meta-tx and this revert the all tx in every case, the relayer would be paying for the failure. This would be a downgrade for what most meta-tx implementation do today : namely, ensure the relayer get paid even if the metatx inner call fails due to a lack ofgas

In any case as pointed out by [@karalabe](/u/karalabe) in the video this will surely have impact on existing contract even if contract are versioned via [EIP-1702](https://eips.ethereum.org/EIPS/eip-1702) as a new contract could be calling old contract and vice versa.

I am not sure how this would work.

Like if a contract U (ungas enabled) call a contract O (old contract), what happen when O or whatever old contract it is calling down the line runs out of gas?

And reversely, what if a contract O call a contract U and U run out of gas?

Similarly what if O need to read gas value ?

---

**k06a** (2020-02-03):

It seems we also need replace THROW with REVERT to avoid gas-eating subcalls. Else this would leads to millions of eaten gas: https://github.com/Synthetixio/synthetix/issues/243

---

**pinkiebell** (2020-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> So if we could get this first : ERC-1930 Allows specification of a strict amount of gas for calls
>
>
> Then maybe we could deprecate the GAS opcode
>
>
> But the problem still remain that existing contracts will be affected

^ This can fix most of the *general* issues about removing `GAS` opcode .

However, another problem I have in mind:

*If I have a system that wants to partly reimburse transaction costs of the current transaction in favour for the caller, how I’m going to do that after UNGAS?*

For everyone wondering, that is a useful property in verification games / fraud proving systems.

I could validate transaction receipts, but that creates a lot of problems and complexity.

---

**3esmit** (2020-02-07):

For GnosisSafe, it will be less impactful if the default value is `0x0000000000000000000000000000000000000000000000000000000000000001`, because it multiplies a calldata parameter `_gasPrice` against the return value of `gasleft()` (`GAS` opcode). So if the value returned is one, they can threat the `_gasPrice` as `_totalFee` without changing the contracts, and users with old software wont be authorizing the transfer of an unknown value.

---

**sorpaas** (2020-02-15):

Maybe relevant to this, also posted on Gitter:

> Look for some reviews on this https://corepaper.org/ethereum/compatibility/leaky/
> TLDR – gas metering is a leaky abstraction, and given current account models, it’s impossible to make gas cost completely unobservable. As a consequence, even account versioning cannot completely fix future issues for gas cost changes. Instead, we should pursuit what I call “reasonable backward and forward backward compatibility”, which can cover majority of cases. I do think this has noticeable amounts of implications (at least for me) for how we should view smart contract backward compatibility.
>
>
> This leads to 57-UNERR, which is a subset of 39-UNGAS and my opinion is that it’s more perferrable, because removing GAS opcode is unnecessary.
>
>
> Also just in case if anyone wants to discuss this in detail, I’ve just got an #ethereum Discord channel for Core Paper! Kulupu

TLDR – completely hiding GAS opcode’s effect is not possible, unless we change the current account model.

