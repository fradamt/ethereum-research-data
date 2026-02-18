---
source: magicians
topic_id: 20080
title: "ERC-7717: Deterministic AA wallet"
author: jaehunkim
date: "2024-05-22"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7717-deterministic-aa-wallet/20080
views: 1359
likes: 6
posts_count: 11
---

# ERC-7717: Deterministic AA wallet

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/453)














####


      `master` ← `jaehunkim:deterministic_aa`




          opened 05:19AM - 30 May 24 UTC



          [![](https://avatars.githubusercontent.com/u/8697531?v=4)
            jaehunkim](https://github.com/jaehunkim)



          [+250
            -0](https://github.com/ethereum/ERCs/pull/453/files)







We propose a non-custodial interface for service providers to provide AA account[…](https://github.com/ethereum/ERCs/pull/453)s.












## Abstract

We propose a non-custodial interface for service providers to provide AA accounts.

## Motivation

Problem:

The `createAccount` function necessitates an `owner` address to establish an account, consequently preventing service providers from creating accounts on behalf of their users without knowledge of the users’ EOA addresses. To resolve this limitation, service providers employ temporary EOAs to deterministically generate an ERC-4337 account for their users, assigning the temporary EOA as the initial owner. This approach, however, introduces a security vulnerability, as the temporary EOAs’ private keys are managed by the service providers. Furthermore, the service providers assume responsibility for these private keys until such a time when users take the ownership.

Solution:

Set a separate contract as the owner when calling `createAccount`, and allow the user to claim ownership at a later date via a signature provided by the service provider.

This approach has its limitations, however. To prevent the predetermined address from being claimed by an external party, most AA wallet factory contracts include the `owner` address when calculating the predetermined address and make sure that the owner of the AA wallet becomes the given `owner` address. In order to satisfy this constraint, service providers opt to creating a new and random private key on their server and sending it later when the user requests it.

## Replies

**jhfnetboy** (2024-05-26):

we got this question in our account service, how do we help end users ignore the technical conceptions and crypto barriers?

the end user can use a web2 account to bind something in the service contract and get a one-time proof(signature) to claim(change) the ERC4337 account ownership.

But what is the credential of the end user?

An email address? the proof get from the separate contract?

---

**jaehunkim** (2024-05-31):

I agree with what you said. Ultimately, the problem of how the end user proves their credential still remains.

Both email and proof get from the separate contract would work.

Or maybe user unique identifier managed by the service owner seem like possible options.

---

**kopykat** (2024-05-31):

Hey, have you checked out modular smart accounts before (eg [ERC-7579: Minimal Modular Smart Accounts](https://eips.ethereum.org/EIPS/eip-7579))? In short, you can use different validation logic (eg passkeys, multi-sig, reovery, …) so you are not restricted to using (custodial) EOAs as the owners of smart accounts

---

**jhfnetboy** (2024-06-01):

I prefer the credential hosted by a “decentralized” service owner, but if it is centralized, it has some risks.

Now we have an idea, the credential is controlled by a temporary community server, and the end user uses a D2FA(decentralized 2FA) to sign every transaction. If the end user feels insecurity, then move to another server, use a social recovery method

---

**jhfnetboy** (2024-06-01):

let me try, do you have some simple demo?

---

**kopykat** (2024-06-01):

you can check out the reference implementation here: [GitHub - erc7579/erc7579-implementation: Reference implementation for ERC-7579](https://github.com/erc7579/erc7579-implementation). In there, theres a factory that lets the user pick any validator and pass its initialization data (eg to set owners)

---

**dror** (2024-06-02):

I think the motivation is not defined properly:

First, it has nothing to do with “createAccount” needs an “owner”: this is just the sample implementation of erc-4337 (though a simple one, that many accounts use)

The problem stems from the fact the account is created counter-factually, and should be assigned to its real owner, whatever “owner” means.

The way to attach an account to an owner requires some owner credential be put as part of the counter-factual address. This way, even if someone front-run the create request, the only thing it can achieve is save gas to the real owner (since after creation, only the real owner should be able to use the account).

The “SimpleAccount” sample in erc4337 uses the simplest “owner” definition, which is an EOA signer. This, however, is bad for long-term account, as it requires the owner to keep the private key of that owner key forever, just in case he wants to deploy on a new network

(that is, the owner can be changed on every network, but the owner has to keep the keys for new network)

So basically your idea is use another global ID of a user (e.g email address) as initial credentials for creating the account.

The only problem is that we need a secure decentralized mechanism to prove the ownership of this global ID

This mechanism, if I understand correctly, is your “securer”.

In the past several attempts were made to define a factory with such mechanism.

I think that with your proposal, you try to separate this authentication-only component from the actual factory, so that it can be used with different account implementations.

One thing I could suggest is that this “securer” can also be used as recovery mechanism: the account support it not only for initial creation, but also for recovering lost key (this is not an automatic feature of accounts, though: some accounts will use it, others will add some “dead-owner” control mechanism, and other might elect to use completely different recovery)

---

**jhfnetboy** (2024-06-04):

Agree with that： So basically your idea is use another global ID of a user (e.g email address) as initial credentials for creating the account.

The only problem is that we need a secure decentralized mechanism to prove the ownership of this global ID.

This is the key question.

---

**jhfnetboy** (2024-06-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> One thing I could suggest is that this “securer” can also be used as recovery mechanism: the account support it not only for initial creation, but also for recovering lost key (this is not an automatic feature of accounts, though: some accounts will use it, others will add some “dead-owner” control mechanism, and other might elect to use completely different recovery)

If, we create a contract account with a passkey signature as part of the initial parameter of the initial code, and a changeable mechanism to change the passkey signature(like BLS of 3/5 guardians).  We also add guardians to launch social recovery, then, we get a 2FA to guarantee every transaction.

And let’s build a decentralized validator mechanism to verify the passkey signature with a BLS threshold signature and a pre-registered public key of your passkey. We get a D2FA with a changeable signature algorithm, which depends not only on the EIP7212.

it is just an idea to “createAccount” action for “securer” ways.

---

**SamWilsn** (2024-06-28):

I’m not sure this is any more secure than just setting a private key as the owner and transferring ownership to the end user when their EOA address is known. You need to keep the private key recognized by the “Securer” as safe as the plain private key, or else an attacker can use the Securer’s private key to change the owner, then perform any desired actions. At best, this just adds an extra step (changing ownership) for an attacker that has access to the private key.

