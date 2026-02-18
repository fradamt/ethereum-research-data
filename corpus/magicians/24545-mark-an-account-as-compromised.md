---
source: magicians
topic_id: 24545
title: Mark an account as compromised
author: nickjuntilla
date: "2025-06-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/mark-an-account-as-compromised/24545
views: 210
likes: 9
posts_count: 12
---

# Mark an account as compromised

Here is a general concept for an EIP. It could also be an ERC, but that would require more work on the application side. The basic idea is that one could mark their own account as compromised so that tools would know not to trust this account in the future. There could be other features, but the game theory is that no one would mark their own account as compromised if they want to maintain their reputation. Therefore, accounts would only ever be marked as compromised if they were compromised or if someone were self sabotaging themselves in which case they should also not be trusted. If someone does not want you to trust them you should not trust them. Therefore you can reliably assume that if an account has ever been marked as compromised that you should not trust it.

Right now if your private key is leaked you can transfer all your funds out of your account, but your account can still be used to log into and sign message, basically until the end of time. There is no way to let the world know that at some point in the past this account was compromised.

Here is how I think it could work:

- A special transaction that ads a flag to an account that it has been compromised.
- Funds could still be transferred, but future tools can deny service or mark this account as unsafe on their end.
- If you wanted to go further accounts could have a backup account that would be the only account that could receive funds, but that seems heavy handed.

NOTE: It would NOT be a good idea to have a “forward” address of the new trusted account as a hacker could have compromised that one as well. One must establish a new reputation on a new account independently.

This could either be accomplished with some kind of account flag or maybe a deployed asset like a soulbound token. A soulbound token would be easy to deploy, but then anyone who cared would have to make a query to an NFT indexer every time they cared to know. That seems like tech debt.  I’d be curious if anyone has any other ideas how this could be implemented.

Thoughts?

## Replies

**katzman** (2025-06-13):

This is an interesting concept! I think that the specification needs to incorporate how this can be accomplished without a transaction executed by the compromised account.

It’s reasonable to assume that a compromised account will auto-sweep Ether that is deposited for paying for the gas associated with signaling a compromise.

As such, this specification should instead describe:

1. how to generate a Compromised Account signature offchain
2. how a separate account can post this signature payload to some registry/storage contract
3. what the topology and eventing must be in the storage contract

---

**nickjuntilla** (2025-06-14):

These are really good points. Yes the insta-sweep on funds preventing any future transactions happens quite frequently so I agree that is highly likely. In light of this an offchain transaction that can be carried by another account makes perfect sense. Also I like the idea of a central registry that can be quickly queried without a need for indexing. This could prevent the need to make any deep alterations.

I wonder though if there has been any success in central registries in the past? Does Ethereum have any example of a central registry that did not fragment into many competing versions? The ENS system is the only I can think of. How do you get the community to acknowledge one registry? Do you just start a registry and then it becomes defacto by virtue of being first? Is this still too much overhead.

Another idea is maybe a standard way of baking it into any smart contract. This would require an account to notify many contracts they have been compromised. So in this model every smart contract implements the it’s own registry. The advantage is you don’t have to worry about fragmented registries. It may take less gas than calling a central registry. I’m not sure about that. The disadvantage of course would be that a transaction would have to be submit to each contract you care about. That might be a non-starter.

I like the central registry idea. How does something like that become official?

---

**MASDXI** (2025-06-17):

