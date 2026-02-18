---
source: magicians
topic_id: 1859
title: "Solidity-related proposal re-opened: make copy / reference semantics more explicit"
author: jpitts
date: "2018-11-09"
category: Magicians > Primordial Soup
tags: [solidity]
url: https://ethereum-magicians.org/t/solidity-related-proposal-re-opened-make-copy-reference-semantics-more-explicit/1859
views: 786
likes: 1
posts_count: 1
---

# Solidity-related proposal re-opened: make copy / reference semantics more explicit

Solidity team lead Dr. Christian Reitwiessner originally opened the issue in June, 2017 but wishes for the discussion to begin again.



      [github.com/ethereum/solidity](https://github.com/ethereum/solidity/issues/2435)












####



        opened 05:06PM - 21 Jun 17 UTC



        [![](https://avatars.githubusercontent.com/u/9073706?v=4)
          chriseth](https://github.com/chriseth)





          breaking change ![warning](https://ethereum-magicians.org/images/emoji/twitter/warning.png?v=12)


          language design :rage4:


          selected for development


          high effort


          high impact


          needs design







Implicit copy operations from storage to memory, from calldata to memory, from m[…]()emory to external function arguments, etc is not possible anymore except for value types.

To make an ordinary value copyable, use the `copyof` operator: `x` cannot be copied, but `copyof x` can be copied. Using `copyof` twice is invalid. Storing a copyable type somewhere erases the copyable property again, i.e. `uint[] memory x = copyof y; c.f(x);` is invalid.












Related tweet: https://twitter.com/ethchris/status/1060829055556206592
