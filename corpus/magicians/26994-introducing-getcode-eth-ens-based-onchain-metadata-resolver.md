---
source: magicians
topic_id: 26994
title: "Introducing *.getcode.eth: ENS based onchain metadata resolver"
author: 0xc0de4c0ffee
date: "2025-12-07"
category: Web
tags: [metadata, ens, devtools]
url: https://ethereum-magicians.org/t/introducing-getcode-eth-ens-based-onchain-metadata-resolver/26994
views: 263
likes: 15
posts_count: 10
---

# Introducing *.getcode.eth: ENS based onchain metadata resolver

# What is *.GetCode.eth?

Solidity compiler by default appends CBOR-encoded metadata to contract’s bytecode. `*.getcode.eth` is an ERC-3668 wildcard ENS resolver that extracts metadata hash from contract’s bytecode and resolves that as ENS contenthash.

## Examples :

a) zAMM contracts: [0x00000000008892d085e0611eb8C8BDc9FD856fD3.getcode.eth](https://0x00000000008892d085e0611eb8C8BDc9FD856fD3.getcode.eth.limo/)

b) Safe Proxy: [0xA23dfEA786465E0Ef51eD6C288c9f0070d047ef7.proxy.getcode.eth](https://0xA23dfEA786465E0Ef51eD6C288c9f0070d047ef7.proxy.getcode.eth.limo/)

### Basic UI with Metadata parsing & download features




      [getcode.eth.limo](https://getcode.eth.limo/)





###



Extract Solidity metadata from any contract as ENS contenthash. View sources, ABI, and download CAR/ZIP archives.










### Resolver source code :

[0x7661a4705F10d828B7d9FAB680c6E9559faEABB0 (verified on etherscan)](https://etherscan.io/address/0x7661a4705F10d828B7d9FAB680c6E9559faEABB0#code)

## 3 modes of operation

Direct mode :

`0x<addr>.getcode.eth  ->  IPFS contenthash (0xe3010170...)  of metadata.json`

CBOR mode :

`0x<addr>.cbor.getcode.eth  -> Returns Raw dag-cbor CID of metadata`

Proxy Mode :

`0x<addr>.proxy.getcode.eth  -> Tries to detect proxy & resolve metadata.json`

## Limitations :

a) old contracts don’t have embedded metadata in contract bytecode

b) all most all contracts with swarm metadata are fail to resolve as they’re not pinned in swarm storage

c) bad proxies like USDC return blank implementation() address

d) lots of contracts don’t have their IPFS metadata pinned in IPFS network

You can read more about this in https://playground.sourcify.dev/, `*.getcode.eth` is same as sourcify playground but 100% onchain using contract’s bytecode & ENS wildcard resolver.

## Replies

**oed** (2025-12-09):

Very cool!

I actually suggested something similar to the Sourcify team recently: [sourcify.eth-subdomains.md · GitHub](https://gist.github.com/oed/6ddfc9ca5f753852a72bd264fc213701)

---

**kuzdogan** (2025-12-12):

Sourcify developer here, very cool! Thanks for shipping this. Is it open source somewhere?

---

**0xc0de4c0ffee** (2025-12-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> Very cool!
> I actually suggested something similar to the Sourcify team recently: sourcify.eth-subdomains.md · GitHub

![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12) I see you’ve `cidv1.eth` ref in gist…  ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12) Hello from Namesys.eth team here. I only published this resolver coz of recent etherscan API drama.![:stuck_out_tongue_closed_eyes:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue_closed_eyes.png?v=12)

There’s new 128 bytes limit for inlined CIDs in [IPIP-0512](https://specs.ipfs.tech/ipips/ipip-0512/)

I’m asking around to increase that limit to at least 256 bytes… https://discuss.ipfs.tech/t/cidv1-eth-onchain-raw-cidv1-library/19444/11?u=0xc0de4c0ffee

Another possible issue, there’s no `index` and ipfs  `_redirect` supported in dag-cbor, and it was was even failing over `cidv1.eth`’s raw dag-pb/unixfs too. I have to recheck that.

Multichain support with CCIP is cool feature, sourcify team have to run their own signed web2 gateway+fallback servers to handle that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kuzdogan/48/13889_2.png) kuzdogan:

> Sourcify developer here, very cool! Thanks for shipping this. Is it open source somewhere?

Resolver is verified on both sourcify & etherscan… UI is basic Helia+CAR builder parsing metadata.json. I even pinged [@ligi](/u/ligi) over twitter to take a look. I’ll be waiting to review & test sourcify’s resolver… ++ I can transfer this `getcode.eth` domain to sourcify team. Just ack and it’ll be yours to deploy v2 with l2 support.

---

Link to ens forum : [Introducing *.getcode.eth: onchain wildcard contract metadata resolver - Integrations - ENS DAO Governance Forum](https://discuss.ens.domains/t/introducing-getcode-eth-onchain-wildcard-contract-metadata-resolver/21692)

we even got new feature request to support `sub-domain-eth.getcode.eth`… I prev removed sub.domain.eth support to save wildcard ssl certs over ethlimo side.

---

**oed** (2025-12-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xc0de4c0ffee/48/5927_2.png) 0xc0de4c0ffee:

> There’s new 128 bytes limit for inlined CIDs in IPIP-0512
> I’m asking around to increase that limit to at least 256 bytes… CIDv1.eth : onchain raw/cidv1 library - #11 by 0xc0de4c0ffee - IPFS Forums

In the case I outlined this isn’t an issue because we wouldn’t be using inline CIDs. Instead, we would calculate the actual CID on-chain, then we’d need to precompute the folder off-chain as well.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xc0de4c0ffee/48/5927_2.png) 0xc0de4c0ffee:

> Another possible issue, there’s no index and ipfs _redirect supported in dag-cbor, and it was was even failing over cidv1.eth’s raw dag-pb/unixfs too. I have to recheck that.

Oh, I thought your dag-pb/unixfs was compatible with the kubo one?

---

**0xc0de4c0ffee** (2025-12-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> In the case I outlined this isn’t an issue because we wouldn’t be using inline CIDs. Instead, we would calculate the actual CID on-chain, then we’d need to precompute the folder off-chain as well.

That’d be last option to go for extra headache managing offchain pinning…

I was checking how much we could squeeze in 128 bytes of dagpb inlined.

max 2 inlined files only, metadata.json comes from contract & static offchain pinned index.html is total 115 bytes using CIDv1 OR 111 bytes using CIDv0… we’ve to use CDN/add js scripts in index.html.

link tested ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) : ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)https://ipfs.io/ipfs/f0170006b12330a221220f4cc38c6dd6d2b1c3d4f9081c017f99d119ca28e22eb7d515a2c6deb25349ebd120d6d657461646174612e6a736f6e12300a22122003d76bfe86d06e9a7a6b044b8979d7961078bef8b1673b6205a7da071ede6b51120a696e6465782e68746d6c0a020801/

