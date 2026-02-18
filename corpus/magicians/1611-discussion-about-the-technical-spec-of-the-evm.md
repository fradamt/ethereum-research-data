---
source: magicians
topic_id: 1611
title: Discussion about the technical spec of the EVM
author: jpitts
date: "2018-10-18"
category: Magicians > Primordial Soup
tags: [evm]
url: https://ethereum-magicians.org/t/discussion-about-the-technical-spec-of-the-evm/1611
views: 1006
likes: 2
posts_count: 3
---

# Discussion about the technical spec of the EVM

[@CJentzsch](/u/cjentzsch) tweeted about this important issue, and several people commented.



      [twitter.com](https://twitter.com/ChrJentzsch/status/1052509763433422851)



    ![image](https://pbs.twimg.com/profile_images/856774253252927489/32OUVL9K_200x200.jpg)

####

[@ChrJentzsch](https://twitter.com/ChrJentzsch/status/1052509763433422851)

  One of the strong safeguards of #Ethereum was/is one complete technical specification: The yellow paper. This virtue should be upheld and it should always be updated *first*. Every consensus relevant EIP should have a PR to the yellow paper including the full specification of it.

  https://twitter.com/ChrJentzsch/status/1052509763433422851










Initially the discussion focused on barriers to participation due to lack of formal background required to work on the Yellow Paper. [@Arachnid](/u/arachnid) commented:

https://twitter.com/nicksdjohnson/status/1052519469782880256

At one point [@cdetrio](/u/cdetrio) mentioned the [Jello Paper.](https://jellopaper.org/), “Human Readable Semantics of EVM in K”:



      [twitter.com](https://twitter.com/cdetrio/status/1052635819998109696)



    ![image](https://pbs.twimg.com/profile_images/1277181658/nsibidi_200x200.jpeg)

####

[@cdetrio](https://twitter.com/cdetrio/status/1052635819998109696)

  @ChrJentzsch @nicksdjohnson The Jello paper is quite readable. Its generated from KEVM, which is an executable spec with comments. It can execute the consensus test suite, so just hit enter to cross-check for correctness. https://t.co/lS28XH20Fj

  https://twitter.com/cdetrio/status/1052635819998109696










Do I hear the sound of a a ring forming?

https://twitter.com/greg_colvin/status/1052698448217235456

## Replies

**jpitts** (2018-10-19):

Here is a related comment on reddit. I am interested in why [@maciej](/u/maciej) believes the spec is “from EF”.

> This is not a quality issue, it’s a communications issue. Parity is a 3rd party following technical specification from EF, we are less involved in writing it than Geth team is. The end result is that there might be hidden assumptions in the spec that not everyone outside of people involved in writing it are aware of. That’s just the nature of things, writing complex software is hard, writing technical specification for complex software is hard. That’s why we have a test net.

https://www.reddit.com/r/ethereum/comments/9onsei/parity_208stable_critical_constantinople_bug_fix/e7x6p96/

---

**maciej** (2018-10-19):

I honestly haven’t looked into the Ropsten issue much, and based my response there over a casual conversation I had over lunch. Thanks for clarifying things on Reddit!

