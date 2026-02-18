---
source: ethresearch
topic_id: 6034
title: Login with Semaphore Authenticate
author: barryWhiteHat
date: "2019-08-26"
category: Privacy
tags: [authentication]
url: https://ethresear.ch/t/login-with-semaphore-authenticate/6034
views: 3245
likes: 5
posts_count: 11
---

# Login with Semaphore Authenticate

Thanks to Wei Jie Koh for review and feedback

## Intro

There has been a lot of interest recently in creating a “Login with Ethereum” button. This seems like a reasonable thing to do. However it does link your login to your transaction history. This can be mitigated with a [mixer](https://hackmd.io/qlKORn5MSOes1WtsEznu_g#) or using an account with zero funds.

Previuosly use of zk-SNARKS have been focused on cryptocurrency transactions. Here we propose the applications of zk-SNARKS to universal login. Using the same circuit we use in Semaphore, we allow members of a group to login to a service without revealing which member they are.

## Note on statefulness

This is directly applicable to stateless applications, where each user does not have a personal state, such as for VPNs. Email, by contrast, is an example of a stateful application. Stateful dApps can also be supported where all of a user’s information is encrypted and anyone who logs in can requires random peices of information which only a legitimate user can decrypt.

## Semaphore Basics

Please see https://github.com/kobigurk/semaphore for introduction

## Semaphore Anon Login

The authenticator creates a list of public keys that it will accept as logins. It then publishes this list and shares the merkle proofs with the users.

Here we need to set the `external_nullifier` so that double logins are not possible.

If we set `external_nullifier` equal `hash("ANONLOGIN" + URL)` of the website this will allow give each login a uniqe nullifier which should not reaveal any information about the users.

## Many Requests Per Site

We can also support multiple requests to a single site. This is useful with VPN logins or sites that require stronger limits on what users can do.

The VPN provider only wants to accept a limited number of logins from every user their for they only accept semaphore proofs with

1. external_nullifer == hash("ANONLOGIN", URL, day_count , ticket_number
2. signal == hash(target_host_pub_key, cookie) target_host_pub_key prevents replay attacks and cookie is the credentail that is used for the rest of this session.

where `day_count` is the number of days since January 1st, 1970 at UTC

and `ticket_number` is any number more than 0 and less than `max_ticket_number`

You can see that each day each user can have a maximum of `max_ticket_number - 1` signals that have uiniqe nullifiers for each URL. Thus the authenticator knows that the total number of connections they need to serve is bounded and they can limit the bandwidth of each connection.

## Group Creation

The creation of these groups is still an open problem. Besides centralised mechanisms, we can employ decentralised mechanisms such as:

1. Burning ETH to impose an econmoic cost of account creation.
2. Charging a fee to join the group and pay this fee to the infrastucture provider.
3. Uniqueness DAO: https://www.humanitydao.org
4. Individuality party, where we hold an global party and users participate to join the group.

## Conclusion

Here we describe a login mechanism that allows users to authenticated by an authenticator without reavealing which account they are using.

This allows us to use stronger proofs of individuality and still maintain privacy. The creations of these groups is an open problem and not addressed here.

## Replies

**weijiekoh** (2019-08-31):

For the VPN use case, it looks like `day_count` and `ticket_number` serve to limit the number of connections per day. However, this means that the `external_nullifier` will have to change all the time, since:

```auto
external_nullifer == hash("ANONLOGIN", URL, day_count , ticket_number)
```

This hash will be different for each day and `ticket_number`. Maybe I’m misreading this proposal, but since Semaphore only holds one `external_nullifier` in storage at a time, how does it support multiple requests?

---

**weijiekoh** (2019-08-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> If we set external_nullifier equal hash("ANONLOGIN" + URL) of the website this will allow give each login a uniqe nullifier which should not reaveal any information about the users.

For the simple example of anonymous login (non-VPN), I see that the external nullifier is the hash of the URL, but what should the signal be?

Can it be something like the hash of a cookie or hash of a JWT token which the user can subsequently use to authenticate with the service?

---

**weijiekoh** (2019-09-01):

It seems that the assumption that these services are stateless poses a challenge. Many VPN services are subscription-based (e.g. $60 per year) so each account has a state (e.g. the user’s registration date) and won’t work after the year has elapsed unless the state is updated (e.g. by setting an account renewal date).

---

**barryWhiteHat** (2019-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/weijiekoh/48/3691_2.png) weijiekoh:

> This hash will be different for each day and ticket_number . Maybe I’m misreading this proposal, but since Semaphore only holds one external_nullifier in storage at a time, how does it support multiple requests?

We would change Semaphore to support multiple external nullifiers.

---

**barryWhiteHat** (2019-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/weijiekoh/48/3691_2.png) weijiekoh:

> For the simple example of anonymous login (non-VPN), I see that the external nullifier is the hash of the URL, but what should the signal be?

It should be the recipient of the signal. This is to prevent replay attacks. It can also include the cookie they are trying to activate.

---

**barryWhiteHat** (2019-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/weijiekoh/48/3691_2.png) weijiekoh:

> It seems that the assumption that these services are stateless poses a challenge. Many VPN services are subscription-based (e.g. $60 per year) so each account has a state (e.g. the user’s registration date) and won’t work after the year has elapsed unless the state is updated (e.g. by setting an account renewal date).

So you let people join the group at any time and just reduce the cost that people need to pay. For example lets say we run a VPN service and people can join once a month and pay 2 eth. You want to join 2 weeks into the service so you only need to pay 1 eth as half of the time has already passed.

---

**weijiekoh** (2019-09-01):

Is the recipient of the signal `target_host_pub_key`? Why not just a nonce?

---

**weijiekoh** (2019-09-01):

How should the system know if a user has an expired account in zero-knowledge?

---

**barryWhiteHat** (2019-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> So you let people join the group at any time and just reduce the cost that people need to pay. For example lets say we run a VPN service and people can join once a month and pay 2 eth. You want to join 2 weeks into the service so you only need to pay 1 eth as half of the time has already passed.

At the end of 1 month all accounts are expired.

---

**barryWhiteHat** (2019-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/weijiekoh/48/3691_2.png) weijiekoh:

> Is the recipient of the signal target_host_pub_key ? Why not just a nonce?

If its just a nonce a host can reply my signal to other hosts and it will appear legitimate. This will probably not be a problem because an attacker would need my cookie to login. But its still a dos attack.

