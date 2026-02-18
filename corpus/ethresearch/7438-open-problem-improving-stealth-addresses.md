---
source: ethresearch
topic_id: 7438
title: "Open problem: improving stealth addresses"
author: vbuterin
date: "2020-05-16"
category: Cryptography
tags: []
url: https://ethresear.ch/t/open-problem-improving-stealth-addresses/7438
views: 8745
likes: 22
posts_count: 25
---

# Open problem: improving stealth addresses

[Stealth addresses](https://hackernoon.com/blockchain-privacy-enhancing-technology-series-stealth-address-i-c8a3eb4e4e43) in their most basic form work as follows:

- Every recipient publishes an elliptic curve point P (they know the corresponding private key p)
- If I want to send a payment to you, I generate a random value r, and I send the payment to an address with the public key P * r (I can generate the address locally)
- I tell you r offline so you can claim the funds using the private key p * r

This allows paying a recipient without the public learning even that the recipient has been paid (think of the recipient’s key P as being *publicly* associated with some real-world identity, eg. via ENS). However, this protocol has the downside that some offline channel is required to learn r. One option is to encrypt r with P and publish this to the blockchain, which solves the problem but it comes at an efficiency cost: the recipient now has to scan through all stealth transactions to learn about any payments that are for them.

Some of the proposals in the [above link](https://hackernoon.com/blockchain-privacy-enhancing-technology-series-stealth-address-i-c8a3eb4e4e43) can solve this problem by assuming that the recipient knows which sender will send them funds, but this is not always the case; sometimes, the sender may even want to be anonymous.

The challenge is: can we improve these protocols in such a way that reduces the scanning overhead for the recipient? The approach above has ~64 bytes and one elliptic curve multiplication per transaction in the anonymity set; can we do better?

There are information-theoretic arguments that show some limits: there must be at least O(N) information that the *total* set of recipients must listen to, as it must somehow contain for every recipient the information of whether or not they received a transaction. If each sender only modifies O(1) elements in this information, then the recipients would have to do an O(N)-sized scan, or else the senders would have to know which portion of the data the recipient is scanning, which can be used to detect transactions that are more likely going to the recipient.

Note that enlisting off-chain actors to perform complicated work (eg. updating the entire dataset after each transaction) to assist the recipients is acceptable.

Here is one fairly inefficient and complicated (but reasonably elementary in the mathematical sense) solution that seems to work:

- Every recipient r picks a prime d_r and generates a hidden-order RSA group (ie. a modulus n_r = p_rq_r) such that the order of 2 is a multiple of d_r. They publish n_r. The list of all d_r values is published through a mixing protocol, so which d_i corresponds to which n_i is unknown. (note: this assumes phi-hiding)
- For every recipient, publicly store a state variable S_i, an integer modulo n_i, which is initialized to 1.
- To send a bit to some recipient r, perform the following procedure. Let n_1 ... n_k be the list of moduli. For every 1 \le j \le k, compute w = 2 ^ {d_1 * d_2 * ... * d_{j-1} * d_{j+1} * ... * d_k} (note that d_j is skipped). Set S_i \leftarrow S_i * w.
- Note that the discrete log base 2 of S_r modulo d_r changes, but the discrete log base 2 or S_t modulo d_t for t \ne r does not change. Hence, only recipient r gets a message and other recipients do not, but no one other than r learns that r got a message. Recipient r can check for messages at any time by computing the discrete log using the factors (p_r, q_r) as a trapdoor.

This does involve a *lot* of work, though it could be outsourced and incentivized and verified via some ZK-SNARK-based plasma scheme (the dataset would be stored off-chain to avoid huge on-chain gas costs for rewriting it).

Another alternative is to use fully homomorphic encryption to outsource checking: use FHE to allow some third party to walk through the entire set of encrypted values, decrypt each value, and return the values that decrypt correctly. Given FHE as a “black box protocol” this is conceptually simpler; it also means that complicated constructions to store and maintain data off-chain are not necessary. However, the FHE approach may be more expensive.

Edit: this problem feels very conceptually similar to [PIR](https://en.wikipedia.org/wiki/Private_information_retrieval) (either the access variant or the search variant) but not quite the same; the main difference is that each recipient must only be able to read their own values.

## Replies

**SebastianElvis** (2020-05-18):

What I can think of is that, there are two directions to optimise the verification overhead of stealth address: 1) optimising the verification overhead of each tx, 2) reducing the number of txs to verify by filtering.

For 1), the optimisation space is very small, as scalar multiplication on an elliptic curve seems to be the cheapest trapdoor function already. For 2), there seems to be a trade-off between privacy and verification overhead.

