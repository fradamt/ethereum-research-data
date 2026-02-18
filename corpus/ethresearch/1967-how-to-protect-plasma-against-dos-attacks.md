---
source: ethresearch
topic_id: 1967
title: How to protect Plasma against DoS attacks?
author: kladkogex
date: "2018-05-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/how-to-protect-plasma-against-dos-attacks/1967
views: 5505
likes: 20
posts_count: 30
---

# How to protect Plasma against DoS attacks?

This is a DoS scenario that came up recently in conversation with a developer that thinks about using Plasma. He brought up the scenario described below.

I do not think it has been discussed in detail in existing Plasma documentation so it is worth discussing it here

The scenario is as follows:

1. A successful ecommerce vendor (e.g. a decentralized ebay) runs a Plasma micropayments chain with 100 million users and $1B in deposits.
2. Eve wants to do a  DoS attack on the vendor
3. Eve deposits $1 into the Plasma chain and spends all of it.
4. Eve intentionally attempts  to pull out the $1 she spent, triggering fraud exits.
5. The entire 100M users rush to exit,  pulling $1B in deposits and paying millions of dollars in ETH fees.

The existing Plasma MVP explanations seem to suggest that if one user does a bad thing, then all users need to exit, which seems to enable the DoS attack described above. Is this really the case?  Must all users exit?

If not, I think the existing Plasma tutorials and docs need to be modified, since the docs seem to suggest  the “all out” strategy as the must.

## Replies

**vbuterin** (2018-05-10):

> The entire 100M users rush to exit, pulling $1B in deposits and paying millions of dollars in ETH fees.

No. The 100m users would only rush to exit in the event of the chain itself being fraudulent. In this case, the users would just challenge the malicious exiter’s withdrawal and move on.

---

**kladkogex** (2018-05-10):

Sorry - looks I totally missed the point.

Then a follow-up scenario:

1. Eve deposits $10 and makes 1,000 payments (in sequence) of one cent to one thousand users (and generates 1000 intermediate UTXOs in the process)
2. Eve then tries to pull her $10.

The question is, is this economical then to submit fraud proofs? Economically it may not make sense for any user to do it, since money spent on ETH fees (probably around 1USD) will be way more than 1 cent recovered. How is it going to work in practice? Is the first guy in the chain of 1000 UTXOs supposed to submit the fraud proof? What if he does not do it because he decides it is not economical?

---

**haydenadams** (2018-05-11):

> The question is, is this economical then to submit fraud proofs?

One easy solution would be to implement minimum withdrawal amounts.

---

**kladkogex** (2018-05-11):

How do you propose to do it exactly ?)

In the example above Eve pulls $10 so it is not a small amount …  If you impose a $20 limit, she can play the same strategy with $30 …

---

**peara** (2018-05-12):

I think Eve need to submit a bond which the challenger will receive for compensation if succeeded as it’s already said somewhere. This makes every challenge economical.

---

**kladkogex** (2018-05-14):

The problem is the amount of the bond  may need to be infinite, as in

[this example](https://ethresear.ch/t/minimal-viable-plasma/426/80)

---

**maxweng** (2018-05-14):

I don’t believe it’s gonna be a big issue, as the user doesn’t have to withdraw all utxos at a time. The user just need to deposit a certain amount of ETH, and repeat that for a few times.

I mean, for the bond, it just needs to be larger than the tx fee, like $1 usd as you mentioned. then others will have the incentives to challenge. It doesn’t have to relate to the amount of withdrawal. my 2c

---

**peara** (2018-05-15):

The example assumes that every invalid utxos must be challenged. But it can be changed to challenging 1 invalid utxo is enough to cancel the whole withdrawal. So bond for just 1 transaction is enough.

---

**kladkogex** (2018-05-16):

You mean that Plasma spec should be changed  ?

---

**peara** (2018-05-16):

No, I don’t think it’s a requirement. It’s just a design choice to handle a special case.

If you feel fit, you can even disable mass withdrawal altogether and this case will never happen.

---

**kladkogex** (2018-05-16):

All of these things need to be defined mathematically and analyzed - every change to the protocol tends to have lots of potential repercussions imho

---

**peara** (2018-05-17):

Yes, I agree. But it is specific for your application/implementation. Plasma in the general sense is a pattern, not a specification. That’s why there are several Plasma styles already .

Also, I believe that in the original plasma paper, the solution for this case has already been discussed. It was mass-exit with bitmap of UTXOs which requires a bond to be placed. Any fraud proof can cancel the whole withdrawal.

---

**hamdiallam** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/peara/48/1293_2.png) peara:

