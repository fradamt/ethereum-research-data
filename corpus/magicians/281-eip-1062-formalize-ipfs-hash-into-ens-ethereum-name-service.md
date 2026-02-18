---
source: magicians
topic_id: 281
title: "EIP-1062: Formalize IPFS hash into ENS(Ethereum Name Service) resolver"
author: PhyrexTsai
date: "2018-05-05"
category: EIPs
tags: [ens, ipfs]
url: https://ethereum-magicians.org/t/eip-1062-formalize-ipfs-hash-into-ens-ethereum-name-service-resolver/281
views: 6324
likes: 27
posts_count: 32
---

# EIP-1062: Formalize IPFS hash into ENS(Ethereum Name Service) resolver

I’ve written an EIP proposing [Formalize IPFS hash into ENS(Ethereum Name Service) resolver](https://github.com/ethereum/EIPs/pull/1062). Any discuss and feedback are appreciated!

## Replies

**Arachnid** (2018-05-07):

Thanks for putting this together. It’s been something I’ve been meaning to do for a long time, and I think it’s sorely needed!

---

**jbaylina** (2018-05-22):

For the http://dappnode.io project, I have been solving this by adding a `text` record with key `dnslink` and a NURI for example: `/ipfs/QmXpSwxdmgWaYrgMUzuDWCnjsZo5RxphE3oW7VhTMSCoKK`

This has the advantages:

- We don’t have to create a new resolver.
- It is compatible and predictable with the current ipfs implementation.
- We don’t have to deal with base58 onchain.
- We can specify other protocols like ipns, swarm or any protocol.  ( I know that this is not strictly necessary, but it is very convenient for real applications, if no, you will end up testing many protocols… )

---

**Arachnid** (2018-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jbaylina/48/261_2.png) jbaylina:

> We don’t have to deal with base58 onchain.

To be clear, this isn’t necessary here, either. Multihashes are stored in binary form, and encoded and decoded offchain.

---

**jbaylina** (2018-05-23):

Ah, ok, I see.

I want to note, that saving the multihash in binary (compared to string) does not improve the storage cost.  In most of the cases this is going to take two 256bit words of storage + the lenght.

In the other hand, if you use the binary format you will need specialised tools to manage this field. If it’s a string, you can use regular tools to check, set, cut and paste, etc…

---

**Arachnid** (2018-05-23):

Most multihash tools I’m aware of support binary representation natively.

---

**jbaylina** (2018-05-23):

Yes, sure.

I’m talking more about generic tools like block explorers, generic smart contract interfaces, blockchain data analysers, etc.

---

**jbaylina** (2018-08-20):

Guys,  right now we have 3 different ways to do this (as far as I know):

1.- Metamask:  Put in the content field the SHA256 value of the content (32bytes)

2.- DAappNode:  Use text field in the resolver with the key `dnslink` and a string like “/ipfs/QmXpSwxdmgWaYrgMUzuDWCnjsZo5RxphE3oW7VhTMSCoKK”

3.- EIP1062:  Use a new field called “multihash” that puts the full multihash in binary (>32bytes).

It would be good to chose one for the standard.

My vote is for 2 (I’m biased)  but this are the arguments:

1.- It is compatible in how this is solved in a regular DNS system

2.- It adds options for different providers:  /ipfs/xxx   /ipns/xxxxx  /swarm/xxxxx   (and it’s open to other providers).

3.- You can use the actual ENS resolvers.

4.- Defining a new `multihash` function for the resolver and storing it in binary it will not save any blockchain storage, as it will take always two 256bit-words.

5.- It is readable from a generic blockchain explorer.  (You can easily do a cut and paste).

6.- You don’t need any special tool to generate the link and to convert.

7.- In case of an automatic import of a dns zone to ENS, the system will continue work.

So because of this, I would like to strongly push for this option.

---

**danfinlay** (2018-08-22):

Since [@PhyrexTsai](/u/phyrextsai) implemented MetaMask’s support, I thought it would surely be compatible with his EIP, 1062, is it not?

I’m happy with revising it if needed, we should try to stay on the same page about this.

---

**eduadiez** (2018-08-25):

If I’m not wrong the [@PhyrexTsai](/u/phyrextsai) MetaMask support implementation uses the public resolver from: https://etherscan.io/address/0x1da022710df5002339274aadee8d58218e9d6ab5. This public resolver doesn’t implement `setMultihash` and `multihash` so I don’t think it’s compatible with this EIP.

Note: According to manager.ens the default public resolver should be 0x5ffc014343cd971b7eb70732021e26c35b744cc4. I don’t know why 0x1da022710df5002339274aadee8d58218e9d6ab5 is tagged as ENS-PublicResolver on Etherscan.

---

**chris-remus** (2018-08-28):

FWIW, I won the ipfshash.eth auction. Let me know if the name could be useful here.

---

**rachelhamlin** (2018-08-29):

Hey [@jbaylina](/u/jbaylina) [@danfinlay](/u/danfinlay), Rachel from Status here. We touched base briefly with [@alexvandesande](/u/alexvandesande) and Bobby (MetaMask) about this.

We’re starting on ENS support for our browser now and were planning to follow the EIP directly with `multihash` and `setMultihash`.

---

**danfinlay** (2018-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eduadiez/48/698_2.png) eduadiez:

> If I’m not wrong the @PhyrexTsai MetaMask support implementation uses the public resolver from: https://etherscan.io/address/0x1da022710df5002339274aadee8d58218e9d6ab5. This public resolver doesn’t implement setMultihash and multihash so I don’t think it’s compatible with this EIP.

If that’s the case, MetaMask will probably update its support to resemble the EIP more closely, especially now that other clients are following that.

---

**portal-chris** (2018-08-31):

[@danfinlay](/u/danfinlay) [@rachelhamlin](/u/rachelhamlin)

This version of public resolver contract (0x1da022710dF5002339274AaDEe8D58218e9D6AB5) which has been widely used right now, does not support the multihash method, so we decided to use the SHA256 hash in content method to set mappings of IPFS/swarm. For the EIP-1062, we use the supportInterface method to determine whether or not the public resolver support multihash.

We are currently developing a new feature that’ll detect whether the ENS is using the old/new resolver; and it’s compatible with SHA256 content and multiash. After testing, we’ll make a pull request to MetaMask.

chris@portal.network

phyrex@portal.network

(kaizen.portal.network)

---

**danfinlay** (2018-08-31):

Great, sounds good, thank you!

---

**jbaylina** (2018-09-03):

In my opinion, the standard MUST define a way to specify the protocol:  “ipfs”, “swarm”, “utorrent”, “storej”, “filecoin” or what ever.

If not, the browser (or any user using the entry) will have to query all possible providers in order to resolve the hash.  This is not efficient and can generate a lot of confusion in case that new protocols are defined.

---

**rachelhamlin** (2018-09-08):

[@jbaylina](/u/jbaylina) agreed.

We’ve discussed this a bit further and now I understand that `multihash` doesn’t actually specify the protocol. Add to that the complication of working with a library for binary storage… it seems like your option #2 above is more straightforward and comprehensive.

[@danfinlay](/u/danfinlay) [@portal-chris](/u/portal-chris) being agnostic about the storage we support is probably our number one priority. What are your thoughts?

---

**danfinlay** (2018-09-09):

I’m all for staying transport agnostic, but we should start with transports we’re ready to support. IPFS first makes a lot of sense because we already have gateways for it. Swarm isn’t quite as web friendly yet, so I would leave it for the future.

> In my opinion, the standard MUST define a way to specify the protocol: “ipfs”, “swarm”, “utorrent”, “storej”, “filecoin” or what ever.
>
>
> If not, the browser (or any user using the entry) will have to query all possible providers in order to resolve the hash. This is not efficient and can generate a lot of confusion in case that new protocols are defined.

Or we follow the path of MIME and support fallback protocols within an ENS resolver type. It could say “I prefer Swarm, but here’s an IPFS hash, and here’s a URL if you don’t have either of those.”

---

**portal-chris** (2018-09-10):

[@jbaylina](/u/jbaylina) [@rachelhamlin](/u/rachelhamlin)

The multihash could have stored with a map structure which the resolver can identify with a specific protocol (IPFS, swarm, storj, and etc.).

We will update EIP-1062 and add the specify protocol.

*Rationale*

`function setMultihash(bytes32 node, string protocol, bytes hash) public only_owner(node);`

`function multihash(string protocol, bytes32 node) public view returns (bytes);`

Our team has commented the EIP-1062 for the above issue on May 18, and I think we can upgrade the EIP1062 and public resolver contract.

Link:

https://github.com/ethereum/EIPs/pull/1062#issuecomment-390080648

---

**rachelhamlin** (2018-09-11):

[@portal-chris](/u/portal-chris) nice, simple enough. That would suit us fine.

---

**Arachnid** (2018-09-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/portal-chris/48/1941_2.png) portal-chris:

> We are currently developing a new feature that’ll detect whether the ENS is using the old/new resolver; and it’s compatible with SHA256 content and multiash. After testing, we’ll make a pull request to MetaMask.

Note that you can deploy your own resolver any time you like, and use that. ENS doesn’t have a system-wide resolver; the public one is only provided for convenience!

If a feature you want isn’t yet deployed, you can deploy your own resolver and use that instead.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jbaylina/48/261_2.png) jbaylina:

> In my opinion, the standard MUST define a way to specify the protocol: “ipfs”, “swarm”, “utorrent”, “storej”, “filecoin” or what ever.
>
>
> If not, the browser (or any user using the entry) will have to query all possible providers in order to resolve the hash. This is not efficient and can generate a lot of confusion in case that new protocols are defined.

Think of it like DNS; it doesn’t specify the protocol for an A record, only the IP address. The protocol is either contextual (eg, default to HTTP) or supplied by the user in the URI.


*(11 more replies not shown)*
