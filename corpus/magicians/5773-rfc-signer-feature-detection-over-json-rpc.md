---
source: magicians
topic_id: 5773
title: "RFC: Signer feature detection over JSON-RPC"
author: danfinlay
date: "2021-03-20"
category: EIPs > EIPs interfaces
tags: [wallet, json-rpc, eip-1559]
url: https://ethereum-magicians.org/t/rfc-signer-feature-detection-over-json-rpc/5773
views: 1091
likes: 6
posts_count: 9
---

# RFC: Signer feature detection over JSON-RPC

We’re quickly entering a multichain world, and the average wallet is connecting to several evm-compatible blockchains at once.

However, with EIP-1559, we’re also creating a wider gap between the behaviors of different EVM chains.

It would be nice if Ethereum wallets maintained “plug and play” interoperability with a trusted node if possible, but since a node may require (or at least support) signatures of different formats, it’s important that nodes provide wallets a method to learn about their varying requirements.

There are lots of ways this could be done, so I’m opening this thread to gather opinions on how, before we present & promote an approach across the client teams.

I’ll note initially that the current pattern is to have one method per variable parameter. We see this with `eth_chainId`, for example. Maybe that’s fine! I’m actually not completely against the one-feature-one-method approach. Maybe the right answer is to add a `eth_1559SupportBlock` method that returns the activation block number for that feature (null for unplanned).

Alternatively, we could provide “all the info a signer should need” under a single method. Maybe `eth_getSignerInfo` could return relevant state:

```auto
{
  chainId: 1,
  1559SupportBlock: 155_BLOCK
}
```

Or maybe some of you will feel that if we’re going to batch data on the RPC, maybe we should batch it all, and have some super-metadata method, like `eth_getNodeInfo`.

I don’t have a strong opinion at all, but hoping with a period of open discussion we’ll get any ideas for improvements integrated into the eventual proposal.

Pinging [@MicahZoltu](/u/micahzoltu) because I know he has some opinions on this and I want to get the record started.

## Replies

**MicahZoltu** (2021-03-21):

I would like to see a capabilities system where you can tell the provider the set of methods you *want* available (and perhaps versions you need) and the provider can reply letting you know which of those it has and what version it uses.

This would make it so that as a dapp, I can query when the provider is first connected to find out what capabilities I have access to and then alter my usage or fail fast for the user as appropriate depending on what is available.

I’m not a fan of coupling with EIPs because there may be features available on one chain that has nothing to do with an EIP but it is equivalent to the same feature on another chain with an EIP.  EIP-1559 is a great example of this because some blockchains have it natively, or have included it under a different change control process thus don’t have it named EIP-1559.

You bring up an interesting point about features that “are not available now but will become available in the future”.  Personally, I feel like that is a feature that won’t end up getting used much so I would prefer to not dedicate engineering effort toward supporting something like that.  When you connect you get the feature set and you should be able to have confidence that that feature set will be available at least for the full session.

---

**shanejonas** (2021-03-22):

`rpc.discover` from OpenRPC could handle the supported methods part.

For which EIPs are supported, a new method like `getSupportedEIPs` would be great, for clients or wallets to support. Another example of that would be returning if a client supports EIP155 or not.

In geth most, if not all the EIPs are implemented as “Forks”, so `if (BYZANTIUM) then xxx`, but ideally they are articulated as EIPs not forks (see https://github.com/ethereum/go-ethereum/pull/18401 for more inspriation)

---

**danfinlay** (2021-03-22):

Linking for the lazy:



      [spec](https://spec.open-rpc.org/#service-discovery-method)





###



The OpenRPC specification










I could definitely see that being a great addition for method detection.

> For which EIPs are supported, a new method like getSupportedEIPs would be great

I’ll also take Micah’s point though that these EIPs are effectively “features” and should probably be identified as features, since different chains might introduce the same features under different proposal IDs.

The MVP goal of this thread for me is to provide RPCs a way of self-declaring EIP-1559 support (though the flag doesn’t need that name), something like `usesMovingBaseFeeMinimumGasPrice` could do. This motivation is so that wallets can begin providing responsive interfaces for any chains that support the new tx format as soon as possible. Features may need to standardize around a feature identifying string in that case, and we might want that to be a common expectation of EIPs that add consumer-affecting features.

---

**danfinlay** (2021-03-23):

Noting that EIP-2930 is another example of a transaction format that a signer might want to be made aware of:


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2930)


    ![image]()

###

Details on Ethereum Improvement Proposal 2930 (EIP-2930): Optional access lists

---

**ryanschneider** (2021-03-23):

Agree that having some sort of RPC to inspect the capabilities of an RPC endpoint is desirable.  I think it needs to be in addition to OpenRPC’s `rpc.discover` since it’d be tricky to parse the discover response to really determine if a endpoint supports -1559 or -2930.

I think we have a tendency to try to solve too many problems at once though and then things get bogged down in details etc, so maybe for this particular case it’d make sense to keep the RPC focused to just “what transaction formats does this endpoint support”?

---

**danfinlay** (2021-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanschneider/48/945_2.png) ryanschneider:

> maybe for this particular case it’d make sense to keep the RPC focused to just “what transaction formats does this endpoint support”?

This was also suggested by [@timbeiko](/u/timbeiko). I’m fine with it, and it solves my current motivations. YAGNI!

---

**shanejonas** (2021-03-25):

Maybe something like:

`eth_getSupportedFeatures`

=>

```auto
{
  "EIP1159": true,
  "EIP2930": true,
  "EIP155": true
}
```

or maybe

```auto
["EIP1159", "EIP2930", "EIP155"]
```

This requires clients to expose features, and less focus on which “Fork” (Byantium/London/etc) its part of.

That being said, is there an API call right now to get which fork a client supports?

---

**danfinlay** (2021-03-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shanejonas/48/1854_2.png) shanejonas:

> That being said, is there an API call right now to get which fork a client supports?

I don’t think so. For detecting ETC, we’d had to do things like query state that was known to have differed per fork.

I think your above example is totally adequate for this purpose, the array seems sufficient since all of these known features are binary (either adopted or not), we don’t *need* future-feature-detection.

If I were going to extend it at all it’d just to be for the response to be a map where the value is the activation block, just because it provides the “instant activation” ability. It’s not a deal breaker to not have that, but I don’t know why we’d exclude it when it’s information that every node is going to embed related to any optional features they activate.

