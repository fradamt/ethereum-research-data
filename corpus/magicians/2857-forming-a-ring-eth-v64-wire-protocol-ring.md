---
source: magicians
topic_id: 2857
title: "Forming a Ring: ETH v64 Wire Protocol Ring"
author: matthalp
date: "2019-03-05"
category: Working Groups
tags: [eth-v64-wire-protoco]
url: https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857
views: 5665
likes: 48
posts_count: 42
---

# Forming a Ring: ETH v64 Wire Protocol Ring

Using the [provided template](https://ethereum-magicians.org/t/about-the-working-groups-category/305):

- Why should people use this category? What is it for?
The ETH v64 Wire Protocol Ring focuses on the next iteration of the ETH Wire Protocol.
- How exactly is this different than the other categories we already have?
There is not a working group scoped to networking changes; specifically not ones meant to be immediately actionable.
- What should topics in this category generally contain?
The scope of this ring should be entirely focused on the ETH v64 wire protocol.
- Do we need this category? Can we merge with another category, or subcategory?
Yes. No.

## Replies

**matthalp** (2019-03-05):

# Call for ETH v64 Wire Protocol Enhancements

## Background

The ETH wire protocol provides the [application layer](https://en.wikipedia.org/wiki/OSI_model#Layer_7:_Application_Layer) for Ethereum clients. A lot has changed and a lot has been learned since the last ETH wire protocol was introduced in 2015.

The significant state requirements to operate a node are hindering the health of the network. Synchronization requires a large amount of state to store and download from peers. The implications of this include:

- Conventional hardware nodes cannot willingly join and participate in the network
- Syncing from scratch takes a very long time (e.g. days)
- Networking bandwidth requirements can be outstanding

## Process

The recommended process for selecting ETH v64 wire protocol enhancements is as follows (the later stages can happen on a proposal-by-proposal basis):

1. Solicit proposals for ETH v64 in this ring: Begin with brainstorming and informal discussions for improvements. This can happen initially happen within this thread, but should probably be broken out into a separate thread if more organization and focus is needed.
2. Establish Contributors and Stakeholders: The ring will identify proposals worth pursuing and establish who will drive them forward.
3. EIP Drafting and Prototyping: Create initial EIPs outlining the enhancements and solicit broader feedback. It is highly encouraged that running prototypes accompany any EIP.*

---

**ajsutton** (2019-03-06):

One common problem encountered when using Eth62 & 63 is that on MainNet there is a mix of ETC and ETH nodes all sharing the same network ID.  While they have different chain IDs, it’s only the network ID that’s sent as part of the ETH63 STATUS message so connections are established and clients have to do things like explicitly request the DAO block or wait until an invalid header is received post-DAO block which triggers a disconnect.  For fast sync these ETC peers are particularly problematic as they can lead to selecting an ETC block as the pivot and then fast sync fails.

Additionally, the difference between chain ID and network ID is a constant source of confusion for users who commonly believe they are the same thing.

I’d propose dropping network ID entirely and using only chain ID which would then be included in the STATUS message. That would allow nodes from different chains to immediately identify the mismatch and reject the connection quickly.

---

**matthalp** (2019-03-06):

### Encapsulate Metadata as a Header Rather than Inlining Before Payload

#### Problem

Provide better encapsulation so that it is easier to add new message header fields in the future (Spoiler Alert: new header fields will be defined below ![:smiling_imp:](https://ethereum-magicians.org/images/emoji/twitter/smiling_imp.png?v=15)).

#### Proposal

Rather than an [ETH wire message](https://github.com/ethereum/wiki/wiki/Ethereum-Wire-Protocol) being MessageCode || Payload replace MessageCode with Header, where

`Header` is a list `[ MessageCode || Metadata-0 || ... lt Metadata-N ]`

Packet is `[ Header || Payload ]` where `Payload` conforms to the specification mandated for the`MessageCode` in the header.

---

**matthalp** (2019-03-06):

### Add a request ID field to Messages

#### Problem

The association between messages exchanged between peers is implicit which adds some code complexity. Making it explicit that a response message is tied to a particular request message would make this easier.

When communicating with a peer, it is not possible to receive messages out of order.

#### Proposal

Adopt the reqId field presented in the [Parity LES documentation](https://wiki.parity.io/Light-Ethereum-Subprotocol-(LES)). Response(s) to a request with a specified reqId would use the same reqId. Ideally this would be placed in the Header proposed above.

---

**matthalp** (2019-03-06):

# Making Pruned State Explicit

## Problem

ETH peers are not guaranteed to have all blockchain and state information stored. The most notable example is that a fast-sync node does not store all archival state. Further, there are emerging proposals to drop older blockchain data; making this problem worse in the future.

|  | Headers | Bodies | Receipts | State |
| --- | --- | --- | --- | --- |
| Light | None | None | None | None |
| Pruned | All | Recent | Recent | Recent |
| Fast | All | All | All | Recent |
| Archive | All | All | All | All |

The table is meant to compare the different types of peers seen on the network and what blockchain and state data they hold; demonstrating that there is somewhat of a hierarchy and way to generalize what any given peer holds. Going bottom up:

- Archive Nodes (geth --syncmode full --gcmode archive): Contains all historical information from genesis until the chain head.
- Fast Nodes (geth --syncmode fast --gcmode full): Contains all historical chain data, but only the recent 127(ish) state histories.
- Pruned Nodes: Are nodes that also choose to drop old blockchain state. There are currently unofficial or experimental builds.
- Light Nodes: Run the light protocol and are really not guaranteed to have anything.

## Proposal

Make pruned state apparent by providing guarantees for data availability from a given client. Specifically, to expose these guarantees as additional "window" fields [on the STATUS message first exchanged between ETH peers](https://github.com/ethereum/wiki/wiki/Ethereum-Wire-Protocol#ethereum-sub-protocol). This allows for better abstractions to orchestrate data exchanges amongst peers.

The “window” corresponds to the maximum distance behind the peer’s current chain head where a given data component will be guaranteed by a client. It is the responsibility of the client to track its peers height to know the current range supported by a window.

|  | HeaderWindow | BodyWindow | ReceiptWindow | StateWindow |
| --- | --- | --- | --- | --- |
| Light | 0 | 0 | 0 | 0 |
| Pruned | MaxValue | 1,000 | 1,000 | 127 |
| Fast | MaxValue | MaxValue | MaxValue | 127 |
| Archive | MaxValue | MaxValue | MaxValue | MaxValue |

#### Considerations

- Older information will become more and more scarce over time (hopefully to some limit with good actors).
- Care will have to be taken amongst peers to have policies to ensure they are connecting to the right peers there will be orders of magnitude more storing minimal state than the maximal state.

---

**matthalp** (2019-03-06):

# Folding LES into ETH

## Problem

The LES subprotocol competes the ETH in two ways. The first, it fragments developer mindshare between the two protocols. Second, it can fragment the code bases that support both. Consolidating the two would be an all around community win.

## Proposal 1: Dropping the DHT

The DHT approach to LES feels too fragile and complex for adoption. Specifically:

- It’s a very complex idea
- Debugging issues is incredibly challenging
- How well it supports use cases (i.e. performance and reliability) is unclear

## Proposal 2: Adding the Various LES Messages to ETH

Incorporate a subset of the LES messages to ETH (especially proof-related ones) and possibly make them more granular/higher-level. Again drawing from the [Parity LES documentation](https://wiki.parity.io/Light-Ethereum-Subprotocol-(LES)):

### Keep

1. (Get)Proof. However, the interface could be made more high-level so that the proof for whether the account state trie, account storage trie(s), or both are being requested.
2. (Get)ContractCodes
3. (Get)TransactionProofs would now have to be (Get)BlockProofs now that the intermediate state root has been removed from transaction receipts.

### Remove

1. Capabilities as they would now be apparent from the proposal for making pruned state apparent.

---

**matthalp** (2019-03-06):

# Consider Incorporating Client-side Flow Control

One idea that is particularly interesting from LES is client-side [flow control](https://github.com/zsfelfoldi/go-ethereum/wiki/Client-Side-Flow-Control-model-for-the-LES-protocol) and may be worth incorporating into ETH. This is particularly useful for managing unbalanced peer relationships. For example a light node constantly requesting state proofs from an archive node could be kept in check and an archive node could now scale the number of light nodes it supports knowing that it will not be overwhelmed. The client-side flow control would also for client implementation to implement the code to handle DoS protection for the messaging layer.

## Proposal

Add a budget field (`budget`) to the message header (proposed above) that denotes the remaining request budget a peer has. A peer request would decrease the budget field by some pre-agreed upon amount, such as applying a gas cost-like scheme to the different messages (e.g. N units budget per header returned for a GetHeader operation). There can be a policy for replenishing a peer’s budget over time (such as what AWS does with vCPU compute units) and also for serving requests. The values for these parameters can be specified in the STATUS message that is first exchanged before continuing the ETH protocol.

---

**FrankSzendzielarz** (2019-03-06):

An additional thing to be aware of that should also help resolve this kind of difficulty is ENR in discovery v5, which is being implemented right now. https://github.com/ethereum/devp2p/tree/master/discv5

ENRs are signed, versioned key/value lists to a maximum of 300 bytes, which will replace the usual ID,IP,PORT tuples passed around in discovery v4. There will be mandatory keys (Eg: identity scheme, id) and then additional, arbitrary extensions to that. By adding a key/value providing the necessary information (network id, chain id), correct nodes can be found without even having to establish a handshake.

---

**karalabe** (2019-03-06):

I have a few pain points I’d like to get addressed. These are not so much theoretical protocol niceties, rather than actual nasty issues that cause some part of node implementations to behave suboptimally.

---

`eth/63` has a `GetNodeData(hash)` method (or some variation of this). This is used to retrieve either a trie node identified by is hash, or a bytecode identified by its hash. In theory this is a nice, flexible thing. In practice, this is horribly too flexible.

This method makes the assumption that nodes store all code and all trie nodes as `hash->value` mappings. This assumption actually **forces** nodes to do this, even though it makes no sense. The false assumption was that nodes will deduplicate data, and this `hash->value` mapping is the most optimal.

Nodes may not want to deduplicate data so aggressively: storage tries across multiple accounts *can* share the same data with the same hash (in practice they won’t much). However, if nodes implement pruning, they need to **duplicate** this data back, because a pruning algorithm won’t b able to track references across multiple account (potentially infinite).

This is a problem, because the `GetNodeData` assumes the node can retrieve a trie node by it’s hash, whereas if it’s duplicated, we also need the **account** to which it belongs to to retrieve.

- Parity hacks around this issue by xor-ing the account into the hash’s last 20 bytes, and when retrieving a trie by hash, they iterate the database for the first 12 byte prefix, and if multiple results are found, they hash on the fly to check which is good.
- Geth’s PoC pruning code currently appends the account to the hash and uses a similar iteration mechanism to pull the data from disk. For us this is problematic because storing them by  order instead of  would give us proximity, but break iterability. Similarly this fetch-by-hash requirement puts a huge burden on in-memory caches, which need extra indexing structured to allow translatinc account-scoped trie nodes into “global deduped trie nodes”.

My request is that the GetNodeData beextended with a context parameter, clearly stating which account a particular trie node should be pulled from. If a node dedupes everything as now, it can simply ignore the context and still work cleanly. If a node stores them contextually, the extra data can help speed access up a lot. During a fast sync you know the context either way when downloading the data, so there’s no overhead there either.

I would also make a separate call for retrieving a trie node and retrieving code. IT makes things cleaner and allows still deduping code and storing it potentially differently.

---

I forgot the other one, damn. Will post here when I remember it.

---

**ferranbt** (2019-03-06):

Hello.

I have been working for the past months on an alternative Ethereum client in Go (https://github.com/umbracle/minimal). The main focus of my work has been to build the different stack components of a client as modular as possible.

These are the problems I have encountered on the wire protocol and transport in general.

- During discovery with discv5 around 60% of the queried nodes are not correct, they either are from a different network or have a different genesis file. It would be nice to have a chainID number on the discovery messages or make the nodes filter from the internal discovery table those nodes not belonging to his network so they are not broadcasted to the network.
- As noted above, the lack of a ReqID is really painful. It limits the number of concurrent requests to a single node (i.e. only one header request per node). Minimal has some workarounds but are quite suboptimal.
- Parity and Geth have different maximum message sizes. That makes it hard to estimate how much memory to reserve.
- The transport layer (RLPX) gives two methods (SendMsg and ReadMsg) to interact with the protocol. I think it would be better to return net.Conn interface from RLPX. That gives you two immediate gains: You can built normal RPC method on top of net.Conn and have reqID functionallity and you can plug and play any other transport. This is already implemented in minimal.
- RLPX needs to have the full message on memory to run compression and encryption. We should encrypt and compress in batches (as TLS does).

---

**matthalp** (2019-03-06):

Frank: I’m in favor of ENRs. I think including this information at the discovery layer can be a useful hint to filter out bad/isolate good peers, however clients will still have to ultimately connect to verify this fact. Unless peers are validating the contents of ENR records before passing them around, this can still be gamed. FWIW I hope peers do this validation!

Adrian: One thing to note that 1:1 replacement of chain ID in place of network ID without updating anything else about the status message would be a breaking change (as the two cannot be distinguished). I think it’s more than likely there will be additional modifications to status messages (see: the proposal to expose pruned state), so this shouldn’t be an issue. If that turns out not to be the case, we can include both the network and chain ID and clients would know to just pay attention to the chain ID.

---

**matthalp** (2019-03-06):

> These are not so much theoretical protocol niceties, rather than actual nasty issues that cause some part of node implementations to behave suboptimally.

I would prioritize solving the nasty issues over theory ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> This method makes the assumption that nodes store all code and all trie nodes as  hash->value mappings. This assumption actually  forces  nodes to do this, even though it makes no sense. The false assumption was that nodes will deduplicate data, and this  hash->value  mapping is the most optimal.

I completely agree! TurboGeth’s data layout is a great example of where duplication improves performance.

> Geth’s PoC pruning code currently appends the account to the hash and uses a similar iteration mechanism to pull the data from disk. For us this is problematic because storing them by    order instead of    would give us proximity, but break iterability.

I actually feel like geth’s the [current state sync logic](https://github.com/ethereum/go-ethereum/blob/master/core/state/sync.go) and current trie sync logic could be enhanced to handle this. For example if the leaf node’s corresponding key was tracked and passed into the `trie.LeafCallback` then you could know whose account’s subtree (really the `keccak256(address)`) was being downloaded. Of course some additional enhancements would be needed too.

> My request is that the GetNodeData beextended with a context parameter, clearly stating which account a particular trie node should be pulled from.

What do you think about being even more explicit to distinguish between the account state trie, individual account storage tries, and account code? Basically three different message request/response pairs:

- (Get)AccountStateNodeData(hash)
- (Get)AccountStorageNodeData(accountIdentifier, hash) where accountIdentifier would either be the addressorkeccak256(address)`
- (Get)AccountCode(accountIdentifier, codeHash)

---

**matthalp** (2019-03-06):

> make the nodes filter from the internal discovery table those nodes not belonging to his network so they are not broadcasted to the network

![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=12) But I think this is really up to the client implementor to do. I would take it a step further and say that peers should disconnect from peers who even relay bad information!

> Parity and Geth have different maximum message sizes. That makes it hard to estimate how much memory to reserve.

Just to make this concise: Are you proposing a `maxMessageSize` field on a `Status` message? I did not know this was an issue, so it’s good to know. Although, are the message size differences so large that you can’t allocation memory for the maximum of the two sizes?

> The transport layer (RLPX)  …

I think you bring up great points, but RLPx enhancements are out-of-scope of things ring as `ETH` sits a layer above.

---

**FrankSzendzielarz** (2019-03-06):

Matthalp: Referring to the equirements document on the validation: https://github.com/ethereum/devp2p/blob/master/discv5/discv5-requirements.md Essentially, yes, to a large extent they will be valid. A balance must be struck (between validating and propagating). Direct validation is an attack vector.

If on higher level protocols these clients do not conform to their advertised capabilities, a similar reputation modification needs to happen as described in the discovery docs above (I think). Similarly, if the discovery level reputation changes (eg: a peer starts misbehaving on that level), the higher level protocol needs to consider disconnecting the peer. Incidentally, this is why I think it is a *design weakness to develop these protocols as totally separate concerns, or to design protocols without a common concept of peer reputation*

> " I would take it a step further and say that peers should disconnect from peers who even relay bad information!"

Yes. Definitely agreed, and it is a core design goal of Disc v5.(again, it’s in the doc above)

**One more thing: if you or anyone else has any other feedback on Disc v5 and Devp2p please add comments/thoughts via pull request to those documents ad lib. We are moving quickly now with implementation.**

---

**matthalp** (2019-03-06):

I will move my thoughts about discovery to your repo.

If you haven’t already you should consider starting a ring was well (and post the link here to direct interested parties). Repos are good for writing finished documents, but may not be the best forum for brainstorming. Just my two wei.

---

**carver** (2019-03-07):

Seems promising!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matthalp/48/1692_2.png) matthalp:

> HeaderWindow
> BodyWindow
> ReceiptWindow
> StateWindow
>
>
>
>
> Light
> 0
> 0
> 0
> 0
>
>
> Pruned
> 100,000
> 1,000
> 1,000
> 127
>
>
> Fast
> MaxValue
> MaxValue
> MaxValue
> Recent
>
>
> Archive
> MaxValue
> MaxValue
> MaxValue
> MaxValue

Some possible typos:

|  | HeaderWindow | BodyWindow | ReceiptWindow | StateWindow |
| --- | --- | --- | --- | --- |
| Light | 0 | 0 | 0 | 0 |
| Pruned | MaxValue | 1,000 | 1,000 | 127 |
| Fast | MaxValue | MaxValue | MaxValue | 127 |
| Archive | MaxValue | MaxValue | MaxValue | MaxValue |

- Pruned nodes have to keep the headers still, AFAIK, to accurately determine longest chain
- I assume some specific value was intended for Fast StateWindow. I’m not claiming to know what it is or should be

---

**matthalp** (2019-03-07):

Good catches – thanks! Both look more reasonable than what was there before.

---

**carver** (2019-03-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> GetNodeData assumes the node can retrieve a trie node by it’s hash, whereas if it’s duplicated, we also need the account to which it belongs to to retrieve.

During fast sync, how does the syncing client get access to the account address preimage in order to make this request to the server?

AFAIK, the syncing client can’t easily generate the address for arbitrary accounts. Instead, is it okay to include the **hash** of the address when requesting a storage trie node?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> I would also make a separate call for retrieving a trie node and retrieving code. IT makes things cleaner and allows still deduping code and storing it potentially differently.

Would you also like the account address (hash) when getting a request for the byte code?

---

**zsfelfoldi** (2019-03-13):

Hi everyone! As the designer of the LES protocol I am really glad to see that some of you support adding my message format extensions to ETH64 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) And even though I might be naturally biased toward these ideas I do think that adding ReqID to request-reply type messages is kind of a no-brainer. I would also strongly suggest using my handshake message format which is a general key-value list allowing peers to communicate extra parameters and capabilities in an easily extendable way.

The most complex addition of LES is the flow control mechanism which I believe has already been more or less proven to be useful but I am currently polishing it to truly show its potential. I would totally support making it available in ETH64 but on the other hand I do realize now that the way it is currently used in LES is probably also too strict and brittle. It has to be implemented precisely in order to avoid disconnections which might be a hindrance in the early development stage of new client implementations. Recently I had a very useful discussion with [FrankSzendzielarz](https://ethereum-magicians.org/u/FrankSzendzielarz) and he suggested adding a message similar to http 503 (temporarily unavailable) or 429 (too many requests) and sending that in case of a buffer underrun instead of instantly disconnecting. This way the flow control could be declared an optional hint mechanism which helps avoiding these nasty messages and the resulting delays but is not an absolute necessity to be perfectly implemented in every client. I believe this approach would be much better suited for ETH64 chain/state retrieval messages too. I will shortly write up a general protocol proposal which I want to apply to LES but I believe could be applied to other protocols in the Ethereum  protocol stack too. Having a common general protocol format would even allow us easily merging LES and ETH64 which was also suggested in this thread and which I would also support if done properly. I’ll try to finish my detailed proposal later this week.

---

**matthalp** (2019-03-14):

> Hi everyone! As the designer of the LES protocol I am really glad to see that some of you support adding my message format extensions to ETH64

[@zsfelfoldi](/u/zsfelfoldi) Thank you for coming up with these ideas! I enjoyed reading through them and thinking about how they would be used. Nice work! ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=12)

> I would also strongly suggest using my handshake message format which is a general key-value list allowing peers to communicate extra parameters and capabilities in an easily extendable way.

This is a good suggestion! This would be a general purpose way to accommodate the [" Making Pruned State Explicit"](https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857/6) proposal. I do think that there should be some mandatory fields, especially to address the [networkId/chainId issue](https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857/3) raised by [@ajsutton](/u/ajsutton). However, these mandatory fields can be moved to be mandatory keys.

> The most complex addition of LES is the flow control mechanism which I believe has already been more or less proven to be useful but I am currently polishing it to truly show its potential. I would totally support making it available in ETH64 but on the other hand I do realize now that the way it is currently used in LES is probably also too strict and brittle.

I agree that [“Consider Incorporating Client-side Flow Control”](https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857/8) is something to have in the long-term. While it may not be there initially, the goal of the [“Encapsulate Metadata as a Header Rather than Inlining Before Payload”](https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857/4) is to make it easy to add metadata fields like this in the future.

> Recently I had a very useful discussion with FrankSzendzielarz and he suggested adding a message similar to http 503 (temporarily unavailable) or 429 (too many requests) and sending that in case of a buffer underrun instead of instantly disconnecting.

This is an interesting idea! I wonder how this would work end-to-end. Would the message contain some information to help the almost-spammy peer know when it can begin sending messages again? It seems like there needs to be some explicit agreement set for what will help the almost-spammy peer’s behavior improve.

> Having a common general protocol format would even allow us easily merging LES and ETH64 which was also suggested in this thread and which I would also support if done properly.

![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12) I was somewhat worried that [" Folding LES into ETH"](https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857/7) would be controversial. I’m glad to hear this is open for consideration.


*(21 more replies not shown)*
