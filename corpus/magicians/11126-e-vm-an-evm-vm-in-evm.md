---
source: magicians
topic_id: 11126
title: E=vm² - an evm vm in evm
author: high_byte
date: "2022-09-30"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/e-vm-an-evm-vm-in-evm/11126
views: 502
likes: 1
posts_count: 1
---

# E=vm² - an evm vm in evm

I have created a small proof of concept - an evm implementation that runs inside evm.

https://github.com/hananbeer/evm2

potential use case #1:

imagine you want to allow delegatecall to an arbitrary contract. but you also want to restrict that contract, e.g.:

- no selfdestruct
- no sstore to slot 0
- all subsequent calls must have 0 value
- etc.

potential use case #2:

imagine you want a new opcode. but you don’t want to go through EIP process which could take year(s) and might not pass.

so you introduce the new opcode in evm2!

*it’s a development layer on top of execution layer.*

would like to hear what the community says. open for discussion. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)
