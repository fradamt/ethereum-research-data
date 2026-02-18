---
source: magicians
topic_id: 4574
title: Sharing Common Data between Solidity Smart Contracts
author: Jules
date: "2020-09-04"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/sharing-common-data-between-solidity-smart-contracts/4574
views: 924
likes: 2
posts_count: 3
---

# Sharing Common Data between Solidity Smart Contracts

I’m aiming to create an Informational EIP about Sharing Common Data between Solidity Smart Contracts.

It’s similar to the Diamond Storage part of the Diamond Standard (EIP-2535).

I would like to check whether that will adversely affect anything that anyone else is working on.

Any comments gratefully received.

## Replies

**jpitts** (2020-09-04):

It is great to have more Informational EIPs coming in!

This thread would be a good place to start collecting needs and impacts, and explore the general idea (this is why I labeled it primordial soup for now). Definitely expand on the basic idea here, and when you’re close to writing up an EIP more formally you can create a new thread within the category EIPs.

---

**Jules** (2020-09-05):

I am working on a Medium article about Smart Contracts Sharing Common Data.

Here is an illustration from that article, for a hypothetical example multi-contract solution, with a Router contract, a Producer contract and a Consumer contract:

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fa3237cd3581df105755daee37f7a8a47d1c1a0c_2_690x388.png)800×450 65.2 KB](https://ethereum-magicians.org/uploads/default/fa3237cd3581df105755daee37f7a8a47d1c1a0c)

The Router must contain the data for all smart contracts.

The subordinate contract functions are invoked by Router using delegateCall.

Each data struct is located in the Router contract, but is located at a random slot along these lines:

```auto
contract QueueDataLocation {
    function queueData() internal pure returns (QueueData storage qds) {
        uint location = uint(keccak256("queue.data.location"));
        assembly { qds.slot := location }
    }
}
```

This contract may be used as a base contract by all the contracts which need to access the data.

In the example, that is the Producer and the Consumer.

I think that this pattern for sharing common data will be very useful for many multi-contract types. That certainly includes [EIP-2535: Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535) which specifies this way of sharing data amongst the facets of a Diamond.

But I think that this technique is more general than that and deserves its own EIP.

Any comments gratefully received.

