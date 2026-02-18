---
source: ethresearch
topic_id: 17017
title: The Application of ZK-SNARKs in Solidity - Privacy Transformation, Computational Optimization, and MEV Resistance
author: Mirror
date: "2023-10-09"
category: zk-s[nt]arks
tags: [mev, zk-roll-up]
url: https://ethresear.ch/t/the-application-of-zk-snarks-in-solidity-privacy-transformation-computational-optimization-and-mev-resistance/17017
views: 44027
likes: 14
posts_count: 11
---

# The Application of ZK-SNARKs in Solidity - Privacy Transformation, Computational Optimization, and MEV Resistance

Authors: [Mirror Tang](https://scholar.google.com/citations?user=_F_wFPAAAAAJ&hl=en) , Shixiang Tang , [Shawn Chong](https://www.linkedin.com/in/shawnceth/) ,Yunbo Yang

# Introduction

Ethereum is a blockchain-based open platform that allows developers to build and deploy smart contracts. Smart contracts are programmable codes on Ethereum that enable the creation of various applications. With the development of Ethereum, certain issues and challenges have emerged, including privacy concerns in applications. Defi applications involve a large amount of address information and user funds. Protecting the privacy of transactions is crucial for users in certain application scenarios. By utilizing privacy-preserving technologies, transaction details can be made visible only to involved parties and not to the public. Through the use of [ZK-SNARKs](https://vitalik.ca/general/2021/01/26/snarks.html) (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge), we can implement transformations on existing applications on Ethereum. This includes adding features such as private transfers, private transactions, private orders, and private voting to existing projects on Ethereum, as well as optimizing computations and addressing MEV (Maximal Extractable Value) challenges in Ethereum application-layer projects.

Through this research, our aim is to promote privacy in the Ethereum application layer and address issues related to privacy transformation, computational optimization (such as [Rollup](https://vitalik.ca/general/2021/01/05/rollup.html)), and [MEV](https://ethereum.org/en/developers/docs/mev/) resistance on Ethereum.

# Existing Issues

1. Competitor Analysis: Smart contracts without privacy features are susceptible to competitor analysis and monitoring. Competitors can gain sensitive information about business operations and strategies by observing and analyzing transaction patterns and data of the contract, thereby weakening competitive advantages.
2. Transaction Traceability: In the absence of privacy features, contract transactions are traceable, and the participants and contents of the transactions can be tracked and identified. This exposes transaction intentions and participants for certain transactions, such as anonymous voting or sensitive transactions.
3. Data Security: Data in smart contracts has become a primary target for attackers. Contracts without privacy features are at risk of data leakage, tampering, or malicious attacks. Attackers often exploit and manipulate contract data through analysis to carry out malicious activities, causing harm to users and contracts.

# Technical Barriers

**EVM Smart Contract Multithreading**: Currently, direct implementation of [multithreading](https://foresightnews.pro/article/detail/34400) is not possible in Ethereum smart contracts. Ethereum adopts an account-based execution model, where each transaction is executed sequentially in a single thread. This is because Ethereum’s consensus mechanism requires sequential verification and execution of transactions to ensure consensus among all nodes. Smart contracts in Ethereum face performance bottlenecks when dealing with large-scale data. To run a significant number of smart contracts containing zero-knowledge proofs on-chain, optimizations such as asynchronous calls, event-driven programming, and delegation splitting need to be implemented to achieve concurrent execution.

**Auditable Zero-Knowledge (ZK)**: [Auditable](https://medium.com/consensys-media/how-is-blockchain-verifiable-by-the-public-and-yet-anonymous-f7415a3231d2) ZK refers to the ability of verifiers to provide received zero-knowledge proofs to third parties (usually the public) for verifying their validity without going through the entire proof process again. This means that third parties can verify the correctness of the proof without knowing the specific details of the statement. Auditable ZK requires more computation and storage operations compared to general ZK implementations, especially in the verification phase. This may have an impact on the performance and resource consumption of smart contracts, placing higher demands on the performance optimization of Solidity and corresponding ZK circuits.

**Proof System Scalability**: Existing proof systems suffer from scalability issues, making it difficult to support large-scale circuits, such as proving LLM circuits. Current potential scalability solutions include [recursive proofs](https://github.com/privacy-scaling-explorations/nova-bench) and [distributed proofs](https://zhuanlan.zhihu.com/p/144908164), which have the potential to enhance the scalability of proof systems and provide solutions for proving large-scale circuits.

**Proof System Security Risks**: Some proof systems, such as Groth16 and Marlin, rely on a [trusted setup](https://vitalik.ca/general/2022/03/14/trustedsetup.html) (also known as toxic waste) that is privately generated. Once made public, the security of the entire proof system cannot be guaranteed.

# Currently Used zk-SNARKs Schemes

## Groth16 (Used by Zcash currently)

In the case where the adversary is restricted to only linear/affine operations, Groth constructed a LIP with a communication cost of only 3 elements based on QAP. Based on this LIP, it constructed a zk-SNARK with a communication cost of 3 group elements and a verifier computational cost of only 4 pairing operations (known as [Groth16](https://eprint.iacr.org/2016/260.pdf)).

**Advantages**: Small proof size, currently the fastest verification speed.

**Disadvantages**: Trusted setup bound to the circuit, meaning that a new trusted setup is required for generating proofs for a different circuit, and the trusted setup cannot be dynamically updated.

## Marlin

To address the inability of zk-SNARKs schemes to achieve global updates, Groth et al. based on QAP, proposed a zk-SNARK with a global and updatable Common Reference String (updatable universal CRS), denoted as [GKMMM18](https://eprint.iacr.org/2018/280.pdf).Building on this, Maller et presented [Sonic](https://eprint.iacr.org/2019/099.pdf) scheme that utilized the permutation argument, grand-product argument, and other techniques to achieve a globally updatable CRS with a size of O(|C|), concise NIZKAoK without additional preprocessing, under the algebraic group model.

[Marlin](https://eprint.iacr.org/2019/1021.pdf) is a performance-improved scheme of Sonic (as is Plonk), primarily optimizing the SRS preprocessing and polynomial commitment, thereby reducing the proof size and verification time of the proof system."

**Advantages**: Support for globally updatable trusted setup, achieving succinct verification in an amortized sense.

**Disadvantages**: High complexity in the proof process, less succinct proof size compared to Groth16.

## Plonk

[Plonk](https://eprint.iacr.org/2019/953.pdf) is also an optimization of the Sonic scheme, introducing a different circuit representation called Plonkish, which is different from R1CS (Rank-1 Constraint System) and allows for more scalability, such as lookup operations. Plonk optimizes permutation arguments through “Evaluation on subgroup rather than coefficient of monomials” and leverages Lagrange basis polynomials.

**Advantages**: Support for globally updatable trusted setup, fully succinct verification, and a more scalable circuit representation in Plonkish.

**Disadvantages**: Marlin may perform better in cases with frequent large addition fan-in; less succinct proof size compared to Groth16.

## HALO2

To reduce proving complexity and the burden on the Prover, researchers introduced recursive proofs and proposed the [Halo](https://eprint.iacr.org/2019/1021.pdf) proof system (as introduced by [Vitalik’blog](https://vitalik.ca/general/2021/11/05/halo.html)). The Halo proof system adopts the Polynomial IOP (Interactive Oracle Proof) technique from Sonic, describes a Recursive Proof Composition algorithm, and replaces the Polynomial Commitment Scheme in the algorithm with the Inner Product argument technique from Bulletproofs, eliminating the reliance on a Trusted Setup.

Halo2 is a further optimization of Halo, mainly in the direction of Polynomial IOP. In recent years, researchers have discovered more efficient Polynomial IOP schemes than those used in Sonic, such as Marlin and Plonk. Among them, Plonk was chosen due to its support for more flexible circuit designs.

**Advantages**: No need for a trusted setup; introduces recursive proofs to optimize proof speed.

**Disadvantages**: Less succinct proof size.

## Circom + Snarkjs

Circom + Snarkjs is a major tool chain to build the zkSNARK proving system. [Snarkjs](https://github.com/iden3/snarkjs) is a JavaScript library for generating zk-SNARK proofs. This library includes all tools required to build a zkSNARK proof. To prove the validity of a given witness, an arithmetic circuit is first generated by Circom, then a proof is generated by Snarkjs. For the usage about this tool chain, we refer the reader to the [guidance](https://github.com/iden3/snarkjs).

**Advantages**: This toolchain inherits the advantages of zkSNARKs such as Groth16, namely having smaller proof sizes and faster verification times.  In order to reduce overall costs, The computationally expensive operations (FFT and MSM) at the prover side can be done off-chain. If Groth16 is used for proving, the proof size on-chain consists of only three group elements, and the verifier can validate proof in a very short time, which leads to lower gas fee. In addition, this tool chain can handle large-scale computing, and the proof size as well as verification time is independent of the size of the computation task.

**Disadvantages**:This language is not particularly ergonomic, making developers keenly aware that they are writing circuits.

### Performance comparison

We use different programming languages (Circom, Noir, Halo2) to write the same circuit, and then test the proving and verifier time with different numbers of rounds. We run all experiments on the Intel Core i5 processor with 16GB RAM and MacOS 10.15.7. The experimental codes are shown in [[link](https://github.com/yyb9882/yyb1)] .

[![1699022015623](https://ethresear.ch/uploads/default/optimized/2X/7/7160976b51db5d4c28a4141af026860694f3780b_2_690x324.png)1699022015623989×465 17.4 KB](https://ethresear.ch/uploads/default/7160976b51db5d4c28a4141af026860694f3780b)

The above table is the experimental results. It shows that the circuit written in Circom outperforms in terms of the prover time, with only around 1s for 10 rounds, and Halo2 outperforms in terms of the verifier time when the circuit size is small.

Both the circuit written in Circom and Noir relies on KZG commitment. Therefore, the overall verifier time of Circom and Noir is independent of the circuit size (number of rounds in the table).  Meanwhile, Halo2 relies on the commitment scheme called inner product argument (IPA). The verifier time of IPA is logarithmic to the circuit size. With the increment of circuit size, the verification time will increase gently.

Generally speaking, circuit written in Circom enjoys the best prover time and verification time.

## Enclave: interactive shielding

In terms of  privacy protection, pure zk proving system can not construct a complete solution. For example, when considering the privacy of transaction information, we can use ZK technology to construct a dark pool. Orders within this dark pool are in a shielded state, which means they are obfuscated, and their contents cannot be discerned from the on-chain data by anyone. This condition is referred to as “fragmentation in shielded state.” However, when users need to maintain state variables, i.e., initiate transactions, they have to gain knowledge of these shielded pieces of information. So, how do we ascertain shielded information while ensuring its security? This is where enclaves come into play. An enclave is an off-chain secure storage area for confidential computations and data storage. How do we ensure the security of enclaves? For the shielding property in the short term, one may use secure hardware modules. In the long term, one should have systems in place for transitioning to trust-minimized Multi-Party Computation (MPC) networks.

With the introduction of enclaves, we will be able to implement interactive shielding. Namely, users can interact with fragmented shielded information while ensuring securiry. Implementing interactive shielding opens up unlimited possibilities while maintaining privacy.

**The ability to have shielded state interact opens up a rich design space that’s largely unexplored. There’s an abundance of low hanging fruit:**

1. Gamers can explore labryinths with hidden treasures from previous civilizations, raise fortresses that feign strength with facades of banners, or enter into bountiful trade agreements with underground merchants.
2. Traders can fill orders through different dark pool variants, insure proprietary trading strategies through RFQ pools with bespoke triggers, or assume leveraged positions without risk of being stop hunted.
3. Creators can generate pre-release content with distributed production studios, maintain exclusive feeds for core influencers, or spin up special purpose DAOs with internal proposals for competitive environments.

Currently available ZK enclaves:

**Seismic**

https://seismicsystems.substack.com/p/on-a-treasure-hunt-for-interactive?r=2zhkov&utm_campaign=post&utm_medium=web

## How to integrate with Solidity?

For the Groth16 and Marlin proof systems, there are already high-level circuit languages and compilers that provide support for solidity, such as [Circom](https://docs.circom.io/)  for Groth16 and Plonk, and [zokrate](https://zokrates.github.io/) for Groth16 and marlin proof systems.

For the halo2 proof system, Chiquito is the DSL of HALO2（Provided by Dr. CathieSo from the PSE team of the Ethereum Foundation）:



      [github.com](https://github.com/privacy-ethereum/chiquito)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/c/0/c098b9a46d8b2e2b9025d70a3dd2a950986a65aa_2_690x344.png)



###



DSL for Halo2 circuits










# Scenario demonstration of ZK-SNARKs integration using Solidity

## Privacy Enhencement

Assuming we need to hide the price of a limit order from the chain and the order is represented as O=(t,s) , where t:= (\phi, \chi, d) , s:= (p, v, α)

> \phi:  side of the order, 0 when it’s a bid, 1 when it’s an ask
>
>
> \chi:  token address for the target project
>
>
> d: denomination, either the token address of USDC or ETH.  Set 0x0 represent USDC and 0x1 represent ETH.
>
>
> p: price, denominated in d
>
>
> v: volume, the number of tokens to trade
>
>
> \alpha: access key, a random element in bn128’s prime field , which mainly used as a blinding factor to prevent brute force attacks

The information we want to hide is the price, but in order to generate proof, we must expose the value related to the price, which is the balance `b`  required for this order. Specifically, if it’s a bid order, the bidder need to pay the required amount of denomination token for the order; If it is a ask order, the seller needs to pay the target token they want to sell. The balance `b` is a pair with the first element specifying an amount of the target project’s token and the second element specifying an amount of the denomination token.

In general, we use poseidon hash to mask out the price and volume of the order and only display the balance required for this order. We use zksnark to prove that the balance is indeed consistent with the price required for the order.

Here is the example circom code:

```circom
pragma circom 2.1.6;

include "circomlib/poseidon.circom";
// include "https://github.com/0xPARC/circom-secp256k1/blob/master/circuits/bigint.circom";
template back() {
    // 1. load input
    signal input phi; // order type, 0 when it is a bid order, otherwise 1
    signal input x;   // target token address
    signal input d;   // domination
    signal input p;   // price
    signal input v;   // volumn
    signal input alpha; // access key

    // 2. define output and temporary signal
    signal output O_bar[4];
    signal output b[2];

    signal temp;

    // 3. construct shielded order O_bar
    // check phi
    phi * (phi - 1) === 0;

    O_bar[0] <== phi;
    O_bar[1] <== x;
    O_bar[2] <== d;

    component hasher = Poseidon(3);
    hasher.inputs[0] <== p;
    hasher.inputs[1] <== v;
    hasher.inputs[2] <== alpha;
    O_bar[3] <== hasher.out;

    // 4. compute b
    // if it's a bid, b[0] = 0, b[1] = p * v
    // else, b[0] = v, b[1] = 0
    b[0] <== v * phi;
    temp <== p * v;
    b[1] <== (1 - phi) * temp;
}

component main{public [phi, x, d]} = back();

/* INPUT = {
    "phi": "1",
    "x": "0x0",
    "d": "0x1",
    "p": "1000",
    "v": "2",
    "alpha": "912"
} */
```

Prover can use the above circuit to generate proof for specific orders using the Circom+Snarkjs toolchain. The Snarkjs tool can export `Verifier.sol`, with the following content [I am using the plonk proof system]. Run command:

```auto
snarkjs zkey export solidityverifier final.zkey verifier.sol
```

then we get the [verifier.sol](https://github.com/Mirror-Tang/The-Application-of-ZK-SNARKs-in-Solidity/blob/master/verifier.sol)

And then, the project developer can use the verifier.sol to construct their project with solidity. The following code is just for demonstration.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Verifier.sol";

contract PrivacyPreservingContract {
    Verifier public verifier;

    struct ShieldedOrder {
        uint phi;  // order type
        uint x;    // target token address
        uint d;    // domination
        uint h;    // hash
    }

    ShieldedOrder[] public orders;

    constructor(address _verifier) {
        verifier = Verifier(_verifier);
    }

    function shieldOrder(
        uint[2] calldata a,
        uint[2][2] calldata b,
        uint[2] calldata c,
        uint[4] calldata input
    ) public {
        // verify the zk-SNARK proof
        require(verifier.verifyTx(a, b, c, input), "Invalid proof");

        // create the shield order
        ShieldedOrder memory newOrder = ShieldedOrder({
            phi: input[0],
            x: input[1],
            d: input[2],
            h: input[3],
        });

        // Store new orders in status variables
        orders.push(newOrder);
    }

    // your project logic
}
```

The last thing I need to emphasize that privacy enhancement has actually brought **MEV resistance** to this project. So I will no longer do anti MEV demonstrations.

## Computational Optimization

Assuming we want to execute the heavy AMM logic off-chain, we only need to perform computational verification operations on the chain.

The following is a simple AMM logic circuit (as an example only, the calculation logic of the actual protocol is much more complex)

```circom
template AMM() {
    signal input reserveA;
    signal input reserveB;
    signal input swapAmountA;

    signal output receivedAmountB;
    signal output newReserveA;
    signal output newReserveB;

    // x * y = k
    // newReserveA = reserveA + swapAmountA
    // newReserveA * newReserveB = reserveA * reserveB
    // newReserveB
    newReserveA <== reserveA + swapAmountA;
    newReserveB <== (reserveA * reserveB) / newReserveA;

    // compute the amount of tokenB
    receivedAmountB <== reserveB - newReserveB;

		// more computation operations...
}

component main = AMM();
```

Similarly, it is necessary to use the circom+snarkjs toolchain to generate proof and export it to verifier.sol.

Finally, AMM project developers can develop their logic code with  `verifier.sol` in  solidity. The example solidity code for the on chain check contract is as follows:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Verifier.sol";

contract AMMWithSnarks {
    Verifier public verifier;

    constructor(address _verifier) {
        verifier = Verifier(_verifier);
    }

    function swap(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[2] memory input,
        uint256 amountA
    ) public returns (uint256) {
        // Verification of zk-SNARKs proofs
        require(verifier.verifyTx(a, b, c, input), "Invalid proof");

        // The actual exchange logic is omitted, as the verification is done through zk-SNARKs

        // Return the amount of tokens obtained after the exchange, which requires calculation in the actual implementation
        return amountA * 2; // Here is just an example of the return value
    }

    // other function，such as addLiquidity, removeLiquidity etc.
}
```

## Anti-MEV attacks

After privacy modification of protocol contracts, MEV attacks often fail to be achieved. Please refer to examples of privacy modification.

# Conclusions

From the example above, we can see that integrating ZK-SNARKs technology into Solidity can effectively address issues of privacy, computational optimization, and resistance to MEV (Maximum Extractable Value) in Ethereum applications. ZK-SNARKs offer privacy features, making it possible to implement private transfers, private transactions, private orders, and private voting within existing Ethereum projects. At the same time, ZK-SNARKs can optimize computational processes and address challenges related to MEV resistance in application-layer projects on Ethereum. By leveraging ZK-SNARKs technology, developers can enhance the privacy, performance, and security of their applications. This reaffirms the feasibility of writing ZK applications in Solidity on Ethereum and indicates that it is a trend for future development. This will bring improved privacy protection, computational optimization, and MEV resistance capabilities to the Ethereum ecosystem, propelling further development and innovation in Ethereum applications.

# Possible Improvements and Future Work

## Establishing a Public ZK Verification Layer on the Ethereum Blockchain

This can provide various benefits such as privacy protection, scalability, flexibility, and extensibility. This can help drive the adoption of ZK technology in the Ethereum ecosystem and provide users and developers with more secure, efficient, and flexible verification solutions.

## ZK Performance Optimization in Solidity

Considering methods such as batching techniques, optimizing computation and communication, parallel computing, caching and precomputation, and optimizing the verification process to improve the performance of ZK calls in Solidity. Enhancing the computational efficiency of ZK proofs, reducing communication overhead, and improving the overall performance of the ZK system.

## Establishing Reusable Solidity ZK Components

This contributes to code maintainability and reusability, promotes collaboration and sharing, improves code scalability, and provides better code quality and security. These components can help developers efficiently develop Solidity applications and also contribute to the growth and development of the entire Solidity community

## Replies

**maniou-T** (2023-10-09):

I like how it breaks down privacy issues and shows how using ZK-SNARKs can make things more private and efficient. The examples make it easier to understand, especially the parts about privacy, optimization, and fighting against certain attacks.  Sincerely, nice job!

---

**DegenMarkus** (2023-10-09):

The authors have brilliantly underscored the significance of both privacy and computational prowess in Ethereum-based applications. The article’s conclusion further solidifies the practicality and promise of ZK-centric applications within Solidity, marking a pivotal direction for Ethereum’s evolution. I’m curious, though: when can we anticipate the debut of Zk-SNARKs within Solidity? The timeline seems rather extended given the challenges.

---

**BirdPrince** (2023-10-12):

Thanks for your contribution. Here are several questions.

1. Why is integrating Solidity and Halo2 more difficult, and what is the key breakthrough to solve this problem?
2. Is an instruction set in the Verifier library incompatible with the official EVM library?
3. In the example of Privacy Enhancement, we need to create a new transaction object and store it in the transactions map. Is there a risk of centralization here?
4. Regarding Anti-MEV attacks, is another alternative mempool needed to handle transactions using ZK-SNARKs?

---

**yanyanho** (2023-10-13):

Thanks for your contribution.   What I understand is that the zkdapp is to calculate off-chain, verify, and change state on-chain.  The trouble is still how to convert the business logic of dex, loan protocol to circuits, and then generate proof. Could you give some reference links about these?

What’s more ,    expect a follow-up series that gives code analysis of the verify function in solidity for each zk algorithm.

---

**Mirror** (2023-10-19):

In fact, zk technology has been widely used in Solidity for a long time. Zokrates is a great toolbox for this purpose: [Introduction - ZoKrates](https://zokrates.github.io/introduction.html).

However, looking back at history, it did not receive enough attention. Tornado Cash is a good example, but we should consider more gentle and friendly privacy cases.

---

**Mirror** (2023-10-19):

Answers to your questions:

1. Why is it more difficult to integrate Solidity with Halo2, and what is the key breakthrough to solve this problem?
The integration between Solidity and Halo2 is more challenging because the Solidity tooling and ecosystem for Halo2 are still incomplete. The key breakthrough to solve this problem is the establishment of a comprehensive toolset and transaction verification library.
2. Is the instruction set in the verification program library incompatible with the official EVM library?
There is no compatibility issue between the instruction set in the verification program library and the official EVM library because all ZK verifications occur off-chain. Since they cannot run on-chain, compatibility is not a concern.
3. In the example of Privacy Enhancement, is there a risk of centralization by creating a new transaction object and storing it in the transaction mapping?
The risk of centralization depends on the application designer. The provided example is merely a simple demonstration of functionality.
4. Regarding anti-MEV attacks, is there a need for an alternative mempool to handle transactions using ZK SNARK?
No, there is no need for an alternative mempool. For Ethereum, a transaction using ZK SNARK is not significantly different from a regular transfer transaction.

---

**Mirror** (2023-10-24):

Unable to edit the theme, let me put the updated circom circuit in the comment section. The following code supplements the circuit parts for the three ZK scenarios mentioned in the original text:

## Privacy Enhencement

Assuming we need to hide the price of a hanging order transaction, there is the following circuit:

```auto
pragma circom 2.1.6;

include "circomlib/poseidon.circom";
// include "https://github.com/0xPARC/circom-secp256k1/blob/master/circuits/bigint.circom";
template back() {
    // 1. load input
    signal input phi; // order type, 0 when it is a bid order, otherwise 1
    signal input x;   // target token address
    signal input d;   // domination
    signal input p;   // price
    signal input v;   // volumn
    signal input alpha; // access key

    // 2. define output and temporary signal
    signal output O_bar[4];
    signal output b[2];

    signal temp;

    // 3. construct shielded order O_bar
    // check phi
    phi * (phi - 1) === 0;

    O_bar[0] .
*/

pragma solidity >=0.7.0  inv {
                let t := 0
                let newt := 1
                let r := q
                let newr := a
                let quotient
                let aux

                for { } newr { } {
                    quotient := sdiv(r, newr)
                    aux := sub(t, mul(quotient, newt))
                    t:= newt
                    newt:= aux

                    aux := sub(r,mul(quotient, newr))
                    r := newr
                    newr := aux
                }

                if gt(r, 1) { revert(0,0) }
                if slt(t, 0) { t:= add(t, q) }

                inv := t
            }

            ///////
            // Computes the inverse of an array of values
            // See https://vitalik.ca/general/2018/07/21/starks_part_3.html in section where explain fields operations
            //////
            function inverseArray(pVals, n) {

                let pAux := mload(0x40)     // Point to the next free position
                let pIn := pVals
                let lastPIn := add(pVals, mul(n, 32))  // Read n elemnts
                let acc := mload(pIn)       // Read the first element
                pIn := add(pIn, 32)         // Point to the second element
                let inv


                for { } lt(pIn, lastPIn) {
                    pAux := add(pAux, 32)
                    pIn := add(pIn, 32)
                }
                {
                    mstore(pAux, acc)
                    acc := mulmod(acc, mload(pIn), q)
                }
                acc := inverse(acc, q)

                // At this point pAux pint to the next free position we substract 1 to point to the last used
                pAux := sub(pAux, 32)
                // pIn points to the n+1 element, we substract to point to n
                pIn := sub(pIn, 32)
                lastPIn := pVals  // We don't process the first element
                for { } gt(pIn, lastPIn) {
                    pAux := sub(pAux, 32)
                    pIn := sub(pIn, 32)
                }
                {
                    inv := mulmod(acc, mload(pAux), q)
                    acc := mulmod(acc, mload(pIn), q)
                    mstore(pIn, inv)
                }
                // pIn points to first element, we just set it.
                mstore(pIn, acc)
            }

            function checkField(v) {
                if iszero(lt(v, q)) {
                    mstore(0, 0)
                    return(0,0x20)
                }
            }

            function checkInput() {
                checkField(calldataload(pEval_a))
                checkField(calldataload(pEval_b))
                checkField(calldataload(pEval_c))
                checkField(calldataload(pEval_s1))
                checkField(calldataload(pEval_s2))
                checkField(calldataload(pEval_zw))
            }

            function calculateChallenges(pMem, pPublic) {
                let beta
                let aux

                let mIn := mload(0x40)     // Pointer to the next free memory position

                // Compute challenge.beta & challenge.gamma
                mstore(mIn, Qmx)
                mstore(add(mIn, 32), Qmy)
                mstore(add(mIn, 64), Qlx)
                mstore(add(mIn, 96), Qly)
                mstore(add(mIn, 128), Qrx)
                mstore(add(mIn, 160), Qry)
                mstore(add(mIn, 192), Qox)
                mstore(add(mIn, 224), Qoy)
                mstore(add(mIn, 256), Qcx)
                mstore(add(mIn, 288), Qcy)
                mstore(add(mIn, 320), S1x)
                mstore(add(mIn, 352), S1y)
                mstore(add(mIn, 384), S2x)
                mstore(add(mIn, 416), S2y)
                mstore(add(mIn, 448), S3x)
                mstore(add(mIn, 480), S3y)


                mstore(add(mIn, 512), calldataload(add(pPublic, 0)))

                mstore(add(mIn, 544), calldataload(add(pPublic, 32)))

                mstore(add(mIn, 576), calldataload(add(pPublic, 64)))

                mstore(add(mIn, 608), calldataload(add(pPublic, 96)))

                mstore(add(mIn, 640), calldataload(add(pPublic, 128)))

                mstore(add(mIn, 672), calldataload(add(pPublic, 160)))

                mstore(add(mIn, 704), calldataload(add(pPublic, 192)))

                mstore(add(mIn, 736), calldataload(add(pPublic, 224)))

                mstore(add(mIn, 768), calldataload(add(pPublic, 256)))

                mstore(add(mIn, 800 ), calldataload(pA))
                mstore(add(mIn, 832 ), calldataload(add(pA, 32)))
                mstore(add(mIn, 864 ), calldataload(pB))
                mstore(add(mIn, 896 ), calldataload(add(pB, 32)))
                mstore(add(mIn, 928 ), calldataload(pC))
                mstore(add(mIn, 960 ), calldataload(add(pC, 32)))

                beta := mod(keccak256(mIn, 992), q)
                mstore(add(pMem, pBeta), beta)

                // challenges.gamma
                mstore(add(pMem, pGamma), mod(keccak256(add(pMem, pBeta), 32), q))

                // challenges.alpha
                mstore(mIn, mload(add(pMem, pBeta)))
                mstore(add(mIn, 32), mload(add(pMem, pGamma)))
                mstore(add(mIn, 64), calldataload(pZ))
                mstore(add(mIn, 96), calldataload(add(pZ, 32)))

                aux := mod(keccak256(mIn, 128), q)
                mstore(add(pMem, pAlpha), aux)
                mstore(add(pMem, pAlpha2), mulmod(aux, aux, q))

                // challenges.xi
                mstore(mIn, aux)
                mstore(add(mIn, 32),  calldataload(pT1))
                mstore(add(mIn, 64),  calldataload(add(pT1, 32)))
                mstore(add(mIn, 96),  calldataload(pT2))
                mstore(add(mIn, 128), calldataload(add(pT2, 32)))
                mstore(add(mIn, 160), calldataload(pT3))
                mstore(add(mIn, 192), calldataload(add(pT3, 32)))

                aux := mod(keccak256(mIn, 224), q)
                mstore( add(pMem, pXi), aux)

                // challenges.v
                mstore(mIn, aux)
                mstore(add(mIn, 32),  calldataload(pEval_a))
                mstore(add(mIn, 64),  calldataload(pEval_b))
                mstore(add(mIn, 96),  calldataload(pEval_c))
                mstore(add(mIn, 128), calldataload(pEval_s1))
                mstore(add(mIn, 160), calldataload(pEval_s2))
                mstore(add(mIn, 192), calldataload(pEval_zw))

                let v1 := mod(keccak256(mIn, 224), q)
                mstore(add(pMem, pV1), v1)

                // challenges.beta * challenges.xi
                mstore(add(pMem, pBetaXi), mulmod(beta, aux, q))

                // challenges.xi^n

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                aux:= mulmod(aux, aux, q)

                mstore(add(pMem, pXin), aux)

                // Zh
                aux:= mod(add(sub(aux, 1), q), q)
                mstore(add(pMem, pZh), aux)
                mstore(add(pMem, pZhInv), aux)  // We will invert later together with lagrange pols

                // challenges.v^2, challenges.v^3, challenges.v^4, challenges.v^5
                aux := mulmod(v1, v1,  q)
                mstore(add(pMem, pV2), aux)
                aux := mulmod(aux, v1, q)
                mstore(add(pMem, pV3), aux)
                aux := mulmod(aux, v1, q)
                mstore(add(pMem, pV4), aux)
                aux := mulmod(aux, v1, q)
                mstore(add(pMem, pV5), aux)

                // challenges.u
                mstore(mIn, calldataload(pWxi))
                mstore(add(mIn, 32), calldataload(add(pWxi, 32)))
                mstore(add(mIn, 64), calldataload(pWxiw))
                mstore(add(mIn, 96), calldataload(add(pWxiw, 32)))

                mstore(add(pMem, pU), mod(keccak256(mIn, 128), q))
            }

            function calculateLagrange(pMem) {
                let w := 1

                mstore(
                    add(pMem, pEval_l1),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l2),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l3),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l4),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l5),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l6),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l7),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l8),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )

                w := mulmod(w, w1, q)


                mstore(
                    add(pMem, pEval_l9),
                    mulmod(
                        n,
                        mod(
                            add(
                                sub(
                                    mload(add(pMem, pXi)),
                                    w
                                ),
                                q
                            ),
                            q
                        ),
                        q
                    )
                )



                inverseArray(add(pMem, pZhInv), 10 )

                let zh := mload(add(pMem, pZh))
                w := 1


                mstore(
                    add(pMem, pEval_l1 ),
                    mulmod(
                        mload(add(pMem, pEval_l1 )),
                        zh,
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l2),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l2)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l3),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l3)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l4),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l4)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l5),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l5)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l6),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l6)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l7),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l7)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l8),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l8)),
                            zh,
                            q
                        ),
                        q
                    )
                )


                w := mulmod(w, w1, q)



                mstore(
                    add(pMem, pEval_l9),
                    mulmod(
                        w,
                        mulmod(
                            mload(add(pMem, pEval_l9)),
                            zh,
                            q
                        ),
                        q
                    )
                )




            }

            function calculatePI(pMem, pPub) {
                let pl := 0


                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l1)),
                                calldataload(add(pPub, 0)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l2)),
                                calldataload(add(pPub, 32)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l3)),
                                calldataload(add(pPub, 64)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l4)),
                                calldataload(add(pPub, 96)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l5)),
                                calldataload(add(pPub, 128)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l6)),
                                calldataload(add(pPub, 160)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l7)),
                                calldataload(add(pPub, 192)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l8)),
                                calldataload(add(pPub, 224)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )

                pl := mod(
                    add(
                        sub(
                            pl,
                            mulmod(
                                mload(add(pMem, pEval_l9)),
                                calldataload(add(pPub, 256)),
                                q
                            )
                        ),
                        q
                    ),
                    q
                )


                mstore(add(pMem, pPI), pl)
            }

            function calculateR0(pMem) {
                let e1 := mload(add(pMem, pPI))

                let e2 :=  mulmod(mload(add(pMem, pEval_l1)), mload(add(pMem, pAlpha2)), q)

                let e3a := addmod(
                    calldataload(pEval_a),
                    mulmod(mload(add(pMem, pBeta)), calldataload(pEval_s1), q),
                    q)
                e3a := addmod(e3a, mload(add(pMem, pGamma)), q)

                let e3b := addmod(
                    calldataload(pEval_b),
                    mulmod(mload(add(pMem, pBeta)), calldataload(pEval_s2), q),
                    q)
                e3b := addmod(e3b, mload(add(pMem, pGamma)), q)

                let e3c := addmod(
                    calldataload(pEval_c),
                    mload(add(pMem, pGamma)),
                    q)

                let e3 := mulmod(mulmod(e3a, e3b, q), e3c, q)
                e3 := mulmod(e3, calldataload(pEval_zw), q)
                e3 := mulmod(e3, mload(add(pMem, pAlpha)), q)

                let r0 := addmod(e1, mod(sub(q, e2), q), q)
                r0 := addmod(r0, mod(sub(q, e3), q), q)

                mstore(add(pMem, pEval_r0) , r0)
            }

            function g1_set(pR, pP) {
                mstore(pR, mload(pP))
                mstore(add(pR, 32), mload(add(pP,32)))
            }

            function g1_setC(pR, x, y) {
                mstore(pR, x)
                mstore(add(pR, 32), y)
            }

            function g1_calldataSet(pR, pP) {
                mstore(pR,          calldataload(pP))
                mstore(add(pR, 32), calldataload(add(pP, 32)))
            }

            function g1_acc(pR, pP) {
                let mIn := mload(0x40)
                mstore(mIn, mload(pR))
                mstore(add(mIn,32), mload(add(pR, 32)))
                mstore(add(mIn,64), mload(pP))
                mstore(add(mIn,96), mload(add(pP, 32)))

                let success := staticcall(sub(gas(), 2000), 6, mIn, 128, pR, 64)

                if iszero(success) {
                    mstore(0, 0)
                    return(0,0x20)
                }
            }

            function g1_mulAcc(pR, pP, s) {
                let success
                let mIn := mload(0x40)
                mstore(mIn, mload(pP))
                mstore(add(mIn,32), mload(add(pP, 32)))
                mstore(add(mIn,64), s)

                success := staticcall(sub(gas(), 2000), 7, mIn, 96, mIn, 64)

                if iszero(success) {
                    mstore(0, 0)
                    return(0,0x20)
                }

                mstore(add(mIn,64), mload(pR))
                mstore(add(mIn,96), mload(add(pR, 32)))

                success := staticcall(sub(gas(), 2000), 6, mIn, 128, pR, 64)

                if iszero(success) {
                    mstore(0, 0)
                    return(0,0x20)
                }

            }

            function g1_mulAccC(pR, x, y, s) {
                let success
                let mIn := mload(0x40)
                mstore(mIn, x)
                mstore(add(mIn,32), y)
                mstore(add(mIn,64), s)

                success := staticcall(sub(gas(), 2000), 7, mIn, 96, mIn, 64)

                if iszero(success) {
                    mstore(0, 0)
                    return(0,0x20)
                }

                mstore(add(mIn,64), mload(pR))
                mstore(add(mIn,96), mload(add(pR, 32)))

                success := staticcall(sub(gas(), 2000), 6, mIn, 128, pR, 64)

                if iszero(success) {
                    mstore(0, 0)
                    return(0,0x20)
                }
            }

            function g1_mulSetC(pR, x, y, s) {
                let success
                let mIn := mload(0x40)
                mstore(mIn, x)
                mstore(add(mIn,32), y)
                mstore(add(mIn,64), s)

                success := staticcall(sub(gas(), 2000), 7, mIn, 96, pR, 64)

                if iszero(success) {
                    mstore(0, 0)
                    return(0,0x20)
                }
            }

            function g1_mulSet(pR, pP, s) {
                g1_mulSetC(pR, mload(pP), mload(add(pP, 32)), s)
            }

            function calculateD(pMem) {
                let _pD:= add(pMem, pD)
                let gamma := mload(add(pMem, pGamma))
                let mIn := mload(0x40)
                mstore(0x40, add(mIn, 256)) // d1, d2, d3 & d4 (4*64 bytes)

                g1_setC(_pD, Qcx, Qcy)
                g1_mulAccC(_pD, Qmx, Qmy, mulmod(calldataload(pEval_a), calldataload(pEval_b), q))
                g1_mulAccC(_pD, Qlx, Qly, calldataload(pEval_a))
                g1_mulAccC(_pD, Qrx, Qry, calldataload(pEval_b))
                g1_mulAccC(_pD, Qox, Qoy, calldataload(pEval_c))

                let betaxi := mload(add(pMem, pBetaXi))
                let val1 := addmod(
                    addmod(calldataload(pEval_a), betaxi, q),
                    gamma, q)

                let val2 := addmod(
                    addmod(
                        calldataload(pEval_b),
                        mulmod(betaxi, k1, q),
                        q), gamma, q)

                let val3 := addmod(
                    addmod(
                        calldataload(pEval_c),
                        mulmod(betaxi, k2, q),
                        q), gamma, q)

                let d2a := mulmod(
                    mulmod(mulmod(val1, val2, q), val3, q),
                    mload(add(pMem, pAlpha)),
                    q
                )

                let d2b := mulmod(
                    mload(add(pMem, pEval_l1)),
                    mload(add(pMem, pAlpha2)),
                    q
                )

                // We'll use mIn to save d2
                g1_calldataSet(add(mIn, 192), pZ)
                g1_mulSet(
                    mIn,
                    add(mIn, 192),
                    addmod(addmod(d2a, d2b, q), mload(add(pMem, pU)), q))

                val1 := addmod(
                    addmod(
                        calldataload(pEval_a),
                        mulmod(mload(add(pMem, pBeta)), calldataload(pEval_s1), q),
                        q), gamma, q)

                val2 := addmod(
                    addmod(
                        calldataload(pEval_b),
                        mulmod(mload(add(pMem, pBeta)), calldataload(pEval_s2), q),
                        q), gamma, q)

                val3 := mulmod(
                    mulmod(mload(add(pMem, pAlpha)), mload(add(pMem, pBeta)), q),
                    calldataload(pEval_zw), q)


                // We'll use mIn + 64 to save d3
                g1_mulSetC(
                    add(mIn, 64),
                    S3x,
                    S3y,
                    mulmod(mulmod(val1, val2, q), val3, q))

                // We'll use mIn + 128 to save d4
                g1_calldataSet(add(mIn, 128), pT1)

                g1_mulAccC(add(mIn, 128), calldataload(pT2), calldataload(add(pT2, 32)), mload(add(pMem, pXin)))
                let xin2 := mulmod(mload(add(pMem, pXin)), mload(add(pMem, pXin)), q)
                g1_mulAccC(add(mIn, 128), calldataload(pT3), calldataload(add(pT3, 32)) , xin2)

                g1_mulSetC(add(mIn, 128), mload(add(mIn, 128)), mload(add(mIn, 160)), mload(add(pMem, pZh)))

                mstore(add(add(mIn, 64), 32), mod(sub(qf, mload(add(add(mIn, 64), 32))), qf))
                mstore(add(mIn, 160), mod(sub(qf, mload(add(mIn, 160))), qf))
                g1_acc(_pD, mIn)
                g1_acc(_pD, add(mIn, 64))
                g1_acc(_pD, add(mIn, 128))
            }

            function calculateF(pMem) {
                let p := add(pMem, pF)

                g1_set(p, add(pMem, pD))
                g1_mulAccC(p, calldataload(pA), calldataload(add(pA, 32)), mload(add(pMem, pV1)))
                g1_mulAccC(p, calldataload(pB), calldataload(add(pB, 32)), mload(add(pMem, pV2)))
                g1_mulAccC(p, calldataload(pC), calldataload(add(pC, 32)), mload(add(pMem, pV3)))
                g1_mulAccC(p, S1x, S1y, mload(add(pMem, pV4)))
                g1_mulAccC(p, S2x, S2y, mload(add(pMem, pV5)))
            }

            function calculateE(pMem) {
                let s := mod(sub(q, mload(add(pMem, pEval_r0))), q)

                s := addmod(s, mulmod(calldataload(pEval_a),  mload(add(pMem, pV1)), q), q)
                s := addmod(s, mulmod(calldataload(pEval_b),  mload(add(pMem, pV2)), q), q)
                s := addmod(s, mulmod(calldataload(pEval_c),  mload(add(pMem, pV3)), q), q)
                s := addmod(s, mulmod(calldataload(pEval_s1), mload(add(pMem, pV4)), q), q)
                s := addmod(s, mulmod(calldataload(pEval_s2), mload(add(pMem, pV5)), q), q)
                s := addmod(s, mulmod(calldataload(pEval_zw), mload(add(pMem, pU)),  q), q)

                g1_mulSetC(add(pMem, pE), G1x, G1y, s)
            }

            function checkPairing(pMem) -> isOk {
                let mIn := mload(0x40)
                mstore(0x40, add(mIn, 576)) // [0..383] = pairing data, [384..447] = pWxi, [448..512] = pWxiw

                let _pWxi := add(mIn, 384)
                let _pWxiw := add(mIn, 448)
                let _aux := add(mIn, 512)

                g1_calldataSet(_pWxi, pWxi)
                g1_calldataSet(_pWxiw, pWxiw)

                // A1
                g1_mulSet(mIn, _pWxiw, mload(add(pMem, pU)))
                g1_acc(mIn, _pWxi)
                mstore(add(mIn, 32), mod(sub(qf, mload(add(mIn, 32))), qf))

                // [X]_2
                mstore(add(mIn,64), X2x2)
                mstore(add(mIn,96), X2x1)
                mstore(add(mIn,128), X2y2)
                mstore(add(mIn,160), X2y1)

                // B1
                g1_mulSet(add(mIn, 192), _pWxi, mload(add(pMem, pXi)))

                let s := mulmod(mload(add(pMem, pU)), mload(add(pMem, pXi)), q)
                s := mulmod(s, w1, q)
                g1_mulSet(_aux, _pWxiw, s)
                g1_acc(add(mIn, 192), _aux)
                g1_acc(add(mIn, 192), add(pMem, pF))
                mstore(add(pMem, add(pE, 32)), mod(sub(qf, mload(add(pMem, add(pE, 32)))), qf))
                g1_acc(add(mIn, 192), add(pMem, pE))

                // [1]_2
                mstore(add(mIn,256), G2x2)
                mstore(add(mIn,288), G2x1)
                mstore(add(mIn,320), G2y2)
                mstore(add(mIn,352), G2y1)

                let success := staticcall(sub(gas(), 2000), 8, mIn, 384, mIn, 0x20)

                isOk := and(success, mload(mIn))
            }

            let pMem := mload(0x40)
            mstore(0x40, add(pMem, lastMem))

            checkInput()
            calculateChallenges(pMem, _pubSignals)
            calculateLagrange(pMem)
            calculatePI(pMem, _pubSignals)
            calculateR0(pMem)
            calculateD(pMem)
            calculateF(pMem)
            calculateE(pMem)
            let isValid := checkPairing(pMem)

            mstore(0x40, sub(pMem, lastMem))
            mstore(0, isValid)
            return(0,0x20)
        }

    }
}
```

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/341103fe7f7f411e77319c66773386efc467b028_2_690x401.jpeg)image1920×1116 112 KB](https://ethresear.ch/uploads/default/341103fe7f7f411e77319c66773386efc467b028)

The corresponding on chain verification contract solidity code is:

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Verifier.sol";

contract PrivacyPreservingContract {
    Verifier public verifier;

    struct ShieldedOrder {
        uint phi;  // order type
        uint x;    // target token address
        uint d;    // domination
        uint h;    // hash
    }

    ShieldedOrder[] public orders;

    constructor(address _verifier) {
        verifier = Verifier(_verifier);
    }

    function shieldOrder(
        uint[2] calldata a,
        uint[2][2] calldata b,
        uint[2] calldata c,
        uint[4] calldata input
    ) public {
        // Verification of zk-SNARK proofs
        require(verifier.verifyTx(a, b, c, input), "Invalid proof");

        // Create a new masked order
        ShieldedOrder memory newOrder = ShieldedOrder({
            phi: input[0],
            x: input[1],
            d: input[2],
            h: input[3],
        });

        // Store the new order in a state variable
        orders.push(newOrder);
    }

    // Function to retrieve the order quantity
    function getOrdersCount() public view returns (uint) {
        return orders.length;
    }
}
```

The above code is only used as an example program, and other operations such as invalid nullifiers need to be generated during the actual production process.

## Computation Optimization

Assuming we want to execute the heavy AMM logic off-chain, we only need to perform computational verification operations on the chain.

The following is a simple AMM logic circuit (as an example only, the calculation logic of the actual protocol is much more complex)

circom code:

```auto
template AMM() {
    signal input reserveA;
    signal input reserveB;
    signal input swapAmountA;

    signal output receivedAmountB;
    signal output newReserveA;
    signal output newReserveB;

    // x * y = k
    // newReserveA = reserveA + swapAmountA
    // newReserveA * newReserveB = reserveA * reserveB
    // newReserveB
    newReserveA <== reserveA + swapAmountA;
    newReserveB <== (reserveA * reserveB) / newReserveA;

    // compute the amount of tokenB
    receivedAmountB <== reserveB - newReserveB;

		// more computation operations...
}

component main = AMM();
```

Similarly, it is necessary to use the `circom+snarkjs` toolchain to generate proof and export it to verifier.sol.

The solidity code for the on chain check contract is as follows:

solidity code:

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Verifier.sol";

contract AMMWithSnarks {
    Verifier public verifier;

    constructor(address _verifier) {
        verifier = Verifier(_verifier);
    }

    function swap(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[2] memory input,
        uint256 amountA
    ) public returns (uint256) {
        // Verification of zk-SNARKs proofs
        require(verifier.verifyTx(a, b, c, input), "Invalid proof");

        // The actual exchange logic is omitted, as the verification is done through zk-SNARKs

        // Return the amount of tokens obtained after the exchange, which requires calculation in the actual implementation
        return amountA * 2; // Here is just an example of the return value
    }

    // other function，such as addLiquidity, removeLiquidity etc.
}
```

## Anti-MEV attacks

After privacy modification of protocol contracts, MEV attacks often fail to be achieved. Please refer to examples of privacy modification.

---

**Mirror** (2023-10-29):

I have obtained permission and will merge the posts and add new content.

---

**Po** (2023-10-30):

Thanks for your explanation. In this example, given the `amount of tokens obtained after the exchange`,  I think actually we could reverse calculate the  private `amount` and `volume` by the AMM algorithm. Then, the expected privacy is not protected. Hope to get your defence.

---

**Mirror** (2023-11-01):

Yes, exactly. But we are focusing on demonstrating zksnark’s ability to do computational optimization in the AMM example, so we are not considering privacy-preserving properties. Forgive us for the fact that the logic of AMM in our example circuit is not complex, but in reality it should be quite complex, and we want to execute it off-chain, and on-chain only validate a clean proof, so we do not intend to additionally demonstrate zksnark privacy-preserving capabilities here.![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

