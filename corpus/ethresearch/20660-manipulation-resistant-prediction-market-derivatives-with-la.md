---
source: ethresearch
topic_id: 20660
title: Manipulation-Resistant Prediction Market Derivatives with Language Models
author: marcgraczyk
date: "2024-10-15"
category: Economics
tags: []
url: https://ethresear.ch/t/manipulation-resistant-prediction-market-derivatives-with-language-models/20660
views: 8804
likes: 12
posts_count: 6
---

# Manipulation-Resistant Prediction Market Derivatives with Language Models

# Manipulation-Resistant Prediction Market Derivatives with Language Models

*Thanks to [Diego](https://x.com/0xfuturistic) for profound discussions that led to this work.

Thanks also to [Sam Hart](https://x.com/hxrts), [David Crapis](https://x.com/DavideCrapis), [Swapnil](https://x.com/swp0x0), [Jorik](https://x.com/mempoolsurfer) and [Finn](https://x.com/f_casey_fierro) for feedback and review.*

![:dvd:](https://ethresear.ch/images/emoji/facebook_messenger/dvd.png?v=14)**TL;DR:** *LLM-based prediction derivatives offer a novel solution to manipulation risks of traditional prediction market derivatives, as well as a new primitive to support potentially richer event landscapes within prediction markets. By using language models to generate index prices, this approach decouples derivatives from manipulable spot markets. Mathematical proofs support the solution’s robustness, while additional strategies that fortify the system reliability are proposed.*

[![super_forecaster](https://ethresear.ch/uploads/default/optimized/3X/3/0/30495fc69ce07b1ad3bef0346e87ec8c2b42e6b4_2_500x500.png)super_forecaster1024×1024 332 KB](https://ethresear.ch/uploads/default/30495fc69ce07b1ad3bef0346e87ec8c2b42e6b4)

Prediction markets effectively aggregate information and forecast events. However, derivative prediction markets introduce a new risk: manipulation of the underlying “spot” market that determines the derivative’s index price.

A recent [failed attack](https://cmsholdings.substack.com/p/failed-polymarket-oracle-attack) on Polymarket exemplifies this vector. On September 6, 2024, an attacker targeted a 2024 US Presidential election derivative market by:

1. Acquiring a large position in the derivative market;
2. Attempting to push the price down in the “spot” market by spending about $7 million;
3. Receiving a $1.5 million payout if successful.

Though this attempt failed, similar vulnerabilities have been successfully exploited on lending markets with analogous market structure, as with [Mango Markets](https://blockworks.co/news/mango-markets-mangled-by-oracle-manipulation-for-112m). These events highlight a key systemic risk inherent in derivative prediction markets.

# LLM-Based Derivatives

As a reminder the key components of a perpetual contract are:

- the mark price, i.e the price at which the perp is traded
- the index price, i.e the price of the underlying asset that is tracked by the perp
- the funding rate, exchanged between the longs and the shorts as the mark price moves away from the index price
- collateral needed to open a position

The perpetual can track for example the mid-price of a ‘YES’ token traded on a prediction market, thereby becoming a prediction market derivative.

Instead of using information endogenous to the prediction market to generate the index price we propose using large language models (LLMs). By decoupling the derivative from spot markets and leveraging diverse, credible sources, this approach is potentially offering greater resistance to manipulation than traditional prediction markets, where any participant can influence the price.

The LLM can be interpreted as a mechanism to commoditize the changing qualitative public information. By aggregating the current information landscape into a probability, it can set a price on which one can build a tradeable instrument. Here is a more precise description of the structure of such a perp:

- the index price is a moving average of the probability calculated by the LLM.
- the longs bet on the likelihood of the event increasing.
- the shorts bet on the likelihood of the event decreasing.
- the funding rate is paid depending on how the derivative market prices the odds compared to the LLM (how much information is hidden from the LLM).

Recent research supports LLMs’ forecasting capabilities. The study [“Approaching Human-Level Forecasting with Language Models”](https://arxiv.org/pdf/2402.18563v1) by Halawi et al. found that a fine-tuned LLM nearly matched and outperformed in some scenarios human forecasters on Polymarket events, having the potential to become a “superforecaster”. This suggests LLMs could effectively serve as oracles for index prices, allowing the creation of derivative instruments from events with thin or non existing spot markets.

## Information Aggregation

The LLM functions as a computational agent, aggregating and automatically incorporating publicly available information. Traders, in contrast, contribute private information through their trading activity.

The system’s manipulation resistance is bolstered by the LLM’s source-weighting mechanism. This limits the impact of manipulating any single information source to the weight the LLM assigns to it. Consequently, the lower an individual source’s weight relative to others, the more resistant the system becomes to manipulation attempts targeting that source.

Let S be the set of all sources used by the LLM. We consider a simple model where the LLM generates its probability P as a weighted average of probabilities from all sources and where all sources are independent: P=\sum_{j \in S}(w_j*p_j). This corresponds effectively to an ensemble probability from multiple LLM inferences on independent data. However, the LLM could generate P differently and sources could have dependencies.

![:open_book:](https://ethresear.ch/images/emoji/facebook_messenger/open_book.png?v=14) **Theorem 1** (*Manipulation Resistance of Weight-Adjusted Sources*)**:** Under the model above, let P be the LLM-generated probability for an event and P_i be the probability that would be generated if source i were manipulated. Then:

|P - P_i| ≤ w_i

where w_i is the weight assigned to source i by the LLM, with \sum w_i=1.

- Proof
Let S_{-i} be the set of all sources except i.
If source i is manipulated, the new probability P_i would be:

P_i=w_i*p_i'+\sum_{j \in S_{-i}}(w_j*p_j)

 where p_i' is the manipulated probability from source i.
 The difference between P and P_i is:

|P-P_i|=|w_i*(p_i-p_i')|

 The maximum possible difference between p_i and p_i' is 1. Therefore,

|P-P_i| \leq w_i

 \blacksquare

This theorem provides a quantifiable measure of manipulation resistance, directly linked to the source weights used by the LLM. Assuming indepence between the information sources, it demonstrates that *LLM-based prediction derivatives* become increasingly resistant to manipulation as the weight assigned to any individual source approaches zero.

![:open_book:](https://ethresear.ch/images/emoji/facebook_messenger/open_book.png?v=14) **Corollary 1** (*Manipulation Resistance of Equally Weighted Sources*)**:** If the LLM uses at least n equally weighted independent sources, then:

|P-P_i|\leq\ \frac{1}{n}

where P is the LLM-generated probability for an event and P_i is the probability that would be generated if source i were manipulated.

- Proof
 If sources are equally weighted, then w_i=\frac{1}{n} for all i.
 Thus, from Theorem 1:

|P-P_i|\leq w_i=\frac{1}{n}

 \blacksquare

This corollary shows that increasing the number of equally-weighted sources reduces the impact of manipulating any single source. Intuitively, the number of available information sources tends to grow as an event nears its resolution, further enhancing the system’s resistance to manipulation.

# LLM-Based Prediction Perpetuals

We formally introduce perpetuals on event probabilities where an LLM generates the index price instead of traditional markets.

Let P be the LLM-generated probability. The perpetual is thus governed by:

\text{Collateral ratio} = \frac{\text{Equity}}{\text{Debt}} = \frac{\text{Collateral quantity} * \text{Collateral price}}{\text{Perpetual quantity} * P*\$1}

We multiply the denominator by $1  since P is a probability, ensuring unit consistency with the numerator.

A funding rate mechanism aligns the traded price (mark) with the LLM-generated probability (index), with the gap intuitively being proportional to how much information is hidden from the LLM.

\text{Funding} = \text{Mark} - \text{Index} = \text{Mark} - P

## Information Aggregation: informational substitutes

A different model of the LLM aggregation mechanism consists in the LLM performing Bayesian updates over a common prior on received individual signals. When presented with all signals simultaneously, it can aggregate them into a single probability estimate. The probability P_t then becomes the result of the most recent Bayesian update over the last set of signals.

Formally, the LLM estimates a common prior P_{LLM}. We denote the variable corresponding to the binary outcome underpinning the market as Y.  As the LLM receives n different signals \{x_1, \dots, x_n\} it outputs a price P = P_{LLM}(Y=1|x_1, \dots, x_n).

Two signals are considered informational substitutes if they are conditionally independent given the ground truth. This is an important condition in the prediction market literature [ensuring incentive-compatibility](https://arxiv.org/pdf/1703.08636).

Such a model allows to study the case of a single LLM inference aggregating multiple substitutable signals or of successive LLM inferences on substituable signals. One signal may correspond to a set of information sources.

![:open_book:](https://ethresear.ch/images/emoji/facebook_messenger/open_book.png?v=14) **Theorem 2** (*Manipulation Resistance of the LLM Under Informational Substitutes Condition*): Under reasonable assumptions about the information structure, if the LLM has access to a sufficient number of signals that are informational substitutes, a malicious agent attempting to manipulate a signal can only expect to bias the final price by at most \epsilon.

- Proof
 This result stems from a reinterpretation of Lemma 1 and Theorem 1 from “Self-Resolving Prediction Markets for Unverifiable Outcomes” by Srinivasan et al.

 We consider a particular signal t that a malicious agent tampers with, resulting in a modified signal \tilde{x_t}.  The LLM also has access to another set of information sources x_{-t}, denoted simply as x_r, where \Omega_r corresponds to the underlying signal space’s structure. The LLM would produce a price P_{LLM}(Y=1 | x_t) upon receiving the true signal x_t.
 We assume crucially that the agent cannot access this information set during manipulation. This assumption holds if the LLM updates instantly from numerous sources (leaving the agent no time to access them) or, alternatively, if we consider each signal as associated to a particular time t. The LLM then first receives the manipulated signal along with the signal from other public sources bundled in \tilde{x_t}, and some time later it receives updates from non manipulated sources as x_r. The latter is perhaps especially interesting if the sources update rapidly over time.
 According to the aforementioned lemma, we have:

E [P_{LLM}(Y=1 | x_r, \tilde{x_t}) | x_t] = P_{LLM}(Y=1 | x_t) + \Delta(\Omega_r, \tilde{x_t}, x_t)

 This equation indicates that the malicious agent’s expectation of the LLM’s price after aggregating other information sources under x_r is affected by an error term dependent on the false report \tilde{x_t}. A larger error term implies greater price manipulation potential.
 Theorem 1 demonstrates that if \Omega_r comprises signals that are information substitutes, the error term can be minimized as the number k of substitutes increases.
 \blacksquare

This theorem demonstrates that when the LLM has access to information sources that are informational substitutes, a malicious agent’s ability to manipulate the final price is significantly limited. Theorem 1 can be of complementary value since one could ensemble several inferences on substitutable signals.

## Market Efficiency

This derivative may achieve a novel form of efficiency, with the LLM rapidly incorporating public information and trading activity integrating private information.

![:open_book:](https://ethresear.ch/images/emoji/facebook_messenger/open_book.png?v=14)**Theorem 3** (*Efficiency of LLM-Based Prediction Perpetuals*)**:** Let P_t be the LLM-generated probability at time t, M_t be the mark price of the perpetual at time t, and I_t be the public information set available at time t. Denote by \delta_t a delta-Dirac function corresponding to a price jump in the mark price related to the arrival of private information. Then:

1. |E[P_t|I_t]-P_t|\leq \epsilon_{\text{LLM}} (LLM Efficiency)
2. Outside of the arrival of private information, P_t \approx M_t (mean reversal)
3. When \delta_t becomes positive and the mark price jumps, after a relaxation time P_t jumps as well (feedback loop between the LLM and the market)

- Proof

 LLM Efficiency: By design, the LLM processes all available public information I_t to generate P_t. The bound \epsilon_{\text{LLM}} represents the maximum error in this process.
- Let f(t)=k(M_t-P_t) be the funding rate at time t, where 1>k>0 is a constant. If M_t>P_t, then f(t)>0, incentivizing traders to sell and driving M_t down. If M_t0 is the speed of adjustment, \sigma is the volatility, and W_t is a Wiener process.
We assume P_t is a slowly changing random variable. This is a realistic assumption since the news landscape does not change suddenly. Then for a time period [t_0,t_1] we have P_t(\omega) \approx P(\omega). The SDE above then gives

|E[M_t]-P(\omega)|=|P(\omega)-M_{t_0}|e^{-k(t-t_0)}

 We hence see exponential mean reversal and P_t \approx M_t under normal market conditions. One can also notice that the error bound on aggregating public information depends entirely on the LLM.
We now introduce \delta_t in the SDE above to account for private information:

dM_t=\alpha(P_t-M_t)dt+ \eta\delta_tdt + \sigma d W_t

 We suppose that \delta=0 outside of ]t(\omega), t(\omega) + \epsilon(\omega)[ where t and \epsilon are random variables, \delta_t>0 inside the interval and \int_{\mathbb{R}} \delta_t =1. The term \eta(\omega) is a random variable quantifying the magnitude of the jump, it can be equal to \pm \eta. Since before t^*=t(\omega) we have M_t\approx P_t it is reasonable to assume that during the time \epsilon(\omega) we have:

dM_t = \eta\delta_tdt + \sigma d W_t

 Thus the average price increase is \eta. We can therefore have the simplified assumption that M_t= M_{t_0} for t t^* + \epsilon(\omega) where t_0 >t^* one finds that:

M_{t_0} + \eta \approx P(\omega)[1-e^{-k(t-t^*)}]

 Hence indeed for large t we must have P_t \approx M_{t_0} + \eta, and the LLM is obliged to follow the initial jump.
\blacksquare



This theorem formalizes the novel form of semi-strong efficiency of LLM-based prediction derivatives (all the public information is priced in), combining LLM information processing with market price discovery.

## Ensuring Further Robustness

The LLM’s design must be resilient to errors such as omissions or inconsistencies. It should rely on credible, manipulation-resistant information sources and strive for maximum observability.

To enhance system reliability and resist manipulation, there exist more strategies:

- Verified information retrieval: Certify the LLM’s data retrieval from specific websites (e.g., using TLSNotary) to ensure information pipeline integrity, crucial for decentralized LLM operations.
- Whitelisting: Restrict the LLM’s sources to ensure authority and relevance.
- Adapted retrieval: Customize priority, API modules, and whitelists based on event types (e.g., sports vs. space flight).
- Contract price tracking: Implement LLM feedback loops to promote convergence between index and mark prices, complementing funding rates and price convergence to 0 or 1.
- LLM prediction ensembling: Reduce variations and inconsistencies by combining multiple predictions.
- Inclusion list mechanism: Require the LLM to review specific data regardless of its internal retrieval decisions.
- Data-backed model identification: Implement a complex ontology to benchmark LLM forecasting, as described in this paper.
- Multi-LLM averaging: Mitigate LLM-specific biases (e.g., poor calibration, overconfidence) through a “wisdom of the silicon crowd” approach with possibly multiple competing LLMs.
- Permissionless mechanism with TEE: the LLM weights could be pre-committed and anyone could re-run the LLM to verify the output. Further, the final prompts could come from various participants (cf. this paper for a general discussion of such mechanisms).

# Extending the event landscape

Prediction markets still support a very limited set of markets. A vast domain such as “science” only contains around 30 markets on Polymarket. By producing a dynamic price which updates as new information comes without the need for initial capital, the LLM could support virtually any market as long as it has access to reliable information sources.

Efficiently exploring the space of possible events through ‘super-questioners’ (the symmetrical role to ‘super-forecasters’) could be crucial to the understanding of the ‘existential’ questions that matter most, as suggested by this [research report](https://static1.squarespace.com/static/635693acf15a3e2a14a56a4a/t/66ba37a144f1d6095de467df/1723479995772/AIConditionalTrees.pdf).

# Closing thoughts

We assumed that LLMs can have some inherent efficiency in aggregating public information into a probability. We also assumed that such forecasting LLMs could realistically be within the manipulation bounds we outlined above. We expect it to be the case if the information structure presented to the LLM is sufficiently rich.

Under these assumptions, the key claim that building a prediction market derivative using an LLM as an index price is both possible and efficient rests on the last result presented above which ensures that the funding rate can drive mean-reversion towards truthful resolution. The first results support the claim that \epsilon_{LLM} can be chosen small enough.

The general intuition is that P_t is a proxy for aggregating the public signals and M_t is a proxy for aggregating public and private signals, while the funding rate drives the derivate price in the correct direction over time.

LLM-based prediction derivatives offer a novel solution to a key manipulation risk in derivative prediction markets. By decoupling from potentially manipulable spot markets, this approach aims to remove a major obstacle in developing derivative markets for event probabilities. We expect this solution to encourage experimentation with prediction market derivatives, particularly in scenarios where corresponding spot prediction markets are illiquid or non-existent.

Furthermore such a primitive might ensure efficiency in a much larger set of markets than what we currently see on e.g Polymarket, allowing us to access novel forms of information aggregation.

## Replies

**famouswizard** (2024-10-16):

How can leveraging large language models (LLMs) for setting index prices in prediction market derivatives reduce the risk of market manipulation, and what are the potential limitations of this approach?

---

**marcgraczyk** (2024-10-19):

Assuming that the LLM is a good world model (it is able to efficiently approximate the information landscape at a given time), its estimate of the probability of an event is based on a large set of information sources. To manipulate the LLM one would then need to tamper with the majority of these sources which might be very difficult. The first result aims at providing intuition for that.

Limitations include the need for the set of sources to be sufficiently large and satisfy an information substitute condition (the information has diminishing marginal value over time). The main question is the design of the underlying LLM system and whether it can be sufficiently robust and responsive to support a perp market where the price might need to update at a high frequency.

---

**MicahZoltu** (2024-10-19):

The number of people who think a thing, or the number of websites that report a thing, is not indicative of the truthiness of that thing.  The LLM here would have the same problem as humans have, which is figuring out what is true in a sea of falsehoods.

---

**marcgraczyk** (2024-10-21):

Yes this is a good point. I do believe it is accounted for in the above framework. You can assume that the cause of a false report is not only an external agent but the source itself, which is distorting reality.

Empirically, LLMs are able to provide a calibrated prediction given a good information retrieval system (with a website whitelist for example). This is also true for resolution where LLMs are able to resolve with 95%+ accuracy events similar to the one listed on prediction markets. But yes the more specific / subjective the event, the more the point you raise becomes challenge.

---

**MicahZoltu** (2024-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/marcgraczyk/48/17547_2.png) marcgraczyk:

> information retrieval system (with a website whitelist for example)

This would just reduce down to “trust these sources”, at which point you don’t need an LLM, you can just directly use those sources as the source of truth.

