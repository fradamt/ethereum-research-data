---
source: magicians
topic_id: 4365
title: "EIP-2733: Transaction Package"
author: matt
date: "2020-06-17"
category: EIPs
tags: [core-eips, transactions, eip-2733]
url: https://ethereum-magicians.org/t/eip-2733-transaction-package/4365
views: 3140
likes: 7
posts_count: 10
---

# EIP-2733: Transaction Package

Discussion thread for [EIP-2733: Transaction Package](https://github.com/lightclient/EIPs/blob/transaction-package/EIPS/eip-2733.md).

This EIP was inspired by the [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718), [native batched transaction](https://ethereum-magicians.org/t/eip-native-batched-transactions/4337), and the need to [maintain atomicity](https://ethresear.ch/t/native-meta-transaction-proposal-roundup/7525) of meta-tx inner txs and payment txs.

## Replies

**MicahZoltu** (2020-06-23):

Thinking out loud, and not sold either way, but I wonder if there is value in generalizing this to say that "in any transaction that has multiple child transaction, `RETURNDATASIZE` and `RETURNDATACOPY` will initially be seeded with the previous transaction’s return data.

This would allow 2718 batch transactions to gain access to return data in subsequent transactions, as well as future transaction types.  We may need to define what is a “batch” though?  What if you have multiple transactions from different accounts that are batched by a third party, do those get return data set or not?

One concern I have with this is that it would allow contracts to discriminate on whether or not the transaction was part of a batch.  On the other hand, I’m hesitant to prevent useful features just because some contract authors will be bad.

---

**matt** (2020-06-23):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> in any transaction that has multiple child transaction, RETURNDATASIZE and RETURNDATACOPY will initially be seeded with the previous transaction’s return data.

I think generalizing this behavior for any batch of txs makes sense. The two issues you raised are interesting:

1. Is it okay to get return data for a tx from a different account?
2. Is it okay that contact authors can discriminate against tx batches?

I don’t have enough context w.r.t. 1), but my intuition is that this is okay since the return values are public anyways. It does seem dirty to leak that information though. I feel stronger about 2) and it seems okay since it brings a lot of functionality. It is also similar to the current ability to discriminate against contracts vs. EOAs.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> We may need to define what is a “batch” though?

I’m thinking we define a “batch” as batch in 2711, since it is the only definition that would be known by the protocol. We should be able to extend this definition to other tx types on a case-by-case basis.

---

**zemse** (2020-07-16):

