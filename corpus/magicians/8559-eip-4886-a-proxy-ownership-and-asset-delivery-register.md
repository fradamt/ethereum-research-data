---
source: magicians
topic_id: 8559
title: "EIP-4886: A proxy ownership and asset delivery register"
author: omnus
date: "2022-03-09"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-4886-a-proxy-ownership-and-asset-delivery-register/8559
views: 2988
likes: 2
posts_count: 6
---

# EIP-4886: A proxy ownership and asset delivery register

---

Proxy Ownership Register

A proxy ownership register allowing trustless proof of ownership between ethereum addresses, with delegated asset delivery

status: Draft

type: Standards Track

category: ERC

---

PR: [Pull request for eip for a proxy ownership register by omnus · Pull Request #4886 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4886)

Docs: https://docs.epsproxy.com/

## Replies

**matt** (2022-04-05):

[@omnus](/u/omnus) do you mind removing the EIP text from you post and just linking to the EIP PR? Thanks

---

**omnus** (2022-04-08):

That’s a good idea [@matt](/u/matt). Done!

---

**SamWilsn** (2022-04-14):

Interesting idea! Seems vaguely similar to [Non-Fungible Token with usage rights](https://github.com/ethereum/EIPs/pull/4512) by [@kkimos](/u/kkimos) and [EIP-4907](https://eips.ethereum.org/EIPS/eip-4907) by [@LanceSnow](/u/lancesnow) (et. al). I’d love to see all of these “separate transfer permission from usage permission” EIPs collaborate, though not strictly required.

---

**cxkoda** (2022-09-05):

Thanks for spinning up this EIP.

A few questions about some design decisions:

- Why did you decide to have a 1:1 relationship between nominator and proxy? Excluding multiple proxies?
- Why does the proxy need to accept the nomination on-chain? Couldn’t this also be done via an ECDSA signature from the proxy that is submitted together with the nomination in a single tx? (enabling the setup of proxies without having to fund them)
- Why did you decide to strip the nominating address of all benefits? In the EIP you give “otherwise two addresses represent the same holding.” as explanation. Whether this is a problem or a feature depends on the PoV and in some cases it might actually be the desired behaviour. In the former case it can easily be solved on the consumer side by doing all of the bookkeeping in terms of the nominating address. Is there more to it?

---

**omnus** (2022-09-06):

Hi [@cxkoda](/u/cxkoda),

Thank you very much for reading the EIP and taking the time to comment, I really appreciate it.

On your questions:

- Why did you decide to have a 1:1 relationship between nominator and proxy? Excluding multiple proxies?

Early on I considered creating a 1:n structure, but in the end opted for 1:1 for a few reasons:

1. To avoid duplicating rights. The rights inferred by owning an NFT are binary; either you own it or you don’t. If you create a 1:n structure then the rights associated with that token could be ‘double spent’.
2. An extension of the first point, but I think that at any moment in time you should be able to unambiguously identify the address that has the rights associated with holding an NFT. You can only do that with a 1:1 mapping.
3. To avoid the need for any unbounded loops within code, particularly on the smart contract side.
4. Ultimately, because it was simpler while still achieving the key use case, which was allowing users to operate as if they had the holding of another address. The key target use case for the protocol is this scenario, where a user owns and controls both the hot and cold wallets and wants to benefit from their holding without exposing it to interactions.

- Why does the proxy need to accept the nomination on-chain? Couldn’t this also be done via an ECDSA signature from the proxy that is submitted together with the nomination in a single tx? (enabling the setup of proxies without having to fund them)

It certainly could, and I think that’s a great idea! My main reason was that I wanted there to be no reliance on any off-chain component at all. Collecting a sig and then combining into another transaction would mean that the register isn’t maintained entirely on-chain.

Making it entirely on-chain has enabled me to deploy EPS as a ‘headless protocol’, in that there is no front-end off chain code required to add or maintain the register, and wallets never need to connect directly to a UI (not even something like etherscan). Instead the protocol exposes an API through ERC20 txns.

I mean to write up the headless protocol as an EIP at some point, I think it’s pretty neat :).

- Why did you decide to strip the nominating address of all benefits? In the EIP you give “otherwise two addresses represent the same holding.” as explanation. Whether this is a problem or a feature depends on the PoV and in some cases it might actually be the desired behaviour. In the former case it can easily be solved on the consumer side by doing all of the bookkeeping in terms of the nominating address. Is there more to it?

Yes that’s true, I could have left the rights for both the cold and hot wallet and relied on the consumer to decide whether it accepted one or the other. But I felt that was somewhat obviating the responsibility to maintain the atomic nature of the rights associated with the NFT. I strongly feel that’s the protocol’s responsibility. The NFT creator envisaged one set of rights when tokenId 3,321 was minted (for example), and any primitive that builds composability on top of that should respect that constraint (imo). So in this regard when those rights and benefits ‘bubble up’ from the cold wallet to a hot wallet they can no longer be ascribed to the cold.

To follow on from that, it also has the benefit of making integration easier (and I like things that are simple ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) ). The consumer doesn’t need to worry about ‘double spend’ of rights, as the protocol won’t allow it. It also allows the very simple ‘find and replace’ integration where instead of querying a contract for a holder’s balance you can query EPS (which is backwards compatible).

Thank you again for the feedback, it means a lot.

