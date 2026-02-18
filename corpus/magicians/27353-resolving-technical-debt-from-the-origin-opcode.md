---
source: magicians
topic_id: 27353
title: Resolving Technical Debt from the ORIGIN OpCode
author: Helkomine
date: "2025-12-29"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/resolving-technical-debt-from-the-origin-opcode/27353
views: 30
likes: 0
posts_count: 1
---

# Resolving Technical Debt from the ORIGIN OpCode

I have reviewed [EIP-2711](https://eips.ethereum.org/EIPS/eip-2711), an old proposal that has long been withdrawn, which contained a great idea that would allow us to receive funding while still maintaining the original transaction sender address. This is something that hasn’t been achievable until now (even with [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702)). I believe this is definitely something we must do if we want to make AA a first-class citizen in the future. I plan to rewrite a new EIP based on this direction, with a focus on minimizing the functionality to reduce its impact on the network. What does everyone think?
