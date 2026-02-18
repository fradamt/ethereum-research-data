---
source: magicians
topic_id: 3095
title: Tokens and NFTs that are more under control of owner accounts + design improvements for state fees, ETH2
author: boris
date: "2019-04-05"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/tokens-and-nfts-that-are-more-under-control-of-owner-accounts-design-improvements-for-state-fees-eth2/3095
views: 1044
likes: 7
posts_count: 5
---

# Tokens and NFTs that are more under control of owner accounts + design improvements for state fees, ETH2

I’ve talked for a long time about writing a blog post called “Tokens live in your wallet and other lies”. ERC20 and ERC721 NFTs are centrally deployed and controlled contracts that store how many tokens are in each user address, centrally.

There was a post:

https://twitter.com/bmann/status/1113925091350523904

And then there were MANY follow up posts and short Twitter misunderstandings. But also lots of interest!

Also, [@expede](/u/expede) was on a plane #whenDoesBrooke land.

https://twitter.com/MuteDialog/status/1113933676465750019

But we think that yes, we can have tokens and NFTs that are more directly “owned” by individual accounts.

https://twitter.com/expede/status/1113944738967605248

https://twitter.com/expede/status/1113947040344461312

> ### “Ethereum is fundamentally an event stream, not a reified DB aggregate”

Some of this thinking may cause us to make different choices about how to construct accounts and tokens in ETH2. Some of them may evolve on ETH1 because of state fees, where we can learn and make some use cases easier / better / more secure in ETH2 – either at the VM layer or elsewhere within the protocol.

Now, there is this long form thread. And eventually #BrookeWillLand.

Please do continue to share links and info. [@Arachnid](/u/arachnid) [@fubuloubu](/u/fubuloubu) [@maurelian](/u/maurelian)

## Replies

**Arachnid** (2019-04-05):

I’m still not sure what you’re getting at here. Why does it matter where the user’s balance is stored? What matters are the rules under which the balance can be modified, and how those rules are defined - and you can set any rule set you want regardless of where the balance is.

---

**maurelian** (2019-04-05):

ya… even bitcoin isn’t ‘in’ the wallet. But, goodnight.

---

**expede** (2019-04-05):

FWIW I agree with you! I really don’t care where the token is stored in a data structure. The idea here is more about breaking up tokens for state rent, and giving users hooks to further control the actions of their funds. All of this is possible today, but all of the metaphors are broken, which lead to many end users misunderstanding how things work, what they have control over, and so on.

---

**expede** (2019-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> #whenDoesBrooke

Hello from my Amsterdam layover ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

