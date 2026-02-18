---
source: ethresearch
topic_id: 832
title: Dynamic per-person-capped ICOs
author: vbuterin
date: "2018-01-21"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/dynamic-per-person-capped-icos/832
views: 2008
likes: 1
posts_count: 3
---

# Dynamic per-person-capped ICOs

Rightly or not, it seems to be considered virtuous for ICOs to sell at below market value - even if there are, for example, $120 million worth of interest in participating at a $120 million valuation, it’s considered greedy to either accept the full $120 million, and possibly even (see Gnosis) to accept some limited amount at a super-high valuation set by the market; rather, one should sell to purchasers an even smaller amount, and on even better terms, than they are willing to offer.

In such a sale, in general we can expect token prices to predictably rise after the sale. Some also suggest that this has positive community dynamics, as a community is happier if most of them experience rising prices, and reduces regulatory risk, because (i) smaller ICO size means less scrutiny, and (ii) regulatory action often results due to complaints, and complaints are more likely if participants experience losses, which are less likely here.

However, such sales have an inherent flaw: if a sale is oversubscribed, then everyone has a large incentive to get in, and to use unintended mechanisms to compete with everyone else to do so. If the mechanism is first-come-first-serve, then everyone will pay super-high gas fees. Very often, the mechanism is some opaque registration process, in which case well-connected crypto elites get in.

I propose an egalitarian alternative. Users whose accounts are confirmed as corresponding to unique humans (eg. through PICOPS) can send any amount of ETH into a contract with a defined contribution time, as well as a defined TOTALCAP (eg. 10000 ETH). When the sale ends, there are two cases:

1. The total amount sold is less than or equal to the TOTALCAP. In this case, everyone gets an allocation equal to the full amount of ETH they sent.
2. The total amount sold is more than the TOTALCAP. In this case, the contract selects that highest possible per-person cap N such that, if who anyone bought more than N had the excess refunded, the total amount still in the contract would be less than or equal to the TOTALCAP. Anyone who bought more than N has the excess refunded, and everyone gets an allocation equal to min(what they originally sent, N).

One can compute this by maintaining a data structure that stores all purchases in sorted order of size. Once the sale ends, one can repeatedly call a function to crawl from the end of the data structure (ie. the largest purchaser), saving along the way the total amount of ETH in the purchases already crawled through (HIGHTOTAL) to the point where, for the first time, the crawler is at the P’th highest purchaser, and TOTAL - HIGHTOTAL + CURPURCHASE * P < TOTALCAP. At this point, the per-person cap is set (one can even linearly interpolate to find the per-person cap between two purchase amounts that gives a total of exactly TOTALCAP), and everyone can send a transaction to finalize their purchase and refund any remaining ETH.

This ensures that consumer surplus from an oversubscribed sale is distributed in an egalitarian way, and ensures a wide coin distribution. The main weakness of this scheme is that it creates incentives to buy PICOPS accounts or repeatedly ask one’s friends to buy in ICOs on one’s behalf. PICOPS account selling can be prevented by identity services that make sure any individual always has the ability to reset their identity to another account, making it very risky or inconvenient to buy accounts; only testing such a scheme in real life can reveal how the second issue plays out.

## Replies

**Benk10** (2018-01-21):

This sounds like a good mechanism, but unfortunately only in theory.

I think that in most cases, it’s too easy to for the same person to use multiple identities in the sale.

The problem I see that it might cause is when the TOTALCAP is extremely low compared to the amount of ETH received *and* big investors used multiple identities. In such a case you might end up restricting only the small investors who invested more per account but less per real participant.

---

**MicahZoltu** (2018-01-21):

> Rightly or not, it seems to be considered virtuous for ICOs to sell at below market value

This is because an ICO that sells *at* market value cannot be flipped for a profit by ICO buyers.  Thus, ICO buyers *hate* ICOs that sell at market value because there is not free money left on the table for them.

> Users whose accounts are confirmed as corresponding to unique humans

This is still an unsolved problem.  All you can do is increase the cost to a Sybil Attack, you cannot prevent it.  The same things that increase the cost of a Sybil Attack also increase the cost to legitimate users, and in most cases the cost on legitimate users is *higher* than that on the attacker because the attacker benefits from scale and experience.

While full on banking-level KYC certainly increases the barrier to entry for a Sybil attacker more than SMS or similar, forging of passports to be “good enough to pass banking KYC” is not an unsolvable problem and you can just buy legitimate registrations from real humans with real passports (which is sometimes cheaper).

If you *know* that the ICO is going to be oversubscribed (and thus easy to flip at profit), you simply need to calculate the cost of the Sybil attack (per fake account) and Sybil attack it until such time as it is no longer profitable enough to continue to do so.  For a well funded attacker flipping an ICO at an estimated 10% profit (risk adjusted), if each account cost $10 to create (labor, engineering, etc.) then it is profitable to Sybil attack the system until such time as each account only gets you $100 more investment.  For a lot of ICOs, this point is not reached until you control the vast majority of the ICO, at which point available capital is a more likely limiting factor.

So, by making it harder for legitimate users to participate in the ICO, and to capitulate to people who *demand* free money be given to them (or else they’ll turn you in to the SEC), you have effectively not solved any problem.  You have simply raised the barrier to entry, thus edging out casual attackers and leaving room only for “big business” attackers.  This is similar to how the government capitulates to lobbyists and ends up allowing big companies to entrench themselves by preventing smaller operations from competing.  Do we really want ICO attacking to be a “big business” thing?

---

I feel like we would be better off coming up with a more direct bribery system for bribing people to not turn the company in to the SEC, rather than giving away free money to the best attacker.

---

Side note: The scheme you have described has been tried before (e.g., 0x), and it was Sybil Attacked pretty badly, by what appears to be numerous attackers who walked away with a not-insignificant share of the pie.  This was even with 0x keeping how they were going to run the ICO close to the vest in an attempt to reduce the time the attackers had to engineer the attack.  If this strategy is common, the attackers will build up tool chests that simplify the process for them (reducing their costs).  ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

