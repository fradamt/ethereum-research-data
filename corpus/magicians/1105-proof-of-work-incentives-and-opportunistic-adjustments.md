---
source: magicians
topic_id: 1105
title: Proof of Work Incentives and Opportunistic Adjustments
author: atlanticcrypto
date: "2018-08-20"
category: EIPs
tags: [eip-1295]
url: https://ethereum-magicians.org/t/proof-of-work-incentives-and-opportunistic-adjustments/1105
views: 995
likes: 2
posts_count: 1
---

# Proof of Work Incentives and Opportunistic Adjustments

Hello everyone,

It’s been suggested by several folks that this is the best launchpad for a discussion on Proof of Work incentives.

By way of background, my name is Brian Venturo, I am the CTO of Atlantic Crypto (ACC). We are a large GPU computing firm based in the US with a sizeable hardware allocation to the ETH network. Currently we represent approximately 0.2% of the global ETH network hashrate. Prior to ACC I operated a systematic fundamental US energy commodity hedge fund, specializing in natural gas and its ancillary markets (electricity, emissions, etc). Before starting this fund I worked at a large environmental asset manager who invested over USD 1billion in Clean Development Mechanism projects under the Kyoto Protocol. Along with my partners, we hold a deep expertise in the energy and environmental markets.

I hope that I can offer some different perspectives regarding current Proof of Work economics, as well as an alternative set of opportunistic adjustments that I believe to be appropriate at this time.

Throughout this post I will utilize our own internal estimates for a number of assumptions - if you have problems with these assumptions, please ask me directly and I can explain our thought process behind them.

A number of required axioms:

Axiom 1: The current network hashrate is approximately 285TH.

Axiom 2: The current watts per MH ratio is approximately 3.85watts/MH.

Axiom 3: The current “equilibrium” network wide Uncle rate is 22.5pct.

Axiom 4: The current cost per MH (full build) is approximately $11/MH for GPU and $9/MH for ASIC.

Axiom 5: There is no alternative use case for the Bitmain E3, Innosilicon A10, etc.

I believe those to be the basic background assumptions required for the analysis going forward. From these we can calculate a number of extremely useful metrics.

**ON THE DEFLATIONARY IMPACT OF NETWORK HASHRATE GROWTH**

I frequently see discussion of reducing the block reward or the overall issuance of ETH as a way to control inflation. Analyzing the impact of network hashrate growth on the underlying purchasing power of ETH quickly shows that the current Proof of Work system has been extremely deflationary for ETH. Over a given time frame, if the growth rate of the network’s hashrate base is greater than the growth rate in total supply, the network is in a deflationary environment. The below image shows a rudimentary assessment of the **base** purchasing power of ETH. This represents the amount of electricity spent to mine 1 ETH - or conversely, the minimum amount of electricity you can buy with 1 ETH.

