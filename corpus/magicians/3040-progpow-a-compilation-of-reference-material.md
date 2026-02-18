---
source: magicians
topic_id: 3040
title: ProgPoW - A Compilation of Reference Material
author: ifdefelse
date: "2019-03-30"
category: EIPs > EIPs core
tags: [progpow, eip-1057]
url: https://ethereum-magicians.org/t/progpow-a-compilation-of-reference-material/3040
views: 5522
likes: 8
posts_count: 7
---

# ProgPoW - A Compilation of Reference Material

We have noted that it can become increasingly difficult to find statements, references or information to ProgPoW. In an effort to remain organized and decrease confusion, we’ve decided to begin to catalogue information here.

We will update this as new information is added. If there is something we should add (complaints,  concerns, governance, articles, reviews), please post it in the thread!

[GitHub - Reference Implementation, Specification, and Original Whitepaper](https://github.com/ifdefelse/ProgPOW)

*This is our original reference implementation. Note that there are other optimized miners contributed by the Ethereum community, and for benchmarking, one of those is more appropriate.*

[GitHub Comments - See Our Replies to Various Issues or Questions](https://github.com/search?q=user%3Aifdefelse+commenter%3Aifdefelse)

*This is helpful if you want to stay up-to-date with technical comments we address on GitHub, rather than searching through the various forums.*

[Article: The Problem with Proof of Work](https://medium.com/@OhGodAGirl/the-problem-with-proof-of-work-da9f0512dad9)

*Addresses the original problem with specialization, proof-of-work, incentives, and Casper FFG. Note that this article was written ten months ago, and thus some of the statements around Ethereum’s ecosystem are outdated.*

[Article: Performance and Tuning (Spec 0.9.2)](https://medium.com/@ifdefelse/understanding-progpow-performance-and-tuning-d72713898db3)

*This article explains a lot of the inefficiencies with Ethash from a GPU saturation and throughput standpoint, and how ProgPoW addresses those.*

[Article: ProgPoW FAQ](https://medium.com/@ifdefelse/progpow-faq-6d2dce8b5c8b)

*This article addresses some of the most frequently asked questions around ProgPoW, including design, early review, and a brief overview of an ASIC implementation.*

[Article: The Cost of ASIC Design](https://medium.com/@ifdefelse/the-cost-of-asic-design-a44f9a065b72)

*Highlights on some of the differences between a cryptocurrency-ASIC designer, and a GPU-ASIC designer; how yields works; why low voltage doesn’t work for ProgPoW ASICs; and clarifies why floating-point math is not used in ProgPoW.*

[Article: A Comprehensive ProgPoW Benchmark](https://medium.com/@infantry1337/comprehensive-progpow-benchmark-715126798476)

*Benchmarking results from an enthusiast miner, including: results with and without VBIOS modifications; a power consumption and hashrate comparison between Ethash and ProgPoW; a power consumption and hashrate comparison between 0.9.2 and 0.9.3.*

[Article: The Miners Benchmark ProgPoW](https://medium.com/@infantry1337/the-miners-benchmark-progpow-e79cab6eabc3)

*Comprehensive testing of ProgPoW, version 0.9.2, for both AMD and NVIDIA.*

[Article: AMD isn’t as simple as ABC](https://medium.com/@infantry1337/amd-isnt-as-simple-abc-a11aefb1b601)

*Addresses a variance between different block heights on both ProgPoW and Ethash, along with  appropriate benchmarking criteria for ProgPoW.*

## Replies

**boris** (2019-03-30):

We have a new [#eips:core-eips](/c/eips/core-eips/35) topic, so I moved this there, and also added the tag [#progpow](https://ethereum-magicians.org/tags/progpow) which gathers together a number of different posts.

Thanks for compiling and sharing this info.

---

**lookfirst** (2019-03-31):

https://medium.com/altcoin-magazine/13-questions-about-ethereums-movement-to-progpow-e17e0a6d88b8

---

**greerso** (2020-03-09):

# ProgPoW resources

## Informational

May 2, 2018 [EIPs/eip-1057.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1057.md)

May 3, 2018 [ProgPOW/README.md at master · ifdefelse/ProgPOW · GitHub](https://github.com/ifdefelse/ProgPOW/blob/master/README.md)

May 3, 2018 [EIP-ProgPoW: a Programmatic Proof-of-Work - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-progpow-a-programmatic-proof-of-work)

May 29, 2018 [The Problem with Proof of Work - K. L. Minehan - Medium](https://medium.com/@OhGodAGirl/the-problem-with-proof-of-work-da9f0512dad9)

October 25, 2018 [Understanding ProgPoW - IfDefElse - Medium](https://medium.com/@ifdefelse/understanding-progpow-performance-and-tuning-d72713898db3)

Nov 17, 2018 [progpow-wiki/ProgPoW.md at master · MariusVanDerWijden/progpow-wiki · GitHub](https://github.com/MariusVanDerWijden/progpow-wiki/blob/master/ProgPoW.md)

December 10, 2018 [ProgPoW - A Programmatic Proof of Work by Kristy-Leigh Minehan (Devcon4) - YouTube](https://www.youtube.com/watch?v=pe1pDGDy6iE)

January 10, 2019 [ProgPoW FAQ - IfDefElse - Medium](https://medium.com/@ifdefelse/progpow-faq-6d2dce8b5c8b)

January 14, 2019 [What GPU miners may not know about ProgPoW - Andrea Lanfranchi - Medium](https://medium.com/@andrea.lanfranchi/what-gpu-miners-may-not-know-about-progpow-a9bb42a0d5a7)

January 17, 2019 [ProgPoW: Progress Update #1 - IfDefElse - Medium](https://medium.com/@ifdefelse/progpow-progress-da5bb31a651b)

February 14, 2019 [Council of Denver - HackMD](https://hackmd.io/wyH2fmZVQFSMQsnSI9DIsw)

February 17, 2019 [The Miners Benchmark ProgPoW - Theodor Ghannam - Medium](https://medium.com/@infantry1337/the-miners-benchmark-progpow-e79cab6eabc3)

February 21, 2019 [Ethereum ProgPoW Explained - Crypto Mining Blog](https://2miners.com/blog/ethereum-progpow-explained/)

March 18, 2019 [13 Questions about Ethereum’s Movement to ProgPow - The Capital - Medium](https://medium.com/the-capital/13-questions-about-ethereums-movement-to-progpow-e17e0a6d88b8)

March 20, 2019 [Skeptical about #ProgPoW? I am too! - Bryant Eisenbach - Medium](https://medium.com/@fubuloubu/skeptical-about-progpow-i-am-too-5211c88faf35)

March 27, 2019 [Comprehensive ProgPoW Benchmark - The Capital - Medium](https://medium.com/the-capital/comprehensive-progpow-benchmark-715126798476)

March 28, 2019 [My stance on Progpow](https://swende.se/blog/Progpow.html)

March 30, 2019 [The Cost of ASIC Design - IfDefElse - Medium](https://medium.com/@ifdefelse/the-cost-of-asic-design-a44f9a065b72)

April 12, 2019 [Ethereum ProgPoW Update - Crypto Mining Blog](https://2miners.com/blog/ethereum-progpow-update/)

September 23, 2019 [In Defense of ProgPow : ethereum](https://www.reddit.com/r/ethereum/comments/d847af/in_defense_of_progpow/)

February 4, 2020 [Antminer E3 Stops Mining Ethereum Classic, Just Over a Month Remaining for Ethereum - Crypto Mining Blog](https://2miners.com/blog/antminer-e3-stops-mining-ethereum-classic-just-over-a-month-remaining-for-ethereum/#When_Will_Antminer_E3_Stop_Mining_Ethereum)

## Ethereum Magicians

August 2, 2108 [Final Request From the GPU Mining Community - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/final-request-from-the-gpu-mining-community)

August 26, 2018 [EIP-1355: Ethash 1a - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-1355-ethash-1a/1167)

September 3, 2108 [What has to be done to get ProgPoW on Ethereum - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/what-has-to-be-done-to-get-progpow-on-ethereum/1361)

January 1, 2019 [Guidelines for ProgPow Hardware Developers - Primordial Soup - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/guidelines-for-progpow-hardware-developers)

February 2, 2019 [On the progpow audit - Action Item - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/on-the-progpow-audit)

March 3, 2019 [My technical take on ProgPow’s weakest link - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/my-technical-take-on-progpows-weakest-link)

March 4, 2019 [Governance concerns after listening to ~all ProgPow discussions on Core Dev calls - Process Improvement - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/governance-concerns-after-listening-to-all-progpow-discussions-on-core-dev-calls)

March 29, 2019 [Motion to NOT include ProgPow without audit - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/motion-to-not-include-progpow-without-audit)

March 30, 2109 [ProgPoW - A Compilation of Reference Material - Core EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/progpow-a-compilation-of-reference-material/)

May 23, 2019 [ProgPoW Audit Delay Issue - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/progpow-audit-delay-issue)

July 8, 2019 [Ensuring ETH 1.x’s Success Without Disenfranchising The Community - Ethereum 1.x Ring - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/ensuring-eth-1-xs-success-without-disenfranchising-the-community)

August 8, 2019 [EIP-centric forking - Process Improvement - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/eip-centric-forking)

## YouTube

October 8, 2018 [Cardano Rust Project | Petro Public Sale | ProgPow | WSJ Attacks Shapeshift (October 2nd, 2018) - YouTube](https://www.youtube.com/watch?v=UFkrFv6RjxI)

October 23 2018 [Ethereum Mining News | FPGA’s Mining | ProgPoW LIKELY | Profitability | Hard Fork Delayed 2019 - YouTube](https://www.youtube.com/watch?v=VYSLEwT5iRs)

December 13, 2018 [Why ProgPoW is BAD for Ethereum - YouTube](https://www.youtube.com/watch?v=taMRiY9MML0)

December 19, 2018 [Bitcoin Rallies Towards 4k - Why? Ethereum Launches ProgPoW GPU Mining Testnet | New HD Minable Coin - YouTube](https://www.youtube.com/watch?v=xnEizZsNnsI)

January 4, 2019 [Ethereum moving to PROGPOW! What’s it mean for Miners? - YouTube](https://www.youtube.com/watch?v=g9tj6-z6Fhk)

January 4, 2019 [Ethereum ProgPoW CONFIRMED! - YouTube](https://www.youtube.com/watch?v=E6BTaTR40JU)

January 5, 2019 [Mining on the ProgPoW Gangnam Ethereum Testnet! - YouTube](https://www.youtube.com/watch?v=VLup3w99Bdg)

January 6, 2019 [6 x Asus RX 570 4GB ProgPoW Gangnam Ethereum Testnet TEST! - YouTube](https://www.youtube.com/watch?v=psRcOR-Xv-Q)

January 7, 2019 [ProgPOW Explained - A Brave New World for Ethereum Miners? - YouTube](https://www.youtube.com/watch?v=k-_w-6YEiWc&t)

January 20, 2019 [CES2019 - North American Bitcoin Conference - GRIN / BEAM - PROGPOW and more! - YouTube](https://www.youtube.com/watch?v=JW9TtaWA8Tw)

January 23, 2019 [Ethereum to ZERO? Eth Chain Split. ProgPow & ETC 51 % Attack. GPU vs ASIC Miners. - YouTube](https://www.youtube.com/watch?v=nSAr9JHNe2s)

January 29, 2019 [Nick Johnson: Future of the Ethereum Name Service and thoughts on ProgPOW - YouTube](https://www.youtube.com/watch?v=DUR8YQZoV3g)

February 19, 2019 [Ethereum Hard Fork Soon? ProgPoW Voting? - YouTube](https://www.youtube.com/watch?v=Be3pefbdo7o)

February 20, 2019 [ProgPoW Merged Into Parity Ethereum | ETHNews Brief - YouTube](https://www.youtube.com/watch?v=MPROxFFKtFE)

February 25, 2019 [How does R7 370, R9 380,380x,390 and more perform on PROGPOW and other Cryptocurrencies in 2019? - YouTube](https://www.youtube.com/watch?v=u0kh8fRs-uo)

March 7, 2019 [PROGPOW Explained in under 4 min. & why it matters to GPU Miners - YouTube](https://www.youtube.com/watch?v=FXeMt8n7zX8)

March 19, 2019 [What is BBT doing with PROGPOW, Why all of the testing? - YouTube](https://www.youtube.com/watch?v=Bg3zSqErgdo)

March 25, 2019 [eVGA RTX 2080Ti FTW3 11GB DDR6 Cryptocurrency Performance Test PROGPOW ETH RVN BEAM GRIN29 GRIN31 - YouTube](https://www.youtube.com/watch?v=BdkSeW9I_Ss)

March 29, 2019 [Ethereum & ProgPoW… What Is Going On? - YouTube](https://www.youtube.com/watch?v=V9heP44KuM8)

May 2, 2019 [Ethereum ProgPow Audit Has Been Funded & Approved - YouTube](https://www.youtube.com/watch?v=pEIDtpBQ9Wg)

July 5, 2019 [Mining News! Monero RandomX | Ethereum ProgPoW 2019 Update | Grin Embraces ASIC miners | Zel Zelhash - YouTube](https://www.youtube.com/watch?v=WQ6aXXhiP4U)

July 24, 2019 [Ethereum ProgPoW AUDIT Is Finally Getting Started… - YouTube](https://www.youtube.com/watch?v=1DCDHJgu8CA)

September 13, 2019 [Ethereum ProgPoW Algorithm Audits Finalized - YouTube](https://www.youtube.com/watch?v=wRZPuldMxng)

September 24, 2019 [An Argument Against ProgPoW a Day - Part 1 - YouTube](https://www.youtube.com/watch?v=W9FeezHgs08)

October 4, 2019 [82  -  Defending ProgPoW with Kristy-Leigh Minehan - YouTube](https://www.youtube.com/watch?v=ckb66ErJzDk)

October 10, 2019 [#36 - Kristy-Leigh of ProgPow discusses the EIP, Satoshi, Code Contributions, and Crypto Mining 2020 - YouTube](https://www.youtube.com/watch?v=7Cc389LVjAs)

November 24, 2019 [Ethereum Classic REJECTS ProgPoW… - YouTube](https://www.youtube.com/watch?v=pMzi3KBuEtk)

December 16, 2019 [Ethereum ProgPoW Implementation Is STILL Coming Right? - YouTube](https://www.youtube.com/watch?v=mI_QEd9hQLE)

December 26, 2019 [Panel: Least Authority’s ProgPoW Audit (Devcon5) - YouTube](https://www.youtube.com/watch?v=2jvRu8DxCoU)

## Podcasts

April 11, 2019 https://podcasts.apple.com/us/podcast/blockchannel/id1307284590?i=1000434669782

September 10, 2019 https://podcasts.apple.com/us/podcast/ethhub-weekly-recap-78-ethboston-compound-drama-eth2/id1443920565?i=1000449269536

September 25, 2019 https://podcasts.apple.com/us/podcast/ethhub-weekly-recap-80-progpow-discussion-doj-extortion/id1443920565?i=1000451214746

October 4, 2019 https://podcasts.apple.com/us/podcast/82-defending-progpow-with-kristy-leigh-minehan/id1436674724?i=1000452312677

## Official Updates

May 18, 2019 Dev Call [#38 - May 18, 2018](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2038.md)

August 24, 2018 Dev Call [#45 - August 24, 2018](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2045.md)

September 28, 2018 Dev Call [#47 - September 28, 2018](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2047.md)

January 4, 2019 Dev Call [#52 - January 4, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2052.md)

January 18, 2019 Dev Call[#53 - January 18, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2053.md)

February 1, 2019 Dev Call [#54 - February 1, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2054.md)

February 11, 2019 [Ethereum Cat Herders Update#1 : EthereumCatHerders](https://www.reddit.com/r/EthereumCatHerders/comments/aphfgd/ethereum_cat_herders_update1/?st=JS0NV4JQ&sh=734f8b7a)

March 15, 2019 Dev Call [#57 - March 15, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2057.md)

May 24, 2019 Dev Call [#62 - May 24, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2062.md)

July 18, 2019 Dev Call [#65 - July 18, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2065.md)

September 10, 2019 [ProgPoW Audits Released - Ethereum Cat Herders - Medium](https://medium.com/ethereum-cat-herders/progpow-audits-released-ed4973ebe073)

September 6, 2019 Dev Call [#70 - September 6, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2070.md)

November 1, 2019 Dev Call [#74 - November 1, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2074.md)

December 13, 2019 Dev Call [#77 - December 13, 2019](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2077.md)

January 24, 2019 Dev Call [#79 - January 24, 2020](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2079.md)

February 21, 2020 Dev Call[#81 - February 21, 2020](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2081.md)

## News Articles

January 4, 2019 [Ethereum Core Devs to Move Forward With ASIC-Resistant PoW Algorithm](https://cointelegraph.com/news/ethereum-core-devs-to-move-forward-with-asic-resistant-pow-algorithm)

January 5, 2019 [Ethereum (ETH) Developers Plan to Implement ASIC-Resistant Proof of Work Mining Algorithm](https://bitcoinexchangeguide.com/ethereum-eth-developers-plan-to-implement-asic-resistant-proof-of-work-mining-algorithm/)

January 7, 2019 [BREAKING: Ethereum Classic (ETC) Hit With 51 Percent Attack A Week Before Ethereum (ETH) Constantinople Hard Fork – Crypto.IQ | Bitcoin and Investment News from Inside Experts You Can Trust](https://cryptoiq.co/ethereum-classic-etc-hit-with-51-percent-attack-a-week-before-ethereum-eth-constantinople-hard-fork/)

January 8, 2019 [ETH Dev Suggests Moving to ‘ASIC-Friendly Algorithm’ After ProgPoW Decision](https://cointelegraph.com/news/eth-dev-suggests-moving-to-asic-friendly-algorithm-after-progpow-decision)

January 8, 2019 [Ethereum Miner Linzhi Calls Out Project Coders for Proposed ASIC Ban - CoinDesk](https://www.coindesk.com/ethereum-miner-linzhi-calls-out-project-coders-for-proposed-asic-ban)

January 8, 2019 [Ethereum (ETH) Core Developers Propose an ASIC Resistant Upgrade - Ethereum World News](https://ethereumworldnews.com/ethereum-eth-core-developers-propose-an-asic-resistant-upgrade/)

January 9, 2019 [Ethereum Classic (ETC) 51% attack proof that shitcoins have no hope of succeeding? | CaptainAltcoin](https://captainaltcoin.com/ethereum-classic-etc-51-attack-proof-that-shitcoins-have-no-hope-of-succeeding/)

January 9, 2019 [What’s ProgPoW? Meet the hot new debate in the Ethereum community | finder.com.au](https://www.finder.com.au/whats-progpow-meet-the-hot-new-debate-in-the-ethereum-community)

January 18, 2019 [Ethereum Core Devs Constantinople Meeting to Be Held on Jan 18](https://www.cryptovibes.com/blog/2019/01/17/ethereum-constantinople-upgrade-meeting/)

February 1, 2019 [Ethereum Core Dev Call #54: Waiting for ProgPoW - The Block](https://www.theblockcrypto.com/genesis/10033/ethereum-core-dev-call-54-waiting-for-progpow)

February 3, 2019 [Will Ethereum Adopt ‘ProgPoW,’ the ASIC-Resistant Mining Algorithm? | CryptoSlate](https://cryptoslate.com/will-ethereum-adopt-progpow-asic-resistant-mining-algorithm/)

February 4, 2019 [Is Ethereum Going to be Adopting ASIC-Resistant ‘ProgPow’ as a Mining Algorithm?](https://bitcoinexchangeguide.com/is-ethereum-going-to-be-adopting-asic-resistant-progpow-as-a-mining-algorithm/)

February 15, 2019 [Ethereum Core Dev Call #55: ProgPoW audits and Vitalik’s Phase 2 updates - The Block](https://www.theblockcrypto.com/linked/12086/ethereum-core-dev-call-55-progpow-audits-and-vitaliks-phase-2-updates)

February 15, 2019 [Recompensas por minería en Ethereum llegan a mínimo histórico | CriptoNoticias](https://www.criptonoticias.com/mineria-bitcoin-criptomonedas/recompensas-mineria-ethereum-mnimo-historico/)

February 28, 2019 [Coinhive dice adiós a la minería web por caída del mercado | CriptoNoticias](https://www.criptonoticias.com/mineria-bitcoin-criptomonedas/coinhive-adios-mineria-web-caida-mercado/)

March 6, 2019 [Ethereum Core Dev Meeting : ProgPow Implementation Receives More Than 50 Percent Votes from Miners - CryptoNewsZ](https://www.cryptonewsz.com/ethereum-core-dev-meeting-progpow-implementation-receives-more-than-50-percent-votes-from-miners/)

March 7, 2019 [The ASIC Resistant Mining Campaign from Ethereum Miners Is Just Getting Started](https://bitcoinexchangeguide.com/the-asic-resistant-mining-campaign-from-ethereum-miners-is-just-getting-started/)

March 12, 2019 [Ethereum’s ProgPoW Proposal: An Expensive Game of Whack-a-Mole - CoinDesk](https://www.coindesk.com/ethereums-progpow-proposal-an-expensive-game-of-whack-a-mole)

March 12, 2019 [Ethereum’s ProgPoW Mining Change to Be Considered for Istanbul Upgrade - CoinDesk](https://www.coindesk.com/ethereums-progpow-mining-change-to-be-considered-for-istanbul-upgrade)

March 14, 2019 [As ProgPoW Aimed at Stopping ASIC Mining Gets Supporting Votes, New Conspiracies and Debates Appear](https://cointelegraph.com/news/as-progpow-aimed-at-stopping-asic-mining-gets-supporting-votes-new-conspiracies-and-debates-appear)

March 15, 2019 [Ethereum’s ProgPow Mining Change Approved Again, But Timeline Unclear - CoinDesk](https://www.coindesk.com/ethereums-progpow-mining-change-approved-again-but-timeline-unclear)

March 17, 2019 [Ethereum Devs Once Again Approve ASIC-Resistant Algorithm ProgPoW](https://cointelegraph.com/news/ethereum-devs-once-again-approve-asic-resistant-algorithm-progpow)

March 18, 2019 [Ethereum (ETH) to Be ASIC-Resistant, No Date Set However - Cryptovest](https://cryptovest.com/news/ethereum-eth-to-be-asic-resistant-no-date-set-however/)

March 27, 2019 [Aumentan desacuerdos en Ethereum por decisión de avanzar con ProgPoW | CriptoNoticias](https://www.criptonoticias.com/mineria-bitcoin-criptomonedas/aumentan-desacuerdos-ethereum-decision-avanzar-progpow-asic/)

March 29, 2019 [Bitmain Co-founder, Jihan Wu: ASIC Miners Makes a Blockchain Network More Decentralized - Coindoo](https://coindoo.com/bitmain-co-founder-jihan-wu-asic-miners-makes-a-blockchain-network-more-decentralized/)

April 8, 2019 [A Fight Over Specialized Chips Threatens an Ethereum Split | WIRED](https://www.wired.com/story/fight-over-specialized-chips-threatens-ethereum-split/)

April 26, 2019 [Funding Approved for Audit of Ethereum’s ProgPoW Mining Proposal - CoinDesk](https://www.coindesk.com/funding-approved-for-audit-of-ethereums-progpow-mining-proposal)

April 28, 2019 [Ethereum Core Devs: Funding for ProgPoW 3rd-Party Audit Approved](https://cointelegraph.com/news/ethereum-core-devs-funding-for-progpow-3rd-party-audit-approved)

April 20, 2019 [Ethereum’s Recent Decline in Hashrate ‘Not Surprising’: Cyber Threat Expert Explains | CryptoGlobe](https://www.cryptoglobe.com/latest/2019/04/ethereum-s-recent-decline-in-hashrate-not-surprising-cyber-threat-expert-explains/)

June 14, 2019 [Proposed Ethereum Istanbul Hard Fork Combed With A Fine Tooth at Cat Herders Meeting](https://bitcoinexchangeguide.com/proposed-ethereum-istanbul-hard-fork-combed-with-a-fine-tooth-at-cat-herders-meeting/)

July 13, 2019 [¿Qué es ProgPoW? La propuesta de algoritmo contra mineros ASIC en Ethereum | CriptoNoticias](https://www.criptonoticias.com/mineria-bitcoin-criptomonedas/software/que-es-progpow-algoritmo-mineros-asic-ethereum/)

August 17, 2019 [Ethereum: ProgPow will be activated on the mainnet next year as a part of Istanbul 2 - AMBCrypto](https://eng.ambcrypto.com/ethereum-progpow-will-be-activated-on-the-mainnet-next-year-as-a-part-of-istanbul-2/)

August 18, 2019 [Ethereum’s ProgPoW To Be Released The First Quarter Of 2020 | UseTheBitcoin](https://usethebitcoin.com/ethereums-progpow-to-be-released-the-first-quarter-of-2020/)

August 19, 2019 [Ethereum to Switch to ProgPoW Mining Algorithm in Upcoming Istanbul Hard Fork](https://coinidol.com/ethereum-make-codebase/)

September 8, 2019 [Ethereum: ProgPoW high level design goals are reasonable towards achieving its intended economic effect - AMBCrypto](https://eng.ambcrypto.com/ethereum-progpow-high-level-design-goals-are-reasonable-towards-achieving-its-intended-economic-effect/)

September 11, 2019 [Chinese Firm Linzhi Set To Mass Produce Ethereum and ETC ASIC Miners As Tests Go Live](https://bitcoinexchangeguide.com/chinese-firm-linzhi-set-to-mass-produce-ethereum-and-etc-asic-miners-as-tests-go-live/)

September 18, 2019 [Ethereum ProgPOW author uninvited from ETC Summit due to Craig Wright association | CryptoSlate](https://cryptoslate.com/ethereum-progpow-uninvited-etc-summit-craig-wright/)

September 19, 2019 [Ethereum reveals launch dates for testing Istanbul - Decrypt](https://decrypt.co/9391/ethereum-reveals-launch-dates-for-testing-istanbul)

September 19, 2019 [Hashing Out: ProgPoW Debate Kicks Up in Ethereum Community Again](https://blockonomi.com/progpow-debate-ethereum-community/)

September 19, 2019 [ETC Summit Invitees List Has No Space for Kristy Minehan](https://www.cryptonewsz.com/kristy-minehan-uninvited-to-etc-summit-under-vague-accusations/)

September 22, 2019 [Ethereum ProgPoW upgrade causing chain split more likely to be from the user side instead of the miner side - AMBCrypto](https://eng.ambcrypto.com/ethereum-progpow-upgrade-causing-chain-split-more-likely-to-be-from-the-user-side-instead-of-the-miner-side/)

September 23, 2019 [ProgPow advocate uninvited to Ethereum Classic Summit over links to Craig Wright](https://finance.yahoo.com/news/progpow-advocate-uninvited-ethereum-summit-214513635.html)

September 24, 2019 [ProgPoW backer steps down from controversial role  - Decrypt](https://decrypt.co/9605/progpow-backer-steps-down-from-controversial-role)

September 25, 2019 [ProgPOW author steps down as Core Scientific CTO, vows to implement algorithm on Ethereum | CryptoSlate](https://cryptoslate.com/progpow-authors-steps-down-core-scientific-cto-ethereum/)

September 25, 2019 [Ethereum ProgPoW proponent Kristy-Leigh Minehan steps down citing perceived conflict of interest - AMBCrypto](https://eng.ambcrypto.com/ethereum-progpow-proponent-kristy-leigh-minehan-steps-down-citing-perceived-conflict-of-interest/)

September 25, 2019 [Core Scientific CTO Steps Down To Push Through Ethereum ProgPOW](https://bitcoinist.com/core-scientific-cto-steps-down-to-push-through-ethereum-progpow/)

September 25, 2019 [ProgPoW author Kristy-Leigh Minehan resigns as CTO of Core Scientific | Cryptopolitan](https://www.cryptopolitan.com/kristy-leigh-minehan-core-scientific/)

September 26, 2019 [New Ethereum ASIC dominates GPU mining performance | CryptoSlate](https://cryptoslate.com/ethereum-asic-dominates-gpu-performance/)

September 26, 2019 [New Ethereum ASIC Fuels Discord Among Ethereum Community](https://www.cryptonewsz.com/new-ethereum-asic-fuels-discord-among-ethereum-community/)

September 28, 2019 [The (alleged) plot against the Ethereum network - Decrypt](https://decrypt.co/9729/the-alleged-plot-against-ethereum)

October 9, 2019 [ProgPoW, the Algorithm Dividing the Ethereum Community: a GPU Manufacturer Ploy? - Ethereum World News](https://en.ethereumworldnews.com/progpow/)

October 9, 2019 [Ethereum Hard Fork Is Coming — Here’s What You Need to Know About ‘Istanbul’ – BeInCrypto](https://beincrypto.com/ethereum-hard-fork-is-coming-heres-what-you-need-to-know-about-istanbul/)

October 27, 2019 [Ethereum ProgPoW’s raison d’etre: To be or not to be - AMBCrypto](https://eng.ambcrypto.com/ethereum-progpows-raison-detre-to-be-or-not-to-be/)

November 4, 2019 [Aragon Opposes Change to Ethereum’s Mining Algorithm Before 2.0 Version](https://cointelegraph.com/news/aragon-opposes-change-to-ethereums-mining-algorithm-before-20-version)

November 7, 2019 [Aragon community against Ethereum ProgPOW](https://www.fxstreet.com/cryptocurrencies/news/aragon-community-against-ethereum-progpow-201911070053)

November 8, 2019 [Ethereum Istanbul Hard Fork Release Date Confirmed By Core Developer](https://cointelegraph.com/news/ethereum-istanbul-hard-fork-release-date-confirmed-by-core-developer)

November 16, 2019 [Ethereum ProgPoW audit contributors on Gitcoin to be refunded in full - AMBCrypto](https://eng.ambcrypto.com/ethereum-progpow-audit-contributors-on-gitcoin-to-be-refunded-in-full/)

November 26, 2019 [Ethereum’s Buterin: PoW algorithms offering medium-level ASIC resistance can be created - AMBCrypto](https://eng.ambcrypto.com/ethereums-buterin-pow-algorithms-offering-medium-level-asic-resistance-can-be-created/)

December 17, 2019 [Ethereum devs move ProgPoW into ‘Eligible for Inclusion’ list - AMBCrypto](https://eng.ambcrypto.com/ethereum-devs-move-progpow-into-eligible-for-inclusion-list/)

January 1, 2020 [Is the ASIC Resistance dream closer to reality, despite claims of it being a myth? - AMBCrypto](https://eng.ambcrypto.com/is-the-asic-resistance-dream-closer-to-reality-despite-claims-of-it-being-a-myth/

---

**CryptoBlockchainTech** (2020-03-10):

Thank you for compiling all of this into a single location!

---

**CryptoBlockchainTech** (2020-03-13):

ROFLMAO. OMG Karma is a Bitch . One week later and guess what? The supposed community of DeFi is imploding. This is a great example how the Dev team was swindled by the Johnny come lately “community” that in the end was only here for one thing…to make money. They could care less about Ethereum or the Developers, and as shown in the call, GPU miners. In the end they will walk away if there is no money to be made

[![image](https://ethereum-magicians.org/uploads/default/original/2X/9/9dabd7c78f8ac96a647100a87eabff6116ac32a9.png)](https://user-images.githubusercontent.com/37913635/76616544-d4e29c80-64e9-11ea-819e-a882881def25.png)

This pales in contrast to all the GPU miners who have stayed with Ethereum PATIENTLY waiting two years for the developers to find the time to include an Ethash change that would remove ASICs from the network. Even at 40% ASICs we are still here! I say we invite the supposed DeFi community back on the next Dev call and see if any of them show up. My guess is they are counting what little money they have left to move on to their next venture.

Don’t be fooled Developers, DeFi is not a community, they are rich greedy bastards that only care about themselves and were using Ethereum to enrich themselves. The GPU mining community has and always will care about the future of Ethereum. We will be here to help GLADLY usher in Eth2.0 and the birth of POS.

---

**VanwaTech** (2020-03-14):

I saw the Pro-Asic clowns in Linzhi’s telegram waiting to buy the ASIC.

Not only are these guys willing to scumbag the entire coin for short term gains - the best part is they will never even make money with their ASIC.

They act like Linzhi is a charity. Why on earth would Linzhi sell the ASICs if they can make more just mining on them?

Linzhi will sell the ASIC once its no longer profitable because they have the new version.

It’s a ponzi scheme, just like all of the other ASIC manufacturers

Can’t wait for Ethereum to die out and a real coin with ASIC resistance to come up - I hear there are a few already gaining traction

