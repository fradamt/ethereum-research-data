---
source: magicians
topic_id: 2774
title: Mobile best practices
author: o_rourke
date: "2019-02-28"
category: Working Groups > Mobile Ring
tags: []
url: https://ethereum-magicians.org/t/mobile-best-practices/2774
views: 916
likes: 8
posts_count: 4
---

# Mobile best practices

Hey all, hope you enjoyed ETH Denver! In our last call we talked about having a repository for best practices for mobile developers. I want to get the conversation started with what my team have come across with building a few SDK’s and user facing mobile applications.

**Managing Data**

Managing data for a dApp is not your usual backend. Efficiently storing and syncing data is important.

- Maintaining an index locally can help retrieving new data only when the user requests it.
- Updating in the background existing data looking for new changes is always a must
- Every request counts, don’t waste API calls for data you can retrieve once and store locally
- Don’t forget to get the transaction count before sending a new transaction, nonces can change really fast
- Because of the asynchronous nature of blockchains, your error handling needs to be flexible enough to cover not only hard error cases, but lack of data for subsequent requests.

**Account management**

Mobile security is a different paradigm offering new solutions for common account security problems.

- Never store private keys in plain text, encrypt them with verified and tested encryption mechanisms
- Always empty out references in memory after signing transactions to avoid memory dumps
- You don’t need wallet keys when reading data from the blockchain, only when sending out transactions
- Even if the private keys are encrypted, use a secure storage mechanism client side to store the encrypted data
- Submit all requests over secure protocols (HTTPS, etc)
- Provide mechanisms to export/import keys securely, so clients can export their wallets to other applications, and back them up

Thoughts on spinning up a repo so we can add more as we think of them or go along our adventures building?

## Replies

**pi0neerpat** (2019-03-03):

Done! From the notes it looked like we wanted to start building this in ETH-Hub, so I created a PR to add a mobile docs page. Not sure what the flow is for making changes. Let me know if you need access to contribute.

https://github.com/ethhub-io/ethhub/pull/221

---

**pcowgill** (2019-03-05):

[@o_rourke](/u/o_rourke) [@pi0neerpat](/u/pi0neerpat) Thanks! I’ll put in some work on mapping out specific tech options available at different layers of the stack as well. If we want to chat back and forth without adding a lot of noise to ETHHub, I like the idea of spinning up a repo.

This is what [@owocki](/u/owocki) did for the Business Models Ring:

https://github.com/FEMBusinessModelsRing/web3_revenue_primitives

I set up something similar for us just now and invited mokn and pi0neerpat and marcelomorgado to the organization. Let me know if anyone else would like to be added as a collaborator too.

Here’s the repo: [GitHub - mobilering/ethhub: Documenting mobile stack and best practices for PRs against EthHub](https://github.com/mobilering/ethhub)

---

**pi0neerpat** (2019-04-08):

Hey just wanted to drop this here. If anyone has free time, I’d be interested to know how well this works! Maybe something we want to include in the mobile “stack”

https://github.com/abcoathup/expo-web3

