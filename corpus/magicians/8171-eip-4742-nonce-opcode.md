---
source: magicians
topic_id: 8171
title: "EIP-4742: NONCE opcode"
author: 0xfoobar
date: "2022-02-01"
category: EIPs > EIPs core
tags: [evm, opcodes, core-eips]
url: https://ethereum-magicians.org/t/eip-4742-nonce-opcode/8171
views: 2769
likes: 9
posts_count: 16
---

# EIP-4742: NONCE opcode

Discussion thread for [EIP-4742: NONCE opcode by 0xfoobar · Pull Request #4742 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4742)

## Abstract

We propose an additional EVM opcode, `NONCE` (0x47), which could provide novel protection against sybil attacks and expand the smart contract design space. This would return `0` for an unused externally-owned address (EOA), `0` for a smart contract address, and, for example, `2` for an EOA which has sent 3 transactions. The account.nonce opcode would exactly track the nonce of the last transaction originating from that address.

## Motivation

NFT contracts commonly use checks on `msg.sender` to limit sybil attacks. However, this is easily circumvented by spinning up new addresses, or even nesting address creation within a smart contract. Letting smart contracts check `NONCE` would add additional costs to this, serving as a “proof of history”. While not bulletproof (as msg.sender is not), it opens up the design space to creative uses.

## Specification

A new opcode, `NONCE`, is introduced, with number `0x47`. The `NONCE` opcode takes one argument from the stack, and pushes to the stack the nonce corresponding to that address.

The gas cost of the `NONCE` is 200.

## Rationale

The EVM makes several global variables available, examples include `block.timestamp`, `block.number`, `block.difficulty`, `msg.sender`, and `gasleft()`. It also provides several context-dependent opcodes, such as `EXTCODESIZE`, `BASEFEE`, and `BALANCE` Smart contracts can leverage these info for novel techniques, such as staking pool emissions, limiting flashloan attacks, or NFTs that embed blockchain state into their mint result.

It is useful to gather information about interacting addresses. NFT minting is an immediate usecase, and it follows that as much information about the underlying blockchain state should be made available to smart contracts.

## Backwards Compatibility

There are no backwards compatibility concerns.

## Test Cases

1. The NONCE of an address with no transactions is 0.
2. The NONCE of an externally owned address (EOA) with one originating transaction is 1.
3. The NONCE of a smart contract, deployed after EIP 161, that has not deployed any other smart contracts is 1.
4. The NONCE of a smart contract, deployed before EIP 161, that has not deployed any other smart contracts is 0.
5. The NONCE of a smart contract, deployed after EIP 161, that has deployed one other smart contract is 2.
6. The NONCE of a smart contract, deployed before EIP 161, that has deployed one other smart contract is 1.

## Implementation

Not provided yet, would need to be integrated into Ethereum clients as this is an EVM modification. However, clients already check the account nonce on each transaction to ensure validity, so exposing this data as an opcode should not add significant processing or development load.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**SamWilsn** (2022-02-01):

It seems like the benefit of using nonce over just burning ETH is that legitimate users likely already have enough transactions on their wallets, so it’s cheap for them; while sockpuppet wallets are empty and would need to spend an additional `~21,000 * N` gas to prove their uniqueness?

---

**0xfoobar** (2022-02-02):

Exactly! Querying an address’ balance seems isomorphic to querying their nonce, it’s already checked in every transaction for signature validity, and opens an interesting smart contract design space for making sybil attacks more expensive.

---

**SamWilsn** (2022-02-02):

I think the only other suggestion I have on the technical side is that the gas cost should mirror `0x31`: if the account is cold it should cost 2600, otherwise 100.

---

**axic** (2022-02-08):

Since this is reading the nonce of any account, it should be called `EXTNONCE` to be in line with the other instructions.

Can you please explain a use case this is needed for? Having a described use case helps in convincing client implementers.

---

**axic** (2022-02-08):

As an alternative, [EIP-2938](https://eips.ethereum.org/EIPS/eip-2938#nonce-0x48-opcode) proposed an opcode for querying the current account’s nonce:

> #### NONCE (0x48) Opcode
>
>
>
> A new opcode NONCE (0x48) is introduced, with gas cost G_base, which pushes the nonce of the callee onto the stack.

---

**jochem-brouwer** (2022-02-09):

This is probably going to lead to some problems in some situations, as clients might internally differ when the nonce is internally updated when running certain transactions.

1. When an account sends a transaction, is the account nonce increased before running the transaction or after? (So, when a fresh account sends a Tx to a contract which stores NONCE, should 0 or 1 be stored? After the transaction completes it is clear that the nonce is 1, but during the transaction…?)
2. Same question, but now when a contract CREATEs or CREATE2s a new contract. The created contract stores the nonces of the contract which initiated the creation. When is the nonce updated, before or after creating the contract?

---

**MicahZoltu** (2022-02-10):

My concern with the motivation here is that it essentially is encouraging spamming the network in order to gain sybil access to things.  While legitimate users won’t have to spam the network, this sort of pattern encourages users to spread their activities across many accounts just so they can have multiple primed accounts for access to “one per person” things like airdrops, sales, etc.  Instead of using one account for everything, a clever user will now use multiple accounts to achieve the same goal.  We already see this behavior from users in response to per-account airdrops, where users will intentionally spread their usage pattern out across many accounts just so they get more “shots on goal” for future airdrops.

The other thing is that exposing nonce could come back to bite us in the future when we try to move to contract wallets.  Not all account access patterns will require a nonce, and not all of those that do will require a monotonically increasing nonce.  By exposing `NONCE` to end-users today, we are increasing the lock-in for the nonce-based pattern of access.

---

**abcoathup** (2022-02-11):

[@0xfoobar](/u/0xfoobar) can you update the title to match the EIP number: EIP4742

---

**0xfoobar** (2022-02-12):

I can’t edit the original post any more, could you grant me added permissions so I can fix it?

---

**abcoathup** (2022-02-13):

[@jpitts](/u/jpitts) can you update the title to EIP4742

---

**zemse** (2022-03-28):

A use case of `NONCE` opcode (nonce of current account/contract) can be useful to calculate CREATE address before the contract deploys the contract. As an example: let’s consider factory contract F and child contracts A and B. The factory contract F wants to pass addresses of B in A’s constructor and address of A in B’s constructor, this is to have the sibling addresses as immutables instead of storage. Currently, that’s not feasible since we just don’t get the F’s nonce in F’s execution context.

---

**3commascapital** (2024-03-04):

Another use case of this opcode would be to nullify signatures held by other individuals / for other contracts. If a signature that holds the current nonce is held by 3rd parties and the contracts that those signatures would be verified in (such as permit or a swap signature) then one could nullify all outstanding messages by simply doing a self transfer. I see this as potentially useful for protecting wallets that initiate gas-less operations.

[@MicahZoltu](/u/micahzoltu) I do not entirely understand how this would encourage people to use more addresses and may do exactly the opposite. Is there a particular situation that comes to mind? Airdrops that do things other than interaction based drops are deluding themselves. Address based is just a bucket for collecting points paid for interactions. Spreading out qualifying airdrop transactions only causes a headache for recipients. Just my 2c.

---

**MicahZoltu** (2024-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3commascapital/48/16215_2.png) 3commascapital:

> @MicahZoltu I do not entirely understand how this would encourage people to use more addresses and may do exactly the opposite. Is there a particular situation that comes to mind? Airdrops that do things other than interaction based drops are deluding themselves. Address based is just a bucket for collecting points paid for interactions. Spreading out qualifying airdrop transactions only causes a headache for recipients. Just my 2c.

My argument was against the premise of the motivation.  Contracts should *NOT* be trying to implement Sybil resistance by only allowing “one per msg.sender” nor “one per msg.sender with nonce > x”.  Both of these strategies encourage users creating multiple accounts, and the latter encourages not only creating multiple accounts but also spamming transactions to them.

---

**0xTraub** (2024-03-04):

How would this work in the case of AA-wallets specifically those with EIP-4337, where the msg.sender may be a smart contract which hasn’t deployed any contracts to increment its own nonce? Would a smart-wallet have to deploy contracts which may be useless to be able to pass this sybil check? This also can be expensive and lead to unnecessary state growth to deploy contracts with no purpose or users.

---

**3commascapital** (2024-03-05):

I think that airdrops as the main use case is the wrong conclusion in general. There are many other use cases. I personally, would be fine with only an equality check. I would prefer direct exposure to it as a number, but only querying it’s value and getting a true/false as a result would be fine for a variety of other use cases, especially competitions or limit orders.

