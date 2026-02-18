---
source: magicians
topic_id: 9517
title: "EIP-5139: Remote Procedure Call Provider Lists"
author: SamWilsn
date: "2022-06-07"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-5139-remote-procedure-call-provider-lists/9517
views: 2520
likes: 18
posts_count: 13
---

# EIP-5139: Remote Procedure Call Provider Lists

https://github.com/ethereum/EIPs/pull/5139

## Replies

**tjayrush** (2022-06-07):

Any time I see these sort of “registry” or “list” ideas, I ask the obvious question: who is allowed to maintain this list.

I’m not in any way arguing that this is or is not a good idea. (In fact, I think it is a good idea), but without at least a discussion of mechanism involved in who manages this list, this has all the obvious problems.

1. who reviews it?
2. who says who’s a valid entry?
3. what are the criteria for a valid entry?
4. how do we avoid people paying to be included (or paying to remove someone else)?

At the very least these questions should be addressed in the document. In fact, I think one would need to fully flesh out how this would work. The fact that these considerations are non-existent in the EIP is a non-starter for me.

---

**SamWilsn** (2022-06-07):

> ChainId being listed ultimately is for readability, a wallet would be remise to not check for chainId/netVersion when connecting to a new rpc endpoint.

Yeah, I’d expect wallets to continue to do that.

> Net Version is used by metamask fwiw.

