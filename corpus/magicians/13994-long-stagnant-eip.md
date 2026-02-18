---
source: magicians
topic_id: 13994
title: Long stagnant EIP
author: RenanSouza2
date: "2023-04-26"
category: Magicians > Process Improvement
tags: [eip-editors]
url: https://ethereum-magicians.org/t/long-stagnant-eip/13994
views: 685
likes: 7
posts_count: 6
---

# Long stagnant EIP

Hey everyone

Has there been a discussion on what to do with EIPs that are stagnant for a long period?

What if after a given time an EIP migrates from ‘stagnant’ to 'withdrawn’or even a new state?

What are you opinions on this?

## Replies

**abcoathup** (2023-04-27):

I see `withdrawn` as the authors have explicitly decided to withdraw the EIP/ERC, so wouldn’t want to see it reused for abandoned EIP/ERCs.

`abandoned` could be an automated state after say 6 months of being `stagnant` but I am not sure if there is a need.

---

**RenanSouza2** (2023-04-27):

I was reading some of the stagnant EIPs and some of them don’t even make sense anymore by either being surpassed by another EIP or porposing something no longer relevant.

So I wondered what of those EIPs could still be revived and if there was a better way of classifying them.

About the `abandoned` state, maybe we can change EIP-1 flux so a `stagnant` EIP that was in review state can return to review state but an `abandoned` one has to return to `draft`

Do you think those changes are relevant? The last thing I wanna do is increase the amount of work to the editors

---

**abcoathup** (2023-04-28):

`stagnant` is a catch all, I am not sure there is a need for additional states.  See if any EIP editors chime in.

---

**RenanSouza2** (2023-04-28):

Makes sense, it doesn’t need to classify what stagnant EIPs are more likely to return because the stagnant itself does that.

Adding another state would not add anything to the process

---

**poojaranjan** (2023-05-03):

An EIP can be resurrected from `Stagnant`. It can go back to the last status it was in. If the proposal does not make sense after coming back to active status,  it can’t be promoted anymore. The author may move it to `Withdrawn` or let the proposal live in `Stagnant` status forever.

Just a note `Abandoned` isn’t a valid status anymore as per [EIP-1](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md#eip-process).

