---
source: magicians
topic_id: 11764
title: Using Kademlia (Kad) for processing transactions; libp2p RPC for Ethereum clients?
author: rook
date: "2022-11-16"
category: Magicians > Primordial Soup
tags: [networking, kad]
url: https://ethereum-magicians.org/t/using-kademlia-kad-for-processing-transactions-libp2p-rpc-for-ethereum-clients/11764
views: 816
likes: 0
posts_count: 1
---

# Using Kademlia (Kad) for processing transactions; libp2p RPC for Ethereum clients?

As it stands, Ethereum nodes will reach out to the Kademlia DHT (Kad) for syncing block data: ([To what extend does Ethereum benefit from Kademlia? - Consensus - Ethereum Research](https://ethresear.ch/t/to-what-extend-does-ethereum-benefit-from-kademlia/7874)).

Ethereum could use Kad’s interface to provide a wider range of services to lite-clients and to the IPFS ecosystem built on Kad.

Kad and Libp2p have very useful features for web3 lite-clients. For example libp2p has advanced solutions for censorship resistance, edge caching, and advanced network hole punching for NAT traversal - making it easy for a client who is on the move to send out a transaction or get an update. Kad is the solution for both BitTorrent magnet tracking and IPFS - and it could also process Ethereum transactions without an additional gateway.


      ![image](https://docs.libp2p.io/logos/libp2p_color_symbol.svg)

      [libp2p](https://docs.libp2p.io/concepts/nat/)



    ![image](https://docs.libp2p.io/logos/libp2p_monochrome_hero)

###



We want libp2p applications to run everywhere, not just in data centers or on machines with stable public IP addresses. Learn about the main approaches to NAT traversal available in libp2p.










Kad is a lite and decentralized way for dapps to interact with chain state without needing to run a full node or rely upon a 3rd party HTTP/websocket gateway. A dapp running on a lite-client can use Kad to talk to Ethereum and IPFS, and for apps to talk to each-other.  In practice dapp will end up tapping into libp2p’s abilities in a growing ecosystem without needing any central authority or gateway.

Ethereum nodes can use Kad’s pub/sub to look for new transactions by monitoring a global pub/sub key.  A lite-client could pass a signed transaction to any Kad node and the network will make sure that this message reaches the global subscription key that is monitored by full Ethereum nodes. This allows clients who are transient or being filtered to pass a message that they know will be delivered to a full node.

State read through Kad is untrusted, but there are transport protocols on-top of Kad that solve this problem.  A signing key would need to be transferred out of band between the client and a trusted node, or using key negotiation.  A public signing key could be shared by all devices or apps from a manufacturer.  This is not unlike the oauth site-id and secret-key used by google oauth. So a vendor could have trusted mobile devices and IoT devices that send or receive trusted or private data from Kad.  TLS works over Kad and is built into libp2p, so trusted certificates could be used to establish trust relationships.



      [github.com/libp2p/specs](https://github.com/libp2p/specs/blob/master/noise/README.md)





####

  [master](https://github.com/libp2p/specs/blob/master/noise/README.md)



```md
# noise-libp2p - Secure Channel Handshake

> A libp2p transport secure channel handshake built with the Noise Protocol
> Framework.

| Lifecycle Stage | Maturity       | Status | Latest Revision |
|-----------------|----------------|--------|-----------------|
| 3A              | Recommendation | Active | r5, 2022-12-07  |

Authors: [@yusefnapora]

Interest Group: [@raulk], [@tomaka], [@romanb], [@shahankhatch], [@Mikerah],
[@djrtwo], [@dryajov], [@mpetrunic], [@AgeManning], [@morrigan], [@araskachoi],
[@mhchia]

[@yusefnapora]: https://github.com/yusefnapora
[@raulk]: https://github.com/raulk
[@tomaka]: https://github.com/tomaka
[@romanb]: https://github.com/romanb
[@shahankhatch]: https://github.com/shahankhatch
```

  This file has been truncated. [show original](https://github.com/libp2p/specs/blob/master/noise/README.md)












      [github.com](https://github.com/libp2p/go-libp2p-tls)




  ![image](https://opengraph.githubassets.com/9a7d00a2ceaff85c9366dbe715665b58/libp2p/go-libp2p-tls)



###



go-libp2p's TLS encrypted transport
