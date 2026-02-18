---
source: magicians
topic_id: 14751
title: Proposal to configure relay builder endpoints in validator clients
author: mxs
date: "2023-06-20"
category: Magicians > Primordial Soup
tags: [validation]
url: https://ethereum-magicians.org/t/proposal-to-configure-relay-builder-endpoints-in-validator-clients/14751
views: 583
likes: 3
posts_count: 2
---

# Proposal to configure relay builder endpoints in validator clients

*This is just a topic to gauge interest / ideas before maybe drafting an EIP, all ideas are welcome.*

As of today, the relay builder endpoints are configured at the beacon level which means that all validation keys managed by a beacon use the same builders. This is unfortunate if you want to have fine-grain selection of relay builders as it implies to duplicate your infrastructure with the combination of configurations you want to support.

Examples of use-cases:

- testing an experimental relay builder on some specific validation keys,
- have some validation keys use ofac/non-ofac relay builders,
- …

It’d be convenient for those cases to be able to specify the relay builder endpoint to be used at the validator client level in the proposer config of the key. For instance:

```auto
proposer_config:
        # Local build (no change)
        0xa1d1ad0714035353258038e964ae9675dc0252ee22cea896825c01458e1807bfad2f9969338798548d9858a571f7425c:
          fee_recipient: 0x15f4b914a0ccd14333d850ff311d6dafbfbaa32b
          builder:
            enabled: false
        # Relay build (new optional relay setting)
        0xb2ff4716ed345b05dd1dfc6a5a9fa70856d8c75dcc9e881dd2f766d5f891326f0d10e96f3a444ce6c912b69c22c6754d:
          fee_recipient: 0x15f4b914a0ccd14333d850ff311d6dafbfbaa32b
          builder:
            enabled: true
            endpoint: "..." # Relay to use for this key
        0x8e323fd501233cd4d1b9d63d74076a38de50f2f584b001a5ac2412e4e46adb26d2fb2a6041e7e8c57cd4df0916729219:
          fee_recipient: 0x15f4b914a0ccd14333d850ff311d6dafbfbaa32b
          builder:
            enabled: true
            endpoint: "..." # Relay to use for this key
```

In this example, blocks proposed by the second and third validation keys would go to the specified relay builder endpoint. If no specific endpoint is set, the beacon would use its current configured relay endpoint (so it would be backward compatible with existing setups).

Such a change would require the following:

- In the Beacon-API, /eth/v1/validator/prepare_beacon_proposer to support the optional endpoint field (so, validators and beacons to be updated),
- Whenever a block is to be proposed using a builder, the beacon will now need to use the corresponding builder endpoint for the key, or fallback to its default endpoint.

Possible alternatives:

- implement the key<>relay mapping in dispatch relay builders such as MEV-boost, this result in a more complex management (as you need to properly keep in sync your validator config with your MEV-boost config),
- go one step further and to specify a list of relay builders at the validator client level, beacons would pick the best proposal out of the list, this would simplify infrastructure setups as there wouldn’t be a need to use MEV-boost to use multiple relay builders,
- your cool idea here.

## Replies

**ManuNLP** (2023-06-20):

A previously (closed) MEV-boost PR about this topic, where the `pubkey: relays` mapping was done directly into MEV-boost: https://github.com/flashbots/mev-boost/pull/186

