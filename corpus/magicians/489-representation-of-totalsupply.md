---
source: magicians
topic_id: 489
title: Representation of totalSupply
author: paulhauner
date: "2018-06-01"
category: Working Groups > Security Ring
tags: []
url: https://ethereum-magicians.org/t/representation-of-totalsupply/489
views: 933
likes: 0
posts_count: 4
---

# Representation of totalSupply

During security reviews, a colleague and I have a bit of an ongoing discussion about how `totalSupply` should be represented when an owner can mint tokens at any time. Consider the following example code (it’s not supposed to be functional):

```
uint crowdsale = 5;
uint mintable = 5;
uint minted;
uint bought;
...
function buy() payable public duringCrowdsale {
    tokens = msg.value;
    bought += tokens;
    require(bought <= crowdsale);
    balanceOf[msg.sender] = tokens;
    ...
}

function mint(uint _count) onlyOwner {
    minted += _count;
    require(minted <= mintable);
    balanceOf[owner] = _count;
    ...
}
...
```

If all available tokens were purchased during the crowdsale but none have been minted, should `totalSupply` be 5 or 10?

One side says it should be 5 because the tokens don’t exist until `mint()` is called. The other says it should be 10 because that’s how many can be transferred at any time.

Keen to hear opinions, other resources, or a better place to post this.

## Replies

**MicahZoltu** (2018-06-01):

Many tokens that support minting allow for unbounded minting of tokens, sometimes via some economic incentivization system.  For all of these, the only value that *can* be displayed is the number of tokens *currently* minted.  Even ETH falls into this category, where there are not a fixed number of tokens that will ever be minted.

I suspect that this is significantly more common than a token that can mint a bounded number of tokens, which is why I think it is most reasonable to say that `totalSupply` means number of minted tokens right now.

That being said, in this very specific example I would probably have `totalSupply` be 10.  Though really I would question why this token exists, it feels like the owner should have just minted themselves `10` tokens from the start.  Perhaps there is more context in a real world example, but in this example I feel like the contract is just silly and shouldn’t be catered to.

---

**paulhauner** (2018-06-01):

My stance is that if the token is advertised as “decentralised”, then the total supply should be 10. Otherwise, it’s up to the owner as to what total supply should be.

I agree the concept is silly (which is pretty much a direct result of being in the “10 camp”). However, I’ve seen this pattern several times, I think it’s done for optics. What I’m trying to say is that I didn’t make this up as a thought experiment, it’s something I am dealing with currently and it’s useful to have additional input (so, thank you ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9))

---

**MicahZoltu** (2018-06-01):

Personally, I would label such a coin as a scam coin and just not deal with it if you have that choice.  If you don’t have the choice, then `10` is probably the best service you can provide to your users.

