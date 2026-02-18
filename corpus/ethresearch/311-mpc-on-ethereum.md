---
source: ethresearch
topic_id: 311
title: MPC on Ethereum
author: dcerezo
date: "2017-12-11"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/mpc-on-ethereum/311
views: 11956
likes: 7
posts_count: 12
---

# MPC on Ethereum

Most solutions to provide privacy to smart contracts are based on SGX, which was a sensible choice years ago but recent attacks have proven it to be inadequate (see list of papers below breaking SGX). Moreover, the security model offered by SGX is much more useful for permissioned than permissionless blockchains.

Right now, the most adequate solution is to use state-of-the-art MPC protocols: 1000x faster than homomorphic encryption and backed by more than 30 years of research.

Note that there aren’t many practical examples of blockchains running MPC: a system implementing MPC for Ethereum is described in the following paper: https://eprint.iacr.org/2017/878.

What practical uses cases in Ethereum would you use MPC for?

–

List of papers describing attacks on SGX:

- Ferdinand Brasser, Urs Muller, Alexandra Dmitrienko, Kari Kostiainen, Srdjan Capkun, and Ahmad-Reza Sadeghi. Software Grand Exposure: SGX Cache Attacks Are Practical, 2017.
- Michael Schwarz, Samuel Weiser, Daniel Gruss, Clementine Maurice, and Stefan Mangard. Malware Guard Extension: Using SGX to Conceal Cache Attacks, 2017.
- Ahmad Moghimi, Gorka Irazoqui, and Thomas Eisenbarth. CacheZoom: How SGX Amplifies The Power of Cache Attacks, 2017.
- Nico Weichbrodt, Anil Kurmus, Peter Pietzuch, and Rüdiger Kapitza. Async-Shock: Exploiting Synchronisation Bugs in Intel SGX Enclaves, 2016.
- Yuanzhong Xu, Weidong Cui, and Marcus Peinado. Controlled-Channel Attacks: Deterministic Side Channels for Untrusted Operating Systems. In Proceedings of the 2015 IEEE Symposium on Security and Privacy, SP ’15, pages 640–656, Washington, DC, USA, 2015. IEEE Computer Society.
- Ming-Wei Shih, Sangho Lee, Taesoo Kim, and Marcus Peinado. T-SGX: Eradicating Controlled-Channel Attacks Against Enclave Programs, 2017.
- Sangho Lee, Ming-Wei Shih, Prasun Gera, Taesoo Kim, Hyesoon Kim, and Marcus Peinado. Inferring Fine-grained Control Flow Inside SGX Enclaves with Branch Shadowing, 2016.
- Marcus Brandenburger, Christian Cachin, Matthias Lorenz, and Rüdiger Kapitza. Rollback and Forking Detection for Trusted Execution Environments using Lightweight Collective Memory, 2017.
- Yogesh Swami. SGX Remote Attestation is not Sufficient… Cryptology ePrint Archive, Report 2017/736, 2017.
- Jaehyuk Lee, Jinsoo Jang, Yeongjin Jang, Nohyun Kwak, Yeseul Choi, Changho Choi, Taesoo Kim, Marcus Peinado, and Brent ByungHoon Kang. Hacking in Darkness: Return-oriented Programming against Secure Enclaves. In 26th USENIX Security Symposium (USENIX Security 17), pages 523–539, Vancouver, BC, 2017. USENIX Association.
- Jo Van Bulck, Nico Weichbrodt, Rüdiger Kapitza, Frank Piessens, and Raoul Strackx. Telling Your Secrets without Page Faults: Stealthy Page Table-Based Attacks on Enclaved Execution. In 26th USENIX Security Symposium (USENIX Security 17), pages 1041–1056, Vancouver, BC, 2017. USENIX Association.
- Yuan Xiao, Mengyuan Li, Sanchuan Chen, and Yinqian Zhang. Stacco: Differentially Analyzing Side-Channel Traces for Detecting SSL/TLS Vulnerabilities in Secure Enclaves. CoRR, abs/1707.03473, 2017.
- Yuan Xiao, Mengyuan Li, Sanchuan Chen, and Yinqian Zhang. Leaky Cauldron on the Dark Land: Understanding Memory Side-Channel Hazards in SGX. CoRR,abs/1705.07289, 2017.
- Frank Piessens Jo Van Bulck and Raoul Strackx. SGX-Step: A Practical Attack Framework for Precise Enclave Execution Control. In In Proceedings of the 2nd Workshop on System Software for Trusted Execution (SysTEX ’17), 2017.

## Replies

**vbuterin** (2017-12-12):

I recommend reaching out to the Enigma folks; I know they are working on something.

---

**Silur** (2017-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dcerezo/48/253_2.png) dcerezo:

> 1000x faster than homomorphic encryption

