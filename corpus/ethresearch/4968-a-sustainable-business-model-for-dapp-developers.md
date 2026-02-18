---
source: ethresearch
topic_id: 4968
title: A sustainable business model for Dapp developers
author: STAGHA
date: "2019-02-09"
category: Economics
tags: []
url: https://ethresear.ch/t/a-sustainable-business-model-for-dapp-developers/4968
views: 4880
likes: 3
posts_count: 14
---

# A sustainable business model for Dapp developers

Developers need steady income in the long run to fund development and to compete with traditional services. How about: The developers charge fees but instead of instant payments the fees are transfered to a kind of DAO. The developers then make a proposal stating the amount of money they need and what kind of development they want to fund. Then users can decide to accept that proposal or to reject. In case of rejection the money would be transfered back to the users.

Advantages

- The problem of collecting fees is that somebody just forks the code and deploys the smart contract without fees. One reason against that is that users want sustainability and innovation and therefore support the development team. This reason would be reinforced by that user have a say in that regard and can acitvely support or reject proposals. For example users can reject a proposal when it is clear that a project turns into a cash cow where there is little to no further development.
- Accountability and transparency would improve a lot.
- The fact that users are kind of investors is an incentive alignment that is obviously very healthy.
- People who use the service more often and pay more fees have higher voting power. People who use the service one time have little voting power. This is a good incentive structure.

Disadvantages

- Higher complexity and and therefore security risk * Higher costs to just simply collecting fees

This is just a simple draft and im a wondering how complex it would be to implement something like that at the current state? Are there dapps like Aragon that could support something like this?

## Replies

**kronosapiens** (2019-02-11):

The answer to the problem of funding the ecosystem in a “fair”, effective, and decentralized way has emerged as a type of holy grail over the last year or so, it’s good to bring this up.

A few questions for you to ponder:

- Would there be a single DAO for all projects? Would each project send fees to this DAO?
- Who would be responsible for reviewing the submissions? Are votes weighted by “fees” paid?
- How would you secure the mechanism against spam requests / make best use of the limited attention of the voters?

It’s easy to say “give it to a DAO” but naive decision-making processes are vulnerable to attack and capture. There are a number of experiments going on at the moment to try and make "DAO"s more robust and secure by developing new decision-making mechanisms. DAOStack is experimenting with a mechanism called “holographic consensus” meant to make better use of the limited attention of voters. Colony is developing a mechanism called “BudgetBox” which seeks to determine allocations based on simple pairwise inputs. MolochDAO is a more recent experiment which looks to solve the problem of complexity by aggressively limiting the space of possible interactions (which BudgetBox does also). Aragon exists in a somewhat complementary space, having less to say on mechanisms but rather contributing a highly flexible permissions and routing system for connecting components.

While I would be skeptical that large number of unrelated projects would be eager to trust an unproven DAO with their revenue, I will note that in the context of one project (Colony, where I work), there is ongoing development of a mechanism (BudgetBox) for supporting projects *in our ecosystem* in a way which meets some of your criteria.

To summarize, while a solution you describe would perhaps be *technically* complex to implement, there are more fundamental hard and unsolved (“wicked”) problems around decision-making mechanisms which would need to be solved first. Fortunately, there are many hypothesis being evaluated at the moment, so hopefully the next 6-12 months will yield something exciting.

---

**STAGHA** (2019-02-14):

Thanks a lot for the answer and the references. I will shortly have a look at that. I heard that the transaction revenue in Polkadot will split into 10% going to the block producer and 90% to a treasury in the first time. I dont know the excact structure but there will be some kind of DAO structure.

---

**MaverickChow** (2019-02-16):

The best business model for dapps, in my opinion, is to treat dapps like software programs in which all transactions are denominated in ETH, while tokens are created to function like corporate shares whereby the token holders have a share of earnings in ETH when people use the dapps.

At the moment, almost everything dapp-related screws up when teams issue tokens that behave more like gift cards with the unnecessary function to run the dapps in order to give the tokens some value. Very bad decision-making, in my opinion. When will ICO teams admit no token is necessary to run any dapp? When will the community realize those tokens they are holding are more or less worthless with a false use case?

The only way to give value to the tokens is by transforming them into securities, like corporate shares, whereby token holders have a claim in potential earnings of the dapps involved. So if a dapp is useful and lots of people are using it, then the potential earnings will be high, and so will be the value of its token. Anything short of being a security will most probably never going to give any sustainable value to the token, in my opinion. Anything that behave like gift cards should have the value of gift cards. And anything that has no real fundamental use case, but instead being unnecessarily made to have artificial use case just to justify it having some value, will create unnecessary complexities into a dapp, making it less effective and efficient than without any token to run it.

