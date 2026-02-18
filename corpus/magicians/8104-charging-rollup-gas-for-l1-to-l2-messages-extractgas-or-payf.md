---
source: magicians
topic_id: 8104
title: "Charging rollup gas for L1 to L2 messages: EXTRACTGAS or PAYFROMORIGIN"
author: yahgwai
date: "2022-01-25"
category: EIPs
tags: [evm, gas, layer-2, transactions, rollups]
url: https://ethereum-magicians.org/t/charging-rollup-gas-for-l1-to-l2-messages-extractgas-or-payfromorigin/8104
views: 2657
likes: 7
posts_count: 13
---

# Charging rollup gas for L1 to L2 messages: EXTRACTGAS or PAYFROMORIGIN

When contracts send messages from Ethereum to a rollup they need to pay for the execution of the message as a tx on the rollup. Arbitrum and Optimism have different approaches to this.

### Arbitrum

Makes the message sending [function on their bridge payable](https://github.com/OffchainLabs/arbitrum/blob/master/packages/arb-bridge-eth/contracts/bridge/Inbox.sol#L280), and expects the caller to send enough value to cover the cost of the L2 execution. The downside of this is that many existing contracts don’t provide the ability to make payable calls, and even if they did the value would potentially need to be passed from the user through all contracts in the path before reaching the payable function.

An example of this is the ERC721 standard. ERC721s provide a _checkOnERC721Received function that will be called after transferring to a contract. This could be used to transfer an ERC721 token to a contract and check that it has been received. However rollups that require a payable deposit function cant use this method, since _checkOnERC721Received doesn’t send any value with it. Instead, in order for a user to send value with the deposit they must split the deposit into 2 separate transactions:

1. Approve a gateway contract to transfer the NFT
2. Execute a transferfrom and send value to the rollup to pay for the L2 execution

### Optimism

To avoid enforcing a payable interface Optimism dont receive any funds for L2 execution of the messages. Instead they [burn gas](https://github.com/ethereum-optimism/optimism/blob/develop/packages/contracts/contracts/L1/rollup/CanonicalTransactionChain.sol#L239) proportional to the L2 tx gas limit to prevent callers from being able to DOS the rollup nodes into processing arbitrary amounts of L2 gas for free. The downside of this is that the burning the gas takes up L1 block space, which is a valuable resource.

Below are two alternative proposals for new Ethereum opcodes that could accept funds without forcing changes on the public interfaces of calling contracts.

### EXTRACTGAS: Convert gas to value

A new opcode (EXTRACTGAS) that extracts gas from the gas stipend of a transaction, converts it to value and sends it to the current address. The opcode increases gasUsed by gasExtracted and sends gasExtracted*tx.gasprice to the current address. Additionally when calculating the total amount of gas used in a block the total amount of gas extracted would need be subtracted from the gas used to ensure that the block gas limit wasn’t effected: blockGasUsed - blockGasExtracted < blockGasLimit.

### PAYFROMORIGIN: Take value from the tx rather than receiving it in a CALL

A new transaction type that includes an additional value field called originValue, and a new opcode (PAYFROMORIGIN) that can take some funds from the originValue field and sends it to the currently executing contract. The originValue field isn’t strictly necessary, but may be nice in providing some protection to the transaction sender to prevent a contract from taking arbitrary amounts of value.

*Edit: This problem could also be solved with [3074](https://eips.ethereum.org/EIPS/eip-3074). A user could use a batch-capable invoker to first make the relevant contract call (which would internally call the bridge) without supplying a value, then call into the bridge contract after and pay for the previously deposited message. However this does has the overhead of having to make two extra calls.*

## Replies

**SamWilsn** (2022-01-26):

With 3074, could the user call directly into the bridge with value and a signed authorization, then the bridge `authcall`s into the relevant contract?

---

**yahgwai** (2022-01-26):

Nice! Yep, that would cut using 3074 down to only one extra call, and in some special cases maybe no extra calls.

---

**DB_1** (2022-01-29):

Won’t EXTRACTGAS re-enable generating revenue from transactions (without sending funds)?

---

**microbecode** (2022-01-29):

Do I understand right that EXTRACTGAS would essentially bring back gastokens? Didn’t we just fight to get them gone ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

---

**yahgwai** (2022-01-30):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/f08c70/48.png) DB_1:

> Won’t EXTRACTGAS re-enable generating revenue from transactions (without sending funds)?

I’m not sure what you mean about generating revenue without sending funds. EXTRACTGAS takes gas (at a rate of tx.gasPrice) from the transaction’s gas which must be paid for in the usual way.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/microbecode/48/15066_2.png) microbecode:

> Do I understand right that EXTRACTGAS would essentially bring back gastokens? Didn’t we just fight to get them gone

Could you explain further? I dont see how this could be used to enable gas tokens. Gas tokens allowed for the storage of gas to be used later via the (now removed) refund. EXTRACTGAS takes gas from the current transaction and pays it to the contract, always reducing the current gas limit. It cant be used to pay for future transactions at future prices.

---

**DB_1** (2022-01-30):

It allows a third party to generate revenue from a crafted transaction via gas. It goes back to a theoretical (I think) attack vector, where one persuades a bot to make a transaction. It may be reverted in case of a loss, but gas value could have been extracted in the past. This may re-enable it. How will it be handled in a reversion?

---

**yahgwai** (2022-01-31):

EXTRACTGAS allows a contract to receive funds from the supplied gas. Contracts can already receive funds from msg.value. Gas must be paid for upfront by the user, in the same way as value. All that EXTRACTGAS does is allow you to receive funds from a different source that already been paid for, rather than the msg.value - I dont see what attack vector this opens up.

A reverted transaction shouldn’t change any state on the chain except the user’s. So the contract wouldn’t receive the funds from EXTRACTGAS in a reversion. Instead the funds could either be sent back to the tx.origin, or be sent to the block producer like the rest of the gas used. I’d recommend they get sent back to the origin, since the block producer hasn’t done the work proportional to the gas extracted in EXTRACTGAS.

---

**microbecode** (2022-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yahgwai/48/4793_2.png) yahgwai:

> Could you explain further? I dont see how this could be used to enable gas tokens. Gas tokens allowed for the storage of gas to be used later via the (now removed) refund. EXTRACTGAS takes gas from the current transaction and pays it to the contract, always reducing the current gas limit. It cant be used to pay for future transactions at future prices.

Well this allows the storage of Ether (extracted from gas), but you’re correct that it’s not quite the same as gastokens.

I think this is an interesting approach, but would need to be thought ot thoroughly for possible attack vectors / abuses. It’s easy to imagine how some contract extracts some fee from the gas without the user knowing about it. With msg.value the sent value is explicit, but if taken from gas, the extracted value can be sort of hidden.

---

**dror** (2022-02-02):

EXTRACTGAS seems a little dangerous:

In the current gas model, a user assigns “gas” to the transaction for execution. It trusts the contract it calls to use that gas for execution. The contract might mis-behave and abuse this gas to grief the user - but can’t make a real profit out of it.

Now we open a way for contract to extract value out of this gas-only money. I just can’t wait for the ingenuity of people to extract value out of it.

I can’t help it, but it strongly reminds me of Reality Bites “[Gas to Money](https://www.youtube.com/watch?v=FW78nfBkjM0)”

(For those who can’t remember: a caring father want his daughter to work for living, but gives his daughter a refueling card. She uses it to “service” people at a self-service station, getting cash and paying with her father’s card.)

---

**yoavw** (2022-02-03):

My bet is that the first one will be airdrops that steal people’s eth in their `claim()` function.

Next comes more creative stuff such as contract wallets abusing contracts with callbacks, e.g. [eip-1363](https://eips.ethereum.org/EIPS/eip-1363) tokens.  Whenever you give someone an allowance to `transferFrom` your tokens, they also pay you some eth.

I think gas and value need to be kept separate, so PAYFROMORIGIN seems a bit safer and allows the user to declare an intention.  But even then, the intention declaration is not specific enough since it doesn’t say which contract is allowed to withdraw.  Since it’s used to pay for gas, the specified amount will be higher than what actually gets charged, so I expect some contracts to take advantage if called late in the transaction, and grab the leftovers.

Batching is indeed a possible solution, and could be used right now without waiting for a protocol change.  A contract wallet or an [ERC 4337](https://eips.ethereum.org/EIPS/eip-4337) wallet can (and should) offer a function that performs both calls.

---

**yahgwai** (2022-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> EXTRACTGAS seems a little dangerous:
> In the current gas model, a user assigns “gas” to the transaction for execution. It trusts the contract it calls to use that gas for execution. The contract might mis-behave and abuse this gas to grief the user - but can’t make a real profit out of it.
> Now we open a way for contract to extract value out of this gas-only money. I just can’t wait for the ingenuity of people to extract value out of it.

Yeah, I agree that this opens up a new way for contracts to trick users. But I would say that there are already many ways to do that - I could send 0.05 ETH to mint an NFT and the contract simply not mint it but keep the funds, or a staking pool could have a broken withdraw function. The amount of mischief with EXTRACTGAS is at least bounded by the gas limit, and if a contract abuses EXTRACTGAS it would become known in the same as other contracts that trick users. Although I wonder if this could become more of a problem if EXTRACTGAS became used widely and for large amounts instead of small - then gas limits would be high allowing for larger amounts to be stolen before being declared malicious.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Batching is indeed a possible solution, and could be used right now without waiting for a protocol change. A contract wallet or an ERC 4337 wallet can (and should) offer a function that performs both calls.

If all user’s had contract wallets then I agree this wouldn’t be a problem. I don’t know, but I would guess, that the vast majority of users have and will continue to have EOAs.

---

**yoavw** (2022-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yahgwai/48/4793_2.png) yahgwai:

> But I would say that there are already many ways to do that - I could send 0.05 ETH to mint an NFT and the contract simply not mint it but keep the funds, or a staking pool could have a broken withdraw function.

The difference is that users would soon realize that they’re not getting the service (not getting an NFT or not being able to withdraw - although that’s trickier until withdrawals are enabled).

With EXTRACTGAS contracts will be able to provide a service, while the user pays a premium unknowingly.  Something like this - a new dex targeting Uniswap users, so it airdrops tokens to all existing Uniswap projects with a short expiration date to induce FOMO.  Users claim the token, while unknowingly paying for these tokens via EXTRACTGAS.  A token presale disguised as an airdrop. Users will see that they’re getting the claimed token, not realizing that they paid for them.

The way to protect the user against such scams will probably be through EOA wallet software like Metamask, which should simulate transactions and clearly warn the user that this transaction is going to pay X to contract Y.  With proper UI it could work.  To help Metamask do that, maybe we should add an `extractedGas` field to the return value of `eth_call` or add a new `eth_estimateGasWithExtraction` call which tells the caller, not just how much gas is used, but also how much gas is extracted by contracts using EXTRACTGAS.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yahgwai/48/4793_2.png) yahgwai:

> If all user’s had contract wallets then I agree this wouldn’t be a problem. I don’t know, but I would guess, that the vast majority of users have and will continue to have EOAs.

The ultimate purpose of account abstraction is to replace EOAs.  ERC 4337 is just the beginning and requires creating a contract wallet, but the endgame is that at some point (in a distant future) there will be [a hard fork that replaces all EOAs](https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538/2) with a proxy contract that points at a precompile wallet emulating an EOA.  Users will then be able to upgrade their proxy in-place to point to more sophisticated wallets.

In the short term I see the value of such opcodes, but in the long term it might fall in the “[enshrining-EOAs-even-further](https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538/1)” category.

