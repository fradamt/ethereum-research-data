---
source: magicians
topic_id: 943
title: User education assessment and Experience tokens
author: ligi
date: "2018-08-03"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/user-education-assessment-and-experience-tokens/943
views: 2142
likes: 15
posts_count: 8
---

# User education assessment and Experience tokens

I was quite inspired by the imToken 2 security quiz: https://twitter.com/mr_ligi/status/1024691441115774976

Wonder now if it perhaps even would be a great idea to use the security experience tokens that the quiz generates to unlock wallet features like:

- receiving more than X
- sending more than Y
- signing transactions with data
- signing arbitrary data
- …

And perhaps also a backup could give you security experience tokens and more for the verification of the backup.

Also there could be one intentionally vulnerable faucet that can give you unlimited security experience tokens

Last but not least: I think we should build a opensource/creative commons database of such questions - unfortunately imToken is closed source so we cannot directly build on top of that. But if every wallet needs to come up with the whole set of security questions - it takes a lot of time. But if every project in this ring just contributes one question - then we already have a great base. We are already 17 Projects in this ring with even more representatives ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=9)![:love_you_gesture:](https://ethereum-magicians.org/images/emoji/twitter/love_you_gesture.png?v=9)![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9) And as often the first step is the hardest I started with the first question here:


      ![image](https://github.githubassets.com/favicons/favicon.svg)
      [github.com](https://github.com/walleth/security_quiz)


    ![image](https://avatars.githubusercontent.com/u/28189800?s=400&amp;v=4)

###



Collection of Ethereum security quiz questions. Contribute to walleth/security_quiz development by creating an account on GitHub.








When writing the second question it became even clearer how much we need a shared language / glossary between apps as we discussed once [@boris](/u/boris). E.g. shoul one call it  “seed phrase”, “mnemonic” , “12 words” , … Having different words for basically the same thing can really confuse users and also might prevent them from answering the questions in this quiz correctly

## Replies

**alexvandesande** (2018-08-03):

It’s an interesting idea, and it might have some applications but I really dislike the general idea of solving complex interfaces by better educating the user (instead of improving the UI). It doesn’t really help adoption, because most users don’t want to have to study or pass exams before using an app. You don’t need to understand about end to end encryption to use WhatsApp, or understand DNS structures to use a web browser.

---

**ligi** (2018-08-03):

Thanks for the feedback. Although I think you are correct there I also think the perfect is the enemy of the good and I have not yet seen ideas around on how to improve the UI (without compromising on core values like decentralisation) so we would not need it.

---

**alexvandesande** (2018-08-03):

I agree, as a temporary measure it could work. In terms of both security and education, it would probably be more effective than, for example, [myetherwallet.com](http://myetherwallet.com) “you must read all these slides” on boarding. It would replace them with “you must read this slide and answer correctly to unlock this feature”, which is not the ideal solution but it might be a fun temporary one for now.

---

**ligi** (2018-08-03):

true - also the timing is really important. Directly after opening the app is a really bad time as people just click these dialogs away without reading them at all. It must come sneaky and unintrusive in between and split into very small chunks. I also found these MEW dialogs really annoying - had to click them away so often …

On android I would make small SnackBars aka “Answer this one question to gain security points.”

---

**p0s** (2018-08-07):

I agree with both of regarding 1) an education assessment is an intermediate solution until 2) we have better UI that doesn’t need explanation, which should be the goal.

I would like to add that imToken/Wallet apps and MEW are fundamentally different from the user perspective and therefore would need different approaches regarding education, if at all.

MEW is ‘one-time use interface’ **vs.** wallet apps are ‘one time setup and then use’.

In MEW the education assessment therefore shows repeatedly and for experienced users **vs.** wallets, where it shows one time.

> also the timing is really important

In imToken you are able to use the app without taking the quiz, **but** with limited capabilities. When you e.g. get to the point where you want to add an additional wallet address, you will get reminded to take the quiz. Again, not optimal, but better than a popup on first app start IMO.

---

**seichris** (2018-08-08):

To 1.) better UI and 2.) restricting features to QUIZ-token holders, I would add 3.) education through games.

Having fun is a better learning environment than force. Still we’d need to force users to have fun.

The wallet app should **take new users through the app** - Force new users to make a transaction and exchange a (worthless) token. And at certain views, it explains the concept of private & public keys, etc. Users wouldn’t be able to skip the tutorial. It could be made fun, too - depending on the target group. Could be a mascot, à la Clippy, guiding users through the app. [@p0s](/u/p0s) i am sure, Chinese would love a mascot.

---

**p0s** (2018-08-09):

You can be our security mascot!

