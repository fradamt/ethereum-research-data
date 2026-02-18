---
source: ethresearch
topic_id: 15390
title: Enabling DNN Model Inference on the Blockchain
author: Canhui.Chen
date: "2023-04-23"
category: Applications
tags: []
url: https://ethresear.ch/t/enabling-dnn-model-inference-on-the-blockchain/15390
views: 2595
likes: 6
posts_count: 8
---

# Enabling DNN Model Inference on the Blockchain

Hi all!  I have enabled AI model inference in blockchain systems in both on-chain and off-chain approaches.

My code is still under development, I will consider making it open-sourced once it’s in a more polished state. If you’re interested in exploring this project or joining the effort, feel free to contact me. I would welcome any questions or discussion.

## On-chain Approach

The smart contract execution environment in the existing blockchain systems lacks operators, instructions, and corresponding mechanisms to support complex DNN operations with high computational and memory complexity, which makes it inefficient or even infeasible to do the AI model inference on chain.

In order to enable on-chain AI model inference, I have extended the operation set in the EVM to support efficient DNN computation. Additionally, I have modified the Solidity compiler to allow for direct AI model inference calls in smart contracts. Currently, I have successfully run small AI model inferences such as a GAN model, which generated some impressive NFT art ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

However, this on-chain approach requires the modification of the EVM, rendering it incompatible with existing Ethereum systems. Therefore, I have shifted my focus to investigating an off-chain approach to address this issue.

## Off-chain Approach

For off-chain AI model inference, I have adopted the optimistic rollup approach which is compatible with Ethereum and other blockchain systems that support smart contract execution.

To ensure the efficiency of AI model inference in the rollup VM, I have implemented a lightweight DNN library specifically designed for this purpose instead of relying on popular ML frameworks like Tensorflow or PyTorch. Additionally, I have provided a script that can convert Tensorflow and PyTorch models to this lightweight library. The cross-compilation technology has been applied to compile the AI model inference code into rollup VM code.

**Performance**: I have tested a basic AI model (a DNN model for MNIST classification) on a PC. I was able to complete the DNN inference within 3 seconds in the rollup VM, and the entire challenge process can be completed within 2 minutes in a local Ethereum test environment.

Despite my unoptimized implementation, this level of performance seems to be acceptable for the current blockchain system.  I plan to further optimize my implementation further to support larger and more complex models such as Stable Diffusion and GPT-2. Optimistically, I believe it will not take me too long to make it practical ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

## Motivation

- Enabling AI model inference on the blockchain can allow for the creation of truly “smart” applications using smart contracts. For instance, embedding ChatGPT on the blockchain would provide the opportunity to develop fascinating metaverse applications on-chain.
- With an off-chain approach to AI model inference, users with available computing power can utilize their resources to complete the tasks of AI model inference and receive corresponding rewards. This can incentivize miners to use their computing power more efficiently, instead of engaging in PoW mining, which could be significant for miners in the previous PoW ETH.

## Replies

**TurboGGS** (2023-04-24):

Hi, that is so interesting! I feel like there would be many fantastic use cases for it. As a non-tech player, may I ask how would the smart app with smart contracts works? Is that means I can send prompts to the model by one transaction? What’s more interesting is that if we want to do a complex defi move with Ai within one transaction, for example send prompts to ask the suggestion from ai, get feedback, swap,do a sandwich attack or flash loan according to the feedback

---

**Canhui.Chen** (2023-04-24):

Thanks for your interest!  You can send inputs (or prompts) to the AI model via a smart contract transaction. The smart contract would then execute the necessary computations using the AI model and provide outputs (or feedback) back to the user. And it is indeed possible to use AI in conjunction with DeFi moves within a single transaction. This could potentially lead to more efficient and automated decision-making within the DeFi space.

The on-chain approach enables AI model inference directly within a smart contract, with a user-friendly interface.

```auto
contract AIContract {
	//...
	function modelInfer(address model_address, bytes memory input_data, uint output_size) public pure returns (bytes memory) {
		bytes memory output = new bytes(output_size)
		// AI model inference interaface
		infer(model_address, input_data, output)
		return output
	}
}
```

To use this approach, the model needs to be stored on the blockchain at `model_address`. Once the model is available, the `infer` function (which has been added through modifications to the Solidity compiler and EVM operation set) can be used to perform the AI model inference on-chain and retrieve the results.

As for the off-chain approach, the user-friendly interface is still under development. Once it’s completed, I will consider publishing and deploying it on the Ethereum test network so that anyone can use the AI model in a decentralized manner.

---

**TurboGGS** (2023-04-24):

Awesome ! Can’t wait to use it and good luck with your development!

btw, I am also a graduate student and I am from Sun Yat-sen University. Is it convenient for you to leave some contact details such as WeChat or etc.?  We can have more communication later after.

---

**Ubrobie** (2023-04-29):

Awesome idea! It would be huge to run ML on Ethereum.

Can you provide more details on the cross-compilation technology used to compile AI model inference code into rollup VM code? How does this process ensure the compatibility and efficiency of the models?

I’m curious if there are more examples of potential use cases for AI model inference on the blockchain beyond metaverse?

Also, would it be potentially possible to enable AI training on the blockchain?

---

**Canhui.Chen** (2023-05-03):

Regarding the cross-compilation technology used in the rollup system, we require a VM on-chain to verify the one-step fraud proof, and we execute the equivalent VM off-chain. To achieve this, we can use a WASM runtime VM or a simple MIPS VM. I currently use the MIPS VM because of its simplicity. Cross-compilation toolchains are available to compile code written in C/C++, Golang, Rust, etc., into the target VM. To ensure the determinism of floating-point calculations, I enforce computation in a single thread with a soft float library. The provided converter to the lightweight ML framework and the cross-compilation tool guarantee the compatibility of the models. I have tested this with some small models, and it works well.

In addition to the metaverse, we can apply ML models to DeFi, creating the possibility of designing an intelligent AMM. Decentralized AI marketplaces can also be hosted on blockchain systems, and fraud detection and prediction markets can be established on-chain. We may even deploy a decentralized recommendation algorithm for DApps.

With respect to enabling AI training on the blockchain, it is technically feasible but may be inefficient. However, I am actively working to make it practical.

---

**0xtrident** (2023-05-03):

Interesting. Curious to learn more about the off-chain piece and which part of the inference or model is off-chain. Thanks.

---

**parseb** (2023-05-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/74df32/48.png) Canhui.Chen:

> could potentially lead to more efficient and automated decision-making within the DeFi space

What is the value added by having models on-chain? Is it about control? Inner-workings transparency? Faster crowd-sourced iterations in real adversarial economic env.?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/74df32/48.png) Canhui.Chen:

> In addition to the metaverse, we can apply ML models to DeFi, creating the possibility of designing an intelligent AMM. Decentralized AI marketplaces can also be hosted on blockchain systems, and fraud detection and prediction markets can be established on-chain. We may even deploy a decentralized recommendation algorithm for DApps.

These all can more or less be done already and don’t seem too leverage much the on-chain environment. Will happen, just not eager to see resources plunging in porting existing things as I feel like most of the web2 uses have no teeth on-chain.

I am sure artificial agents will manage their own energy budgets and dominate on-chain activity.

