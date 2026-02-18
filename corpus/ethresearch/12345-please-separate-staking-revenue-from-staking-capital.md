---
source: ethresearch
topic_id: 12345
title: Please separate staking revenue from staking capital
author: Michael2Crypt
date: "2022-04-06"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/please-separate-staking-revenue-from-staking-capital/12345
views: 3331
likes: 8
posts_count: 14
---

# Please separate staking revenue from staking capital

Hello,

Once Proof of stake is implemented, I plan to run nodes and affect the revenue to different charities I know, helping people suffering from homelessness, addictions, mental illnesses, aids, unemployment, …

I asked a lawyer and an accountant about the way to do this.

They made me aware of a problem :

- if I run the nodes by myself and give the money to charities, I will have to pay taxes first. Given the level of taxes in my country (income tax, social taxes, sole trader taxes because running a node is seen as a professional activity, local taxes …), charities will get 1/3 of the revenue in the best scenario.
- a better scheme would be to make my own non profit fund and to give the usufruct of the Ethers to the fund (the usufruct is the right to enjoy, for a certain period of time). The nonprofit fund would run the nodes (without taxes), and would give the revenue to charities.

In order to secure the scheme, the lawyer told me it is necessary that the revenue from the nodes are separated from the capital.

If the addresses are not separated, the lawyer told me it wouldn’t be possible to separate my capital from the revenue of the fund, and the tax administration is likely to consider that there is no separation between me and the non profit fund. As a result, I would have to pay at least 2/3 of the revenue in taxes, with heavy penalties.

So please manage the implementation of proof of stake to pay the revenue of staking on a separate address from the address containing the capital.

It would also be very useful for long term Ether investors, because investors want to secure their funds, they don’t want to run nodes by themselves. As a result, coders running the nodes should not have access to the private key of the address containing the capital of the investors. In this case too, the addresses should be separated.

Moreover, a separation would create job opportunites for Ether enthusiasts having the knowledge to run a node, because they would be able to partner more easily with investors, each having its separate address and responsability.

Such a separation is therefore likely to attract additional investors, to create job opportunities for Ether enthusiasts, and to have a  positive influence on the long term value of Ether.

I understand there may me slashing penalties affecting the capital (even if  I would prefer the penalties to affect only the address containing the revenue, because slashing is a problem of poor execution, not a problem of capital), but at least separate the revenue of staking from the capital. Thanks.

## Replies

**quickBlocks** (2022-04-06):

I love this idea.

Have you looked into a group called Giveth? They’re building what they call “The future of giving.” I’m not saying they are doing anything like this, but the missions are very well aligned, and they might find this idea interesting and be able to help (at least in a cheerleader sense) with the idea. I’ll post a link to this idea in their discord.

Also, this aligns (in mission) to a the underlying ideas behind GitCoin’s mission as well. I’ll copy a link there too.

---

**Michael2Crypt** (2022-04-06):

Thanks for posting the idea to these groups. I didn’t know about Giveth and Gitcoin.

In my view, the operational activity of the node, which could be managed by independent individuals, firms or non profit organizations, should be separated from the capital contribution.

The revenue of the node should be paid to the address of the node operator, and his Ethers could be slashed in case of poor execution.

Investors providing the capital to run the nodes should be rewarded by the node operator, on a consensual basis. Maybe they won’t ask any revenue at all to the node operator, if this operator is a non profit organization.

**It would be very positive for the reputation of Ethereum if non profit organizations could get revenue this way, by running a node.**

On the other hand, investors should have their funds secured on a separate address, making it impossible for node operators to take the funds of investors.

If an investor provides 32 Eth on a separate address to enable an operator to run a node, he should be able to get back the exact same amount of 32 Eth.

This conservation of capital is important, because it helps to prove to the legal and tax authorities that the investor is not linked to the everyday management of the node, that he is only a passive investor.

The legal and tax rules for business operators and for passive investors are totally different, which is also a good reason to separate staking revenue from staking capital.

---

**MicahZoltu** (2022-04-08):

A more generalized solution to this would be to make it so withdraws can be targeted at a specific contract, and the attestation key cannot change that.  The target contract could then have some mechanism for distributing received assets, so you can “prove” that the funds were never in your control, they were automatically allocated based on a pre-programmed thing.

