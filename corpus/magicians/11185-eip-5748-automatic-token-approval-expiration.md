---
source: magicians
topic_id: 11185
title: EIP-5748 Automatic Token Approval Expiration
author: turanzv
date: "2022-10-05"
category: EIPs
tags: [token, token-approval]
url: https://ethereum-magicians.org/t/eip-5748-automatic-token-approval-expiration/11185
views: 1092
likes: 2
posts_count: 4
---

# EIP-5748 Automatic Token Approval Expiration

Outstanding token approvals increase a token holder’s exposure to vulnerabilities and zero days in contract code. We (Go+ Security, Jeff Hall, Xavi [@XaaaaavitheFool](/u/xaaaaavithefool) , and myself) and our friends in the Web3 security space have been discussing making expiration times standard on token contracts, so that tokens can expire automatically.

This would reduce the exposure to outstanding token approvals and restrict exposure to vulnerabilities across transaction.

The PR with relevant implementation: [Add EIP-5748: Approval Expiration for EIP-20 Tokens by Mr-Lucky · Pull Request #5748 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5748)

## Replies

**XaaaaavitheFool** (2022-10-08):

Guys, we are happy to answer any questions about the proposal！ ![:smiley_cat:](https://ethereum-magicians.org/images/emoji/twitter/smiley_cat.png?v=12)

---

**chrisfarms** (2022-10-08):

I think allowing wallets to surface information about what is being approved is important.

So I think maybe it would be better if either:

- it intentionally breaks/reverts on use of the legacy version
- or there should be a standard way to fetch the default value used for the legacy call so it can be presented to the user

---

**turanzv** (2022-10-11):

Agreed, would be great to see wallets expose users to this security principle.

Getters and setters for the default value is definitely missing in the current iteration. We’ll push the update ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

In the name of having an accessible bar for minimum compliance, I like the idea of a getter to pre-empt use of the legacy call rather than a hard break. Ideally wallets would be able to be a custodian of a user-defined default as well. I’m not sure how hard breaks would affect adoption of the EIP

