---
source: magicians
topic_id: 14356
title: Timebound ERC20 Tokens for Subscriptions
author: sk1122
date: "2023-05-19"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/timebound-erc20-tokens-for-subscriptions/14356
views: 1455
likes: 2
posts_count: 10
---

# Timebound ERC20 Tokens for Subscriptions

Subscriptions in web3 have been a tricky problem to solve. Existing solutions like streaming ERC20 tokens have their flaws. For instance, they require upfront token approval, which opens the door for potential abuse. Imagine a streaming protocol withdrawing all approved ERC20 tokens! One workaround is to approve small amounts, but that means users have to keep approving multiple times to maintain their subscriptions.

**We can solve this issue by upgrading ERC20 tokens with timebound approvals.**

### Concept

The lack of time-bound restrictions in ERC20 token approvals allows dApps to withdraw all approved tokens in one go, posing security risks. Instead of enabling dApp to withdraw all approved tokens at a single time, dApps will be able to withdraw only certain amount of token between certain intervals. So now, that user will approve 1 token at interval of every 30 days for 6 months, dApp can withdraw that 1 token anytime in those 30 days, if they fail to withdraw those tokens, it will be carried forward in the next interval. This way, users can be certain that they are paying only for what they are using and that dApps can’t defraud them

### Interface

```auto
interface IERC20 {
    struct Recurring {
        uint256 allowedAmount;
        uint256 timePeriod;
        uint256 timeLimit;
        uint256 nextInterval;
    }

    mapping(address => mapping(address => Recurring)) public recurringAllowance;

    function recurringApprove(
        address spender,
        uint256 amount,
        uint256 timePeriod,
        uint256 timeLimit
    ) public virtual returns (bool);

    function transferFromRecurring(
        address from,
        address to,
        uint256 amount
    ) public virtual returns (bool);
}
```

Would love to get opinions from Ethereum Magicians community

Reference Implementation - [Github](https://github.com/shivam2320/erc20r)

## Replies

**0xRobinR** (2023-05-21):

you can check the already proposed [ERC20 token standard for subscription](https://ethereum-magicians.org/t/erc-subscription-based-erc20-token/13964), feel free to discuss and contribute to this eip

---

**sk1122** (2023-05-22):

Where can I find more details regarding this, you haven’t mentioned any links to implementation or documentation?

---

**0xRobinR** (2023-05-22):

yeah, just found that! ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12) here’s the link - [EIP-6932](https://github.com/360core/EIPs/blob/master/EIPS/eip-6932.md)

---

**0xRobinR** (2023-05-22):

working on the implementation, will be adding it as well.

---

**0xRobinR** (2023-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xrobinr/48/9258_2.png)
    [ERC: Subscription Based ERC20 Token](https://ethereum-magicians.org/t/erc-subscription-based-erc20-token/13964/7) [EIPs](/c/eips/5)



> a working implementation on auto-debit subscription-based erc20 token - EIP 6932

---

**sk1122** (2023-06-05):

nice implementation!

but why let dApps deploy a receiver contract? if a dApp has 3 subscription plans, then will they deploy 3 different smart contracts?

in our smart contract design, we let dApps keep subscriptions flexible, it can be any amount, any time period etc and not depend on a receiver contract, this will help them to change their subscription terms without much concern and also include specialised prices of certain businesses which is usually the case with SaaS companies.

---

**0xRobinR** (2023-06-06):

for auto-debit to be in action, I used an auto calculation based on the receiver contracts implementation of the `subscriptionInfo` variable.

for dApps, it will be easier for them to manage different subscriptions with different users on a different contract, by this, they can charge users accordingly, and can upgrade user subscription level as well.

moreover, [EIP-6932](https://github.com/360core/eip-6932) is an `auto-debit`, instead of giving dApps to trigger `transferFromRecurring` at every interval, they only have to deploy the contract once, and the `subscriptionAmount` will be auto-credited to their `receiverContract` at every interval, without triggering the contract.

---

**sk1122** (2023-06-06):

nice, how does auto-debit work?

---

**0xRobinR** (2023-09-21):

[check this](https://github.com/360core/eip-6932/tree/master) for more details

