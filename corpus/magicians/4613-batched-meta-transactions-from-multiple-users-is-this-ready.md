---
source: magicians
topic_id: 4613
title: Batched meta transactions (from multiple users) - Is this ready for an EIP draft?
author: cmango
date: "2020-09-13"
category: Magicians > Primordial Soup
tags: [erc-20, meta-transactions]
url: https://ethereum-magicians.org/t/batched-meta-transactions-from-multiple-users-is-this-ready-for-an-eip-draft/4613
views: 1708
likes: 7
posts_count: 19
---

# Batched meta transactions (from multiple users) - Is this ready for an EIP draft?

Hi all!

I’ve made a proof-of-concept for batched meta transactions (from multiple users): [GitHub - defifuture/erc20-batched-meta-transactions: A proof-of-concept for batching meta transactions.](https://github.com/defifuture/erc20-batched-meta-transactions)

The motivation behind this idea is to help **reduce the transaction cost** for the end user (a meta tx sender).

In addition to being used as a standalone solution, batched meta transactions can also work with popular L2 solutions (sidechains, rollups) which require an on-chain deposit transaction before they can be used.

I would love to hear your feedback about this proof-of-concept. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=9) **Do you think it’s ready to be submitted as the EIP draft?**

Thanks,

Matt

## Replies

**matt** (2020-09-14):

Nice work! I think amortizing the intrinsic cost over meta-txs is one of its best use cases. Has this not been included in any prior EIP? It might also be useful to see how Gnosis Safe performs meta-txs. I had the understanding they were already doing this (or capable of it).

---

**cmango** (2020-09-14):

Hey Matt, thanks for the feedback! ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=9)

