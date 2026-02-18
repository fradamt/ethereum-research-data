---
source: ethresearch
topic_id: 18860
title: "IMO: Initial Model Offering"
author: fewwwww
date: "2024-03-04"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/imo-initial-model-offering/18860
views: 2692
likes: 4
posts_count: 2
---

# IMO: Initial Model Offering

## TL;DR

- ORA introduced IMO, Initial Model Offering.
- IMO = Model Ownership (ERC-7641 Intrinsic RevShare Token) + Inference Asset (eg. ERC-7007 Verifiable AI-Generated Content Token).
- IMO will benefit open-source AI models by enabling an efficient way of funding and fostering contributions to open-source AI models.
- ORA enables IMO with OAO (Onchain AI Oracle) for onchain AI model, and proposes ERC-7641 Intrinsic RevShare Token for adding revenue sharing mechanism to make IMO token valuable.

## 0. IMO: Initial Model Offering

**In this age of AI, we are introducing a new mechanism, IMO (Initial Model Offering):**

- IMO launches an ERC-20 token (more specifically, ERC-7641 Intrinsic RevShare Token) of any AI model to capture its long-term value.
- Anyone who purchases the token becomes one of the owners of this AI model.
- Token holders share revenue of the IMO AI model.

Many open-sourced AI models face the challenge in monetizing their contributions, leading to a lack of motivation for contributors and organizations alike. As a result, the AI industry is currently led by closed-source, for-profit companies. The winning formula for open-source AI models is the need to gather more funding and build in public.

With IMO, we can win the fight for open-source AI. IMO can enable the sustainability of the open-source AI model’s ecosystem by fostering long-term benefits and encouraging engagement and funding to the open-source AI community. The win is when we have better open-source models than proprietary models.

IMO tokenizes the ownership of open-source AI models, sharing its profit to the token holders.

## 1. IMO Mechanism

**Anyone can own model and receive its revenue by simply holding ERC-7641 token**.

In the current design, tokens from IMO will be issued on the Ethereum as ERC-20 and ERC-7641 token. Token holders will receive a share of profits from its model revenue and its generated NFT fee (eg. the royalty fee of AIGC-NFT generated from the Stable Diffusion model).

The overall architecture of the IMO mechanism is illustrated like this:

[![Untitled (4)](https://ethresear.ch/uploads/default/optimized/2X/8/8d4e7c461a9bb008c60a07ee99eb9f8c51457fbe_2_690x388.jpeg)Untitled (4)1920×1080 506 KB](https://ethresear.ch/uploads/default/8d4e7c461a9bb008c60a07ee99eb9f8c51457fbe)

In IMO, there are two core components:

- Onchain AI Model with Verifiability
- Revenue Sharing of Onchain Usage

### a) Onchain AI Model

We need a way to run IMO AI models fully on chain and verifiably. This is critical because we need to make sure that tokens are indeed tied to the right model and the right AI inference.

There are two mainstream approaches to implementing onchain AI models: zkML (by generating cryptographic proofs of the model) and opML (by using cryptoeconomics to ensure that the model is correct). We also invented [opp/ai](https://arxiv.org/abs/2402.15006), a combination of two approaches with both of their advantages. Based on practicality and performance, we adopt opML to port AI models onchain for now.

**opML is at the core of OAO (Onchain AI Oracle), which is essential to bring AI models to IMO**.

### b) Revenue Sharing through ERC-7641 Intrinsic RevShare Token

Holders of IMO tokens will receive the benefits of revenue streams including but not limited to:

- Revenue of model usage (Model Ownership, ERC-7641 Intrinsic RevShare Token): Each use of the AI model onchain will incur a fee, which will be distributed to IMO tokens.
- Revenue of AI-generated content (Inference Asset, eg. ERC-7007 Zero-Knowledge AI-Generated Content Token): Each use of the AI model generates a specific output and result (e.g. Stable Diffusion for an image NFT and Sora for a video NFT), which may carry a royalty fee and a mint fee that can be distributed to IMO tokens.

[![Untitled (5)](https://ethresear.ch/uploads/default/optimized/2X/3/3a28612bc563c671682610dcf777a1efc9201ebf_2_690x388.jpeg)Untitled (5)1920×1080 67.3 KB](https://ethresear.ch/uploads/default/3a28612bc563c671682610dcf777a1efc9201ebf)

The AI model distributes the fees directly to the IMO tokens. We have introduced an extension to ERC-20: ERC-7641, which standardizes revenue-sharing logic.

[![Untitled (6)](https://ethresear.ch/uploads/default/optimized/2X/8/8e54a5b6ab8d51e43990ac6b93ca0a9b783335bc_2_690x388.jpeg)Untitled (6)1920×1080 120 KB](https://ethresear.ch/uploads/default/8e54a5b6ab8d51e43990ac6b93ca0a9b783335bc)

Holding IMO tokens is owning a part of an AI model and its future revenue. Imagine now you own a part of LlaMA2, Stable Diffusion, or Mistral. This not only benefits token holders but also contributes to the sustainable funding of open-source AI models.

## 2. Future of AI x Crypto is IMO

IMO is the future of AI x Crypto. Own AI model onchain and earn its revenue with IMO. Stay tuned and more updates soon!

Watch our talk “**[AI Isn’t Evil and Smart Contract Proves It](https://twitter.com/EthereumDenver/status/1763342326359805981)**” at ETHDenver on IMO.

Dive deep into our works on Onchain AI:

- OAO, Onchain AI Oracle
- opML, Optimistic Machine Learning
- opp/ai, Optimistic Privacy-Preserving AI

## Replies

**kartin** (2024-04-04):

The biggest AI narrative on Ethereum is coming.

