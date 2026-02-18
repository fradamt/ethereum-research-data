---
source: magicians
topic_id: 3557
title: EIP-2242 Transaction postdata
author: adlerjohn
date: "2019-08-17"
category: EIPs > EIPs core
tags: [eth1x]
url: https://ethereum-magicians.org/t/eip-2242-transaction-postdata/3557
views: 4171
likes: 0
posts_count: 12
---

# EIP-2242 Transaction postdata

[Link to EIP on GitHub](https://github.com/ethereum/EIPs/pull/2242).

The discussion on transaction calldata gas cost reduction—EIP-2028—yields numerous data points that support extremely aggressive reduction in costs of posting data on-chain, in order to curb state growth. This EIP introduces a separate field in transactions for data that is used exclusively for this purpose (*i.e.*, not readable in the EVM).



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/ac8455/48.png)
    [EIP-2028: Transaction data gas cost reduction](https://ethereum-magicians.org/t/eip-2028-transaction-data-gas-cost-reduction/3280) [EIPs](/c/eips/5)



> This is to discuss the EIP I am currently creating. Will fill this out later

## Replies

**guthlStarkware** (2019-08-19):

Thanks [@adlerjohn](/u/adlerjohn) for building on top of 2028.

To be honest, I don’t see the point in having an extra field. As explained in the analysis, going through the EVM costs less than 0.3 gas per word. I don’t see the point of adding an extra field as it would create a formatting and development overhead without strong benefits.

---

**adlerjohn** (2019-08-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> As explained in the analysis, going through the EVM costs less than 0.3 gas per word.

This analysis, I’m presuming?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png)[EIP-2028: Transaction data gas cost reduction](https://ethereum-magicians.org/t/eip-2028-transaction-data-gas-cost-reduction/3280/14)

> For a calldata input of size N bytes, if this verification operations were done in the EVM, the gas cost would be 30 gas for the first invocation of keccak and 6 gas for each additional word (32 bytes), totaling 30+6 * N / 32 gas. Asymptotically (neglecting the first 30 gas) this gives a gas price of roughly 6 for every 32 bytes, or 0.2 gas per byte.

You’d have to account for the costs of Merkeizing the data (some schemes require this, rather than simple hashing), which would end up quite a bit higher. You’d also have to account for the cost of calldata itself, which is going to be 16 gas per byte. So the costs of performing this operation on-chain are actually quite high.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> I don’t see the point of adding an extra field

If you’re using fraud proofs, you can’t simply re-post a transaction and check the calldata, as the transaction’s calldata and the contract call’s calldata may be completely different:

https://twitter.com/nicksdjohnson/status/1155672897756774400

Additionally, the separate field is particularly useful for [multi-threaded data availability](https://ethresear.ch/t/multi-threaded-data-availability-on-eth-1/5899), which is going to be the subject of a sister EIP.

---

**guthlStarkware** (2019-08-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adlerjohn/48/2165_2.png) adlerjohn:

> If you’re using fraud proofs, you can’t simply re-post a transaction and check the calldata, as the transaction’s calldata and the contract call’s calldata may be completely different:

How would it be different? Also, is not collecting the transmission data easy to extract from the sync?

If you want to push fraud proof, the first person to post the data needs to show the link between the statement and the data. Therefore, needs to be part of the EVM.

---

**adlerjohn** (2019-08-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> How would it be different?

Did you read the linked Twitter thread? It actually answers this exact question.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> Also, is not collecting the transmission data easy to extract from the sync?

Not really, at least not without breaking backwards compatibility.

https://twitter.com/nicksdjohnson/status/1155685078774820865

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> If you want to push fraud proof, the first person to post the data needs to show the link between the statement and the data.

Yes, you would need to save something in state, in this case some unique identifier for the transaction. Unfortunately, I just realized there is no opcode for such an identifier ([though one was proposed](https://github.com/ethereum/EIPs/issues/222)). It would be fairly trivial to implement as a dependency to this EIP, or this EIP could be wrapped into the sister one I mentioned above. I personally prefer the former, what do you think?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guthlstarkware/48/2064_2.png) guthlStarkware:

> Therefore, needs to be part of the EVM.

The linked ethresearch post describes how this would be done in a backwards-compatible manner:

> Clients can then go through transactions in a block (or even in their mempool!) and compute the reduction, inlining the result into the appropriate transaction’s calldata.

---

**guthlStarkware** (2019-08-22):

My bad! I did not see it was a twitter thread. Went right away on the multithread part. Getting back to you ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**adlerjohn** (2019-08-22):

Haha it’s all good. I was actually confused as heck at first as well, when [@Arachnid](/u/arachnid) brought it up.

The essence is here:

https://twitter.com/nicksdjohnson/status/1155669590032228352

with the note that “data only available to an archive node” isn’t easy to re-post on-chain in a provably attributable manner.

---

**guthlStarkware** (2019-08-22):

So, I’m going to reply superficially. I don’t see relying on archive node to be a no go as any full node can recreate an archive node. Data Availability for layer 2 is a worst case scenario mechanism. Using a simple calldata with a merklelizer precompile is probably the easiest path.

In any case, this is very superficial answer as I did not have the time to look at all the links you posted. Let me take some time to dive in and understand it better ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**MrChico** (2019-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adlerjohn/48/2165_2.png) adlerjohn:

> Did you read the linked Twitter thread? It actually answers this exact question.
>
>
>  guthlStarkware:

I’m not sure I understand why this is a counterargument.

It seems like it would be quite easy to include fraud proofs in tx data, just send a tx to a noop contract (for exmple with code `0x00`). To get your fraud proof, simply get the tx.data. What am I not getting here?

On another note, even if your tx would run out of gas, your `postdata` would still be available and serve its purpose. It doesn’t seem quite right from a design perspective to retain the same utility regardless of how much gas would be used.

---

**adlerjohn** (2019-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrchico/48/1427_2.png) MrChico:

> It seems like it would be quite easy to include fraud proofs in tx data, just send a tx to a noop contract (for exmple with code 0x00 ).

The linked explanation is for sending *from* a contract, not sending *to* a contract. There’s no easy way to link calldata to a transaction’s `data` field, as the calldata may come from a contract (modifying `data`).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrchico/48/1427_2.png) MrChico:

> On another note, even if your tx would run out of gas, your postdata would still be available and serve its purpose. It doesn’t seem quite right from a design perspective to retain the same utility regardless of how much gas would be used.

I agree. As written, that seems to be what happens. The EIP should be re-written to use the same semantics as calldata (which I’m assuming is: if the account doesn’t have enough gas to pay for calldata, then the transaction is invalid, rather than valid but reverting). Good catch.

---

**MrChico** (2019-09-20):

> The linked explanation is for sending  from  a contract, not sending  to  a contract. There’s no easy way to link calldata to a transaction’s  data  field, as the calldata may come from a contract (modifying  data ).

Exactly, this is why the linked explanation seems irrelevant to the topic at hand. Your proposal wouldn’t allow contracts to submit tx postdata either (because only EOA can make transactions).

There doesn’t seem to provide any substantial benefit over just using the `tx.data` field for your purposes

---

**adlerjohn** (2019-09-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrchico/48/1427_2.png) MrChico:

> There doesn’t seem to provide any substantial benefit over just using the tx.data field for your purposes

I agree! I split up the whole proposal into what will become a series of EIPs. This first one on its own is in fact basically pointless. See twitter thread ![:point_down:](https://ethereum-magicians.org/images/emoji/twitter/point_down.png?v=12)

https://twitter.com/jadler0/status/1174859441377828865

