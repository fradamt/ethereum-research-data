---
source: ethresearch
topic_id: 5720
title: "Highlight: Robin Hanson's more owner-forgiving modified Harberger tax"
author: vbuterin
date: "2019-07-10"
category: Economics
tags: []
url: https://ethresear.ch/t/highlight-robin-hansons-more-owner-forgiving-modified-harberger-tax/5720
views: 2318
likes: 10
posts_count: 2
---

# Highlight: Robin Hanson's more owner-forgiving modified Harberger tax

From [Fine Grain Futarchy Zoning Via Harberger Taxes](https://www.overcomingbias.com/2019/01/fine-grain-futarchy-zoning-via-harberger-taxes.html) :

> Added 11pm: One complaint people have about a Harberger tax is that owners would feel stressed to know that their property could be taken at any time. Here’s a simple fix. When someone takes your property at your declared value, you can pay 1% of that value to get it back, if you do so quickly. But then you’d better raise your declared value or someone else could do the same thing the next day or week. You pay 1% for a fair warning that your value is too low. Under this system, people only lose their property when someone else actually values it more highly, even after considering the transaction costs of switching property.

There’s many different ways to implement similar ideas that have slightly different user experience. One possibility is to set up a system where users pay the Harberger tax by prepaying funds into a contract, and there exists a separate mechanism where users can submit bids for any item of property; each bid must be fully collateralized. The tax rate that the current owner pays is computed based on the value of the highest bid. The owner has the ability to sell to the highest bidder at the bid price at any time (or the sale happens automatically if the prepaid tax contract runs out of money). This system is more favoring because sales are owner-initiated rather than buyer-initiated. One can also provide owners a further measure of stability by limiting the rate at which their tax can go up (eg. to one doubling per week).

This kind of owner-forgiving Harberger tax is not very useful for the “market-based eminent domain” use case: if Elon Musk suddenly puts up bids for an entire strip of houses going through a city to build a hyperloop there, then once some owners sell the other owners will know they can extract high prices and would be able to raise their prices (whereas with the traditional harberger tax everything would get snapped up at once). However, it seems very useful in cases where you’re not expecting buyers to want to buy a large set of items at the same time, eg. ENS domains.

## Replies

**skilesare** (2019-07-11):

I’ve spent a good deal of time thinking about this and I think it makes sense to start something like this with more fungible assets like corporate shares.  In the past I’ve proposed something along the lines of a limited liability tax where any entity that is granted limited liability by a governing entity is subject to a tax.  Each year, x% of their stock is uniformly taken from all account holders and put up for public auction.  Once the auction closes the original owners have the right to buy back the stock at the highest bid.  If they elect not to, it goes to the bidder.  All proceeds go to the benefit of the commons.

Smart contracts could make the administration of this trivial.  If applied to the US Economy a 10% on the Russell 3000 gets pretty close to replacing the US Budget. If you extended this to private companies things get really interesting.  Personal income tax in the US could be just about eliminated.  I’m still waiting for governments to figure out how much easier taxation gets with crypto-economic systems.

