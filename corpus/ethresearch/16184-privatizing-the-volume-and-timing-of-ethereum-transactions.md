---
source: ethresearch
topic_id: 16184
title: Privatizing the Volume and Timing of Ethereum Transactions
author: trevormil
date: "2023-07-25"
category: Privacy
tags: []
url: https://ethresear.ch/t/privatizing-the-volume-and-timing-of-ethereum-transactions/16184
views: 2087
likes: 13
posts_count: 11
---

# Privatizing the Volume and Timing of Ethereum Transactions

In this post, I share my paper VTBC on privatizing the volume and timing of blockchain transactions (with an implementation using Ethereum). Full paper can be found [here](https://github.com/trevormil/privatizing-blockchain-timestamps/blob/98c5265d4686279faed362c8781e150e41de1516/VTBC_preprint.pdf). It has been accepted to [ICCCN 2023](http://www.icccn.org/icccn23/index.html) in July.

**Problem:** Existing privacy-preserving blockchain solutions can maintain confidentiality and anonymity; however, they cannot privatize the volume and timing of transactions for an application. This is problematic for volume-dependent or time-dependent applications, such as a Dutch auction where everything is priced at $10 on day 1, $5 on day 2, etc (time-dependent), and there are only 10 items for sale (volume-dependent).

Such an auction cannot be implemented currently on blockchains in a privacy-preserving manner because volume and timing metadata for an applications’ transactions is always leaked due to core blockchain architecture. This means it will always leak information like number of sales, bids, the sellers’ revenue, etc. which all may want or need to be privatized in many situations.

Or, think of a grading policy for student assignments which is time-dependent and volume-dependent. For example, students can submit late for a 10% penalty and/or submit multiple times for a 10% penalty. Currently, the public volume and timing metadata can be used to deduce information about the students’ grades, even if all submissions are anonymous and confidential.

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/eea3f4e0817915bf2c4b0a6f2911120fe8a59e74_2_690x184.png)image2146×574 47.2 KB](https://ethresear.ch/uploads/default/eea3f4e0817915bf2c4b0a6f2911120fe8a59e74)

**Solution**: The solution proposed in this paper is to build on top of existing privacy-preserving solutions (zkSNARKs, the Hawk paper’s model) and create applications which support decoy, no-op transactions. Decoy transactions are simply no-op transactions that do not contribute to the outcome of the application but are used to obfuscate the overall volume and timing dataset because they are indistinguishable from “real” transactions.

For example, if we have a student exam deadline where exams can be late or on-time, students can obfuscate the volume and timing of their submission by submitting one real and one decoy submission on either side of the deadline. The grading function will take in both submissions but never leak which one was real and which was fake.

For enforcing adequate obfuscation of the volume and timing metadata, we show that applications can define K time periods that correspond to all possible outcomes and enforce that all users must submit >1 transaction during each of the K time periods, or else, they are “disqualified”. If transactions are submitted outside the time period, those transactions are ignored. These rules help to maintain that sufficient noise is added to not leak any useful information to adversaries.

In the paper, we propose a solution based on the Hawk multi-party privacy-preserving blockchain application model which uses a minimally trusted manager to help facilitate the application.  The manager is trusted for maintaining privacy; however, **they are not trusted for correctness of execution**. They are not to be equated with a trusted third party. The correctness of execution can be publicly verified by anyone to be fair and honest (due to the properties of zkSNARKs and using the blockchain as the trusted timekeeper).

**Results:** We evaluated our method via an Ethereum private blockchain and tested with up to N=128 inputs / transactions. We found that our proposed method is implementable and deployable on a blockchain such as Ethereum but can add significant overhead (especially as N or the number of decoy transactions increases). Libraries (contracts) can exceed 160 KB in size, and transactions can exceed 12m gas (30m limit per block).

We believe that, over time, our approach will continue to become more scalable and reasonable for a public blockchain like Ethereum (as zkSNARKs and blockchain scalability continue to improve). For now, our solution is suitable to private or permissioned blockchain environments, where resources are not as scarce.

Feel free to ask any questions below!

## Replies

**baddee** (2024-01-05):

all users must submit >1 transaction during each of the K time periods, does this mean that a user must submit more than 2 transactions per transaction? Then how can we determine which transaction is the real one? And which transaction is a fake transaction?

---

**trevormil** (2024-01-06):

Not sure I understand what you mean “more than 2 transactions per transaction”.

There are K time periods (each user must submit a minimum one transaction (real or decoy) within each of the K time periods). At the end, in the computation phase, we use zero knowledge proofs to verifiably prove the outcome was legit without ever revealing whether any transaction is real or decoy.

---

**Pfed-prog** (2024-01-07):

Very interesting premise and paper

Did you consider data obfuscation by forcing users to submit always the same total amount of tx each K period.

So for example, during K_1 we have 150 txs , K_2 - 150 txs and K_t also 150 txs.

In addition, I think [@baddee](/u/baddee) was really looking to learn on whether a third party could read the transactions and get the data in another way.

I believe that the tx might still contain the data regarding whether the tx is noop or not

---

**trevormil** (2024-01-08):

Yea, we did consider enforcing all users submit **exactly** 1 tx during each time period. That is totally possible solution, but we ultimately decided against it it for a couple reasons:

- It leaks exact amount of users for the application (e.g. 150 txs per period = 150 users). When keeping it >=1 tx, there could theoretically be 1-150 possible users for an application which has 150 txs per time period. The number of users could be valuable in an auction, for example, where bidders correlate to demand / final sale price.
- The >=1 approach also lends itself nicely to posting decoys on behalf of other users (e.g. a teacher submitting decoys to obfuscate their students’ submissions). This wouldn’t be the same user submitting the txs.
- The reason we have each time period being as short as possible is to prevent pattern analysis (analyzing the time and volume to deduce whether any tx is a noop or not). For example, real ones may be more likely to be submitted closer to a deadline (e.g. students procrastinating). The more txs there are, pattern analysis becomes less feasible.

Yea, agreed that for a completely brute forced solution and a perfect timing / volume dataset, all you would need is 1 tx per user all submitted during all K carefully selected time periods. However, the properties above wouldn’t hold. We just ultimately went for the approach of the more obfuscation, the better. But yea, different applications will have different requirements and can set the parameters based on the properties they desire.

The transaction contents are all only stored after being encrypted on-chain. Thus, to be able to determine if any one transaction is a no-op, you would have to break a decryption (assuming all trust assumptions in the models holds and the plaintext is not leaked in any way). In my opinion, I think the weak point is the manager. They decrypt in plaintext during the computation phase in order to generate the computation ZKP. So, social engineering is the most likely way for a malicious party to obtain useful information, in my opinion.

I would love to see a way that it could be done fully without a minimally trusted manager decrypting and seeing the plaintexts, but we ultimately opted for this method because zkSNARKs are pretty universal and can be used for many applications (as its basically supports a whole programming language) rather than other methods (FHE, sMPC, etc) which are more limited in their scope of applications.

---

**lottewi** (2024-01-13):

Is the decoy transactions also required to be provided by the user? I thought it was automatically generated by the system. Another problem is that if there are too many decoy transactions it will take up a lot of space and gas, and if there are too fewdecoy transactions, it will not be easy to create the purpose of mixing. What I said may not be right, just for reference.

---

**trevormil** (2024-01-13):

Yes, you are right. That is the most difficult tradeoff to consider and get a solution for. On one hand, you need enough decoys to obfuscate everything. However, too many will bloat the blockchain with decoys.

We personally believe the decoy approach is the only way to solve this issue because by nature of the core architecture of blockchains, volume and timing of transactions must be known to achieve consensus. So if it must be known, the only way to privatize this metadata for volume or time dependent applications is through an approach that assumes all such metadata is public (which is where we came up with the decoy approach).

Within the paper, we are pretty transparent about how much gas the whole application takes up (spoiler alert: it is a lot). We hope that with other advancements (zero knowledge proofs getting better, blockchains gaining scalability, etc) that this will become more feasible in practice. I also had little experience with zero knowledge development before, so there could very well be low-hanging optimizations as well.

There are a couple approaches we considered with regards to who submits the decoy transactions.

1. Users submit >= 1 transactions (could be real or decoy) in all of K time periods preselected by the application. If they fail to do so, they are disqualified from the application.
2. Another entity could generate the decoys (e.g. a teacher obfuscating on behalf of the students).

We ultimately went with approach 1 because the absolute worst outcome is to leak privacy for such applications because that was our whole goal. With approach 1, there are incentives to post decoys (disqualification) and you are guaranteed a minimum amount of noise (U users * >=1 transaction per K time periods = a minimum of U * K transactions). Approach 2 is a valid solution, as long as sufficient noise is generated, but it lacks the incentive and minimum baseline.

---

**edenore** (2024-01-15):

Is it possible to consider this: provide users with the option of submitting a decoy transaction, and use the decoy transaction if they need privacy protection, or not use the decoy transaction if they don’t need it. Since the object of privacy protection is ultimately the user himself, would it not be more scientific to let the user choose whether to submit a decoy transaction or not? And this would also reduce congestion and gas.

---

**brigge** (2024-01-15):

This is indeed an interesting idea, but a large number of mixed transactions are flooding the chain, in other words, you can also say that a large number of garbage stays on the chain, so that although it can bring some effect on privacy protection to a certain extent (only a part of the effect, rather than complete privacy protection (because the normal transactions are also on the chain), but the burden is also relatively high, increasing the garbage transactions, and also increasing the GAS fees. Be that as it may, it’s a good thought!

---

**trevormil** (2024-01-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/edenore/48/14727_2.png) edenore:

> Since the object of privacy protection is ultimately the user himself, would it not be more scientific to let the user choose whether to submit a decoy transaction or not?

Yes, a lot of functionality can be implemented on an application-specific basis. So in your example, this is a valid solution if the application lends itself nicely to this idea.

However, our paper focused on preserved **anonymity** of users as well (i.e. no two transactions could be linked to being from the same user). We not only achieved volume and timing privacy but also implemented a fully privacy preserving application (e.g. anonymous and confidential student exam submissions). So in our cases, we were not just trying to protect the privacy for individual users if they wanted privacy. We needed to protect the volume and timing privacy of the dataset of ALL transactions because volume and timing analysis can still be performed on the overall dataset to learn confidential information (even if transactions are anonymous and could not be distinguished to be either real or decoy). Our paper focused on maintaining the volume and timing privacy for the whole application.

For example, lets say we have a student exam deadline at T1 for a class of 10 students and there is a penalty for submitting late. If we observe that only 1 transaction was submitted before T1, we know that 9 out of 10 submitted late. This would leak privacy or valuable information about the **entire class**.

It is all about finding the right balance, and a lot can be adapted and optimized to suit specific application requirements.

---

**trevormil** (2024-01-15):

Totally agree. It is not an optimal solution in terms of resources and bloating the chain. However, because of the core architecture of blockchains (and having volume and timing metadata public), I do not think another solution is possible. My hope is that blockchain scalability and zero knowledge advancements will make this a feasible solution. For now, I think it can be used in more private blockchain settings (where scalability isn’t too much of a concern).

Note: I disagree on the “it only brings some privacy”. Even though the “real” transactions are still on-chain, full privacy is still maintained with a well designed application.

