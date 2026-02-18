---
source: ethresearch
topic_id: 13139
title: Verify ed25519 signatures cheaply on Eth using ZK-Snarks
author: garvitgoel
date: "2022-07-25"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/verify-ed25519-signatures-cheaply-on-eth-using-zk-snarks/13139
views: 8174
likes: 20
posts_count: 14
---

# Verify ed25519 signatures cheaply on Eth using ZK-Snarks

*Prepared by : Garvit Goel, Rahul Ghangas, Jinank Jain*

In this article, we will discuss how you can verify Ed25519 signatures on Ethereum today in a very gas-efficient way, without the use of any pre-compiles such as the proposed EIP665. We will use the same principles as used by many zk-rollups. We have already shipped the code for this, albeit not yet audited. Let’s get to it.

For dApps that want to verify Ed25519 signatures on Ethereum, rather than verifying the signature(s) directly on Ethereum, (and performing the curve operations inside a solidity smart contract), one can construct a zk-proof of signature validity and verify the proof on-chain instead.

Gas cost for verification of a single Ed25519 signature is about ~500K gas (when the Ed25519 curve is implemented directly in Solidity). On the other hand, the gas cost for verifying a zk-snark on-chain is about ~300k gas. These gas savings become significant when you want to verify a large number of signatures in one batch, then you can just create a single ZK-proof for the entire batch.

At Electron Labs, we have built a circom-based library that allows you to generate a zk-snark proof for a batch of Ed25519 signatures.

