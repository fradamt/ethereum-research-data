---
source: magicians
topic_id: 1693
title: Topics for Wallet Ring gathering tomorrow 15:30 in the workshop room of National House Smichov
author: ligi
date: "2018-10-28"
category: Web > Wallets
tags: [wallet, council-of-prague, hardware-wallet, walletconnect]
url: https://ethereum-magicians.org/t/topics-for-wallet-ring-gathering-tomorrow-15-30-in-the-workshop-room-of-national-house-smichov/1693
views: 2140
likes: 13
posts_count: 13
---

# Topics for Wallet Ring gathering tomorrow 15:30 in the workshop room of National House Smichov

This will be an unconference - so topics will be decided on the spot. I just want to throw in some ideas that I would like to talk about. Please add your ideas. This is mainly so people can decide between different tracks and *roughly* have some idea about the content.

- Wallet distribution: e,g, how do we get less reliant on google and apple here. Discuss alternatives to them like f-droid. Also think about the future - decentralized distribution systems anyone? Reproducible builds?
- Wallet reputation staking on standards? E.g. we agreed last year at DevCon3 on EIP681 and a lot of wallets did not yet implement it - which causes a lot of trouble. So one idea would be that projects could stake reputation on standards and it gets slashed when they do not implement it in the agreed timeframe. This reputation could then be used in the decentralized distribution systems mentioned above.
- Storage of private keys (currently extremely excited about the status.im hardware wallet: https://github.com/walleth/khardwarewallet )
- WalletConnect - how to push it forward and get more adoption (on wallet and application side) - Versioning/Upgrade paths/backward compatibility
- How to decentralize more (light client incentive layer like VipNode, ultra light clients, minimal verification clients like INCUBED) - other ideas? Classification
- mETHadata
- making wallets accessible on low end devices (e.g. nokia one) for the emerging world. Also how to make wallets work in bad network conditions
- Wallet (interoperability) comparison matrix

Meta:

- mission statement - suggestion: “Make wallets more useful, interoperable, user friendly, private, decentralized, secure, accessible.”
- SubRings?: mobile/desktop/hardware?

## Replies

**Tbaut** (2018-10-28):

Thanks a lot Ligi for all those great ideas.

Happy to share my experience with f-droid, building light-clients and possible enhancements.

---

**ligi** (2018-10-28):

[@Tbaut](/u/tbaut) that sounds great - looking forward to it!

I just got the information that the team from the status.im hardware wallet cannot be there as they have an important meeting at the very time our workshop is. As I really would like a session with wallet developers and them I suggest to do a pop-up session - perhaps in one of the breaks? Who would be in for this?

---

**wighawag** (2018-10-29):

Hi [@ligi](/u/ligi)

If there is interest I would like to present a scheme that would make web3 browsers more usable while keeping them secure.

I created a topic here for discussion : [3 Proposals For Making Web3 A Better Experience](http://ethereum-magicians.org/t/3-proposals-for-making-web3-a-better-experience/1586)

---

**ligi** (2018-10-29):

[@wighawag](/u/wighawag) Sounds great - please join us!

That said:

- I do not control the agenda - I just facilitate - so if/how much time the topic gets will be decided by the attendees
- Seems that our 1.5h will be jam-packed - so we will not have much time for each topic (so please try to be brief when introducing the topic)
- I believe wallet!=web3browser - yes currently they often get hand in hand - but I firmly believe they should be 2 separate entities (mainly for security reasons) - perhaps we should even craft a web3browser ring

---

**ligi** (2018-10-29):

PSA: the whole schedule is pushed back 30min - so we will start 16:00

and FYI: I have a Nokia one with me. So if any wallet dev wants to test his app on a very low end phone that is targeted for the emerging world - you are very welcome to use this phone at the session to test your apps!

---

**wighawag** (2018-10-29):

Actually, realised there is a web3 UX session. So whoever is interested in web3 browser security and usability, come there.

I ll join the wallet session too though as it obviously related.

Cheers

---

**brunobar79** (2018-10-29):

Notes from today’s meeting:

Imtoken: Popular in china, handling 10% of Ethereum transactions volume.

- Kaz -  dev
- Phillip - Business dev.

Status:

- Corey Petti - Security Eng.
- Michelle - Hardware wallet dev.
- Guy-Louis Gray - Product and biz

Walleth

- Ligi

MetaMask

- Bruno - Dev

Hardware wallet from status:

- Integration with phones and card reader
- Requires PIN, and has no screen
- There are other ones (UBI which use bluetooth)
- Would be cool to integrate with metamask (wallet connect maybe?) USB not an easy way through card reader
- Android support only (iOS is blocked because of limited NFC support)
- Status has a Java library already
- Public Repo: https://github.com/status-im/hardware-wallet
- Discussed the challenges of backing up cards
- Biometrics for PIN auth? Ideally would be a good 2nd factor auth. Could be added optionally
- BIP 44 for different set of keys for whisper / other identity scenarios (for ex. Door unlocking)
- Action items: Create a specific “room” on ETH-Magicians to follow up

Imkey

- Hardware wallet from imToken
- Works via Bluetooth
- Has a screen

Feel free to add anything I might have missed.

Great talking to you guys!

---

**ligi** (2018-10-29):

[@brunobar79](/u/brunobar79) thanks so much for taking notes and attending!

I will add some things when copying it over to the pop-up session. (PSA: these are the notes for the ad-hoc pop-up session about key management 11:30 and not for the wallet session 16:00 - especially at all the time-cops listening in - we did *not* use a time machine to post these notes before the session)

---

**thibmeu** (2018-10-29):

I would add a topic on offchain payments and how they should interface with existing wallet.

---

**seichris** (2018-10-30):

Someone proposed the topic of finding a common design system for DApps. I just wanted to note that Aragon just funded Beltran in defining a Web3 Design System. Link: https://github.com/lyricalpolymath/nest/blob/master/grants/Web3DesignSystem/roadmap.md

---

**taratan** (2018-10-30):

Notes https://hackmd.io/s/SJmJAB0sQ

---

**ligi** (2018-10-30):

Thanks to everyone attending. And a special thanks to [@taratan](/u/taratan) for note taking!!

PPS: I edited the notes a bit and invite everyone to do the same and add things they think are missing.

