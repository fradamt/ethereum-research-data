---
source: magicians
topic_id: 9079
title: How do EIP numbers get assigned?
author: PaulRBerg
date: "2022-04-28"
category: EIPs
tags: [eip-editors]
url: https://ethereum-magicians.org/t/how-do-eip-numbers-get-assigned/9079
views: 1933
likes: 11
posts_count: 6
---

# How do EIP numbers get assigned?

I’ve read the the [EIPs](https://eips.ethereum.org/) home page and [EIP-1](https://eips.ethereum.org/EIPS/eip-1) but I’m still not 100% sure how EIP numbers get assigned.

EIP-1 says this:

> Once the EIP is ready for the repository, the EIP editor will:
>
>
> Assign an EIP number (generally the PR number, but the decision is with the editors)
> …

So am I correct to assume that is up to the *EIP editors*, who oftentimes are different from the *EIP authors*, to assign a number to an EIP?

If yes, and they do not want to use the PR or the issue number, is it common practice to increment the number used in the last EIP, or do they sometimes skip some values for brevity reasons (e.g. EIP-5500 is easier to remember than EIP-5497)?

Here’s why I find this confusing. There currently exist two proposals in which the authors seem to have assigned whatever numbers they wanted:

- EIP-5555
- EIP-9000

This is in spite of the fact that the latest PR number on GitHub is 5045:

[![GitHub EIPs repo](https://ethereum-magicians.org/uploads/default/original/2X/9/9398b65847af541faec185ecb94f026f3937025d.png)](https://i.stack.imgur.com/wxIZw.png)

My guess is that these proposals haven’t been vetted yet by EIPs editors - but I want to make sure that my guess is correct.

## Replies

**matt** (2022-04-28):

Your guess is correct. Unfortunately we don’t control what people *claim* their EIP numbers to be.

---

**alxi** (2022-04-29):

But the claimed EIP is over-written by the editors correct?

---

**poojaranjan** (2022-05-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/paulrberg/48/5860_2.png) PaulRBerg:

> So am I correct to assume that is up to the EIP editors, who oftentimes are different from the EIP authors, to assign a number to an EIP?

As per the current process, an EIP number has to be assigned by EIP editor(s).

Usually it is the first Pull Request (or Issue, in some cases) for that proposal on [EIP GitHub](https://github.com/ethereum/EIPs). We are strongly recommending discussion-to at [FEM](https://ethereum-magicians.org/), hence authors are suggested to create a pull request with the proposal and most likely that pull request number is going to be the EIP number.

In rare cases where EIP editors observe one/many spam pull requests or issues in the repo followed by a proposal on an attractive number like EIP-5555, EIP editors veto and allocate another unused number.

> Here’s why I find this confusing. There currently exist two proposals in which the authors seem to have assigned whatever numbers they wanted:
>
>
> EIP-5555
> EIP-9000
>
>
> This is in spite of the fact that the latest PR number on GitHub is 5045:

I understand this can be confusing, looking at a discussion thread with already assigned number without the `Draft` in pull request.

We can not control what an author chooses to create a FEM thread for vetting the proposal, rest assured, at the time when added as a pull request `Draft`, chances are that EIP authors will allocate the EIP number which may be different than whatever shared earlier. As a team working on process improvement, we can educate people to follow good practices and self allocating an EIP number of own choice is certainly not a good one.

---

**high_byte** (2022-05-22):

I propose EIP-10000: use clear descriptive titles in EIP proposals rather than numbers. e.g. this proposal could be EIP-Descriptive-EIPs

---

**triddlelover69** (2022-05-24):

It is a very useful and educational thread on how EIP numbers get assigned. I have learned a lot.