---

**Michael2Crypt** (2022-04-08):

Yes, it would be possible to implement smart-contracts in different ways. In my mind, 1 single smart-contract would be enough :

1. the capital holder and the future node operator discuss with each others.  The capital holder chooses a new Ethereum address with no Ether on it, and communicates the public address to the future node operator.
2. the node operator signs a smart-contract of staking with the address of his choice. During the implementation of the smart contract, he writes that the 32 Ethers will be deposited on the public address told by the capital holder.
3. the capital holder deposits 32 Ethers on the address he chose previously, enabling the node to run since the capital condition is met (“proof of capital deposit”). The operator would get the revenue of staking, but he could lose some income in case of slashing.
4. if additional security is needed, the node operator may be obliged to deposit a small amount of Ethers before starting to operate the node, in order to be sure there is a loss in case of bad behavior. This “staking margin” could be zero if the network is calm and safe, and could be increased to 1 Eth or more if the network is under attack. While the node is running, the balance of the node operator address would have to stay always above the staking margin, and the node would stop in case the balance falls below this level, due to slashing or due to a withdrawal of funds.

With this scheme, the capital holder would be very likely considered as a passive investor by the legal and tax authorities, since he would receive no gain or loss in Ether during the process of validation, and the only action he would have done is to move 32 Ethers to another address of his choice. And moving cryptos to another address is not a taxable event.

The investor would keep the control of his funds, and he could move again his 32 Ethers at any moment : in that case the capital condition wouldn’t be met any more, and the node would stop.

The node operator would eventually pay a fee, or a share of the profit to the capital holder, but it would only depend of a free contract between them, outside of the blockchain.

**Such a scheme would be very good for decentralization** : if it is possible to separate the capital from the operative aspect of the node, holders will be incited to allow other persons to run nodes : non profit organizations, start-ups, students,  friends, …

For example, if an investment fund has 3 200 Eth, he could potentially run 100 nodes. A strategy could be :

- to run 70 nodes directly, inside the fund
- to make a partnership to allow some local start-ups to use 320 Ethers to run 10 nodes, with a contract of profit sharing. The investment fund would be able to communicate about this, as a start-up helper.
- to give the right to use 320 Ethers to local universities and colleges, who would run 10 nodes. The investment fund would be able to communicate about this.
- to give the right to use 320 Ethers to non profit organizations, who would run 10 nodes. The investment fund would be able to communicate about this, improving its reputation and the reputation of Ethereum : it could be NGO fighting for climate (because Ether staking is a green and energy efficient process), NGO for social welfare, NGO about cultural and artistic activities, …

This separation of capital holders and node operators would therefore help Ethereum to spread, and would be very good for decentralization.

This scheme of giving the use of Ethers to NGO, start-ups, … would be much better for Ethereum than giving Ethers directly, because when most organizations receive Cryptos, they usually sell them. If these organizations are given only the right to use Ethers, they will run Ether nodes and will sell only the revenue of staking.

On the contrary, if there is no possible separation between capital holders and node operators, capital holders will be much more cautious due to the increased risk of losing their capital in the process of staking. They will run the nodes by themselves, inside their firms,  or they will contract with specialized staking firms, with a lot of resources, heavy security measures, a huge legal team, expensive insurances in case the funds are lost … Staking would therefore become a very specialized and centralized activity.

The long term outcome would be that the vast majority of nodes would be managed by specialized staking firms, huge investment funds, and wealthy (elderly) individuals.

This is a chosen outcome since with the proposed scheme of separation, it’s possible to achieve the same level of security, while opening the activity of node management to more students, start ups, non profit organizations, …

---

**ehariton** (2022-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/michael2crypt/48/8077_2.png) Michael2Crypt:

> If an investor provides 32 Eth on a separate address to enable an operator to run a node, he should be able to get back the exact same amount of 32 Eth.

This investor has nothing at stake. PoS requires that participants can loose their stake. Otherwise the whole incentive system breaks down and bad-actors take over the network.

---

**Michael2Crypt** (2022-04-13):

