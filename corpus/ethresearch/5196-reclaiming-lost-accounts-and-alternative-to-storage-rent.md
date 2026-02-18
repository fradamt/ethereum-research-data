---
source: ethresearch
topic_id: 5196
title: Reclaiming lost accounts and alternative to storage rent
author: bobbinth
date: "2019-03-22"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/reclaiming-lost-accounts-and-alternative-to-storage-rent/5196
views: 2081
likes: 4
posts_count: 8
---

# Reclaiming lost accounts and alternative to storage rent

### Basic idea

For an average person, the finality of crypto is perhaps one of the more scary things. If you lose your account keys, your money is gone forever. Similarly, if you mistakenly send money to a wrong address, there is no way to get it back. Yes, it is one’s personal responsibility to protect themselves against such woes - but people are people, and everybody makes mistakes.

There are some solutions that try to prevent such problems at a wallet level, but there could be a mechanism that can prevent them at the base protocol level as well. Here is how it could work:

1. You can submit a claim against any account and provide a new public key as a part of the claim.
2. If your claim is successful, the account is destroyed, and all money (and other data) stored in the account is moved to the new key you provided.

This idea is not intended for any specific blockchain - it’s more theoretical at this point.

### More detailed explanation

To prevent the above mechanism from being abused, we need to put some safeguards in place:

1. When you submit a claim, you must “stake” some funds together with it. The required funds could be proportional to the account’s balance (e.g. 5% - 10%).
a. If your claim is successful, these funds are returned to you,
b. But if your claim fails, you lose the staked funds (they are “burned”).
2. The claim is recorded in the blockchain - so, everyone can see which accounts have claims submitted against them.
3. If a long time (e.g. 12 months) passes after a claim is submitted against an account, and the account still shows no activity, the claim succeeds.
a. But, if the account’s owner executes a transaction against it (something that requires usage of the account’s private key), the claim fails immediately.

### Example

Let’s say I had an equivalent of $10,000 in an account and I lost the key. I would submit a claim against the account and stake $500 (5% of balance) together with it. Since nobody else has the key I lost, nobody would be able to cancel my claim. My claim would mature in 12 months, and I would receive $10,500 under the new key I provided with the claim. Yes, it would take me a year to get the money back - but it’s much better than losing it forever.

Just as I can submit a claim against my account, so can anybody else - but they are unlikely to do so. This is because I can very easily cancel their claim against my account. All I need to do is execute a transaction that proves that I still have the private key, and they’d be out of $500. So, unless you are absolutely sure that an account’s owner is not able to use their private key, you would not want to submit claims against their account.

### Alternative to rent

The above mechanism can be adjusted to achieve goals similar to “storage rent”. Specifically:

1. Remove accounts that users forget/stop caring about from the sate.
2. Impose small costs on accounts that consume state storage.

To achieve the first goal, no significant changes to the “claiming” mechanism are needed. Since anyone can submit a claim against any account, people could monitor accounts and submit claims against accounts that they believe are stale.

For example, if an account hasn’t had any activity for months and has a very low balance (e.g. within 10x of current average transaction fee), it is very likely that the owner has abandoned the account. If I’m right, I could make a little money by submitting a claim against this account. If I’m wrong, I would lose an amount roughly equivalent to a transaction fee.

We can incentivize this behavior more explicitly like so:

If an account hasn’t had any activity for extended period of time (e.g. 3 months), and if the balance held in the account is lower than 10x (or 20x etc.) of the average transaction fee, a claim submitted against the account succeeds immediately. (no need to wait for a year for a claim to mature).

The average fee can be calculated as an average over the last 6 months to reduce volatility. It also can be calculated on per-byte basis, so that accounts consuming more storage would have to hold more funds to avoid being claimed by others. This would also naturally impose higher costs on accounts that consume more storage (goal #2).

## Replies

**MaverickChow** (2019-03-23):

If a criminal knows a person to be holding a lot of crypto in a specific account, what is there to stop this criminal from murdering this person in secret, and then make a claim for his account?

I slowly come to believe:

1. The complicated UX may need to stay; it has its own major advantages that come with being complicated.
2. The people that wants to own crypto should make a hard decision once and for all to get educated and take responsibility for themselves instead of expecting everything to be easy for them, just the same as people that decide to be traders (for money’s sake) made up their mind to get complicated by studying technical analysis and even beyond. So no excuse for owning and securing crypto too.

---

**bobbinth** (2019-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> If a criminal knows a person to be holding a lot of crypto in a specific account, what is there to stop this criminal from murdering this person in secret, and then make a claim for his account?

I don’t think the risk here is any higher than the following scenario:

If a criminal knows a person to be holding a lot of crypto in a specific account, what is there to stop this criminal from kidnapping this person (or their loved ones), and torturing them until the person gives up their keys?

---

**MaverickChow** (2019-03-23):

The risk in both scenarios is no different from the risk in having lots of fiat money too. A person that is publicly known to have lots of fiats cannot expect to walk freely on the street without the risk of getting mugged or kidnapped. When it comes to money, every human is a gremlin. That is why privacy feature is important for crypto. I would think of ways to freeze stolen accounts than ways to make the average users get by being less responsible with their keys by having easy solutions, one of which as you suggested that may also give rise to new problems, i.e. criminals murdering someone and make false claim for his fat account.

If a person cannot prevent a criminal from torturing him in giving up his key, then he cannot also prevent a criminal from murdering him and making false claim of his account. In fact, there is no real solution to such risk other than doing our best to stay safe as much as possible. Otherwise, a solution that can be applied to crypto can also be applied to fiat as well.

And just because a person has no solution to prevent getting tortured into giving up his keys does not mean he should support a solution that may also risk getting him killed as well. Best action is to go back to the drawing board and think of a much better solution.

---

**bobbinth** (2019-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> The risk in both scenarios is no different from the risk in having lots of fiat money too.

Absolutely. If someone knows you have access to lots of money, and they have aptitude and ability to do you harm, your money is not safe. Doesn’t really matter whether its fiat or crypto, or whether you can reclaim lost accounts or not. But that’s not the problem I’m trying to solve.

As far as I can tell, there is no additional security risk imposed by the mechanism I described in the OP (and based on your quote, you seem to agree?). And there are huge benefits for people who lose access to their keys for one reason or another.

In general, one must have a very good reason to justify poor UX. Think about it this way: your email provider does not need to offer password recovery procedure. They could say that if you lost/forgot your password, you’ll never be able to use the same email address ever again. But that’s poor UX, and if your goal is for average people to use your service, providing password reset/recovery services is very good idea.

---

**marckr** (2019-03-24):

The original problem for this with cryptography was Yao’s Millionaire problem, afaik.

Perhaps all that needs to be compared are ordinal values, so whether a sum is greater or less than another, there is still a means to compare them. May be off on my own direction here, however.

---

**bobbinth** (2019-03-26):

After some thinking, I realized that the “claiming” mechanism could be used as an alternative to “storage rent”. I’ve updated the post with the new section to describe this.

---

**jfdelgad** (2019-03-29):

I think this is important, and although I would also like to see people taking control of their keys and funds directly, is unlikely that this will happen any soon or ever. On the contrary not offering mechanisms that make users more confortable with blockchain is likely to keep then away and delay mass adoption.

I wonder if some of these aspects can not be managed by smart contracts. Having funds or tokens in a contract wallet rather than a EOA make possible things like set several EOAs as valid user such that if one is lost, the others can be used to move funds, set emergency mechanisms like saving a hashed password that then can be used put in motion a time-lock on the contract, etc.

