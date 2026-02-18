---
source: magicians
topic_id: 2721
title: Security Review Period for Hardfork Roadmap
author: boris
date: "2019-02-22"
category: Working Groups > Ethereum 1.x Ring
tags: [security, istanbul, roadmap]
url: https://ethereum-magicians.org/t/security-review-period-for-hardfork-roadmap/2721
views: 1923
likes: 14
posts_count: 6
---

# Security Review Period for Hardfork Roadmap

I’ve added a section to the [Istanbul Roadmap page on the Ethereum wiki](https://en.ethereum.wiki/roadmap/istanbul) proposing a security review period for proposed Core EIPs.

This means having some people do security reviews – which might mean engaging external auditors. But it also means communication around the Core EIP proposals that are effectively Last Call, but focused on security issues. Pay attention, have a look, does this impact your current or future use cases.

I’ve suggested `2019-06-21` (June 21st), this is half way between the hard deadline for proposals, and the soft deadline for major client implementations.

## Replies

**AlexeyAkhunov** (2019-02-24):

It is a very good idea. However, I would invite to think about this a bit more. Giving extra time will not necessarily result in more reviews, as we have seen historically.

As I suggested in my [final part](https://medium.com/@akhounov/looking-back-at-the-ethereum-1x-workshop-26-28-01-2019-final-part-6-988134a36073) of Eth1x workshop blog posts, we may need to more “formally” appoint a reviewer (or two) for each change. Otherwise the time will drag on, and review will only happen just before the hard fork (and it does nowadays).

---

**boris** (2019-02-24):

I’m not suggesting more time.

Rather - a defined review period time where the specific purpose is security.

I also think we have to find funding to pay people for reviews. If people volunteer to do reviews as well — great! But I don’t think we can count on it.

Having people sign up to focus on reviewing all aspects of a change is definitely a good idea.

---

**maurelian** (2019-03-05):

Also relevant:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tintinweb/48/1450_2.png)
    [EIP: mandatory "Security Considerations" for EIPs](https://ethereum-magicians.org/t/eip-mandatory-security-considerations-for-eips/2839) [EIPs](/c/eips/5)



> Hi everyone,
> To better manage the security risks in the Ethereum Change Management Process we propose a change to the EIP minimum requirements to include a mandatory “Security Considerations” section for the documentation of security relevant information directly with the EIP.
> This proposal is adapted from the IETF’s Request for Comments (RFC) system (RFC 7322 - Section 4.8.5) where this is mandatory already.
> The Meta EIP is currently in Draft status. We would love to get you involved making …

I think embedding the security considerations into the EIP itself is important.

---

**boris** (2019-03-05):

Yeah there’s two parts to this. One is adding security requirements to EIPs, the other is a security review period for release planning.

This proposal is the latter ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) so: yes, AND.

---

**owocki** (2019-03-19):

For what it’s worth, Gitcoin has added a 20 ETH security bounty for EIPs which starts in Mid May.  https://github.com/gitcoinco/skunkworks/issues/89