There is something at stake : the **staking margin** the node operator may be obliged to deposit to start the node. This staking margin could be zero if the network is calm and safe, and could be increased to 1 Eth or more if the network is under attack.

While the node is running, the balance of the node operator address would have to stay always above the staking margin, and the node would stop if the balance falls below this level, due to slashing or due to a withdrawal of funds.

More precisely, slashing is intended to punish a bad node management. This is a problem of node operation, not a problem of capital. The capital holder doesn’t need to be punished, because he’s fulfilling its role : providing capital, which is rare, in order to limit the number of nodes. He doesn’t need to have something at stake because he doesn’t need to be punished as a legit capital provider.

If the capital holder is a bad actor willing to finance bad nodes again and again, he would also have to pay for the **staking margin** of the nodes operators, because no legit node operator would accept to work with him. So yes, he would have something at stake and he would lose money.

Apart form that, I think the proposed scheme increases the level of security of the Ethereum network :

- the current implementation is designed to resist opponents having succeeded to gather a significant minority of nodes.
- but there are many other threats, especially from regulators willing to take more and more control of the crypto environment.

Ethereum would do much better against this regulatory pressure if thousands of nodes where spread across colleges, universities, non profit organizations, start-ups, … because it would make Ethereum much more popular, and thus, more difficult to restrain.