ICO teams with unrealistic expectation and ambition in trying to create their own separate economic circle and dream of outgrowing such economic circle beyond the superset that is the Ethereum network through gift card tokens mainly out of greed are very naive to say the least.

---

**STAGHA** (2019-02-17):

I agree with a lot of that but currently i am just looking for ways of generating income. From your statement " So if a dapp is useful and lots of people are using it, then the potential earnings will be high, and so will be the value of its token" i assume you propose fees for dapp users right?

The problem is in your scenario why should people not just fork the code and use the software without paying fees? Especially when those fees are distributed to some shareholders.

Regarding your point on value of tokens i agree very much. Like this is the approach you take in traditional finance to value bonds and stocks. A stock has value because you have a right on future dividends. That most tokens are worthless and might be true. Still people seem to value them and the question is why.  Nevertheless it shows the need for steady income.

---

**MaverickChow** (2019-02-17):

Yes, fees for dapp users. Workable if dapp is developed like some corporate product/service whereby users need to pay to use. I am sure there is a way to maintain the codes in private to prevent forks. People continue to value worthless tokens because they have monetary attachment to them. The only way these tokens can generate sustainable financial value is when they are converted into STOs. Decentralized may not necessarily mean “strictly copy-able”.

Edit: Fees denominated in ETH. Similar to the way you are charged when you use EtherDelta or LocalEthereum. No token whatsoever ever needed. Additionally, IDEX being a quasi-DEX is unforkable.

---

