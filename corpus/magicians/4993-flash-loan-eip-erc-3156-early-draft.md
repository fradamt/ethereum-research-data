---
source: magicians
topic_id: 4993
title: Flash Loan EIP - ERC-3156 - Early draft
author: albertocuestacanada
date: "2020-12-03"
category: EIPs
tags: [defi, erc-3156]
url: https://ethereum-magicians.org/t/flash-loan-eip-erc-3156-early-draft/4993
views: 2327
likes: 8
posts_count: 7
---

# Flash Loan EIP - ERC-3156 - Early draft

Hi guys, I’m drafting a Flash Loan EIP with fubuloubu, onewayfunction and hexonaut.


      ![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/n71oYp2gTn6TOCwX_YZymQ)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###










It’s my first, so I would appreciate some advice on language, content gaps, and anything that you might see it lacks. I don’t want to make it too big, I would like just a standard so that integrating flash loans is easier, and so that people avoid some of the pitfalls I’ve fallen into ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=15)

Also, discussion on flash loans is always fun.

## Replies

**jpitts** (2020-12-04):

This is great! Here are some comments;

This should be positioned as an “ERC” (but still would go through the EIP process).

“Simple Summary” - After the description of what flash loans are, this section needs more of a summary of the ERC itself.

“Motivation” - Links to documentation of AAVE, DxDy, Yield’s flash loan interfaces would be helpful here. Also, it could start w/ a more general description of the technical reason the interface is needed in order for a flash loan to function.

“Rationale” - This should start w/ a general rationale about why the ERC is needed w/ its general approach, etc. The rationales for each of the methods are still useful though.

Hope this helps!

---

**albertocuestacanada** (2020-12-05):

@fifikobayashi added a good chunk of technical knowledge to the motivation and security consideration sections, and following that lead I filled the remaining gaps and added a couple other exploits I know of.

Does anyone have any advice on polishing the document further? I was advised to not write too much, so maybe the security considerations can be tightened somehow.

---

**albertocuestacanada** (2020-12-08):

Hey guys, I’ve now opened this in the EIP repo:

https://github.com/ethereum/EIPs/pull/3156

Thanks!

---

**albertocuestacanada** (2020-12-09):

And it’s been merged! ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=9)

---

**MicahZoltu** (2020-12-31):

Why does the receiver have to be the same person that gets the callback?  What if you want to loan ETH to address X but callback to address Y?

Why not allow the caller to decide the callback and provide all of the parameters?  They already can query for fee, and the amount being loaned is known to the caller in advance of the call.  So you could just do `receiver.call(_calldata)` which would allow the caller to also decide what method was called.

---

**albertocuestacanada** (2021-01-01):

Hi Micah, thanks a lot for the questions. I replied [here](https://ethereum-magicians.org/t/erc-3156-flash-loans-review-discussion/5077/2).

