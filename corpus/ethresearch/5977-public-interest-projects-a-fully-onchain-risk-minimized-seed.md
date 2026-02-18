---
source: ethresearch
topic_id: 5977
title: Public Interest Projects - A Fully Onchain, Risk Minimized Seed Funding Mechanism
author: shinyshiba
date: "2019-08-15"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/public-interest-projects-a-fully-onchain-risk-minimized-seed-funding-mechanism/5977
views: 5447
likes: 30
posts_count: 15
---

# Public Interest Projects - A Fully Onchain, Risk Minimized Seed Funding Mechanism

**Public Interest Projects - A Fully Onchain, Risk Minimized Seed Funding Mechanism**

This post is a summary of the Public Interest Project. If you’d like to read the full paper, please click [here](https://file.globalupload.io/nEL7kCrIqQ.pdf). The full paper goes into more detail on the state of the ICO and IEO markets, the shortcomings of the ICO and IEO, the customization of PIPs, and gives more depth overall on this topic. We recommend reading it for the extra context.  (Also, as this is my first post, I will unfortunately have to remove hyperlinks in this post as I am restricted to only two - the full paper has all the links included.)

**Introduction**

As ICOs grew in popularity during the 2017 crypto bull market, the structural problems of ICOs were magnified and abused.  The main criticism of ICOs is that funds are received in one lump sum.  This makes it convenient for scams to occur and removes the concept of milestone-based funding.  In traditional financing, teams raise small seed funds and then raise larger funds through Series A, B, C and so on. Subsequent fundraises only occur if teams achieve milestones and build investor confidence.  With the popularization of ICOs, the concept of seed rounds for crypto projects financed by crypto participants have been largely overlooked.

The Public Interest Project (PIP) is a fully onchain seed funding mechanism which solves the many issues with ICOs while removing the risk of losing the patron’s principal, assuming the smart contract is correctly built.

**How it Works**

PIPs fund projects in a way that, assuming the PIP smart contracts are secure, are risk free to the patron. This is an extremely beneficial property of PIPs given that the risk of losing invested capital is highest during the earliest phases of a project, such as a seed round. If the team proves themselves to the crypto community during the PIP phase, they can choose to conduct a follow on funding via a DAICO. (Contributors to PIPs will be referred to as patrons because it is important to make the distinction that patrons are **not** investors.)

The PIP is simply an addition to ideas already being discussed and implemented in the crypto community such as by PoolTogether, ZeframLou, PaulRBerg, rDai, and probably many others out there who have similar ideas.  (The full paper has links to each of these people/projects)

Below is a *simplified* explanation of how the PIP works. At the end of this section is a link to the github repository which has the *technical* explanation and diagrams. Simplified version:

- A token project deploys a smart contract which interacts with the Compound protocol. Patrons can then send assets to the smart contract.
- The interest yielded from the patrons’ assets in the smart contract are then sent to the token project, creating a stream of interest funding for the token project.
- The smart contract will send back an equivalent amount of the project’s native token to the patron based on the interested yielded from that individual patron’s staked assets.
- The token project (or anyone else) could create a market on Uniswap for the token to create a pool of liquidity for patrons to trade with. This price discovery would result in a market rate for the token to derive the amount of tokens necessary to send back to the PIP patrons.

To help tie the PIP mechanism together, let’s go through a simple example. Alice, Bob, and Carol decide to pool their assets to fund Project XYZ and in return will receive XYZ tokens. Alice sends 200,000 DAI, Bob sends 300,000 DAI, and Carol sends 500,000 DAI for a total of 1,000,000 DAI in the PIP smart contract. In this example, assume that the interest rate (APR) is 10%. For simplicity, assume that the interest is paid daily and the project’s tokens are returned daily. Finally, assume the price of XYZ token is equivalent to $0.5 USD and that DAI is equivalent to $1.00 USD. The diagram below shows how this would play out.

[![image](https://ethresear.ch/uploads/default/original/2X/8/8cba242d8af090750c84b9141a6f09de79b3da4a.png)image507×307 37.4 KB](https://ethresear.ch/uploads/default/8cba242d8af090750c84b9141a6f09de79b3da4a)

The technical explanation of how PIPs work can be found in this [github repository](https://github.com/kraikov/pip-seed-funding-mvp). This repository also contains example smart contracts. ***These example smart contracts are not audited and are simply meant to help others get started quickly. These should NOT be used without further due diligence.***

PIP Seed Funding Benefits and Limitations

The PIP solves many of the problems that ICOs have been criticized for.  Assuming the PIP smart contracts are working as intended and that the price of DAI remains at $1 USD, the benefits of PIPs are:

- PIPs are a way for token projects to access seed funding fully onchain.  If the project proves itself and builds investor confidence, it can choose to do a follow on round through a DAICO.  This will help filter projects more effectively.
- Typically, the earlier that funding occurs, the riskier it is.  The PIP removes the risk from seed round financing because funds are only sent via interest on the patron’s capital. The patron only “loses” out on the opportunity cost of having invested that capital elsewhere.  To compensate for this, the patron receives tokens from the token project equivalent to the interested gifted.
- PIPs essentially introduce milestone based funding to crypto financing because patrons can remove or add more assets to the PIP contract depending on their assessment of the project’s development.  This should create more motivation for teams to continue to build versus the lump sum model of ICOs.
- PIPs reopen funding opportunity to all who wish to participate because this is done entirely on the Ethereum blockchain, without reliance on outside entities.
- Projects funded through PIPs are not dependent upon centralized exchanges to provide liquidity.  Projects can simply create their own Uniswap market from the beginning if they want.

Although PIPs carry many benefits, there are also limitations and unknowns which are:

- Since funding is sent as interest yielded from staked assets, the amount of funding a project receives may not reach very high amounts.  Given that PIPs are meant to address the lack of seed funding mechanisms in the crypto market, the lower fund size is to be expected.
- If PIPs as a fundraising mechanism were to grow rapidly, it would introduce a large influx of loans supplied to the Compound protocol.  All else equal, this would push the interest rates down for these assets.  There may be a ceiling in the short term on how many projects could simultaneously run large PIPs.
- If interest rates dropped drastically, it would create strain for the projects funded through a PIP.  However, this does not differ much when compared to projects funded through Ether or other cryptos, which have declined drastically in price since the peak of the previous bull market.  As always, responsible capital management is essential.
- The DeFi ecosystem is relatively brand new.  There are still a lot of unknowns that could create unforeseen side effects from an influx of loan supply.

**Closing Thoughts**

The bull market of 2017 created a massive spike in popularity of ICOs.  Although ICOs have helped enable innovation for the crypto industry, the structural flaws of the ICO have been abused by scammers, have rewarded teams without any milestone structure, and have unfortunately led to many investors losing funds.

PIPs act as a seed round for crypto projects to get off the ground.  Through this process, teams can prove themselves to the broader crypto community before taking on further funding.  PIPs, assuming the smart contracts work as intended, remove the risk of losing patrons’ capital since funds are contributed through interest yielded on the staked capital.  Although the patron will lose out on opportunity cost, the patron will receive tokens in return for the interested gifted to the team.

The PIP is an example of how the crypto ecosystem can self-regulate and self-correct and move together towards more responsible mechanisms. Hopefully the PIP can serve as a seed funding option to help further the innovation of the crypto ecosystem at large while protecting patrons’ capital.

## Replies

**vbuterin** (2019-08-16):

Interesting! I really like this for multiple reasons:

1. It has the DAICO-like property that instead of getting burst funding all at once developers get money over time, and if they stop performing, people can take their deposits out and make developers stop getting money.
2. There is no risk of “loss of principal” to depositors, which is both nice psychologically and likely reduces risks legally.
3. More opportunity for people to join over time, rather than just a one-time event.

Risks I see are basically what you mention: that demand for borrowing coins is limited, so the total revenue that the system can generate for projects is capped. Also, rates for ETH are even now very low on Compound (0.02%), so you would need to switch to DAI to get significant rates (now ~10%).

---

**CBobRobison** (2019-08-17):

It seems the risk could be mitigated by substituting or supplementing Compound with other income generating opportunities, such as PoS rewards once implemented. And if projects still prefer to earn interest from their PIP in something more stable, like DAI, rewards could get passed through UniSwap or some other non-custodial exchange.

---

**shinyshiba** (2019-08-17):

Your second point is really interesting because if there is no risk to the patron’s capital, I wonder if the “investor protection” consideration would be invoked to prevent something like this.

Agreed on the ETH point.  I am assuming that most PIPs would be funded via DAI or USDC.  However, a large influx of loan supply would push rates down, all else equals.  Also with DAI, there is a ceiling to how much could be contributed since the circulating supply of DAI is relatively not that high and creating new DAI has a stability fee of 20.5% at the moment.  For PIPs to become a very popular funding mechanism, loan capacity and DAI creation would both have to increase considerably in a sustainable manner.

I’m hoping to see projects start experimenting with PIPs in the near future so these ideas can evolve further!

---

**MaverickChow** (2019-08-17):

On the flip side, the idea will put higher pressure on ICO team members to commit to significant and prolonged market manipulation to avoid depositors from withdrawing their money.

Ultimately depositors are still investors in their right mind, so the standards used to judge what is performing and what is not will be subjective unless it is hard-coded into the contract and audited. To the depositors, an outperforming token price indicates performance. To the developers, that is not the case.

Still, who will decide if the ICO project is performing or otherwise? If the depositors are the one to decide, personal subjectivity and emotion reigns. If the ICO developers are the one to decide, there many be conflict of interest and power bickering and may not allow withdrawal even if the project underperforms.

Most ideally, the blockchain should not be used for launching ICO projects with utility tokens that can be done without, and much less discuss about how to do better ICOs and IEOs.

To discuss about how to do better ICOs and IEOs can be likened to discussing about how to ride horses better, in a world where automobiles reign. By right, the horses should be retired. And by right, the ICOs and IEOs should not be encouraged.

---

**kraikov** (2019-08-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> Ultimately depositors are still investors in their right mind, so the standards used to judge what is performing and what is not will be subjective unless it is hard-coded into the contract and audited. To the depositors, an outperforming token price indicates performance. To the developers, that is not the case.
>
>
> Still, who will decide if the ICO project is performing or otherwise? If the depositors are the one to decide, personal subjectivity and emotion reigns. If the ICO developers are the one to decide, there many be conflict of interest and power bickering and may not allow withdrawal even if the project underperforms.
>
>
> Most ideally, the blockchain should not be used

How the team members can manipulate the market, since the tokens are minted (and transferred to the patrons) based on the funding they receive (i.e. the accrued interest)? The only pressure I can imagine is a pressure on the team to make progress and to earn patron’s trust over time.

The withdrawals are meant to be open unconditionally. Even if the team decides to put a “locking mechanism”, the patrons can always decide not to fund the project. And even if they decide to lock their funds, they won’t lose their principal.

You can always measure the performance and the progress when it comes to software development. And it’s indeed subjective and in that case this is good. In traditional investing, the seed funding comes in tranches and the investor can always say that he won’t give you the next tranche, because you didn’t achieve a certain milestone.

---

**MaverickChow** (2019-08-17):

Manipulation by way of token price pump and dump, by shilling and hyping the project every now and then, by making an announcement of an announcement of a purportedly bullish news, etc. Price pump and dump alone involves layering, wash trading, spoofing, etc.

In theory we may have the tendency to expect everything to progress smoothly and perfectly without any glitch, but through repeated experience, we know well enough that is usually not the reality.

Besides, doing an ICO or an IEO in a much better way does not justify them having utility tokens in the first place that the projects can be done without.

---

**bgits** (2019-08-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Risks I see are basically what you mention: that demand for borrowing coins is limited, so the total revenue that the system can generate for projects is capped. Also, rates for ETH are even now very low on Compound (0.02%), so you would need to switch to DAI to get significant rates (now ~10%).

These risks maybe smaller than expected. Rates impact demand, so more inflow to the money market will drive rates down but all else the same it will increase demand bringing rates back to pre inflow.

The total return is `interest + price appreciation`, given DAI is mean reverting we usually ignore the price appreciation. I would postulate as these markets become more efficient the relationship of returns will approximate `DAI * DAI_COMPOUND_RATE == ETH * ETH_COMPOUND_RATE * ETH_RETURN` where if the main use case for borrowing DAI is to buy more ETH then `ETH_RETURN = DAI_COMPOUND_RATE * ETH_RISK`

---

**shinyshiba** (2019-08-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> Besides, doing an ICO or an IEO in a much better way does not justify them having utility tokens in the first place that the projects can be done without.

Hey these are good points, thank you for adding them to the discussion!

Maybe I am more optimistic, but since there is no capital at risk, I would hope everyone involved is more level minded about it (big hope I know).  Announcements of announcements generally don’t go over well for any project and is a quick way to lose trust in the broader community.  If a project wants to do this, there’s no stopping them of course.  This might even help in the very short term.  However, in the long run, that is a quick way to lose reputation and interest.  If a project wants to do a follow on after a PIP via something like a DAICO, the project’s track record during PIP should be examined closely.

Btw, I totally agree that things will not progress smoothly and perfectly without any glitch.  I don’t think that an ideal path was ever implied.  This is simply just another vehicle for funding that limits abuse - and if abuse does occur, at least the patron’s principal is not at risk.  ICOs and IEOs will continue to happen - these will never completely go away.  I believe improving the flaws of ICO/IEO is important on its own.  If the token being distributed really has no use case, I don’t see why anyone would want to acquire these through interest funding.

---

**r** (2019-08-18):

In countries where all crypto funds must be declared at the time they are received a standard ICO will place the maximum tax burden on the recipient. In contrast the PIP spreads this out over months or years allowing the recipient more favorable taxation options. I like this idea a lot.

---

**shinyshiba** (2019-08-18):

Thanks for sharing the tax perspective.  That benefit never crossed my mind but that makes a lot of sense.

---

**KyleJKistner** (2019-08-19):

Compound is just one of many interest bearing protocols in DeFi at this point. It would make more sense to have it interact with a rebalancer such as Idle.Finance, Topos, or MetaMoneyMarket. There’s no reason to just settle for Compound when Fulcrum and dYdX frequently offer higher rates.

---

**Swader** (2019-08-23):

Great idea. Is anyone working on this contract template yet? If not, I could give it a spin. If yes, I offer my help in looking it over and providing feedback.

---

**kraikov** (2019-08-24):

Hey, thanks!

There is an example implementation hosted on GitHub - https://github.com/kraikov/pip-seed-funding-mvp

There are slots for a lot of improvement, so feel free to fork/contribute/raise issues.

---

**muonnoi** (2022-04-11):

Thanks for sharing! Looks like the links to full paper mentioned in this thread and also in github are no longer working. Appreciate any updated link to the paper.

