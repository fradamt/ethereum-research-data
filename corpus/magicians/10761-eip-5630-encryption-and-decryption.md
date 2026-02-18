---
source: magicians
topic_id: 10761
title: "EIP-5630: Encryption and Decryption"
author: firnprotocol
date: "2022-09-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5630-encryption-and-decryption/10761
views: 11691
likes: 68
posts_count: 131
---

# EIP-5630: Encryption and Decryption

Opening the discussion for EIP-5630; see **edit:** link to the EIP: [ERC-5630: New approach for encryption / decryption](https://eips.ethereum.org/EIPS/eip-5630)

## Replies

**darcys22** (2022-09-10):

I love this idea, a pretty big thing i wanted for ERC5570 was to encrypt the receipts so they were private. So wanted a way for a business to encrypt the metadata of an nft against the owners address.

This implementation seems to separate the decryption key, this is great because it would mean you could provide the decrypting key to an external financial system without giving it the ability to sign transactions and send fund.

---

**firnprotocol** (2022-09-10):

exactly! and yes, you’re correct that the decryption key is separated. appreciate the feedback.

---

**SamWilsn** (2022-09-19):

Is retrieving a recipient’s public key out of scope for this EIP? If so, would you be open to working on a standard for doing that as well? I’ve been toying with the idea of publishing PGP keys to ENS. Perhaps something like that would work.

---

**firnprotocol** (2022-09-19):

good question. retrieving the public key is very much *in* scope, and is in fact spec’d out in the EIP. **edit** what’s spec’d is a *local* RPC routine to retrieve *your own* public key. what you then do with that—e.g., whether you publish it to ENS, or something else—is not (currently) in scope. perhaps there should be a separate EIP to dictate how exactly that key gets serialized and published to ENS?

I’m pretty sure PGP keys are RSA; we are opting to use `secp256k1` keys instead. this is essentially for cryptographic and compatibility reasons. but other than that—yes, publishing these to ENS would be absolutely a good idea! let me know if you have questions.

---

**Pandapip1** (2022-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/firnprotocol/48/7909_2.png) firnprotocol:

> I’m pretty sure PGP keys are RSA;

If you want to use GPG keys instead, those support many more schemes - including ECDSA

---

**firnprotocol** (2022-09-19):

hmm. it would be intriguing to make our `decrypt` spec exactly match what GPG does. if possible. GPG [says that](https://wiki.gnupg.org/ECC) they support “ECDH” over `secp256k1`. (this is confusing, since, ECDH is a key agreement scheme, not an encryption scheme. so I assume they actually mean ECIES?)

---

**firnprotocol** (2022-09-19):

update: as far as I can tell, GPG *doesn’t* support full-on ECIES, only ECDH. so drop-in replacement might not be viable. moreover, it appears that their ECDH spec makes some weird choices, [including a KDF](https://www.rfc-editor.org/rfc/rfc6637#section-7) which differs from [SEC 1, § 3.1.6] (in particular, they put the 4 counter bytes on the left of the message, instead of on the right). so not sure how fruitful this direction is. note that implementing SEC 1-compliant ECIES “from scratch” is not difficult; we’ve already built a reference implementation at [GitHub - firnprotocol/eth-sig-util at encryption](https://github.com/firnprotocol/eth-sig-util/tree/encryption) (using a very good existing library).

so, to put it simply, i think the idea is absolutely the right one, but whether we “formally” can agree with GPG is hard to say. in any case, you can get the same functionality regardless.

---

**kdenhartog** (2022-09-19):

ECDH is being used to setup a symmetrical encryption key rather than using asymmetric encryption (ECDH) since asymmetric is notoriously slow in comparison when encrypting large messages and hits other cryptographic limitations that aren’t traditionally faced.

I still don’t believe the current design here is a good fit as it’s only a one way encryption scheme meant only to encrypt messages from the dApp to the wallet.

---

**kdenhartog** (2022-09-19):

When you say a “recipient’s key” who would be playing the role of a recipient?

---

**kdenhartog** (2022-09-19):

Can we take a step back here and align on what use case we’re trying to solve and what’s the threat model we’re trying to address? I don’t think we’ve got alignment on that yet.

---

**firnprotocol** (2022-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> I still don’t believe the current design here is a good fit as it’s only a one way encryption scheme meant only to encrypt messages from the dApp to the wallet.

I’m truly at a loss to understand your objection, to be honest. All public-key encryption schemes are “one-way”, by definition. And *no*, encryption from dApp to wallet is *not* the only intended use here.

---

**SamWilsn** (2022-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> I still don’t believe the current design here is a good fit as it’s only a one way encryption scheme meant only to encrypt messages from the dApp to the wallet.

Ah, I see. So this EIP is more about creating a secure keystore than it is about general purpose encrypted messaging. The note about e2e encrypted messaging threw me off.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> When you say a “recipient’s key” who would be playing the role of a recipient?

I’m imagining the scenario where you want to send me an encrypted message without having communicated beforehand. I would be the recipient.

In light of my new understanding above, I guess the pattern would be to:

1. Create a new public/private key pair.
2. Publish the public key using some other EIP (maybe using ENS.)
3. Request an encryption key using eth_getEncryptionPublicKey.
4. Encrypt the private key created in (1) using the the key from (3).
5. Publish the encrypted private key using some other EIP.

Then anyone wanting to message me could retrieve my public key from ENS, and send the message. I could read the message by fetching my encrypted private key, decrypting using `eth_decrypt`, and then decrypting the message.

---

**firnprotocol** (2022-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Ah, I see. So this EIP is more about creating a secure keystore than it is about general purpose encrypted messaging. The note about e2e encrypted messaging threw me off.

That is not the intention—we *do* want to be able to support e2e messaging here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> In light of my new understanding above, I guess the pattern would be to:
>
>
> Create a new public/private key pair.
> Publish the public key using some other EIP (maybe using ENS.)
> Request an encryption key using eth_getEncryptionPublicKey.
> Encrypt the private key created in (1) using the the key from (3).
> Publish the encrypted private key using some other EIP.
>
>
> Then anyone wanting to message me could retrieve my public key from ENS, and send the message. I could read the message by fetching my encrypted private key, decrypting using eth_decrypt , and then decrypting the message.

I think this is more complicated than you need! here would be the flow:

1. locally call eth_getEncryptionPublicKey; obtain a public encryption key.
2. post that key to your ENS.

then whenever anyone wants to encrypt to you, they retrieve the public key from your ENS, encrypt locally, and then send the ciphertext to you. you decrypt using `eth_decrypt`. no need to generate a separate keypair, and encrypt its secret key.

---

**kdenhartog** (2022-09-19):

> And no , encryption from dApp to wallet is not the only intended use here.

Cool let’s start by listing off the ones that we’re working for here because in my experience building 2 versions of an asynchronous messaging protocol (DIDComm V1 and V2) we’re going to go around and around in circles on this if we don’t define this first.

---

**firnprotocol** (2022-09-19):

sure. i think our preliminary list of target use cases can be:

1. encrypt/decrypt from a dApp to a user’s wallet.
2. end-to-end encrypted messaging.

(1) we’ve already discussed—but I think we’re also fully equipped to support (2) in this EIP too (if you think otherwise, let me know why). namely, the flow would be as suggested above:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/firnprotocol/48/7909_2.png) firnprotocol:

> locally call eth_getEncryptionPublicKey; obtain a public encryption key.
> post that key to your ENS.
>
>
> then whenever anyone wants to encrypt to you, they retrieve the public key from your ENS, encrypt locally, and then send the ciphertext to you. you decrypt using eth_decrypt.

let me know your thoughts.

---

**firnprotocol** (2022-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/firnprotocol/48/7909_2.png) firnprotocol:

> then send the ciphertext to you

as far as the details of how to “send”: though it’s probably out of scope for this EIP (and might be worth a separate EIP), one way to do it would be to create a simple contract (or extend ENS) with a `mapping (address => bytes[])`, essentially associating to each address / ENS name an arbitrary-length, *append-only* list of ciphertexts. anybody could freely append a ciphertext, i.e. a `bytes`, to this list—it’d be the “inbox” for that ENS. then the user can trivially go through this list and locally `eth_decrypt` each new message it gets.

there could even be a fun extension where you have to pay someone to send them a message.

---

**kdenhartog** (2022-09-20):

> encrypt/decrypt from a dApp to a user’s wallet.
> end-to-end encrypted messaging.

Some other cases to consider:

For end-to-end encrypted messaging or are we doing 1 to 1 messaging only or group messaging and what size groups are we thinking here?

Are we expecting both parties to be online (synchronous communication) or are we planning for some parties to be offline (async communication)?

Ok, now just taking these two uses cases let’s start to build a threat model for this.

Some things to consider:

Is dApp to wallet communication bi-directional (any party can encrypt a message from one to another) or uni-directional (e.g. only one party can encrypt a message for another)? Follow up discussion for this:

1. How do we handle key discovery for these parties whether bi-directional or uni-directional?
2. How does key rotation occur? With signing crypto operations limits of keys are much larger if there are any to the point they can largely be ignored. With ECIES though we’re limited based on the cipher chosen.
3. How are nonces being coordinated to prevent nonce reuse attacks if AES-CTR or AES-GCM is used?
4. How are we transporting these ciphertexts and what sort of adversarial actors are we looking to avoid here?
5. Are we attempting to achieve perfect forward secrecy, weak perfect forward secrecy, or post compromise security?
6. What integrity guarantees are we looking to achieve?
7. What’s the average size of a message we’re expecting? 100KB/10MB/1GB

Are we wanting to store these messages as well?

1. If so are we planning to re-encrypt the message once received or are we going to store it as received?
2. Are we planning to publish them to the chain?
3. Doesn’t that introduce gas fees?
4. What if a user doesn’t pick the message up by the time the block gets pruned?
5. What if a key is broken or an implementation vulnerability is discovered later so that the ciphertext is able to be decrypted later?

What’s our adversarial privacy threat model look like since we want to provide confidentiality guarantees?

1. How are we linking the controller of a key to the subject of the ethereum account (do we even care who the subject is?) to know that the identity is trusted and someone we want to share information with?
2. What time frame are we trying to keep the plaintext message confidential?

These are just some of the questions we should be aligning on first before we start working on a solution here because each of these is going to lead to a different type of solution. Furthermore the more use cases we try to address at once the more likely we’re going to end up with a far more complex solution.

For example, take a look at [Message Layer Security (MLS)](https://messaginglayersecurity.rocks/) to see how complex group messaging can become.

---

**kdenhartog** (2022-09-20):

Even with [DIDComm V2](https://github.com/decentralized-identity/didcomm-messaging) we ended up with a lot of optionality that’s pretty hard to parse through and that decided to exclude group messaging beyond the scope of a single DID.

Additionally, given [walletconnect](https://www.businesswire.com/news/home/20220720005034/en/WalletConnect-Unveils-the-Future-of-Web3-Chat-With-Wallet-to-Wallet-Messaging-Preview) is looking to address the E2E messaging case, would it make sense for us to remain focused on just dApp to wallet communication?

---

**firnprotocol** (2022-09-20):

thank you for the questions. i want to please ask that we limit the scope of this discussion to this EIP, which specifies a way to do simple encryption and decryption. while most of your questions are legitimate, they are concerns for the builders of applications, and lie beyond the scope of this EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> How do we handle key discovery for these parties whether bi-directional or uni-directional?

though it’s out of scope, one way would be to use ENS (by adding a “public key” field), or something like it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> How does key rotation occur? With signing crypto operations limits of keys are much larger if there are any to the point they can largely be ignored. With ECIES though we’re limited based on the cipher chosen.

the message length limitation is only *per message*, and has nothing to do with encrypting many different messages under the same key. moreover, CBC mode [appears to have no length limit](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf). if you want to adopt a key rotation strategy, that’s up to you—same as in the case of signing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> How are nonces being coordinated to prevent nonce reuse attacks if AES-CTR or AES-GCM is used?

note that we propose CBC mode. the determination of IV is fully specified by [the spec](https://www.secg.org/sec1-v2.pdf); as for the generation of random ephemeral keys, this is handled by the spec and by the implementation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> How are we transporting these ciphertexts and what sort of adversarial actors are we looking to avoid here?

transport of ciphertexts is out of scope (though could optionally be done on-chain; see my comments above). the adversarial model is the standard one: indistinguishable multiple encryptions under chosen ciphertext attack. ECIES satisfies this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Are we attempting to achieve perfect forward secrecy, weak perfect forward secrecy, or post compromise security?

these could be optionally achieved by building on top of this EIP, but they’re out of scope—this EIP only provides simple encryption.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> What integrity guarantees are we looking to achieve?

the same ones ECIES guarantees: CCA-security.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> What’s the average size of a message we’re expecting? 100KB/10MB/1GB

up to the user.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> If so are we planning to re-encrypt the message once received or are we going to store it as received?

up to the client to do whatever it wants with its messages.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Are we planning to publish them to the chain?

up to the users.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Doesn’t that introduce gas fees?

if you choose to publish your messages on chain, then yes; otherwise, no.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> What if a user doesn’t pick the message up by the time the block gets pruned?

i have to say that I don’t find to be a legitimate question. Ethereum state doesn’t get “pruned”. perhaps if you *only* post it to calldata, but not anywhere in contract storage, then this could be an issue; if some user were to *choose* to operate in that way, then that user would need access to a full (archive) node.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> How are we linking the controller of a key to the subject of the ethereum account (do we even care who the subject is?) to know that the identity is trusted and someone we want to share information with?

it’s up to the consumer of this API to do this however it wants. one way would be to publish your public encryption key to your own ENS, or elsewhere on-chain that links the public key to your known Ethereum address.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Additionally, given walletconnect is looking to address the E2E messaging case, would it make sense for us to remain focused on just dApp to wallet communication?

I don’t see a rationale for narrowing the scope, since that project appears tied to a specific product, and not Ethereum-wide.

---

**friedtrout** (2022-09-20):

[@kdenhartog](/u/kdenhartog) Thanks for your questions.

I think it’s worth reiterating the actual point of this EIP: We want to create a simple generic way of leveraging Ethereum keys to securely encrypt and decrypt generic bytes. Importantly, this EIP avoids being prescriptive of *how* this functionality can be used, e.g. off-chain or on-chain. The key is that the capability of encryption/decryption is a natural fit for Ethereum.

The core components of this EIP are the encryption spec used and how the encryption/decryption keys are derived. We should consider which questions are relevant to the EIP itself, versus design decisions for products or tooling that could leverage this EIP.


*(110 more replies not shown)*
