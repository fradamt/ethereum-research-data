---
source: ethresearch
topic_id: 7210
title: Privacy-Preserving Distributed Contact Tracing [COVID-19]
author: sourabhniyogi
date: "2020-03-28"
category: Applications
tags: []
url: https://ethresear.ch/t/privacy-preserving-distributed-contact-tracing-covid-19/7210
views: 1587
likes: 1
posts_count: 2
---

# Privacy-Preserving Distributed Contact Tracing [COVID-19]

I was shocked to learn that several dozen Ethereum people tested positive  (or were refused testing despite being symptomatic) for COVID-19 in early/mid March – closely followed a Google spreadsheet that showed Ethereum community members with COVID-19 symptoms with a few other bits:

1. who had what symptoms [name, Twitter handle]
2. what locations people may have been infected
3. whether the person was hospitalized
4. whether the person recovered
This was a form of distributed contact tracing powered not by dapps and crypto but by public tweets and public Google Docs, but it showed a ton of personal information … so, sadly, the spreadsheet was  taken down for privacy reasons (I think …). I hope all of the people (and probably hundreds of people likely infected by the people on the sheet) have recovered and will exit from self-quarantine in the next couple of weeks.

Well, all of us are aware of China’s massive success in cutting down the reported cases through horrifying authoritarian measures. The goal is to reduce transmission of disease by bringing R0=0 or at least under 1, but in China it was done in part through by smartphone applications with zero privacy (e.g. you can’t get on public transportation without your app showing “GREEN” because its tied to national databases doing ML on everything associated with your digital identity). Singapore recently released a mobile app [TraceTogether](https://play.google.com/store/apps/details?id=sg.gov.tech.bluetrace&hl=en_US) that uses Bluetooth Low Energy (BLE) in a less authoritarian way, but still relies on a central database, and so many engineering efforts are going to follow Singapores lead in a more privacy conscious way.  An excellent summary to catch up on these effort is [Cho et al (2020)](https://arxiv.org/pdf/2003.11511.pdf)’s Contact Tracing Mobile Apps for COVID-19: Privacy Considerations and Related Trade-offs.

Well, I have spent the last few weeks working with [CoEpi](https://coepi.org) to engineer open source [iOS app](https://github.com/Co-Epi/app-ios)/[Android app](https://github.com/Co-Epi/app-android)/[server](https://github.com/co-epi/coepi-backend-go/) implementations of a “CEN protocol” (CEN=Contact Event Number, where CEN is what your phone broadcasts to others and receives from others in a Bluetooth neighborhood) to get at pretty good privacy-preserving distributed contact tracing, using elementary crypto primitives familiar to all of us.

CoEpi apps works like this, following a CEN protocol (now called TCN), in storyboard form:

1. Alex got COVID-19 at EthCC on March 5th, but he didn’t know that at the time.
2. Vitalik got within sneezing distance of Alex on March 5th at EthCC, but Sourabh did not.
3. Alex and Vitalik’s CoEpi apps are sharing CENs, but never with a server.
4. Alex finds out he has COVID-19 on March 12th and send his report to a CEN node (along with some information X), to altruistically share with all the people who know his CEN
5. Vitalik and Sourabh download potential infectors from a CEN node.
6. Vitalik finds a match on X, and might deduce that it was at THIS lat-long-time, and probably Alex, but ideally Vitalik shouldn’t know if possible.
7. Sourabh does not find a match, and nor does any government, any CEN node.
In all cases the user is under control of their altruistic report, but the goal is to not have snoopers, your contacts or the government learn much about you. The end result is reduction of disease transmission through altruistic reporting while preserving privacy, and not privacy of medical information more generally, which can be done with other means.

I encourage all of you to apply your crypto engineering skills to this pressing problem.  Now that Apple and Google have joined in, we need to hold Big Tech/Big Govt in check, while still allowing life saving activity to occur.

## Replies

**sourabhniyogi** (2020-04-23):

In case you guys missed it, Apple and Google posted their specifications on Contact Tracing:

- Contact Tracing - Bluetooth Specification
- Contact Tracing - Cryptography Specification
- Contact Tracing - Framework API
- Privacy-safe contact tracing using Bluetooth Low Energy
- Android Contact Tracing API

I was really happy to see so many groups propose similar ideas at the same time, culminating in the above which is largely a variation on



      [github.com](https://github.com/TCNCoalition/TCN)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/b/d/bd19ef70a6713126a447147ecd4ccf89afaf92cc_2_690x344.png)



###



Specification and reference implementation of the TCN Protocol for decentralized, privacy-preserving contact tracing.










Should you wish to participate in this in a technical capacity please join:

https://tcn-coalition.org/

TCN is the new name for CEN, and many groups are continuing in parallel to centralized Big Tech/Big Govt.

I have steered our group to work on social distancing:

  [![image](https://ethresear.ch/uploads/default/original/3X/f/9/f9eb09161a7ecab42d90688190e990cab0e8deb0.jpeg)](https://www.youtube.com/watch?v=NuRJQny2bu4)