I’ve recently finished my research on FHE on ethereum (EIP760) and I really doubt this number. Recent advances in homomorphic encryption made bootstrapping possible < 140ms on an i7, and a decent FHE circuit evaluation in 180ms.

---

**dcerezo** (2017-12-19):

Please note that I’m not against homomorphic encryption: I would like it to be faster but some very deep breakthroughs are needed before it catches up with MPC.

As a rule of thumb, MPC with pre-processing is 3 orders of magnitude faster than homomorphic encryption for general purpose circuits given current encryption schemes. Some note about this claim:

- this is a rough estimate that compares the fastest schemes of MPC with the fastest schemes for homomorphic encryption. In reality, the security levels and assumptions behind both paradigms are very different.
- I’m aware of the publication[3] that you are using: each binary gate runs in 13 ms in FHE mode (i.e., 77 gates per second); the 23-to-8 leveled LUT runs in 1 second and leveled multiplication of 2 inputs of 32 bits runs in 1 second (i.e., 1024 gates per second). Compare that to the 500 million AND gates per second of some recent MPC protocols [4].
- if you design special schemes for specific algorithms using homomorphic encryption (i.e., you drop the general purpose requirement), the difference between MPC and homomorphic encryption can be lowered to 2 orders of magnitude [1, 2]
- but using pre-processing for MPC results in an order of magnitude speed-up, not available in current homomorphic encryption schemes

Actually, the biggest handicap of homomorphic encryption in a public permissionless blockchain like Ethereum is not performance, it’s ciphertext expansion: it will be extremely expensive to store encrypted information on-chain because homomorphic encryption expands the size of the ciphertext by a factor of thousands (the concrete factor depending on the homomorphic encryption scheme used).

---

[1] Eleftheria Makri and Dragos Rotaru and Nigel P. Smart and Frederik Vercauteren. “PICS: Private Image Classification with SVM” https://eprint.iacr.org/2017/1190

[2] M. Sadegh Riazi and Christian Weinert and Oleksandr Tkachenko and Ebrahim M. Songhori and Thomas Schneider and Farinaz Koushanfar. “Chameleon: A Hybrid Secure Computation Framework for Machine Learning Applications” https://eprint.iacr.org/2017/1164

[3] Ilaria Chillotti, Nicolas Gama , Mariya Georgieva, and Malika Izabachène “Improving TFHE: faster packed homomorphic operations and efficient circuit bootstrapping” https://eprint.iacr.org/2017/430

[4] Jun Furukawa and Yehuda Lindell and Ariel Nof and Or Weinstein. “High-Throughput Secure Three-Party Computation for Malicious Adversaries and an Honest Majority” https://eprint.iacr.org/2016/944

---

**weikengchen** (2018-01-23):

I think it depends on the applications.

MPC can also use homomorphic encryption. But we usually refer MPC to be based on garbled circuits, which is fast if the input is not too large.

If the input is too large, it would be better to combine homomorphic encryption and garbled-circuit-style MPC.

**One paper that is exactly the example:**

Valeria Nikolaenko, Udi Weinsberg, Stratis Ioannidis, Marc Joye, Dan Boneh, Nina Taft

Privacy-Preserving Ridge Regression on Hundreds of Millions of Records

https://docs.google.com/file/d/0B5qjSJpwjTbNYmRUVjNkZHVyaWs/edit?usp=sharing

Any idea on some applications?

---

**dcerezo** (2018-01-24):

Hey Weikeng,

By the textbook definition of garbled circuits, it’s true that it’s not an efficient technique for secure computation on large inputs. Nonetheless there are techniques that workaround this limitation:

- Combinations of garbled circuits with ORAMs[1]
- Clever uses of Oblivious Transfers[2]
- Garbling RAM Programs[3]

If you are interested on practical applications, I have just published a short paper about this:

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3103343

–

[1] Xiao Shaun Wang and Yan Huang and T-H. Hubert Chan and abhi shelat and Elaine Shi

“SCORAM: Oblivious RAM for Secure Computation” https://eprint.iacr.org/2014/671

[2] Chongwon Cho and Nico Döttling and Sanjam Garg and Divya Gupta and Peihan Miao and Antigoni Polychroniadou “Laconic Oblivious Transfer and its Applications” https://eprint.iacr.org/2017/491

[3] Steve Lu and Rafail Ostrovsky “How to Garble RAM Programs” https://eprint.iacr.org/2012/601

---

**weikengchen** (2018-01-24):

Hi David,

I would be more excited to point out this paper:

Global-Scale Secure Multi-Party Computation Xiao Wang, Samuel Ranellucci, and Jonathan Katz In ACM Conference on Computer and Communications Security (CCS), 2017.

Paper: http://eprint.iacr.org/2017/189.pdf

Slides: https://drive.google.com/open?id=0B8xyDDLfC4YKa0xlLXEtY3J3clk

