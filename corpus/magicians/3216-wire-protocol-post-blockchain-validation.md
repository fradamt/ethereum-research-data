---
source: magicians
topic_id: 3216
title: Wire protocol post blockchain validation
author: dominic
date: "2019-04-29"
category: Magicians > Primordial Soup
tags: [light-client, networking]
url: https://ethereum-magicians.org/t/wire-protocol-post-blockchain-validation/3216
views: 1357
likes: 1
posts_count: 1
---

# Wire protocol post blockchain validation

Hi Guys in this group,

reading through the different proposals I would like to propose to split the discussion of

1. Constrained Blockchain Validation algorithms such as FlyClient and our own BlockQuick and
2. The wire protocol used after the blockchain has been validated.

While I believe that the discussion will go on for some time for 1), the 2nd question could quicker lead to alignment within the community. And different blockchain validation schemes could still use the same wire protocol.

Just probing for interest in the community here. We’re working on a protocol already to define requests and responses. But I imagine other constrained protocols will have similar needs.

Primarily this is to retrieve block information, account balance & state information. Many of these commands exist semantically already in [ethereum RPC](https://github.com/ethereum/wiki/wiki/JSON-RPC) majorly missing is though the transport of **corresponding merkle proofs.** For constrained protocols it’s going to be inevitable to retrieve merkle proofs together with any account information. There is an EIP for [ethereum RPC,](https://github.com/ethereum/EIPs/issues/1186) but I’m not aware of a standardization of constrained devices.

Furthermore what is the communities stance on light clients fetching contract variable values. E.g. you want to inspect a contract state value that is in a **variable such as a map[mykey] => value.** As an “eth_call” is not trustable, we use state fetching and merkle proofs directly to read variables from account state, but it means we hard-code Solidity semantics about how and where maps are serialized. Any thoughts on best practices here?

Another open question here. What data formats are you guys using for communication? What were the considerations?

As for us as we have been **prototyping with json rpc via raw tls** - but because of the binary encoding overhead are thinking of format that is keyless and can do binary natively. E.g. **ASN1** is an alive candidate for us since all our targeted microchip based devices have within their TLS implementation already an ASN1 parser on-board but usually not much else.

Best
