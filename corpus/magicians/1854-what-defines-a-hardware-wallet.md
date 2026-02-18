---
source: magicians
topic_id: 1854
title: What defines a Hardware Wallet?
author: ligi
date: "2018-11-09"
category: Web > Wallets
tags: [wallet, hardware-wallet, epistemology]
url: https://ethereum-magicians.org/t/what-defines-a-hardware-wallet/1854
views: 2132
likes: 13
posts_count: 14
---

# What defines a Hardware Wallet?

As a first post in the new Hardware Wallet Ring - let’s take this PR as a seed to talk about what a hardware wallet actually is as it is currently not very well defined.



      [github.com/novasamatech/parity-signer](https://github.com/novasamatech/parity-signer/pull/185)














####


      `master` ← `hardware-cold`




          opened 07:24AM - 09 Nov 18 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/9/9b6b8814fe21f5ae3d1d3cf967e12f6498467bdc.jpeg)
            lexfrl](https://github.com/lexfrl)



          [+1
            -1](https://github.com/novasamatech/parity-signer/pull/185/files)







https://en.bitcoin.it/wiki/Hardware_wallet
https://en.bitcoin.it/wiki/Cold_stor[…](https://github.com/novasamatech/parity-signer/pull/185)age

We shouldn't claim Parity Signer as a something which "Turns your smartphone into a hardware wallet" . Simply because it confuses user: in the first place, Parity Signer doesn't turn user's phone into a *wallet*, and it doesn't turn it into a *hardware wallet* especially.

We need to fix it everywhere we declare it so (blogposts, wikis etc.).

## Replies

**AtLeastSignificant** (2018-11-09):

I’m not even sure the average user even agrees on what the difference between wallet and interface is.  I mean, MyEther*Wallet* kind of screwed that up IMO.

---

I’ve always used the following to help people understand the security and usability of different products:

• **Blockchain Interface** - software that allows a user to input external sensitive information and output useful processed/formatted data.  This is what MyCrypto and MEW are.

• **Wallet** - a software *interface* (as defined above) that *stores* sensitive information.  MetaMask, Jaxx, and any other software that uses some kind of authentication method to access.  This also encompasses exchanges, but I differentiate those by calling them “curated wallets” since the user doesn’t have direct control over the software or access to it.

• **Hardware Wallet** - a *wallet* (as defined above) that emphasizes security by physically air-gapping the sensitive information and using strong encryption.  I consider the USB drive running Tails and a KeePass DB with my PK inside to be a hardware wallet.  It’s air-gapped, and uses MyCrypto for the interface.

---

Potentially conflicting/confusing terms we use now that might not follow this classification schema:

• **“Paper wallets”** - they aren’t wallets. They are equivalent to writing your password on a stickynote.  To fit the wallet analogy, the *thing* has to both 1) hold something of value, and 2) have purposeful design that supports use of the value stored within.  You don’t call a change jar a “wallet”, even though it meets much of the same purpose as a wallet.  The difference is in design/function in addition to storage of value.  To be clear, value is generally synonymous with sensitive information like PKs.

• **“Vaults”** - this is a term I’ve seen Coinbase use.  It’s essentially a curated wallet with extra authentication / anti theft measures.

• "**Software wallets"** - it’s redundant.  “Wallet” should inherently imply that it’s at least partially software.  It would only be a useful term to use when contrasting it against a hardware wallet solution.

• **Hot/Cold Storage** - I’ve seen hot/cold be used to describe both security and use.  “Cold” wallets *should* be a subset of hardware wallets, but “hot” wallets can really be anything as long as it’s geared towards frequent use. Frequent use =/= insecure.

---

I don’t use Parity Signer, but from my understanding it is what it’s called - a signer.  If it doesn’t store information, it’s not a wallet at all. Just a secure interface.

---

**ligi** (2018-11-09):

Thanks for the writeup. Perhaps this could be the start for a glossary we really need.

But I would really love to see a distinguishment between “hardware wallet” and “offline signer”. I can loose a hardware wallet like my TEZOR - but when loosing a “offline signer” like the parity signer - this is a problem …

---

**hahnmichaelf** (2018-11-09):

I think that phone apps should be called “Mobile Signers”.

