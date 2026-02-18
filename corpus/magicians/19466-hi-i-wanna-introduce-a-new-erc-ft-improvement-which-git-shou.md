---
source: magicians
topic_id: 19466
title: Hi, I wanna introduce a new ERC FT improvement, which GIT should I pr my request to? EIPs or ERCs?
author: catiga
date: "2024-04-01"
category: Uncategorized
tags: [erc]
url: https://ethereum-magicians.org/t/hi-i-wanna-introduce-a-new-erc-ft-improvement-which-git-should-i-pr-my-request-to-eips-or-ercs/19466
views: 787
likes: 3
posts_count: 6
---

# Hi, I wanna introduce a new ERC FT improvement, which GIT should I pr my request to? EIPs or ERCs?

Hello, Ethereum community!

I hope this message finds you well. I am reaching out to seek guidance and clarification on the correct process for submitting a new proposal for an ERC (Ethereum Request for Comments) standard improvement, specifically for fungible tokens.

Over the past few months, I have been working on developing a new ERC standard that aims to introduce significant improvements to the existing fungible token framework. This proposal includes several innovative features designed to enhance token stability, value transparency, and liquidity mechanisms, among other benefits. I believe this improvement has the potential to contribute positively to the Ethereum ecosystem and the broader DeFi community.

However, as I’m preparing to officially submit my proposal, I’ve encountered a bit of confusion regarding the appropriate GitHub repository for PR (Pull Request) submission. Given the recent discussions and potential changes in the Ethereum improvement proposal process, I’m unsure whether I should submit my PR to the traditional Ethereum EIPs (Ethereum Improvement Proposals) repository or if there’s a separate repository specifically for ERC proposals.

Could anyone please provide me with the latest guidelines or direct me to the correct repository for submitting an ERC improvement proposal? Your assistance would be greatly appreciated, as I want to ensure that my proposal is reviewed and considered by the community in accordance with the current best practices.

Additionally, if there are any tips or recommendations you could share about the proposal submission process, they would be incredibly valuable to me and perhaps to others in the community who might be in a similar situation.

Thank you very much for your time and assistance. I am looking forward to contributing to the Ethereum ecosystem and engaging with the community on this exciting improvement.

Best regards,

JC

## Replies

**abcoathup** (2024-04-02):

Tokens are app layer, so any PR should be done in the ERC repo: [GitHub - ethereum/ERCs: The Ethereum Request for Comment repository](https://github.com/ethereum/ERCs)

---

**catiga** (2024-04-02):

Got it, I’ll make my PR in ERC repo

If it is convenient, please take a look at the post of my ERC proposal.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/catiga/48/12163_2.png)

      [ERC-2510: Enhanced Liquidity and Value Backing Token Standard](https://ethereum-magicians.org/t/erc-2510-enhanced-liquidity-and-value-backing-token-standard/19478) [ERCs](/c/ercs/57)




> ERC-2510: Enhanced Liquidity and Value Backing Token Standard
> Abstract
> ERC-2510 is an innovative extension to the ERC-20 standard, establishing an intrinsic value and liquidity model within token contracts. By integrating a base liquidity pool, ERC-2510 aims to mitigate the risk associated with reliance on external liquidity providers. This ensures token stability and retains value even in the absence of third-party market makers.
> Motivation
> In light of recent market events highlighting the vul…

---

**abcoathup** (2024-04-03):

Please note, ERC numbers are issued by ERC editors and associates, you don’t get to pick your own number.

Once you have created a PR with a complete specification (currently it doesn’t look like you have completed the specification) an ERC number can be issued.

---

**catiga** (2024-04-03):

Yes, I know this, thx

---

**catiga** (2024-04-14):

Can I invite you to review and discuss my topic here, [ERC2510: Embedding Perpetual Value and Liquidity in Tokens](https://ethereum-magicians.org/t/erc2510-embedding-perpetual-value-and-liquidity-in-tokens/19577)

Looking forward to your suggestions.