> rlp([N, rlp([nonce, v, r, s, [inner_tx_0, ..., inner_tx_n]])
> inner_tx_n = [chain_id, to, value, data, gas_limit, gas_price]

Was checking out the EIP, and I got a thought of pulling the `chain_id`out. Because is it possible to process multiple `chain_id`s in a particular chain?

`rlp([N, rlp([nonce, 2 * chain_id + 35 + v, r, s, [inner_tx_0, ..., inner_tx_n]])`

`inner_tx_n = [to, value, data, gas_limit, gas_price]`

Is there any flaw in this?

---

**matt** (2020-07-16):

Yep, that is a good point. Thank you for your suggestion. This EIP is overdue for an update - I’m thinking of rewriting it to focus on the cross-tx communication and rely on EIP-2711 for batching semantics (which is extracting the `chainid`). But if we don’t go down that path I will update with your suggestion.

---

**axic** (2020-09-07):

After reading the EIP, I actually thought both `chain_id` and `gas_price` should be outside, and not part of the `inner_tx`.

Furthermore it would make sense to highlight that a contract could use `returndatasize() != 0` to check whether they are being executed as part of a transaction package (as a follow-up transaction).

Additionally an example use case would be useful, given one would imagine these subsequent transactions go to contracts which expect the results and act accordingly.

Even though reusing `returndata` sounds like a clever mechanism, it seems to be using some encoding similar to the ABI-encoding or one used by precompiles. The EVM does not have such opcodes, and perhaps specific opcodes would be preferred instead.

> An alternative to using return opcodes to propagate  RESULT  would be to append the  RESULT  to the subsequent transaction’s  data  field. Unfortunately, in many cases contracts generated using Solidity will fail to resolve the intended function if additional data is present. Another alternative is introducing new opcodes to expose the result data were not proposed.

I did not fully understand what do you mean Solidity will fail to resolve such transactions? I think the problem is more like that we would be kind of including ABI encoding into the EVM.

---

**matt** (2020-09-08):

> After reading the EIP, I actually thought both  chain_id  and  gas_price  should be outside, and not part of the  inner_tx .

Yep, that makes sense. I think when I originally wrote it, we were thinking of ways to have a “base” tx type so that future tx types were composable, but as you pointed out, what I have now isn’t much good.

> Additionally an example use case would be useful, given one would imagine these subsequent transactions go to contracts which expect the results and act accordingly.

Good idea, I’ll add this!

> Even though reusing  returndata  sounds like a clever mechanism, it seems to be using some encoding similar to the ABI-encoding or one used by precompiles. The EVM does not have such opcodes, and perhaps specific opcodes would be preferred instead.

I may be misunderstanding this, but it seems like you are suggesting that specific opcodes for this EIP would be preferred (e.g. `SUCCESS`, `GASUSED`, …, etc)? I’m not opposed to this, but it would introduce ~5 new opcodes I believe. Are you concerned with defining an ABI-encoding for the return data and populating the return buffer with it? In that case, it should be up to the contract to parse the values appropriately. Do you think this is a weak approach?

> I did not fully understand what do you mean Solidity will fail to resolve such transactions? I think the problem is more like that we would be kind of including ABI encoding into the EVM.

Please correct me if I am wrong, but as I understand it, when a Solidity contract is compiled, it creates a check to ensure that a function is be called with the exact number of parameters it expects. If that isn’t the case, it fails. Therefore, if a tx package contains a tx that *doesn’t* expect to be in a package (say the package starts with an ERC-20 approve, followed by and ERC-20 transfer), the transfer would fail if the return data was appended to the `calldata`, instead of through the return data opcodes.

---

**matt** (2020-10-11):

I’ve made some significant changes to this EIP based on our discussion in the last [breakout room](https://github.com/ethereum/pm/issues/213).

The main changes are:

1. added a “type” field which can be used to allow for future upgrades (maybe even the upper ~4 bits as a flag)
2. an “extra” field which is defined to be empty initially empty, but may be used for future features
3. “max_gas_price” instead of “gas_price” to improve the bundling UX,
4. added a brief discussion on how such a tx can be validated (and monitored) efficiently, under security considerations

full text: https://eips.ethereum.org/EIPS/eip-2733

---

**ekpyron** (2021-03-12):

So while researching the complexity of certain optimizations for Solidity (resp. rather yul) code, an optimization step https://github.com/ethereum/solidity/pull/11093 fell out of it as an example, which actually makes use of the fact that `RETURNDATASIZE` is initially zero at the beginning of a transaction.

The savings aren’t breathtaking, but since it does dial down codesize slightly and will save a few gas here and there, my position was “why not actually do it” - until [@axic](/u/axic) brought up this EIP, which may just be a sufficient reason why not ;-).

However, there may be some existing hand-written minimal proxy contracts out there that already use that `returndatasize` is zero, so potentially this is an issue on chain already (we haven’t actually found it again yet, though).

So yeah, this is definitely something to watch out for and keep in mind. I guess we will keep this optimization step on hold for now at least - if it turns out that this EIP must for example add a flag indicating whether or not to propagate returndata or add special transactions clearing returndata or whatever to ensure backwards compatibility with contracts relying on returndata being empty anyways, then there’s no reason for us to hold back on that optimization. But if this optimization actively breaks progress on improving the EVM, it might just not be worth it.

But it would be nice to have clarity on this eventually…

---

**matt** (2021-03-12):

Interesting, thanks for that information [@ekpyron](/u/ekpyron). I will probably withdraw this EIP as I’m focusing more on EIP-3074 now. I will keep that optimization in mind in the future though.

