---
source: magicians
topic_id: 477
title: Add Last Call for EIPS, with RSS feed [PULL REQUEST]
author: fulldecent
date: "2018-05-29"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/add-last-call-for-eips-with-rss-feed-pull-request/477
views: 1071
likes: 1
posts_count: 2
---

# Add Last Call for EIPS, with RSS feed [PULL REQUEST]

This PR adds a two-week “Last Call” process for every EIP. You can subscribe to these EIPs via RSS so you can have a last say before something becomes final. There have been 400 new pull requests since ERC-721, I only want to review the serious ones that make it to Last Call.

ERC-721 (currently stuck in Draft status) will be the first ERC to go to Last Call. See #1101.

Because some of the current EIP-1 wording is inaccurate, confusing or contradictory, it was necessary for me to fully rewrite the workflow section and document each EIP status and transition of statuses. I hope this makes the text more approachable for all readers.

Pasting my proposed update below for convenience. / [Link to live updated version](https://github.com/fulldecent/EIPs/blob/patch-11/EIPS/eip-1.md#eip-work-flow) / [Link to current text to be replaced](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md#eip-work-flow)

---

**Following is the process that a successful EIP will move along:**

```auto
[ WIP ] -> [ DRAFT ] -> [ LAST CALL ] -> [ ACCEPTED ] -> [ FINAL ]
```

Each status change is requested by the EIP author by @-mentioning or emailing the EIP editors. The EIP editors will process these requests as per the conditions below.

- Work in progress (WIP) – Once the champion has asked the Ethereum community whether an idea has any chance of acceptance, they will write a draft EIP as a [pull request]. Consider including an implementation if this will aid people in studying the EIP.

 Draft – If approved, EIP editor will assign the EIP a number (generally the issue or PR number related to the EIP) and merge your pull request. The EIP editor will not unreasonably deny an EIP.
- Draft – Reasons for denying draft status include being too unfocused, too broad, duplication of effort, being technically unsound, not providing proper motivation or addressing backwards compatibility, or not in keeping with the Ethereum philosophy.

**Draft** – Once the first draft has been merged, you may submit follow-up pull requests with further changes to your draft until such point as you believe the EIP to be mature and ready to proceed to the next status. An EIP in draft status must have implementations to be considered for promotion to the next status.

- Last Call – If approved, the EIP editor will assign Last Call status and set a review end date, normally 14 days later.
- Last Call – A request for Last Call status will be denied if material changes are still expected to be made to the draft. We hope that EIPs only enter Last Call once, so as to avoid unnecessary noise on the RSS feed. Last Call will be denied if the implementation is not complete and accepted by the community.

**Last Call** – This EIP will listed prominently on the http://eips.ethereum.org/ website (subscribe via RSS at [last-call.xml](/last-call.xml)).

- – A Last Call which results in material changes or substantial unaddressed complaints will cause the EIP to revert to Draft or worse.
- Accepted (Core EIPs only) – After the review end date, the Ethereum Core Developers will vote on whether to accept this change. If yes, the status will upgrade to Accepted.
- Final (Not core EIPs) – A successful Last Call without material changes or unaddressed complaints will become Final.

**Accepted (Core EIPs only)** – This is being implemented by Ethereum Core Developers.

- Final – When a Standards Track Core EIP is implemented in at least three viable Ethereum clients, and it is deployed on at least 50% of deployed nodes, and the implementations pass a common set of test suites, then the status is upgraded to Final.

**Final** – This EIP represents the current state-of-the-art. A Final EIP should only be updated to correct errata.

Other exceptional statuses include:

- Deferred – This is for core EIPs that have been put off for a future hard fork.
- Rejected – An EIP that is fundamentally broken and will not be implemented.
- Active – This is similar to Final, but denotes an EIP which which may be updated without changing its EIP number.
- Superseded – An EIP which was previously final but is no longer considered state-of-the-art. Another EIP will be in Final status and reference the Superseded EIP.

## Replies

**fulldecent** (2018-06-03):

If you are agreeable to these changes, don’t just pass by. Please make a quick endorsement with your formal “Approve” review on the GitHub pull request at https://github.com/ethereum/EIPs/pull/1100

We need strong support to make a change to EIP-1. You are the support!