Let me informally prove this statement below. I cannot guarantee it’s fully correct, and I’m happy to be proven wrong.

We shatr from proving the necessity of the randomness r for constructing stealth address.

**Lemma 1**: To receive money without revealing the receiver’s address, 1) the sender should always use a secret r and send r to the receiver privately, and 2) the receiver should always scan all txs on the blockchain to find txs going to himself.

**Proof**: Without the first condition, each stealth address can be mapped to a real address deterministically, which leaks the real address.The second condition is always necessary regardless of the stealth address. Consider payments without stealth address, the receiver should still compare his address with addresses in txs on the blockchain.

Then, we identify the security foundation of the stealth address, namely the CDH.

**Lemma 2**: To break the privacy guarantee of stealth address, one should break Computational Diffie-Hellman.

**Proof**: Easy from the security proof of the stealth address, i.e., prG = pR = Pr.

CDH relies on a trapdoor function. So far the most practical trapdoor function seems to be the elliptic curve scalar multiplication already. I don’t know any trapdoor function that is more lightweight than this. If there exists one, replacing EC scalar multiplication with this trapdoor can speedup verification directly.

Then, we consider the second possibility: filtering txs so that the receiver only needs to perform trapdoor functions on a subset of txs rather than all txs.

Here is a simple solution. In a nutshell, each tx attaches a short prefix of the receiver’s PK, and the receiver only needs to run trapdoor functions over txs with his PK’s prefix.

Each tx attaches an extra byte b equal to the first byte of the receiver’s PK. Upon a tx, the receiver checks whether his PK’s first byte equals to this tx’s b. If no, then this tx is not for the receiver. If yes, the receiver further computes the trapdoor function to see whether this tx is really for himself.

This allows the receiver to run trapdoor functions on \frac{1}{16} of all txs only.

However, the privacy downgrades for 16 times in the meantime, as the search space narrows down for 16 times.

It’s easy to see that, given a fixed trapdoor function, there is a trade-off between privacy and verification overhead.

Less verification overhead -> fewer txs to verify using trapdoor function -> fewer txs to search for identifying the receiver.

---

**vbuterin** (2020-05-21):

Yeah I agree the linear privacy / efficiency tradeoff exists and can be exploited. I *do* think there may be fancier tricks that let us go down from 1 ECsig per transaction (in the anonymity set) to something closer to the theoretical minimum of a few bits per transaction though.

---

**SebastianElvis** (2020-05-22):

Then we should eliminate all asymmetric crypto operations. Consider using something like one-time address scheme. Assuming Bob wants to transfer 1ETH to Alice.

- Alice chooses a random string x
- Alice constructs a transaction tx with input of 1ETH in Bob’s address and output of 1ETH in Alice’s one-time address H(alice\_addr || x)
- Alice sends Bob tx, and Bob commits tx to the blockchain
- Alice scans txs on the blockchain to see if there is a transaction with output H(alice\_addr || x)
- When spending tx, Alice should show x

In short, this embeds a hashlock to the address, and Alice generates a one-time address scheme for receiving money everytime.

If Alice doesn’t want to construct tx herself, she can just send Bob H(alice\_addr || x) and let Bob do that.

If you want even more security, say anyone other than Alice can know who receives this money even with the knowledge of x, you can replace hash using a VRF. Only Alice can generate a proof. Unfortunately this requires EC operations again.

In this scheme, Bob cannot know Alice’s address, so cannot prove he sent Alice money. In addition, it only needs a hash function and Alice can scan txs efficiently, as she only needs to compare the one-time address with all addresses in existing txs (or just compare txid as she generated this tx).

The downside is that, creating receipts can be hard in this scheme.

Note that this approach requires hard forks. Not sure if there is any other design consideration.

To me stealth address may not need asymmetric crypto.

Homomorphism (of EC scalar multiplication) adds no more security than the scheme above.

In the original stealth address scheme,

- Bob is responsible to choose r
- Bob can send Alice either r or R
- Bob still needs interaction with Alice, namely sending r/R

