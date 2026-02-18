---
source: ethresearch
topic_id: 9039
title: On the (im)possibility of privacy-preserving quadratic funding
author: seresistvan
date: "2021-03-29"
category: Privacy
tags: [transaction-privacy]
url: https://ethresear.ch/t/on-the-im-possibility-of-privacy-preserving-quadratic-funding/9039
views: 2670
likes: 0
posts_count: 3
---

# On the (im)possibility of privacy-preserving quadratic funding

***Privacy?***

In this post, we ask the question, whether we can achieve privacy-preserving quadratic funding or what  privacy guarantees one can even hope for in this context. The post is only intended to be a discussion-starter, so don’t expect any rigorous arguments/protocols/solutions! (not yet!)

[Quadratic funding](https://poseidon01.ssrn.com/delivery.php?ID=515027005118071087107089121017093006004012017087001025006118127010070102078068114028123027038060024046098070113066125009114100010016003015051068027126087102110109105073077091088093103093069079111018122077083066083084111078064098095118091093025009100078&EXT=pdf&INDEX=TRUE) is one of the most exciting and important developments in public goods mechanism-design by Buterin, Hitzig, and Weyl since the [1970s](https://en.wikipedia.org/wiki/Vickrey%E2%80%93Clarke%E2%80%93Groves_mechanism). A more accessible primer on quadratic funding (QF) can be found [here](https://vitalik.ca/general/2019/12/07/quadratic.html). QF has already been implemented and successfully used in funding [Gitcoin’](https://gitcoin.co/)s grants. Gitcoin’s 9th round has just been finished a few days ago with [many](https://gitcoin.co/grants/explorer/) [fascinating](https://gitcoin.co/grants/258/beaconchain-open-source-eth2-blockchain-explorer) [projects](https://gitcoin.co/grants/543/the-moonmath-manual-to-zk-snarks).

***Motivation***

You don’t want the whole world to know that, for instance, you [supported Edward Snowden](https://edwardsnowden.com/donate) with 10k in DAI. It might be the case, that in your jurisdiction (e.g. in the US.) [it is unlawful](https://www.zdnet.com/article/snowden-donations-rocket-after-obamas-cybersecurity-order-outlaws-fund/) to support such a “criminal”.

**Setting: super short background on QF**

In QF, we have 3 types of participants.

*Senders*: these are the people who wish to fund public goods in the ecosystem.

*Recipients*: these are the people who seek to receive funding to be able to deliver their awesome public goods.

*Smart contract/Matching pool*: there is a smart contract on chain (or might be a trusted benevolent party) who holds the matching pool. The pool is provided by benevolent actors to match the contributions of the senders according to a quadratic formula detailed below.

**Quadratic Funding formula**

Essentially, parties want to compute the following formula in a privacy-preserving manner. Suppose a project received k contributions from senders each sending a contribution with value of c_i for i\in[1\dots k]. Then, according to the QF formula the project altogether receives (\Sigma_{i=1}^{k}\sqrt{c_i})^2 funding.

**Wanted Privacy Guarantees**

Let’s briefly review what privacy guarantees one might hope for in a privacy-preserving Gitcoin!

**Sender anonymity**

Sender’s identity unfortunately needs to be known. This has to do with [avoiding collusion attacks](https://vitalik.ca/general/2019/04/03/collusion.html) against the mechanism, which cannot be circumvented without introducing identities. For example, Gitcoin relies on Github identities.

**Sender confidentiality**

If we cannot hide the fact that we participated in a Gitcoin grant round, can we hide the amount we contributed to a project? Sure! With confidential transactions, this problem can easily be solved.

**Receiver anonymity and confidentiality**

We also would like to have privacy about the projects we supported. The easiest solution would be to just use stealth addresses for funding the public projects. Imagine that each project publishes a public key on-chain that would allow any sender to contribute to the projects in an unlinkable fashion. However, in that case the smart contract/matching pool would not be able to compute the QF formula at the end of the matching round. This could potentially be solved with some clever zero-knowledge proof system, where you prove that you received k incoming transactions each of them having value c_i and you want your rightful matching contributions.

**Vision**

Most likely, a confidential QF mechanism could be implemented with the help of confidential notes akin to [AZTEC confidential notes](https://medium.com/aztec-protocol/an-introduction-to-aztec-47c70e875dc7). Obviously, there might/will be some privacy loss whenever people enter and leave the confidential pool to exchange their funds from/to confidential assets. This is the curse of Ethereum not having privacy/confidentiality/anonymity by default. But, this seems to be the best approach we can hope for.

## Replies

**vbuterin** (2021-03-30):

Have you looked at [GitHub - appliedzkp/maci: Minimal anti collusion infrastructure](https://github.com/appliedZKP/maci) and http://clr.fund/ ?

The current versions don’t solve privacy with respect to the operator, though I think you should be able to add an inner ZK layer to add that (and until then, just run MACI inside an SGX).

---

**SebastianElvis** (2021-08-25):

It seems that the sender-anonymity, sender-confidentiality and receiver-anonymity can be satisfied simultaneously, and achieving receiver-confidentiality is tricky.

To achieve sender-anonymity (i.e., hide the sender’s identity), the system can employ a Tornado-cash-style mixer in front of the matching process. Specifically, when depositing coins for funding projects, the sender has to decompose its coins into a number of fixed-amount notes (1 ETH, 10 ETH, 100 ETH, …). To fund a project, the sender can only use these fixed-amount notes. Then, even if the adversary can observe the sender deposits some coins into the system, it cannot learn what projects the sender funds. If the sender funds more projects with more coins, the sender has larger anonymity set and thus achieves better sender-anonymity.

Sender-confidentiality (i.e., hiding the amount) is also achieved based on the above mechanism. Another approach, as you suggested, is using confidential transactions.

To achieve receiver-anonymity (i.e., hide the receiver’s identity), the receiver (rather than the senders) can choose a unique random number r, generate a stealth address with r totally by himself, and send the stealth address to the senders secretly off-chain. The receivers can send money to the stealth address without revealing the receiver’s real address.

To achieve receiver-confidentiality (i.e., hide the the amount of coins received), the system should not allow the QF function to be calculated on-chain. This will make the guarantee quite different from the non-private one, where all funds are known on-chain. If we really want this property, then the receiver can use the traditional stealth address scheme (using a unique address for each transaction). Each receiver calculates its own QF function and reveals the amount when necessary.

