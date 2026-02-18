---
source: ethresearch
topic_id: 17302
title: Introducing Yu, A very suitable for L3, independency application blockchain framework
author: Lawliet-Chan
date: "2023-11-05"
category: Applications
tags: [layer-2]
url: https://ethresear.ch/t/introducing-yu-a-very-suitable-for-l3-independency-application-blockchain-framework/17302
views: 2098
likes: 1
posts_count: 7
---

# Introducing Yu, A very suitable for L3, independency application blockchain framework

Hi, guys.

I have contributed codes to tendermint and substrate, and I find both of them are not very useful. Then I have developed an independency application blockchain framework for about 3 years:



      [github.com](https://github.com/yu-org/yu)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/b/9/b9716d6daf83e102817754053394841ccda5018e_2_690x344.png)



###



Yu is a highly customizable modular blockchain framework.










It can help developers develop an independency appchain like developing a web API which is much easier and more customized than substrate and cosmos-sdk.

As [@vbuterin](/u/vbuterin) and Starkware [mentioned](https://vitalik.ca/general/2022/09/17/layer_3.html):  **L2 is for scaling, L3 is for customized functionality/scaling**.   We can define various assets and some large transactions on Ethereum L1, most transfer on L2 for scaling, and customized functionality on L3. As we know, L2 solutions are almost for scaling, but we still need some app-specific scenes. Just like if you want to develop a decentralized Uber, you can use Yu to develop one with rich golang third-party libs for expanding more functions.

Yu includes but not limited to the following functions:

(1) Modular onchain txs(writing) and queries(reading)

(2) Customizable consensus. It contains POA by default, but you can develop easily any consensus protocol you want. Yu provides you free tx packaging and verification methods, simple P2P interfaces, blockchain interfaces and so on.

(3) You can move EVM into yu as a module to compatible with solidity, also you can use something other than the EVM  to compatible with js/python/shell/…  as the chain’s scripts codes. Just like Chrome’s extensions.

More details please visit the above link.

In all, I think yu is the most suitable one for L3 app-specific blockchain.

Certainly, you can also use yu to develop the decentralized sharing sequencer, L2 side-chain and any customizable blockchains as you need.

I will keep developing yu, I hope developers can use it to develop app-specific chains easier and it can even help developers from web2 easily get started developing L3 appchain.

I hope to receive suggestions and opinions from everyone,

Please connect me any time if you want.  [crocdilechan@gmail.com](mailto:crocdilechan@gmail.com)

Thank you very much.

## Replies

**1010adigupta** (2023-11-05):

How is this different and more advanced than, Zksync’s Hyperchains or Substrate’s parachains or tendermint system?

---

**Lawliet-Chan** (2023-11-05):

Zksync’s hyperchains,  polkadot’s parachains are definations.

Substrate is a SDK, tendermint is the base for cosmos-sdk, they are development framework.

The frameworks can implement the definations. In fact, all these frameworks can almost implement  various blockchains theoretically no matter which Layer they are.  For example, Madara of StarkNet is built by Substrate, but Madara is not the parachain, it is a decentralized sequencer.

Yu has a higher degree of customization compared to other frameworks, and the development threshold is much lower than those frameworks(just like developing web APIs)

For details, pls refer to these links:



      [github.com](https://github.com/yu-org/yu/blob/master/README.md)





####



```md
# 禹

Yu is a highly customizable blockchain framework.

[Book](https://yu-org.github.io/yu-docs/en/)
[中文文档](https://yu-org.github.io/yu-docs/zh/)

### Overall Structure
![image](yu_flow_chart.png)

### Usage
```go
type Example struct {
    *tripod.Tripod
}

// Here is a custom development of an Writing
func (e *Example) Write(ctx *context.WriteContext) error {
    caller := ctx.GetCaller()
    // set this Writing lei cost
```

  This file has been truncated. [show original](https://github.com/yu-org/yu/blob/master/README.md)










[https://yu-org.github.io/yu-docs/en/2.快速开始.html](https://yu-org.github.io/yu-docs/en/2.%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.html)

---

**BirdPrince** (2023-11-09):

Have you considered that the migration of liquidity and tools is a huge undertaking?

And how do you ensure the consensus and security of YU-based application chains?

---

**Lawliet-Chan** (2023-11-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/birdprince/48/13573_2.png) BirdPrince:

> And how do you ensure the consensus and security of YU-based application chains?

Yu is a blockchain framework, it means you can customize your consensus. The consensus and security of Yu-based application chains depends on whether the consensus you design is safe or not.

What specifically do you mean by  liquidity and tool migration?

---

**maniou-T** (2023-11-10):

Your insights into Yu’s features are fascinating, especially the emphasis on customizability and modularity. It’s clear that Yu is designed with developers in mind. I’m curious if you could share a real-world example or case study where Yu’s customizability has played a pivotal role in the development of an app-specific blockchain. Looking forward to learning more!

---

**Lawliet-Chan** (2023-11-10):

Thank you for your appreciation.

Taking some examples:

1. Customized Dex: A ready-made example is dydx, they used cosmos-sdk to customize their dex appchain.
2. The decentralized sequencer: it is really an application chain. You may design the consensus for your sequencer chain and it can not copy the traditional Layer1 consensus. Also you need to compatible with the deferent blokchain protocol except Ethereum.
3. Some future web3 apps: for example, Web3 Uber. You may develop a decentralized O2O-Taxi software. Can you use smart contract development? Maybe not, you may develop an appchain with a traditional program language and define/transfer your assets on Ethereum L1/L2.