Bob sending R to Alice seems to hide the real value of r. This can somewhat prevent Alice from proving “she receives money from Bob”, as Alice should show her sk to prove this. I see no point of making “Alice receiving money from Bob” deniable and unprovable. Meanwhile, with r Bob can still prove he sent some money to Alice’s address by revealing r.

---

**vbuterin** (2020-05-22):

> When spending tx , Alice should show x

One big challenge with the scheme is here; showing `x` allows anyone else to create a spending transaction and potentially front-run her.

Additionally, third parties can’t generate stealth addresses by themselves; Alice has to generate the address for them, so it doesn’t quite fit into the same pattern.

---

**SebastianElvis** (2020-05-22):

> One big challenge with the scheme is here; showing  x  allows anyone else to create a spending transaction and potentially front-run her.

The output is hold by Alice. How can others create a transaction spending this money without knowing Alice’s secret key?

> Additionally, third parties can’t generate stealth addresses by themselves; Alice has to generate the address for them, so it doesn’t quite fit into the same pattern.

Like I said, Alice (the receiver) can be the one who creates transactions for Bob (the sender). And what do you mean by “third party” here? There seems to only have sender Bob and receiver Alice.

---

**vbuterin** (2020-05-22):

Ah sorry, I mean Bob can’t perform the entire procedure offline, and it requires interaction from Alice. That’s the property I was trying to achieve.

---

**SebastianElvis** (2020-05-22):

I see. Indeed Bob needs to wait for Alice to send the transaction to him. If we don’t want Bob to reveal Alice’s identity, then this is inevitable.

To make this protocol non-interactive (for Bob), what we can do is to let Bob choose the random number x, construct/commit a transaction with output H(alice\_addr || x), and sends x to Alice. This achieves the same security guarantee as the original stealth address, yet minimises Alice’s scanning overhead.

---

**seresistvan** (2020-06-24):

Vitalik observes the \mathcal{O}(n)/\mathcal{O}(1) tradeoff: namely if sender only modifies \mathcal{O}(1) number of bits, then recipient necessarily needs to do a \mathcal{O}(n) scan. The protocol described below shows that it is possibe to achieve \mathcal{O}(\log n)/\mathcal{O}(\log n) scan sizes asymptotically for sender and recipient. However the concrete efficiency of the scheme is terrible as it requires huge group elements.

**Preliminaries: the used cryptographic assumption**

