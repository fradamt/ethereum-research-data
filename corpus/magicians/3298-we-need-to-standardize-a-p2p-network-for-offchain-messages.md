---
source: magicians
topic_id: 3298
title: We need to standardize a P2P network for offchain messages
author: vbuterin
date: "2019-05-19"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/we-need-to-standardize-a-p2p-network-for-offchain-messages/3298
views: 3546
likes: 23
posts_count: 12
---

# We need to standardize a P2P network for offchain messages

There’s a lot of important use cases in ethereum applications that demand some kind of p2p broadcast network. Particularly:

- Mixers: for a mixer to actually be privacy-preserving, it can’t be you that directly pays the tx fee to claim funds from the mixer contract, as then the ETH you use to pay the tx fee becomes a deanonymization vector. So we need to have a system where users broadcast claim receipts (eg. containing ring signatures, ZKPs, etc) on a p2p network with bounties for whoever includes them, and an ecosystem of relayers emerges that includes them, pays the fees, and collects the fees from the bounties prescribed by the claim message / mixer contract.
- Multisig wallets: multisig wallets are currently inconvenient because they require maintaining two accounts, one being the “real” multisig wallet and the other a single-key wallet for storing ETH to pay fees. If instead multisig withdrawal messages are broadcasted via a p2p network and included by incentivized relayers, then we can remove the need for the second wallet.
- Transactions sending to ZK Rollup networks: users need to send transactions to relayers so relayers can package them up into a rollup transaction, but this requires a p2p network; otherwise, the solution that will likely win is the lazy one where users send their transactions directly to a single relayer (there’s also the intermediate solution where relayers register their IP addresses on a contract but… come on)

Note that none of these use cases require advanced functionality such as the ability to store messages that have been broadcasted for even a short duration, and they do not require 100% reliability; if sending a message fails, you can always resend. All that they require is a p2p network that ideally supports some notion of publishing on and subscribing to channels.

Candidates for this that I know about include libp2p and SSB, and presumably one could use Whisper for this if it’s ready though it may be overkill. One could simply use the same software stacks that ethereum 2.0 is using. However, it’s important to standardize this across all major ethereum wallets (full nodes, light nodes, Metamask, MyCrypto, MEW, Opera…) so that applications can rely on it as basic functionality, so that it doesn’t become a special tool that one wallet uses to secure a dominant network effect.

## Replies

**MadeofTin** (2019-05-20):

*eth1X working group intensifies*

---

**fubuloubu** (2019-05-21):

This is a really necessary initiative!

My vote is for libp2p to match with eth 2.0 stack.

---

**yoav** (2019-05-22):

A standardized p2p layer would definitely be useful, but as for the specific use cases above, doesn’t the Gas Stations Network ([EIP-1613](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1613.md) /  [GSN repo](https://github.com/tabookey/tabookey-gasless)) solve them without requiring a p2p layer?

**Mixers** - The mixer implements the RelayRecipient interface and compensates relayers using the mixed deposits.  The client (an ETH-less address) randomly selects a relayer from the RelayHub contract and sends the transaction. The relayer calls the mixer’s accept_relay_call() which verifies the ring signatures / ZKPs and confirms relay fee paid by the mixer.  Then, the relayer delivers the transaction and the client gets the ETH.

**Multisig wallets** - the multisig wallet implements RelayRecipient, with an accept_relay_call() that returns true only for the multisig participants, and compensates the relayer for their transactions.  ETH-less signer selects a relayer from RelayHub, sends the transaction, the relayer checks accept_relay_call(), delivers the transaction, and gets compensated.

**Transactions sending to ZK Rollup networks** - requires GSN relayers to implement packaging into rollup transactions, but otherwise doesn’t change the model.  Why do you consider registering IP addresses (or rather, URLs) on a contract a bad thing?  Ethereum already has this infrastructure (GSN has active relayers and is going on mainnet very soon), and will already have incentivized relayers registered in the RelayHub contract, so we might as well reuse them for ZK rollup.

I’m not saying we don’t need a standard p2p layer, but for many use cases there may be a simpler solution that reuses existing infrastructure and can work in a standard browser without having to deal with the connectivity nightmare of maintaining p2p connections across firewalls and NAT gateways.  This is especially true for the **Multisig wallets** use case which is often used in enterprise networks, where p2p protocols are likely to be blocked but web is permitted.

---

**greg** (2019-05-24):

We just started working on this after competiting at ETHNY (https://mobile.twitter.com/_tmio/status/1130246581297516545). We are releasing a POC of the specification today and encourage everyone to contribute to the minimmal viable messaging layer.

The actual messaging is being standardized to be extremely simple, and we will have improvement proposals to fix add different protocols such as ethereum transactions (our demo above from ethny had an ethereum tx as an example).

---

**christoph2806** (2019-06-27):

I think Gas Station Network by TabooKey is solving some of these issues, offering a relay service for transactions (https://medium.com/tabookey/1-800-ethereum-gas-stations-network-for-toll-free-transactions-4bbfc03a0a56 and https://github.com/tabookey/tabookey-gasless), they have also written an EIP 1613 to standarize these relay networks (https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1613.md)

But I think your intention is more on the system how relayers and transaction senders can communicate, and therefore an easy to use P2P network would be great. Why can’t whisper serve as such?

---

**d1ll0n** (2019-07-02):

(post withdrawn by author, will be automatically deleted in 24 hours unless flagged)

---

**d1ll0n** (2019-07-02):

(post withdrawn by author, will be automatically deleted in 24 hours unless flagged)

---

**d1ll0n** (2019-07-04):

I tried posting this before and the messages got flagged, I tried deleting them because I couldn’t make any edits but I still see them here, so if you guys see the old ones sorry about that.

I started working on a set of tools I’m calling Ethernet. The idea is to have a p2p network where peers are identified by Eth addresses, with support for the Signal protocol and a key derivation scheme called TreeKEM, which is an asymmetric DH ratchet for large groups (basically Signal protocol for groups, but far more efficient than the methods used by WhatsApp or Signal).

Here’s the signal for secp256k1 package https://github.com/d1ll0n/eth-signal

I don’t have time to work on this right now, I plan on getting back to it when my work schedule slows down a bit.

I forked a bunch of the libp2p repos to work with eth addresses as peer ids. Main repo here https://github.com/d1ll0n/eth-libp2p

I want this network to support ENS usernames as well as a new PKI I am working on called Identity, which is sort of like ENS + Keybase.

---

**fubuloubu** (2019-07-05):

Really weird that it got flagged, but sounds like a cool project. I would strongly caution against calling it “Ethernet” though, unless you enjoy the ire of millions of devops engineers worldwide ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9)

It was a clever name though!

---

**jpitts** (2019-07-07):

RE: the flagging, Sorry [@d1ll0n](/u/d1ll0n), Discourse has a tendency to do this for new users, I’ll keep an eye out for these!

---

**d1ll0n** (2019-07-15):

Lol yeah I may end up changing the name, the important thing is to make it work first though.

[@jpitts](/u/jpitts) no worries, I think it was just because I tried putting a bunch of links to projects.

Here’s the treekem library, I worked on this a bit and then a friend fixed some errors and refactored it to typescript. https://www.npmjs.com/package/eth-treekem

