---
source: ethresearch
topic_id: 1397
title: "DAICO: Praise and Critique"
author: akomba
date: "2018-03-15"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/daico-praise-and-critique/1397
views: 3086
likes: 3
posts_count: 6
---

# DAICO: Praise and Critique

## Praise

Vitalik’s DAICO idea was badly needed. It’s really good to see the right message propagated from the top.

If I were to describe blockchains in one word, it would be “blockchains make things more accountable”. If I were allowed only a single word, it would be “accountability”.

The fact that ICOs don’t do everything they can to keep themselves accountable is a disgrace to the technology and community. So Vitalik highlighting the issue and proposing a solution is very important.

### DAICO

According to the proposal, DAICOs have three extra functionalities, compared to multisig wallets:

**“The Tap”**: Owners of the DAICO aren’t able to withdraw all the funds. The DAICO only allows them to withdraw a pre-defined amount per unit time (usually monthly).

**“Opening The Tap”** : If the project is doing well, the ICO token holders can increase the monthly allowance by “opening the tap”. However, they can’t reduce it. The process is one way only.

**“Closing Shop”**: If the project is not doing well, the ICO token holders can vote to close down the DAICO. In this event all the remaining funds are returned to the current token holders.

## Critique

The above proposal is very sensible, and a great step to the right direction. However, it has several weaknesses. I would like to go through them one by one, explain them and propose solutions. The list of weaknesses are below, then a detailed explanation follows.

- Automating The Tap
- Pre-Sale Exploits
- Public Sale Exploits
- “Closing Down” Exploit
- Proposed Solutions

### 1. Automating the Tap

Asking the community to “open the tap” more every time is not practical.

From one side, a properly planned business will have a sensible and explainable spending curve. It will start low, and then it will increase, according to the business plan. It makes sense to put this expected emission curve into the DAICO, so if the business is going as planned, then there is no action needed from the community.

This also deals with the problem that the business might die or miss opportunities because not enough of the community can be bothered to vote to increase the allowance.

The possibility for the community intervention to open the tap even more should be still implemented, but only be used under exceptional circumstances, when the company needs to deviate from the plan (spend more, with a good reason).

### 2. Pre-Sale Exploits

This exploit aims to take away the ability of the token holder community to use the “Closing Shop” option. In principle 51% of the token holders must vote “yes” to close shop.

This can be easily circumvented by a fraudulent ICO.

During the pre-sale phase of ICOs there are large percentage of ICO tokens get sold, and it is not always known what the project gets for the tokens. It is inevitable, because pre-sale contributors might pay with cash, fiat currencies, shares, etc. Many of these don’t have a proper representation on the blockchain yet.

The exploit is trivial: A fraudulent team might just do a large pre-sale, where they issue near 50% of all tokens to themselves.

Please note that they don’t have to own 50%. Much smaller amount is enough to make it difficult for the rest of the token holders to reach consensus. For example the fraudsters running the ICO only issue 25% of the tokens to themselves — now the rest of the community only owns 75%, so the 51% requirement to close down now was increased to 68%.

### 3. Public Sale Exploits

Even if there is no pre-sale, an exploit can be carried out during the public sale as well. A fraudulent group can borrow a significant portion of ether, and buy their own tokens on the public sale.

After the sale they can return the ether gradually from the tap, with interest.

This is a less attractive option, but similarly to the pre-sale exploit, it can make the closing down significantly more difficult.

Also, there is no financial risk for the lenders, because the ether is there, it just takes time to get to it.

### 4. “Closing Down” Exploit

This is an interesting variation of the pre-sale exploit. The fraudsters acquire tokens as described in the pre-sale exploit. Then they trigger the close down. They might even apologize — because of reasons, the project can’t continue, but worry not, all eth is accounted for. Except that it’s not true.

Then money gets returned to the token holders — including them, since they own a large amount of tokens. They go scott free, having made a potentially large profit.

## Proposed Solutions

The “automating the tap” issue contains its own solution: implement a rising emission curve that is in accordance with the project’s business plan, and supermajority voting to permit extra raises as an exception if properly explained.

The other issue — meddling with the shutdown — is more complex. Especially when considering the “Closing Down” exploit. The technical solutions for these are all complex and uncomfortable:

### Solution 1: No Presale

One solution is to forbid having a presale. This is technically easy, but business-wise difficult, might even be a deal-breaker. It means that it would be enforced that no special business deals could be made. From an idealistic point of view it is defendable, but realistically thinking it might not always be acceptable. Not all private deals are bad.

Also, this does not fix the “public sale” exploit.

### Solution 2: Two Tokens

Another natural solution is to mandate that only public sale tokens can be used to vote for the shutdown. Of course, the problem with this is that it implies that we either have two different tokens (presale tokens, public sale tokens) or somehow we make the tokens non-fungible.