You can check out the details of our mathematical approach [here](https://docs.electronlabs.org/reference/overview). You can even test proof generation today using the APIs given on the previous link.

Check out the complete code base [here](https://github.com/Electron-Labs/ed25519-circom)

### The Performance of a Single Ed25519 is as below:

All metrics were measured on a 16-core 3.0GHz, 32G RAM machine (AWS c5a.4xlarge instance).

|  | Single ED25519 Signature |
| --- | --- |
| Constraints | 2,564,061 |
| Circuit compilation | 72s |
| Witness generation | 6s |
| Trusted setup phase 2 key generation | 841s |
| Trusted setup phase 2 contribution | 1040s |
| Proving key size | 1.6G |
| Proving time (rapidsnark) | 6s |
| Proof verification Cost | ~300K gas |

Furthermore, for batching we support:

1. Max batch size supported = 99 signatures
2. Proof generation time for a batch of 99 signatures = ~16 minutes.

While these metrics are good for a PoC, we need to do a lot better. Hence, as next steps, we are planning to integrate recursive snarks. This will increase the max batch size and reduce proof generation time by multiple orders of magnitude.

### Use Cases:

We believe one of the best use cases for this tech is extending light client bridges to Ethereum. This includes Polygon Avail, IBC and Rainbow Bridge. One could also build zk-rollups that use Ed25519 for user accounts.

### Ending Note:

We would love to work with teams that want to use this tech. We are also looking for research groups who are working on recursive snark technology to help us scale our tech.

## Replies

**oberstet** (2022-11-12):

Hi there,

author of EIP665 here, I just stumbled across this post now: this is really a cool approach, great work! Love it. Thanks for sharing!

FWIW, the EIP665 never went anywhere even though I’ve implemented the proposal as a precompile in different EVM implementations. Reasons were worries about precompile security / added complexity, and by pointing to eWASM which would then presumably render the whole “new precompiles suck” angle pointless, as one could then efficiently implement those directly in user contracts. I agree in principle with the latter. However, years later, eWASM has yet to arrive;)

> We would love to work with teams that want to use this tech.

Please let me expand a bit and then explain why I’m still interested in this stuff.

I am doing quite a bit of OSS work, e.g. I am original author of https://wamp-proto.org/

This is a modern and unique application messaging protocol that can run natively over WebSocket and provides both PubSub and RPC (in a routed fashion) in one protocol (a network protocol that is).

There are many implementations, one of which is another project of mine:



      [github.com](https://github.com/crossbario/crossbar)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/3/e/3ec7dd22d16c6b67877318e4c261ea5503d81efb_2_690x344.png)



###



Crossbar.io - WAMP application router










You’ll find a couple of client library implementations under that some GitHub org.

Now, WAMP is using Ed25519 since ages for one of it’s authentication methods (“WAMP-cryptosign”).

This is where my original interest came from: being able to use such “WAMP native” signatures.

Another, independent motivation was: make application services exposed via WAMP in a payable fashion, e.g. every 1000 calls to this procedure, or every 1h of events on some topic cost so and so much.

We’ve implemented this using off-chain payment channels implemented in Crossbar:

[sorry, I can only post 2 links per post]

One problem with that still is:

- 2 signature schemes (Eth and Ed25519) are used in the system
- high gas costs for payment channel open/close

Actually, sorry for the amount of stuff, but I’d like to give you the “complete picture”.

After all of above “experiments”, we now want to reuse the end-to-end encryption stuff we’ve added to WAMP during above service payment experiments, and first want to expand single-operator WAMP to a federated WAMP network of router nodes operated by different parties. And use Eth L2.

If we could also reuse Ed25519, and if we could improve meta-data privacy at the WAMP network level using ZK-Snarks, that sounds fantastic !!!

So yes, if you are interested in discussing this stuff, possibly working together, pls let me know, I’m interested/curious =)

Cheers,

/Tobias

---

**garvitgoel** (2022-11-12):

Hi [@oberstet](/u/oberstet)

Many thanks for reaching out! Would love to connect and discuss more. Have DM’ed you ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**nemothenoone** (2022-12-10):

A more efficient [Placeholder proof system](https://crypto3.nil.foundation/papers/placeholder.pdf)-based trusted setup-free (i.e. done with PLONK-ish artithmetization over LPC commitment scheme) Ed25519 signature scheme proof generation and its in-EVM verification was done back in 2021 by [=nil; Foundation](https://twitter.com/nil_foundation) as a part of [Solana’s Light-Client Proof in-EVM verification](https://github.com/NilFoundation/solana-state-proof) project with a test stand available in here: https://verify.solana.nil.foundation.

### Performance

As shown on a test stand, it takes about 1,5 hour to generate Solana’s state proof with AMD EPYC 7542 and about 13Gb of RAM. Such a proof contains something like 2k Ed25519 signatures and it costs about ~2,5m gas to verify all that with no trusted setup required.

---

**oberstet** (2022-12-15):

Interesting!

So I’ve been looking around in the “State proof generator”



      [github.com](https://github.com/NilFoundation/solana-state-proof/blob/dadff9b5d085f0adb5b9148929dd75f930b5cec3/bin/state-proof-gen-mt/src/main.cpp#L269)





####



```cpp


1. for (const boost::json::value &deep_arr: val.as_array()) {
2. ret[i].emplace_back(boost::json::value_to>(deep_arr));
3. }
4. }
5. return ret;
6. }(o.at("votes"))
7. };
8. }
9.
10. template
11. void proof(const state_type &state) {
12. auto start = std::chrono::high_resolution_clock::now();
13.
14. using curve_type = nil::crypto3::algebra::curves::pallas;
15. using ed25519_type = nil::crypto3::algebra::curves::ed25519;
16. using BlueprintFieldType = typename curve_type::base_field_type;
17. constexpr std::size_t WitnessColumns = 9;
18. constexpr std::size_t PublicInputColumns = 1;
19. constexpr std::size_t ConstantColumns = 1;
20. constexpr std::size_t SelectorColumns = 26;
21. using ArithmetizationParams =


```










However, I can’t find the “In-EVM state proof verificator” mentioned here [GitHub - NilFoundation/solana-state-proof: In-EVM Solana Light Client State Verification](https://github.com/NilFoundation/solana-state-proof#in-evm-solana-light-client-state-verification)

Also, is there a rendered version available for



      [github.com](https://github.com/NilFoundation/solana-state-proof/blob/dadff9b5d085f0adb5b9148929dd75f930b5cec3/docs/design/chapters/verifier.tex)





####



```tex
\chapter{In-EVM State Proof Verifier}

This introduces a description for Solana's 'Light-Client' state proof in-EVM
verifier.

Crucial components which define this part design are:
\begin{enumerate}
    \item Verification architecture description.
    \item Verification logic API reference.
    \item Input data structures description.
\end{enumerate}

\input{chapters/verifier/architecture}
\input{chapters/verifier/api}
\input{chapters/verifier/input}
```










?

---

**maanav** (2023-11-07):

Hi [@garvitgoel](/u/garvitgoel), I noticed you mentioned that the gas cost for verification of a single Ed25519 signature is about ~500K gas. I wanted to ask which Solidity implementation you used here to benchmark Ed25519 signature verification, I haven’t been able to find any implementation elsewhere.

---

**zilayo** (2023-12-07):

there’s a few implementations on github such as https://github.com/rdubois-crypto/FreshCryptoLib/blob/e2830cb5d7b0f6ae35b5800287c0f5c92388070b/solidity/src/FCL_eddsa.sol but i am still to find one in the wild.

Really cool work!

It seems like there has been a renewed interest in edDSA on ethereum recently so will be interesting to see future use cases

---

**sasicgroup** (2023-12-08):

I like the idea of saving gas but how fast can it be pushed into the mainstream? cant it be done in a form of account abstration standalone wallet or ontop of intmax if mainstream(into core eth) fails?

---

**Johnchuks1** (2023-12-09):

I noticed you mentioned that the gas cost for verification of a single Ed25519 signature is about ~500K gas. I wanted to ask which Solidity implementation you used here to benchmark Ed25519 signature verification, I haven’t been able to find any implementation elsewhere.

---

**garvitgoel** (2023-12-09):

Hi [@Johnchuks1](/u/johnchuks1) thank for this. We got this number from the work by Rainbow bridge, who had created an implementation of Ed25519 in solidity. Since then, I believe Rainbow has released more gas efficient implementations, which you should be able to find on their Github

---

**2R1Stake** (2023-12-11):

Do you think it could be generalize to build light client bridge (i.e trust minimised bridge) for a pure DA layer like Celestia or Avail with a (ZK)rollups on top ?

---

**garvitgoel** (2023-12-12):

yes it surely can be. we are also coming up with faster and better proving tech soon that will make it even easier to support such applications.

---

**garvitgoel** (2024-01-01):

Seeing the recent increase in interest in this topic, we have started a telegram group for this. Folks can join here - [Telegram: Join Group Chat](https://t.me/+YkeE6WcFHrRiMzE1)

---

**danylonepritvoreniy** (2024-12-01):

How can integrating recursive zk-SNARKs improve the efficiency and scalability of verifying Ed25519 signatures on Ethereum, particularly for applications like light client bridges and zk-rollups?

