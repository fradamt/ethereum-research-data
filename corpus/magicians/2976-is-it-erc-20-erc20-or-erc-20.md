---
source: magicians
topic_id: 2976
title: Is it ERC-20, ERC20 or ERC 20?
author: fulldecent
date: "2019-03-24"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/is-it-erc-20-erc20-or-erc-20/2976
views: 825
likes: 3
posts_count: 2
---

# Is it ERC-20, ERC20 or ERC 20?

Let us canonicalize the references for EIPs. They are inconsistently referred to as EIP-123 and EIP123 in the EIP documentation as well as the EIPs themselves. Another option is EIP 123.

Original issue: https://github.com/ethereum/EIPs/issues/1464

The end-user public is increasingly exposed to technical details like EIP numbers. I hope we can please come to a consensus on this issue and use it consistently in the EIP repo. This is the same process we went through to standardize on using the [eips.ethereum.org](http://eips.ethereum.org) URLs instead of the GitHubs URLs (see https://github.com/ethereum/EIPs#preferred-citation-format).

I’m not asking you to do any work. Just please confirm if there is appetite here to make this change, and if we can be happy with one consistent format. I will then use this mandate to:

1. Make a PR which fixes the EIPs repository (other than the actual EIPs) this requires EIP editor signoff
2. Make PRs against individual EIPs to use this consistent format, and request they accept the change

## Replies

**jpitts** (2019-03-24):

I believe that it should have a dash in the name, for accuracy, readability, and for convenient tagging. Typically when I see a post in this forum that appertains to an ERC or EIP I will add EIP-XXX / ERC-XXX in front of the title, as well as tag it with the same, but lower-cased.

