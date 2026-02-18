---
source: magicians
topic_id: 15211
title: ERC7399 - Flash Loans
author: albertocuestacanada
date: "2023-07-25"
category: ERCs
tags: [token, defi]
url: https://ethereum-magicians.org/t/erc7399-flash-loans/15211
views: 1386
likes: 2
posts_count: 8
---

# ERC7399 - Flash Loans

After a long while with ERC-3156 in the open, and given the lacklustre adoption, @ultrasecr.eth and I decided to replace it with a more flexible approach: [ERC-7399](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7399.md).

ERC-7399 segregates the control and asset flows to allow more efficient flash loan wrappers and more efficient flash loans for those using a push architecture.

ERC-7399 also allows for multiple callbacks to be defined, cutting on some complexity present on all borrowers.

## Replies

**wjmelements** (2023-07-25):

> function flashLoan

You’re using the wrong verbs for the identifiers. To “loan” is to lend to someone else. The top-level call should be “borrow” not “loan”, and the callback should be “loan”. If you insist on having “loan” in the initiating call, you should change the verb to “initiate” or “begin” or something grammatically correct.

> function(address, address, IERC20, uint256, uint256, bytes memory) external returns (bytes memory) callback

I don’t like that you parameterize the callback function into the ABI. It doesn’t make sense; instead the callback function should be standardized.

---

**wjmelements** (2023-07-25):

(I’m still sharing my thoughts on the grammar.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> You’re using the wrong verbs for the identifiers.

I have used “flash” as a verb in the past to describe this exact behavior, but if flash is the operative verb we don’t need an object.

ERC20 grammer is like `token.transfer(to, amount)` in which

- CALLER aka msg.sender is the subject
- transfer is the verb
- token is the object

---

**albertocuestacanada** (2023-07-25):

`flashLoan` was used in ERC3156, so for continuity I would be keen on keep on using it. Although I agree with you on the grammar, to “flash borrow” is not a common use of the concept. “beginFlashLoan” or anything that prepends a verb is grammatically correct, but also more verbose.

---

**albertocuestacanada** (2023-07-25):

> I don’t like that you parameterize the callback function into the ABI. It doesn’t make sense; instead the callback function should be standardized.

That was my initial thought as well, but parameterizing the callback function works pretty well. It allows to have several callback flows without encoding a callback type in `data`, which then would need to be decoded in the callback before the flow gets routed to the appropriate function. [No parameterized callbacks](https://github.com/yieldprotocol/yvarb/blob/7ac3648142ff48bbd0c12e429885697001007993/src/YieldNotionalLever.sol#L274) / [Parameterized callbacks on the lender](https://github.com/alcueca/erc3156pp/blob/56ba9dfdee8ad34150bc77de2bb67c950a1bb415/src/FlashLender.sol#L78) / [Parameterized callbacks on the borrower](https://github.com/alcueca/erc3156pp/blob/main/src/test/FlashBorrower.sol).

Also, this EIP intends to segregate the control and asset flows. The callback receiver can be different from the loan receiver. The callback parameter includes both, which helps with conciseness.

---

**albertocuestacanada** (2023-07-25):

I don’t mind using `flash`, tbh. There is no other “flash” in ethereum that would lead to confusion.

---

**wjmelements** (2023-07-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/albertocuestacanada/48/3057_2.png) albertocuestacanada:

> flashLoan was used in ERC3156, so for continuity I would be keen on keep on using it

If you aren’t also preserving all of the parameter types, there is no compatibility benefit to preserving the function name identifier. In fact, using the same identifier can cause confusion. An example of avoiding confusion in Compound V3:

```auto
function approveThis(address manager, address asset, uint amount) override external
```

---

**SamWilsn** (2025-06-10):

> maxFlashLoan and flashFee return numerical values on impossible loans to allow sorting lenders without having to deal with reverts.

The effort required to deal with reverts is trivial when compared to the risk of improperly handling a sentinel return value. It’s just safer to use reverts since they’re out-of-band compared to acceptable numeric values.

