---
source: magicians
topic_id: 12095
title: "EIP: ETH as ERC20 Precompile"
author: Philogy
date: "2022-12-11"
category: EIPs
tags: [evm, precompile]
url: https://ethereum-magicians.org/t/eip-eth-as-erc20-precompile/12095
views: 1196
likes: 0
posts_count: 4
---

# EIP: ETH as ERC20 Precompile

## Simple Summary

Precompile allowing ETH to directly be treated as and transferred as an ERC20 token, without intermediary wrapping / unwrapping steps.

## Motivation

WETH is a very popular contract, almost constantly in the [“top 30-40 gas guzzlers” according to etherscan](https://etherscan.io/gastracker). WETH provides the very useful ability for contracts to have a unified interface to transact in both ERC20 tokens and the native EVM asset (Ether ETH on Ethereum).  Furthermore it gives ETH some added features due to its compliance with the [ERC20 standard](https://eips.ethereum.org/EIPS/eip-20):

- Safe force send: When WETH is transferred it does not trigger any code in the recipient meaning the transfer cannot be rejected or lead to reentrancy
- Approvals: WETH can be transferred from an account without its explicit action via transferFrom if it has approved a spender
- Events: Transfers of WETH emit events allowing off-chain applications to more easily track the flow of funds

However because this abstraction is not native to the EVM but a distinct contract it creates some friction for EOAs and overhead for application developers: EOAs need to submit an added transaction to “wrap” their ETH before it can be used with ERC20 only contracts. Developers who want to make that step seamless must implement additional logic to handle both ETH & WETH paths, increasing code size, complexity and as a result the attack surface of the contract. An example of this is the [Uniswap Router](https://ethereum-magicians.org/t/add-to-ether-the-erc20-token-logics-get-rid-of-weth/3659) which has duplicate methods to handle a user’s desire for ETH / WETH input / output.

## Proposal

- Proposal is implemented as a hard fork at some introduction_block
- Adds a precompile to the EVM at address eth_as_erc20_precompile_address which can be called as an ERC20 + ERC2612 token
- Transfers of the “token” at eth_as_erc20_precompile_address lead to “parallel” transfers of the actual balance of accounts, enforcing the invariant a.balance == IERC20(eth_as_erc20_precompile_address).balanceOf(a)
- Transferring ETH via the new precompile does not trigger the code of the recipient unlike transfers with CALL
- All transfers of ETH via CALLs and via the precompile after the introduction_block must emit a Transfer event
- Besides the standard methods dictated by the ERC20 and ERC2612 standards the precompile has optIntoETHasERC20() nonpayable returns () and usingETHasERC20(address) view returns(bool) methods
- Contracts created before the introduction_block must opt-into the “ETH as ERC20” behavior by calling an added optIntoETHasERC20() method
- The usingETHasERC20 method returns whether or not the passed address has access to the “ETH as ERC20” behavior, defaults to true for all contracts created post introduction_block

## Security Considerations

The above precompile breaks the invariant that

> ETH cannot be transferred out of an account unless it 1. Submits a valid transaction or 2. Executes a CALL call directly or indirectly in a valid sub-context initiated by DELEGATECALL or CALLCODE

Therefore, for the sake of backwards compatibility the “ETH as ERC20” behavior should be opt-in for contracts created prior to the implementation of such a precompile. Older contracts may still be vulnerable, even with the “required opt-in” protection if they do not expect the above invariant to be broken **and** are somehow able to trigger the precompile’s opt-in method via an arbitrary external call method or selector collision. To protect such contracts an alternative approach may be to altogether disable access to the precompile for older contracts.

Another security consideration would be the ability to receive ETH without having triggered although this is already a possibility today with the `SELFDESTRUCT` opcode and is likely to remain even after its “deactivation” when it’s changed to `SENDALL` for the sake of backwards compatibility.

## Other Considerations

One important consideration that hasn’t been mentioned above is what the cost of the different methods of the precompile should be. Considering that the precompile could safely be more tightly integrated with client implementations it’s likely fair to price the cost of some methods cheaper than what an ERC20 implementation would be. Furthermore the tradeoff of “protocol complexity vs. application users & developers” is also important to consider. I’ve left this considerations open for discussion as I’m not a client dev and think it’d be sensible to get some feedback before implementing a more fleshed out proposal.

## Conclusion

Allowing users and contracts to worry less if at all about the difference between ETH / ERC20 tokens would greatly improve UX & DX and make newer contracts simpler, more efficient and more secure.

Note this is not entirely a new idea, credit to this older discussion: [Add to ether the ERC20 token logics (get rid of WETH)](https://ethereum-magicians.org/t/add-to-ether-the-erc20-token-logics-get-rid-of-weth/3659)

Interested in hearing your feedback! Thx ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

## Replies

**moodysalem** (2022-12-11):

Not necessarily a con but it would be the first precompile with a function lookup table.

It would also be more complex for any new contract to natively support ETH after the change, which might still be cheaper than using the precompile, even if for example precompile#balanceOf is priced the same as BALANCE. Also there is a SELFBALANCE opcode, would the balanceOf call be expected to be cheaper if address of caller is passed in?

---

**Philogy** (2022-12-11):

That’s a good question, from the perspective of trying to price the precompile accurately I’d have the `balanceOf` method price the same as the `BALANCE` opcode. While there is the `SELFBALANCE` opcode it seems fairer to consider a `balanceOf(address(this))` call equivalent to `ADDRESS BALANCE` rather than `SELFBALANCE`.

If the function switch is deemed to complex to implement client side each method could have its own precompile with an actual contract being the switch. Contracts looking to interact with ETH as an ERC20 would then `DELEGATECALL` this custom contract which would trigger the relevant precompiles on its behalf.

---

**fedekunze** (2024-03-05):

Love this proposal. For Evmos we took a different approach and we instead created a precompile using the `IERC20Metadata` ABI on top of the native token (EVMOS in this case). The address of the precompile is the same as the current Wrapped EVMOS token to maximize compatibility with existing dApps. You can see our implementation [here](https://github.com/evmos/evmos/blob/main/precompiles/werc20/werc20.go).

Since Evmos is a BFT chain, we can execute a token migration during a software upgrade to trigger the `WEVMOS9.sol` contract’s `withdraw()` and convert the wrapped asset to native.

You can read more about the impact on users in our [blog post](https://medium.com/evmos/evmos-introduces-native-tokens-as-erc-20-for-cosmos-1a4c7de5c3e9)

