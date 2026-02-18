---
source: ethresearch
topic_id: 18551
title: Privacy preserving nullifiers for proof of identity applications
author: turboblitz
date: "2024-02-03"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/privacy-preserving-nullifiers-for-proof-of-identity-applications/18551
views: 4061
likes: 20
posts_count: 15
---

# Privacy preserving nullifiers for proof of identity applications

*Thanks [Jan](https://github.com/Janmajayamall), [Aayush](https://twitter.com/yush_g), [Yanis](https://twitter.com/yanis_mezn), [Michael](https://mrosenberg.pub/about) and [Maxence](https://www.linkedin.com/in/maxence-guillemain-d-echon) for feedback and discussions.*

A growing number of applications like [Proof of passport](https://github.com/zk-passport/proof-of-passport), [anon-aadhaar](https://github.com/anon-aadhaar/anon-aadhaar) and [zk-email](https://github.com/zkemail/zk-email-verify) use existing infrastructure from institutions to verify identities, respectively electronic passports, India’s Aadhaar system and DKIM registries. As they are based on already existing Public Key Infrastructure, building privacy preserving nullifiers can be quite tricky.

We’ll take the example of [Proof of Passport](https://github.com/zk-passport/proof-of-passport), but what is discussed here applies to many other projects. Proof of Passport allows users to scan the NFC chip in their government-issued passport and generate zk proofs showing that they have a valid identity. It can be used for proof of humanity, sybil resistance and selective disclosure of private data like nationality or age.

We want to build a proof of passport SBT that [displays information the user wants to disclose](https://testnets.opensea.io/fr/assets/goerli/0x64bfeff18335e3cac8cf8f8e37ac921371d9c5aa/0). It shouldn’t let someone mint two SBTs with a single passport.

Naively, one can think of using the hash of the government’s signature as a nullifier and storing it publicly. It does prevent reusage of a proof, but if the government keeps a database with all signature it has issued, it can link each nullifier with each user’s address. As the [ICAO specifications](https://www.icao.int/publications/pages/publication.aspx?docnum=9303) do not describe whether governments should do it or not, we can assume some governments keep those signatures. Additionally, anyone that gets access to the passport data before or after a mint can store it and deanonymize users. Same problem with zk-email: nullifying an email publicly deanonymizes the user to the mail server that signed the email.

Note that in the following constructions, we are not trying to hide the fact that a user minted a SBT from the government. This would be hard to do as the government has the same information as the user, and can just request a new SBT to see if the request is rejected or not. Instead, we’re trying to at least hide the user’s address from the government.

### Using a trusted server

One approach would be to let applications manage user privacy themselves. Each application would have a server with its own key pair that can sign government attestations so that:

\begin{aligned}
nullifier &= hash(server.sign(attestation))
\end{aligned}

The flow would be the following:

- The user extracts their government attestation from their passport and sends it to the application’s trusted server
- The server signs the attestation and hashes the result to get the nullifier. If it has already been included on chain, it refuses the request and responds \{false, \emptyset\}. If it’s not already included, it responds with the \{true, signature\}.

When the user submits the proof on chain, they shows that:

- The disclosed attributes (e.g. nationality) are valid given the government attestation
- The nullifier, a public output of the proof, is correctly computed as a hash of the server’s signature of the attestation

The nullifier is then stored on chain.

The server has to block duplicate requests because if it doesn’t, a government could pose as a user, send an attestation, get back a nullifier and identify the user’s address. Note that the government can still know if a user has minted an SBT, but not their address.

The main drawback here is obvious: the server sees every government attestation, so it can link every user’s attestation to its address. Also, there is a liveliness assumption on the server. This might be sufficient for some applications like a vote that happens only once. It can also be improved by keeping the secret in an SGX. But for long-lasting general purpose applications like the proof of passport SBT, it’s insufficient.

### Using two-party MPC

A better way to do it is using two-party MPC. This way, we can have the user and the server compute a circuit together so that the server does not learn the government attestation.

The circuit takes as inputs:

- The disclosed attributes, e.g. nationality (public)
- The government pubkey (public)
- The list of nullifiers already on chain (public)
- The server’s public key (public)
- The server’s private key (known only to the server)
- The government attestation (known only to the user)

Over MPC, the user and the server compute the signature of the attestation, hashe it and compare it with the nullifiers already posted. Just like before, if it’s included the circuit returns \{false, \emptyset\} and if it’s not included it returns \{true, nullifier\}. The user and the server then generate SNARKs proving they performed the MPC correctly and they can be verified on chain.

Note that we have to do the whole computation from disclosed attributes to nullifier over MPC and in one proof. If we tried to split it so that only the nullifier generation is done over MPC, the user’s proof would have to disclose the government attestation or something deterministically derived from it, which would allow the government to identify them.

Now, the server can’t link user’s attestations to their addresses. However:

- If the server colludes with the government and shares its private key, they can deanonymize users.
- There is still a liveliness assumption on the server

### Using n-way MPC

If we had something like [iO](https://en.wikipedia.org/wiki/Indistinguishability_obfuscation), we could do an obfuscated inclusion check on chain. This way, if a government tried to provide the same proof as a user, it would be able to know if the SBT was already minted, but not to which address. We can try to emulate this by extending the MPC setup. It also relaxes the liveliness assumption on a single server.

A rough flow would be:

- Nodes join a network. This can be done on top of EigenLayer so as to slash nodes that misbehave.
- The circuit is computed by the user together with the nodes. This time, the server secret is a threshold secret reconstructed from t/N nodes.

Again, each participant can prove correct computation using a snark. In particular, nodes show their secret is consistent over time by showing the hash of their secret is always the same. This guarantees the reconstructed secret is always the same, which makes the nullifier generation deterministic.

Signing the attestation with a threshold private key can be replaced with hashing it with the threshold secret for convenience.

To avoid putting a large burden on the nodes, it might be possible to adapt the design to something closer to [Octopus](https://ethresear.ch/t/octopus-contract-and-its-applications/17844).

Something very similar can be done with threshold FHE. The main difference is that instead of being part of the setup, the user encrypts the attestation with their FHE private key, makes their evaluation key public, and at the end of the process decrypts the encrypted nullifier before posting it on chain. Depending on the overhead of threshold FHE, this could be lighter for the user, but probably heavier for the nodes.

But this setup raise new issues:

- Leaking secrets is undetectable. A government corrupting t nodes privately could deanonymize every user. It would be possible to slash nodes only if they make their secret public to everybody. We can still have some cryptoeconomic security, but it’s insufficient if we assume governments are willing to forgo tens of millions in slashing rewards.
- There must be a way for nodes to rotate, so secrets need some way to be shared or at least added and removed.
- After some turnover, there will be a point at which nodes that stopped restaking or taking part in the computation can collude at no cost and deanonymize everyone.

### Using embedded private keys

A growing number of official documents like [new passports](https://hackmd.io/@TCEn_IDhTDWLjwyItiiBcQ/BJ4LX0m9p), [most of EU’s ID cards](https://www.inverid.com/blog/European-Identity-cards) and Japanese [Myna Cards](https://github.com/MynaWallet) not only contain a signed attestation from the issuing authority, but also their own public-private key pair. Authentication is done dynamically by asking the chip to sign a message. This is called active authentication, as opposed to passive authentication. It prevents cloning by simply copying the attestation on a forged document.

Most smart cards are designed to generate their own private key so that it can never leave the chip. If a passport is made this way, the government attests to the public key without ever knowing the private key. In this case, we can construct a privacy preserving nullifier as the hash of a signature of a fixed message.

\begin{aligned}
nullifier = hash(chip.sign(\text{"NULLIFIER"}))
\end{aligned}

We can prove in a SNARK that the signing private key is correctly derived from the attestation, but it’s impossible for the government to deanonymize the user without knowing their private key.

Some documents do not support Active Authentication but only Chip Authentication. Chip authentication does not allow for signing messages but performs semi-static ECDH. It involves a scalar multiplication on a secure elliptic curve so it can be used for nullifier generation in the same way.

This design is really cool because it doesn’t only hide the address of the user, it can also make it impossible for the government to even know if a user has minted a SBT, as it can’t produce the right signature.

Unfortunately:

- We do not currently know how much authorities generate the private keys on the chip vs embed them and store them in a registry. Please reach out if you know more about this.
- This doesn’t work with passive attestations like anon-aadhaar, email DKIM signatures and older passports.
- This only works if the signature is deterministic. The ICAO docs allow for RSA or ECDSA to be used. If there is no way of choosing the random k used in ECDSA, then it only works with RSA.
- It does not prevent someone accessing the document before or after the mint from recording the same signature and deanonymizing the user.

### Other approaches

If some application needed to always combine multiple sources, we could nullify the combination using a hash of multiple attestations. This way, all institutions involved would have to collude to deanonymize users.

Another approach would be storing hard hashes (Argon2, PBKDF2 or scrypt) of nullifiers to make them harder to check. It would make checking a large set of people impractical, but an attacker looking for one person could easily find it.

Another approach would involve biometrics. The photo signed in the passport chip looks too low-resolution to do any significant [zkml](https://github.com/zkonduit/ezkl), but using FaceID or TouchID to sign deterministic messages from a smartphone’s secure enclave might be promising while adding a relatively low trust assumption.

We are actively looking for better ideas. Please reach out if you have one!

## Replies

**secparam** (2024-03-29):

There’s an easier and completely trustless way to have a nullifier for minting a credential that is unlinkable from using the credential. You have a layer of indirection between converting the passport to a credential and using it. You use the passport as a zk-supporting-documentation to prove you should be issued the credential, reveal anything you want, but showing the credential you get is done separately. To issue issuing credentials trustlessly, you put the credential on a blockchain or transparency log. To show, you prove membership in the log, Zcash/tornadocash style.

The idea is from a 2014 paper [Decentralized Anonymous Credentials](https://eprint.iacr.org/2013/622.pdf), and a newer paper [zk-creds](https://eprint.iacr.org/2022/878), which gets composability and support for passports using SNARKs. In the second paper, we can safely reveal the signature on the passport when issuing a credential, preventing double registration, and we can add fields and even secret keys to the credential that are unknown anyone, including the passport authority. You can even do cool things like make sharing credentials with people and using them too much trustlessly de-anonymize the credential and revoke it.

![](https://ethresear.ch/user_avatar/ethresear.ch/turboblitz/48/10155_2.png) turboblitz:

> Note that in the following constructions, we are not trying to hide the fact that a user minted a SBT from the government… Instead, we’re trying to at least hide the user’s address from the government.

Note, this leaks that user registered, which I assume is ok from the what you said.  If you want to now make an address not connected to registration, you need to use the credential to make the address. You can easily make one time use credentials to allow the user to only make one address per credential.

---

**Lev-Stambler** (2024-08-02):

There is a relatively straightforward modification to the trusted scheme to remove the trust from the server. The following is a brief outline for the idea but by no means a replacement for a fully proved/ put together protocol.

Basically, you want to make use of [blind signatures](https://en.wikipedia.org/wiki/Blind_signature) where the server can sign a message without learning its underlying content.

Rather than having the server reject/ accept a signature, the server can simply sign every incoming message via the following interactive protocol between Alice and the Sever.

## The protocol

First, we will associate key pair (pk, sk) with the server that they use for signing. The the protocol proceeds as follows:

### Alice:

- Produce attestation att to passport. We’re going to assume that att is deterministically produced (i.e. is the same every time)
- Sample randomness for the server via a random oracle, H to get r = H(att)

### Alice and the Server:

- Will use shared randomness, r, as the seed randomness for the blind signature protocol
- Alice and the server engage in the (possibly interactive) blind signature protocol so that Alice produces a signature \mathbf{s} as well as a proof that H(att) was the seed randomness for the signing protocol

### Verification

- We then will set
nullfier = hash(\mathbf{s})
- When submitting a proof on chain, Alice will prove whatever necessary disclosed attributed, that nullifier = hash(\mathbf{s}) where \mathbf{s} is a valid signature of att under the server’s public key pk, and that the seed randomness used to produce \mathbf{s} is H(att).

## Why it works (intuitively)

Basically, a valid signature of att under public key pk has high (pseudo)-entropy to every party not holding the secret key sk. So, dictionary attacks on the part of the government no longer work.

Every attestation, att, also is associated with one unique nullifier which will pass all the verification checks and so uniqueness is preserved.

#### Remark on producing proofs

This may or may not be very technically tricky depending on what blind signature protocol is used. The choice of protocol heavily depends on application. If long term soundness/ privacy is required, you may want to use a post-quantum protocol.

### PS

This is not my area of expertise, and I may be wrong somewhere in the above.

---

**turboblitz** (2024-08-09):

Hi, thanks for the message!

This solution is good in that it prevents the server from learning the attestation of the user. It’s akin to the two-party MPC described above, or VOPRF.

There is still a liveliness assumption on the server, and more importantly the server colluding with the issuer can deanonymize all users. This is because the blind signature scheme has to be deterministic, so that nullifiers are fixed for each attestation, so the issuer having all the attestations and obtaining the server’s private key could recompute all the nullifiers. It goes as follows: compute all r=H(att), compute all s=blindsign(sk, r), then compute all nullfier=hash(s).

The issuer can also check if a specific person registered by getting a signature of r from the server and hashing it.

To tackle this problem in contexts like shadow election, the [FreedomTool](https://freedomtool.org/) team is working on an implementation using TEEs, which seems like a reasonable compromise for most use cases.

---

**nanaknihal** (2024-08-14):

We encountered the same problem. Here is our proposed solution, a threshold VOPRF – I think it might help. [A Threshold Network for “Human Keys” to solve privacy and custody issues](https://ethresear.ch/t/a-threshold-network-for-human-keys-to-solve-privacy-and-custody-issues/20276)

---

**barajeel** (2024-10-23):

How can the proposed nullifier system be adapted to ensure compliance with varying global privacy regulations while maintaining user anonymity?

---

**MicahZoltu** (2024-10-24):

Compliance and privacy are at odds with each other, because compliance means stripping away privacy.

---

**wldksa007** (2024-11-17):

How can long-term privacy protection be ensured, considering the risks of secret leakage in multi-server and MPC-based solutions, especially in the context of resilience against node compromise?

---

**donat55** (2024-11-17):

How does the proposed use of embedded private keys in official documents, like new passports and ID cards, enhance privacy and security in the generation of nullifiers, and what are the potential limitations or challenges associated with this approach?

---

**garyrob** (2024-11-18):

If anyone knows of open-source software implementing one of these schemes, please share! Also, a reference to relevant legal considerations would be useful.

---

**p4u** (2024-11-19):

I’m not fully up-to-date regarding this discussion, sorry if I’m not providing a realistic solution.

Would it make sense to create a global zk identity registry? Where identities are zk and nullifier friendly?

Let’s call this new identities “SIK” (secret identity key) which acts as user commitment. Each SIK is linked to a Public Key.

The SIK is forged through hash(pubKey || secret). The secret can manifest as a password, a hashed ECDSA signature or any deterministic entropy input.

The SIK compilation resides in a Snark-Friendly Merkle tree (i.e Circom SMT). In this Merkle tree, the hash of the passport public key delineates the path to a specific leaf where the SIK is stored. The Root of the tree is stored by the Ethereum smart contract.

To add or update a SIK, the user needs to provide:

- a signature over its new SIK
- the publicKey
- the government proof (a signature over the publickey?)
- the new root of the merkle-tree
- a zkProof as the transition to the new root is correct (only adds/updates its SIK)
- something else I’m probably missing…

The smart contract verifies everything and if so, updates the root.

So at this point we have a Merkle-Tree with SIKs (user commitments).

Then any application can make use of this registry. For instance, a voting application might require:

1. A Signature done with the Passport
2. A zkProof as:

the publicKey signing, has an assigned SIK on the Root merkle-tree
3. The application nullifier, which is constructed by hash(secret + somethingElse)
4. The user knows the secret which, together with the publicKey generates the SIK

At Vocdoni we have been using a similar approach to this for anonymous voting on ECDSA signatures. But as I said, sorry if it does not actually solve the issue you are facing.

---

**MicahZoltu** (2024-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/p4u/48/6501_2.png) p4u:

> Would it make sense to create a global zk identity registry?

Who issues IDs for this registry?  This is the hard problem.  If it is totally open access, then a big random number generator works great and is already available in the form of private key generators.  If it is restricted access, then you are right back to the centralization problem that allow some centralized actor to censor some subset of users.

Of course, being able to prove set inclusion in some centralized list without giving third parties details about you is great, but you need to get government buy-in for most of the value here (since that is usually where identity comes up), and awesome technical solutions won’t solve that problem and it is rare that governments choose the right solution to problems, usually they just choose the most easily sold solution.

Once you have a list of IDs (could just be numbers), proving that you know a secret associated with an item in that list is one of the simplest problems to solve with a ZK circuit.  Alternatively, users could get something like a JWT signed by the ID issuer that attests to your inclusion in the list, no need for ZK anything here and third parties won’t know who you are, just that you are attested by the ID issuer.

---

**p4u** (2024-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/turboblitz/48/10155_2.png) turboblitz:

> signed attestation from the issuing authority

OK, I see, thanks.

From the original post, I understood there is already a signed attestation from the issuing authority over the electronic Passport data (including public key). And the issue was to generate a Nullifier.

---

**Madmaxs2** (2024-11-22):

How can we design a privacy-preserving nullifier system that ensures robust anonymity against both government and third-party deanonymization attempts while maintaining practical scalability and usability for widespread applications like Proof of Passport?

---

**Trarda54** (2024-11-23):

Is it possible to create a decentralized solution for private nullifiers without relying on servers or governments , using zk-SNARKs or FHE ? What are the main risks and ways to minimize them ?

