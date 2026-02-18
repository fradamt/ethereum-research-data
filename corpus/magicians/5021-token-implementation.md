---
source: magicians
topic_id: 5021
title: Token Implementation
author: JhonnyJason
date: "2020-12-10"
category: Uncategorized
tags: [token]
url: https://ethereum-magicians.org/t/token-implementation/5021
views: 637
likes: 2
posts_count: 2
---

# Token Implementation

Hello Folks - Just on the Journey of Token Implementation and thought I would ask for Opinions to some design decisions.

1. Do most brutish raw implementation of ERC20 in vyper to skip on most all checks.
2. Allow ZERO_ADDRESS transfers - burn and minting would use the tokens contract address instead.
3. Default to approve X for one transaction.
4. Donot set approvals back to 0 again instead use int128 and set it to -1 - so the space will not become freed. Update -> this is nonsense xD, because free will also return gas, and is overall more gas efficient

---

Point 3 probably needs some further explaination and is also the part with highest level of uncertainty.

From my perspective there are 3 different ways how to approve.

1. give Full Approval and done until revoked
2. give Approval for a max of X tokens to be spend for 1 transaction
3. increase or decrease the Approved amount of tokens to be spent

The thing is for nr. 2 that as soon as you have approved for 1 transaction…

- …you actually expect that it definately will be used
- …it would reset any left amount to -1. -> Update: reseting to 0 is better
- …well, is debatable if it is more desirable not reset the left amount to -1 afterwards^^ -> Update: reseting to 0 is better

To me it appears that the default thought behaviour is that nr. 2 without the limitation of only one transaction.

When does the case ever occur where it is necessary to grant a spending limit over multiple transactions?

Isn’t better then to use the increase, decrease allowance mechanics for this case instead?

## Replies

**JhonnyJason** (2020-12-10):

So in the meantime everything has changed due to the update that setting allowances to -1 is not really useful and also the transferFrom function which always resets to 0 is not as gas-efficient as the version of just subtracting the used amount.

So now it mainly boils down to:

1. absolute raw brutishness of implementation
2. Allow ZERO_ADDRESS transfers - as burn and minting address will be the token contract itself.

[Here](https://github.com/JhonnyJason/jhonnyjason-token/blob/master/contracts/JhonnyJasonToken.vy) is the implementation - is this implementation acceptable? XD

