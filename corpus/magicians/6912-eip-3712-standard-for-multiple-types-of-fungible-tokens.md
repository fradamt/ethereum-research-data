---
source: magicians
topic_id: 6912
title: "Eip-3712: Standard for Multiple Types of Fungible-Tokens"
author: "1999321"
date: "2021-08-20"
category: EIPs
tags: [smart-contracts]
url: https://ethereum-magicians.org/t/eip-3712-standard-for-multiple-types-of-fungible-tokens/6912
views: 1436
likes: 2
posts_count: 6
---

# Eip-3712: Standard for Multiple Types of Fungible-Tokens

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3712)














####


      `master` ← `naturaldao:Eip-Branch`




          opened 10:57AM - 10 Aug 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a51e9d9399c657d18b06178ba6476725cd045714.png)
            1999321](https://github.com/1999321)



          [+337
            -0](https://github.com/ethereum/EIPs/pull/3712/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/3712)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

You can find it from :
- https://github.com/naturaldao/EIPs/blob/Eip-Branch/EIPS/eip-3712.md

## Replies

**SamWilsn** (2022-03-07):

A couple questions whose answers I think should be added to the EIP specification section:

- If one of the batch transfers fails, what happens to the rest of the transfers?
- What does the boolean return value of the transfer family of functions mean?

---

**1999321** (2022-03-11):

Thank you very much for your question. If one of the batch transfers fails, the rest of the transfers will be in error and this transation will fail too. the boolean return value of the transfer family of functions means whether all transfers are success.

---

**SamWilsn** (2022-03-11):

That makes sense! I’d recommend adding that to the EIP itself, since it seems pretty important.

---

**zhous** (2022-03-12):

Great questions and suggestion, Sam! Yes, it is very important!

After several discussions, we’ve arranged this work on the schedule.

Thank you very much!

---

**zhous** (2022-05-01):

We’ve recently modified EIP-3712, and also have published a Chinese version (only for explanation).

And we’re also managing this EIP with versions:

https://github.com/naturaldao/EIP3712