Informally, the [quadratic residuosity assumption](https://en.wikipedia.org/wiki/Quadratic_residuosity_problem) states that given integer a and a a semiprime N such that (\frac{a}{N})=1 ([Jacobi-symbol](https://en.wikipedia.org/wiki/Jacobi_symbol)), it is computationally infeasible to decide without knowing the factors of N with success probability non-negligibly larger than simply guessing, whether a\bmod{N} is quadratic residue or not.

**Stealth transaction screening protocol**

*Setup*

Each participant i generates a modulus N_i=p_{i}q_i and publishes a quadratic non-residue \mathit{qn}_{i}\bmod{N_i} such that (\frac{qn_i}{N_i})=1. Since i knows the factors of N_i can easily generate such a quadratic non-residue \mathit{qn}_{i}. Each participants posts the pair (N_i,\mathit{qn}_{i}) to the blockchain and as of now let’s assume that the number of participants in the stealth address system is a fixed constant. We can furthermore assume wlog. that gcd(N_i,N_j)=1 for each i\neq j. Let N=\Pi_{i}N_i.

*Sending stealth transaction*

Let’s assume sender wants to send a transaction to participant with index i. Then sender generates k\in_{R}\{0,1\}^{\lambda}, where \lambda is the security parameter. Then sender computes x\in\mathbb{Z}_{N} such that x\equiv qn_{i}^{2k+1}\bmod{N_i} and for all j\neq i we want x\equiv qn_{j}^{2k}\bmod{N_j}. Such an x can be efficiently computed by applying the Chinese-Remainder Theorem. The motivation behind generating x this way is that it is a quadratic residue by definition modulo every non-recipient index, but it is a quadratic non-residue for the recipient. For every non-participating user quadratic residuosity with respect to any modulus remains hidden, unless they break the quadratic residuosity assumption. Sender attaches x to its transaction and posts it unto the blockchain. Note, that unfortunately the size of x is huge, which is a big disadvantage of the scheme. Given many stealth transactions, we build a binary tree using the x values as follows. Each non-leaf node is computed as the multiple of its children \mod N. See this figure for a tree containing 4 stealth transactions!

[![image](https://ethresear.ch/uploads/default/original/2X/8/8f1134199726f365bcb9f09ff5208b89c030be3f.png)image575×256 8.13 KB](https://ethresear.ch/uploads/default/8f1134199726f365bcb9f09ff5208b89c030be3f)

*Screening for a stealth transaction*

After every incoming stealth transaction either on-chain, but most likely off-chain we update the binary tree of the x_j values. The number of the leaves correspond to the number of stealth transactions. Whenever a user comes online, checks whether the root is quadratic non-residue with respect to her modulus. If no, then she did not receive a transaction. If yes, then checks which of the children is a quadratic non-residue with respect to her modulus and recursively can find the corresponding x_j value whose quadratic non-residuosity propagated to the root with respect to her modulus. Once this specific x_j was found, the referenced transaction on the blockchain can be found easily (for instance there will be an event which logs the x value of each stealth transaction). And then only the correct event needs to be fetched with the specific x_j value.

Altogether this method allows a logarithmic lookup of a stealth transaction in the number of all stealth transactions. However, the scheme is not practical, since all the values in the tree are prohibitively large, given that they are elements in \mathbb{Z}_N, where N is the product of all participants moduli.

**Immediate downsides**

1. Nodes in the tree are prohibitively large as they are elements in \mathbb{Z}_{N}.
2. Only an odd number of incoming stealth transactions can be detected this way as the effect of two incoming transactions would kill each other, since the multiple of two quadratic non-residues is quadratic-residue.

**Advantages**

1. Asymptotically interesting construction
2. It allows to detect not only whether recipient got a stealth transaction but also recipient can locate the stealth transaction in logarithmic time.

Could there be a way to make this scheme practical?

---

**vbuterin** (2020-06-25):

Isn’t N = \prod_i N_i an O(n) sized value, and so the x value that the sender needs to publish to chain would also be O(n) sized? How is this asymptotically better than more naive approaches? Is it optimized for a “many *transactions* but not many *users*” scenario?

---

**seresistvan** (2020-06-26):

Yes, you’re right. Indeed, x\bmod{N} would be a huge \mathcal{O}(n) sized value. I was taking the asymptotics in the number of stealth transactions and considered any group operation as constant regardless of the size of the underlying group. Maybe there is a tension between number of users and stealth transactions? Would be nice to have a scheme which is scalable to many users **AND** many stealth transactions.

Maybe one could demand from senders that x should be not more than, say 2048 bits. When sender sends a stealth transaction to participant j, then x is generated such that x\equiv qn_{i}^{2k}\bmod{N_i} for all i\neq j and  x\equiv qn_{j}^{2k+1}\bmod{N_j} by using the Chinese Remainder Theorem. *MAYBE* sender could choose the k values in a way, that the resulting x would be small. But I suppose the best approach would be for this is brute-forcing k unless factoring or composite DLOG is easy.

---

**vbuterin** (2020-06-26):

One way to improve concrete efficiency might be: have every participant declare, for every prime in \{2, 3, 5 ..... 997\}, whether or not that prime is a residue. Then Alice could just choose a random x, solve a linear system of binary equations to figure out which subset of those to multiply it by to make x have the right residuosity over all moduli, and use that value. Would still be O(n) but at least it would only be a few bits per participant.

---

**seresistvan** (2020-06-26):

Wow! This is a nice idea!

---

**seresistvan** (2020-06-27):

If I understand correctly your idea then it would allow essentially constant-sized leaves, say 2048-bits. Altogether this improvement yields logarithmic-sized tree root (in the number of stealth transactions). I suppose to maintain such a tree on-chain is prohibitively expensive. This makes the scheme *just a theoretic curiosity*.

Other major drawbacks/challenges none of the two proposed schemes above solved so far:

1. Fixed set of recipients
To make such a technique practical it must be permissionless. Namely, it should be able to support any parties to join the stealth transaction scheme after the stealth transaction scheme launched.
2. Security against malicious senders
Both of the proposed schemes implicitly assumed honest senders. Ie. they took granted that participants will insert leaves honestly in the tree or in Vitalik’s scheme they will compute the value S_i correctly. This obviously could be solved with simple zero-knowledge proofs, but would make the schemes even more inefficient as, in general, ZKPs for hidden order groups are quite inefficient, see Bangerter et al. This is obviously not true, if zk proofs are not needed to be posted on-chain.

---

**Varun2703** (2020-06-30):

This is a solution I came up with!

Notation :

M: Number of receivers

t : Index of last checked stealth transaction

t’ : Index of latest stealth transaction

R_i : receiver

S : Sender

**Setup**

Each receiver broadcasts a scan public key pk_i, for a homomorphic encryption scheme

An array A is initialized as [Enc_{pk_1}(0), … Enc_{pk_M}(0) ]

**Send**

To send a transaction to receiver R_i, the sender S creates an array,

txA = [Enc_{pk_1}(0), … Enc_{pk_1}(1),..., Enc_{pk_M}(0) ]

and computes

A' = txA + A = [Enc_{pk_1}(s_1), … Enc_{pk_i}(s_i + 1),..., Enc_{pk_M}(s_M)]

(Basically add an encryption of 1 to the receiver’s encryption and an encryption of 0 to all others.)

Sender broadcasts the updated A'

**Receive**

A receiver R_i comes online at index t’, (let the array A_{t'} be the array) and check if Dec(A_{t'}[i]-A_{t}[i]) > 0.

If yes, this implies that there exists a transaction for R_i in the interval [t,t’].

R_i then checks Dec(A_{t'}[i]-A_{(t’+t)/2}[i]) and Dec(A_{(t’ + t)/2}[i] - A_{t}[i]). The receiver can decide to go left or right and recursively compute the index of its transaction. The complexity of the receiver thus is O(log(t’ - t)).

Privacy of the recipient is guaranteed since only the receiver is able to decrypt the encryption at its index. With respect to efficiency, the receiver needs to do only O(log (t’-t)) checks.

Downsides:

- The sender needs to compute O(M) encryptions for each stealth transaction.
- O(M) encryptions will also be on the chain per transaction (this could be potentially stored offline, and only a merkle root hash needs to be on the chain)

Other nice things we can do:

- Receiver can reset its counter at any time by providing a new public key
- Sender can choose the set of anonymity by computing and sending update only on a subset m out of M of all receivers
- we can take an encryption scheme like Paillier where the receiver can also extract the randomness r used to encrypt. This could be the same r the sender also uses to build the actual stealth transaction. Now in the case that a cheating prover tries to create a transaction without using r can be caught and proven to be acting maliciously.

---

**vbuterin** (2020-06-30):

Does this approach require the sender to broadcast (publish to chain?) an O(M) sized piece of data? If so I do think that’s unfortunately too inefficient. On-chain data is expensive ![:frowning_face:](https://ethresear.ch/images/emoji/facebook_messenger/frowning_face.png?v=14)

That said, if you’re willing to use medium-degree somewhat-homomorphic encryption (ie. lattices), you can solve this whole problem by just outsourcing the search - which could in the long run be the most correct approach.

---

**GV** (2020-09-03):

The following protocol exploits the subgroup hiding assumption in groups of unkown order to hide a bit *(or few, see “Some considerations”)* of information sent to users’ public registers. This bit tells recipient if they received one or more stealth transaction from their last check.

In practice, the sender sends a 1 bit to the recipient of his stealth transaction, while sends the 0 bit to all other members in the anonymity set.

Feedbacks are welcome!

## The protocol

**Keygen.** User i generates two safe primes p_i= 2\tilde{p_i}+1 and {q_i} = 2\tilde{q_i}+1 and computes n_i = p_iq_i. It follows that |\mathbb{Z}_{n_i}^*| = 4\tilde{p_i}\tilde{q_i} = 4\tilde{n_i} and randomly chooses g_i,u_i of order \tilde{n_i} in \mathbb{Z}_{n_i}. Sets h_i = u_i^{\tilde{q_i}} \text{ mod }n_i (so h_i has order \tilde{p_i}) and publishes his public key as (n_i, g_i, h_i).

**Register Initialization.** Each user i initializes a public register S_i to h_i^{r_i} \text{ mod }n_i for a random value r_i and sets a secret register \omega_i to 1.

**Send.** A sender wants to send a secret bit b to user i:

- If b=1,  he chooses random a and computes w_i = g_i^a \text{ mod }n_i;
- if b=0,  he chooses random b and computes w_i = h_i^b \text{ mod }n_i;

he then updates user’s public register as S_i = S_i\cdot w_i \text{ mod }n_i.

**Receive.** User i computes s_i = S_i^{\tilde{p_i}} \equiv g_i^{\tilde{p_i}\sum_l a_l} \text{ mod }n_i and checks if s_i is equal to \omega_i. If they’re equal, he then received only 0 bits from his last check. If not, he received at least one 1 bit and updates his secret register \omega_i as \omega_i = s_i.

**Register Reset.** After receiving one or more 1 bit, each user i could reset his public register by computing w_i = S_i^{\tilde{q_i}-1}\cdot h_i^{r_i} for random r_i and letting S_i = S_i \cdot w_i \text{ mod }n_i. He then resets his secret register \omega_i to 1.

## Some considerations

- The values w_i can be aggregated to a single public value w using the Chinese Remainder Theorem, so that w satisfies w \equiv h_j^{b_j} \text{ mod }n_j for j \neq i and w \equiv g_i^a \text{ mod }n_i. In this case register updates’ can be publicly done by third parties but the bitsize of w is O(M) where M is the number of users in the anonymity set.
- The sender could privately update some public registers, while other updates can be delegated by publishing an aggregated (but shorter) value w on/off-chain. To hide senders actions, some updates can be performed by nodes in the network by sending 0 bits to random users.
- To allow receivers know how many 1 bits they received, the sender when sending a 1 bit to user i could compute the value w_i = g_i \cdot h^b \text{ mod }n_i, with b random instead (the h_i^b blinds the g_i when the public register is updated).  In this case the receiver has to bruteforce S_i^{\tilde{p_i}} \equiv g_i^{\tilde{p_i}\sum_l a_l} \text{ mod }n_i in base g_i^{\tilde{p_i}}. However it would be then necessary to implement a mechanism which enforces that no higher power of g_i is used (i.e. all a_l are at most 1).
- The Register Reset operation is optional and indistinguishable from a normal Send. It could be relevant in case the receiver keeps tracks of how many 1 bits he received (see previous point), so that the bruteforce is done for few values only per check.
- The secret register \omega_i defines and underlying notion of time: for example, the receiver could regularly checks at intervals of k blocks his public register by checking if he received 1 or more 1 bits: if S_i^{\tilde{p_i}} \text{ mod }n_i  is different from the last checked secret register \omega_i, it means that some sender multiplied his public register with a random \tilde{n}-order element and so there are new stealth transactions addressed to him in the last k blocks.

---

**kladkogex** (2020-09-03):

Well - what is described here does look very much like identify-based signatures.

There is a master key that can be used to derive private keys from public strings …


      [en.wikipedia.org](https://en.wikipedia.org/wiki/ID-based_cryptography)




###

Identity-based cryptography is a type of public-key cryptography in which a publicly known string representing an individual or organization is used as a public key. The public string could include an email address, domain name, or a physical IP address.
 The first implementation of identity-based signatures and an email-address based public-key infrastructure (PKI) was developed by Adi Shamir in 1984, which allowed users to verify digital signatures using only public information such as the user...

---

**seresistvan** (2020-09-03):

To me it seems that this construction is quite similar in its nature to the one described above using quadratic residuosity (QR). Note, that also the QR assumption is a subgroup hiding assumption of some sort. Vitalik’s idea for reducing the size of \omega also applies here. So you can claim \mathcal{O}(1) sizes for \omega at the expense of increased \mathcal{O}(M) sender computation for generating the correct \omega.

It is cool that you can “store” several bits in the register.

---

**GV** (2020-09-03):

[@kladkogex](/u/kladkogex) Looks interesting, but I didn’t really get how it applies here. IDB is not my area, but from the Wikipedia description the advantage seems to be that senders can generate receivers’ public key on the fly and send their bits: this would indeed improve efficiency (no need to download PKs)although you would need a central authority, which usually is not desiderable… If you meant another application could you please elaborate more with a small example?

[@seresistvan](/u/seresistvan) Yes they have clear similarities, although this construction solves the problem of not detecting an even number of received transactions.

---

**seresistvan** (2020-09-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/g/977dab/48.png) GV:

> this construction solves the problem of not detecting an even number of received transactions.

Fwiw, I think, also the QR construction can easily be made to support several incoming transactions. But in that case, you need to assume and rely on the hardness of the [higher residuosity problem](https://en.wikipedia.org/wiki/Higher_residuosity_problem). The whole construction could be generalized into that direction. Receiver could check higher residues on her end, not only just quadratic (non-)residues.


*(4 more replies not shown)*
