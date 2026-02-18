---
source: ethresearch
topic_id: 4117
title: "Ethereum 2.0 Data Model: Actors and Assets"
author: fubuloubu
date: "2018-11-04"
category: EVM
tags: []
url: https://ethresear.ch/t/ethereum-2-0-data-model-actors-and-assets/4117
views: 10142
likes: 30
posts_count: 30
---

# Ethereum 2.0 Data Model: Actors and Assets

As a summary from this week, I think I have realized that the execution and data structure components of the ETH 2.0 roadmap are still very much in flux, especially the data structures.

One idea I have been thinking about this week is a few concepts relating primarily to the “actor model” that Erlang and Elixer uses (Read [this](https://www.javaworld.com/article/2077999/java-concurrency/understanding-actor-concurrency--part-1--actors-in-erlang.html) for more info), thanks to some conversations with [@expede](/u/expede). Another undercurrent is the idea of treating assets (tokens, Ether, other forms of controllable state with value) as first class citizens in this “asset control network” we’re building called Ethereum. Agoric is also doing some neat things along this concept (see talk [here](https://www.youtube.com/watch?v=vvdZKzct2-U)). [@johba](/u/johba)’s Plasma Leap (see thread [here](https://ethresear.ch/t/plasma-leap-a-state-enabled-computing-model-for-plasma/3539)) also has some very similar concepts of a token that controls it’s own state.

---

More narrowly, the idea I have been playing with would be functionality that allows certain “actors” (like token contracts) to issue pieces of state to other actors (regular users). We would store these pieces of state in a new key-value data structure called “asset storage” (similar to how Ether balances are kept). Each asset could contain specific logic for transfer to other actors, or could link back to a function in that contract for more complex coordination logic (conditional transfers). They could issue logs, etc.

In this data structure, the issuing contract would be the key, so access control is built into the data structure as we could enforce only the issuing contract is allowed to modify given state or make external calls, etc. For upgradability, there might be a way for the issuer to change the key by calling a specific operation. Transfer of simple, uncontrolled tokens could even happen without ever requiring interaction with the issuer contract. Minting comes from the issuer, and burning could be a feature of the token internally. I am sure there are other useful features for an asset to have, but I think this can be reduced quite nicely to a few core features, and augmented with allowing the asset to store it’s own rules.

A nice side effect of all of this is that tokens (and other relevant state e.g. access rights to the issuing contract) no longer fully depend on a central contract for their control, which means the central issuer contract has much less authority over these valuable pieces of state in case of a hack.

This also has another nice side effect relating to storage rent: since much less state is being stored in central contracts, the concept of who pays for a particular contract to stay alive is reduced (we could define minimums to eliminate it). Each account is now in charge of managing their own assets, and in a rent scheme, this means ensuring the upkeep of their assets too. Rent could allow you to “drop” tokens you don’t care about.

---

This idea is definitely not fully baked, but I would say that now is the time for re-architecting the data model in order to make sure that the future state of Ethereum makes more sense to developers (I think the actor-asset model is very clear), and can be sustainable as well.

Thoughts?

## Replies

**antoineherzog** (2018-11-04):

Totally agree with you!

I actually talked about it with ATjohba ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) as well during devcon4.

Another side effect is signature curve upgradability where actor can upgrade their signature going from Secp256k1 to Ed2551.

Another good side effect are the possilbity to upgrade actor smart contract from one sig to multi-sig easily or provide easily social recovery options.

And also cherry on the top, we could add actor ID immutability which means that we can generate a first public/private key where the public address is the actor ID. When we want to create our actor smart contract, the public address could stay the same which give us a nice user experience (so we could upgrade the same generated address with the custom actor smart contract). So for a standard user, the Actor ID never changes from the first generation of public/private key which is a very good property. We don’t need to add an extra layer such a ENS to provide Actor ID immutability.

---

**fubuloubu** (2018-11-05):

Hmm, another interesting side effect might be that cross-shard communication gets a little easier as we reduce the reliance on central contracts to perform transfers, since they can now be p2p instead.

---

**johba** (2018-11-05):

You framed the topic nicely ![:clap:](https://ethresear.ch/images/emoji/facebook_messenger/clap.png?v=9)

It may be worth mentioning that the idea for transfer restrictions has come up in [Bitcoin Covenants](https://fc16.ifca.ai/bitcoin/papers/MES16.pdf) already.

I’m intrigued how the [Zexe paper](https://eprint.iacr.org/2018/962.pdf) has extended this and allows to model any asset with only a `birth` and `death` predicate.

My curiosity currently circles around off-chain breeding of crypto-kitties. Is there a way that my kitty is born on a side-chain and the main-net would be able to verify that it’s genetic transition was correct and all cool-off durations has been adhered to by the parents once it gets back to main-net ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=9)

---

**expede** (2018-11-06):

# Smart Contract as Actor

> One idea I have been thinking about this week is a few concepts relating primarily to the “actor model” […] I think the actor-asset model is very clear), and can be sustainable as well.

![:clap:](https://ethresear.ch/images/emoji/facebook_messenger/clap.png?v=12)![:clap:](https://ethresear.ch/images/emoji/facebook_messenger/clap.png?v=12)![:clap:](https://ethresear.ch/images/emoji/facebook_messenger/clap.png?v=12)

…and also…

> To be clear, at this point I [Vitalik] quite regret adopting the term “smart contracts”. I should have called them something more boring and technical, perhaps something like “persistent scripts”.

Yep, obviously [@fubuloubu](/u/fubuloubu) and I chatted a bit about this Prague, so I’m broadly in favour of this line of thought ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

The words that we use impact how we work with a system. I think that “actor” is a really nice match here, is an existing concept, and has no legalistic implications while emphasizing that these are separate chunks of autonomous code. Actors are best known as a way to model concurrency, but you can restrict your model to a single-threaded version. This ends up describing exactly what smart contracts are today, plus allow for extension for in-transaction concurrency (rather than the macro-level superposition that we currently use).

(Also, “actor” is much shorter to say and type than “smart contract” ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12))

# Reworking Storage/Control

> no longer fully depend on a central contract for their control […] reduce the reliance on central contracts to perform transfers, since they can now be p2p instead

I totally get that this is a sketch of an idea at this point, but to help clarify, do you have a concrete example of how this would be used?

AFAICT, the current data layout and one where the data “actually lives in your account” are isomorphic for most uses, though this reworked version does add some complexity to things like upgrades resetting or proliferating the number of pointers to other contracts (like the creating/controlling one).

To use tokens as an example: they’re simply a balance (a number), and invariants, access control, and so on are handled by the wrapping contract; you’ll need to check in with that contract in any case, since it may have effects beyond simply what the user is doing directly (ex. change `totalSupply`). There are workaround (such as a broadcast event stream), but there is a nontrivial increase in overall complexity (which is fine — it’s a question of cost/benefit).

## A Brief Case for Decoupling

While we’re tossing around ideas, I wonder if there may be another architecture to achieve these aims using decoupled storage and behaviour? OZ is already starting to approach this, but they’re treating it more as something to hide (in the data hiding OO tradition) rather than to embrace (in the actor model or networked styles). This can be done today with no hard forks (opt-in and backwards compatible)

```plaintext
Referenced Account
        ^
        |
        |
        V
    Data Store  another interesting side effect might be that cross-shard communication gets a little easier as we reduce the reliance on central contracts to perform transfers

For sure. This ended up getting raised briefly during a Devcon talk, as well. I’m guessing that it’s uncontroversial that we want this coordination/routing/etc to happen below the application layer.

---

**fubuloubu** (2018-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/expede/48/7027_2.png) expede:

> [T]o help clarify, do you have a concrete example of how this would be used?

Well, guess what I was doing on the plane?

---

Actor: a smart contract or private key, referenced by address

Issuer: an actor (typically a smart contract) that has the ability to define and issue state according to an immutable specification (non-contract actors can only issue a “basic” ether-like token)

Asset storage tree: merkle tree of key-value pairs, replacing the eth balance tree. The key corresponds to the issuing actor (in the case of ether, this is the 0x0 address). The value corresponds to an asset whose data type is defined by the issuing actor.

---

The asset’s type can be one of 3 options, with the following formats:

1. A uint256 (ether, ERC-20)
2. A list of bytes objects (ERC721, NFTs)
3. A mapping of bytes32 → uint256 (ERC-1400, PFTs)

The asset balances are publicly available, and can be queried using an opcode to return the data from the tree at the specific issuer address.

The issuer should provide an entry in the ABI for non-essential information about the asset (such as ticker symbol, etc). The issuer contract can define this for convenience as well.

The issuing actor defines the asset’s structure by calling an opcode that allows the issuing actor to define the asset’s type and initialize the supply characteristics. Nodes can use this to store tracking information. This information is as follows for each of these formats:

1. Total supply of 0 (represented by uint256)
2. Empty merkle tree root hash
3. Total supply of 0 (represented by uint256)
The issuer can only issue one asset.

---

Transferring an asset requires the issuer to send a message with the following data field:

SEND_OPCODE, issuer’s address, recipient’s address, assets to transfer (also matches asset structure). In order to be successful, this message’s asset structure must meet the conditions corresponding to it’s asset type:

1. Asset is a uint256 GT 0, but LEQ the balance in asset storage
2. Asset is a non-empty subset of entries in owner’s asset storage list
3. Asset is a list of key-value pairs, where the value is a uint256 GT 0, but LEQ the balance of the sub-asset referenced by the key.
If these conditions are not met, the transfer reverts execution.

Assets can have complex requirements for a transfer function if the issuer defines a transfer predicate. This predicate must match the signature `transfer(to: address, from: address, asset: asset_type)` and is called against the issuer’s address. The function can revert the transfer for whatever reason, as well as make internal state changes (if necessary) to it’s own storage (never the owner or receipient). If no matching function is present, the asset is assumed freely moveable (this takes care of selfdestructed contracts as well as ether) as the predicate cannot revert.

The account receiving the asset will then merge them according to the following rules:

1. Current balance adds received balance. Reverts if GEQ 2**256. Transferred balance is deducted from sender’s account.
2. Received entries are appended to the receiver’s list, and removed from the sender’s. Empty lists can be deleted.
3. Balance of sub-assets are merged according to rule 1. Empty keys can be deleted.
If the structure does not exist in the receiver’s account for the issuer’s key, a new entry will be created.

The receiver (if a contract) can define a receive function that matches the signature `recieve(issuer: address, from: address, asset: asset_type)`. It can revert or do whatever it would like with this information as it sees fit. If no function is defined, the transfer is successful

Transaction receipts should contain a summary of all transfer messages that occurred in a given transaction.

---

An asset can be destroyed by sending a transfer message to the 0x0 account. This triggers the explicit removal of the asset from data storage as the 0x0 account does not store any tokens except ether (as it did issue all ether). Nodes will remove this entry from state.

An asset can only be minted by the issuer with the same opcode used to encode the structure in the orignal issuance, and can be passed by transfer message to another account, if desired. The rules for minting are as follows:

1. Number minted must not overflow total supply
2. ID minted cannot be in list of all assets (merkle tree proof)
3. Sum of the increases of all sub-assets cannot overflow the total supply.
Updates are captured if the minting does not violate these invariants.

---

Positive attributes:

- Stateful message passing of assets (Ether receive logic! Token receive logic!)
- Decentralization of asset storage (security and storage rent benefits!)
- Decentralization of message passing (sharding benefits!)
- Reduced complexity of token issuance contracts
- Assets as a first class citizen (not just eth!)
- May enable token gas payments?

Negative attributes:

- Increased complexity at protocol layer
- More inflexible API (did I miss one?)
- Requires changes to ether balances
- 4 opcodes added (register, issue, transfer, query)
- NFT MT is probably a DoS vector. There is probably a better way to prove nonmembership in the set of already minted UIDs that the issuer may not own.

Other ideas:

- Add a bool asset type, used primarily for ownership and access rights. Could also be an enumeratation.

---

**antoineherzog** (2018-11-07):

I believe this conversation extremely interesting. The actor-asset is for sure the base of any next generation blockchain.

Regarding the asset storage, i am not sure this is the most urgent issue to fix.

ERC20 are working pretty well on the way to save states of an ERC20. However, the missing part of the ERC20 is how it has been designed. The basic Transfer function of a ERC20 check directly the address signature where ideally we would need to delegate to the actor authorization. This way, the ERC20 Token will not need to check if the signature is correct but the actor will check if the signature is correct. This way, the transfer of asset goes from one actor to another actor. Crypto address are not first class citizen, Actors are.

In the current ERC20 Token, i cannot easily change my public signature without moving my assets to a new address which is huge pain for mass-adoption. Traditional end-user not familiar to crypto already have the opportunity to increase the security of their Gmail account without the need to “re-create an account”. Ideally being able to to deploy a smart contract to the my current public address would be very useful  (kind of a new opcode CREATE3) because it gives a seamless experience for end-user to upgrade their actor account security. At the beginning my public address is my actor ID then later on, it is not necessarily anymore the case because i always keep my Actor ID however I can still switch to another type of Curve or multi-sig to transfer assets.

I consider there is 2 main types of condition to transfer an asset:

- internal condition delegated and checked by the actor, does my signature (1 or several) matches the condition to move my asset
- external condition from the issuer. does this asset can be moved from Actor A to Actor B (ex: checked how TPL works https://tplprotocol.org/)

In my opinion, before improving the asset storage, the actor model needs to be well defined.

To get mass adoption from the end-user, we need to make sure end-user can create an actor account easily, defining easily how many and which public key/private key will be used to allow transfer and potentially optiinally how to recover their private key from a social recovery schema (https://www.youtube.com/watch?v=FAC9uqHJ4H0)

I hope my comment helps. I suggest we co-write an article regarding this topic?

I believe this topic is a major to get mass adoption solved.

Kind regards,

Antoine

---

**AlexeyAkhunov** (2018-11-30):

Thank you for the ideas!

Now I finally got to this thread and see that it has at its core the same idea as I had for Linear Cross-Contract Storage (LCCS) for Ethereum 1x  State Rent proposal. I identified it as not a “nice to have”, but as a necessary primitive for most existing contracts to transition into the State rent regime. I see that LCCS makes Actor-Asset implementation almost trivial. One difference that I see is this: In LCCS proposal, I specified that the cells are only readable by two entities: by owner, and by writer (actor in your terminology). The reasoning behind this is to allow contracts (mostly actors) to collect CALLFEEs for calling them, so that they can pay rent for their code and account info. If it is allowed for anybody to read the cells, then it would be possible to circumvent this and deprive the contract from this revenue opportunity, and therefore, from the ability to pay rent for its code. I will expand on this in the next version of the document.

---

**antoineherzog** (2018-12-01):

hi [@AlexeyAkhunov](/u/alexeyakhunov)

I am glad you are interested in the actor/asset model as I believe it will be the core of the Internet of Values.

Actually, we are finalizing an article about it but we have still one unanswered remaining question about the current ethereum protocol:

**Do you know why it is not possible to deploy a smart-contract to an empty specific ethereum address if the user can prove that he owns the private key of this specific address?**

If we could allow to deploy a smart contract to an empty specific ethereum address if the user can prove that he owns the private key of this specific address, then actor creation could be free, and should be possible to do in an offline environment (with a simple public/private key generation). We should follow the same motivation than the EIP https://github.com/ethereum/EIPs/issues/1056

I hope you can enlight us about this ethereum protocol question ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Kind regards

Antoine

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> If we could allow to deploy a smart contract to an empty specific ethereum address if the user can prove that he owns the private key of this specific address, then actor creation could be free

Sorry, I must be missing the chain of reasoning here - why is this possible, and how is this useful?

---

**antoineherzog** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Sorry, I must be missing the chain of reasoning here - why is this possible, and how is this useful?

let me start first with what we want to achieve for the end-user to get mass-adoption:

1. being able to create for free an immutable account
2. being able to receive for free assets linked to an account
3. being able to send assets linked to an account and pay potentially some fees during the transfer
4. being able optionnaly to recover ownership of an account even if the user lost its original private key by trusting some friends or some KYCs providers or both (mimic the current forget password feature available on 99.99% of websites)
5. being able to manage the security of an account and for example switch from 1 sig to multi-sig to authorize transfer of your assets.

In the current environnement, you can achieve 1,2,3 with Bitcoin or Ethereum easily. You generate a public/private key for free and you can start receiving or sending some assets.

If you want to achieve 4,5, you will need to delegate the security approval of an asset transfer to a smart actor contract.

In the current environnement, address of smart contract are necessarily different of the first original public address a user create freely offline. Which means that at some point, for a user to get additionnal property such as 4) and 5), he will need to move its assets into its new address and also tell all his friends that his address to receive assets has changed. Of course it is doable, but if you really care and think deeply about mass-adoption, a normal user will never do that, it is way to much complicated. You want to provide 1,2,3,4,5 without the need to change addresses for a user.

Another solution is to use ENS to achieve address redirection but i disagree with this approach because it adds another layer of complexity and cost not necessary to achieve account immutability.

From what i understand, the current limitation of the ethereum protocol could be easily change: we could deploy a smart-contract to an empty specific ethereum address if the user can prove that he owns the private key of this specific address.

I believe this is the right way to improve our goal to have an account immutability which will get the property 1,2,3,4,5

I hope it helps

Kind regards,

Antoine

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> From what i understand, the current limitation of the ethereum protocol could be easily change: we could deploy a smart-contract to an empty specific ethereum address if the user can prove that he owns the private key of this specific address.

In Constantinople, there’s CREATE2 opcode, which allows to deploy contract to a deterministic address (which can be linked to user’s address). Then, the contract itself would verify if its address is derived from user’s address, and authorise an action. Is this not enough?

---

**antoineherzog** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Is this not enough?

Unfortunately, I don’t think so.

Lets take a quick user story example. Antoine create a set of public/private key. He got a new address for free :  0xAAA123456. Yay!

He is very happy because now he can receive tokens! He give this address to all his friends and he starts to receives 12 ETH, 12 REP, he is getting rich now!

Now, he is worry about the security of its account and would like to enable a private key recovery mode. He would like that if he lost his original private key, he could get a new one for its account if his friend Marta, Aleksey and Bob submit a Shamir Secret for him.

Of course, Antoine doesnt’ want to move assets or change its beautifull 0xAAA123456.

This user-story is not possible in the current ethereum protocol because Antoine cannot deploy a smart user contract on 0xAAA123456.

i hope it helps!

---

**vbuterin** (2018-12-02):

If 0xAAA123456 is a public key-derived address, then Marta, Aleksey and Bob can submit the shamir secrets to help Antoine recover the private key, and he will be able to keep using his REP as normal.

I don’t see the issue.

---

**antoineherzog** (2018-12-02):

So you mean i can receive and send ETH on 0xAAA123456 which is at the beginning an empty account address and then later deploying a smart contract on 0xAAA123456 ? If we can do that, that’s all we need.

---

**AlexeyAkhunov** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> So you mean i can receive and send ETH on 0xAAA123456 which is at the beginning an empty account address and then later deploying a smart contract on 0xAAA123456 ? If we can do that, that’s all we need

Yes, it is currently possible - when you deploy a contract at an address which contains a non-zero balance, this balance will be added to the new contract’s endowment

---

**kladkogex** (2018-12-17):

What we ended up doing at Skale for all of our Solidity contracts is splitting  each contract into state-full data contract and state-less behavior contract as people suggested here.

A data contract should only have state plus getters and setters.  A behavior contract should be stateless … Ideally one would have it as a keyword in Solidity …

---

**jtremback** (2018-12-18):

The rest of this thread is interesting, and I support the terminology of “actor” instead of “contract”, but this proposal looks terribly complicated and rigid. Ethereum found success because it provided a totally open environment for people to program their own abstractions. There is little overhead of trying to fit your application into some preconceived notion of what someone thought you should build. This is what made Ethereum appeal to so many more people than older systems like colored coins and Master Protocol etc.

This proposal seems to be a big step backwards. Now I’ve got to understand your categories, and figure out how to make my app fit into them. I’ve got to learn a whole framework instead of writing some turing complete code to implement whatever logic and storage my app needs. If I want to have logic in a transfer, now I’ve got to do some ceremony with a predicate.

My guess is that if this proposal went forward, people would keep coming in with things that are difficult to implement using it. Exceptions and extensions would keep being added to it to support different use cases. This proposal reads like something that can only grow in complexity. To become fully general it would have to contain every possible use case within it, becoming infinitely complex.

To test my theory:

1. How would you do https://github.com/ethereum/EIPs/issues/1644 in this system?
2. How would you do this: https://github.com/AztecProtocol/AZTEC
3. How would you do this: https://github.com/ethereum/EIPs/issues/865

---

**fubuloubu** (2018-12-18):

I won’t disagree that my spec wasn’t very well written, but I don’t think it precludes the use cases you brought up:

1644: Issuer’s transfer rules allows reclamation by designated 3rd party (i.e. caller doesn’t have to be msg.sender)

AZTEC: not deeply familiar with the protocol, but from I know the smart contract basically acts as a mixer so nothing really changes?

865: Ether is treated like an ERC20 (or potentially as a semi-fungible token), so I would imagine the same methodology would perhaps be easier to leverage.

I think a better counter-argument for the “framework” would be a use case where there is no clear stateful asset being interacted with (including the contract itself as an “actor” that is owned), or that can’t be accounted for with the 4 proposed types of assets.

I tried to make it general enough where it could encompass the vast amount of use cases I have come across, but specific enough where the programming model of how to utilize them is clear.

---

**vbuterin** (2018-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/jtremback/48/2634_2.png) jtremback:

> The rest of this thread is interesting, and I support the terminology of “actor” instead of “contract”, but this proposal looks terribly complicated and rigid. Ethereum found success because it provided a totally open environment for people to program their own abstractions. There is little overhead of trying to fit your application into some preconceived notion of what someone thought you should build. This is what made Ethereum appeal to so many more people than older systems like colored coins and Master Protocol etc.
>
>
> This proposal seems to be a big step backwards.

This is exactly why I personally support having something like [A minimal state execution proposal](https://ethresear.ch/t/a-minimal-state-execution-proposal/4445) as the base layer. This actor/asset model, along with other approaches, can fairly easily be built as layer 2 systems on top.

---

**sg** (2018-12-19):

For 1st layer: TxVM + IvyLang would be very good beginning point I think.

For 2nd layer: I would suggest an UTXO Contract generative DSL in this [deck](https://speakerdeck.com/shogochiai/stateful-txo-is-the-new-contract)


*(9 more replies not shown)*
