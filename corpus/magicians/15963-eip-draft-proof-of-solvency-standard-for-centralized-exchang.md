---
source: magicians
topic_id: 15963
title: "EIP-DRAFT: Proof of Solvency Standard for Centralized Exchanges"
author: adrianmcli
date: "2023-10-01"
category: Magicians > Primordial Soup
tags: [erc]
url: https://ethereum-magicians.org/t/eip-draft-proof-of-solvency-standard-for-centralized-exchanges/15963
views: 1856
likes: 11
posts_count: 10
---

# EIP-DRAFT: Proof of Solvency Standard for Centralized Exchanges

The [PSE](https://pse.dev/) team, funded by the EF, is working on creating a standard for Proof of Solvency for centralized exchanges (CEXs). We are initiating this discussion to gather valuable community feedback.

**Abstract**

Building upon foundational work, notably Vitalik’s [blog post](https://vitalik.ca/general/2022/11/19/proof_of_solvency.html), we propose a standard interface for proofs of solvency. We have developed the following:

- An EIP draft,
- A two-part explanatory blog post: Part 1 and Part 2, and
- A GitHub organization with additional details, including a reference implementation.

**Motivation**

Given the historical instances of exchanges facing insolvency, the need for a standardized, transparent way to validate solvency is evident. We believe this standard serves as a foundational step toward addressing this gap.

**Specification and Implementation**

To keep this post short, we recommend reviewing the above links for full details. The EIP draft contains the technical specifications, and the GitHub organization houses the proof of concept.

**Request for Feedback**

We are particularly interested in technical feedback regarding the standard’s feasibility and security. Comments on real-world use-cases and potential for integration with existing systems are also valuable. Input from industry stakeholders, such as CEXs or regulatory bodies, is encouraged.

## Replies

**lightning-li** (2023-10-11):

Thank you for your valuable contribution. I wanted to mention that Binance introduced its proof of solvency system a few months back. In the protocol’s design, every user is associated with multiple asset pairs, each of which includes both debt and equity fields, thereby facilitating the loan business. You can find a comprehensive description of these intricacies at the following link: [Notion – The all-in-one workspace for your notes, tasks, wikis, and databases.](https://gusty-radon-13b.notion.site/Proof-of-solvency-61414c3f7c1e46c5baec32b9491b2b3d). I would appreciate it if you could explore the possibility of incorporating these use cases into the standard.

---

**Mikhail** (2023-10-11):

curl https://mainnet.gateway.tenderly.co/7YUXvcqdCc4OibqFKHYJXm

-X POST

-H “Content-Type: application/json”

-d ‘{“jsonrpc”:“2.0”,“id”:0,“method”:“tenderly_simulateTransaction”,“params”:[{“from”:“0xd8da6bf26964af9d7eed9e03e53415d37aa96045”,“to”:“0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2”,“gas”:“0x0”,“gasPrice”:“0x0”,“value”:“0x0”,“data”:“0xa9059cbb00000000000000000000000020a5814b73ef3537c6e099a0d45c798f4bd6e1d60000000000000000000000000000000000000000000000000000000000000001”},“latest”]}’

---

**Mani-T** (2023-10-11):

It allows for the verification of exchange solvency without revealing sensitive information about individual user balances, which is a significant improvement over traditional systems.

---

**alxkzmn** (2023-10-11):

Thanks for bringing it up! I believe that we can easily incorporate the debt positions in our proposal as we are using the Merkle sum tree. We can calculate the total asset balance in the leaf based on equity and debt. The question is whether we need to constraint this calculation inside the ZK circuit or just use the total value and let the user verify that the total was calculated correctly. Do you think that the former approach has advantages?

---

**lightning-li** (2023-10-11):

Let’s consider a scenario where Alice owns 2 BTC and uses 1 BTC as collateral to borrow 1000 USDC. If we only store the total asset information in the leaf node, it becomes challenging to keep track of Alice’s specific asset details. Furthermore, there is a risk of losing track of the debt information. In such a case, it might be unclear for the user whether they have borrowed USDC or another asset like USDT.

To enhance user-friendliness and maintain transparency, it’s advisable to include both Alice’s equity and debt information in the public input of the circuit. These details can be fetched from a centralized exchange (cex) and ensure that the user has a clear understanding of their assets and liabilities.

---

**alxkzmn** (2023-10-20):

These are valid points, we will consider incorporating them. Thank you for the feedback!

---

**adrianmcli** (2023-10-20):

Thanks [@lightning-li](/u/lightning-li) for bringing up a very good point and providing the concrete example. I think that is something we must consider going forward.

In the mean time, I think we have given this draft enough time that I will be submitting it as a PR to get an EIP number. Given that it will still be in draft status, we can definitely consider incorporating more ideas going forward. We just hope this draft is good enough as a first stepping-stone towards a standard most exchanges can agree to trying out.

---

**enricobottazzi** (2023-10-26):

Hi [@lightning-li](/u/lightning-li)!

Thanks for the link provided! We really appreciate the open-source implementation and detailed documentation.

As I was looking into the different links attached to Binance implementation such as [codebase](https://github.com/binance/zkmerkle-proof-of-solvency), notion doc that you linked and [technical blogpost](https://www.binance.com/en/blog/tech/how-zksnarks-improve-binances-proof-of-reserves-system-6654580406550811626#idrichtexttextconfigcontentperformancestyle) we found some differences in the benchmark provided.

Can you please provide further clarification on the following?

- Witness + Proof Generation time for individual merkle tree zk proof
- User Proof of Inclusion generation time.
- Overall estimated cost in terms of time and $ to run a round of proof of solvency

---

**makemake** (2023-11-17):

While it’s possible to prove that they do have assets matching user deposits, we can’t really get info about a centralized financial institutions liabilities.

Exchanges can also just *lie*, which is pretty likely to happen if they are doing shady stuff with customer funds.

