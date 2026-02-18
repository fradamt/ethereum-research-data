---
source: ethresearch
topic_id: 17538
title: Privacy and Regulation in our decentralized future
author: JiangXb-son
date: "2023-11-27"
category: Privacy
tags: [layer-2]
url: https://ethresear.ch/t/privacy-and-regulation-in-our-decentralized-future/17538
views: 5712
likes: 19
posts_count: 32
---

# Privacy and Regulation in our decentralized future

In this post, I want to figure out: what privacy should be built.


      ![](https://ethresear.ch/uploads/default/original/2X/3/32f2c2579dd4c41c2ec5bf2227cb15da0bb80b26.png)

      [HackMD](https://hackmd.io/@sin7y/rJ_ZY3-rT)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd231863ebeb783c60343a8e1e943178c5cb44c7_2_690x362.jpeg)

###



During DevConnect Istanbul, I had the privilege of engaging with various project teams and researchers dedicated to privacy-oriented initiatives. We discussed a range of privacy-related topics. To my surprise, I found that the concept of ‘privacy’ is...










Please don’t hesitate to leave your thoughts, thanks.

## Replies

**MicahZoltu** (2023-11-27):

You start with the assumed premise that “privacy regulations” will stop crime and/or usage of the proceeds from crime.  However, all of the evidence we have of the last 50+ years of attempts to curb crime in this way results in zero evidence that this works at all.  Even with the most draconian financial surveillance systems in place, criminal behavior does not appear to be impacted.

While I suspect many/most would agree that it would be great if we could stop bad people from doing bad things, we should not be falling into the same trap that prior financial systems have fallen into where it is assumed (without any evidence) that stopping crime is as easy as controlling who has access to money.

The only thing that KYC has done in the legacy financial system is to prevent honest users from engaging with the financial system and creating regulatory moats for established participants.

If you want to pursue this course of research, I recommend first showing evidence that financial surveillance has a significant positive impact on crime reduction, and then showing that that positive impact outweighs the negative impact caused by side effects of financial surveillance systems.

---

**JiangXb-son** (2023-11-28):

Thanks for your kind reply. I believe the main point I want to convey is not to “stop” the crime but to “catch” the crime. Crime will always exist in this world whether it’s web2 or web3, the only thing we want to do is that when crime happens, how can we reduce losses as soon as possible? This is the real problem I want to solve.

---

**MicahZoltu** (2023-11-28):

KYC has no evidence of catching criminals in any significant amount either.  It is at most a nuisance to criminals.  I still recommend as a first step you show that some form of financial surveillance has significantly impacted the rate at which criminals are caught (which would also impact the rate at which crime is committed) and compare that against the costs to society for that financial surveillance scheme.

Recent history is littered with attempts to solve the crime problem through financial surveillance, so if KYC actually helps you should be able to find data to support the claim!

The thing to remember is that any financial surveillance scheme you concoct can be worked around.  You should not assume that criminals will do the exact same thing in the face of novel tracking/detection methods.  When TradFi implements KYC, criminals simply hire, kidnap, or scam people so they have many bank accounts that they can withdraw from.  This is annoying, but it is effective at breaking financial surveillance schemes designed to stop them from using their illicit funds.  Meanwhile, legitimate users suffer all of the costs of these financial surveillance schemes and many honest users get caught up in the crossfire.

---

**JiangXb-son** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> financial

Yeah, I definitely agree with you. I don’t think KYC could reduce the crime rate as well. This is also my view, and I believe I give similar thoughts on it in the post.

Could you tell me which part makes you get this meaning? I would try to fix it.

---

**MicahZoltu** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/jiangxb-son/48/8193_2.png) JiangXb-son:

> Could you tell me which part makes you get this meaning? I would try to fix it.

Pretty much the entire article is based on the premise that financial surveillance actually solves something.

I think the most direct statement to this effect is this:

> for privacy-focused projects, irrespective of their design, it is imperative to ensure that regulatory bodies/organizations can pinpoint the target without additional information. Otherwise, it could be extremely dangerous.

You are lobbying for financial surveillance, without first showing that financial surveillance will actually fix the problem.  This is the strategy that basically every regulator for the past 50+ years has taken, where they assume financial surveillance will allow them to seize stolen assets, so they introduce financial surveillance regulations, and then those regulations fail to put a meaningful dent in recovery of stolen assets.

To put it another way, you have a problem statement along the lines of:

> Problem: People acquire money through criminal activity, and they use various tools to launder that money, and some of these tools involve blockchains.

And you have a proposed solution along the lines of:

> Solution: Regulate who can and cannot transact.

What you need to do is show how the solution actually addresses the problem.  Many people believe that it is “obvious” that this particular solution will solve the above problem, but historically it has never actually worked.  The real world is a whole lot more messy than on paper, and criminals will find the most clever ways to get around your solution, whatever it is.

---

**PhilipEriksson** (2023-11-28):

I disagree with this (Do note that I am part of the same team as the author for context). The article does not imply or insinuate that the solution aims for any form of “financial surveillance”. What is the exact definition/interpretation of “financial surveillance” in your view?

We are suggesting a scheme where encrypted data can be traced in a completely decentralized system, where users can opt in to use said system, without any KYC mechanisms, as that would require a centralized entity to perform said KYC, hence, not making it a completely decentralized system anymore. Judging from your first two responses, I am also under the impression that you believe that such a design would require KYC, which is not the case.

The solution neither suggests that we need to regulate who can and cannot transact - this is your interpretation, happy to receive feedback on where this is insinuated. It is even stated that the beliefs are that KYC amongst other, are insufficient solutions in a decentralized world, under the topic:

“Additional Regulatory-Friendly Measures”

To clarify on this.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> for privacy-focused projects, irrespective of their design, it is imperative to ensure that regulatory bodies/organizations can pinpoint the target without additional information. Otherwise, it could be extremely dangerous.

I can understand this being misinterpreted thinking in the terms of traditional financial surveillance. The word “Regulation” itself may insinuate more than what was meant to describe throughout the article.

To use your terms - what we are lobbying for is a system that is fully decentralized, permissionless and private, that isn’t a complete black box, where encrypted data can be traced.

Now on that topic you brought up about getting data to back your claims - we actually have no data whatsoever on how regulation can/should be conducted on completely decentralized systems, as there has not existed any programmable, private and fully decentralized systems up until today (To my knowledge). And centralized systems have completely different assumptions, so I don’t believe historical statistics on this would give us any valuable insights, but as mentioned in previous responses, applied measures will most likely lead to making criminals get more creative to work around the system.

We merely suggests, given the current technical constraints, an architecture / design where regulatory bodies (Or any third party for that matter) can trace encrypted data without compromising users transactional and data privacy.

Why do we suggest this?

1. The world we know today is predominantly based on centralized systems, in order to ever bridge and onboard new users and liquidity from the world we are familiar with today and a future world encompassing more decentralized systems, in our view, there needs to be non-black box, decentralized private system that is deemed acceptable by current regulatory bodies, otherwise said systems are prone to be sanctioned / pressured under legal scrutiny.
2. Such a design scheme would not stop criminal activity, nor will it make it harder for criminals to conduct crime, but aid in tracing the flow of illicit funds once identified, thus potentially being able to catch these actors elsewhere.
3. Leading onto the tracing mechanism of bullet point 2 - there may be technical additions in the future where DAOs or similarly can provide evidence to certain funds being fraudulent / illicit and vote to freeze certain encrypted data. Speculating on potential designs.

If you would opt for an architecture where the system itself is a private black box, regulation will most likely be enforced on dApps, central exchanges and other, creating a system of enforced regulation at an application level, creating many centralized end points.

With all that said, we are happy to receive any constructive feedback but I don’t agree with you that this makes any claims towards “lobbying for financial surveillance”. It’s a solution to bridge two worlds without our future world being viewed as the wild west.

---

**MicahZoltu** (2023-11-28):

**TL;DR:** In the end, it comes down to a conflict between censorship resistance and censorship. Anything that censors bad actors necessarily means the system has the ability to censor. Since we cannot algorithmically define who is a good actor and who is a bad actor, there will always be some person or group that is defining the blacklist, and this is in direct opposition to the principal of censorship resistant finance.

![](https://ethresear.ch/user_avatar/ethresear.ch/philiperiksson/48/14087_2.png) PhilipEriksson:

> The solution neither suggests that we need to regulate who can and cannot transact - this is your interpretation, happy to receive feedback on where this is insinuated.

My conclusions come from me having spent a *lot* of time thinking about these systems and discussing various designs with people, and it has lead me to believe that all such systems eventually reduce down to deciding who is and isn’t allowed to transact, and any such system either doesn’t serve the stated purpose or deteriorates into totalitarian financial control.

Take, for example, the Privacy Pools design.  Lets even assume that you solve all of the UX problems with delayed withdraws and you fully solve for the UX around providing proofs.  It would allow one to prove that the provenance of their funds is not from any account in a particular list.  There is no KYC and no whitelist, just a blacklist of “bad actors”.  *The problem is that at the end of the day you still have a list of bad actors, and someone, or some group, decides who is on that list.  Anyone who ends up on that list is now not allowed to transact with the rest of the world.*

Decisions are being made about who is and who isn’t allowed to transact with everyone else.  This is a list of people who are excommunicated from the financial system.  Many such lists have been created in the past, and they **always** start with a very reasonable set of people on them.  The governance system of every such list in history has *also* eventually been captured and started adding people to it that many would agree shouldn’t be on it.  The canonical example of this is the US Sanctions list which now includes all innocent civilians from many nations, software developers who committed no crimes, and (as if to intentionally make clear how far it has fallen from original goals) immutable open source public goods.

The above assumes the system works perfectly, and there are no loopholes or ways around it.  This is a *huge* if, but one could certainly imagine it being possible.  If instead we assume that the system is imperfect then that is great, because it is much harder to capture an imperfect system.  However, an imperfect system then doesn’t actually fulfill the stated goals.  Instead, you make it so people have have to jump through some additional hoops and anyone who ends up on a captured list gets to suffer significantly, and in exchange the bad actors still work around it all.

![](https://ethresear.ch/user_avatar/ethresear.ch/philiperiksson/48/14087_2.png) PhilipEriksson:

> It’s a solution to bridge two worlds without our future world being viewed as the wild west.

On a more philosophical note, the entire reason the “wild west” was so successful is because they didn’t try to integrate with the old system.  They acknowledged that the old system was horribly broken and the set off to build their own new system.  It was chaotic and came with a lot of uncertainty, but it also saw some of the fastest growth and innovation that the world has ever seen.

While I can appreciate people’s desires to integrate tightly with the legacy financial system, I think most of us can agree it is horribly broken.  Attempts to sacrifice our principals of censorship resistant finance in order to integrate smoothly with that system will eventually just make what we are building more of the same.

---

**MicahZoltu** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/philiperiksson/48/14087_2.png) PhilipEriksson:

> With all that said, we are happy to receive any constructive feedback but I don’t agree with you that this makes any claims towards “lobbying for financial surveillance”.

On totally unrelated note, I didn’t actually see a concrete proposal in the linked document.  It appeared to be more of an opinion piece on how we should introduce some mechanisms for censorship into DeFi so we can integrate with TradFi.

Did I miss something?  If you have a concrete proposal for a novel architecture to solve this problem I can try to provide more concrete feedback.

---

**PhilipEriksson** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> TL;DR: In the end, it comes down to a conflict between censorship resistance and censorship

I agree.

I don’t think the design we are proposing enables any kind of censorship, what we want to achieve is a fully decentralized system, you can only trace encrypted data but not govern over it. Now, it would be possible, technically, to implement DAO features etc as I mentioned, which would enable censorship, and it would also be possible to, once exiting the system through trust-less bridges (A smart contract on the layer the encrypted execution environment sends its proofs) to have your data be censored on said other system.

In theory - (I haven’t deeply thought about all the consequences of a completely censorship free system) I think it is desirable to have a complete censorship resistant system (I would need to think a lot more about to have a more educated opinion as I may not consider all the downsides).

But even if we assume that that is the end goal, is it feasible to get the population of the world migrating into such a system just like that, when a majority of all assets owned are sitting in the “old systems”. Especially when the old system will deem it a haven for criminal activity and actively work against it.

This is a debate that has been pushed by the “cryptopunk” movement for decades now and in theory that may very well be the best future we can envision, but what’s the road to getting there. Rome wasn’t built in a day and I believe if that’s the end goal I believe there are certain steps to get there.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> On a more philosophical note, the entire reason the “wild west” was so successful is because they didn’t try to integrate with the old system. They acknowledged that the old system was horribly broken and the set off to build their own new system. It was chaotic and came with a lot of uncertainty, but it also saw some of the fastest growth and innovation that the world has ever seen.

I believe this is open for debate as well. I myself agree that  there are many flaws in our existing systems and that the wave of innovation has been marvellous and we’ve done a lot of great things, but the amount of fraudulent activity that has taken place has not been a pretty sight.

And actually, talking about other attempts / teams building in the space who are building complete black box infrastructures today, are co-operating with what you refer to as the “old systems” in enforcing regulation in other areas.

---

**PhilipEriksson** (2023-11-28):

I believe the article only showcases the high level design of our thoughts on privacy in the diagram.

We are actively building a ZKVM (encrypted execution environment) as an L2 “or L(N)” scaling solution that provides privacy to public blockchains, and you will find more resources on our website as well as research on HackMD accesible through the website.



      [olavm.org](https://olavm.org/)





###



Ola is a ZKVM-based, high-performance L2 platform that brings programmable privacy and scalability to Ethereum, helping people gain complete data ownership while shaping their own Web3 journey.










You can also refer to our Whitepaper here:



      [github.com](https://github.com/Sin7Y/olavm-whitepaper-v2/blob/51eda0d5606183b5ec51e8dd93ed53be7218a8d7/Ola%20-%20A%20ZKVM-based,%20High-performance,%20and%20Privacy-focused%20Layer2%20platform.pdf)





####

  This file is binary. [show original](https://github.com/Sin7Y/olavm-whitepaper-v2/blob/51eda0d5606183b5ec51e8dd93ed53be7218a8d7/Ola%20-%20A%20ZKVM-based,%20High-performance,%20and%20Privacy-focused%20Layer2%20platform.pdf)










It’s rather providing infrastructure for DeFi to deploy on, rather than DeFi itself. Anything can deploy on a ZKVM stack. I still don’t agree that this is bringing mechanisms for censorship into DeFi, as the entire infrastructure don’t allow for it unless implemented (However as mentioned above, allows for censorship once exiting the system, in other systems).

---

**MicahZoltu** (2023-11-28):

Is there a subsection of the white paper I should read if I’m only interested (at the moment) on your thoughts around how one “regulates” money in a censorship resistant way?  From what I have read of the original post here and skimming elsewhere my guess is that you are imagining something like privacy pools which allows for individual actors to define blacklists, and to interact with such an actor you need to provide a proof that your transaction history doesn’t include a blacklisted account after the account landed on the blacklist.

If that is your design, I can go into more details on why I believe it will not work the way you think it will.  However, I’m hesitant to provide a highly specific critique of a straw man design.  ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12)

---

**PhilipEriksson** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I should read if I’m only interested (at the moment) on your thoughts around how one “regulates” money in a censorship resistant way?

This is what I tried to explain/ I thought could be a potential misinterpretation in the above response. Depending on the use of the word “Regulation”.

I would read section 1.2 and 5 to understand the mechanism of states inside encrypted UTXO objects. Section 5.5 have some framework diagrams as well.

Any kind of dApp ranging from Social to DeFi to xyz can deploy on the architecture.

We are not building any identical scheme that relates to proofs of innocence or similar lists suggested by many different prominent researchers in the Ethereum/Blockchain ecosystem.

We are building a system where all transactions are encrypted per default (If interacting with a private dApp, we want to provide the option to build and interact with fully public dApps as well).

Only the sender knows the recipient (if the transaction happens to be a peer to peer payment and not interacting with a dApp). From a third party perspective you would see that some encrypted data, commitment (CM1) has been consumed, to create CM2.

In terms of censorship resistance. The only thing that is provided towards the third party is insight to the flow of encrypted data and possibility to perform analytics on this. Should it be identified that certain data belongs to a fraudulent actor, you can follow that, and try to impose measures when they exit the system.

---

**MicahZoltu** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/philiperiksson/48/14087_2.png) PhilipEriksson:

> I would read section 1.2 and 5 to understand the mechanism of states inside encrypted UTXO objects. Section 5.5 have some framework diagrams as well.

Hmm, I read over these sections and it looks like a pretty standard zkUTXO system overall, with contracts added but that doesn’t fundamentally change much when it comes to “regulation and privacy”.

If you aren’t building a proof of innocence system, then it is still unclear to me how your system is more “regulation friendly” than something like ZCash or Tornado.

---

On an unrelated note, I recommend storing only a hash of private state on-chain, rather than the whole thing.  Since private state can only be read by the user with the private key, you don’t need to store it on-chain.  Instead, you can leave it up to the user to store their state and only a hash is stored on-chain (which can then be used to verify the provided private state is accurate when private functions are called against it).

---

**PhilipEriksson** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If you aren’t building a proof of innocence system, then it is still unclear to me how your system is more “regulation friendly” than something like ZCash or Tornado.

Correct - we are building off of the work of ZCash like pretty much every other team building in the zkUTXO space.

The difference from a privacy/regulation perspective (compared to the other teams in the zkUTXO / ZKVM space) is in the private merkle tree structure. Whereas opposed to having a complete black box versus having linkable encrypted commitments (UTXOs) that are traceable through the updatable private tree.

There are other ZK/language/etc differences as well.

Other solutions solely rely on viewing keys which aren’t enforceable as they are derived from an enduser’s private key, hence these systems will most likely require KYC / enforced regulation on dApps / CEXes, enforced sharing of viewkey to interact etc.

These are some of the issues we are trying to avoid without sacrificing decentralisation by allowing for tracing of the encrypted data, it may create situations where you can prove your innocence if need be because you can always decide to share your viewkey as an honest user if analytics can be done on the network when/if regulators try and impose regulation.

This leads us back in a circle to the censorship / vs censorship resistance question and what is the right direction to move in / what system is optimal as of today and in the future.

---

**MicahZoltu** (2023-11-28):

Would it be accurate to summarize what you are adding as “the ability to reveal the destination of a single transaction, without revealing anything else about your activities”?

---

**PhilipEriksson** (2023-11-28):

Well, yes you can put it that way, I would probably phrase it differently but yes, the statement is not false.

As we have both a public tree and private tree, in an intiial transaction from pub → pri you’ll see only the sender.

Once you move within the private tree, pri → pri your statement holds accurate, some encrypted data is consumed to create some new encrypted data, where you have:

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> the ability to reveal the destination of a single transaction, without revealing anything else about your activities

if you want to exit pri → pub only the recipient is public and full corresponding backchain is still encrypted.

To also emphasize on the backchain of encrypted data → since they are linkable, should you identify down the line that a certain set of encrypted data in the private tree can actually be proven to belong to a fraudulent actor, you can trace it back in block history to try and perform analytics as well on where the funds have been spent, if this is only a fraction of it. (Just like analytics can be performed on the BTC network which is transparent, to assess what UTXOs belong to which wallet, depending on wallet type)

Refer to the diagram in the article for a visualization of this.

---

**JiangXb-son** (2023-11-28):

The ability definitely comes from the design about “the input and output are both commitments”, not the classic way “the input is nullified and the output is commitment”. It’s easy to understand.

Private transactions are linkable now and it’s helpful to trace the evil behavior without depending on anything

---

**JiangXb-son** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/philiperiksson/48/14087_2.png) PhilipEriksson:

> olavm-whitepaper-v2/Ola - A ZKVM-based, High-performance, and Privacy-focused Layer2 platform.pdf at 51eda0d5606183b5ec51e8dd93ed53be7218a8d7 · Sin7Y/olavm-whitepaper-v2 · GitHub

Btw, the privacy section in WP is not the final version now. We will release our new design in the latest version. Sorry for this.

---

**zilayo** (2023-12-07):

the privacy issue isn’t a deterrent for bad actors imo.

if they are located in certain countries or are state actors then they won’t care if their privacy isn’t 100% private.unfortunately crime will always find a way to slip through the cracks, although the same could be said for the non-crypto financial system as well.

imo we’re going down a path where increased surveillance will cause more friction & harm for normal users than those who it is intended to stop.

---

**d-ontmindme** (2023-12-10):

Interesting article and perhaps I need to read it closer but generally agree that there’s an inherent tension between the opt-in nature of most privacy-focused projects’ regulatory compliance strategy and the reality that that is almost always insufficient for regulators (no one who would ever opt-in will be people regulators care about for the most part).


*(11 more replies not shown)*
