---
source: ethresearch
topic_id: 4294
title: Security considerations for Shamir's secret sharing
author: peg
date: "2018-11-17"
category: Security
tags: []
url: https://ethresear.ch/t/security-considerations-for-shamirs-secret-sharing/4294
views: 8970
likes: 20
posts_count: 9
---

# Security considerations for Shamir's secret sharing

A bit of an update from ‘Dark Crystal’. We are continuing to develop our identity recovery system, working on ‘forwarding’ shares to people other than the author of the secret. Parallel to this we are currently researching two areas.  Adopting secp256k1 keys, and security issues/vulnerabilities with Shamir’s secret sharing and how to approach them.  This article is about the latter, and is heavily inspired by a recent security review from [Dominic Tarr](https://github.com/dominictarr). We hope that this will be useful for other projects considering using Shamir’s scheme for identity recovery.

***Note:*** As a new use I am apparently only allow to add two links to posts, so i had to cut the links out of the references.

## Security considerations for Shamir’s secret sharing

In general, Shamir’s scheme is considered information-theoretically secure.  That is, individual shares contain absolutely no semantic information about the secret, and it can be said to be ‘post quantum’ cryptography.

An interesting anecdote, the root key for ICANN DNS security, effectively the key which secures the naming system of the internet, is held by seven parties, based in Britain, the U.S., Burkina Faso, Trinidad and Tobago, Canada, China, and the Czech Republic. Cryptographer Bruce Schneier has alleged that they are holders of Shamir’s secret shares, which indicates the scheme is taken quite seriously.

However, it is not without its problems:

### The need for verification of individual shares

Harn and Lin consider the situation in which ‘cheaters’ claiming to be holders of shares introduce ‘fake’ shares, causing the incorrect secret to be recovered.  Of course without having the other shares they have no control over the content of the ‘incorrect’ secret.

This is not so much of a concern for us as we already have a way to validate who is a custodian.  However we also considered the possibility that genuine holders of shares might have a motivation for not wanting the secret to be recovered, and could maliciously modify their share.  Furthermore, the shares might be modified by some accidental or external cause, and it is important to be able to determine which share is causing the problem.

It might be very easy to determine that we have recovered the wrong secret.  Either because we have some idea of how we expect it to look, or as we have recently implemented in dark crystal, an identifier is added to the secret to allow the correct secret to be automatically recognised.  (We concatonate the secret with the last 16 bytes of its SHA256 hash).

However, the problem here is that although we might know for sure that we have not successfully restored our secret, we have no way of telling which share(s) have caused the problem, meaning we do not know who is responsible.

The solution is to introduce some verification of shares, and a number of different methods of doing this have been proposed.  Typically, they rely on publicly publishing some information which allows verification of a given share.

Here are some possible solutions:

#### Publicly publishing the encrypted shares

This is what we were originally planning to do, but this only helps in this context if the encryption scheme used is deterministic.  That is to say encrypting the same message with the same key twice will reliably give the same output.  The problem here is that such encryption schemes are vulnerable to replay attacks.  Most modern asymmetric schemes introduce some random nonce to evade this problem. The scheme we are using (libsodium’s secret box) typically takes a 24 byte random nonce.  So this is not a good option.  However we actually already ‘wrap’ shares in a second level of encryption to to allow the secret owner to publish their own encrypted copy of the share message with its associated metadata as a way to keep a personal record of what was sent to who. When we looked at other schemes for verifiable secret sharing we found they involved a similar practice, and we decided to use an existing well-documented scheme.

#### Publicly publishing the hash of each share

This is also something we considered, but feel that it gives custodians more unnecessary extra information and less accountability compared to other methods.

#### Feldman’s scheme

Paul Feldman proposed a scheme in 1987 which allows custodians to verify their own shares, using homomorphic encryption (an encryption scheme where computation can be done on encrypted data which when decrypted gives the same result as doing that computation on the original data) on top of Shamir’s original scheme.

#### Schoenmakers scheme

More recently Berry Schoenmaker proposed a scheme which is publicly verifiable (originally introduced by Stadler, 1996).  That is, not only custodians, but anybody is able to verify that the correct shares were given.  The scheme is described in the context of an electronic voting application and focusses on validating the behaviour of the ‘dealer’ (the author of the secret).  But it can just as well be used to verify that returned shares have not been modified, which is what we are most interested in.

#### Implementations

We are currently considering the following implementations:

- github songgeng87/PubliclyVerifiableSecretSharing - C implementation built on secp256k1 used by EOS
- github FabioTacke/PubliclyVerifiableSecretSharing - A Swift implementation
- github dfinity/vss - Dfinity’s NodeJS implementation built on BLS, and used for their distributed key generation

However, these do not give a drop-in replacement for the secrets library we currently use.  Adopting verifiable secret sharing would require a large change to our codebase and mean we need to reconsider several aspects of our model.  But it would bring a great advantage in terms of security.

### Share size has a linear relationship with secret size

Anyone holding a share is able to determine the length of the secret.  Particular kind of cryptographic keys have a characteristic length.  So the scheme gives away more information to custodians than is necessary.  Our solution to this is to add padding to the secret to increase share length to a standard amount.

### Revoking shares if trust in a custodian is lost

Suppose we loose trust in one person holding a share. This might be because they had their computer stolen. Or maybe we had a really bad argument with them. Or maybe we found out they weren’t the person they were claiming to be.

In Shamir’s original paper he states that one of the great advantages of the scheme is that it is possible to create as many distinct sets of shares as you like without needing to modify the secret. Each set of shares is incompatible with the other sets. Using Glenn Rempe’s implementation, if we run the share method several times with the same secret, we get each time a different set of shares. When generating a new set, an extra check could be done to rule out the extremely improbable case that an identical set had been generated.

This means in a conventional secret sharing scenario (imagine the shares are written on paper and given to the custodians), we could simply give new shares to the custodians we do still trust and ask them to destroy the old ones. This would make the share belonging to the untrusted person become useless.

In our case, we are using Secure-Scuttlebutt’s immutable log, and have no way of destroying a message. A solution we are considering, is to use ephemeral keys which are used only one time for a particular share and can be deleted when a new set of shares is issued. This gives greatly increased security, but the cost is more keys to manage and increased complexity of the model.

### Secure computation

Having a good system of encryption does not give us security if the host system is compromised. We are considering using a dedicated virtual machine for secure computation, such as [Dyne.org](http://Dyne.org)’s ‘Zenroom’. However there, are many more considerations one needs to make, especially if secret is initially stored on disk.  But this goes beyond the scope of assessing the security of Shamir’s scheme.

## Conclusion

We feel confident that we are able to address the issues we have explored in this article, although not all of them will be implemented in the next release. However, we have focussed here mainly on technical limitations of the scheme.  There are many other social aspects which pose threats to our model, which we will explore in another article.

## References

- Beimel, Amos (2011). “Secret-Sharing Schemes: A Survey” cs.bgu.ac.il/~beimel/Papers/Survey.pdf
- Blakley, G.R. (1979). “Safeguarding Cryptographic Keys”. Managing Requirements Knowledge, International Workshop on (AFIPS). 48: 313–317. doi:10.1109-/AFIPS.1979.98.
- Feldman, Paul (1987) “A practical scheme for non-interactive Verifiable Secret Sharing” Proceedings of the 28th Annual Symposium on Foundations of Computer Science
- Harn, L. & Lin, C. Detection and identification of cheaters in (t, n) secret sharing scheme, Des. Codes Cryptogr. (2009) 52: 15.
- Schneier, Bruce (2010) - DNSSEC Root Key held by 7 parties worldwide
- Schoenmakers, Berry (1999) “A Simple Publicly Verifiable Secret Sharing Scheme and its Application to Electronic Voting” Advances in Cryptology-CRYPTO’99, volume 1666 of Lecture Notes in Computer Science, pages 148-164, Berlin, 1999. Springer-Verlag.
- Shamir, Adi (1979). “How to share a secret”. Communications of the ACM. 22 (11): 612–613. doi:10.1145/359168.359176.
- Zenroom, a virtual machine for fast cryptographic operations on elliptic curves

## See Also…

- Our ‘list of applications and articles on Shamir’s secret sharing’
- ‘Brainstorming Coconut-related scenarios’ (‘Coconut death’ refers to a role playing game we did as part of our research where we tried to recover the keys of members of the group who had been hit by coconuts)
- ‘Thoughts on verifying received shards in dark crystal’
- You can also follow our development on Secure Scuttlebutt channels #darkcrystal #dark-crystal and #mmt

## Replies

**dlubarov** (2018-11-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/peg/48/2798_2.png) peg:

> (We concatonate the secret with the last 16 bytes of its SHA256 hash).

For your use case, is it safe to assume the dealer is honest? A dishonest dealer could generate a 16 byte partial collision, and present two different “recovered secrets” to two different observers. It might not be a concern at all in the context of your application, but if there’s any doubt, it might be good to use 32 bytes just in case?

![](https://ethresear.ch/user_avatar/ethresear.ch/peg/48/2798_2.png) peg:

> [Publishing share hashes] is also something we considered, but feel that it gives custodians more unnecessary extra information and less accountability compared to other methods.

Could you elaborate on this? I don’t really understand the concerns. Assuming you just need to protect against malicious custodians and not malicious dealers, publishing share hashes seems as good as anything else AFAICT.

---

**peg** (2018-11-18):

[@dlubarov](/u/dlubarov) - thanks very much for your reflections

> is it safe to assume the dealer is honest?

in this context, we are making a system where people can backup their secrets (typically private keys) by sending shamir’s shares to their friends. so yes we can assume the dealer is honest, as it is in their interest to facilitate recovering the original secret.

> it might be good to use 32 bytes just in case?

the reason we have truncated it is too keep shares small. With the secret sharing implementation we are using, shares are roughly four times the length of the original secret.  And Scuttlebutt messages (which we use to transmit shares) have a maximum size, meaning there is an upper limit on the secret size.

> [Publishing share hashes] Could you elaborate on this? I don’t really understand the concerns. Assuming you just need to protect against malicious custodians and not malicious dealers, publishing share hashes seems as good as anything else AFAICT.

I’m pleased you brought this up as this is something I’d like to give more thought to, and it is an appealing option because it is so simple.

The concern was that each custodian now has their own share as well as hashes of the remaining shares.  In my understanding of shamir’s scheme, this does not create a vulnerability, but I am a little unsure of this. At the very least, it exposes the number of custodians, and gives a way to brute-force the secret.  But i expect any zero knowledge verification would do this.  I’d love to hear your opinion on this.

The other concern was accountability - we do not want to publicly expose the identities of custodians, so we would need to publicly publish only the hashes, not who they were given to.  If two custodians presented identical shares we would have no way to tell which one of them had originally received it.

My feeling is that I would prefer to use a verification scheme which is well documented and used by other projects, so I’d be interested to find examples where this, or something similar is being used.

---

**omershlo** (2018-11-18):

**A few remarks:**

- It seems that your use case will benefit significantly from PVSS.  VSS scheme will handle malicious dealer at distribution protocol. PVSS will also handle bad secret share holders (custodians) at reconstruction protocol and will flag the ones that are revealing bad shares.
- I would suggest to not assume the dealer is honest such that you would be able to capture for example hacked client that distributes secret shares wrongly.
- As best practice I think you should stick with existing P/VSS schemes and not try something not proven (i.e. publishing share hashes) or introduce new assumptions.
- There is another VSS scheme, by Pedersen. Maybe libs implementing this scheme will fit more your code base.  check out the paper: Non-interactive and information-theoretic secure verifiable secret sharing or just the protocol given in section 2.3 in [1]
- [Rust implementation for Feldman VSS](https://github.com/KZen-networks/multi-party-schnorr/blob/be7e8cd3fe2164f596c081532d5a815f118a2084/papers/provably_secure_distributed_schnorr_signatures_and_a_threshold_scheme.pdf supports multiple elliptic curves, update secret shares and share validation.

[1] https://github.com/KZen-networks/multi-party-schnorr/blob/master/papers/provably_secure_distributed_schnorr_signatures_and_a_threshold_scheme.pdf

---

**tetratorus** (2018-11-19):

The [project](https://tor.us) I’m working on also uses PVSS, and we used a modification of the Shoenmaker’s scheme. One thing to note about the [Schoenmakers’ scheme](https://www.win.tue.nl/~berry/papers/crypto99.pdf) is that the secret is of the form G^s (look at page 7)… This means you can’t use a scalar secret, which is what private keys normally are.

You can convert Schoenmakers’ scheme to use scalar secrets, but you end up either needing to implement some form of verifiable encryption of discrete log or accepting a failure mode where a malicious node can stall an honest node during the key generation phase. We decided to go with the latter and do batched key generations upfront and restart the PVSS process with different nodes if there are failures.

You may also want to take a look at proactive secret sharing, to handle mobile adversaries that can compromise several servers over time. Those schemes usually come in two flavors: adding some sort of “0-y-intercept” polynomial or resharing subshares.

---

**thericciflow** (2018-11-20):

[@peg](/u/peg)

In the hashing solution, you need to publish all the shares hashes which, in addition to reveling the number of all custodians, increments the list of auxiliary information each time a new custodian is added. Whereas in a VSS such as Feldman’s scheme, the list of auxiliary information is constant as it is related to the polynomial degree.

---

**antoineherzog** (2018-11-21):

Hi [@peg](/u/peg)

I am really interested in your project. I think this is awesome because we need social recovery to get mass-adoption. On our side, we started to draft an article to explain the key components needed for the internet of values to get to mass-adoption. Could you give me your email in PM?

I would like to continue the conversation with you.

Kind regards

Antoine

---

**kladkogex** (2018-11-22):

At Skale Labs we are developing a generic key sharing/threshold signature/aggregated library, which includes a set of Solidity contracts. We use joint-Feldman DKG scheme that includes verification of shares. We will be releasing the library soon under GPL license.

---

**omershlo** (2018-11-23):

[@kladkogex](/u/kladkogex) what is the motivation/ use cases you see for your DKG and threshold signing schemes? what elliptic curve and signing algorithm will you support?

If you are doing ECDSA:

If it helps we are implementing Steven Goldfeder and Rosario Gennaro DKG and threshold signature paper:

[Fast Multiparty Threshold ECDSA with Fast Trustless Setup](http://stevengoldfeder.com/papers/GG18.pdf). you can check our Rust code [here](https://github.com/KZen-networks/multi-party-ecdsa) (go to the proper branch).

We also support in this library [LIndell’s 2 party ecdsa paper](https://eprint.iacr.org/2017/552).

If you are implementing GG18 DKG let’s talk - there are a few typos and small corrections (for example - the PoK in phase3 DKG is not needed).