Neither of the options are attractive, not to mention that it is dubious if it could be technically carried out. Think about the madness on the exchanges. This is a no-go.

Also, again, this does not address the “Public Sale” exploit.

### Solution 3: A Centralized Shutdown Switch

All of the exploits above come from the fact that the number of votes can be manipulated with. There is an obvious solution — using the existing legal framework.

By creating a special account that can be proven to be able to shut down the DAICO, and return the funds to the token holders. Then depositing this key with a known, independent party (lawyer, etc).

In case of fraud, a lawsuit can be launched and the key can be demanded. This shutdown switch would not replace the community’s ability to close the shop, it would be added as an extra feature.

The purpose of an ICOs is to raise funds in an accountable, yet easy manner. The purpose of an ICO is not to be above the law. Almost all projects or companies should be exposed to the extant legal processes. The backend key could expire after some period of time.

## Conclusion

DAICO is needed, great step to the right direction

Should use an emission curve instead of asking the community to increase the tap

Create a centralized shutdown switch that can be activated by a legal process.

There are other steps that we can take to make ICOs more accountable. For example tokenizing the pre-ICO deals and fiat currencies. I will expand on those and propose a full solution in the upcoming post.

Thanks go to Virgil Griffith for the review and suggestions.

Original post: https://medium.com/@akomba/daico-praise-and-critique-2c5bcee2acfe

## Replies

**vbuterin** (2018-03-15):

I fail to understand how (4) is an exploit. Sure, holders can close a project down and get their tokens back. But where does their “potentially large profit” come from? Are you saying that this would happen if ETH suddenly appreciates a lot after a sale? If so, then I agree that could be a problem but I think the easiest solution is to denominate the DAICO in DAI.

In general, I would argue that in a “good” sale, public sales should make up a great supermajority of all token issuance. If some tokens need to be held back for future sales, that can be done by simply not issuing them until the time for the future sale comes. In fact, you can even require a future sale to be one of the events that the DAICO token holders need to vote to unlock.

> Asking the community to “open the tap” more every time is not practical. From one side, a properly planned business will have a sensible and explainable spending curve. It will start low, and then it will increase, according to the business plan.

There is a tradeoff here. In principle, I agree that allowing taps to be dynamic curves instead of numbers is ideal and allows for more options. That said, requiring explicit public approval for each step of growth has benefits; it creates more choke points where people can demand accountability. There is an inevitable tradeoff here, and it’s not yet clear what the ideal point on it is.

> Solution 3: A Centralized Shutdown Switch

Are you suggesting a centralized shutdown switch in place of, or alongside, the token holder voted switch. If it’s in place of, I would argue that that’s a bad idea, because in general legal systems are designed for detecting malfeasance, not underperformance, and we want DAICOs to be shut down in the event of underperformance too. If alongside, then shutdown attacks by voters could still happen (if you’re worried about shutdown attacks; I personally am not that worried, as in the event of a fraudulent shutdown the developers can just restart the DAICO).

---

**akomba** (2018-03-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I fail to understand how (4) is an exploit.

Example: BadICO issues 50% of the tokens for themselves in the presale. They sell the other 50% for 100 eth. Then they activate the shutdown switch and the 100 eth gets distributed among the 100% of the token holders, thus netting them 50 eth.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Are you suggesting a centralized shutdown switch in place of, or alongside

Alongside. You are right, I will make that more clear.

---

**vbuterin** (2018-03-15):

> Example: BadICO issues 50% of the tokens for themselves in the presale. They sell the other 50% for 100 eth. Then they activate the shutdown switch and the 100 eth gets distributed among the 100% of the token holders, thus netting them 50 eth.

This is an excellent argument for not giving non-public-sale-participants liquid tokens, at least until the DAICO runs out.

---

**clesaege** (2018-03-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This is an excellent argument for not giving non-public-sale-participants liquid tokens, at least until the DAICO runs out.

To solve this, we could have two tokens, the utility one and the DAICO one. In order to vote, we would need both the utility and the DAICO tokens. Presale and teams would only get utility tokens. DAICO tokens, not matched with the utility one would be worthless, we can even simplify transfers by wrapping both of them into a combined token.

---

**akomba** (2018-03-17):

I like this.

Since I wrote the original article, I came up with a similar solution: Everyone gets the ICO tokens, but control tokens only gets handed out during the public sale. So only being a public sale supporter gives you the privilege to approve / shutdown.

Then it’s only up to that public-sale-contributor person if they want to give up / sell that right (aka sell the control token).

I originally did not think of tying the voting rights to having both tokens. But the more I think about it the more I like the idea.

