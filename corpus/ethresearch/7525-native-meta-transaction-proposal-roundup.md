---
source: ethresearch
topic_id: 7525
title: Native Meta-Transaction Proposal Roundup
author: matt
date: "2020-06-10"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/native-meta-transaction-proposal-roundup/7525
views: 3330
likes: 10
posts_count: 7
---

# Native Meta-Transaction Proposal Roundup

The concept of meta-transactions was first popularized by Alex Van de Sande in EIP-1077 [[1]](https://github.com/ethereum/EIPS/blob/2d6f114fa27d731c97f2d59ed2772ef6467a9675/EIPS/eip-1077.md) and Austin Griffith with his burner wallet [[2]](https://github.com/austintgriffith/burner-wallet). It has become a staple in high profile projects, such as Reddit’s Community Points [[3]](https://www.reddit.com/community-points/). However, new proposals such as UNGAS [[4]](https://specs.corepaper.org/39-ungas) and Oil [[5]](https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip/7394) threaten to break some of its assumptions.

Relay contracts assume they have the ability to catch reversions in their children, which they do by providing their children a fraction of the total gas so that the call’s result can be processed. Changing the semantics of `CALL` so that it always sends *all* the remaining gas would render this technique useless, since any revert would cascade through entire call stack.

In order to resolve this issue, there will either need to be additional modifications to core protocol or the gas observability proposals will need to properly support meta-transactions. I believe there are two important, but orthogonal attributes that a solution should provide:

1. Atomicity: it should be possible to construct a protocol which allows for transactions to be paid for using assets other than ether without complex interactions transpiring across multiple blocks.
2. Interoperability: contracts should not need to provide special interfaces (e.g. EIP-1271 [6] compliant) to authenticate the sender of a message. In other words, CALLER should return the address of the sender not the relayer.

## Atomicity Solutions

The protocol currently provides atomicity across a single transaction. Atomicity in scenarios where a subcall fails has been achieved using the less-than-best-practice technique described above. If Oil / UNGAS / significant changes in the gas schedule break this functionality, relayers will have to accept the risk that they may pay for a tx without being compensated. Whether or not this is an acceptable risk is being discussed [[7]](https://ethresear.ch/t/meta-transactions-oil-and-karma-megathread/7472/10)).

#### Rich Transactions

> A new reserved address is specified at x, in the range used for precompiles. When a transaction is sent to this address from an externally owned account, the payload of the transaction is treated as EVM bytecode, and executed with the signer of the transaction as the current account.

Pros:

- expressive construction which allows complex scripts to be defined and will open many new use cases
- no modification to transaction object required

Cons:

- if gas becomes completely unobservable, this will not provide atomicity since subcalls will always receive all remaining gas
- large surface area for attacks

#### Native batched transactions

> Allow EOA to execute atomic batch transactions, where only one nonce and one signature would be provided for a given batch of transactions.

Pros:

- simple to reason about

Cons:

- transactions are inherently independent of each other, therefore its unclear how pay for the exact amount of gas spent in a previous tx in the batch
- a new transaction object would be needed or the existing one would need to be extended

#### Account abstraction

Suppose transactions to a reserved address are given a fixed amount of gas and are deemed valid if they execute a new opcode, `PAYGAS`, before running out of gas. All other logic, including how to handle the call data is arbitrary – opening the door for “rich transactions”.

Pros

- allows custom transaction validation functions

Cons

- increases the complexity of the tx pool
- does not provide more value than rich transactions
- does not resolve atomicity for EOAs

#### Transaction-Specifiable Subcall Gas

There are a few mechanisms for achieving this that are enumerated in [[11]](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433), but the high-level goal is to delocalize the gas provided to subcall so that it can be specified by an external source, like a new field in the transaction object.

Pros

- less complex than some alternatives

Cons

- another quirk added to the EVM
- calls which were not susceptible to reentry may become vulnerable [12]
- gas is still observable [13]

#### Expansion of Miner Duties

Suppose miners begin to accept requests to relay certain transactions. If they deem a transaction worth relaying (e.g. it will pay them in some other token), then they include it in the block with a gas price of 0.

Pros

- could be implemented without a hard fork
- builds on existing meta-tx work like EIP-1077 [1]

Cons

- txs paying in esoteric tokens would face increased latency [15]
- the duties of the miner would increase significantly to provide these services [15]
- the relationship is strictly between the signer and the miner, so not all onboarding use cases for dapps would be covered [15]

#### Do Nothing

> So this leads to a philosophical question: why not just implement none of these proposals, keep tweaking gas costs as needed for sustainability as we’ve done before, and just publicly state the social norm that you should never hardcode gas limits into a contract, and all inputs to CALL that are not just “send all gas” should have gas values provided by the transaction?

Pros

- we don’t have to do anything
- hard coding gas limits has already been considered bad practice for awhile

Cons

- gas is still observable
- existing contracts will continue to be broken with repricings
- relayers must take on more risk, since failing txs won’t pay them (referred to as “type-2 breakage” in [7])

–

## Interoperability Solutions

Interoperability for meta-transactions is currently not possible at the protocol level [[17]](https://ethereum-magicians.org/t/eip-callwithsigner-as-a-potential-fix-for-the-msg-sender-problem/4340). While it is orthogonal to atomicity, it is still an important aspect of meta-transactions that deserves a proper solution. It is also possible that there are better synergies between some atomicity solutions and interoperability solutions than others. For those reasons, the related proposals have also been included in this discussion.

#### CallWithSigner

Suppose a new opcode is added to the EVM with the same semantics as `CALL`, except it takes three additional parameters `[v, r, s]` and in the child frame `CALLER` returns the resulting `ecrecover` of that signature on the hash of the call data.

Pros

- straightforward addition to the EVM
- flexible, composable

Cons

- breaks tx pool validity invariant [18]
- signatures are not segregated and therefore it’s unclear how to compress them with a ZKP [19]
- couples EVM execution to account authentication

#### Sponsored Transactions

Suppose the current transaction object is amended to support an additional, optional `sponsor` signature. Transactions with this signature would first verify the sender’s signature + nonce, then it would verify the sponsor’s signature and balance to ensure it has at least `value + gas_price * gas_limit`.

Pros

- relatively minimal change

Cons

- not flexible
- increased tx pool complexity

#### Add PAYGASFROM to Account Abstraction

> Introduce a new opcode PAYGASFROM whose arguments are gasprice, from, and calldata. Once executed, the from account will be called with the calldata to verify that it plans to pay for the execution of the transaction. Upon successful verification, it will update any replay protection mechanisms and then return control to the original entry point to continue execution.

Please see [[10]](https://ethereum-magicians.org/t/implementing-account-abstraction-as-part-of-eth1-x/4020) for more background on account abstraction.

Pros

- provides more utility for account abstraction

Cons

- signatures are not segregated and therefore it’s unclear how to compress them with a ZKP [19]
- not applicable to EOAs

### Links

**
Expand to see all**

[1]: [EIPs/EIPS/eip-1077.md at 2d6f114fa27d731c97f2d59ed2772ef6467a9675 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPS/blob/2d6f114fa27d731c97f2d59ed2772ef6467a9675/EIPS/eip-1077.md)

[2]: [GitHub - austintgriffith/burner-wallet: 🔥👛Burner Wallet to move crypto quickly in a web browser. Sweep to cold storage when you get home. 🏠👨🏻‍🚒](https://github.com/austintgriffith/burner-wallet)

[3]: https://www.reddit.com/community-points/

[4]: https://specs.corepaper.org/39-ungas

[5]: [Oil: adding a second fuel source to the EVM (pre-EIP)](https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip/7394)

[6]: [EIPs/EIPS/eip-1271.md at 2d6f114fa27d731c97f2d59ed2772ef6467a9675 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/2d6f114fa27d731c97f2d59ed2772ef6467a9675/EIPS/eip-1271.md)

[7]: [Meta transactions, Oil, and Karma megathread - #10 by holiman](https://ethresear.ch/t/meta-transactions-oil-and-karma-megathread/7472/10)

[8]: [EIPs/EIPS/EIP-draft-rich-transactions.md at f6a2640f48026fc06b485dc6eaf04074a7927aef · Arachnid/EIPs · GitHub](https://github.com/Arachnid/EIPs/blob/f6a2640f48026fc06b485dc6eaf04074a7927aef/EIPS/EIP-draft-rich-transactions.md)

[9]: [EIP-? Native Batched Transactions - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-native-batched-transactions/4337)

[10]: [Implementing account abstraction as part of eth1.x - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/implementing-account-abstraction-as-part-of-eth1-x/4020))

[11]: [Counter-proposal to oil/karma: per-account gas limits](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433)

[12]: [Counter-proposal to oil/karma: per-account gas limits - #2 by holiman](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433/2)

[13]: [Counter-proposal to oil/karma: per-account gas limits - #4 by holiman](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433/4)

[14]: [Meta transactions, Oil, and Karma megathread - #23 by 3esmit](https://ethresear.ch/t/meta-transactions-oil-and-karma-megathread/7472/23)

[15]: [Meta transactions, Oil, and Karma megathread - #24 by matt](https://ethresear.ch/t/meta-transactions-oil-and-karma-megathread/7472/24)

[16]: [Counter-proposal to oil/karma: per-account gas limits - #12 by vbuterin](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433/12)

[17]: [EIP ? - CallWithSigner as a potential fix for the msg.sender problem - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-callwithsigner-as-a-potential-fix-for-the-msg-sender-problem/4340)

[18]: [EIP ? - CallWithSigner as a potential fix for the msg.sender problem - #2 by matt - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-callwithsigner-as-a-potential-fix-for-the-msg-sender-problem/4340/2)

[19]: [EIP ? - CallWithSigner as a potential fix for the msg.sender problem - #3 by sergio_lerner - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-callwithsigner-as-a-potential-fix-for-the-msg-sender-problem/4340/3)

[20]: [EIP-2711: Sponsored, expiring and batch transactions.](https://eips.ethereum.org/EIPS/eip-2711)

[21]: [Meta Transactions x Account Abstraction - HackMD](https://hackmd.io/@matt/S1Jg85588#PAYGASFROM-opcode)

## Replies

**3esmit** (2020-06-15):

Thanks for putting this up.

I would like to defend the EIP-2473 (Gas Abstraction through Expansion of Miner Duties):

---

---

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> #### Expansion of Miner Duties
>
>
>
> Pros
>
>
> could be implemented without a hard fork
> builds on existing meta-tx work like EIP-1077 [1]
>
>
> Cons
>
>
> txs paying in esoteric tokens would face increased latency [15]
> the duties of the miner would increase significantly to provide these services [15]
> the relationship is strictly between the signer and the miner, so not all onboarding use cases for dapps would be covered [15]

---

---

> Cons: txs paying in esoteric tokens would face increased latency

**Can be worked around:**

Miners could automatically monitor several DEXes to find good trade deals with esoteric tokens, and include the DEX trade to ether in the last transaction of the block, and **only seal the block if the new block renders the state where they have the ETH they want.** This can be done whenever there is some “free gas” in the block to fill this DEX trade transaction.

*This is not necessary for well established tokens, such as Wrapped ETH (guaranteed 1-1 ETH rate) and tokens that don’t vary a lot in the ETH rate, as benevolent miners would prefer to accumulate them and exchange them in big trades to save gas (which is “free” for them but have a network cost)*

---

> Cons: the duties of the miner would increase significantly to provide these services

Agreed, however :

- This can also increase the earnings of block validators.
- This can also increase the value of ETH as the ecossystem becomes more versatile, and ETH still used as base market. (miners usually change ERC20 to ETH after the transaction is done)
- This is optional free market, miners would still be able as they currently, but can opt-in to accept tokens with well established ETH value, and the exchange for ETH can be automated with DEX.
- This process can be standardized (possibly by other ERCs), but essentially ERC20 gas market would be more expansive than ETH market, so would be rational for users exchanging some ETH to get faster transaction timing and cheaper gas rates.
- Is in the best interest of miners to accept good deeds for a gasPrice, even if it means including a gasPrice 0 transaction, so I wouldn’t be surprised if a miner build this closed source and have exclusivity in ERC20 gas market, where they can rule the price.

---

> Cons: so not all onboarding use cases for dapps would be covered

**Can be worked around:**

- it’s possible to relay in top of another contract which pays the meta-transaction in ETH (gasToken set to zero) and passes the user signature to the identity user account contract. (Meta-meta-transaction with innermost gasPrice and gasToken set to zero)

---

---

---

---

# Additional considerations:

- This is the smallest change to network possible to provide this feature, which is opt-in by miners.
- Can co-exist with future changes to EVM, with remarks to EIP-2489*

### *EIP-2428 - UNGAS EVM EIP:

- as it is now, would automatically invalidates any previous meta-transaction (it would fail at SafeMath.mul() due int overflow and in gasLimit). However, if the EIP-2489 uses default value of “GAS” OPCODE to one, gasPrice becomes a fixedFee variable, and gasLimits gets kicked off.
- meta transactions could use delegatecall to a library-contract that contains gas payment logic, which could have its bytecode upgraded together with EIP-2489.
- EIP-1077 could be designed from beginning without gasLimit and gasPrice*gasUsed, and start off using a plain totalFee which is paid regardless of cost of transaction, but only when succeeded.
- It is very improbable that EIP-2428 ever gets approved as it changes fundamental things solidity used for in many livenet contracts, and being a very complex/risky upgrade of EVM.

---

**stonecoldpat** (2020-06-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> #### CallWithSigner
>
>
>
> Suppose a new opcode is added to the EVM with the same semantics as CALL , except it takes three additional parameters [v, r, s] and in the child frame CALLER returns the resulting ecrecover of that signature on the hash of the call data.
>
>
> Pros
>
>
> straightforward addition to the EVM
> flexible, composable
>
>
> Cons
>
>
> breaks tx pool validity invariant [18]
> signatures are not segregated and therefore it’s unclear how to compress them with a ZKP [19]
> couples EVM execution to account authentication

I forgot to reply on the ethereum magicians post. (I’ll do that after this one).

If callWithSigner was to re-use the account system nonce, then yes it would break the tx pool validity invariant (e.g. you need to see if the nonce has been re-used). I think that is a good reason to avoid that approach (this was proposed as an alternative approach).

The main approach in the EIP forcallWithSigner is to let the opcode deal with its own replay protection (e.g. it would have storage) and it would be independent of the account system replay protection.

Pro:

- We can use MultiNonce replay protection that lets the user send up to N concurrent transactions abd it does not matter what order they are accepted in. We already use it here too

Con:

- First precompile/opcode that maintains storage (e.g. a mapping of H(address | nonce1) → nonce2)
- We may no longer have access to ETH (to avoid breaking the tx pool). But that should be OK since there is WETH.

I’ll update the EIP writeup to make this more clear!

Also thanks for summarising everything! I didn’t know about some of these proposals so will check it out.

---

**stonecoldpat** (2020-06-16):

I just had a thought.

Most third party relayers tend to send the transaction via a Relay.sol contract before executing the users transaction. The reason for this in any.sender is 1) record a log of job and 2) refund the relaying key. For the GSN, it is to 1) swap the ERC20 token payment into ETH

The sponsored signature approach might not work with the above… since you cant send the transaction via a relay contract to refund the relaying key. Long term it doesn’t impact any.sender, but it will impact relayers that rely on payment at the time of transacting.

So you need sponsored signature + batch transaction, or the on-chain opcode approach.

---

**matt** (2020-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/3esmit/48/503_2.png) 3esmit:

> I would like to defend the EIP-2473 (Gas Abstraction through Expansion of Miner Duties):

Thanks for your response [@3esmit](/u/3esmit). I hope other authors will take the time to defend their proposals – I believe will lead us to the best solution.

![](https://ethresear.ch/user_avatar/ethresear.ch/3esmit/48/503_2.png) 3esmit:

> This is optional free market, miners would still be able as they currently, but can opt-in to accept tokens with well established ETH value, and the exchange for ETH can be automated with DEX.

The problem with it being optional is that depending on the number of miners participating, latency could be high. Even for popular tokens.

![](https://ethresear.ch/user_avatar/ethresear.ch/3esmit/48/503_2.png) 3esmit:

> it’s possible to relay on top of another contract which pays the meta-transaction in ETH (gasToken set to zero) and passes the user signature to the identity user account contract. (Meta-meta-transaction with innermost gasPrice and gasToken set to zero)

This is already possible today though and I would argue a very important aspect of meta-transactions. If we’re going to put a lot of work into a solution, I believe it needs to address this.

![](https://ethresear.ch/user_avatar/ethresear.ch/3esmit/48/503_2.png) 3esmit:

> It is very improbable that EIP-2428 ever gets approved as it changes fundamental things solidity used for in many livenet contracts, and being a very complex/risky upgrade of EVM.

This may be true, but there is a growing desire to improve the metering system in the EVM. This is especially true w.r.t. eth1.x and accounting for variable witness expenses. So it’s likely we see a significant change in the next few years, even if it isn’t UNGAS.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> The main approach in the EIP forcallWithSigner is to let the opcode deal with its own replay protection (e.g. it would have storage) and it would be independent of the account system replay protection.

You’re right, that would definitely resolve the mempool issue. My concern is that adding an additional replay protection system as part of this opcode seems hacky. The opcode is catered to a very niche application – unless there are strong advantages of it over sponsored transactions, I can’t see how the additional complexity will be warranted.

---

**matt** (2020-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> So you need sponsored signature + batch transaction, or the on-chain opcode approach.

Yep, absolutely agree. We need a solution for both atomicity and interoperability. Unfortunately, the on-chain opcode approach won’t solve the atomicity portion of the equation if guarded subcalls become impossible due to UNGAS / Oil.

---

**3esmit** (2020-06-17):

Hey. thanks a lot for the feedback.

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> The problem with it being optional is that depending on the number of miners participating, latency could be high. Even for popular tokens.

I agree this can be a problem, but only if the market would not be interested - as demand for token gas relay in specific tokens rises, the availability of this secondary gas market would rise.

But how any *good* solution would force the availability of a token gas relay? I don’t think that is possible, in free market, to force the price/availability of any product/service.

I see that the gas market can be improved, such as the tooling allowing for more rational choices, as being discussed in [EIP-1559](https://github.com/ethereum/EIPs/blob/392f36fc0e4f1df1bbd76edcc631e3a49a521ecc/EIPS/eip-1559.md). I just don’t see how *any other* solution can also ensure the availability of token gas markets.

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> This is already possible today though and I would argue a very important aspect of meta-transactions. If we’re going to put a lot of work into a solution, I believe it needs to address this.

Yes, and this EIP would integrate this solution and make free transactions like they are today, but easier as you won’t need to run any service to do that, the miners would do it, and you would be able to pay the gas for your application using meta-meta-transactions. The only clunky thing is the meta-meta aspect, however it’s not a problem, as the inner-most transaction uses zero for everything related to gas and totally ignore the gas refund.

I agree we can include that specification in EIP-1077, so it covers all use-cases we identify. That’s already my plan, that’s why I simplified the interface in the recent versions to `executeGasRelay(bytes calldata _execData, uint256 _gasPrice, uint256 _gasLimit, address _gasToken, address _gasRelayer, bytes calldata _proof) external;` where execData can be anything the “called contract” can execute, and proof whatever proves this execution can be done.  Also, the standard specifies that when gasRelayer is zero the payment go to `block.coinbase`, as a preparation to EIP-2473 soft-fork, and to work as a `COINBASE_CALL` (EIP-2474).