**haokaiwu** (2019-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> ICO teams with unrealistic expectation and ambition in trying to create their own separate economic circle and dream of outgrowing such economic circle beyond the superset that is the Ethereum network through gift card tokens mainly out of greed are very naive to say the least.

I don’t agree with this. I don’t see why ICO’s are any different than what Ethereum tried to do once upon a time. Isn’t Ethereum itself trying to “create its own economic circle?” By this same logic, Ether would have been pointless to start as well.

In the backlash over unwarranted ICO hype, I think we’ve forgotten why tokens exist in the first place. Designed well, tokens can accrue value while ensuring the validity of decentralized decision-making.

Any time you have a DApp that requires:

1. Reliance on Ethereum’s security guarantees (even if “indirect” via an exit game)
2. Decentralized decision-making that’s native to the DApp
3. Optimizations that likely won’t be available on the base protocol

You need tokens plus some sort of staking to bootstrap your network. Use cases without #3 can just be a smart contract on Ethereum, while use cases without #1 should just be another blockchain. Use cases without #2 are some sort of private chain or STO. I agree that DApps that truly meet all three criteria are few and far between, but the few that are doing so provide a compelling argument (Loom, OMG, etc.).

Chris Dixon covers the high-level concept below. I personally think he’s too optimistic of the types of tokens provide such incentives, but his general point still stands. It’s the underlying principle of value in Ether after all.

https://medium.com/s/story/why-decentralization-matters-5e3f79f7638e

---

**MaverickChow** (2019-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/haokaiwu/48/2969_2.png) haokaiwu:

> I don’t agree with this. I don’t see why ICO’s are any different than what Ethereum tried to do once upon a time. Isn’t Ethereum itself trying to “create its own economic circle?” By this same logic, Ether would have been pointless to start as well.

And that is the problem with such reasoning. What Ethereum seeks to achieve is vastly different from what the ICO projects seek to achieve.

If the token is necessary, I am fine with it. But if it is there for fund-raising accountability and then be made to have an unnecessary use case just to justify the value, then I am not fine with it.

Imagine McDonald’s implement a new policy. If you want to buy a burger, you can no longer pay with dollars. Instead you need to buy MCD token that have the same value as your dollars, and use such token to buy burgers. Stupid people would hoard such token. Smart people would find such token totally unnecessary. Why do you want tokens to accrue value? Is it because the dapp truly + sincerely + honestly cannot survive without it? Or is it just because of the money? If it is because of money, then going the STO route is the best. In the future, most if not all the Fortune 500 companies will have STOs and probably none of them will have anything to do with private chain, in my opinion + speculation.

There are many factors contributing to the value of ETH. Being decentralized is one tiny part of it.

---

**haokaiwu** (2019-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> If the token is necessary, I am fine with it. But if it is there for fund-raising accountability and then be made to have an unnecessary use case just to justify the value, then I am not fine with it.

Then we agree. I don’t think anyone who takes the space seriously supports meaningless tokens. That’s not what I’m trying to say.

My issue with over-relying on STO’s is that it merely recreates the existing system of centralized control, VC funding, and power accumulation by a corporate entity. STO’s build a system of incentives to accrue value to a single entity: the corporation. Just because you’re putting the securities on a blockchain doesn’t mean it’ll create anything different than equity.

The promise of Ethereum and any other decentralized network is that it provides a viable alternative. The people doing the work (miners, stakers, DApp developers, etc.) are not part of a central entity, but each are incentivized to make the system work. Yeah, it’s very hard to make this work, but saying that it’s impossible neglects the fact that Ethereum/Bitcoin have done it already.

Going back to the original question, Maker has a model like this. Fees from generating CDP’s go to a DAO. Token holders then vote on what development to fund.

This provides a sort of cash flow both which supports developers and provides potential means for valuation. See here for further thoughts:

https://twitter.com/QWQiao/status/1091118154510675968

---

**MaverickChow** (2019-02-20):

Being able to create STOs is just a feature of the Ethereum network, and that does not mean STOs will dominate the entire network just the same as ICOs do not dominate the entire network, although currently the state of things do give such wrong impression, leading to false conclusion that the value of Ethereum network relies on ICO trend. STO is just a way of tokenizing equity ownership. And as the network will accommodate global economies, various ways of doing things will be developed. STO is just one such ways. It has nothing to do with changing the PoW/PoS structure or turning decentralization into centralization. I believe given enough time, every blockchain will become centralized, regardless of STOs or ICOs.

And even though professional qualification in finance/investment (like CFA) stresses DCF as one of several methods of investment valuation, that doesn’t mean DCF is the right way of estimating the value of Ethereum. Regarding DAO, I believe it is not general human nature to be generous, i.e providing services for free. Otherwise, we don’t need the blockchain for such a wonderful world to take hold. Otherwise, a DAO should make the best economic decision that will incentivize everyone involved to do their best by aligning everyone’s interests, particularly financial interests. And STOs being similar to corporate shares, albeit tokenized, may be proven to be a very feasible way to go.

---

**STAGHA** (2019-02-20):

“Fees from generating CDP’s go to a DAO. Token holders then vote on what development to fund.” I think that is not true as the stability fee is paid in MKR and that Maker gets burned right ? Therefore there is no distribution of fees.

---

**bgits** (2019-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/stagha/48/3203_2.png) STAGHA:

> A stock has value because you have a right on future dividends. That most tokens are worthless and might be true. Still people seem to value them and the question is why.

Some tokens have or plan to have governance capabilities over the protocol. If the protocol does start to accrue value in it’s vaults and the token holders can not find a better use for the funds, they can always choose to disburse the funds back to the token holders.

A simple thought experiment. Imagine a protocol at the end of it’s useful life, it’s already been replaced by other new and better protocols. However over it’s lifetime it has accumulated 10,000 ETH in it’s vaults. The intrinsic value of all it’s combined tokens would be at least the liquidation value of the vault (10,000 ETH), if the tokens could be acquired for less, someone could acquire a large enough amount to pass a vote and acquire ETH for less than the market price of ETH.

---

**bgits** (2019-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> Why do you want tokens to accrue value?

Here are a couple possible reasons why:

In many jurisdictions income received is a taxable event while value accrual is not. A DApp that captures value via accrual over income might be able to offer the same service for less due to a lower operating cost thanks to it’s lower tax burden.

Users can not only contribute value to the network but also participate in economic growth of the network they helped build.

An asset such as a token is easier to collateralize for lending against than a stream of income lowering the cost of debt against tokens vs income stream.

---

**Econymous** (2019-05-27):

My theory for resolve contracts fixes this, but honestly, to prove that you’ll need to hit my testnet or just wait for me to roll out data visualization.

http://terrible-music.surge.sh/#/market

I don’t feel like writing a long post, just wanted to let you know  we have a solution. So here’s the thread I started introducing the powerful concept of Resolve Distribution.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/econymous/48/11192_2.png)
    [Is a Tree of Pyramid schemes our best bet for a scaling solution?](https://ethresear.ch/t/is-a-tree-of-pyramid-schemes-our-best-bet-for-a-scaling-solution/5459/5) [Layer 2](/c/layer-2/32)



> It’s on ropsten testnet.
> The website’s a bit broken. it requires metamask to work, I’ll fix that shortly.
> http://terrible-music.surge.sh/#/market
> the website can now load without metamask, but the exchange can not be seen without metamask. working on that. now

Distribution solves a lot.

It solves governance (of funds) & it solves proof of stake.

Many more things as well. So much potential once we’ve mastered a whale resistent distributed token.

