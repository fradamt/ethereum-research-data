---
source: magicians
topic_id: 22182
title: "EIP-7840: Add blob schedule to execution client configuration files"
author: matt
date: "2024-12-12"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7840-add-blob-schedule-to-execution-client-configuration-files/22182
views: 423
likes: 7
posts_count: 8
---

# EIP-7840: Add blob schedule to execution client configuration files

Adds a new object to the EL genesis chain config:

of the shape:

```json
"blobSchedule": {
  "prague": { "target": 6, "max": 9 },
  "osaka":   { "target": 12, "max": 16},
  ...
}
```



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9129)














####


      `master` ← `lightclient:blob-config`




          opened 03:17PM - 12 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/d/d19a611f5bc5047810f500c047e648150a65aa2c.png)
            lightclient](https://github.com/lightclient)



          [+69
            -0](https://github.com/ethereum/EIPs/pull/9129/files)







Adds a new object to the EL genesis chain config:

of the shape:

```json
"[…](https://github.com/ethereum/EIPs/pull/9129)blobSchedule": {
  "prague": { "target": 6, "max": 9 },
  "osaka":   { "target": 12, "max": 16},
  ...
}
```

## Replies

**jochem-brouwer** (2025-01-06):

Is the genesis chain config specified anywhere? I don’t think it is standardized anywhere but most clients need to import the same config, so I guess this naturally evolves to some kind of standard config file?

Maybe it would be a good idea to specify these genesis / chain spec files somewhere (if this is not yet done) then additions to this config file can then be added to this specification.

---

**matt** (2025-01-06):

it isn’t defined officially anywhere AFAIK.

---

**jochem-brouwer** (2025-01-06):

I think we should spec it out. What would be a good location for this spec?

---

**matt** (2025-01-07):

It’s tough because EIPs aren’t the best suited for specs that are change regularly. We’ve gotten around this for the RPC by creating `execution-specs` repo. I think something like `genesis-specs` might be the right way. I would probably check with the ethpandaops team as they are kinda the premiere genesis creator / consumer.

---

**jochem-brouwer** (2025-01-09):

Cool, I was thinking along the same lines, something like `execution-apis` or `execution-specs` comes close but does not feel like the right place. I agree that a new repo like `genesis-specs` would be the “right” place for this. I’ll contact ethpandaops sometime in the near future about this.

---

**rjl493456442** (2025-01-24):

Is there any specific reason to define this in the chain configuration instead of hardcoding it?

The EIP states:

> Ensure there is a way to dynamically adjust the target and max blob counts per block.

However, in practice, these constants are only updated during hard forks. Coordinating a constant change without a hard fork via the configuration file is extremely challenging.

Probably we want to define different parameters for different networks?

---

**matt** (2025-01-24):

In particular, we want the ability to test different blob counts on test networks. If we hard code it, it’s quite difficult to try different configurations across clients.

