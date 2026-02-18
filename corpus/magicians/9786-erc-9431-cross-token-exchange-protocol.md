---
source: magicians
topic_id: 9786
title: "ERC-9431: Cross-Token Exchange Protocol"
author: axelar-person
date: "2022-06-28"
category: ERCs
tags: [token, cross-chain, multi-chain]
url: https://ethereum-magicians.org/t/erc-9431-cross-token-exchange-protocol/9786
views: 920
likes: 3
posts_count: 4
---

# ERC-9431: Cross-Token Exchange Protocol

There is broad-based demand for standardization of cross-chain transfers of ERC-20 tokens. (See for example [this proposal from Optimism](https://ethereum-magicians.org/t/outlining-a-standard-interface-for-cross-domain-erc20-transfers/6151).) We at Axelar are seeking feedback on a proposal targetting the following goals:

- Simplicity and flexibility.
- This standard should be abstract enough to facilitate token transfer to both EVM and non-EVM chains.
- The caller doesn’t need to know how cross-chain transfers are implemented.

The idea is to add a `transferXChain` method that behaves like a conventional `transfer` except it also accepts a `destChain` argument. Similarly, we add `allowanceXChain`, `approveXChain`, `transferFromXChain` methods and accompanying events `TransferXChain`, `ApprovalXChain`. Taking inspiration from [ERC-223](https://github.com/ethereum/EIPs/issues/223), we also add a generic `auxiliaryData` argument to these new methods so as to facilitate additional features at the discretion of the implementer.

With these items in mind, the new interface might look something like:

```solidity
interface IERC20XChain is IERC20 {
    function transferXChain(
        string recipient,
        uint256 amount,
        string recipientChain, // new
        bytes auxiliaryData    // new
    ) external returns (bool);

    function approveXChain(
        string spender,
        uint256 amount,
        string spenderChain, // new
    ) external returns (bool);

    function allowanceXChain(
        address owner,
        string spender,
        string spenderChain, // new
    ) external view returns (uint256);

    function transferFromXChain(
        string sender,
        string recipient,
        uint256 amount,
        string recipientChain, // new
        string senderChain,    // new
        bytes auxiliaryData,   // new
    ) external returns (bool);

    event TransferXChain(
        string indexed from,
        string indexed to,
        uint256 value,
        string toChain,       // new
        string fromChain,     // new
        bytes auxiliaryData   // new
    );

    event ApprovalXChain(
        address indexed owner,
        string indexed spender,
        uint256 value,
        string spenderChain, // new
    );
}
```

## Notes

- The implementer has complete flexibility in how to interpret recipientChain and how to execute the cross-chain transfer. For example, the implementer could use a cross-chain platform such as Axelar.
- The recipientChain is string to afford maximum flexibility and to play nice with block explorers. We recommend a separate standard such as CAIP-2 on a universal convention for which string sequences correspond to which chains.
- The recipient is now string to afford maximum flexibility for the address format in the destination chain. (For most chains an address fits into a bytes32 but we do not wish to preclude chains with longer addresses.)
- recipientChain need not be different from the current chain. Presumably, implementers would optimize their implementation for this special case so as not to spam cross-chain infrastructure.
- approveXChain and allowanceXChain have a new spenderChain argument so that the spender’s address can reside on a different chain.

Example: Alice holds token T on chain A, approves Bob on chain B. Bob can post a tx to chain B that sends Alice’s tokens from chain A to Charlie on another chain C. Alice’s approval of Bob on chain B should be restricted only to chain B—Bob should not be able to use this approval to send tokens on Alice’s behalf from any chain other than B.
- It is the responsibility of the implementer to execute and enforce this behaviour.

Possible uses of `auxiliaryData`:

- Define the unlocking condition for a token returning to its native chain.
- Execute functions elsewhere outside of this token transfer.
- Point to a specific on-chain mapping chain string -> chain data.

## Community call

We want your feedback! You’re invited to a community call on Wednesday, July 13, 2022 at 13:00–13:30 UTC to discuss this proposal. [[zoom link]](https://us06web.zoom.us/j/88358657959?pwd=K2dZaEd4YlBSdXFLQXAxOEpBa0c3UT09)

Anyone who has read this far is welcome to attend. Explicit invitations for the following forum members who have expressed interest in this topic in the past: [@maurelian](/u/maurelian) [@TransmissionsDev](/u/transmissionsdev) [@Dzack23](/u/dzack23) [@fredlacs](/u/fredlacs) [@luzius](/u/luzius) [@akolotov](/u/akolotov) [@frangio](/u/frangio)

## Replies

**frangio** (2022-07-04):

What is the reasoning to add these in the token itself?

---

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/a/65b543/48.png) axelar-person:

> We recommend a separate standard on a universal convention for which string sequences correspond to which chains.

See [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-2.md).

---

**axelar-person** (2022-07-05):

FYI the community call has been rescheduled to Wednesday, July 13, 2022 at 13:00–13:30 UTC.  The original post has been updated to reflect this change.

---

**weijia31415** (2022-07-05):

We have submitted a crosschain identity of bytes32 format.  This format can provide chain id for hard fork cases.  The human readable version can be done by a registration smart contract.

https://eips.ethereum.org/EIPS/eip-3220