> No, I don’t think it’s a requirement. It’s just a design choice to handle a special case.
> If

In our implementation, there is a minimum bond when exiting that is forfeited to the challenger if successful. This is to ensure that it always economically makes sense to challenge, discourages a user to submit multiple exits for funds ( your scenario above ), and encourages people to play the role of bounty hunters of a side chain. Revenue for just watching and ensuring the integrity of the plasma chain.


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [GitHub](https://github.com/fourthstate)



    ![](https://ethresear.ch/uploads/default/original/3X/9/3/93b79fd11ad0a601755a948321879392930639e4.png)

###



Blockchain Scalability Research Lab. FourthState Labs has 4 repositories available. Follow their code on GitHub.

---

**kfichter** (2018-05-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Eve deposits $10 and makes 1,000 payments (in sequence) of one cent to one thousand users (and generates 1000 intermediate UTXOs in the process)

In this scenario, if Eve attempts to withdraw her original $10 output, then someone can just submit a single fraud proof showing that that $10 output was spent. The bond placed with the withdrawal is deliberately large enough that it covers the cost of challenging. I’m not sure I see the issue here.

---

**kladkogex** (2018-05-17):

Can you explain this more?

Each time Eve spends 1 cent she generates a new intermediate UTXO,  If one exits all these intermediate UTXOs at once - how can a single fraud proof be used for all of them ?

---

**kfichter** (2018-05-17):

Ah you’re saying exit *all* intermediate UTXOs. The value of the UTXO doesn’t matter, just that the minimum bond must be large enough to cover the cost of challenge. So there’s some small UTXO value at which it’s no longer worth it to exit.

Let’s say cost to exit < 1c, so Alice will try to exit from the UTXOs. Alice puts up a bond = cost to challenge, which may be larger than 1c. Someone is therefore incentivized to challenge, even if the UTXO values are small.

---

**kladkogex** (2018-05-17):

Lets say, Eve puts $10,000 dollars, and then creates 1,000,000 intemediate UTXOs

If Eve exits all of these UTXOs unchallenged, then her potential gain is  $5B

Lets say exit transaction gas fee is $1, then Eve needs to have $1M to pay for the gas fees.

Now the challengers will need to pay (altruistically) $1M to submit fraud proofs to challenge Eve.

if they successfully challenge Eve, then Eve loses $1M and challengers lose $1M.

Eve can then make another attempts.  Lets say after 100 attempts she exhausts the money that challengers are altruistically willing to pay. At that point  both Eve and challengers  kist $100M each.

Since challengers dont have any more money (or are not willing to fight any more), Eve makes $1B and wins.

So crypto economically it seems that challengers need to be compensated ? Would you agree?  Otherwise it seems to be hard to rely on altruistic behavior …

---

**hamdiallam** (2018-05-18):

In addition to the $1M Eve has to pay for the gas costs of each exit, she has to put up a bond on each individual exit. This is so that the challenge never loses money by successfully challenging. Hence, it will cost Eve at least $2M to exit the 1M intermediate UTXOs she has created.

---

**kfichter** (2018-05-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Now the challengers will need to pay (altruistically) $1M to submit fraud proofs to challenge Eve.

We never want to make users doing anything altruistic. Every exit has a bond attached that will pay the challenger’s gas cost and more. So the challenger pays X in gas cost (and some other costs) but receives X+N in return for a successful challenge.

---

**kladkogex** (2018-05-18):

Ok - good ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Now I understand ) I think this can be a way to address the issue.


*(9 more replies not shown)*