I haven’t seen batched meta transactions (from various senders) in any EIP so far. The closest one is [EIP-1776](https://github.com/wighawag/singleton-1776-meta-transaction) by Ronan (wighawag), but it is about batching txs/calls of a single user, not batching meta txs of multiple users (it might be the same with Gnosis Safe, but I can’t find the meta tx implementation in their [Solidity code on GitHub](https://github.com/gnosis/safe-contracts)…).

I believe this is because when there was a big hype around meta txs (about a year ago), the gas price was not an issue. So everyone focused on the feature of enabling gasless transactions for users/addresses that don’t hold any Ether. Batching meta txs to lower transaction costs was not that important back then ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**matt** (2020-09-14):

Thanks for looking into that. If this approach hasn’t been documented before, I suppose it makes sense to EIP it. I am on the fence whether this is considered an informational or interface EIP. Although it is specifying an interface, it isn’t really necessary to document on-chain interfaces as EIPs, unless interoperability is desired. In your case, it doesn’t appear to describe how the interface will be used by multiple parties, only the a single relayer and relayer front-end. If this is what you plan to build, I would recommend making an information EIP and focus on explaining how meta-txs can be used to amortize the intrinsic tx gas cost in a general purpose way. You can also skip the EIP and just implement your project. Alternatively, if you hope this interface will be used by some relayer *network* then it makes sense to write this as an interface EIP.

---

**cmango** (2020-09-14):

I see my proposal in the same category as [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) (the *permit()* function) - so basically a function that extends the ERC-20 standard. I’m not really sure whether to classify it as an informational EIP or an interface EIP.

Regarding how the *processMetaBatch()* function can be used - it’s in fact agnostic to the usage. It can be used by a single relayer, or by a network of relayers. For smaller dApps I believe a single relayer would suffice, but for bigger dApps (meaning the ones with more traffic) a network of relayers would be needed, so that they can do load balancing and avoid collisions (meta txs with the same nonce).

---

**matt** (2020-09-14):

Ah, apologies. I had in my head that this was a general proposal, rather than one focused on ERC-20, but as you’ve pointed out you are indeed hoping to extend the ERC-20 interface. In that case, that makes sense to go down the interface EIP route.

---

**jpitts** (2020-09-20):

FYI, I noticed that Discourse was incorrectly hiding some messages in this topic. I have restored them!



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)
    [My topic is temporarily hidden - what to do?](https://ethereum-magicians.org/t/my-topic-is-temporarily-hidden-what-to-do/4641/2)



> Hi! Probably the Discourse software marked this “hidden” because this is your first post here. I’ll fix it shortly…

---

**cmango** (2020-09-20):

Just an update, I’ve completed the **gas usage tests** and as it (unfortunately) turns out, batched meta transactions are **not cost-effective for M-to-M use cases** (many senders, many recipients with 0 previous token balance).

In case of 100 meta txs in a batch (100 senders, 100 recipients with 0-balance, all unique), the **average gas per meta tx is 57’000** (see Test #6), which is higher than a normal on-chain token transfer transaction (**51’000 gas**).

It’s worth noting that this is the case where recipients haven’t held any tokens before, so a “worst-case” scenario. In case all recipients had a **non-zero token balance before**, the average gas used per meta tx would be **42’032.75** (see Test #7).

Other use cases, such as **1-to-M** (1 sender, many recipients - Test #4) and **M-to-1** (many senders, 1 recipient - Test #5) **have better results** (for “zero-balance” recipients). In case of 100 meta txs in a batch, the 1-to-M example used 33’813.11 gas/meta tx, while the M-to-1 example had used 38’025.83 gas/meta tx (**34% and 25% gas reduction** compared to an on-chain token tx, respectively).

The **link to complete test results** is **in the first post** in this topic.

> The system doesn’t allow me to post new replies containing a URL address - @jpitts can you look into that? I’m getting the “Sorry you cannot post a link to that host” error.

At this point I don’t think I should publish this as an EIP, because my main hypothesis has failed. But I see potential in the M-to-1 use case, especially as a bridge to other L2 solutions where people have to first deposit their funds to a constant address (this is where batched meta txs might come useful).

Eager to hear your opinions! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**matt** (2020-09-20):

Thanks for doing this analysis, [@cmango](/u/cmango). In your tests, did the meta-nonce start at zero or some non-zero integer?

---

**cmango** (2020-09-21):

Well, AFAIK the mapping automatically “sets” nonce to 0 for all possible addresses. When the first meta transaction (for a sender) is completed, the nonce is set to 1.

In my M-to-M gas tests each sender only sends one meta transaction, and I think the first transaction is always the most expensive. So yeah, I could probably do another test where a sender already had made one meta tx (and the nonce is set to 1), and then test how much the second meta tx would cost.

Did you had that in mind or something else?

---

**matt** (2020-09-21):

IMO, updating a non-zero nonce is the most practical scenario (15k less gas per meta-tx) and will not fail your hypothesis.

---

**cmango** (2020-09-22):

Hmmm… Perhaps I could separate gas usage for a 1st meta transaction (of a sender) from gas usage of subsequent meta txs of the same sender…

Practically, a relayer could charge the first-time senders (senders with a zero nonce) more than others, and not average it out (it’s hard to know in advance what the average of a batch would be anyway).

I’ll redo the README and the results to account that.

---

**matt** (2020-09-22):

> Practically, a relayer could charge the first-time senders (senders with a zero nonce) more than others, and not average it out

This is line with how Ethereum handles `CALL` and `SELFDESTRUCT` to new accounts, they are more expensive.

---

**cmango** (2020-09-22):

Hey, just an update: I conducted another test (Test #8) where senders have a non-zero meta nonce value and receivers have a prior non-zero token balance.

In this case the gas usage per meta tx drops quite significantly, to around 27’000 gas/meta tx, which is almost 50% less than a normal on-chain token transfer (51’000 gas).

I guess now I could proceed with issuing an EIP, right? I’m open to hear different opinions on this ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**matt** (2020-09-23):

That sounds like the proper next step!

---

**cmango** (2020-09-23):

I just thought of another thing to consider ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Currently, my benchmark is an ERC-20 token transfer that costs 51’000 gas. This is in case the recipient hasn’t held token balance before.

If the recipient has a prior token balance, the gas cost is 36’000 gas (15’000 less gas).

So a meta transaction in Test #8 (from a sender with non-zero nonce, to a receiver with non-zero prior balance) shouldn’t be compared to 51’000 benchmark, but instead to 36’000 gas benchmark.

The Test #8 result is still lower than the benchmark (27’000 gas vs 36’000), but not that significantly anymore.

---

**cmango** (2020-09-25):

The EIP-3005 has been published now, comments are welcome either on the PR page or on Ethereum Magicians: https://github.com/ethereum/EIPs/pull/3005 ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=9)

---

**jpitts** (2020-09-27):

Congrats!

Once the proposal has a number it is a good idea to create a new topic w/ EIP-XXXX in the title, and we can link back to this “primordial soup” discussion.

---

**cmango** (2020-09-27):

Thanks, Jamie! I’ve opened a new topic here: [EIP-3005: The economic viability of batched meta transactions](https://ethereum-magicians.org/t/eip-3005-the-economic-viability-of-batched-meta-transactions/4673)

