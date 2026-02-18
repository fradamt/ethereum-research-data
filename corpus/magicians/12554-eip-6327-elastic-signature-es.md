---
source: magicians
topic_id: 12554
title: "EIP-6327: Elastic Signature(ES)"
author: JXRow
date: "2023-01-13"
category: EIPs
tags: [erc, signatures]
url: https://ethereum-magicians.org/t/eip-6327-elastic-signature-es/12554
views: 2413
likes: 4
posts_count: 10
---

# EIP-6327: Elastic Signature(ES)

I built an algorithm to make password as privatekey, and it works well on EVM.

Many new crypto users abandoned at wroten down the privatekey, I hope this password algorithmcan bring them back (without privatekey). It’s decentralized, base on ZK-SNARK and smart contract, it can be also used as multi-sign with privatekey, to be double security for protecting assets.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6327)














####


      `master` ← `JXRow:master`




          opened 06:19AM - 13 Jan 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/f/f1271509a23d324d61ca3dd662befa090c1743c1.png)
            JXRow](https://github.com/JXRow)



          [+316
            -0](https://github.com/ethereum/EIPs/pull/6327/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6327)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**sullof** (2023-01-14):

That is super interesting. I will take a deep look.

---

**xinbenlv** (2023-04-10):

The EIP looks good as a draft. And thank you for this creative idea!

[Peer Review] The only technical concern I have is that in 2008-2009 the Bitcoin’s hashrate globally is 10MHash/s, today it’s 400EHash/s which is 4e13 times more. If the hash rate of Poseidon increases as fast in that rate, it will be cracked in 100seconds in 15th year. 116586246y = 3.6766638539e+15sec

---

**JXRow** (2023-04-10):

Thank you, thanks for the notice, we are following, if any better way, we will update

---

**sullof** (2023-04-13):

Do you have a working implementation somewhere?

---

**JXRow** (2023-04-15):

sure, https://www.zksafe.pro/

---

**alinush** (2023-06-06):

I’m having trouble understanding the motivation for this.

It seems to me that I could have password-based accounts in Ethereum (w/ or w/o EIP-4337) by just deriving my SK from a password (using whatever memory-hard hash function I prefer).

I guess I cannot “rotate” my password, but I could implement this via the EIP-4337 standard using a digital signature from my old password-derived SK on a new PK.

Why bring complicated ZKPs into this when simple digital signatures with password-derived SKs seem to work just fine?

---

**JXRow** (2023-06-06):

Using certificate + password => private key, it needs to store certificate. Losing certificate is a big secure problem.

Another way is using public private key + path => new private key, like BIP-32, incording to the BIP, it donsen’t support password, but you can still encode password to path, maybe it can work, I’m not sure, I guess it may need a long time(a few minutes, ZKP is seconds) to generate the new private key, if you have tried, share your idea, I‘ll glad to know.

---

**alinush** (2023-06-06):

I am not able to parse your reply, sorry.

What “certificate” are you referring to?

Not sure I get your point about BIP-32 either. Your approach is not BIP-32 compatible, AFAICT. Neither is the approach I’m proposing above (i.e., derive an SK in whatever secure manner you want from a password).

---

**JXRow** (2023-06-13):

Sorry, so busy these days, I tryed to create HDwallet([HD Wallet](https://docs.ethers.org/v5/api/utils/hdnode/)) using ethers.js@v5.7(), but failed, return

‘TypeError: Cannot read properties of undefined (reading ‘fromMnemonic’)’

if you can create wallet from password, show the codes, thx

