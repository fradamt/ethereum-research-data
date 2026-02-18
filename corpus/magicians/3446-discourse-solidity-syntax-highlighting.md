---
source: magicians
topic_id: 3446
title: Discourse Solidity syntax highlighting
author: abcoathup
date: "2019-07-05"
category: Magicians > Site Feedback
tags: []
url: https://ethereum-magicians.org/t/discourse-solidity-syntax-highlighting/3446
views: 958
likes: 1
posts_count: 1
---

# Discourse Solidity syntax highlighting

Is Ethereum Magicians using Solidity syntax highlighting?

What did you use?

If not, then on the Zeppelin community forum we are using the following:


      ![image](https://us1.discourse-cdn.com/flex022/uploads/zeppelin/optimized/3X/3/5/354421cb667d85bfdc0ea6bf3fc1350fb8d014e4_2_32x32.png)

      [OpenZeppelin Forum – 27 Jun 19](https://forum.openzeppelin.com/t/discourse-solidity-syntax-highlighting/267/11)



    ![image](https://us1.discourse-cdn.com/flex022/uploads/zeppelin/original/1X/1b0984d7ee08bce90572f46a1950e1ced436d028.png)



###





          General





          Meta






I have installed the custom theme-component and enabled on the Light and Dark Theme.    We now have Solidity syntax highlighting.  pragma solidity ^0.5.0;  import "openzeppelin-solidity/contracts/token/ERC721/ERC721Full.sol"; import...










```auto
pragma solidity ^0.5.0;

import "openzeppelin-solidity/contracts/token/ERC721/ERC721Full.sol";
import "openzeppelin-solidity/contracts/drafts/Counters.sol";

contract GameItem is ERC721Full {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721Full("GameItem", "ITM") public {
    }

    function awardItem(address player, string memory tokenURI) public returns (uint256) {
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(player, newItemId);
        _setTokenURI(newItemId, tokenURI);

        return newItemId;
    }
}
```