For example, look at the indian and the russian regulators. The central banks of India and Russia were willing to ban cryptocurrencies totally, but the governments finally gave up this idea. The prime minister of Russia gave the real reason : “*We are well aware that we have more than 10 million young people having opened crypto wallets so far*” ( [MSN](https://www.msn.com/en-us/money/news/russian-prime-minster-estimates-citizens-hold-over-10-trillion-rubles-in-crypto-report/ar-AAW53d2) ).

It means governments are reluctant to go against their youth, especially the more qualified and skilled part, because these goverments need this youth to run the computer and data structure of these states. The more crypto, smart-contracts and DEFI are popular among colleges, universitites, start-ups and non profit organizations, the more liberal and soft the regulations will be.

And precisely, the proposed separation of capital holders and node operators makes it much easier to spread nodes across colleges, universities, non profit organizations, start-ups …

---

**Michael2Crypt** (2022-04-14):

The proposed separation of capital holders and node operators would only require small changes in the code, but it would make a huge difference regarding the legal and fiscal approach of POS Ethereum.

**A) Legal approach :**

The main question is to know whether POS Ethereum would be considered as a security or not. POW Ethereum was not considered a security so far, in part because Ethers are mainly used to run smart-contracts. Yet, with the implementation of POS, this aspect has to be studied closely again.

More precisely, the 4 questions of the [Howey test](https://www.sofi.com/learn/content/howey-test/) have to be answered :

- is there an investment of money ? (and are there risks of loss requiring investor protection from the SEC ?)
- is there a common enterprise ?
- is there a reasonable expectation of profits ?
- would a profit be derived mainly from the efforts of others ?

It would be better for POS Ethereum not to be considered as a security, because securities have to follow strict and complex rules.

In my opinion, the proposed separation of capital holders and node operators would reduce the risks for POS Ethereum to be considered as a security.

*1/   Is there an investment of money ? (and are there risks of loss requiring investor protection from the SEC ?)*

The proposed separation of capital holders and node operators would give nothing to capital holders, since all the revenue would be obtained by node operators for their participation to  the protocol.

Ethereum holders may obtain a revenue, but it would depend on their agreement with the operator of the node, outside of the blockchain. Such an agreement would of course be very easy if they are at the same time the node operator, but it wouldn’t be required by the protocol.

Without any separation, the situation is more risky, because many holders of 32 Ethers are just looking at the percentage they would obtain from staking. It gives the impression that they are investing to get an annual return on their investment. The risks for POS Ethereum to be considered as a security would be much higher this way.

The [SEC considered](https://www.sec.gov/divisions/corpfin/cf-noaction/2019/turnkey-jet-040219-2a1.htm) a token wasn’t a security because it was “*marketed in a manner that emphasizes the functionality of the Token, and not the potential for the increase in the market value of the Token.*”

Ethereum shouldn’t be widely seen and marketed as a way to get an annual percentage on a capital, because of the risk to be considered as a security.

Apart from that, the proposed separation of capital holders and node operators would reduce the risks of loss because Ethereum holders would keep the control of their funds on a separate address.

Finally, capital holders wouldn’t risk to lose their funds during the process of validation, because slashing would only apply to node operators, not to capital holders.

It means additional measures of investor protection from the SEC wouldn’t be needed, reducing the risks of POS Ethereum to be considered as a security.

*2/   Is there a common enterprise ?*

It seems the SEC has clarified that [sharing rewards and delegating validation](https://egg.fi/blog/staking/sec-call-for-crypto-staking-services/) makes staking services a “common enterprise.”

With the proposed proposed separation of capital holders and node operators, there wouldn’t be any sharing reward or delegated validation inside the POS protocol, because all the revenue would be collected by node operators for their participation to the protocol.

A capital holder may or may not conclude a contract to gain a revenue from  the node operator, but it would be their arrangement, outside of the blockchain, outside of the POS protocol.

In many cases, if the node operator is a non profit organization, a college or an university, the capital holder may asks nothing, so all the revenue of the node would be kept by the node operator.

*3/  Is there a reasonable expectation of profits ?*

With the proposed separation of capital holders and node operators, there wouldn’t be any expectation of profit for the capital holder, because the protocol would give all the revenue to the node operator.

There may be some form of contracts or agreements between them, but outside of the blockchain.

*4/ Would a profit be derived mainly from the efforts of others ?*

With the proposed proposed separation of capital holders and node operators, it would be easier to argue that capital holders are just passive investors which are just moving 32 Ethers from an address to another, if they want to enable an operator to run a node.

As passive holders, the protocol wouldn’t distribute any profit to them, and the value of their Ethers would rather depend mainly on the supply and demand, not on the efforts of others.

**B) Fiscal approach :**

The proposed proposed separation of capital holders and node operators would be much better regarding the clarity of taxation : all the revenue of staking would be paid to the node operator. It would therefore be entirely a revenue of independent business activity.

Without any separation, it’s difficult to say if the revenue is an interest on the 32 Eth staked, or a revenue of the activity of node management. Many countries require a trade registration for mining or staking, meaning they consider the participation to the network as professional activity. But at the same time, many stakers consider that it is just an interest they collect on their capital. So the situation is pretty confusing.

Without any separation, it is also very difficult to say which Ethers are sold. For example, let’s consider someone who has 32 Ethers on an address. He stakes his Ethers, and a year and half later, he has a little bit more than 34 Ethers on his address. At this point, this person is selling 1 Ether. Without any separation, it’s very difficult to say if the Ether sold comes from the Ethers obtained from staking, or if it is part of the 32 Ethers he had before starting to stake.

This is very confusing because in one case, the revenue may be considered as  business income, and in the other case it may be a capital gain. And things can be more complicated because of local  rules.

For big stakers, this may result into heavy tax penalties just because they filled the wrong case due to this confusion.

With the proposed separation of capital holders and node operators, contracts may occur between them, but it would be outside of the blockchain. Some custom contracts may be opportunities to structure the revenues and wealth of both.

For example, it may be possible for node operators to earn revenues of independent business activities, or to earn wages if they run a node inside a company. Depending on local rules, it may be more interesting to gain whether business income or wages, because of health insurance, retirement benefits, lower taxation rate, …, …

For Ethereum holders, it may be possible to contract with node operators and to earn a fixed revenue rewarding the use of their Ethers to fulfill the capital condition. The contract may also decide that the revenue would vary  depending on many factors.

It may also be possible for Ethereum holders to earn dividends : they would for example create a company, and provide a capital contribution made of the right to use  Ethers to fulfill the capital condition of staking. The company would run the node, and, with the profit, would be able to pay dividends to the shareholder. Since the Ethereum holder would just have to move Ethers from one address to another address of his choice, he would keep the ownership of his Ethers, having just transferred to the company the right to use them for staking, in exchange of shares of this company.

For Ethereum holders, it may also be possible to collect tax deductions if they give to charities the right to use their Ethers to fulfill the capital condition for staking. It may therefore be possible to collect tax deductions while passively holding Ethers (depending on local rules).

As a conclusion, the proposed separation of capital holders and node operators would improve fiscal clarity, predictability and optimization.

And it may reduce the risks for POS Ethereum to be considered as a security.

---

**MicahZoltu** (2022-04-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/michael2crypt/48/8077_2.png) Michael2Crypt:

> The investor would keep the control of his funds, and he could move again his 32 Ethers at any moment : in that case the capital condition wouldn’t be met any more, and the node would stop.

It is critical that the staked 32 ETH cannot be moved at a moments notice by the owner (whoever they are) as slashing almost always occurs *after* the attack.

![](https://ethresear.ch/user_avatar/ethresear.ch/michael2crypt/48/8077_2.png) Michael2Crypt:

> There is something at stake : the staking margin the node operator may be obliged to deposit to start the node. This staking margin could be zero if the network is calm and safe, and could be increased to 1 Eth or more if the network is under attack.

If only 1 of the 32 ETH is at risk, then the actual stake is only 1 ETH.  If this is something we want, we can just lower the staking requirements to 1 ETH rather than requiring people come up with 32 ETH only to put 1 of them at risk.  There are reasons we don’t lower the staking threshold to 1 ETH, but that is out of scope of this discussion.

On a more personal note, I’m strongly against designing Ethereum’s economic system to slot into The Current Rules of some particular country.  We should be designing Ethereum to make economic sense rather than to cater to the obscure and ridiculous tax laws of various countries around the world.  Keep in mind that tax laws change *incredibly frequently* and even if we did design things to slot into today’s tax laws in some country, they may not fit anymore in a year.

---

**Michael2Crypt** (2022-04-23):

Interesting.

I understand that the amount of 32 Ethers is in no way a passive capital deposit.

This is really the amount at stake, meaning the entire amount could be lost due to slashing.

This is an important information, because it makes things clearer :

**A) Legal approach :**

With this design, the activity of node validator is in no way an “investment”.

This is a demanding and risky business, and all the staking could be lost in case the node operator makes mistakes, uses a corrupt software to stake, …

This designs may reduces the risks for POS Ethereum to be considered as a security by the SEC, because of the answer to the fourth question of the [Howey test](https://www.sofi.com/learn/content/howey-test/) :

“Would a profit be derived mainly from the efforts of others ?”

The answer seems to be no because the possible profit would be derived mainly from the effort of the node operator himself, his ability to keep the funds safe, to choose a legit staking software or staking platform …

Additionally, Ethereum officials should not announce POS Ethereum as a way to gain a passive income (because it is just not the case), nor as an opportunity “[for the increase in the market value of the token](https://www.sec.gov/divisions/corpfin/cf-noaction/2019/turnkey-jet-040219-2a1.htm)”.

In the EU, the draft proposal of [MICA regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2020%3A0593%3AFIN) says that “*it will be notified to the national competent authorities with an assessment whether the crypto-asset at stake constitutes a financial instrument under the Markets in Financial Instruments Directive (Directive 2014/65/EU)*” .

This [directive 2014/65/EU](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014L0065) lists financial instruments in Section C, which includes in particular “*transferable securities*”, whose definition includes “*bonds or other forms of securitised debt*”.

There would be no guaranteed income or interest for an Ethereum validator, since the possible profit would be derived mainly from the effort of the node operator himself.

As a result, Ethers may not be considered as transferable securities under the directive 2014/65/EU, but things have to be confirmed and monitored closely. And even if Ethers are not considered as securities, it may be necessary to notify the  competent authorities because some Ethers are at stake.

**B) Fiscal approach :**

You said that tax laws of various countries change all the time. That’s partly true.

There are also international norms. Most countries are likely to qualify a revenue the same way, whether it is an income from employment, a business profit, an interest, a capital gain, …

That’s why there is a “[Model Tax Convention on Income and on Capital](https://read.oecd-ilibrary.org/taxation/model-tax-convention-on-income-and-on-capital-condensed-version-2017/model-convention-with-respect-to-taxes-on-income-and-on-capital_mtc_cond-2017-3-en)” published by the Organisation for Economic Co-operation and Development (OECD).

[![OECD_](https://ethresear.ch/uploads/default/optimized/2X/5/58fcd538a927bcb189bc4822bff62c2651eb0b34_2_415x500.jpeg)OECD_642×772 90.9 KB](https://ethresear.ch/uploads/default/58fcd538a927bcb189bc4822bff62c2651eb0b34)

More than 100 countries (including most of the G20 and developed countries) have joined the “[OECD Multilateral Convention](https://www.oecd.org/tax/treaties/multilateral-convention-to-implement-tax-treaty-related-measures-to-prevent-beps.htm)”.

With respect to the OECD  Model Tax Convention, the income obtained from staking Ethereum would be considered as Business profits (Article 7).

In particular, it is very unlikely to be an interest, a capital gain, or an income of employment.

There was a former article 14 “Independent Personal Services”, and Ethereum staking could have been considered as an independent activity under this article, but it was [suppressed in 2000](https://www.oecd-ilibrary.org/taxation/no-07-issues-related-to-article-14-of-the-oecd-model-tax-convention_9789264181236-en) and included in Business profits (Article 7).

It means that most developed countries :

- are likely to consider the income obtained from an Ethereum node as a Business profit (or as an income from independent activity if they haven’t merged yet this category with Business profits, just like the OECD did in 2000) ;
- are likely to consider anyone running an Ethereum node as a business operator.

With this in mind, il would be important to give Ethereum validators **the option of collecting the income of staking on a separate Ethereum address of their choice**.

Look at this validator on the Beacon chain :

[![validator](https://ethresear.ch/uploads/default/optimized/2X/f/f53f62d7a47da3b6d13a0f8c1a19c34562e5af08_2_690x408.jpeg)validator891×527 95.1 KB](https://ethresear.ch/uploads/default/f53f62d7a47da3b6d13a0f8c1a19c34562e5af08)

His balance is 33,15251 Ethers.

This includes 1,15251 Ethers of Business profits from validation, and an amount of 32 Ethers, probably purchased as an investment before the beginning of staking.

After the merge, if this validator sells 1 Ether, he will have to fill his tax return, which means :

- determining the type of income
- calculating the net income

If the business profit of 1,15251 Ethers and the 32 Ethers of initial investment are each on a separate address, it will be much easier to fill the tax return correctly, because it will be possible to identify precisely from which address the 1 Ether is sold.

If the 1 Ether sold comes from the address containing the 1,15251 Ethers obtained from validation, the income type will be plausibly “business profits” in most countries. But if it comes from the address containing the 32 Ethers purchased before the beginning of staking, the income type will more likely be “capital gains”, except if the investor is a professionnal trader as well.

The rules applying to the categories “business profits” and “capital gains” are totally different in most countries, that’s why it’s important to identify the origin of the Ether sold.

As the IRS says : “*You may identify a specific unit of virtual currency either by documenting the specific unit’s unique digital identifier such as a private key, public key, and address*” ([Q40](https://www.irs.gov/individuals/international-taxpayers/frequently-asked-questions-on-virtual-currency-transactions))   . It is the same in many other countries.

Therefore, if the business profit of 1,15251 Ethers and the 32 Ethers of initial investment are each on a separate address, it will be much easier to say if the 1 Ether sold is a Business income or a capital gain, and to fill the tax return correctly.

On the contrary, if the business profit of 1,15251 Ethers and the 32 Ethers of initial investment are on the same address, with a balance is 33,15251 Ethers, it will be much harder to identify which Ethers are sold.

For example, if 1 Ether is sold, it will be much harder to say if this Ether comes from the business activity of validation, or from the initial investment.

It may result in unfortunate consequences :

- if the seller estimates that this income of 1 Ether comes from the initial investment, he may report the net amount as a capital gain. But the tax office may disagree and consider that this 1 Ether comes from the business activity of validation, and should have been reported as a business profit. This may result in tax penalties due to unreported income and hidden business activity
- on the contrary, if the seller estimates that this income of 1 Ether comes from the business activity of validation, he may report the net amount as a business profit. But the tax office may disagree and consider that this 1 Ether comes from the initial investment of 32 Ethers (FIFO method), and should have been reported as a capital gain. This may result in tax penalties due to unreported income
- if the seller estimates that this 1 Ether come partly from the profit of business validation and partly from the initial investment, he will have to choose a method to calculate each fraction, and the tax office may disagree again
- the rules to calculate the net income from “business profits” and “capital gains” are totally different in most countries. Therefore it will be difficult in many cases to calculate the net income properly if the business profit of 1,15251 Ethers and the 32 Ethers of initial investment are on the same address

Perhaps it’s not possible to implement this separation for the Beacon chain, because the smart-contract is already done, but, for the future implementation of POS Ethereum, it would be a great service to Ethereum validators to give them **the option of collecting the income of staking on a separate Ethereum address of their choice**.

---

**Cotabe** (2022-05-06):

Hey [@Michael2Crypt](/u/michael2crypt) this is Cotabe from Giveth! I think the proposal would have a lot of benefits. Hope it gets implemented from the very beginning or later on. I love the idea of universities. NGOs and other decentralized stakeholders running nodes.

I also love the idea of for-good organizations harnessing revenue from stacking and building a source of sustainable funding for their operations. I am supporting all those who want to build the future of giving. I would love to explore how can we help you.

My handles are:

(at)Cotabe in Telegram, (at)Cotabe_M in twitter and Cotabe#4096 in Discord. Feel free to reach out.

Thanks [@quickBlocks](/u/quickblocks) for bringing this to our attention ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

---

**jgm** (2022-05-07):

A no-changes-required (partial) solution is for validators after the merge to send block transaction fees to a known charitable address.  These will never touch the validator’s account (or indeed the consensus chain at all), making separation a much simpler problem.

The flow of block transaction fees is shown in green in the images at [Understanding post-merge rewards](https://www.attestant.io/posts/understanding-post-merge-rewards/)

---

**jonreiter** (2022-05-08):

[@MicahZoltu](/u/micahzoltu) agreed that modifying the design to match individual interpretations of laws seems odd.  and [@jgm](/u/jgm) agreed that this looks solved already for validators. if you aren’t running a validator on your own then you are already involved in some sort of collective scheme and it is unclear to me how this accomplishes more than possibly removing one additional layer of smart contract(s).

not to say that isn’t potentially more efficient…i guess that depends whether this represents 1% or 50% of the computation involved in administering the scheme.

the goal of involving folks with smaller balances in validation activities is admirable. but as we need stake >> average rewards for slashing to work, so long as average rewards remain “high” then some sort of collective organizing/financing/acting feels required and parties just need to deal with whatever requirements that imposes.

---

**Michael2Crypt** (2022-05-23):

It’s a good point that validators will have the option to collect transaction fees on the address of their choice.

It would be even better to give validators the option to collect all the income of staking on a separate Ethereum address of their choice, and not only transaction fees.

In previous posts, I tried to list several economic, legal, fiscal and philanthropic reasons.

The fiscal argument is very important because mixing the staking capital of 32 Eth with the staking revenue creates a confusion between capital gains and business income (except for firms, everything is business income for them).

This confusion could give the opportunity for tax offices to impose various tax penalties on validators : unreported income due to filling the wrong case, hidden business activity, professional “contamination” of all crypto assets detained by a person, accounting problems due to more uncertainty choosing an intentory method : FIFO (globally or per address), LIFO (globally or per address) or Average cost (globally or per address), given the impossibility of specific identification due to the mix of staking revenue and staking capital  …

Apart from that, there are also security reasons to give validators the option to collect the whole  income of staking on a separate Ethereum address of their choice.

With such a choice, 32,5 Eth could be stored on a long term cold wallet or a multisig address (0,5 Eth more than 32 Eth, in order to be able to stay above 32 Eth in case of minor slashing).

Validators wouldn’t have to withdraw income from this address containing their capital. They could earn all the income and withdraw the funds on a separate address, their “everyday business address”.

They would be able to withdraw the funds without using the private key of the address containing the capital, wich is important for security.

For validators running several nodes, it would also be very convenient to be able to receive all the income on the “everyday business address” of their choice, without having to use the private keys of the different addresses cointaining the capital of 32 Eth.