“Hardware Wallets”  should remain as only specialized hardware devices (like Ledger and Trezor). This would probably include the encrypted tails usb that [AtLeastSignificant](https://ethereum-magicians.org/u/AtLeastSignificant) uses.

---

**AtLeastSignificant** (2018-11-10):

So I’ve read the Parity Signer Mobile App wiki, but I’m still confused about what it does…

It would seem that if you dedicate a mobile device to this app and remove all the connectivity, then the Parity Signer software would meet the interface and storage requirements to be considered a wallet.  The air-gapped + strong encryption bumps that up to hardware wallet by my definition.

However, if you don’t dedicate the phone to this purpose and are simply running the app on a normal smartphone, I wouldn’t consider it more than just a mobile wallet. The overhead to actually set this up properly seems very high, including both steep hardware requirements *and* usage requirements.  Too many ways to mess up, so IMO it’s not a great solution in terms of high security for the average user.  Certainly no worse than any other online wallet though.

> I can loose a hardware wallet like my TEZOR - but when loosing a “offline signer” like the parity signer - this is a problem …

Why is losing the offline signer more of a problem than losing a TREZOR/Ledger?  You are instructed to write down your recovery phrase when setting up an account - is that not something that can be used to retrieve private keys?  Or are you saying that somebody could compromise the Parity Signer much easier than the TREZOR?

---

**hahnmichaelf** (2018-11-10):

> Or are you saying that somebody could compromise the Parity Signer much easier than the TREZOR?

I believe that was the point that ligi was making.

> However, if you don’t dedicate the phone to this purpose and are simply running the app on a normal smartphone, I wouldn’t consider it more than just a mobile wallet.

Maybe the distinction can be is “dedicated hardware”. Ledger, Trezor, and your USB are all dedicated devices. Their sole purpose is crypto key storage/transaction facilitation.

With a mobile phone, if it’s sole purpose is to store cryptographic keys and allow for the signing of transactions then it can be called a hardware wallet. Otherwise, a phone that is used as a phone + with the auxillary function of storing keys and signing transactions/messages, would just be a mobile signer. I can see this as being a point of contention though, as the two devices (mobile phones with an app on it) are the same. Which is why i tried to remove this point altogether by just calling phone apps “mobile signers”.

---

**ligi** (2018-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> Or are you saying that somebody could compromise the Parity Signer much easier than the TREZOR?

yes - exactly. The problem is that you can e.g. brute force the password for a parity signer. You cannot do this for a TREZOR as it has an exponential back-off for decryption attempts and you cannot get the encrypted key without attacking the hardware. So I think a TREZOR (which for me falls into the class of hardware wallets) is much more secure as it is protected against attacks with physical access than a parity signer (which for me falls under the class of offline signers).

Again - I think both have their use-cases - we should just be careful with wording as when we put both into the same class - then users might get confused and assume both have the same security guarantees.

---

**fckt** (2018-11-12):

> yes - exactly. The problem is that you can e.g. brute force the password for a parity signer. You cannot do this for a TREZOR as it has an exponential back-off for decryption attempts and you cannot get the encrypted key without attacking the hardware.

btw, where does this opinion come from? For the sake of my understanding: is there any real snag (in principle) which blocks us to implement such a protection in the signer-like class tools (apps)? In principle, it’s possible to such a layer not in the app itself, but on the device level (or some virtual environment). So, that would make a device into a what we call “hardware wallet” today (with the same promises) (maybe (but I don’t really like the word “wallet” in the context - I’d better propose ‘“virtual” vault’)) - at least according to the proposed definition principle:

> So I think a TREZOR (which for me falls into the class of hardware wallets) is much more secure as it is protected against attacks with physical access than a parity signer (which for me falls under the class of offline signers)

I’m pretty sure there is a such a hardware protection in the phones already (in iOS devices AFAIK, but I’m sure there should be something for Android devices too!).

My point is that maybe it is not a best idea to rely on that property in the final definition… Just because it could be not a common denominator for all products for that class…

Fair point made here is that people could name (for themselves) that kind of “product” depending on how they are using it (use case). In the same time, point of the current discussion (as I see it) is not to play with public opinions about things, but rely (as strict as possible) on the properties of the product itself. The point (as I see it) is to extract the common denominator and come up with the definition which must be as consistent as possible.

IMHO: we’d better to rely on the best practices (security) on how to use such tools and the final definition must include this idea just not to confuse users (to be as honest as possible with the definition).

The current (official) [usage best practices](https://github.com/paritytech/parity-signer#device-security) are:

> Parity Signer was built to be used offline. The mobile device used to run the app will hold valuable information that needs to be kept securely stored. It is therefore advised to:
>
>
> Get a separate mobile device.
> Make a factory reset.
> Enable full-disk encryption on the device, with a reasonable password (might not be on by default, for example for older Android devices).
> Do not use any kind of biometrics such as fingerprint or face recognition for device decryption/unlocking, as those may be less secure than regular passwords.
> Once the app has been installed, enable airplane mode and make sure to switch off Wifi, Bluetooth or any connection ability of the device.
> Only charge the phone on a power outlet that is never connected to the internet. Only charge the phone with the manufacturer’s charging adapter. Do not charge the phone on public USB chargers.

Too much “meta(meta)” levels in the comment… Deeply sorry for that ![:man_facepalming:t2:](https://ethereum-magicians.org/images/emoji/twitter/man_facepalming/2.png?v=12)

---

**AtLeastSignificant** (2018-11-12):

I have 2 major problems with things like the Parity signer -

1. The security relies on disciplined/aware users
2. The hardware is not purpose-built

People are lazy, you need to force them to be secure (in the least obvious ways possible).  Case in point: the MyCrypto desktop app supports the use of PKs, while the website does not.  Parity signer should probably require the user to accept certain app permisions so that every time it’s run it automatically disables wifi/blutooth or puts the phone in airplane mode if that’s even possible.

My personal gripe with the product is that it’s being marketed as a secure solution, but it inherently relies on insecure / general purpose hardware.  I would much prefer a platform that meets the minimum CIA/AAA requirements running on “dumb” embedded hardware.  Phone apps potentially violate Kerchoff’s law since I don’t know everything about the system.

If the verbiage to describe this type of product is nearly identical to the verbiage used to describe a true hardware wallet, I can’t see any possible way that is beneficial to users.

---

**Tbaut** (2018-11-12):

> Parity signer should probably require the user to accept certain app permisions so that every time it’s run it automatically disables wifi/blutooth or puts the phone in airplane mode if that’s even possible.

Switching on airplane mode when the app is used doesn’t make the phone any more secure. The phone should be offline once and for all ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> My personal gripe with the product is that it’s being marketed as a secure solution, but it inherently relies on insecure / general purpose hardware.

It is a reasonably secure solution if it is used as intended compared to most of what users use today, it’s a fact. The design of the app makes its usage for on daily basis quite annoying: needing to have a node/infura app running on an additional device to scan a QR code.

As a reminder, there is no business model for this app, Parity doesn’t make a penny on it, so there is no such thing as pretending to be better than it is, we have nothing to earn in doing this.

---

**fckt** (2018-11-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> My personal gripe with the product is that it’s being marketed as a secure solution

That’s why I [proposed a change](https://github.com/paritytech/parity-signer/pull/185/files) in the first place. The statement `Parity Signer - Turn your smartphone into a hardware wallet` is an adventurous and dangerous definition.

---

**AtLeastSignificant** (2018-11-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbaut/48/1142_2.png) Tbaut:

> It is a reasonably secure solution if it is used as intended

That’s the huge glaring problem - to use it as intended is nearly impossible.

In America anyways, most cellphone providers will take back the phone after your contract expires and you are able to get a new phone without paying full price upfront. Few people actually drop $1000 on a new phone every couple years to truly own it.  Even if you do have a phone that’s 2 or 3 years old and still works fine, why not just sell it for a TREZOR or something and pocket the rest?  It’s not a cost effective solution even for the niche it appeals to.

On top of that, the user experience doesn’t exactly sound easy. We’re looking at a niche of a niche of a niche that will actually do this properly.  If the app doesn’t force users to be secure, then they won’t be.  Since the vast majority won’t be that secure, it’s extremely misleading to call the product secure.

If I put on my tinfoil hat for a second - even if you have the phone “offline once and for all”, I don’t believe that’s actually the case for many phones.

So, it’s really *not* a reasonable secure solution compared to what people do today, because those people will rarely use it as intended.  Thus, the app should force security when possible, and be very upfront about its limitations.

> As a reminder, there is no business model for this app, Parity doesn’t make a penny on it, so there is no such thing as pretending to be better than it is, we have nothing to earn in doing this.

I really couldn’t care less if Parity makes money or not.  Misleading *users* into a false sense of security is my problem.  They are absolutely pretending to be better than they really are (in terms of security).  Don’t think for a second that “we’re not charging, so don’t complain” absolves Parity of causing harm to users.

---

**ligi** (2018-11-29):

I think I found a solution. We just coin a new term: “openardware wallet”

Reasoning: my main concern was that things I consider having very different security properties where thrown into the same bucket by calling themselves a hardware wallet. By giving them the same name common users think they have the same security guarantees. Which they do not.

For me using “openhardware wallet” could solve the problem as we draw an important line there. What do you think?

A TREZOR is a openhardware wallet. A parity signer, WallETH, Ledger, … is not - simple as that. Would work for me…

---

**fckt** (2018-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> For me using “openhardware wallet” could solve the problem as we draw an important line there. What do you think?

That seems reasonable to me… But what the manufacturers think about?

BTW, this [new ToB report](https://blog.trailofbits.com/2018/11/27/10-rules-for-the-secure-use-of-cryptocurrency-hardware-wallets/) is kind of an interesting input into the discussion.