I’m mostly going for compatibility with [EIP-3326](https://eips.ethereum.org/EIPS/eip-3326), which uses chain id as the key. Would adding net version help wallets verify the RPC endpoint, and if so, how often do net versions change?

---

**SamWilsn** (2022-06-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> who reviews it?

It would ultimately be up to the end user to review whatever list they choose to use. Most of the time, users would default to the list provided by their wallet, which would be maintained by the wallet developers. Since we already give ultimate control over private keys to wallets, it seems reasonable to also delegate provider list maintenance to wallet devs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> who says who’s a valid entry?

In a formatting sense, wallets would be expected to validate lists against the JSON schema. In a more practical sense, that’s really up to the user to decide who to subscribe to. Maybe some service will come along that monitors your RPC activity and in exchange recommends products and services you might like ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> what are the criteria for a valid entry?

If the schema validates, it’s a valid list. If the providers listed don’t work, then it’s a bad list and you shouldn’t subscribe to it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> how do we avoid people paying to be included (or paying to remove someone else)?

We don’t. I completely expect each wallet to have their own list and not list competing providers. That’s no different from what we have now. The benefit of this standard is to allow users to easily choose other lists, without normalizing adding random one-off providers from whatever dapp you happen to be on.

---

I’ll add some of this to the document.

---

**sbacha** (2022-06-08):

I do not think net_version helps at all actually, more of an artifact of a pre-ChainId environment.

Are you wanting to use the latest JSON-Schema format as I see its using `https://json-schema.org/draft/2020-12/schema` version? I ask because I would have thought using OpenRPC format would be natural (I do not know the differences if any).

Are you also wanting to enumerate custom RPC methods that may be supported by difference RPC Providers? What sort of help do you want?

Cheers

---

**SamWilsn** (2022-06-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> I do not think net_version helps at all actually, more of an artifact of a pre-ChainId environment.

Good to know, I won’t include it then.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> Are you wanting to use the latest JSON-Schema format as I see its using https://json-schema.org/draft/2020-12/schema version?

I did choose the latest version, though I’m not super familiar with JSON Schema. I can use an older version if there’s a good reason?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> I ask because I would have thought using OpenRPC format would be natural (I do not know the differences if any).

I think OpenRPC is for defining an interactive API, while JSON Schema is for defining the structure of a single file, though I may be mistaken. These lists are single files, so I went with JSON Schema.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> Are you also wanting to enumerate custom RPC methods that may be supported by difference RPC Providers? What sort of help do you want?

I have a few concerns about adding this kind of information:

1. What is the value of adding this information to the list instead of the wallet trying the functions itself?
2. How do you account for different implementations of the same function (eth_signTypedData being a prime example)?
3. Is this a lot to ask of list maintainers?

---

**sbacha** (2022-06-21):

Will get back to you after hearing more about this its looking nice ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**sbacha** (2022-07-28):

thanks for answering my questions, have a few more now:

should there be support for `user@pass:fqdn.rpc.com` style RPC endpoints?

also, can there be an optional field for RPC endpoints that have a status/healthccheck?

---

**SamWilsn** (2022-07-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> should there be support for user@pass:fqdn.rpc.com style RPC endpoints?

Would `user` and `pass` be parameters, or included in the list itself? I think a literal `https://user:pass@example.com` should Just Work™, but passing in the user’s credentials might be out of scope?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> also, can there be an optional field for RPC endpoints that have a status/healthccheck?

Are these standardized? I think there’s some appetite for a capabilities exchange in a handshake, and I could see a status endpoint being a part of that.

---

**LefterisJP** (2022-08-20):

Hey Sam,

Thanks a lot for taking the time to write this EIP.

We have something sort of similar in rotki. Each user has a list of nodes they can use and a probability by which each node will be used by any query in the app: [rotki Usage Guide — rotki 1.25.2 documentation](https://rotki.readthedocs.io/en/latest/usage_guide.html#ethereum-rpc-nodes)

Our implementation is more rotki specific. And not important here. But we allow each user to completely customize their suscribed nodes.

Having it in a standardized way like this EIP suggests may be a good idea. Some comments.

1. The versioning is perhaps an overkill and overcomplication? I mostly imagine people subscribing to a list and then changing things on their own, creating their own custom list at the end.
2. I think it can be extended. Wallets probably don’t care about this but apps like rotki that need the node to query historical data care. So we could have a new key, let’s say capabilities containing an object that defines the capabilities of the node.

Something like:

```json
{
    is_archive: false,
    history_pruned_after_block: 120000,
    gas_limit: 3600000
}
```

The list of capabilities just popped in my mind right now and probably could be expanded. The ones I mentioned are important for an app using historical data since:

- archive: Would determine if we can query historical state.
- history_pruned_after_block: Would help us figure out if the node is pruned. If it is and the block is recent we know that we can’t ask it for transactions/receipts before the block. This has hit us often in rotki for example, and it’s always so annoying to debug the issue to figure out that the node the user used was just pruned.
- gas_limit: In a query context gas limit is also really important. If you use something like a multicall that loops over many subcalls the gas limit is what would determine how many such subcalls you can fit in a single rpc call.

These are just some thoughts off the top of my head. They are all guided by our own experience and uses in rotki.

---

**SamWilsn** (2022-08-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lefterisjp/48/107_2.png) LefterisJP:

> The versioning is perhaps an overkill and overcomplication? I mostly imagine people subscribing to a list and then changing things on their own, creating their own custom list at the end.

Do you mean versioning specifically, or extension lists?

I’m on the fence about extension lists, since they add a ton of complexity, but on the other hand, they do let users port/share the same customizations between different wallets, so… I’m really not sure.

Versioning I think is useful regardless of whether there’s extension lists. If the list maintainer removes an entire rollup for some reason, I think it’d be good to make that visible to the user.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lefterisjp/48/107_2.png) LefterisJP:

> I think it can be extended. Wallets probably don’t care about this but apps like rotki that need the node to query historical data care. So we could have a new key, let’s say capabilities containing an object that defines the capabilities of the node.

Capabilities have come up quite a few times now ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12) They seem sorely needed. Would you rather have this information in the list itself, or in some kind of handshake (new RPC endpoint?) between the provider and the consumer?

---

**tjayrush** (2022-08-20):

Capabilities is a great idea. We would use it, but it seems to me this should be a new RPC method in the best case.

---

**sbacha** (2023-04-15):

am working on this but for gRPC v2 spec methods, completely clean of existing json rpc v1

