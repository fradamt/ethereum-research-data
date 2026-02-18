---
source: magicians
topic_id: 920
title: "imToken 2.0 ethereum: URL-WTF"
author: ligi
date: "2018-08-01"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/imtoken-2-0-ethereum-url-wtf/920
views: 2065
likes: 16
posts_count: 9
---

# imToken 2.0 ethereum: URL-WTF

imToken just had the 2.0 launch event and I was reading up on it: https://help-center.token.im/hc/article/360003147833

Then I scanned one of their QR-Codes and got this:

`ethereum:0x?address=0xEcB88987C3Df520C19720b7a916683Fe6e1E00db&data=%5B%7B%22name%22%3A%22data%22%2C%22type%22%3A%22string%22%2C%22value%22%3A%229mjarj0xpl%22%7D%5D&minVersion=1.3.0&mode=sign_typed_data&md5=b2307ccb`

WTF where they thinking? The missing prefix makes it a pay 681 URL - but completely disregarding the standard. Anyone has a contact to the ones behind this? Would be great if they could join the wallet ring so things like this can be prevented. If they go so off-standard - then they should not use the ethereum: scheme - they could use imtoken: or something like this - but this way they completely fuck up UX! Ideally they propose their own prefix for this use case and submit some EIP for it so we can have interoperability between wallets. e.g. `ethereum:signtypeddata-0x...` could work. But this is really really bad ![:angry:](https://ethereum-magicians.org/images/emoji/twitter/angry.png?v=9)

## Replies

**p0s** (2018-08-01):

Hey! Philipp from imToken here. Appreciate that you followed our 2.0 launch ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=9)

**First**: No need to be angry. You scanned an **old** QR code screenshot on the user support site, not in the app itself.

Let me clarify: If you open the actual imToken 2.0 app, you can see the ‘pay’ scheme is following your [EIP831](https://eips.ethereum.org/EIPS/eip-831):

`"ethereum:pay-<to>@<chainId>? value=<value> &contractAddress=<contractAddress> &from=<from> &gas=<gas> &gasPrice=<gasPrice> &decimal=<decimal>"`

Again, we are moving fast with developing imToken 2.0, and well, updating screenshots on the user support site isn’t that high a priority. Our Simon promised to change the screenshot soon though ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9)

**Second**, let’s set-up/improve our communication. I assumed, putting our name on [the list](https://github.com/ethereum-magicians/scrolls/wiki/Wallet-Ring) and following the forum would be enough for now. But that was apparently not enough.

Yes, we want to establish standards. Very much so. I assume, we both have pretty much the same motivation: bringing **adoption** through good UX and interoperability. And being the big mobile wallet app that we are, we are de facto bringing 6mio MAU (or an average of 10% of eth transactions) towards that threshold of an established standard. Big numbers. Let’s use those to establish standards.

So **3rd:** Please take a look at the new imToken 2.0 ([Android + iOS](https://token.im/download?locale=en-US)). We are more than happy to get your feedback! Getting feedback on the actual app would be even better ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) But seriously, I really appreciate your open feedback!

To continue the discussion and progress: How can we help? How do we go forward in participating in the wallet ring? Being active in EIPs, and in this forum? Do we plan a call?

FYI, from oue side, Ben and me will stay in touch with you and the ring + our engineers are following EIPs.

---

**ligi** (2018-08-01):

Hey, thanks so much for your answer! This really calms me down and I am happy again. Was really quite worried before that imToken will be just another player that shits on standards and ruins UX for everyone and/or leads to code with a lot of special cases this way. Great to hear I was wrong - thanks for that!

We really need to work on communication - but as you have not been on the list before I was posting this (https://github.com/ethereum-magicians/scrolls/wiki/Wallet-Ring/_history) I thought it’s not a problem of communication channels but that you just don’t care - great to see this is not the case.

Currently in the process of trying out your app - where is your issue tracker ?-) Would love to give you a stacktrace of a crash and a screenshot with a problem.

Btw.: great idea with the security quiz - I like this!

---

**p0s** (2018-08-01):

Great!

Right, we put our name (Ben’s name + imToken website) there 2 weeks ago, but under *potential*, as I didn’t understand what it was, at that time: Forum or meeting or collaboration etc.

Regarding app crash, we both continued the conversation on twitter.

Now that you mention it, props on your walletconnect integration!

Keep in touch!

---

**ligi** (2018-08-01):

great! OK now I also understand this miss understanding - “potential” was the list with which I started the page and Ideas who might want to join. Did not see you added yourself there. Great!

Are you also planning to support walletconnect? that would be awesome!

---

**jpitts** (2018-08-01):

This conversation is the nicest I’ve ever seen that started with a “WTF” in the title LOL! I love this community!

---

**p0s** (2018-08-02):

Alright!

Yes, we were fast in agreeing on integrating Walletconnect, and pretty much everybody in the team is a huge fan of the idea.

It’s still only in the back log though. Our internal roadmap says: First deeplinks, then walletconnect.

https://medium.com/balance-io/0x-dharma-imtoken-join-walletconnect-87a3dd4dea8d

On a side note, we already have this cold wallet feature, where you sign transactions via QR, using an old mobile phone as air-gapped cold storage. Similar idea.

---

**p0s** (2018-08-02):

Haha I agree! ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)

---

**ricburton** (2018-08-23):

Thanks a lot for your support of WalletConnect. It really means a lot.

