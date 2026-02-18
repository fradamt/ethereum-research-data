---
source: ethresearch
topic_id: 19220
title: Charity Bond Account Generation for Social Networks and More
author: MicahZoltu
date: "2024-04-07"
category: Economics
tags: []
url: https://ethresear.ch/t/charity-bond-account-generation-for-social-networks-and-more/19220
views: 1139
likes: 4
posts_count: 2
---

# Charity Bond Account Generation for Social Networks and More

Also blogged here: [Charity Bond Account Generation for Social Networks and More | Micah Zoltu](https://listed.to/authors/33689/posts/50805)

Musical rendition of this concept also available: [Charity Bond Account Creation - Boy Band.mp3](https://bafybeibbfboye32palpogfpfqj7fzdiy7zqk4oq3aywf2qyis2by4ri3yq.ipfs.zoltu.io)

## Abstract

A system for limiting account generation and stopping spam in systems with a moderation system in place.

## Motivation

Most successful online social networks have a problem with spammers.  Spammers are able to create many accounts and then spam with them.  These accounts inevitably get banned, but often not before the damage is done.  Online social networks want to make account generation free, because network effects dominate their success which means they can’t just charge people to create an account.

## Solution

1. Provider creates a list of charities:  The provider creates a list of charities that they consider legitimate.  This list should be as comprehensive as possible and is not meant to reflect the values of the provider, but rather provide a list of “probably not scam” charities.  All of the charities should be able to accept donations in the form of a crypto-currency that is available on a blockchain that supports contracts.
2. User selects a charity:  When a user begins the account creation process, they choose one of the charities that the provider has included in its list.  The user should choose a charity they feel is legitimate, and one that they wouldn’t mind donating to.
3. User pays a bond:  After selecting a charity, the user places a bond that is of meaningful size.  This doesn’t need to be prohibitive, but it does need to be significant.  $5 (at today’s value) is perhaps a proper order of magnitude.
4. User’s bond is put into a contract that either returns to user or pays the charity:  The users bond does not go to the provider.  It is put into a contract where the provider can only do one of two things with it: (A) Return it to the user or (B) forward it to the charity selected by the user.  The contract associates the bond with the user account identifier on the provider’s platform.
5. If the user closes their account voluntarily, they get the bond back:  When a user terminates their account with the provider, their bond is returned to them after a reasonable timeout (days).
6. If the user’s account is closed by the provider for spamming, the bond goes to the charity:  If a user is caught spamming, their account is closed but they do not get their bond back.  Instead, the bond is forwarded to the charity the user selected.

## Rationale

- The bond ensures that spammers will have to pay a significant fee for each spam account they create.
- The bond is given to a charity rather than the provider when the user spams to ensure there is no direct financial incentive for the provider to close accounts as a source of revenue.
- The bond is given back to the user rather than the charity on voluntary account closure to maintain a “0 cost” (exception: time value of money) account creation process.
- The charity list is created by the provider to ensure that users cannot designate a scam charity that just gives them their money back.
- The specific charity is selected by the user to ensure that if the account is closed inappropriately or the provider is otherwise malicious, there is a silver lining for the user in that a charity they like received a small donation.
- There is a timeout after account closure before refunding the user to prevent users from spamming and then immediately closing their account before getting caught.

## Remarks

This mechanism can be used for any system that is susceptible to spam and has an existing system in place for closing spammer accounts.  Social networks are the obvious top choice, but one could also imagine something akin to CloudFlare’s captcha-replacement token, where users can pay a bond to acquire a token and if their token is used as part of a spam attack, their bond goes to charity.

This system also is remarkably resilient to some degree of false positives.  With a sufficiently large charity list, even when a user gets caught up in a mass ban, they may not feel that bad since their bond just went to a charity of their choice anyway.  This is in stark contrast to when traditionally paid user accounts get caught in a mass ban because the people doing the banning were financially rewarded for getting it wrong, which feels very bad for the user.  A user whose bond went to charity may simply shrug and create another account, writing off the bond loss as a charitable donation that they would/should have done anyway.

## Replies

**MicahZoltu** (2024-04-08):

For those who prefer music to prose text, a musical rendition of this concept can be found at [Charity Bond Account Creation - Boy Band.mp3](https://bafybeibbfboye32palpogfpfqj7fzdiy7zqk4oq3aywf2qyis2by4ri3yq.ipfs.zoltu.io)

