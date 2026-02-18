---
source: magicians
topic_id: 13710
title: "[Draft] EIP Meta: Permit to Link"
author: xinbenlv
date: "2023-04-06"
category: EIPs
tags: [eip, governance]
url: https://ethereum-magicians.org/t/draft-eip-meta-permit-to-link/13710
views: 667
likes: 0
posts_count: 1
---

# [Draft] EIP Meta: Permit to Link

*This DRAFT is not ready for review.*

On a high level, with my experience as EIP Author, I subjectively believe it’s important to let authors cite links when they believe it’s important to make their argument. Today, with EIP-5757 the policy is too restrictive, hence I want to work on an argument to propose better permit to link.

It’s understandable that some EIP editors held strong opinion and prefer to link to a very restrictive and small set of allowlisted sources as demonstrated in previous discussion and the introduction of EIP-5757. I disagree and understand the sentiment of not repeatedly debate about this issue. Therefore, this Draft is meant to be prepared for a longer time range, (e.g. in 12-18 months) to form community consensus and revisit this decision of introducing EIP-5757. This EIP is a working draft and is not ready for review. *Comment is welcomed but not required, please feel free to ignore*.

On [EIPIP Meeting #78](https://github.com/ethereum-cat-herders/EIPIP/issues/224), editors debated one question, should Yellow Paper be allowed to link from EIP repository.

TODO([@xinbenlv](/u/xinbenlv)): to add argument about both sides why Yellow Paper should and should not be linked from EIP repositories.

### Records

#### 2023-04-06 Example of Final ERC being out of date

[@matt](/u/matt) On the EIPIP meeting April 5th yesterday, we debated about link to Yellow Paper. “Yellow Paper” is out of date and lack of maintenance, as the main argument for not permitting to link to Yellow Paper.

To counter this argument I cited final ERC could be out of date yet it’s still permitted to be linked to final ERCs.  [@matt](/u/matt)  asked: ERC are only Final to be linked and they will not be out of date? I didn’t provide a good answer yesterday

Today I ran into one: ERC-137 is an example where a finalized ERC could be out of date. The reason it’s out of date is that its solidity version language is out of date and keywords like “constant” are updated to “pure”.

I like to put this into the record of the debate about permit to link as an evidence that legit links could be out of date in some parts of this document, and subjectively I believe it’s still useful for author to cite and use that to support their proposal.
