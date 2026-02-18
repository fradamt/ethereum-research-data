---
source: magicians
topic_id: 3835
title: "Identity and Quadratic Funding: standards to help fund projects and commons"
author: jpitts
date: "2019-12-08"
category: Uncategorized
tags: [identity, funding]
url: https://ethereum-magicians.org/t/identity-and-quadratic-funding-standards-to-help-fund-projects-and-commons/3835
views: 4299
likes: 18
posts_count: 17
---

# Identity and Quadratic Funding: standards to help fund projects and commons

Is anyone interested in organizing standards for quadratic funding?

https://twitter.com/owocki/status/1203732163151028224

At nearly Magicians’ gathering there is a group of people coming together to discuss the issue of funding in the community. [@anett](/u/anett) and I even had a discussion at Devcon in Osaka, a session with the EF Grants Team and Cat Herders to discuss the funding of Magicians’ work.

Many prominent efforts have emerged as alternatives to “grants from whales”: Moloch DAO, MetaCartel DAO, all of the options that Gitcoin offers, and the innovations of Vitalik Buterin / Zoë Hitzig / Glen Weyl. It might be helpful to  to have an open tool set for funding based on the ideas of “[Liberal Radicalism](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3243656)” (CLR), perhaps this would lead to wider adoption and new things build on top of the approach.

