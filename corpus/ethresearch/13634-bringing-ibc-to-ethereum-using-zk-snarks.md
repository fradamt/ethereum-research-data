---
source: ethresearch
topic_id: 13634
title: Bringing IBC to Ethereum using ZK-Snarks
author: garvitgoel
date: "2022-09-12"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/bringing-ibc-to-ethereum-using-zk-snarks/13634
views: 18058
likes: 59
posts_count: 21
---

# Bringing IBC to Ethereum using ZK-Snarks

*Authors: Garvit Goel, Jinank Jain (Electron Labs)*

This is an article on how to bring IBC to Ethereum. The goal of the article is to provide an overview of the technical details of this project and gather support from the Ethereum community. Let’s dive into it.

IBC stands for Inter Blockchain Communication - the cross-chain standard in the Cosmos ecosystem https://ibcprotocol.org/

### Problem background

IBC works on the light client principle where the light clients of the origin and destination blockchains need to be implemented as smart contracts in order to verify cross-chain transactions.

This means that in order to connect IBC to Eth, we will need to run the tendermint light client on Ethereum as a solidity smart contract. However, this turns out to be an extremely gas expensive operation since this requires verification of hundreds of ed25519 signatures in solidity, and ed25519 pre-compiles are not available on Ethereum. One ed25519 costs 500K gas. This means that verifying full light client headers would cost at least 50 mn gas (100 validators) and go up to 500 mn for larger cosmos chains with 1000 validators.

Hence we must find an alternative to verify these signatures cheaply on Ethereum.

### Solution

We have achieved this by taking inspiration from zk-rollups. Rather than verifying the ed25519 signatures directly on Ethereum, (and performing the curve operations inside a solidity smart contract), we construct a zk-proof of signature validity and verify the proof on-chain instead.