Like the proof-of-stake, select a group of people who pay the deposit, and let them run the protocol?

And one of them can report the (encrypted) result with a proof that what they do is correct, and the blockchain rewards them?

---

**weikengchen** (2018-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/weikengchen/48/10211_2.png) weikengchen:

> otocol?
>
>
> And one of them can report the (encrypted) result with a proof that what they do is correct, and the blockchain rewards them?

Warning: these three might be slow. Especially, ORAM over GC is, as you can see, working on small input, like a 4-byte integer.

---

**dcerezo** (2018-01-25):

Yes, that idea of using the blockchain for rewards[2, 3, 4, 6, 7] and penalties[1, 5, 6, 7] is the basis of a number of papers: we just need to make them real-world useable.

__

[1] Iddo Bentov, Ranjit Kumaresan “How to Use Bitcoin to Design Fair Protocols” https://eprint.iacr.org/2014/129

[2] Iddo Bentov, Ranjit Kumaresan, Andrew Miller “Instantaneous Decentralized Poker” https://eprint.iacr.org/2017/875

[3] Bernardo David, Rafael Dowsley, Mario Larangeira “Kaleidoscope: An Efficient Poker Protocol with Payment Distribution and Penalty Enforcement” https://eprint.iacr.org/2017/899

[4] Marcin Andrychowicz, Stefan Dziembowski, Daniel Malinowski, Łukasz Mazurek “Secure Multiparty Computations on Bitcoin” https://eprint.iacr.org/2013/784

[5] Aggelos Kiayias, Hong-Sheng Zhou, Vassilis Zikas “Fair and Robust Multi-Party Computation using a Global Transaction Ledger” https://eprint.iacr.org/2015/574

[6] Ranjit Kumaresan, Vinod Vaikuntanathan, Prashant Nalini “Improvements to Secure Computation with Penalties” https://people.csail.mit.edu/vinodv/ccs2016.pdf

[7] Ranjit Kumaresan, Iddo Bentov “How to Use Bitcoin to Incentivize Correct Computations” http://www.cs.technion.ac.il/~ranjit/papers/incentives.pdf

---

**abhvious** (2018-02-03):

Your last comment suggests ways that the blockchain can help solve issues with MPC (e.g., fairness, penalties for cheating, etc.), but I would like to get back to your original question, “What practical uses cases in Ethereum would you use MPC for?”

One of my group’s recent papers (to appear in Oakland’2018) uses MPC to solve the problem of threshold signatures (aka multi-sig wallets).  Instead of using an on-chain contract to handle a fundamentally crypto operation, we suggest using a crypto protocol to compute the ECDSA signature, and just rely on the contract to handle the “business logistics” of holding the money.  (The benefits of our protocol over prior work for the same problem has to do with using no new assumptions like DCR and being 10x faster.)

Extending the idea, I would like to hear feedback on the idea of replacing “voting” and “threshold checking” code found in smart contracts with simpler contract logic and MPC.

---

**dcerezo** (2018-02-04):

Hi Abhi,

Regarding voting, blockchains and MPC:

- To improve voter turnout and solve the problem of voter fatigue/apathy, voters should earn tokens: it’s irrational to vote because the probability that an individual’s vote will change the outcome of an election is near zero; therefore people only vote when the perceived value of satisfying their “civic duty” is higher than the economic costs of voting. To improve voter turnout, they could get rewarded for voting (or at least cover their transaction fees): this is easier to implement with blockchains/smartphones than with cash in the real world.
- Most cryptographic e-voting methods only consider simple tallying functions (e.g., majority voting). Modern research in voting theory uses game theory to prove complex properties of election methods (e.g., the independence of clones criterion to measure the robustness to strategic nomination; the generalized Condorcet/Smith criterion; the independence of irrelevant alternatives) generating more complex ranking and tallying algorithms (e.g., Schulze method, Tideman method, Minimax Condorcet, …): it’s natural to implement them with MPC in order to guarantee the secrecy of the votes (and it’s in line with your paper “Secure Stable Matching at Scale”[1] implementing game theoretic algorithms in MPC). Coincidentally, the inavailability of complex tallying functions is one of the reasons cryptographic e-voting isn’t more extended.

__

[1] Jack Doerner, David Evans, abhi shelat. “Secure Stable Matching at Scale”. https://eprint.iacr.org/2016/861

---

**abhvious** (2018-02-04):

David,

That is an interesting direction you are suggesting; when i used “voting” and “threshold”, I was referring to contracts like DAO and multi-sig wallets (and searching for other examples) in which the contract logic is implementing a basic voting+threshold check.

From my understanding, a lot of the parity bugs are due to engineering efforts to reduce the cost/gas associated with doing these checks (e.g., one library, complex control flow thru default calls, etc).  One idea is that some of this can be outsourced to off-chain MPC, thereby leaving only the parts with “handle the real world” on the chain.