I’ve to recheck to find how much of dag-pb/unixfs extra data we can skip in this without breaking… but for your use case of 2 files that should work within 128 bytes.

```auto
// cidv0, = NO hex"0170" prefix
bytes internal index_html_cid = hex"122003d76bfe86d06e9a7a6b044b8979d7961078bef8b1673b6205a7da071ede6b51";
bytes internal metadata_json_cid = hex"1220f4cc38c6dd6d2b1c3d4f9081c017f99d119ca28e22eb7d515a2c6deb25349ebd";

// ready to concat format using cidv0
//0170006b12330a22___CIDv0(metadata.json)___120d6d657461646174612e6a736f6e12300a22___CIDv0(index.html)__120a696e6465782e68746d6c0a020801

```

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> Oh, I thought your dag-pb/unixfs was compatible with the kubo one?

it is compatible & tested with kubo/helia js data. I mean there’s no index file supported with dag-cbor (index works for dag-pb only, eg link above) & _redirects isn’t working if it’s raw dag-pb/dag-cbor 0x00.

---

**oed** (2025-12-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xc0de4c0ffee/48/5927_2.png) 0xc0de4c0ffee:

> link tested  : https://ipfs.io/ipfs/f0170006b12330a221220f4cc38c6dd6d2b1c3d4f9081c017f99d119ca28e22eb7d515a2c6deb25349ebd120d6d657461646174612e6a736f6e12300a22122003d76bfe86d06e9a7a6b044b8979d7961078bef8b1673b6205a7da071ede6b51120a696e6465782e68746d6c0a020801/
>
>
> I’ve to recheck to find how much of dag-pb/unixfs extra data we can skip in this without breaking… but for your use case of 2 files that should work within 128 bytes.

Wow, that’s pretty cool! Your index.html isn’t resolving though ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**0xc0de4c0ffee** (2025-12-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oed/48/15357_2.png) oed:

> Wow, that’s pretty cool! Your index.html isn’t resolving though

Using CIDv1?  https://ipfs.io/ipfs/f0170122003d76bfe86d06e9a7a6b044b8979d7961078bef8b1673b6205a7da071ede6b51

CIDv0 only supports base58, for CIDv1/base16 `f` in gateway we’ve to add version `01` + dag-pb `70` prefix.

---

**oed** (2025-12-23):

I get a 504 on this link.

---

**0xc0de4c0ffee** (2025-12-24):

could be coz my local pinning server was down.. ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=15)

[![Screenshot](https://ethereum-magicians.org/uploads/default/optimized/3X/d/7/d7309837a6aac58a5b941688a669acc1453cdfe2_2_517x86.png)Screenshot1726×290 49.3 KB](https://ethereum-magicians.org/uploads/default/d7309837a6aac58a5b941688a669acc1453cdfe2)

[![Screenshot](https://ethereum-magicians.org/uploads/default/optimized/3X/5/4/54b8030c8d5f1ab3a7b2d2607af162129a21123b_2_517x103.png)Screenshot1482×298 42.3 KB](https://ethereum-magicians.org/uploads/default/54b8030c8d5f1ab3a7b2d2607af162129a21123b)

with full js reading ./metadata.json

[![Screenshot](https://ethereum-magicians.org/uploads/default/optimized/3X/4/6/46567c0e563df139a6f5d7e648e4026d22bfc863_2_517x177.png)Screenshot2302×792 410 KB](https://ethereum-magicians.org/uploads/default/46567c0e563df139a6f5d7e648e4026d22bfc863)

/merry xmas & happy new year ![:vulcan_salute:](https://ethereum-magicians.org/images/emoji/twitter/vulcan_salute.png?v=15)