I think it can be site in first place, like [4bytesdict](https://www.4byte.directory), or [GitHub - celo-org/compliance](https://github.com/celo-org/compliance)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nickjuntilla/48/8321_2.png) nickjuntilla:

> Right now if your private key is leaked you can transfer all your funds out of your account, but your account can still be used to log into and sign message, basically until the end of time. There is no way to let the world know that at some point in the past this account was compromised.

This applies to EOAs (Externally Owned Accounts). But what about smart contracts? Especially those that control or manage other contracts?

It should work on a consortium blockchain that you can control, label accounts, and rapidly update the registry to be up to date without worrying about the gas.

---

**nickjuntilla** (2025-06-17):

Yes that’s an interesting concept, being able to mark a smart contract as well. There would have to be a deterministic way to decide who has the authority to deem a smart contract as compromised. The only way I can think of that is deterministic is that the deployer would have to sign a transaction that the contract has been compromised. The same game theory applies that no one would purposely sabotage their own contract unless it were true. Yes, contracts can have other owners according to the rules of the contract, but that not a universal standard. I think it would have to be the deployer. The problem is I don’t think you can get that data from another smart contract. Someone correct me if I’m wrong.

I think being able to get the compromise data from other smart contracts would be really useful. If we go the route that all the data is in some offchain registry what guarantees the registry will always exist? Is this a privately owned company? Are there many competing companies? If it’s a just a github repo who manages it? Who has the permissions? I’m not a big fan of that idea. I think this needs to be permissionless, evaluated by cryptography and as permanent as possible.

As for being cross chain there are many instances of the same group of smart contracts being deployed on many chains. There can be a cannon address on each chain (preferably the same one). Then the data is alive as long as the chain is alive. Yes this does present the problem of not marking an address as ‘dead’ on every chain, but since we have discussed above being able to submit a transaction on someone else’s behalf maybe services can be created that help mark them all at once.

So the one question remains, how do you mark a smart contract as compromised? Maybe this is already baked into Ethereum. Maybe it should be up to developers to use the **`selfdestruct`** function that already exists? This seems like the standard way to do this now. If your function is gated for the owner it accomplished essentially the same thing.

---

**MASDXI** (2025-06-17):

- In theory, any contract can be a program, and it’s possible for one program to interact with multiple others. If one contract is compromised, it may propagate incorrect or malicious data to other contracts. This raises the question: if a contract is interacting with another that may be compromised, how can it protect itself?

`modifier isCompromised(address)`

- IPFS can be used to cache and serve the registry; however, it may suffer from outdated information. Further exploration is needed to determine who is responsible for maintaining and updating this data.
- Cross-chain interoperability remains challenging, especially when bridges or providers do not adhere to established standards. It’s also inaccurate to assume all contracts are equivalent across chains. In some cases, even if the same deployer, code, and nonce are used, the resulting state may differ once any associated contract or address is compromised. In such scenarios, it is standard practice for the protocol or owner to transfer all ownership to a new, uncompromised address.
- Not sure, should explore more compare pros and cons of each possible solution

---

**ryley-o** (2025-06-18):

I think allowing any account to mark any other as compromised via standard signed message verified on-chain makes sense - this would eliminate the risk of sending funds to a compromised wallet.

In order to become the standard, it has to beat out centralized solutions (like etherscan’s account labeling system). I think it would be potentially difficult to win because this system costs gas if it involves sending transactions. Sponsored L2 or even L3 solutions could be interesting, but still may not prove practical considering the incentive here.

---

**nickjuntilla** (2025-06-19):

Yes, IPFS could potentially be used for this, but as you said, who pays the bill to keep the data alive ultimately.

One option could be having the cannon registry exist on one chain, like Arbitrum or perhaps the ENS purpose made layer 2. This could provide a cheap credibly neutral space to host the data. It is related in that it’s metadata about addresses. [@ryley-o](/u/ryley-o) This would also allow for cheap sponsored transactions.

I’m not too worried about beating out private solutions like etherscan because until there is a community driven permissionless option I think there is a niche that needs to be filled. Also if we go the route of self identified signed testimony we have a much more deterministic and exact solution than a loose subjective tagging system.

The main problem I see with having a cannon chain or IPFS is that this data would be inaccessible to smart contracts. I don’t think this is a deal breaker, but it would be a great nice-to-have.

Ok so far I think we have some consensus on:

- A system that included self implicated, self signed transactions that can be submitted by any party.
- A desire to include smart contracts in this system
- Recognition contracts may be different on different chains

What we don’t know:

- Where the data will be kept
- How a contract is marked as compromised. Is it per contract? Can we use modifier isCompromised(address)

Right now I’m not focusing on the actual format of the compromise transaction since it should be pretty straightforward once we have these big issues out of the way.

If we have a central registry on a designated layer 2 we would have to include the blockchain identifier as well so that could solve the difference in bytecode between different addresses on different chains.

---

**abcoathup** (2025-06-20):

You could do as an ERC, using a soulbound NFT that anyone can mint but needs a signature from the compromised account.

---

**Trying2Cook** (2025-09-14):

Could this be used as a mechanism to stop a Validator from exiting or other additional security on a Validator?  My withdrawal account was compromised.  Then with the introduction of EIP-7002, the attacker then using the compromised account sent an exit message.  Now my validator will be exiting into a compromised wallet.  I’m just watching the clock count down.

---

**nickjuntilla** (2025-09-23):

If you knew your account was compromised ahead of time it would help, but it would have to be used in combination with some other mechanism to send your funds to a pre-configured backup account. That backup account would also need to have some kind of change delay so an attacker couldn’t just change it any time.

So yes I think this is one step in the right direction for addressing these kinds of problems. Unfortunately right now there is nothing.

Since I have seen some interest in this I believe I will write up a draft for people to review.

---

**Trying2Cook** (2025-09-26):

Something to consider from a marking as compromised, but also allowing an option to indicate for funds to be forwarded. The forwarding account can’t be a new account that the wallet had only interacted with recently.  I’m thinking that if you had a second wallet that you sent funds to and from, or even a trusted friend that had several transactions from a long waiting period, then you could trigger your account as compromised and indicate one of those addresses as the receiving receipt for future fund deposits.

