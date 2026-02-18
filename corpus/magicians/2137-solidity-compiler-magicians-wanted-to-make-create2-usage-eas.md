---
source: magicians
topic_id: 2137
title: Solidity (compiler) magicians wanted to make CREATE2 usage easier
author: AlexeyAkhunov
date: "2018-12-06"
category: Protocol Calls & happenings > Announcements
tags: [solidity, call-to-action]
url: https://ethereum-magicians.org/t/solidity-compiler-magicians-wanted-to-make-create2-usage-easier/2137
views: 2252
likes: 3
posts_count: 4
---

# Solidity (compiler) magicians wanted to make CREATE2 usage easier

Yesterday I made this ERC20 contract (which is supposed to work under State rent when holders pay for storing their tokens): work: https://github.com/ledgerwatch/eth_state/blob/master/erc20/TokenContract.sol

As you can see in the code, Solidity provides `create2` assembly function, but working with it is cumbersome. It would be much easier if there were 2 new features in Solidity:

1. new2 operator. Similar to new, but also accept salt parameter, and uses CREARE opcode. So in my Factory I would have written Holder holder = new2(Holder, _owner) without having to put the byte code of the Holder contract inside the function
2. Function create2_address, which allows computing address of CREATE2 contract. I would have used it twice, first in Token.getHolderContract function: address payable holder_address = create2_address(factory, a, Holder), and second in Holder.setOwner function: require(create2_address(factor, _owner, Holder) == address(this))

It would be great to have (at least in a branch) a version of Solidity (derived from the current) supporting these two things. That would make further development of contracts like that much easier.

EDIT: Also linked this to: https://github.com/ethereum/solidity/issues/2136

## Replies

**jochem-brouwer** (2019-01-07):

Check this out! Should at least make your life a little bit easier! ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9) (It is a contract exposing all functions as `public` but it can of course be rewritten as a library/contract where all functions are `internal`/`private`)


      [gist.github.com](https://gist.github.com/jochem-brouwer/118ff785686742cf7fdadde9cc544cbd)




####

##### ConstantinopleTools.sol

```
/*
Copyright 2019 Jochem Brouwer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
```

This file has been truncated. [show original](https://gist.github.com/jochem-brouwer/118ff785686742cf7fdadde9cc544cbd)

---

**AlexeyAkhunov** (2019-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Check this out! Should at least make your life a little bit easier!

Thank you very much! Not exactly what I wanted, but a good start! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**efn** (2019-05-13):

Recently I also needed to implement the same thing

You can preserve a bit more of the new semantics by  doing: `new(salt) C(args...)` that will create the contract  `C` using `args` as arguments with `create2`.

The address could be accessed with `C.create2Address(salt)`

