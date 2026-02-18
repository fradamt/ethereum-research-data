---
source: magicians
topic_id: 655
title: MyCrypto is deprecating usage of private keys in the browser
author: spence
date: "2018-07-05"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/mycrypto-is-deprecating-usage-of-private-keys-in-the-browser/655
views: 1198
likes: 0
posts_count: 5
---

# MyCrypto is deprecating usage of private keys in the browser

Hey all, as a follow-up to the wallet unconference at EDCON hosted by [@lrettig](/u/lrettig), we at MyCrypto are one step closer to deprecating private keys (and keystores, and mnemonics) on the web.

Would love to get your opinions, feedback, and ultimately your support for this decision as we think it’s a step in the right direction for the ecosystem as a whole.

Our post: https://medium.com/mycrypto/a-safer-mycrypto-79d65196e7d8

In an ideal world, other developers would begin to implement this.

## Replies

**jpitts** (2018-07-06):

This is going to help a lot of people! And some will complain, but this is the right move IMO.

**One thing though: I don’t see enough description to users about how they can/should use the current URL-reachable MyCrypto dapp to transact.**

It may require a clear screenshot saying: this is how you’re going to transact on the URL-reachable dapp, otherwise you’ll need to download to transact the way you might be used to.

Also, I want to call dapps that reside on current web something memorable. URLy DApps?

---

**MicahZoltu** (2018-07-06):

As a developer/advanced user, I will find this mildly annoying.  I often use MEW/MyCrypto to validate my application, troubleshoot problems with signing or keys, test that my libraries are doing the right thing, etc.  I use MEW/MyCrypto because it is convenient, I can access it from anywhere, doesn’t require signing up for anything or downloading anything, and it supports a number of options so I can troubleshoot many things in one place.

That being said, I can appreciate the desire to protect users.  I worry that requiring users download something before they can use their keys will turn a lot of people away from MyCrypto.  This feels like a trade-off between security and usability and almost always usability wins.  For example, people may simple switch over to using MEW (or any competitor) rather than sacrifice the usability of a website.

In general, I am of the opinion that “you can lead a horse to water but can’t make it drink” applies here.  MyCrypto has done a lot to help educate users but some *will* slip through the cracks and get burned.  I personally believe that in order for us (humans) to learn as a whole we must be willing to accept some casualties along the way.  Requiring an app download takes power and usability away from users, rather than continuing to try to train them to use good operational security.  IMO, this isn’t a good long term solution, though it probably will help reduce losses short term.

---

**AtLeastSignificant** (2018-07-06):

It’s definitely a bold choice…  I love the sentiment, but I can’t see how this will possibly be good for MyCrypto, since even those of us who appreciate what they are doing are also not thrilled about the impact to usability.  Wrt the website, MyCrypto hasn’t differentiated themselves enough from MEW to really give users a good reason to stick with MC over MEW, which I think is unfortunate. Perhaps the real issue here is with timing, and once MC has a bigger reach they can start making the Apple-like innovations.

I can definitely see this leading to an exodus (lol) from MC back to MEW and other wallets, which both defeats the purpose of removing PK access but also subjects users to the arguably less secure MEW/other services.  I say arguably less secure just because of the differences in quality of the codebases between MEW and MC.

This decision doesn’t increase current security, it just removes less secure features that are already standard in the industry.  Perhaps the better choice is to sacrifice something other than usability to achieve better security, all while adding features.  It’s completely anti-MyCrypto philosophy, but maybe adding 2FA to PK access methods is a better way to go for both the company and community?  I think this would mean centralizing aspects of MC, as well as compromising anonymity to an extent, but it does increase security across the community moreso than everyone just switching to MEW.  This also differentiates the desktop app from the website even more, hopefully encouraging more people to use it instead of any website (which is one of the best outcomes possible).

Another thing I’m concerned about is how this decision will ultimately increase the dependency on MetaMask.  There’s a surprisingly large amount of people using hardware wallets (not sure how popular the Parity Signer is), but for those who aren’t, they are left with only one way to access their funds and it’s through a product that the MyCrypto team has very little control over.

What happens if a vulnerability is found in MetaMask?  What happens if the app page gets compromised and everyone with MM now has a malicious program installed?  From a security standpoint, browser plugins are one of the worst offenders for wide-spread attacks, and they can impact even those with good security practices.

MetaMask is/was already a huge privacy problem, and encouraging people to use it is a double-edged sword IMO.  I’d rather it be a more optional choice for those wanting to use MC.

Perhaps another thing to consider is a MyCrypto “login” plugin that is separate from MM?  I imagine it could be quite small and secure, and removing all the Web3 stuff would make me rest just a tiny bit easier.

---

**tjayrush** (2018-07-07):

I think this is absolutely excellent. The world is slowly realizing that in a decentralized world, the users need to decentralize. I’ve been saying for a while, “Escape from the browser…there’s wide, wide desktop out there.”

