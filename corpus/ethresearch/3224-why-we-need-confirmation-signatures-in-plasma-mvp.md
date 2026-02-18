---
source: ethresearch
topic_id: 3224
title: Why we need confirmation signatures in Plasma MVP?
author: dcb9
date: "2018-09-05"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/why-we-need-confirmation-signatures-in-plasma-mvp/3224
views: 3033
likes: 7
posts_count: 6
---

# Why we need confirmation signatures in Plasma MVP?

Hi there,

I’m a newbie here. After reading [Minimal Viable Plasma](https://ethresear.ch/t/minimal-viable-plasma/426), i am wondering about the confirmation signatures.

> User Behavior
> The process for sending a Plasma coin to someone else is as follows:
>
>
> Ask them for their address.
> Send a transaction that sends some of your UTXOs to their address.
> Wait for it to get confirmed in a block.
> Send them a confirm message, signed with the keys that you use for each of > your UTXO inputs.

I couldn’t figure out why we need the step 4, what possible problems can it solve.?

Thanks

## Replies

**m0t0k1ch1** (2018-09-05):

I had the same question too. I think the following thread is very helpful for understanding confirm sig.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/jchoy/48/1270_2.png)
    [Why do/don't we need two phase sends plus confirmation](https://ethresear.ch/t/why-do-dont-we-need-two-phase-sends-plus-confirmation/1866) [Plasma](/c/layer-2/plasma/7)



> Hi ethresear.chers! These days, I’m reading Plasma and Plasma Cash. I saw the transaction on Plasma chain is complicating. Let’s assume a transaction A->B. Correct me if I’m wrong.
> On Plasma, the process should be:
>
> A makes transaction and send to operator.
> Operator makes a block including above transaction and update on parent chain.
> A is waiting for the information to be included in Root chain
> After that, A signs and sends to B
> B signs and the transaction is confirmed
>
> I’m wondering why A sh…

---

**MihailoBjelic** (2018-09-05):

Yes, the post which [@m0t0k1ch1](/u/m0t0k1ch1) linked to should help you, especially [this comment](https://ethresear.ch/t/why-do-dont-we-need-two-phase-sends-plus-confirmation/1866/14), it answers your question in a very clear, easy to understand way.

For future references, basic and technical questions are more suitable for StackExchange. Ethresear.ch is more about research ideas, results and related discussions. Don’t worry, I was making the same mistake, until someone explained this to me. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**dcb9** (2018-09-06):

That’s very helpful! Thanks a lot!

---

**dcb9** (2018-09-06):

Thank you for your pointing out the comment which i should pay attention to and your advice!

---

**MihailoBjelic** (2018-09-06):

You’re more than welcome. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

