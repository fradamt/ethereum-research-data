---
source: magicians
topic_id: 15216
title: "EIP-7406: Multi-Namespace Onchain Registry"
author: zihaoccc
date: "2023-07-26"
category: EIPs
tags: [ens, registry]
url: https://ethereum-magicians.org/t/eip-7406-multi-namespace-onchain-registry/15216
views: 1802
likes: 1
posts_count: 9
---

# EIP-7406: Multi-Namespace Onchain Registry

This EIP proposes a universally accepted description for onchain registry entries with support for multi-namespaces, where each entry is structured as a mapping type. The multi-namespace registry enables the storage of a collection of key-value mappings within the blockchain, serving as a definitive source of information with a traceable history of changes. These mapping records act as pointers combined with onchain assets, offering enhanced versatility in various use cases by encapsulating extensive details. The proposed solution introduces a general mapping data structure that is flexible enough to support and be compatible with different situations, providing a more scalable and powerful alternative to current ENS-like registries.

Blockchain-based registries are fundamental components for decentralized applications, enabling the storage and retrieval of essential information. Existing solutions, like the ENS registry, serve specific use cases but may lack the necessary flexibility to accommodate more complex scenarios. The need for a more general mapping data structure with multi-namespace support arises to empower developers with a single registry capable of handling diverse use cases efficiently.

The proposed multi-namespace registry offers several key advantages:

- Versatility: Developers can define and manage multiple namespaces, each with its distinct set of keys, allowing for more granular control and organization of data. For instance, single same key can derive as different pointers to various values based on difference namespaces, which a namespace can be specified as a session type, if this registry stores sessions, or short URL → full URL mapping is registry stores such type of data.
- Traceable History: By leveraging multi-namespace capabilities, the registry can support entry versioning by using multi-namespace distinct as version number, enabling tracking of data change history, reverting data, or data tombstoning. This facilitates data management and governance within a single contract.
- Enhanced Compatibility: The proposed structure is designed to be compatible with various use cases beyond the scope of traditional ENS-like registries, promoting its adoption in diverse decentralized applications.

https://github.com/ethereum/EIPs/pull/7406

## Replies

**SamWilsn** (2023-08-22):

As a non-editorial comment, do you think it would be useful to split the “ability to set a key” from the “ability to change the owner of a key” into two separate roles? Something along the lines of approvals from ERC-20 tokens.

---

**zihaoccc** (2023-08-22):

[@SamWilsn](/u/samwilsn) yes, I think it is a great idea and valuable suggestion, for split more roles with extensional flexibility to fulfil different case is the motivation we propose this EIP, to supply a general enough registry to adapt different use cases.

Based on your suggestion which inspired me, that we might can have even more roles to enhance the ability of management on the registry with hierarchical control.

for example, maybe we can have something like this:

```auto
modifier authorization(bytes32 node) {
        address owner = records[node].owner;
        require(owner == msg.sender || authorized[owner] ||
                    approver[node] || registrar[node] || );
        _;
}
```

---

**mengshi.zhang** (2023-08-22):

[@SamWilsn](/u/samwilsn) Thank you for the comment and the suggestion is very inspirational!

In our design, “ability to set a key” is a special case of “ability to change the owner of a key” (e.g., the original owner is NULL), however, this proposed split can help us to achieve finer-granularity of registry control ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**dongshu2013** (2023-09-01):

Loved this proposal! We are building a on-chain service network where user can subscribe difference services on-chain, and are looking for this two-layer registration structure for the service registry(namespace => service type, key => service entity). This seems to be a perfect fit for us, let’s definitely talk more to see how we can push forward the standard!

---

**dongshu2013** (2023-09-01):

one more question: since the resolver follows the same spec of EIP-137, it only takes key as input, which means it has no context of the namespace. It’s ok if each namespace have independent resolver, but considering the case where one resolver serving multiple namespaces, the current interface will not sufficient. Should we update the resolver interface as well in this case?

---

**mengshi.zhang** (2023-09-01):

Thank [@dongshu2013](/u/dongshu2013) for the great suggestion! Yes, we should make a new proposal to extend EIP-137 and build a more generic resolver.

---

**zihaoccc** (2023-09-01):

This is a good point. In the current specification defined in EIP-137, there is a limitation when it comes to resolving with a namespace included as part of the input alongside each key. For the existing EIP-137 resolver, we have two potential approaches to address this issue:

1. We could enhance the resolver’s interface implementation to support namespace resolution. However, this approach may not provide a generalized solution and might lack elegance in its design.
2. Alternatively, we could design specific resolvers for each individual namespace. However, this approach may not be versatile enough and could result in less elegant designs.

We are eagerly looking forward to the acceptance of this EIP, as it will pave the way for proposing another EIP to extend new resolver specification that can effectively handle namespaces. Your valuable feedback on this matter is greatly appreciated.

---

**Yuan** (2023-09-02):

I’m thrilled to come across this proposal, which aligns perfectly with our current use case. It involves implementing a graphical connection mapping, where each entry has its own stack and is leveraged by different namespaces. This approach sets it apart from ENS-like registries, as all data is organized in a tree structure inheriting from a single root node. This stack-like structure is versatile and can be applied in various scenarios.

Introducing the multi-authorizer, as mentioned earlier, could potentially elevate this EIP to a wider scope. I’m eagerly anticipating an offline discussion to explore possible collaboration opportunities.

