---
source: magicians
topic_id: 5263
title: "Interesting question / idea: \"allowing a tx to only lock part of the state trie, and pay for how much each locks\""
author: jpitts
date: "2021-01-31"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/interesting-question-idea-allowing-a-tx-to-only-lock-part-of-the-state-trie-and-pay-for-how-much-each-locks/5263
views: 563
likes: 1
posts_count: 1
---

# Interesting question / idea: "allowing a tx to only lock part of the state trie, and pay for how much each locks"

Posted by [@mhluongo](/u/mhluongo) on a [Twitter thread](https://twitter.com/mhluongo/status/1355663429764313088):

> Pretty sure this was discarded years ago in the annals of Ethereum L1 design, but have we totally given up on allowing a tx to only lock part of the state trie, and pay for how much each locks?
>
>
> It’s crazy to me that every tx gets a global lock by default. Being familiar with a UTXO model, I remember I was shocked. No wonder gas is high — you should have to pay out the nose for that privilege.
>
>
> Paying for the scope of a tx’s state lock would open up more parallelizable verification, etc, but it’d also be more fair to folks who are just pushing tokens around and are only touching a single contract.
>
>
> It’d also be satisfying to see our flash loan arb friends pay for the superpower.

[@prestwich](/u/prestwich) [responded](https://twitter.com/_prestwich/status/1355682402895446020):

> there’s some movement in this direction with eip 2930. But it’s not sufficient. Stateless eth had some shakeups lately and I wouldn’t count on it being a thing for several years
