---
source: magicians
topic_id: 13126
title: "ERC-5023: Shareable Non-Fungible Token"
author: jpitts
date: "2023-03-02"
category: ERCs
tags: [nft, token, shareable]
url: https://ethereum-magicians.org/t/erc-5023-shareable-non-fungible-token/13126
views: 564
likes: 6
posts_count: 6
---

# ERC-5023: Shareable Non-Fungible Token

As [@yaruno](/u/yaruno) gave a lightning EIP talk about this today, I am posting this to get feedback.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5023)





###



An interface for creating value-holding tokens shareable by multiple owners

## Replies

**yaruno** (2023-03-03):

Was great to see you all, and hope to see you also in the ETHDenver ![:sunglasses:](https://ethereum-magicians.org/images/emoji/twitter/sunglasses.png?v=12) Please leave feedback about the presentation and if our EIP and our project peaked your interested checkout atarca.eu . We’ll have [ATARCA Seminar Week - ATARCA](https://atarca.eu/seminar/) on next week online about how digital economies can be governed with anti-rival digital tokens such as sNFTs.

---

**stoicdev0** (2023-03-03):

Nice idea. I was recently thinking about NFTs which are songs and can be duplicated/shared under some conditions and I think this interface it’s the perfect minimal thing you’d need.

Any special reason why you are restricting transfer on the implementation?

Also, I **think**  you should increment the `_currentIndex` on the `share` function.  It’s always nice to have tests included for the reference implementations.

Edit: I just saw this is already final

---

**yaruno** (2023-03-06):

Short answer for restricting use of transfer method was that we wanted to create ‘soulbound’ shareable NFTs in our research project. I agree that tests would be great for refence implementations, though the official EIP/ERC document is a bit restrictive format to include tests.

But to add to that I really like [@xinbenlv](/u/xinbenlv) presentation at ETHDenver about the ERCRefs that should scratch this itch. I’ll try to get our projects reference implementation added to [GitHub - ercref/ercref-contracts: ERC Reference Implementations](https://github.com/ercref/ercref-contracts) .

---

**yaruno** (2023-03-06):

I’m also adding here a blog post that I wrote a couple of months ago where I reflected our EIP journey. It contains some self-reflection and some advice and links to resources for prospective EIP authors. Maybe it’ll be helpful for someone who stumbles upon this discussion.

https://medium.com/@jarno.marttila/eip-process-reflecting-our-eip-5023-journey-9fc4d53f8a0f

---

**yaruno** (2023-04-30):

In case someone gets interested on the deeper reasoning side of the utility and development of shareable NFTs. Here’s our research paper on development of sNFT called [Digital Protocols as Accounting and
Incentivization Mechanisms in AntiRival Systems - Developing a Shareable Non-Fungible Token (sNFT)](https://www.etla.fi/wp-content/uploads/ETLA-B281-05-article.pdf) .

