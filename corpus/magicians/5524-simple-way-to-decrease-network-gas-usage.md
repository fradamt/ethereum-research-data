---
source: magicians
topic_id: 5524
title: Simple Way to Decrease Network Gas Usage
author: junderw
date: "2021-03-10"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/simple-way-to-decrease-network-gas-usage/5524
views: 1909
likes: 5
posts_count: 8
---

# Simple Way to Decrease Network Gas Usage

Sort the top gas spenders of the past 24 hours and what do you see? Centralized Exchanges as far as the eye can see. (Also, it is very common for exchanges to have multiple accounts splitting responsibilities like forwarding funds from deposit addresses etc.)

[![スクリーンショット_2021-03-10_14-29-18](https://ethereum-magicians.org/uploads/default/optimized/2X/2/2866fe4ade4ec90b50136afa6a0cf20814b296a1_2_690x463.png)スクリーンショット_2021-03-10_14-29-181375×924 117 KB](https://ethereum-magicians.org/uploads/default/2866fe4ade4ec90b50136afa6a0cf20814b296a1)

Even if you sort by the largest gas guzzler contracts, what do you see (besides Uniswap)? ERC-20 stable coins. Who uses ERC-20 stable coins the most (by direct call, not internal call)? Centralized Exchanges.

[![スクリーンショット_2021-03-10_14-32-41](https://ethereum-magicians.org/uploads/default/optimized/2X/9/915f91102881edac3b7d68cf56d96ab04a191502_2_690x464.png)スクリーンショット_2021-03-10_14-32-411376×926 135 KB](https://ethereum-magicians.org/uploads/default/915f91102881edac3b7d68cf56d96ab04a191502)

What can we do that is easy and will decrease the footprint of CEX on Ethereum?

**Answer**

Add a memo field in the transaction. This can be added during the London hard fork.

It can be inserted after the data field, and each byte added to memo will cost the same as calldata bytes (iirc. 16 gas for non-zero byte, 4 gas for zero byte)

This memo should not be accessible from EVM.

***Why not just use the data field?***

While txes to EOA accounts would be fine, ERC20 transactions would need to append the memo to the end of the transfer calldata. This might be fine now, but Solidity dev has said that in the future Solidity might check upper bounds on calldata. Also there is no guarantee that contracts don’t revert on extra data.

***Why make memo invisible to EVM?***

This is to prevent contracts from preventing memos.

***Why allow useless data?***

Set a max size for memo if that worries you. But tbh as long as there is a gas cost for bytes it shouldn’t be a problem.

***How does this lower gas usage?***

Currently, most exchanges do the following:

1. Deposit account is EOA hot wallet. User sends to deposit EOA (21000 gas (40~60k for ERC20)) X deposit count
2. Deposit sends to central single wallet (hot or cold). (21000 gas (40~60k for ERC20)) X deposit count

This essentially doubles the gas usage that is actually needed.

If there was a memo field, there could be an address format that specifies the memo field to be an identifier for each user. Or (like XRP and XLM) we could just tell them to manually copy paste the memo data.

Then each deposit would all be sent to the same account, no need to double the gas usage by creating a new tx.

Related threads I have created in the past.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/junderw/48/2808_2.png)

      [EIP: Add memo to Transaction (Requires hard fork)](https://ethereum-magicians.org/t/eip-add-memo-to-transaction-requires-hard-fork/4982) [EIPs](/c/eips/5)




> This is related to EIP-2876
> The following idea is an alternative to the above EIP for deposit systems (centralized exchanges and merchants being major use cases) to differentiate funds moving toward a single account.
> By adding a memo space (it can be small and very limited, 8 bytes etc.) all deposits can be sent to one single cold wallet account, and the deposit watching system could just check the memo for an identifier.
> This would allow for apps like BTCPay to easily support ETH deposits, E…



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/junderw/48/2808_2.png)

      [EIP-2876: Deposit contract and address standard](https://ethereum-magicians.org/t/eip-2876-deposit-contract-and-address-standard/4504) [EIPs](/c/eips/5)




> This ERC defines a simple contract interface for managing deposits. It also defines a new address format that encodes the extra data passed into the interface’s main deposit function.
> EIP is here: https://eips.ethereum.org/EIPS/eip-2876
> Sample Implementation is linked in the EIP.
> One major question brought up: Why not EIP-681? It also supports ERC-20 which many exchanges need.
> I mention why no ERC-20 support is not an issue in the EIP (separation of logic and keys) and as for why not EIP-681…

EIP2876 is “how do we do this without a hard fork? (assuming memo feature fails)”

I think we can use the address format from EIP2876 as a format that exchanges can use with each other.

I will write up an EIP about this hard fork proposal, and modify EIP2876 to focus on the address format, and switch between the Deposit interface or the memo field depending on whether the hard fork change passes.

I like the discussions on other scaling methods, but there are some low hanging fruit here that can really help with congestion.

## Replies

**junderw** (2021-03-10):

[@poojaranjan](/u/poojaranjan) and myself discussed this issue along with the EIP I have proposed.

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/b/be898d15eb6985f13285c9c543bfc1ff5ad592f8.jpeg)](https://www.youtube.com/watch?v=ha8uOWNT6sg)

---

**holiman** (2021-03-10):

Several years ago, we (IIRC in particular [@Arachnid](/u/arachnid)) tried to convince centalized exchanges to use the calldata. And make contracts, essentially (pseudocode):

```auto
function deposit(uid) payable{
  assert( checksum_ok(uid))
  emit Paid( uid, msg.value)
}
```

So exchanges would put up a contract, which they could fetch money from whenever they saw fit. They were concerned that users would bungle the data, but since the data can be verified in the contract, I seems like that would be pretty solvable.

But essentially, their stance was “If a user can do it wrong, they will. And the user deposit may thus revert, and the user won’t succeed in making the deposit. We prefer to create N thousand EOA accounts for deposits, rather than adding any extra complexity to the deposit UX”.

So that’s why things are like they are. Based on that, which is tragic and IMO very wrong, I don’t see how they (CEX:es) would be amenable to the `memo` approach, since the memo approach is more or less the same idea, however:

- If the memo data is bungled, there is no way to revert the transaction. Instead, people would have to contact the CEX and say “Hey I sent over XX ether, but got the memo wrong, help?”. And they’d have a huge problem sorting it all out.

---

**holiman** (2021-03-10):

Other schemes are possible too. For example, you could make users just send to the same place, *without* any extra data at all.

If the user can then (off-chain) provide one of these things:

- A signed tx which is unexecutable (e.g. nonce 0), with the data 0xXXX... is owned by , or
- A signed message, saying Transaction XXX from YYY was sent by .

So there definitely *are* ways of solving all these problems, but I have the feeling that none of these options have been seriously investigated (at least not to my knowledge) by the large CEX:es, due to their conviction that ease of deposit trumps *everything* else.

---

**junderw** (2021-03-10):

This is exactly what EIP-2876 does. It also defines a new address format solely for use with these types of interfaces.

However, I think that it would be better to have the address format from EIP-2876 and instead of defining it to mean “use the Deposit function signature from EIP-2876” instead define it to mean “place the 8 byte id in the memo” (if the memo feature were added)

If there was a simple address format (emphasis on simple) where it was trivial for exchanges to implement the encoding and decoding of them, and they contained an identifier. The problem then becomes “where should the identifier go?”

Best case is “a new memo field added via hardfork” and the compromise is the current EIP-2876 contract interface.

If you have time, please watch the PEEP an EIP, we discuss the issue in depth.

---

**junderw** (2021-03-10):

> ease of deposit trumps everything else.

This is also a big hurdle. Which I think can be overcome if the simple account+id address format were adopted by both wallets and other exchanges.

It is a chicken and egg problem, BUT I think if we can standardize it, the network fee savings for CEXes will be significant. We spent millions every year in ETH fees. That could be half.

---

**adietrichs** (2021-03-11):

To point out one other potentially relevant EIP here: [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074), currently being considered for inclusion in London, would allow CEXes to significantly reduce the gas footprint of collecting ERC-20 deposits even under their current one-address-per-user-and-asset design. Basically, CEXes could collect multiple deposits within one single transaction, where each collection would only have the static gas cost overhead of a signature check and a call (~4000 gas).

A solution like e.g. the discussed memo field, where funds can be immediately sent to the correct final destination, would of course be even more advantageous for this specific issue though.

---

**junderw** (2021-03-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adietrichs/48/14646_2.png) adietrichs:

> Basically, CEXes could collect multiple deposits within one single transaction, where each collection would only have the static gas cost overhead of a signature check and a call (~4000 gas).

While this proposal sounds great and has many use cases, especially for DeFi, it should be noted that a lot of CEX platforms tend to limit the scope of their deposit/withdraw systems to use EOA accounts only (ie. every operation is an external call) because the cost of developing, testing, and auditing a solidity contract is magnitudes higher than an application that just uses some JavaScript with web3 to do some external contract calls to a token contract. (IERC20.transfer etc.)

On a slightly related note, this is also why a lot of CEXes don’t detect ETH deposits from internal contract calls. All the ethereum stack exchange solutions are “build a contract and emit events, then watch those events…” which then leads to “nope, parse every tx in every block and match the `to` field to our giant list of EOA deposit accounts.” because no one wants to touch smart contract development because of the high maintenance cost (not to mention lack of skilled engineers who know about EVM security, let alone “can code solidity”.)

The result of this is that CEX systems are highly inefficient, which doesn’t matter much to them (us) because we take large fees for withdrawals anyways. So we essentially pass the inefficiency off to the customers, and the ETH network as a whole suffers for it.

I do like EIP-3074, though, and it sounds like a great idea for what its trying to accomplish.