[![Screenshot%20from%202018-08-20%2012-16-40](https://ethereum-magicians.org/uploads/default/optimized/1X/efd81313d0cf75e528e5b3c5371aeb41dd1f69ce_2_690x435.png)Screenshot%20from%202018-08-20%2012-16-40878×554 34.6 KB](https://ethereum-magicians.org/uploads/default/efd81313d0cf75e528e5b3c5371aeb41dd1f69ce)

The underlying purchasing power of ETH has benefited from the investment in network hashrate growth - this tends to act as a long term fundamental driver of price (see BTC’s network hashrate).

**ON POWER CONSUMPTION AND ENVIRONMENTAL IMPACTS**

The instantaneous power load of the ETH network hashrate is approximately 1,100 MW. This is equivalent to a SINGLE medium sized Combined Cycle Natural Gas Turbine unit. The entire ETH network hashrate can be powered by a single power plant. One. This equates to 4.8mm tCO2e per year.

For reference on the emissions statistic:

In 2004 in the United States, manure and expelled body gas from livestock (predominantly cows and pigs) contributed more than 13 millions tons of methane, according to a 2014 study published in the Journal of Geophysical Research: Atmospheres.

Methane has a global warming potential (GWP) of 28, versus the baseline GWP of 1 for CO2.

**In summary, cow and pig flatulence in the United States accounted for 364mm tCO2e in 2014 versus the ETH network’s current 4.8mm tCO2e.**

As a large operator, we are constantly looking for ways to identify cheap power sources. Cheap power sources are typically renewables based. The network’s search for cheap power is naturally going to lead to a migration to renewable energy sources - many of which have been stranded because government green energy subsidies have lead to the overbuild of many types of renewable energy in very concentrated areas. For instance, ERCOT North wind gen locations trade at -$10/MW due to the government wind subsidies being larger than the negative instantaneous price. There are a large number of utility level issues with the management of renewables on a large power grid, the largest being its intermittency and the requirement to hold spinning reserves (basically, a coal power plant idling to meet any supply swings caused by wind change or cloud cover) - the dirtiest type and status of generation.

As an investor in GHG reduction projects, I look at the ETH network’s power consumption as an easily manageable issue - one that I believe is being managed by the mining community as it matures.

**ON HASHRATE COMPOSITION**

Deploying and operating a scale GPU facility is hard. Deploying and operating a scale ASIC facility is not. When we entered this hobby turned enterprise we made the decision that the flexible computing power of a GPU was a better long-term investment than plugging in a bunch of Bitmain hardware. After operating a large operation, we continue to believe this.

The burgeoning use cases for GPU compute are extremely exciting, and there are several projects launching on the ETH mainnet to help distribute these new workloads across the world. The ETH network has, with or without knowing, incentivized the creation of the largest flexible computing infrastructure on the planet. This build phase has left the ETH network to be hyper-overbuilt, leading to a discussion on the “over-secured” nature of the network. As use cases for the GPU compute infrastructure continue to emerge, we expect that the overbuilt conditions will ease as market prices for the compute cycles equalize over time - drawing GPUs from ETH to other areas. As the ETH network transitions from PoW to hybrid PoW/PoS to PoS at some point in the future, this hardware base will be gradually moving to other areas - offering opportunities to reduce ETH issuance along the way. I believe that by the time PoS emerges the use cases for GPUs will be so great that the transition from PoW to PoS will not be contentious at all.

HOWEVER, with the introduction of ASICs into the network, I believe there is a large risk for a number of contentious forks as the network moves to PoS. With an ETH ASIC having a singular use case, there is no alternative to the ASIC owners than to find another use case using the ETHASH algorithm. With the enterprises behind the development of these ASICs being large and the miners who purchase them being the same, I worry about the network being largely composed of ASICs going forward. **The singular use case can lead to malicious intent at the end of the PoW window.**

I believe the network is early enough in the rollout of ASICs that a Proof of Work algorithm change can be effective in eliminating these risks down the road. IfDefElse presented their PoW algorithm, Programmatic Proof of Work in EIP #1057 ([EIPs/EIPS/eip-1057.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1057.md)). I believe that their implementation is an excellent medium term solution to the network hardware composition risk.

**ON ISSUANCE AND BLOCK REWARDS**

I wrote and proposed an EIP (#1295) discussing issuance and block rewards about two weeks ago. I am going to repost it here:

**Simple Summary**

Network security and overall ecosystem maturity warrants the continued incentivization of Proof of Work participation but allows for a reduction in ancillary ETH issuance and the removal of the Difficulty Bomb. This EIP proposes a reduction of Uncle and removal of Nephew rewards while diffusing and removing the Difficulty Bomb with the Constantinople hard fork.

**Motivation**

Network scalability and security are at the forefront of risks to the Ethereum protocol. With great strides being made towards on and off chain scalability, the existence of an artificial throughput limiting device in the protocol is no longer warranted. Removing the risk of reducing throughput through the initialization of the Difficulty Bomb is “low-hanging-fruit” to ensure continued operation at a minimum of current throughput into the future.

The security layer of the Ethereum network is and should remain robust. Incentives for continued investment into the security of the growing ecosystem are paramount. At the same time, the ancillary issuance benefits of the Ethereum protocol can be adjusted to reduce the overall issuance profile. Aggressively adjusting Uncle and removing Nephew rewards will reduce the inflationary aspect of ETH issuance, while keeping the current block reward constant at 3 ETH will ensure top line incentives stay in place.

**Rationale**

The Difficulty Bomb was instituted as a type of planned obsolescence to force the implementation of network upgrades with regular frequency. With the success of and resulting investment in the Ethereum protocol, these network upgrades have been secured through outright adoption and the size of the development community. With a result of the Difficulty Bomb being a reduction in effective network throughput and the risk of inaction inside the development community being reduced substantially, the original purpose of the Difficulty Bomb seems to have been diffused itself. With the focus on scalability for the protocol, eliminating a mechanism whereby the throughput of the network can be limited artificially, due to any circumstance, is a logical step to ensure continued minimum network operation at the current throughput level.

Through August 4th, the 2018 year to date reward issued to Uncle blocks totaled over 635,000 ETH. The average reward per Uncle totals 2.27 ETH. The year to date average Uncle rate is 22.49%. Using the year to date metrics, the ongoing average ETH paid as an Uncle reward per block is 0.51 ETH plus the Uncle inclusion reward of 0.021 ETH (0.09375 ETH * .2249), total Uncle related reward per block being over 0.53 ETH. With total year to date block rewards totaling approximately 3,730,000 ETH, the network has paid an additional 17pct in Uncle rewards. This is issuance that can be reduced while still maintaining the overall integrity and incentivization of network security.

Reducing the issuance of ETH in rewarding Uncle blocks (forked blocks caused by latency in propagation, a multi-faceted problem) should directly incentivize the investment in technologies and efficiencies to reduce the overall network Uncle rate which may lead to a reduction in Network wide Uncle rates, reducing ancillary issuance further.

Reducing the Uncle rewards from the current specification to the proposed will yield two levels of ancillary ETH issuance for Uncles:

Level 1 Uncle → 0.75 ETH

Level 2 Uncle → 0.375 ETH

These levels are sufficient to continue incentivizing decentralized participation, while also providing an immediate economic incentive for the upgrade of the Ethereum node network and its tangential infrastructure.

The Nephew reward structure should be entirely eliminated.

With a reduction to the Uncle and removal of the Nephew reward, ancillary ETH issuance should drop (under normal market conditions, i.e. 22.49% uncle rate) by over 75pct and total ETH issuance from the successful sealing and mining of valid blocks should drop over 10pct.

Paired with the diffusal and removal of the Difficulty Bomb, this proposal strikes a balance between ensuring status quo network throughput, reducing overall ETH issuance, and continuing top line incentives for investment in infrastructure and efficiencies to continue expanding the Ethereum protocol’s operational security.

**IN SUMMARY**

I hope this is a good starting point to begin discussing the goals of managing ETH issuance, the types of hardware composing the network, and the mechanisms through which you can attack them.

Thank you for your time and consideration.
