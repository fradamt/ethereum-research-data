---
source: ethresearch
topic_id: 4584
title: Analysing contract permissions using symbolic analysis and decompiled sources - example
author: kolinko
date: "2018-12-14"
category: EVM
tags: []
url: https://ethresear.ch/t/analysing-contract-permissions-using-symbolic-analysis-and-decompiled-sources-example/4584
views: 1417
likes: 0
posts_count: 1
---

# Analysing contract permissions using symbolic analysis and decompiled sources - example

Hi all,

We just hacked a proof of concept tool for finding addresses that are being referenced by a smart contract: https://showme-1389.appspot.com/

It uses API from the [eveem.org](http://eveem.org) symbolic decompiler to figure out stuff like this:

[![15](https://ethresear.ch/uploads/default/optimized/2X/3/3cd3153dcf48ef88bc796abc85ddff023400689c_2_690x419.png)151944×1182 342 KB](https://ethresear.ch/uploads/default/3cd3153dcf48ef88bc796abc85ddff023400689c)

If anyone’s interested in how it’s done, you can check the github for sources, and also the intermediate language form that is the basis for the analysis, available here:

http://eveem.org/code/0x06012c8cf97bead5deae237070f9587f8e7a266d.json