But I wonder: isn’t it too early to standardize? Shouldn’t it be roughly tested more with the community first with efforts like [Gitcoin CLR Matching](https://medium.com/gitcoin/gitcoin-grants-clr-matching-ecbc87b10038)? *Update: in a comment Vitalik points out that for quadratic funding standards, work is needed right now in identity systems.*

**Please respond here if you are interested, and reach out to those in the community already discussing CLR and identity.** This includes [Kevin Owocki](https://twitter.com/owocki), [Alex Masmej](https://twitter.com/AlexMasmej), [Mark Beylin](https://twitter.com/MarkBeylin). If a Ring forms, I will create a category here in the Forum to encourage discussions.

Also, for more deep diving and explorations, check out Vitalik’s latest ball of lightning: [Quadratic Payments: A Primer](https://vitalik.ca/general/2019/12/07/quadratic.html)

## Replies

**vbuterin** (2019-12-08):

Not sure if “standardization” is the right frame for this sort of thing. What I was thinking is to keep supporting the Gitcoin and the [MACI](https://ethresear.ch/t/minimal-anti-collusion-infrastructure/5413) teams on their own paths (and in parallel keep working on better identity systems), and at some point one should integrate the other and we can have a standardized package for running QV / QF instances.

The one place where we *could* use more standardization work right now is identity systems.

---

**jpitts** (2019-12-08):

Agreed, a better frame might be coordinated experimentation. **And the requirement for quadratic voting/funding/etc to work in decentralized smart contract systems is standard identity.**

Those prototyping on these ideas could simply get into communications to compare notes and find common points to work on together, attract more to the scene. This has been happening in the DAO zone.

IMO premature standardization can be premature optimization in the coordination sense. But the communications / organziing makes identifying needs and creating shared resources a lot easier.

---

I didn’t even know there were MACI teams!



      [github.com](https://github.com/privacy-scaling-explorations/maci)




  ![image](https://opengraph.githubassets.com/e790e8701a5b8284f61c2efb26fec01b/privacy-scaling-explorations/maci)



###



Minimal Anti-Collusion Infrastructure (MACI)

---

**jpitts** (2019-12-08):

[Responses](https://twitter.com/owocki/status/1203778979594821633) from [@owocki](/u/owocki) on Twitter (to my original post here):

> Imho we need two standards - one for grants, the second for administration of CLR

> Personally I think standardization is valueable, but the real killer app would be a whitelabel Grant/CLR platform (that doesn’t have the assumptions gitcoin does around GitHub login/open source focus )…
>
>
> This way @glenweyl & co can administer CLR in many diff verticals

---

**pcowgill** (2019-12-09):

Agreed that it’s too early for a standard, but I am interested in working on some coordinated CLR experimentation (and I would be happy to work as a dev on building an open platform for CLR pilots).

Gitcoin in particular does all of their CLR logic off-chain (which I think makes a lot of sense for their purposes given speed to market, their current architecture, etc.), so I wonder if the standard would make sense as an EIP unless more of it is onchain? There could be non-EIP standards though, of course.

Gitcoin will be presenting at the next Chicago Ethereum Meetup in part about quadratic voting / CLR, and we may have our members do a mini CLR to decide how to prioritize which dapp pilots we want to run at upcoming meetups with a small matching pool.

I’ll note that whenever a standard emerges, different architectures would make sense for small numbers of M contributors and N recipients than for large numbers. For instance, if the numbers are small enough, the approved M and N addresses could live directly in a contract so that the distribution at the end could happen via a contract function call.

---

**jpitts** (2019-12-09):

[@pcowgill](/u/pcowgill),  excellent to hear that there is a Meetup focusing on this topic!

[@vbuterin](/u/vbuterin), regarding identity, I took a look at the state of standardization / development / adoption. There are highly developed standards and initiatives for this, and for Ethereum smart contracts in particular. There are usable implementations and some adoption. I will list some out here.

*It seems as if the momentum in this area is very good; are there concerns about the current work?*

---

**The key Ethereum-related standards**

[ERC-1056](https://github.com/ethereum/EIPs/issues/1056) - DID-compliant lightweight identity

[Jolocom DID Method](https://github.com/jolocom/jolo-did-method/blob/master/jolocom-did-method-specification.md)

[ERC-725 v2](https://github.com/ethereum/EIPs/issues/725)

**Identity resources and readings**

[Different Approaches to Ethereum Identity Standards](https://medium.com/uport/different-approaches-to-ethereum-identity-standards-a09488347c87)

[List of Ethereum Identity Specs, EIPs, implementations](https://decentralized-id.com/blockchain/ethereum/) - DIDecentral

**Significant implementations**

[uPort](https://www.uport.me/) - implements DID

[Jolocom](http://jolocom.com/) - implements DID

[Bloom](https://bloom.co/docs) - full DID compatibility proposed in [BLIP-6](https://github.com/hellobloom/BLIPs/issues/14)

**Initiatives**

[W3C DID WG](https://www.w3.org/2019/did-wg/)

[DIF / Digital Identity Foundation](https://identity.foundation/)

[Rebooting Web-of-Trust](https://www.weboftrust.info/)

[ERC 725 Alliance](https://erc725alliance.org/)

---

**vbuterin** (2019-12-11):

The problem with most “identity standards” today is that they solve the account administration and persistent-username problems, and don’t solve the unique human problem. I’d be interested in a taxonomy of solutions to the unique-human problem specifically.

---

**jpitts** (2019-12-11):

To expand on [@vbuterin](/u/vbuterin)’s  point about the human uniqueness challenge in self-sovreign identity systems, this is to prevent manipulation of systems which depend on users being actual people e.g. Sybil attacks.

Identity systems can use **verifiable claims**, enabling other users or algorithms to determine human uniqueness of an identity based on the credibility of the claims.


      ![image](https://miro.medium.com/v2/resize:fill:256:256/1*IGcfeU06EP-BajH1Gf3Okg.png)

      [Medium – 13 Jun 18](https://blog.sovrin.org/fixing-the-five-problems-of-internet-identity-b55ea072c3ea)



    ![image](https://miro.medium.com/v2/resize:fit:1200/1*nA6UI-Uf-7ITXA0MpKEE4g.jpeg)

###



by Phillip J. Windley, Ph.D., Chair, Sovrin Foundation



    Reading time: 5 min read











Identity systems can use video stream or other **analog proof** and a human or algorithmic verifier, without depending on third-party central authorities (but then these system themselves become central authorities).


      ![image](https://secure.gravatar.com/blavatar/8de2850cbea028965ee5fb54850ef3aadb87404f3571d9a6be62bc539c2f101e?s=32)

      [Technophile Musings – 1 Mar 18](https://jamespflynn.com/2018/03/01/kuwa-a-decentralized-pseudo-anonymous-and-sybil-resistant-individual-identification-system/)



    ![image](https://i0.wp.com/jamespflynn.com/wp-content/uploads/2018/03/defining-kuwa2.jpg?fit=440%2C330&ssl=1)

###



Like cookies and milk, cryptocurrencies and Universal Basic Income (UBI) are two particularly promising concepts that could go great together. If we’re to give money to the needy, then we sho…










Identity systems can use the **peer-to-peer** approach, allowing a chain of human uniqueness proofs to emerge by repeating a social behavior pattern.



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Key_signing_party)





###

In public-key cryptography, a key signing party is an event at which people present their public keys to others in person, who, if they are confident the key actually belongs to the person who claims it, digitally sign the certificate containing that public key and the person's name, etc.  Key signing parties are common within the PGP and GNU Privacy Guard community, as the PGP public key infrastructure does not depend on a central key certifying authority and instead uses a distributed web of Al...










and

**[POAP - The Proof of Attendance Protocol](https://www.poap.xyz/)**

---

**pcowgill** (2020-01-05):

Here is the Gitcoin Grants page for an open CLR / quadratic funding platform as described by [@owocki](/u/owocki) in the Twitter thread that [@jpitts](/u/jpitts) [linked to above](https://ethereum-magicians.org/t/identity-and-quadratic-funding-standards-to-help-fund-projects-and-commons/3835/4)!


      ![image](https://app.buidlbox.io/favicon.ico)

      [app.buidlbox.io](https://app.buidlbox.io/)



    ![image](https://buidlbox.io/images/buidlbox-twitter-card.png)

###



Ongoing and upcoming hackathons. Every buidlers gateway into the digital frontier.

---

**pcowgill** (2020-01-05):

(CRL -> CLR typo fixed on the Gitcoin Grants page, but it may continue to show the old version as a preview here.)

---

**anett** (2020-01-06):

[@jpitts](/u/jpitts) wrote an article on how Ops ring works " [The Operations Behind The Magic](https://medium.com/@jpitts/the-operations-behind-the-magic-b5123ef41b6b)" ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=9)

We put up [Gitcoin Grant](https://gitcoin.co/grants/223/ethereum-magicians) any support is highly appreciated and will be used for the sake of the community and in-persons meetings ![:money_mouth_face:](https://ethereum-magicians.org/images/emoji/twitter/money_mouth_face.png?v=9)

(it’s still in reviewing process but it’s live, sadly I’m not sure if it will make it into CLR matching ![:confused:](https://ethereum-magicians.org/images/emoji/twitter/confused.png?v=9) )

---

**adamstallard** (2020-01-10):

I started [BrightID](https://www.brightid.org/) a couple of years ago to specifically target the unique human problem.

---

**GriffGreen** (2020-01-12):

I love the narrow scope that brightID is committed to. Solely for providing “Proof of Uniqueness” It would be a great addition to CLR… I don’t know if it works well in the gitcoin implementation… as they have github for identity. But maybe it could be built into [@pcowgill](/u/pcowgill)’s Open Funding

---

**pcowgill** (2020-01-15):

Yep, for sure! I’m going to be hacking with the BrightID folks at ETHDenver as well.

---

**jpitts** (2020-04-16):

Kleros has a related project: [Proof of Humanity](https://docs.google.com/document/d/1z01MS0-h75ESVmWymU2Gv3Z43p35oZAFtQLStOeu7Ek/edit).

> A common problem on the internet is the lack of sybil-resistant identity systems. Users can generally create multiple accounts using different pseudonyms (or address in the case of crypto-networks) to receive rewards multiple times, bias votes, write multiple fake reviews, etc.
>
>
> We introduce Proof of Humanity, a system combining social verification with video submission in order to create a Sybil proof list of humans.

According to the [Kleros Development Update: April 2020](https://blog.kleros.io/kleros-development-update-april-2020/), smart contracts have been developed for the Proof of Humanity project.

---

**owocki** (2020-05-11):

Working plan for grants round 6 is to do SMS (or some zero knowledge version of it) for anti Sybil verification https://github.com/gitcoinco/web/issues?q=is%3Aissue+is%3Aopen+sms

---

**jpitts** (2020-08-21):

Here is a comprehensive overview of proof of personhood protocols.

[Who Watches the Watchmen?  A Review of Subjective Approaches for Sybil-resistance in Proof of Personhood Protocols](https://arxiv.org/pdf/2008.05300.pdf) [PDF]

> In this article, we will outline the approaches of these new and natively digital sources of authentication - their attributes, methodologies strengths, and weaknesses - and sketch out possible directions for future developments

