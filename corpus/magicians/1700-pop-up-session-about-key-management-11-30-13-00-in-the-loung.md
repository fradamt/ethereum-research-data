---
source: magicians
topic_id: 1700
title: Pop up session about key management 11:30..13:00 in the lounge area
author: ligi
date: "2018-10-29"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/pop-up-session-about-key-management-11-30-13-00-in-the-lounge-area/1700
views: 1462
likes: 8
posts_count: 8
---

# Pop up session about key management 11:30..13:00 in the lounge area

as a follow-up from: [Topics for Wallet Ring gathering tomorrow 15:30 in the workshop room of National House Smichov](https://ethereum-magicians.org/t/1693/5)

We will have a breakout session at 11:30 - 13:00 about key management

The main reason is that the people behind the [status.im hardware wallet](https://hardwallet.status.im) cannot join the wallet session as they have to leave before it starts. So we do a pop.up session at the mentioned time. I want to scope it a bit wider. So topics *can be*(1):

- interoperability and hardware wallets
- key backups
- key transfer
- link pinless derivation paths to pin protected derivation paths
- getting hardware wallets into the hands of as many people as possible (perhaps by using status.im hardware wallets like ether.cards to a: easily onboard people with tokens/keys with nice UX b: have them use these cards as hw wallets afterwards)
- a new JSON key format: JSON UTC Version 4
- BIP32 defines a way to generate hierarchical trees of keys which can be derived from
a common master key. BIP32 and BIP44 defines the usage of these keys as wallets.
In this EIP we describe the usage of such keys outside the scope of the blockchain
defining a logical tree for key usage which can cohesist (and thus share the same
master) with existing BIP44 compatible wallets. https://notes.status.im/s/SJMhfgMhm#
- …

(1) just topic suggestions - topics will be decided on the spot - please suggest more topics here

## Replies

**brunobar79** (2018-10-29):

[@ligi](/u/ligi) in which room is this gonna happen?

---

**ligi** (2018-10-29):

Unfortunately we have no free room anymore so we will do it in the lounge. But as it is parallel to sessions we should be fine in the lounge as it should not be to noisy then. If a workshop finishes early and a room gets free we can also (given it has consensus) move to this then free room.

But also suggestions welcome  - this is not set in stone - was mainly following the suggestion from [@boris](/u/boris) to do it there ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) But if we move we have to leave redirect notice as I already shared the lounge as the location.

---

**ligi** (2018-10-29):

there will be a bit of delay as the intro session takes a bit longer. So we will directly start after this one is finished.

---

**ligi** (2018-10-29):

Meeting notes (based on [Topics for Wallet Ring gathering tomorrow 15:30 in the workshop room of National House Smichov](https://ethereum-magicians.org/t/1693/8) and extended a bit)

**Attendees**:

[Status hardware-wallet](https://hardwallet.status.im):

- Corey Petti - Security Eng.
- Michelle - Hardware wallet dev.
- Guy-Louis Gray - Product and biz

[Imtoken](https://token.im): Popular in china, handling 10% of Ethereum transactions volume.

- Kaz - dev
- @p0s  - Business dev.

[Walleth](https://walleth.org)

- @ligi

[MetaMask](https://metamask.io)

- @brunobar79  - Dev

**Talking points**

Hardware wallet from status:

- Integration with phones and card reader
- 6-digit PIN or pin-less paths
- has no screen
- There are other ones (UBI or coolwallet which use bluetooth
- Would be cool to integrate with metamask (leverage NFC on phone via wallet connect maybe?) USB not an easy way through card reader
- Android support only (iOS is blocked because of limited NFC support) (note from ligi: this is not a bug, but a feature)
- Status has a Java library already: https://github.com/status-im/hardware-wallet
- higher level Kotlin libary emerging: https://github.com/walleth/KHardWareWallet
- Discussed the challenges of backing up cards without exposing the key to a untrusted device
- Biometrics for PIN auth? Ideally would be a good 2nd factor auth. Could be added optionally
- BIP 44 for different set of keys for whisper / other identity scenarios (for ex. Door unlocking)
- using it as a backup solution - no more mnemonic keys - improving UX. Question: will the card work in XX years? A: 1) same chips used for sim-cards with some guarantees of keeping working. 2) they are cheap - so one could get multiple ones and distribute them (even to untrusted parties) - then there could be a protocol that you challenge these parties to prove that they still have the cards (via pinless path)
- using them as a initial token/ETH distribution way (like ether.cards) - Idea: wrap them in sealed and aluminium wrapped packaging - so no pin is needed - just get to a store - buy a card preloaded with eth. Unwrap and tap to your phone -> finished. This also prevents from trolls rendering them inaccessible by making requests with wrong pins without buying
- How to remove the tight coupling to a specific wallet. Currently it is already quite decoupled - one thing is left: when a user has no wallet installed that can deal with the cards - the play store is invoked and suggests installing status.im. In the future it will be possible to change this via commands - currently you have to recompile the applet. Ideally there is a proxy app that knows about what wallets that are compatible with the phone/card/region and offers to install any of them (can be build using https://github.com/ethereum-wallets - field needs to be added there)
- Plausible deniability (we need to get the ability to define a pin that leads to a different derivation path - the status hardware wallet team mentioned they think about this problem and want to add this in the future)

Imkey

- Hardware wallet from imToken
- Works via Bluetooth
- Has a screen

**Action items:**

1. Create a specific “room” on ETH-Magicians to follow up
2. Get these wallets in the hand of users (status.im will make an initial run of 1000 in january)
3. Get more wallets to support this
4. Add field in https://github.com/ethereum-wallets to indicate which wallets support which hardware wallets (might at some point also help with 3)

---

**bitgamma** (2018-10-31):

Do we already have a room?

I think it would be also worth to have a discussion on https://notes.status.im/s/SJMhfgMhm if possible. Before submitting this as EIP I would like to have more input.

---

**ligi** (2018-10-31):

[@bitgamma](/u/bitgamma)  Sounds great! Hope to see [@boris](/u/boris) or [@jpitts](/u/jpitts) today to ask if they can create the room.

---

**bitgamma** (2018-10-31):

In addition, I have opened GitHub issues on https://github.com/status-im/hardware-wallet/issues to sum up all the applet-specific changes we discussed during the days in Prague. Feel free to add your own or add comments on the existing ones.