At Electron Labs, we have built a circom-based library that allows you to generate a zk-snark proof for a batch of Ed25519 signatures. Check out the complete implementation [here](https://github.com/Electron-Labs/ed25519-circom)

**How to try this out?**

We have deployed a server whose endpoints allow you to submit a batch of signatures and get the zk-proof in return. You can test this out right now using the API reference given in our docs - [docs.electronlabs.org/reference/generate-proof](http://docs.electronlabs.org/reference/generate-proof)

### Details of our Mathematical Approach

Creating a ZK-prover for ed25519 is a hard problem. This is because ed25519’s twisted Edwards curve uses a finite field that is larger than that used by the altbn128 curve (used by zk-snarks). Performing large finite field operations inside a smaller field is difficult because several basic operations such as modulo and multiplication can become very inefficient.

To solve this problem, we were able to find 2^85 as a base over which to define our curve operations for twisted Edwards curve. Since the ed25519 prime p = 2^255 - 19 is a close multiple of 2^85, we were able to come up with efficient basic operators such as multiplication and modulo (under 25519 prime) for base2^85 numbers.

Next, we used these custom operations to define curve operations such as point addition, scalar multiplication, and signature verification inside our ZK-circuit.

It is hard to do justice to the details of the mathematics behind this in this doc, please refer to our detailed docs explaining this given [here](https://docs.electronlabs.org/reference/overview).

### Performance of Single Signature Proof

As a result of the above optimizations, we were able to achieve the following performance figures for a single signature.

| Circuit Performance for Single ED25519 Signature |  |
| --- | --- |
| Constraints | 2,564,061 |
| Circuit compilation | 72s |
| Witness generation | 6s |
| Trusted setup phase 2 key generation | 841s |
| Trusted setup phase 2 contribution | 1040s |
| Proving key size | 1.6G |
| Proving time (rapidsnark) | 6s |
| Proof verification Cost | ~300K gas |

**All metrics were measured on a 16-core 3.0GHz, 32G RAM machine (AWS c5a.4xlarge instance).*

### Performance of Batch Prover

To understand the performance at a system level, we need to look at 3 parameters-

- Proof generation time per signature ~ 9.6s (averaged out)
- Number of Signatures per batch/proof = ≤ 100 (maximum value)
- Time to generate zk-proof for the batch = 16 mins for 100 signature batch

The proof generation time scales linearly (almost) with respect to the number of signatures per batch. We can increase/decrease the number of signatures per batch and the proof generation time changes accordingly.

[![image](https://ethresear.ch/uploads/default/original/2X/c/c611fe11f4f71939893ec5ce35db433c2882419d.png)image600×371 14.4 KB](https://ethresear.ch/uploads/default/c611fe11f4f71939893ec5ce35db433c2882419d)

Proof production time will be visible as latency. To reduce this, we can put a lesser number of signatures in one zk proof. However, this means more proofs will be required for the same batch size (or per light client header), which will increase the gas cost of verifying that batch.

Hence, reducing the latency will increase the gas cost. Below we have laid out the expected cost of verifying a tendermint Light Client (LC) header on Ethereum as a function of latency and the number of validators participating in that cosmos chain. We can give the users/cosmos chains the option of deciding the latency and gas fees they wanna to work with.

| Number of Validators | Latency (minutes) | Number of Signatures per Proof | Tx Cost per Light Header ($) | Cost Reduction (X) achieved by using ZK |
| --- | --- | --- | --- | --- |
| 200 | 16 | 100 | 9.0 | 166.7 |
| 500 | 16 | 100 | 22.4 | 166.7 |
| 1000 | 16 | 100 | 44.8 | 166.7 |
| 10000 | 16 | 100 | 448.5 | 166.7 |
|  |  |  |  |  |
| 200 | 8 | 50 | 17.9 | 83.3 |
| 500 | 8 | 50 | 44.8 | 83.3 |
| 1000 | 8 | 50 | 89.7 | 83.3 |
| 10000 | 8 | 50 | 896.9 | 83.3 |
|  |  |  |  |  |
| 200 | 2 | 12 | 76.2 | 19.6 |
| 500 | 2 | 12 | 188.4 | 19.8 |
| 1000 | 2 | 12 | 376.7 | 19.8 |
| 10000 | 2 | 12 | 3740.3 | 20.0 |
|  |  |  |  |  |

**based on gas prices on 5th August 2022.*

We have selected 200 validators and 50 signatures per proof as the base case for further analysis.

### Cost of Relayer Infrastructure

Since the tendermint block production rate is ~ 7 sec and the proof generation time is 8 minutes, we will need multiple prover machines in parallel to keep up with the block production rate.

Number of parallel machines required = 8 mins *60 / 7 sec = 69 machines

We recommend using m5.8xlarge AWS cloud instance for proof generation.

Hence the cost of this infra = $1.536*69 = $106 per hr

Machine Cost per light client header = 106/3600/7 = $0.206

### Estimating Total Transaction Cost

Consider the case for 8 mins latency and 200 validators.

Total Cost of on-chain light client verification = $17.9 + $0.206 = $18.1

Let us assume a worst-case scenario (from a tx fees point of view) when only one cross-chain transaction is present in one block. Then the entire cost of verifying the LC header is borne by that transaction. Adding some overhead cost, then verifying the cross-chain transaction is ~$ 20.

Assuming an optimistic case when there 10 transactions per block, this cost will be ~$2 which is similar to the cost of a Uniswap transaction on Ethereum.

### How can we reduce the gas cost and latency (using recursive)?

In order to reduce latency down to seconds and gas costs down to a few cents per transaction, we are working on recursive proof technology. This will enable us to generate multiple proofs together in parallel and then recursively combine them into a single proof.

We are evaluating various recursive libraries available in the market such as plonky2, and the works by Mina, Aztec and Starknet teams. We invite anyone working on recursive to connect with us.

By use of recursion and the use of hardware-based acceleration, we believe we can achieve sub-5 second latency for cross-chain transactions.

In the future, we can even combine multiple light headers in a single proof, costing just $4.5 per proof, and potentially <$1 per cross-chain transaction.

## System Level Design Overview

**Current IBC Design (Simplified)**

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9ba15634424aa84d4555f9b63f29bfb1b54552b7_2_690x276.png)image2608×1044 128 KB](https://ethresear.ch/uploads/default/9ba15634424aa84d4555f9b63f29bfb1b54552b7)

**Proposed IBC Design**

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/0f6c56c2db0024643ee38e1f8c1ed0e104a88e3e_2_690x422.png)image2684×1644 223 KB](https://ethresear.ch/uploads/default/0f6c56c2db0024643ee38e1f8c1ed0e104a88e3e)

**Points to note regarding proposed design**

1. The IBC interface stays the same. This makes adoption very easy since no new developer docs and developer re-education is required. The existing code bases will also get used as it is.
2. No Governance updates are necessary on app-chains
3. Two changes are required to IBC on Ethereum side-

The relayer, rather than submitting the full light client header, will now just submit the proof of validity for the same.
4. The on-chain light client modules on Ethereum side will include a zk-proof verifier instead of ed25619 signatures verifier.

### What Next?

We invite the Ethereum and ZK community at large to provide their comments and help us gather support to make this proposal a reality.

**Execution Plan:**

Phase1: Integration of our ZK engine with IBC

Phase2: Bringing down latency to ~5s through recursive proofs and hardware acceleration.

Phase3: Deploy a demo-app chain that uses connects to Ethereum via zk-IBC.

Phase4: Run the demo app-chain setup for extensive testing, and enable the community to test out transactions

Phase5: Security Audits

Phase6: Mainnet Deployment

## Replies

**cwgoes** (2022-09-12):

Very nice! The general approach & revision of the IBC dataflow model all makes sense to me. A few questions on your investigations & alternatives:

- Would switching Tendermint’s signature scheme (secp256k1 or eventually BLS) cut the proving time a lot, or not so much?
- Is the cost of verifying Merkle proofs (required for packets, should be possible to use Ethereum’s sha2 precompile) significant? Do you have any benchmarks of gas required per packet (which would add to the amortised header cost)?
- What about verifying the Ethereum consensus on the other side? Does ETH2 have a cheap light client which you can just use out of the box or would additional work be required (to retain the IBC security model)?

---

**alexeiZamyatin** (2022-09-13):

Sounds pretty cool

Would a Flyclient like construction be compatible here to reduce the number of headers needed?

You could then further reduce the number of proofs needed by using contingent transaction aggregation ([TxChain: Efficient Cryptocurrency Light Clients via Contingent Transaction Aggregation](https://eprint.iacr.org/2020/580))

This would just be on top but can significanly reduce the number of headers and tx inclusion proofs you need. Leaving here as possible consensus-level scaling improvements

---

**weikengchen** (2022-09-13):

Just to refer to one of our recent works: https://eprint.iacr.org/2022/1145.pdf

If eventually EIP-1962 will be back, then there are ways to cut the constraints significantly as well as to avoid the use of Groth16 setup/large proving key.

Note: this paper does not include the cost of SHA512.

---

**MicahZoltu** (2022-09-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/garvitgoel/48/9085_2.png) garvitgoel:

> IBC

I feel like this post would be significantly better if you said what IBC stood for at the beginning. It is a new term for me, and the entire post is hard to follow without knowing what it is referring to.  Just a single external link, or even just the deacronymed full name would probably be sufficient.

---

**Wizdave97** (2022-09-13):

IBC stands for Inter Blockchain Communication Protocol, here’s a link to the spec https://github.com/cosmos/ibc

---

**garvitgoel** (2022-09-13):

thank you ser for the feedback. Have added it now to the beginning of the article ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**garvitgoel** (2022-09-13):

Hi [@cwgoes](/u/cwgoes) thanks for your comments. Here are my answers -

1. Yes, secp256k1 or BLS will produce significant benefits. However, this would require convincing the entire cosmos community to move away from ed25519 and switch to these schemes.
2. We can actually prove the merkle proof within the circuit itself. I will add the benchmarks of gas required per packet here soon.
3. I think eth2 comes with BLS signatures, which are aggregable? We know that folks over at NEAR have a working on-chain eth2 light client.

Hope this helps!

---

**hu55a1n1** (2022-09-13):

Cool stuff! How do you plan to address Ethereum’s delayed finality?

---

**BennyOptions** (2022-09-14):

Hey [@garvitgoel](/u/garvitgoel) this is certainly an interesting approach. I happened to see this being circulated on twitter and wanted to confirm my understanding.

![](https://ethresear.ch/user_avatar/ethresear.ch/garvitgoel/48/9085_2.png) garvitgoel:

> Hence we must find an alternative to verify these signatures cheaply on Ethereum.

Correct me if I’m wrong, but from my understanding of IBC, the key differentiating factor is what you’re proposing to alter here. IBC operates with no trust assumptions outside of the consensus of the two chains interacting with one another (light clients on source/dest chains), while this proposed solution does off-chain verification then submits a zk-proof. It does not appear to verify validator signatures / blockheaders on chain, which impacts some of the core security assumptions of IBC I believe.

[![Screen Shot 2022-09-13 at 8.47.46 PM](https://ethresear.ch/uploads/default/optimized/2X/4/42ab5773c5d3c7bf6370b538416620de706d6930_2_690x230.png)Screen Shot 2022-09-13 at 8.47.46 PM918×306 11.3 KB](https://ethresear.ch/uploads/default/42ab5773c5d3c7bf6370b538416620de706d6930)

Imo the ideal solution would be some changes to the Cosmos SDK to allow for cheaper verification of both blocks and validator signatures on target-networks rather than making any changes to the security assumptions/verification mechanisms. Of course, this is a difficult solution that would take more R&D.

To be clear, I think this is a great idea and use case of zk-proofs. I just think that it’s quite a different solution from IBC. Using zk-proofs for cross-chain communication could be a stand-alone new project imo. Let me know what you think, I could be way off-base here, I just find the topic interesting.

---

**garvitgoel** (2022-09-14):

Hi [@BennyOptions](/u/bennyoptions) thank you for the comments. So that’s the thing about ZK-Proofs, they don’t introduce any new trust assumptions. The signatures are still getting validated in a trustless manner since the zk-proof gets verified on-chain.

---

**BennyOptions** (2022-09-14):

I see, thanks for the reply. So long as no additional assumptions are introduced, it seems like a viable solution if the cost and latency aspects can be solved. What’s the best place to follow along on your progress?

---

**garvitgoel** (2022-09-14):

Hi Benny, will be starting a telegram group soon. Will post the link here itself ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**edsonayllon** (2022-09-25):

What’s the motivation for this? The problem background addresses technical limitations, without addressing why one would want to do this.

---

**adi_rr** (2022-09-26):

[@edsonayllon](/u/edsonayllon) IBC is perhaps the most trust-minimized, general-purpose interoperability protocol available today.

Over the past 18 months, nearly 50 public blockchains (and a handful of enterprise chains) have implemented IBC. It has accounted for greater than 50m cross-chain transfers and a USD vol of nearly 60bil. We believe that IBC offers a solution to act as the connective tissue between all blockchains.

A direct IBC connection between two chains requires that both chains have instant finality. Given Ethereum’s double-slot finality and the high costs of on-chain sig verification, an IBC connection from Cosmos chains to Ethereum have been infeasible until now. The use of succinct proofs (as shown above) could offer a solution to this problem.

---

**bluto658** (2022-10-03):

Why focus on communication with the Cosmos and not on communication between Ethereum roll ups?

---

**garvitgoel** (2022-10-06):

L2<>L2 bridging does not need light clients for trustlessness. Furthermore, the Eth2 light client is based on BLS signatures which are aggregable, which means that the Eth2 light client does not really need Zk-based compression.

---

**gMoney** (2023-01-16):

[@garvitgoel](/u/garvitgoel) interesting post. Why does L2 <> L2 bridging not require light clients trustlessness?

---

**garvitgoel** (2023-04-08):

Actually, L2 <> L2 bridging can also be solved using this approach.

---

**bsanchez1998** (2023-04-12):

[@garvitgoel](/u/garvitgoel) This is fascinating and if implemented could have a significant impact on cross-chain communication. I’m particularly intrigued by your plans to further reduce latency and gas costs using recursive proofs and hardware acceleration since the performance figures are impressive. I would be interested to see how relayers will have to update to fix this, particularly new decentralized relays.

I’m looking forward to seeing the progress of this project.

---

**garvitgoel** (2023-04-12):

We have started a telegram group for this. Folks can join here - [Telegram: Join Group Chat](https://t.me/+s6pl2wqiLZ84ZDA5)

