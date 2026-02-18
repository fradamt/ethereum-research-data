---
source: magicians
topic_id: 1969
title: EIP-1577 - Multiaddr support for ENS
author: rachelhamlin
date: "2018-11-21"
category: Working Groups > Provider Ring
tags: [ens, provider-ring]
url: https://ethereum-magicians.org/t/eip-1577-multiaddr-support-for-ens/1969
views: 2068
likes: 17
posts_count: 16
---

# EIP-1577 - Multiaddr support for ENS

Let’s get the party started, Provider ring.

Back in May, [EIP1062](https://ethereum-magicians.org/t/eip-1062-formalize-ipfs-hash-into-ens-ethereum-name-service-resolver/281) kicked off conversation about standardizing an ENS resolver field for resource hashes.

After some discussion, the group had consensus that:

- Any storage protocol should be supported
- The protocol should be identifiable w/o additional context

The latest proposal for the ENS resolver is now [EIP1577](https://eips.ethereum.org/EIPS/eip-1577). It uses a new `contenthash` field, which supports `multiaddr`, and calls for deprecation of the `content` and `multihash` fields.

[@decanus](/u/decanus) and [@Arachnid](/u/arachnid) have updated [PublicResolver.sol](https://github.com/ensdomains/resolvers/blob/master/contracts/PublicResolver.sol), and I’d like to propose that the Ethereum providers plan to add support for this new EIP in the coming weeks.

Should be a trivial change, and we can maintain backwards compatibility for DApps using the `content` field (rare, to my knowledge) until EOY. DApps moving to IPFS or Swarm will be able to follow this standard from the start.

Thoughts [@p0s](/u/p0s) [@wolovim](/u/wolovim) [@bitpshr](/u/bitpshr)?

## Replies

**decanus** (2018-11-22):

I opened issues on [Status](https://github.com/status-im/status-react/issues/6688) and [Metamask](https://github.com/MetaMask/metamask-extension/issues/5742) repositories to get this integrated.

---

**justelad** (2018-11-25):

Greetings from the Swarm team.

We’ve been following the discussion on EIP-1062.

We already have an [issue](https://github.com/ethersphere/go-ethereum/issues/940) to track this since September and now that the discussion has converged into something more concrete and extensible we could proceed to implement the necessary changes on our side too.

Great work on this topic. ![:beers:](https://ethereum-magicians.org/images/emoji/twitter/beers.png?v=9)

---

**rachelhamlin** (2018-11-28):

Awesome [@justelad](/u/justelad). We’ll probably prioritize it in our next sprint.

Thanks for creating that issue [@decanus](/u/decanus)!

---

**bitpshr** (2018-11-29):

Thanks for raising this [@rachelhamlin](/u/rachelhamlin) and for filing a related issue [@decanus](/u/decanus). We’re planning to tackle this in our next sprint as well.

---

**andrey** (2018-12-12):

hey, I have a few questions

1. is new publicresolver deployed only in mainnet? do we have it deployed in testnets (ropsten, rinkeby) ?
2. how dapps developers can use this new contenthash  field . i know two ens managers
https://manager.ens.domains/
https://resolver.portal.network/
but both support only “old” content field, do we know who works on these two and if there are any plans to add contenthash  field support?

---

**Arachnid** (2018-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/andrey/48/635_2.png) andrey:

> is new publicresolver deployed only in mainnet? do we have it deployed in testnets (ropsten, rinkeby) ?

It’s deployed on mainnet; I don’t believe we’ve updated the Ropsten or other test network resolvers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/andrey/48/635_2.png) andrey:

> how dapps developers can use this new contenthash field . i know two ens managers

We’ll add support to the new manager soon. It’ll be up to others to add support themselves; we’ll be reaching out to them to help with that.

---

**angerborn** (2018-12-14):

Is there any known address that can be used to test a contenthash implementation?

I haven’t found any that use the new resolver yet.

---

**decanus** (2018-12-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/a/b782af/48.png) angerborn:

> Is there any known address that can be used to test a contenthash implementation?

yeah there is: pac-txt.eth

---

**pldespaigne** (2019-01-10):

Hi everyone !

I have just deployed an EIP1577 compliant resolver on **ropsten** so anybody can experiment ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

The code has been verified so you can interact with the resolver directly on etherscan !

https://ropsten.etherscan.io/address/0xde469c7106a9FBC3fb98912bB00be983a89bDDca

Also, if you need I have made a small npm lib to encode / decode content hashes : [content-hash](https://www.npmjs.com/package/content-hash)

---

**justelad** (2019-02-18):

[@Arachnid](/u/arachnid), [@decanus](/u/decanus)

1. If I am not mistaken the public resolver code on the main go-ethereum codebase has to be updated (the one under contracts/ens/contract/PublicResolver.sol). Should I submit the change? I’m not sure about how you roll out these sort of changes and indeed this change affects all ethereum users that use ENS so it should be tested out thoroughly. Please advise how to proceed
2. The EIP description has a small mistake and mentions that Swarm and IPFS proto-codes are 0xee and 0xef, when in fact they are 0xe3 and 0xe4

---

**Arachnid** (2019-02-18):

You’re right, that will need updating for swarm. If you’d like to submit a PR, that’d be great.

I’ll fix the codes in the eip.

---

**justelad** (2019-02-19):

> If you’d like to submit a PR, that’d be great.

I’m on it ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**justelad** (2019-03-07):

The EIP specification mentions that the

> values are encoded as v1 CIDs without a base prefix

1. This means that they are in fact not valid CIDs (as according to the CID spec)
2. This kind of pulls the rug out from using the multiformat libraries to maintain compatibility with the spec.
3. The EIP spec does not mention the default (only allowed?) encoding assumed (I am assuming base16 but IPFS assumptions are base58? so both should assume base16). Without a base prefix we must assume a certain encoding in order to unmarshal safely.

Thanks!

---

**Arachnid** (2019-03-07):

The CIDs are encoded in binary format. The CID spec says:

> NOTE:   Binary  (not text-based) protocols and formats may omit the multibase prefix when the encoding is unambiguous.

---

**mcdee** (2019-03-18):

FYI for testing purposes I’ve set up content hashes for `ipfs.enstest.eth` and `swarm.enstest.eth` on both ropsten and mainnet.

`swarm` is set with hash `d1de9994b4d039f6548d191eb26786769f580809256b4685ef316805265ea162` and `ipfs` with hash `QmRAQB6YaCyidP37UdDnjFY5vQuiBrcqdyoW1CuDgwxkD4`

