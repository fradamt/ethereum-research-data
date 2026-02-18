---
source: ethresearch
topic_id: 10774
title: Decentralised CloudFlare - using RLN and rich user identities
author: blagoj
date: "2021-09-17"
category: Privacy
tags: []
url: https://ethresear.ch/t/decentralised-cloudflare-using-rln-and-rich-user-identities/10774
views: 4361
likes: 5
posts_count: 8
---

# Decentralised CloudFlare - using RLN and rich user identities

### Authors and attributions

Blagoj and [Barry WhiteHat](https://ethresear.ch/u/barrywhitehat).

# Introduction

We propose an idea for a decentralised rate limiting service for web applications which offers protection from brute force, DoS and DDoS attacks, Web Scraping and API overuse.

We plan to implement this service by using the RLN (Rate Limiting Nullifier) construct and InterRep.

RLN (Rate Limiting Nullfier) is a construct based on zero-knowledge proofs that enables spam prevention mechanism for decentralized, anonymous environments.

For RLN to be used, the users first need to register to the application with their public key - they’re added to a membership Merkle tree upon successful registration. After that they can use the protocol protected by RLN, but with each action they leak a portion of their private key and if they break the anti-spam threshold with a predetermined frequency of requests their private key can be fully reconstructed (by the properties of [Shamir’s Secret Sharing scheme](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing)). By having their private key revealed the user can be removed from the membership tree and their protocol related stake can be slashed, if staking is enabled for the RLN application. You can find out more about RLN [here](https://medium.com/privacy-scaling-explorations/rate-limiting-nullifier-a-spam-protection-mechanism-for-anonymous-environments-bbe4006a57d).

InterRep is a service for linking user web3 identities with their reputable social media accounts. You can find more about InterRep [here](https://jaygraber.medium.com/introducing-interrep-255d3f56682).

# Why it is important?

Request spamming attacks on application layer are big problem for many applications.

Brute force attacks, DoS and DDoS attacks, Web Scraping and API overuse can lead to revenue loss, increased infrastructure costs and valuable information leakage. Also brute force attacks can make certain websites impossible or at least prohibitively expensive to run.

The solutions on the market offering request spam protection are not efficient enough and degrade the user experience in the false-positives scenario - the users usually need to solve CAPTCHAs to verify their identity. The spam-resistance, efficiency level of spam detection and the user experience on the application layer can be largely improved by using RLN and rich user identities.

Additionally there aren’t any privacy-first rate limiting services on the market, and the desirability for and privacy and anonymity is ever increasing. As ZK technology develops, more anonymity and privacy focused application will emerge on the market which will be in need of rate limiting services.

We also think that by combining new and experimental technologies such as RLN and InterRep which are more web3 native, we can provide useful services to the web2 world and attract more people into the web3 world.

This project is an interesting experiment that tries to bridge the gaps between web2 and web3 and will enable us to explore what impact the web3 technologies can have on the web2 world.

# Description

Rate limiting/DDoS protection service for websites and web applications which offers protection from Brute force attacks, DoS and DDoS attacks, Web Scraping and API overuse. The request spam protection is on application layer of the network stack (layer 7 protection), and it will be functioning similarly in a traditional way as the Cloduflare’s Rate Limiting product.

The Cloudflare Rate-Limiting service works by the websites defining rate-limiting rules, which when broken the user is either temporarily banned from accessing the application or is given CAPTCHA challenges to solve. The Cloudflare Rate-Limiting service also rate-limits the users by their IP address.

We can improve upon these features by offering to users to be able to create ZKPs instead of solving CAPTCHAs themselves, and for the applications to have better request spam protection by identifying the users by their rich user identities in an anonymous way. By using ZKPs, the applications are not aware of the real identities of their users and user privacy is preserved. A rich user identity is a Web3 identity such as Ethereum address linked with personal credentials of high value such as reputable twitter account, email, driver’s licence, bank account. The rich user identities have the property of hard replicability, thus reducing the possibilities for sybil attacks a lot.

The initial idea is to implement the rate limiting service as a centralised server at the start and leverage a more distributed architecture later.

The rate limiting service will act as a middleman between the frontend clients and their backends.

It will rate limit the users based on their IP addresses, but also it will be able to verify ZK proofs that the users will generate. The users will need to be registered to the service to generate valid ZK proofs. The service will enable user registration for the users that want to avoid solving challenges manually by providing a user interface, where by using InterRep the users will be able to register to the service.

The server will host a single membership Merkle tree for all of the users, meaning that the users are registered at service level and not on application level. In other words after registering users will be able to access all of the applications protected by the rate limiting service.

If a user sends too many requests per second, the service will be able to reliably identify and remove the user from it’s membership tree, by the properties of the RLN proof system. Once slashed the users will not be able to access the applications protected by the rate limiting service again, nor be able to register (this might be too restrictive, and we might loosen up these conditions).

# Implementation details

The solution can be logically divided in three parts:

- Rate limiting service
- Frontend clients
- Backend apps

### Rate limiting service

A device or group of devices (for now a centralised server) which will store a single RLN membership tree, additional data structures for keeping track of ZKP metadata such as nullifiers and key shares, data structures necessary for web3 identity linking (the InterRep part), as well as additional data structures such as a ban list.

Upon user registration the service will store the user identity commitment (Poseidon hash of their private key) in its RLN membership merkle tree.

If a user exceeds request limits the service will be able to reconstruct the user’s private key and from the private key reveal the identity commitment and ban the user by removing them from the RLN membership merkle tree.

The service will also provide an UI through which the users will be able to register and also a REST API though which registered users can obtain the parameters necessary for generating valid ZK proofs in a trust-less manner.

### Frontend clients

The frontend clients for the apps that want to be protected by the rate limiting service will need to implement a special library which will handle the communication with the rate limiting service.

The frontend clients will generate and store the private key for the user.

The library will be able to generate ZK proofs and include the ZK proof as well as additional parameters necessary for verification of it as a HTTP headers. All of the HTTP requests will be sent to the rate limiting service. The frontend clients will obtain the root of the membership merkle tree and their auth path (parameters necessary for generating the ZK proofs), from the rate limiting service via API calls.

### Backend apps

The backend apps will only receive filtered requests, redirected from the rate limiting service only. If a user tries to access the backend app (while skipping the rate limiting service), they will be redirected to the rate limiting service first.

## References and further reading

1. RLN introductory post - https://medium.com/privacy-scaling-explorations/rate-limiting-nullifier-a-spam-protection-mechanism-for-anonymous-environments-bbe4006a57d
2. InterRep overview - https://jaygraber.medium.com/introducing-interrep-255d3f56682
3. What is rate limiting - https://www.cloudflare.com/en-gb/learning/bots/what-is-rate-limiting/

## Replies

**blagoj** (2021-10-22):

Since the latest write up, we’ve updated the idea. The Semaphore and RLN identities have been abstracted in a separate library: https://github.com/appliedzkp/libsemaphore, and also the constructs have been changed to use identity commitments of the same form. This allows for better integration between RLN (the cloudflare rate limiter) and Semaphore (InterRep) apps. In this case the user registration on the cloudflare rate limiter app is skipped, and we rely on the semaphore groups at InterRep for user registration (if the users are registered at InterRep they can use the apps protected by the rate limiter without any integration). We believe this step is an UX improvement. I’ve also written more about the considerations regarding the InterRep and RLN app integrations: [RLN Interrep integration (tree storage and interactions) - HackMD](https://hackmd.io/@aeAuSD7mSCKofwwx445eAQ/SJpo9rwrt).

In the meanwhile, we’ve worked on a PoC that demonstrates a rate-limiting service and the InterRep <> RLN integration and interactions, which also uses a generalized version of the RLN construct: https://github.com/bdim1/rln-interrep-cloudflare.

In the PoC we use the following variables for the RLN construct:

- spam_threshold - the spam threshold is set to 3. The circuits (NRln) are built with limit=3, polynomial of degree 2 is used.
- epoch - string concatenation of the website url and a random timestamp. This allows the spam filtering to be more granular - for url, per time interval. The users will be slashed if they send more than spam_threshold requests per time interval, at a given url.
- signal - random string, used as a request id. Must be different for every request, otherwise the requests would be rejected
- rln_identifier - random identifier, different for each application.

---

**meridian** (2021-11-08):

Cloudflare offers a way to bypass the CAPTCHA via [GitHub - privacypass/challenge-bypass-extension: Privacy Pass: a privacy-enhancing protocol and browser extension.](https://github.com/privacypass/challenge-bypass-extension)

[This reminds me of an IETEF specification called Reputons](https://datatracker.ietf.org/doc/html/rfc7070)

A reputon expressed in JSON is a set of key-value pairs, where the keys are the names of particular attributes that comprise a reputon (as listed above, or as provided with specific applications), and values are the content associated with those keys. The set of keys that make up a reputon within a given application are known as that application’s “response set”.

A reputon object typically contains a reply corresponding to the assertion for which a client made a specific request. For example, a client asking for assertion “sends-spam” about domain “[example.com](http://example.com)” would expect a reply consisting of a reputon making a “sends-spam” assertion about “[example.com](http://example.com)” and nothing more. If a client makes a request about a subject but does not specify an assertion of interest, the server can return reputons about any assertion for which it has data; in effect, the client has asked for any available information about the subject. A client that receives an irrelevant reputon simply ignores it.

Could this service offer sponsorship where an account can “sponsor” (i.e. subsidize) another account for rate limiting?

---

**blagoj** (2021-11-08):

Thanks for the documents, I haven’t known about the challenge bypass extension, nor the IETEF specification. They are looking very interesting.

Regarding the sponsorship, could you elaborate more? What would sponsoring another account for rate limiting mean in this case? To be honest I am not sure what this means and how it could be implemented. The identity of the user is unknown, and delegation of tasks between users is natively impossible (except if we modify the protocol). But please feel free to share more about your idea

---

**samueldashadrach** (2021-11-12):

This seems very interesting. I have some questions though. You’ve proposed two forms of identity that can be used - economic stake and social reputation. I guess the analysis goes very differently for both, so might be worth separating them.

For economic stake:

a) How much stake would be sufficient?

b) If there is a way for people who don’t have their financial assets on a blockchain to use this system? Could a payment provider or (non-crypto) mobile wallet work with this system?

For social reputation:

c) If it is a centralised account like twitter, couldn’t twitter also be trusted with limiting number of tokens or sign ins per unit time? So twitter provides the website an anonymous token every time someone wants to sign in, no ZKP or SSS needed. Anonymous SSO I think.

---

**blagoj** (2021-11-12):

In general those are the two common forms of stake that can be used in these kind of systems, which enable sybil attack prevention and disincentives for spamming.

Specifically for this project, the second option is more applicable and can be applied more broadly because the system is designed to be fully offchain and also the number of users that have web2 social media accounts > the number of users that have or willing to stake cryptocurrencies. Also onchain registration for this usecase will be a worse UX than using something as InterRep (where the users might already be registered).

But regarding the questions in general case (not specifically for this usecase):

For economic stake:

> How much stake would be sufficient?

A: This is again largely app dependent, but large stake - higher barrier for entry and stronger disincentives for spamming, small stake - lower barrier for entry and weaker disincentives for spamming. Both scenarios should be applicable for different use cases. “Large” and “small” are relative terms and the actual numbers should be carefully obtained, not just by theoretical measures but also by performing tests and “trial and error”.

> b) If there is a way for people who don’t have their financial assets on a blockchain to use this system? Could a payment provider or (non-crypto) mobile wallet work with this system?

Subsidizing user’s registration is technically possible by using a relayer, but this would enable lower disincentives for the users not to spam and transfer the “staking part” to the relayer instead of the smart contract. If we use relayer then the relayer needs to ensure that a slashed user cannot register again, thus they need to “authenticate” to the relayer with some sort of asset/account which is hard to replicate. This asset would again be probably something like web2 social media account, so using just a social reputation system (i.e InterRep) would be much more useful and less complex.

For social reputation:

> If it is a centralised account like twitter, couldn’t twitter also be trusted with limiting number of tokens or sign ins per unit time? So twitter provides the website an anonymous token every time someone wants to sign in, no ZKP or SSS needed. Anonymous SSO I think.

Could you please elaborate more on the anonymous token and anonymous SSO parts? I am not sure if I understand them correctly.

We’re using InterRep for anonymous linking of a web2 social media profile with an identity commitment. InterRep places the identity commitment into a semaphore group. This allows for the users to prove that they own a reputable account (defined by some reputation criteria depending on the platform, i.e followers, stars, etc) without actually revealing their identity. So in our use-case the users will need to create zk proofs to prove that they’re part of a certain group (i.e they’re eligible for access) and also to preserve their anonymity by doing so. Basically the RLN is used here as a mechanism to prevent spamming (request overuse in this case) in a system where anonymity needs to be preserved.

If I understood your question correctly, by using twitter directly to Sign in the users, and then just use the oauth tokens, then the user’s public data is exposed and there is basically no anonymity, which is contrary to what we’re trying to achieve.

Note that when users link their web2 social profile on the interrep server the anonymity is preserved - i.e the user’s twitter profile is not associated with their identity commitment.

---

**samueldashadrach** (2021-11-13):

Thanks for your reply!

> This is again largely app dependent,

Yep, but I thought knowing the order of magnitude would still be useful. I guess the worse case is if people want to maximally burn their stake for a DDOS attack. So some estimate on how much money do we require the DDOSer burn to take down the website for how many minutes or hours.

> by using twitter directly to Sign in the users, and then just use the oauth tokens,

Basically twitter can issue “anonymous oauth” tokens - twitter can tell you that a twitter user has signed in but not which twitter user,

---

**blagoj** (2021-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> Yep, but I thought knowing the order of magnitude would still be useful. I guess the worse case is if people want to maximally burn their stake for a DDOS attack. So some estimate on how much money do we require the DDOSer burn to take down the website for how many minutes or hours.

Definitely, those kind of measures need to be taken into account. The goal would be to determine a quantity that is sufficient to disincentivize a rational actor to spam.

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> Basically twitter can issue “anonymous oauth” tokens - twitter can tell you that a twitter user has signed in but not which twitter user,

I see your point that Twitter might act as a semaphore group, but I don’t think that is feasible.

First I think that such feature is not available from twitter at the moment (anonymous oauth), or at least I couldn’t find it. Basically for each oauth token that twitter issues, the app can “fully verify the credentials” for the user, so no privacy is preserved whatsoever.

Even if such an API endpoint existed that returns a binary output (only wether user is registered or not), and user privacy is preserved on app level, twitter will still know which users granted which app for access (oauth tokens) and thus privacy is leaked. And the downside for a binary output endpoint is that the user can’t be classified - meaning barriers for entry are set low, and sybil attack resistance is much lower.

Basically the whole custom RLN ZK setup allows for these properties to be met without exposing privacy, which could not be met with just using an oauth token.

