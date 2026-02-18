---
source: ethresearch
topic_id: 21254
title: Agent-based Simulation of Execution Tickets
author: pascalst
date: "2024-12-11"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/agent-based-simulation-of-execution-tickets/21254
views: 806
likes: 7
posts_count: 1
---

# Agent-based Simulation of Execution Tickets

# Agent-based Simulation of Execution Tickets

*by [Pascal Stichler](https://x.com/pascalstichler) ([ephema labs](https://www.ephema.io/))*

*Many thanks to [Julian](https://x.com/_julianma), [Jonah](https://x.com/_JonahB_), [Marc](https://x.com/marc_nitzsche) and [Chris](https://x.com/cshg0x) for valuable feedback and special thanks to [Barnabé](https://x.com/barnabemonnot) for prompting the research in the first place and guiding it.*

> Please note: This is only a summary of the findings. The complete research report can be found here and the code is available on Google Colab and Github. Instructions on how to run the simulation are shared here. Simulation results are available in this folder and a recording of a presentation at Devcon 2024 on the topic can be found here.

# TL’DR

- We reviewed and holistically scoped the mechanism design space for Execution Tickets and evaluated potential concrete mechanism designs through a structured review and agent-based simulation.
- Execution Tickets are an effective mechanism for capturing MEV rewards at protocol level, however block builder decentralization and resistance to Off-Chain Agreements (OCA-proofness) remains a challenge.
- Auction-based pricing formats perform well on capturing MEV rewards, while an adapted EIP-1559 style pricing shows less favorable dynamics.
- Enabling a secondary market in the simulation fostered decentralization and MEV capture.
- The outcomes of the simulation on centralization and MEV capture are very sensitive to execution ticket holder attributes, particularly the ability to extract MEV and volatility specialization. This is in line with previous literature.

# Background

Execution Tickets are currently discussed as a promising next evolutionary step for enhancing Ethereum’s block space allocation mechanism. With Execution Tickets the protocol sells the right for execution block proposing. This is done by offering tickets, which allow ticket holders to participate in a lottery to be drawn as an execution block proposer in the future. It separates consensus rewards such as priority tips paid by users from execution rewards such as Maximum Extractable Value (MEV). It aims to foster decentralization among beacon chain validators by reducing the sophistication requirements for validators by removing optimization shenanigans like timing games [1]. Further, it enables protocol-level capture of MEV. Thereby, it essentially aims to tackle two problems: the “allocation” problem that currently MEV rewards leak to block proposers and secondly the “centralization” problem of the MEV supply chain [2].

Execution Tickets were initially introduced by Justin Drake [here](https://www.youtube.com/watch?v=IrJz4GZW-VM) outlining the motivation. He explains the general mechanism design of separating consensus from execution layer rewards and selling Execution Tickets for participating in a lottery to be chosen as the execution block proposer. Mike Neuder formalized and more clearly outlined the mechanism design [here](https://ethresear.ch/t/execution-tickets/17944) and also collected several open questions. We provide a more colloquial introduction on how and why protocol mechanisms evolved [here](https://www.ephema.io/blog/beyond-the-stars-an-introduction-to-execution-tickets-on-ethereum). In a good economic analysis [here](https://ethresear.ch/t/economic-analysis-of-execution-tickets/18894) and [here](https://arxiv.org/pdf/2408.11255) by Jonah Burian, Davide Crapis and Fahad Saleh it is shown that when priced correctly, Execution Tickets can internalize all value generated MEV rewards at protocol level. However, with the important limitation that “*the protocol must be capable of selling tickets at their intrinsic value*”. Further, Barnabé Monnot provides a good overview of protocol considerations over time and how Execution Auction (EA) as a special implementation of Execution Tickets with a fixed 32-slot advance period could function [here](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ). The idea of Execution Auctions is further extended by Thomas Thiery [here](https://ethresear.ch/t/proposers-do-play-dice-introducing-random-execution-auctions-randeas/20938) by introducing a randomization element (randEA).

As the previous literature often focuses on the bigger picture and leaves out the knits and grits of the mechanism design we plan to focus on the details of the mechanism design. For example, what is the best pricing mechanism for selling Execution Tickets? Should there be a variable or fixed amount of tickets [3]? Shall tickets be expiring and resaleable? Or maybe returnable to the protocol?

To provide insights into answering these questions, we developed a theoretical framework identifying the primary objectives of an Execution Ticket mechanism design, metrics how to measure them, and propose desirable price characteristics. Further, we outlined the main mechanism design parameters and their possible expressions. Based on a theoretical evaluation and an agent-based simulation, we draw primary conclusions on the mechanism design.

# Methodology

The approach to validate potential mechanism designs for Execution Tickets is twofold.

In the first step, we conduct a theoretical analysis of the objectives that the mechanism aims to optimize and propose several metrics to measure the achievement of these objectives. Next, we outline the design space of possible mechanism attributes and their potential values. This includes properties of the tickets as well as potential pricing and allocation mechanisms (e.g. auction-based formats vs. quoted-price formats). Based on a preliminary theoretical analysis, potential concrete mechanism designs are proposed and evaluated using a theoretical framework.

In the second step, these findings are verified using an agent-based simulation. Simulations (e.g. [EIP-1559 simulation](https://ethereum.github.io/abm1559/notebooks/stationary1559.html)) have proven to be a suitable tool to estimate the impact of potential mechanism design choices. The simulation emulates the allocation, trading, and redemption processes of Execution Tickets. The scope of the simulation is to run the previously designed configurations and compare them based on the objectives. Furthermore, conclusions can be drawn from the simulation about each parameter to determine favorable choices. The simulation is implemented in Python using existing industry standard frameworks ([radCAD](https://github.com/BenSchZA/radCAD)). For brevity reasons the simulation assumptions and specifications are not outlined here, but can be found in the [research report](https://drive.google.com/drive/folders/1G9Rln1UL1iOlm5NK4q8ggHr0mF0Zk1r0?usp=drive_link) in Chapter 5.1.

# Mechanism Objectives & Design Space

To outline the possible design mechanisms, we first outline the desired mechanism behavior and the solution space of different configurations before evaluating them.

|  | Objectives | Measurement metrics |
| --- | --- | --- |
| Optimization Parameters | 1. Decentralization  2. MEV Capture  3. Block Producer Incentive Compatible (BPIC) | 1. Market share, Nakamoto-coefficient & Herfindahl-Hirschman Index  2. MEV-Share Protocol |
| Pricing Behavior | 1. Price Predictability  2. Price Smoothness  3. Price Accuracy | 1. Garman-Klass (GK) Measure  2. V(Δp) 3. MEV-Share Protocol |

*Table 1: Summary of important objectives*

Execution Tickets aim to optimize two key objectives: fostering decentralization among beacon chain proposers and capturing Maximum Extractable Value (MEV) at the protocol level. Thereby it addresses the two key goals of the Ethereum roadmap segment “[The Scourge](https://vitalik.eth.limo/general/2024/10/20/futures3.html)”: (i) Minimize centralization risks at Ethereum’s staking layer and (ii) Minimize risks of excessive value extraction from users.

Decentralization is a key aspect, as it prevents several unfavorable dynamics. In the context of Execution Tickets it can be divided into beacon chain validator and execution chain decentralization. Execution chain centralization can happen on ticket holder or on block builder level [2]. Generally, decentralization ensures liveness in the sense that not a single actor can voluntarily or involuntarily halt the chain and impair liveness. Further, it contributes to censorship resistance [4]. For these reasons, beacon chain validator decentralization is paramount. Execution chain proposer decentralization is less critical under the assumption that beacon chain validators can force certain transactions into the block, for example with a version of inclusion lists and JIT top-of-block auctions. In this case, execution chain proposer decentralization is mainly relevant to avoid liveness risk and to foster competitive bidding for ETs.

Capturing MEV at the protocol level is essential as it removes MEV rewards from beacon chain validator rewards and most likely burning the rewards is the most neutral way to do so. Additionally, from a game theory perspective the mechanism should adhere to certain criteria outlined in [5]. Firstly, block producers must be incentivized to participate and propose non-empty blocks, described as Block Producer Incentive Compatible (BPIC) [6]. Secondly, it should be resistant to Off-Chain Agreements (OCA-proof), meaning that participants cannot mutually benefit from making off-chain agreements. Lastly, it should be Dominant-Strategy Incentive Compatible (DSIC), meaning for each participant there is a dominant strategy they can apply regardless of the behavior of other participants. For example, in a sealed-bid first price auction participants need to theorize about the intrinsic valuations of other participants and their bidding strategies to calculate their bid, making it not DSIC and thereby making it more complicated for participants and potentially not incentivizing to reveal their true intrinsic valuation.

We propose to measure decentralization through three metrics: Nakamoto coefficient, Herfindahl-Hirschman Index (HHI) [7], and market share of the largest ticket holder. Further, MEV capture can be assessed by the share of MEV rewards of ticket holders captured at the protocol level.

Execution Ticket price behavior we see of secondary importance, however still worthwhile to consider. Thereby we focus on three aspects: price predictability, smoothness, and accuracy. Price predictability is crucial for validators to participate in auctions and plan long-term. As summarized in [8], volatility can be a measure for price predictability in financial markets, following methods like the Garman-Klass (GK) measure [9]. The Garman-Klass measure is traditionally used in financial markets to measure volatility by including the daily opening, low, high and closing price. For our purpose the time interval needs to be adjusted, e.g. to epoch-based intervals. Price smoothness ensures stability during market fluctuations, reducing risk for ticket holders, with the variance of consecutive price changes (V(Δp), essentially being autocorrelation of prices) proposed as a measurement. Lastly, price accuracy reflects the true value of ETs, aiming to capture the maximum share of MEV while remaining attractive to participants, measured similarly to MEV capture.

In table 2 we outline the design space of possible configurations of Execution Tickets.

| Ticket Attributes | Configurations |
| --- | --- |
| Amount of tickets | Variable / Fixed |
| Expiring tickets | Yes / No |
| Refundability | Yes / No (unallocated & allocated) |
| Resalability | Yes / No (unallocated & allocated) |
| Enhanced Lookahead | No / Yes (x epochs) |
| Possible Pricing Mechanisms | FPA, SPA, EIP-1559 style, AMM style |
| Target Amount | # of tickets (for variable / fixed) |

*Table 2: Outline of possible execution ticket configurations*

While most attributes are straightforward, we will provide some background on the pricing mechanisms. Unlike MEV-Boost, where rewards may go to block producers, Execution Ticket earnings are intended to benefit protocol token holders by being burned, thereby increasing social welfare [10]. Fixed pricing mechanisms are deemed inefficient for maximizing social welfare [11], so the focus is on dynamic pricing mechanisms.1

The pricing mechanisms are categorized into two main categories being auction-based and adaptive quoted price formats:

1. First-Price Auctions (FPA): Bidders submit bids without knowing others’ bids, and the highest bidder wins and pays their bid amount. FPAs often lead to bid shading, where bidders underbid their true valuations, resulting in inefficiencies and high volatility. Sealed-bid first price auctions are not DSIC (Dominant Strategy Incentive Compatible) [5]. Open ascending-bid first price auctions can be DSIC (h/t to Julian for pointing this out!). As they behave similarly to SPAs, we focused on sealed-bid FPAs.
2. Second-Price Auctions (SPA): Also known as Vickrey auctions, bidders submit sealed bids, and the highest bidder wins but pays the second-highest bid. This format encourages truthful bidding since bidders pay less than or equal to their true intrinsic value. While SPAs are almost OCA-proof (Off-Chain Agreement proof), they may be susceptible to manipulation through fake bids [13]. However, since Execution Ticket earnings are burned rather than rewarded to validators, this risk is mitigated but might make them more susceptible to off-chain agreements.
3. Adapted EIP-1559 Pricing: An adapted version of EIP-1559 for Execution Tickets involves the protocol quoting a price that adjusts similarly to EIP-1559. However, while for EIP-1559 the adjustment is based on the gas usage, for Execution Tickets it needs to be based on the number of outstanding tickets relative to a target amount. Tickets could either be sold on a continuous basis where ticket holders can always buy a ticket from the protocol if they desire or in a batch process where at each slot between zero and a specified maximum of tickets are sold. While EIP-1559 has been effective in maintaining gas usage near the target [14], its retroactive price adjustments may lag during MEV spikes making it more challenging for Execution Tickets.
4. Adapted AMM-like Pricing: The adapted version of an AMM-like pricing entails the protocol dynamically updating the price of the tickets based on a bonding curve and the amount of outstanding tickets. Here as well a target amount of outstanding tickets needs to be defined and the bonding curve function needs to be adapted and carefully designed. In the research paper we outline three options how this might be adapted and implement one in the simulation. However, this remains the scope of future research on how to best adapt it.

# Potential Mechanism Designs

To substantiate the parameters, several possible mechanism designs are outlined. Given that based on the categorial parameters alone already 512 configurations are possible2, only sample mechanism designs are evaluated. In more detail, the following configurations are evaluated:

|  | Simple FPA auction | JIT second price slot auction | Flexible 1559-style | Fixed SPA | Flexible, refundable AMM | Fixed, resellable FPA |
| --- | --- | --- | --- | --- | --- | --- |
| Amount of tickets | Fixed | Fixed | Flexible | Fixed | Flexible | Fixed |
| Expiring tickets | Yes | Yes | No | No | No | No |
| Refundability | No (unallocated & allocated) | No (unallocated & allocated) | No (unallocated & allocated) | No (unallocated & allocated) | Yes (unallocated) | No (unallocated & allocated) |
| Resalability | No (unallocated & allocated) | Yes (allocated) | Yes (unallocated & allocated) | No (unallocated & allocated) | No (unallocated & allocated) | Yes (unallocated & allocated) |
| Enhanced Lookahead | No | Reduced | Yes for Execution Validators | Yes for Execution Validators | No | No |
| Pricing Mechanisms | FPA | SPA | 1559-style | SPA | AMM | FPA |
| Target Amount | 32 | 1 | undefined | 1024 | undefined | 1024 |

*Table 3: Overview of possible mechanism design configurations*

# Simulation Results

[![Table 4: Simulation results on selected mechanism designs](https://ethresear.ch/uploads/default/optimized/3X/5/2/52f19e983ee79da55161fd3e6ffde9edfbc61075_2_656x500.png)Table 4: Simulation results on selected mechanism designs1256×956 95.3 KB](https://ethresear.ch/uploads/default/52f19e983ee79da55161fd3e6ffde9edfbc61075)

Generally, the simulation results of over 300 simulation runs show that in all configurations decentralization remains a challenge. None of the configuration scores particularly well on the decentralization metrics. This is driven by the diverse abilities of ticket holders (based on [15], [16]) and the fact that in most scenarios the bids are based on expected future valuations which leaves out specialization factors. It shows that in cases with a secondary market enabled, the centralization forces are reduced. This derives from specialized ticket holders being able to more accurately estimate the true value of MEV for a slot in just-in-time (JIT) auctions and thereby winning the auction. With regards to MEV capture, we can see different attributes emerge. The auction formats generally score well, similarly the AMM-style pricing scores well. The 1559-style pricing is capturing less MEV due to a step-wise and less dynamic price adaptation mechanism. With regards to the price predictability, smoothness and accuracy we can observe that the auction formats that operate with a longer lookahead are very predictable and smooth, while JIT auctions and a 1559-style pricing are less smooth.

## Findings on Auction Formats

### First Price Auctions

With regards to first price auctions, we saw a “winner’s curse” play out, in the terms that assuming that bidders have differing intrinsic value expectations for a ticket which are following a normal distribution, the most optimistic bidders wins. And the most optimistic bidder with the highest valuation overestimates the value the most and thereby makes a loss on the trade. This is a known problem of auctions (e.g. [17]). However, noteworthy to point out, as this leads to higher “risk-adjustments” by bidders which in turn could lead to reduced MEV capture by the protocol.

With regards to the simulation it shows that first price auctions generally perform well, however two things need to be critically challenged here. Firstly, we have implemented it as a sealed bid auction, as we assume the operational communication overhead for a leaderless auction with ascending bids is too high. Therefore, holding sealed-bid on-chain auctions must be feasible. As outlined in the research report, several proposals for this are currently being discussed, however still in the earlier stages [18], [19]. Secondly, as sealed-bid first price auctions are not DSIC, no single dominant bidding strategy exists. Hence, in the simulation the bidding is based on a heuristical bidding strategy where bidders have no information on the intrinsic valuations of other bidders. This assumption will not hold true in multi-round scenarios of Execution Ticket selling. So more sophisticated bidding strategies based on historical bids of competitors might emerge that might potentially reduce the captured MEV. So it is unclear yet if first price auctions can be actually designed in this scenario in a way to behave differently than second price auctions.

### Second Price Auctions

For second price auctions we observed that the MEV capture highly depends on the competitiveness of the specific simulation. In cases with at least two similarly strong ticket holders, the MEV capture was high. However, on average it was only medium, given the missing competition.

###

*Figure 1: Example simulation results for second price auctions with two similarly capable ticket holders (Source: 2024-09-24_10-52 UTC, runs: 10, time steps: 1000)*

### EIP-1559 Style Pricing

As outlined above, the EIP-1559 pricing needs to be adapted to work with Execution Tickets and we have implemented it as a batch process. However, we observe that this leads to self-reinforcing oscillating ticket prices. Even adjusting the price adjustment factor does not lead to better outcomes in our simulations. This leads to the conclusion that a batch update process is not sufficient. How a continuous price update process can be technically implemented in a decentralized setting remains an open question. Overall, the pricing mechanism needs to be carefully designed to achieve the desired price behavior.

[![](https://ethresear.ch/uploads/default/optimized/3X/c/a/cad8cf204af75bf9d5caa565640a53513c6b1ffc_2_512x306.png)1000×600 35.8 KB](https://ethresear.ch/uploads/default/cad8cf204af75bf9d5caa565640a53513c6b1ffc)

*Figure 2: Price curve for EIP-1559 style pricing*

Further, in certain simulations4 we have observed that if one ticket holder has a significantly higher willingness to pay, the prices stabilize at a point where only this ticket holder is able to purchase tickets, leading to a high centralization.

### AMM-style Pricing

For the AMM-style pricing as outlined above it needs to be adapted to be suitable for Execution Tickets. Running configurations with AMM–style pricing shows that the pricing mechanism can be sensitive to the adjustment factor. A too slow adoption does not accurately capture the demand, a too large adaption factor is not granular enough to differentiate the expected valuations and would lead to a latency race.

However, the simulations show promising results that this mechanism is able to capture a high level of MEV. From an operational perspective it remains to be investigated how this could be implemented to suit the selling process needed for Execution Tickets.

### Conclusion on Auction Formats

Taking into consideration the different observations, based on the simulation results we conclude that an auction based format, most probably second price auction, is the most feasible format. It leads to a high captured MEV, is DSIC and leads to favorable price properties in the simulation. An AMM-style pricing seems also to be a promising solution, however more open design questions on mechanism and implementation remain.

One relevant question remains open around OCA-proofness, in case the ET earnings are burned. There might be a sybil attack vector where block builders bribe the actor / committee defining the winning bid and thereby being able to achieve a lower price. E.g. if the winning bid is 10 ETH, the block builder however pays the committee members 5 ETH to artificially set the winning bid price at 1 ETH, there could be a 4 ETH profit margin. To avoid this, bids or prices would need to be on-chain which is not feasible given the time horizon of the auction. Another option could be a leaderless auction as outlined by [20].

### Findings on Ticket Attributes

We observe that the question of a fixed vs. a variable amount of tickets is closely related to the pricing mechanism. For certain mechanisms, fixed amounts of tickets make more sense (auctions) while for others (EIP-1559 and AMM-style) a flexible amount is better. Hence, we see this more as a secondary attribute that is deducted from the pricing mechanism.

Regarding expiring tickets, we observe in the simulation that especially for short expiry times the MEV capture is impaired, as ticket buyers need to discount the value of a ticket on the primary market and on the secondary market since the possibility of a ticket expiry without redemption needs to be priced in. This leads to generally lower captured MEV values. Further, we observe that it has secondary complications as the pricing of each actor becomes more sophisticated as the expiry period, outstanding tickets etc. need to be factored in. This leads to the conclusion that non-expiring tickets seem to be the favorable configuration.

Regarding refundability, we only observe limited effects on the market dynamics with the tested discount (around 20 %). It leads to more security for ticket holders. However, this depends on the discount. Further it is closely related with the secondary market. In case a secondary market exists, this option is often more attractive to dispose of tickets. It shows that allowing for refundability does not influence the mechanism in a substantial way and complicates the design choices as well as the decisions for ticket holders. Hence, the preliminary analysis leads to the conclusion that tickets shall not be refundable.

Regarding the secondary market, an interesting finding is that this increases decentralization. Due to the ability of more specialized ticket holders to buy tickets just-in-time in periods where they are able to capture higher MEV due to specialization. Further, it leads to overall higher MEV captured due to reduced risks for the primary ticket holders. Additionally, we observe that in some configurations with discrete pricing (e.g. AMM-style pricing) it leads to arbitrage opportunities, if the AMM-pricing is not adapting fine granularly enough and tickets can be bought by the ticket holder with the lowest latency and then be resold at a higher price at the secondary market. Given that also from a technical perspective it is difficult to prevent a secondary market, a preliminary recommendation is rather embrace the benefits of it and try to foster it.

# Limitations

Our research did not focus on the beacon round attestation and the secondary effects ETs might have on it.

Additionally, we did not focus on the specific details of inclusion lists. They are briefly discussed in the research report as a potential mechanism to ensure liveness, but in the simulation and configurations it will not be a focus of the work. This ties closely to multi-block MEV. As we have shown in our [previous work](https://ethresear.ch/t/does-multi-block-mev-exist-analysis-of-2-years-of-mev-data/20345), it has historically not been structurally observed, however might be a concern for Execution Tickets. The topic is hence briefly discussed in the research report, but not in-depth evaluated and not implemented in the simulation. Further, timing games are not included in the simulation. Additionally, assuming sealed-bid auctions, we work with static demand functions of the ticket holders that do not take into consideration the bids of other ticket holders. In addition, considerations around private order flow are not modeled in the simulation. Furthermore, the role of relays is left out and we don’t simulate missed blocks and missed block penalties.

Regarding the pricing mechanisms, we propose initial versions of how they can be designed, however leave the verification and formal definition to future research. This includes the more in-depth research of specific parameters such as adjustment steps for EIP-1559-style pricing and others. We only look at this from an exploratory perspective.

Further, we exclude a more in-depth analysis around the burning mechanism of the earnings from the Execution Ticket sales. As outlined in [21], burning mechanisms usually impair the OCA-proofness of mechanisms.

# Conclusion

Execution Tickets present a promising next evolutionary step for enhancing Ethereum’s block space allocation mechanism. It separates consensus rewards from execution rewards and sells the execution rights in an effective manner. It aims to foster decentralization among beacon chain validators and enables protocol-level capture of Maximum Extractable Value (MEV).

We developed a theoretical framework identifying three primary objectives of an Execution Ticket mechanism design: decentralization, MEV capture, and Block Producer Incentive Compatibility (BPIC). Further, we propose metrics on how to measure the objectives. For decentralization we propose to use the highest market share, Nakamoto coefficient, and Herfindahl-Hirschman Index, while for MEV capture we propose to measure the MEV share of the protocol from Execution Ticket holder earnings. Further, the three price characteristics of price predictability, smoothness and accuracy are identified as desired attributes.

To evaluate the parameters and configurations, we implemented an agent-based simulation and based on over 300 simulation runs several findings are concluded. Results indicate that while none of the mechanisms scores particularly well on decentralization, enabling a secondary market reduces centralization by allowing specialized ticket holders to purchase tickets just-in-time. Regarding MEV capture, auction formats and AMM-style pricing performed well, whereas EIP-1559-style pricing captures less MEV and has stronger price fluctuations. Auction formats with longer lookahead periods demonstrated favorable price predictability and smoothness while scoring slightly less favorable on price accuracy.

Based on this, a second-price auction format seems most promising as it achieves high MEV capture, adheres to Dominant-Strategy Incentive Compatibility (DSIC) and exhibits favorable price characteristics. First-price auctions and AMM-style pricing formats show promising results in the simulation as well, however leave more questions open from a theoretical mechanism perspective. Non-expiring tickets score better as they avoid impairing MEV capture due to discounted valuations from expiry risk. Refundability was found to have limited impact on market dynamics and adds complexity; thus, non-refundable tickets are suggested. Embracing a secondary market seems favorable, as it enhances decentralization and increases overall MEV capture. Nevertheless, in line with [22] and [23] we observe that the decentralization of the builder market is challenging and highly depends on the MEV extraction capabilities of the top builders.

Overall, inline with previous theoretical work [2], [22], [24] we conclude that Execution Tickets pose a promising mechanism to foster beacon chain validator decentralization and capture MEV at protocol level. However, questions remain around block builder centralization, proneness to off-chain agreements and multi-block MEV.

# References

[1] C. Schwarz-Schilling, F. Saleh, T. Thiery, J. Pan, N. Shah, and B. Monnot, “Time is Money: Strategic Timing Games in Proof-of-Stake Protocols,” May 2023, [Online]. Available: [[2305.09032] Time is Money: Strategic Timing Games in Proof-of-Stake Protocols](http://arxiv.org/abs/2305.09032)

[2] J. Burian, D. Crapis, and F. Saleh, “MEV Capture and Decentralization in Execution Tickets,” Aug. 21, 2024, arXiv: arXiv:2408.11255. Accessed: Oct. 14, 2024. [Online]. Available: [[2408.11255] MEV Capture and Decentralization in Execution Tickets](http://arxiv.org/abs/2408.11255)

[3] C. Schlegel, “Inelastic vs. Elastic Supply: Why Proof of Stake Could Be Less Centralizing Than Execution Tickets - Research,” The Flashbots Collective. Accessed: Oct. 14, 2024. [Online]. Available: [Inelastic vs. Elastic Supply: Why Proof of Stake Could Be Less Centralizing Than Execution Tickets - Research - The Flashbots Collective](https://collective.flashbots.net/t/inelastic-vs-elastic-supply-why-proof-of-stake-could-be-less-centralizing-than-execution-tickets/3816)

[4] J. Lee, B. Lee, J. Jung, H. Shim, and H. Kim, “DQ: Two approaches to measure the degree of decentralization of blockchain,” ICT Express, vol. 7, no. 3, pp. 278–282, Sep. 2021, doi: 10.1016/j.icte.2021.08.008.

[5] T. Roughgarden, “Transaction Fee Mechanism Design,” ACM SIGecom Exch., vol. 19, no. 1, pp. 52–55, 2021, doi: 10.1145/3476436.3476445.

[6] M. Bahrani, P. Garimidi, and T. Roughgarden, “Transaction Fee Mechanism Design with Active Block Producers,” 2023, [Online]. Available: [[2307.01686v2] Transaction Fee Mechanism Design with Active Block Producers](https://arxiv.org/abs/2307.01686v2)

[7] L. Heimbach, L. Kiffer, C. Ferreira Torres, and R. Wattenhofer, “Ethereum’s Proposer-Builder Separation: Promises and Realities,” Proc. ACM SIGCOMM Internet Meas. Conf. IMC, pp. 406–420, May 2023, doi: 10.1145/3618257.3624824.

[8] S.-H. Poon and C. W. J. Granger, “Forecasting Volatility in Financial Markets: A Review,” J. Econ. Lit., vol. 41, no. 2, pp. 478–539, Jun. 2003, doi: 10.1257/002205103765762743.

[9] S.-K. Tan, J. S.-K. Chan, and K.-H. Ng, “On the speculative nature of cryptocurrencies: A study on Garman and Klass volatility measure,” Finance Res. Lett., vol. 32, p. 101075, Jan. 2020, doi: 10.1016/j.frl.2018.12.023.

[10] A. Kiayias, P. Lazos, and J. C. Schlegel, “Would Friedman Burn your Tokens?,” Papers, 2023, [Online]. Available: [Would Friedman Burn your Tokens?](https://ideas.repec.org/p/arx/papers/2306.17025.html)

[11] V. Buterin, “Blockchain Resources Pricing.” 2019. Accessed: Mar. 21, 2024. [Online]. Available: [research/papers/pricing/ethpricing.pdf at 139e3dd83b06fae918792c495b8ccd0d1635b0d4 · ethereum/research · GitHub](https://github.com/ethereum/research/blob/139e3dd83b06fae918792c495b8ccd0d1635b0d4/papers/pricing/ethpricing.pdf)

[12] M. Neuder, P. Garimidi, and T. Roughgarden, “On block-space distribution mechanisms - Proof-of-Stake / Block proposer,” Ethereum Research. Accessed: Oct. 28, 2024. [Online]. Available: [On block-space distribution mechanisms](https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764)

[13] M. Akbarpour and S. Li, “Credible Auctions: A Trilemma,” Econometrica, vol. 88, no. 2, pp. 425–467, 2020, doi: 10.3982/ECTA15925.

[14] Y. Liu, Y. Lu, K. Nayak, F. Zhang, L. Zhang, and Y. Zhao, “Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security,” Proc. ACM Conf. Comput. Commun. Secur., pp. 2099–2113, 2022, doi: 10.1145/3548606.3559341.

[15] S. Yang, K. Nayak, and F. Zhang, “Decentralization of Ethereum’s Builder Market,” May 2024, [Online]. Available: [[2405.01329v3] Decentralization of Ethereum's Builder Market](https://arxiv.org/abs/2405.01329v3)

[16] B. Öz, D. Sui, T. Thiery, and F. Matthes, “Who Wins Ethereum Block Building Auctions and Why?,” Jul. 18, 2024, arXiv: arXiv:2407.13931. Accessed: Oct. 02, 2024. [Online]. Available: [[2407.13931] Who Wins Ethereum Block Building Auctions and Why?](http://arxiv.org/abs/2407.13931)

[17] M. H. Bazerman and W. F. Samuelson, “I Won the Auction But Don’t Want the Prize,” http://dx.doi.org/10.1177/0022002783027004003, vol. 27, no. 4, pp. 618–634, 1983, doi: 10.1177/0022002783027004003.

[18] H. S. Galal and A. M. Youssef, “Verifiable Sealed-Bid Auction on the Ethereum Blockchain,” 2018, 2018/704. Accessed: Oct. 14, 2024. [Online]. Available: [Verifiable Sealed-Bid Auction on the Ethereum Blockchain](https://eprint.iacr.org/2018/704)

[19] P. Momeni, S. Gorbunov, and B. Zhang, “FairBlock: Preventing Blockchain Front-Running with Minimal Overheads,” in Security and Privacy in Communication Networks, vol. 462, F. Li, K. Liang, Z. Lin, and S. K. Katsikas, Eds., in Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, vol. 462. , Cham: Springer Nature Switzerland, 2023, pp. 250–271. doi: 10.1007/978-3-031-25538-0_14.

[20] D. White, D. Robinson, L. Thouvenin, and K. Srinivasan, “Leaderless Auctions,” Paradigm. Accessed: Oct. 04, 2024. [Online]. Available: [Leaderless Auctions - Paradigm](https://www.paradigm.xyz/2024/02/leaderless-auctions)

[21] T. Roughgarden, “Transaction Fee Mechanism Design for the Ethereum Blockchain: An Economic Analysis of EIP-1559,” 2020, [Online]. Available: [[2012.00854v1] Transaction Fee Mechanism Design for the Ethereum Blockchain: An Economic Analysis of EIP-1559](https://arxiv.org/abs/2012.00854v1)

[22] M. Bahrani, P. Garimidi, and T. Roughgarden, “Centralization in Block Building and Proposer-Builder Separation,” Jan. 2024, [Online]. Available: [[2401.12120] Centralization in Block Building and Proposer-Builder Separation](http://arxiv.org/abs/2401.12120)

[23] M. Pan, A. Mamageishvili, and C. Schlegel, “On sybil-proof mechanisms,” Jul. 22, 2024, arXiv: arXiv:2407.14485. Accessed: Oct. 28, 2024. [Online]. Available: [[2407.14485] On Sybil-proof Mechanisms](http://arxiv.org/abs/2407.14485)

[24] J. Burian, “The Future of MEV - An Analysis of Ethereum Execution Tickets,” 2024. [Online]. Available: [[2404.04262] The Future of MEV](https://arxiv.org/abs/2404.04262)

---

*1 Note that further pricing mechanism proposals exist with winning changes being proportional to the paid price as e.g. outlined in [12]*

*2 2 (Amount of Tickets) * 2 (Expiring Tickets) * 4 (Refundability) * 4 (Resalability) * 2 (Enhanced Lookahead) * 4 (Pricing Mechanisms)*

*3 Results based on 10 runs with 1000 timesteps for each configuration. Color coding of results based on literature and subjective judgment*

*4 E.g. see simulation results 2024-05-14_18-09_1_1000_EIP-1559 for details*
