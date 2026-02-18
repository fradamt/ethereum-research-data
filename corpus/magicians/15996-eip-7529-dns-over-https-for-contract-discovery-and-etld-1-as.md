---
source: magicians
topic_id: 15996
title: "EIP-7529: DNS over HTTPS for Contract Discovery and eTLD+1 Association"
author: TtheBC01
date: "2023-10-04"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7529-dns-over-https-for-contract-discovery-and-etld-1-association/15996
views: 2764
likes: 6
posts_count: 19
---

# EIP-7529: DNS over HTTPS for Contract Discovery and eTLD+1 Association

At Snickerdoodle Labs, we’ve had good success leveraging whats proposed in this draft EIP in our own protocol. We decided to write it up as a proposal and see if the Ethereum community would also find it useful.

This proposal describes a simple standard to leverage TXT records to discover smart contracts and verify their association with a known DNS domain. This is enabled by the relatively recent support for DNS over HTTPS (DoH) by most major DNS providers.

This is my first time attempting to contribute an EIP, I’ve tried my best to stick to the contributor instructions, so apologies if I’ve missed a step.

Link to draft pr: https://github.com/ethereum/EIPs/pull/7815

## Replies

**SamWilsn** (2023-10-30):

Hey! Haven’t had a chance to look at your EIP in depth yet, but [Add EIP: Domain-contracts two-way binding by VenkatTeja · Pull Request #6807 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6807) seems like it might be similar. Perhaps your team and [@web3panther](/u/web3panther) would like to coordinate?

---

**TtheBC01** (2023-10-30):

cool, we’ll check it out!

---

**SamWilsn** (2023-10-30):

Why mention DNS-over-HTTPS and not DNSSEC? I was under the impression that they accomplish roughly similar goals.

---

What benefits does including the TXT record have over simply serving the dapp over HTTPS? You can still check that the domain is in the contract for the “cross-checking” you mention.

---

I’m not entirely sure what the benefit of checking the domain in the contract is. If the domain is compromised, can’t the attacker point to a different contract that’s malicious?

If the “good” contract is used by an unapproved domain, is that bad?

This part of the proposal just seems to hurt the modularity/lego bricks philosophy of Ethereum contracts, locking them to a single domain. Imagine if the Uniswap contracts charged a fee to be included in their approved domains list!

---

**TtheBC01** (2023-10-30):

Thanks for the engagement [@SamWilsn](/u/samwilsn)! So I wrote up some responses for you here:

1. DoH is just an interface specification to a DNS provider who then uses DNSSEC to securely fetch the requested record. It is our understanding based on their docs that Cloudflare actually uses DNSSEC upstream of their DoH API. DoH is just the standard that allows for direct querying of DNS records straight from the browser, so technically DoH isn’t what’s really important, is the TXT record, but DoH is the enabling RFC standard for dApps to access DNS records directly. If you think it makes sense, we could simply reference the use of TXT records rather that specifying DoH specifically, since that seems to be the way to access DNS records from the browser without a proprietary API.
2. One high-value use case here is if you are on a third-party dApp or regular webapp that allows for the exploration or use of smart contracts deployed by other companies/projects, this lets the user-client independently verify association of the smart contracts with the aledged domains they claim to be associated with. The other high-value use case is that I can directly ask a DNS domain if any smart contracts are associated with it on a given network, then quickly verify that by an on-chain lookup which could be an interesting capability for browser-extension based wallets or even traditional web-crawlers that want to add on-chain asset searchability.
3. So I agree, an attacker who has compromised your DNS security could point users to a malicious contract. Using DNS records to “discover” a contract is indeed susceptible to DNS poisoning. However, I argue that if the DNS records of your business domain are under attack, you’re already in serious trouble, IMO. Open to further discussion on this point for sure.
4. As far as a “good” contract being used by an unapproved domain, that is fine, we don’t intend for this ERC to prevent other sites from using an asset, but to allow other tools/libs to verify they are interacting with an asset from a known DNS domain. Example: I’m on uniswap and I want to be sure i’m actually swapping between authentic PYUSD, and USDC; this standard could be used to ensure that the assets in the pool are actually the ones associated w/ paypal.com and circle.com. Additionally, it could be useful for a google-like token search functionality within Uniswap where a user could just type in “Paypal” or “Circle” and find tokens issued from those businesses.
5. In regards to locking smart contracts to use by a single domain (as mentioned in some of the other points) this won’t lock down usability whatsoever (as discussed in point 4) unless that is what the client-side software using the ERC decides to do with it. For example, if Metamask used this ERC, they might pop up a warning if the user is about to make a transaction with a smart contract that is not associated with the domain the user is currently on. Additionally, a contract can be linked to more than one domain if the use case makes sense.

Last thing here; if anyone comes across this ERC and is interested to try this in their own application, Snickerdoodle has published a helper package for fetching and cross-checking domains/contracts as specified in this proposal:

https://www.npmjs.com/package/@snickerdoodlelabs/erc7529

---

**SamWilsn** (2023-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tthebc01/48/8185_2.png) TtheBC01:

> DoH is just an interface specification to a DNS provider who then uses DNSSEC to securely fetch the requested record. It is our understanding based on their docs that Cloudflare actually uses DNSSEC upstream of their DoH API. DoH is just the standard that allows for direct querying of DNS records straight from the browser, so technically DoH isn’t what’s really important, is the TXT record, but DoH is the enabling RFC standard for dApps to access DNS records directly. If you think it makes sense, we could simply reference the use of TXT records rather that specifying DoH specifically, since that seems to be the way to access DNS records from the browser without a proprietary API.

Ah, that’s interesting! I didn’t realize that browsers didn’t directly validate DNSSEC. So this whole proposal relies, for browser extension wallets anyway, on DoH? A native wallet could use DNSSEC directly, but those are a rare breed. Makes sense to keep it as DoH in the proposal then.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tthebc01/48/8185_2.png) TtheBC01:

