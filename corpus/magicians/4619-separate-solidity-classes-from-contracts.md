---
source: magicians
topic_id: 4619
title: Separate Solidity classes from contracts?
author: Jules
date: "2020-09-15"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/separate-solidity-classes-from-contracts/4619
views: 499
likes: 0
posts_count: 1
---

# Separate Solidity classes from contracts?

I’m suggesting that in a future version of Solidity, we explicitly separate classes from Solidity contracts.

That would mean that we could build a contract solution using 1 contract and a collection of classes.

I have written articles about Solidity class features and other Solidity foibles (in [medium.com](http://medium.com)).

In conclusion, I think it would be very useful to have useable classes similar to non-blockchain languages:

```
class X [is Y] { // non-payable
    constants
    enums
    types (I wish!)
    functions
    blah
}

contract MyContract is Z { // payable
   X x;
   blah
}
```

Any helpful comments please.
