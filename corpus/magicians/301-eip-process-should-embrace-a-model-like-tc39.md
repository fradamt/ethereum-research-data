---
source: magicians
topic_id: 301
title: EIP process should embrace a model like TC39
author: backus
date: "2018-05-07"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/eip-process-should-embrace-a-model-like-tc39/301
views: 1984
likes: 2
posts_count: 3
---

# EIP process should embrace a model like TC39

The web browser world has been dealing with similar problems forever. If a certain API is introduced that people depend on, it is hard to replace it. The [smoosh vs. flatten](https://github.com/tc39/proposal-flatMap/pull/56) debate is a perfect example.

Still, I think the web standards world has figured out a good middle ground. Plenty of companies were created when ES5.1 was the standard that died before ES6 was fully supported by browsers.

Deciding on the right web standards is similar to deciding on the right standards for the Ethereum community. The fact that standards have to be adopted by many different browser vendors is very similar to new standards needing to be adopted by many different wallets.

The web community has two obvious practices that I think are valuable to consider:

- TC39 defines stage-0 through stage-4 with criteria for moving between each stage. The standards committee can take their time to get to stage-4 while also signaling to people that the risk profile of prematurely adopting something has changed now that it has transitioned from stage-1 to stage-2, for example.
- Browsers expose features early, often with vendor prefixes before they are ready. For example, before transition was fully adopted, people could use -o-transition, -webkit-transition, and -moz-transition

Browsers can expose some functionality early and let people polyfill the JS functionality they want early. You can decide whether you want to go with `babel-preset-2` or `babel-preset-3` depending on what level of potential breakage you are willing to tolerate. You can transpile your CSS using `autoprefixer` and use `browserslist` to specify what level of compatibility you want (so elegant too! `"browserslist": ["> 1%","IE 10"]`)

---

For proposals that are unclear from a security perspective, I think it totally makes sense to say that no one should adopt it until that hurdle is cleared. Otherwise though, the community should embrace the fact that some companies may want to adopt EIPs that are effectively in `stage-1`.

How long do we expect startup companies building on Ethereum to last? If they don’t have a product that totally takes off in ~4 years, I think it is normal for people to lose interest by then. How long does it take to get an EIP accepted as a draft? Accepted? If it takes 6 months for an EIP to go from proposed to OK to use in production, that means a company built on Ethereum might generously last for 8 EIP cycles until it effectively starts dying if it isn’t a success.

I think the Ethereum community will be in a better place in a few years if the EIP process adopts stages and wallets expose vendored functionality (`metamask__signTypedData`) when appropriate. A lot of valuable information is gained by putting functionality in front of users earlier.

---

This isn’t supposed to be a specific plan of action, but instead a perspective that I don’t think is expressed as frequently in the Ethereum world. Excited to hear what others think ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9)

## Replies

**fulldecent** (2018-05-20):

[@backus](/u/backus) Thanks for sharing. I support adding an additional stage. This stage, is implemented in a pure-play pull request:

- Pull request: https://github.com/ethereum/EIPs/pull/1100
- Discussion: Add two-week review to EIP process [MERGEABLE]

---

**Ethernian** (2018-09-29):

[@backus](/u/backus), [@fulldecent](/u/fulldecent)

Are you in Prag and go to [EIPs & Ecosystem Standards](https://hackmd.io/s/ByIVnZVdX#13-EIPs-amp-Ecosystem-Standards) discussion?

Your opinion and experience will be much needed!

