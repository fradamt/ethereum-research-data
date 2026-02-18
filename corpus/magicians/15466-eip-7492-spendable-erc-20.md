---
source: magicians
topic_id: 15466
title: "EIP-7492: Spendable ERC-20"
author: omnus
date: "2023-08-16"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7492-spendable-erc-20/15466
views: 783
likes: 2
posts_count: 5
---

# EIP-7492: Spendable ERC-20

An extension of ERC20 that allows user’s to initiate a transfer of tokens that:

1. Transfers the tokens.
2. Calls a hook in the receiver passing arguments.
3. Receives returned arguments.

This allows contract interations that are currently performed with the approve → pull pattern to be executed with a single EOA method call.

Any ERC20 interaction beyond a simple transfer requires the user to authorise a contract to their token then make a call on this contract. This has two main disadvantages:

1. The holder of the ERC20 token must make two contract calls for a single operation. This increases friction and gas cost.
2. The holder gives permission to transfer tokens (in some cases for all of their holding), to another address. This has obvious security implications, and is the root cause of many stolen tokens.

ERC20Spendable allows ERC20s to operate as ‘spendable’ items, i.e. an ERC20 token that can trigger an action on another contract at the same time as being transfered. Similar to ERC677 and the hooks in ERC777, but with more of an empasis on interoperability (returned values) than ERC677 and specifically scoped interaction rather than the general hooks of ERC777.

https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7492.md

## Replies

**radek** (2023-08-20):

I wonder what are the + / - to other similar EIPs? E.g. [ERC-1363: Payable Token](https://eips.ethereum.org/EIPS/eip-1363)

---

**omnus** (2023-08-21):

Hi [@radek](/u/radek)!

The two most similar EIPs are ERC-777 and ERC-677.

For a long time ERC-777 was seen as the natural successor to ERC-20. ERC-677 is the transferAndCall standard developed by chainlink.

Soooo, how does EIP-7942 compare?

**ERC-777** ([ERC-777: Token Standard](https://eips.ethereum.org/EIPS/eip-777)): ERC-777 introduces hooks into fungible tokens, allowing ERC-777s to take actions when tokens are received, just like EIP-7492. But it’s adoption has been held back because:

1. So much infra already supports the ERC-20 interface (ERC-777 has send rather than transfer for example). This means that moving everything from ERC-20 to ERC-777 is a heavy lift.
2. Hooks are great, but they make the token re-entrant. If people just post ERC-20 functions to ERC-777s you can bet we will see re-entrancy issues.

The hooks in EIP-7492 operate in a similar way, but the developer can make a choice to use them. To use the hooks you need to be making use of the `spend` method. You will have access to the current ERC-20 `transfer`, which not only cannot be re-entered, gives backwards compatibility.

You have the best of both worlds: full ERC-20 compatibility, a non-reentrant `transfer` method, and hooks on the `spend` method.

**ERC-677** (https://github.com/ethereum/EIPs/issues/677). Other than use in chainlink, I can’t find many examples of this being used. Indeed, even the `transferAndCall` method is less used now, with the advent of chainlink v2 and subscription contracts.

The functionality here is similar to EIP-7492, but EIP-7492 is clearer about how data is passed back up the call stack. ERC-677 is really about one-way traffic, wherever EIP-7492 envisages actions in the called contract hook, and indeed in the caller (through `_handleReceipt`) if required.

Thanks for asking, I really appreciated it!

---

**radek** (2023-08-23):

Thanks for the elaboration on that!

Honestly, I already forgot about https://github.com/ethereum/EIPs/issues/677 as it is not considered ERC anymore ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) Not listed on the EIP/ERC web, PR closed, etc.

However [ERC-1363: Payable Token](https://eips.ethereum.org/EIPS/eip-1363) is considered to be the successor of #677 and finally [ERC-223: Token with transaction handling model](https://eips.ethereum.org/EIPS/eip-223) (the predecessor to #677) got attention to become regular ERC.

Can you also compare to these for the completeness? (1363 and 223)

---

**omnus** (2023-08-31):

Hi [@radek](/u/radek),

Sorry for the slow reply.

Two excellent examples! The differences:

**ERC-223:** The main drawback here is that it isn’t compatible with existing ERC-20 architecture. It’s an entirely separate standard, that uses the same `transfer` function signature and requires that any contract recipient implement the receiver. Any contract that doesn’t will revert. See for example from the EIP:

[![Screenshot 2023-08-31 at 1.32.42 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/5/52ef274ba6390226616ce053748e59ff281dc1b3_2_690x156.png)Screenshot 2023-08-31 at 1.32.42 PM2088×474 85.3 KB](https://ethereum-magicians.org/uploads/default/52ef274ba6390226616ce053748e59ff281dc1b3)

This means you can’t just roll ERC-223 into a world that supports the current IERC-20 interface and have it work. It’s more revolution than evolution. I’m down for revolutions, but in this case I think it puts too much pressure on immediate mass adoption.

**ERC-1363:** This is similar to the proposal here in EIP-7942. I’d happily use it! But I think it’s inability to pass meaningful data back up the call stack is a weakness. It means you can’t use it for a genuine two way interaction, where the sending contract has a hook to process when the token has been confirmed as received. That’s something that is built into EIP-7942, and while it might not get used often, I think it’s an interoperability enhancement that is worth having.

Once again, I really appreciate your input!