> One high-value use case here is if you are on a third-party dApp or regular webapp that allows for the exploration or use of smart contracts deployed by other companies/projects, this lets the user-client independently verify association of the smart contracts with the aledged domains they claim to be associated with.

I’m not sure I understand what kind of dApp you’re describing. Let me know if I’m completely off base here:

I imagine I’m in an android app called `MegaWeb3App` that has built a uniform UI for several popular dApps. I can browse their collection of UIs, and pick Uniswap. So `MegaWeb3App` dutifully checks the contract it plans to interact with against the domain `uniswap.org`’s TXT record, and the domain against the contract’s on-chain allowlist.

If the app is malicious, it can straight up lie and say it did the validation. If the domain is compromised, it prevents the user from interacting with the legitimate contract. If the contract is compromised, and the Uniswap team updated their TXT record, I suppose this would catch that. Just seems like a small win.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tthebc01/48/8185_2.png) TtheBC01:

> The other high-value use case is that I can directly ask a DNS domain if any smart contracts are associated with it on a given network, then quickly verify that by an on-chain lookup which could be an interesting capability for browser-extension based wallets or even traditional web-crawlers that want to add on-chain asset searchability.

Hm, that’s an interesting idea. Could also be done with some [Open Graph](https://ogp.me/)-style tags.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tthebc01/48/8185_2.png) TtheBC01:

> So I agree, an attacker who has compromised your DNS security could point users to a malicious contract. Using DNS records to “discover” a contract is indeed susceptible to DNS poisoning. However, I argue that if the DNS records of your business domain are under attack, you’re already in serious trouble, IMO. Open to further discussion on this point for sure.

For sure! I think I was looking at this proposal from a security perspective because I had just finished going over [EIP-6807](https://github.com/ethereum/EIPs/pull/6807). I’m wondering if it’s possible to have an on-chain timelock, so that you have some time to react if your DNS is compromised. So it’d be (1) update DNS records (2) prove on-chain (3) timelock period (4) domain’s allowlist is updated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tthebc01/48/8185_2.png) TtheBC01:

> As far as a “good” contract being used by an unapproved domain, that is fine, we don’t intend for this ERC to prevent other sites from using an asset, but to allow other tools/libs to verify they are interacting with an asset from a known DNS domain. Example: I’m on uniswap and I want to be sure i’m actually swapping between authentic PYUSD, and USDC; this standard could be used to ensure that the assets in the pool are actually the ones associated w/ paypal.com and circle.com. Additionally, it could be useful for a google-like token search functionality within Uniswap where a user could just type in “Paypal” or “Circle” and find tokens issued from those businesses.

So it isn’t necessarily about the top-level contract. Neat. That clears up a lot of the use cases I think.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tthebc01/48/8185_2.png) TtheBC01:

> In regards to locking smart contracts to use by a single domain (as mentioned in some of the other points) this won’t lock down usability whatsoever (as discussed in point 4) unless that is what the client-side software using the ERC decides to do with it. For example, if Metamask used this ERC, they might pop up a warning if the user is about to make a transaction with a smart contract that is not associated with the domain the user is currently on. Additionally, a contract can be linked to more than one domain if the use case makes sense.

Yeah, that makes a lot of sense. Thanks for clearing that up!

---

Putting my editor hat back on, I think a lot of this content would go very well in your motivation section!

---

**TtheBC01** (2023-12-12):

Adding a link to the latest write up for ERC-7529 in the new ERC repo:

https://github.com/ethereum/ERCs/pull/33/files

---

**TtheBC01** (2024-03-20):

I got the opportunity to present ERC-7529 at the ETHDenver EIP Day and got some great feedback from the attendees. I’ve incorporated their suggestions in an update PR for the draft ERC here:

https://github.com/ethereum/ERCs/pull/331

---

**xinbenlv** (2024-03-24):

Hi authors of ERC-7529, this is Victor, an EIP editor and current operator of AllERCDevs.

I like to invite you to our next AllERCDevs meeting (online) to present for 10min of your ERCs if you are interested!

AllERCDevs is a bi-weekly meeting for ERC authors, builders and editors to meet and help the drafting and adoption of an ERC. The next one is 2024-04-02 UTC 2300, let us know if this time works for you, I can put this ERC in the agenda, or you can add a response directly at [(Future) 2024-04-02 (E2S2) AllERCDevs Agenda Thursday (Asia/US friendly time) · Issue #19 · ercref/AllERCDevs · GitHub](https://github.com/ercref/AllERCDevs/issues/19)

---

**TtheBC01** (2024-03-25):

absolutely! I’ll sign us up

---

**xinbenlv** (2024-03-25):

Cool, we look forward to it!

---

**sullof** (2024-03-27):

I like the proposal.

I suggest to change the name of

```auto
function getDomain(string calldata domain) external view returns (bool);
```

What you are doing there is checking if that smart contract has a specific domain.

Calling the function with a more specific `hasDomain` or something similar could make it clearer.

*getDomain* would make sense if, for example, you put the domains in an array and get a domain by the index in the array.

---

**TtheBC01** (2024-03-27):

ya, thats a good point. I was actually thinking the same thing the other night.

What about getETLDp1()?

---

**sullof** (2024-03-27):

I would not say it make it clearer ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**TtheBC01** (2024-03-27):

I’ll riff on a better name, definitely open to suggestions

---

**sullof** (2024-03-27):

I think `checkDomain` may be good

---

**TtheBC01** (2024-03-27):

i like that, definitely clearer than “get”

---

**TtheBC01** (2024-03-29):

Took your suggestion and updated the draft to use `checkDomain` instead.

---

**fulldecent** (2024-04-02):

I think this approach is needed–lean on DNS for reputation management.

---

But this is limited by the size of TXT records. We are using `string[]` when there is a more scalable `map<>` available.

Please see how DKIM uses DNS for this. We could allow querying arbitrary contracts using a different approach like this to get a yes/no answer:

TXT 0x1234543456543456.1._domaincontracts.example.com “yes”

And then

TXT primary.1._domaincontracts.example.com “0x1234543456543456”

to allow discovery.

---

Instead of eTLD+1 there is an existing infrastructure for this. Please see the Mozilla Public Suffix List (PSL). We can specify that a client will query hierarchally up to the PSL+1.

