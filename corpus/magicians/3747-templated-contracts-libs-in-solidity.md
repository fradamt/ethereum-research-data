---
source: magicians
topic_id: 3747
title: Templated contracts/Libs in Solidity?
author: Amxx
date: "2019-11-02"
category: Magicians > Tooling
tags: [solidity]
url: https://ethereum-magicians.org/t/templated-contracts-libs-in-solidity/3747
views: 1317
likes: 0
posts_count: 4
---

# Templated contracts/Libs in Solidity?

Hello,

While solidity native constructions like mapping and arrays are good enough for most use-cases, the inability to search an array in constant time, and the inability to traverse are mapping, are sometimes critical to smart contract developers. Combining the two into a richer structure trades compuation for storage. This trade might not be effective to everyone, but it is sometime necessary.

This thing is, many people are writting such structures, are re-use is limited by the specialisation of the type (are you considering structure containing bytes32? addresses? bytes4?). We could ask the devs to cast all inbound/outbound values, but that raises other issues.

In order to stop having duplicates of my structure in each an everyone of my projects, I made a [dedicated package](https://github.com/Amxx/SolStruct) with code for sets (searchable list without duplicate) and map (traverseable key-value store). The “templating” is achieved using `sed` for text replacement … which is working but limited to natural types as it is not (yet?) smart enough to add `memory`/`calldata` where needed.

I’ll continue developping this repo, and everyone is free to contribute, but I think at some point this should be part of either the solidity langage or some recognised package like openzeppelin.

Is there any similar effort I might have missed? Have templated structs/contracts/libraries ever been considered in solidity?

## Replies

**axic** (2019-11-04):

> Is there any similar effort I might have missed? Have templated structs/contracts/libraries ever been considered in solidity?

I suggest to open one or more issues on [GitHub - ethereum/solidity: Solidity, the Smart Contract Programming Language](https://github.com/ethereum/solidity) explaining what features you are missing. By searching open issues you may also find that some of them could be already under discussion. (There definitely is an issue about templates.)

---

**serapath** (2019-11-12):

Would you consider adding a README.md to your repository with an example and the rational behind it?

Maybe we can add you to https://smartcontract.codes ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) We are right now in the process of finishing our next release and that includes categories for popular libraries or contracts or generally just recommended ones so people can discover cool templates to re-use or at least learn from.

---

**Amxx** (2019-11-15):

I’m thinking of refactoring it … but I’ll push a readme next week anyway

