---
source: magicians
topic_id: 2269
title: "[WhiSpeG] Summary on current Whisper UseCases"
author: Ethernian
date: "2018-12-20"
category: Working Groups > Ethereum Architects
tags: [whisper]
url: https://ethereum-magicians.org/t/whispeg-summary-on-current-whisper-usecases/2269
views: 878
likes: 0
posts_count: 1
---

# [WhiSpeG] Summary on current Whisper UseCases

## Summary

One week ago I had a call with [@atoulme](/u/atoulme) about Whisper UseCases.

The idea of the call was to break various UseCases apart up to particular requirements and map it to Whispers features (either existing or desired). Unfortunately, we have not found a lot of new UseCases and they are not understood and specified with all the details. Therefore requirements for some general purpose messaging system like Whisper are still quite unsharp.

Here are my personal summary of discussions and readings last time.

### Secure Messaging for Social Networks

This is usual and most defined UseCase. This [classic paper](https://www.google.de/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwjgxr-Coa_fAhWwp4sKHZmDCOUQFjAAegQICRAC&url=http%3A%2F%2Fcacr.uwaterloo.ca%2Ftechreports%2F2015%2Fcacr2015-02.pdf) provides great review of many aspects and features of secure messaging in general.

Status.IM Team works hard on developing of next generation messaging protocol and published some interesting [works](https://status.im/research/whisper_pss.html) and [link collection](https://github.com/status-im/awesome-secure-messaging).

Looks like most developers (both Status and EF) consider current limitations are more in protocol itself than in its specification.

### Secure Messaging for Machine Communications

There is an UseCase about Messaging for Network Configuration.

Nodes joining and leaving permissioned network need some kind of secure messaging for it.

[CANTO proposal](https://ethereum-magicians.org/t/canto-a-scalable-blockchain-system-interconnect-model/2203) will need some messaging on the top of `devp2p/RLPx` to broadcast network changes.

Whisper fits requirements of this UseCase not in the best way, because Whisper’s PoW-based anti-spam protection is in trade-off with guaranteed delivery, which is much needed.

### Conclusions

A native ethereum messaging is much required for interconnect between corporate networks behind firewalls, because connection from ethereum node to an external messaging service (like rabbitMQ) is fragile and opening additional ports is a pain.

Looks like the Whisper adoption (as the native ethereum messaging stack) stucks not on missing specification but more on gap between UseCase requirements and implemented set of features.

Current research on Secure Messaging brings set of trade-offs, but no single universal solution suitable for all UseCases. It means the native ethereum messaging should offer more flexibility among trade-offs than current Whisper implementation to fit different UseCases.

Research on possible UseCases is quite important and should be done first. I would look for new UseCases and for requirements on [ethresear.ch](https://ethresear.ch).

Any objections and critic are welcome.
