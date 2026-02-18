---
source: magicians
topic_id: 22383
title: Event Ticketing infrastructure
author: MidnightLightning
date: "2025-01-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/event-ticketing-infrastructure/22383
views: 104
likes: 0
posts_count: 4
---

# Event Ticketing infrastructure

I think a key use-case that NFTs can (eventually) provide a better option than current (centralized, “web 2”-style) systems is event tickets to physical events. The issuing, secondary selling, and validating at the entrance to events.

For digital events, having a specific NFT be required to gain entrance is trivial, as visitors can join the digital event from their own home or other space they are confident of their own physical safety and preventing of eavesdropping. But thinking of physical events, I think there’s a decent amount of infrastructure that is needed to make NFT-gating physical events be safe and easy. So, setting up a thread here to do some musing:

Let’s call the NFT that needs to be owned to get access to the event the Key NFT:

The system needs to allow for event attendees to **not have to carry the Key NFT on their person** (owned by a wallet in a mobile device they have with them at the event). For Key NFTs that are designed as “lifelong membership passes” to events like this, having that NFT on a software wallet at the event is a liability for the mobile device to get hacked/stolen and the Key NFT stolen with it.

The system needs some form of fallback for **offline gatekeeping**. At the door to the event, if both the event attendee and the bouncer doing the checking need live network access (to a custom website or to the blockchain network to verify data), that’s a weak link, and could cause complications. It also limits the system to events that are in areas that have good network coverage.

The system should make it easy for new buyers of a Key NFT to know if they are getting access to the event or not. If there is a separate “Ticket NFT” that Key NFT owners are allowed to claim, it should be easy for newcomers to tell **if a given Key NFT has “claimed” their Ticket NFT yet or not**. It should especially avoid a situation where a Key NFT could be listed for sale as still having its claim active, having a new buyer submit a transaction to buy the Key NFT, and have the original owner of the Key NFT front-run the transaction by claiming the Ticket NFT and still have the new buyer’s purchase transaction go through.

# The Infrastructure

To solve those needs, we should build a platform that includes:

A Ticket NFT system where event organizers can launch a new event token, set which other NFT is the Key NFT, and set purchase price and max event capacity. This can be an ERC-1155 token, where each new event is a new “class” of tokens issued with it. ERC-2135 can also be baked into it, as a standardized way to show when a Ticket NFT has been redeemed.

A web front-end that uses the Ethereum Attestation Service (EAS) to make a QR-code-embeddable ownership claim. This would serve as the link between a human standing at the door, and which address they’re attesting to be the owner of. If the event venue has network access, the person seeking access can sign the attestation right there. Or it could be created beforehand and printed out. This should be done as an off-chain signature, as merely possessing it is being used as the link to the physical world that the human that is carrying the signed attestation is the person allowed to use it. The EAS website already has a generic explorer that allows for verifying off-chain messages, which a bouncer could use to verify a signature. EAS messages have a standard for embedding into a QR code, so a bouncer would just need to scan an attendee’s screen or printed QR code to verify it.  This still requires the attendee to access a website at some point before the event, but they could do the attesting and print out the QR code in advance, if they wanted to.

EAS is not an EIP, but is designed to be a universal tool, so seems a good fit for this last-leg verification.

If an ERC-1155 token was created for all to use as a Ticket NFT, and a generic web interface for attendees to delegate and attest their ownership, is that all that would be needed to bootstrap event-running via NFTs? If an event has a limited number of tickets to sell, and they limit to only one per Key NFT, having a way to easily tell which Key NFTs haven’t “claimed” yet is still a problem to be solved…

## Replies

**Atenika.Protocol** (2025-01-08):

what the status ? whre is it going ?

---

**Atenika.Protocol** (2025-01-09):

Is there any software develope ? and or mobile app  already ?

---

**MidnightLightning** (2025-01-12):

The status is “gathering feedback”. If no one comes up with any strong cases against this structure (ERC-1155 tickets, with EAS attestations), I plan to start building an implementation of it around Q2 2025.

