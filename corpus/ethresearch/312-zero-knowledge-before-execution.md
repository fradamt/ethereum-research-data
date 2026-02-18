---
source: ethresearch
topic_id: 312
title: Zero-knowledge before execution
author: dcerezo
date: "2017-12-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zero-knowledge-before-execution/312
views: 2139
likes: 2
posts_count: 5
---

# Zero-knowledge before execution

In smart contracts, zero-knowledge is being used to prove properties/execution of the code after it has been executed.

It would be much more useful to provide proofs of properties of the code before executing the smart contract: before entering into any contractual arrangement, before irreversibly sending ether to any smart contract, it would be very helpful to first obtain and check proofs providing guarantees about the smart contract  (termination and correctness; pre-conditions, post-conditions and invariants; economic like fairness, double-entry consistency, equity; self-enforcement of regulations).

The following paper describes a technical solution to this problem: https://eprint.iacr.org/2017/878 (see section 5).

What properties about a smart contract would you like to check before executing it?

## Replies

**vbuterin** (2017-12-12):

So basically doing a SNARK over a formal verifier? Sounds totally reasonable to me.

---

**dcerezo** (2017-12-12):

Although that’s a very succinct way to describe it, the paper proposes an alternative method to obtain better concrete efficiency because the circuits of a formal verifier and all the proofs from the smart contracts would be prohibitively expensive by only using zk-S[NT]ARKs. Instead, a more efficient way is proposed:

(1) Certifiable certificates from Proof-Carrying Code: order of magnitudes shorter that their corresponding proofs.

(2) Instead of zk-S[NT]ARKs, there are better ways to obtain efficient zero-knowledge for general purpose Boolean circuits [ZKBoo, ZKBoo++, Ligero].

(3) Note that he combination of (1) and (2) subsumes most uses of zk-S[NT]ARKS.

The current approach of misplacing the burden of the proof of the correctness/security of smart contracts to users or third parties is severely limiting their adoption: it creates high transactions costs that are usually associated with market failures [1, 2]. The development and adoption of this technology would unleash this restrained demand, easily justifying its development and posterior use.

__

[1] [Econometrics of Contracts: an Assessment of Developments in the Empirical Literature on Contracting](http://www.development.wne.uw.edu.pl/uploads/Courses/institutional_masten_saussier.pdf)

[2] [Transaction Cost Economics: An Assessment of Empirical Research in the Social Sciences](https://scholarship.law.duke.edu/cgi/viewcontent.cgi?article=2287&context=faculty_scholarship)

---

**yhirai** (2017-12-13):

Is there something I can read about the size of certifiable certificates of proof-carrying code?

---

**dcerezo** (2017-12-19):

I have updated the [publication](https://eprint.iacr.org//2017/878) with a new sub-section 5.2 that covers that topic and references other publications.

