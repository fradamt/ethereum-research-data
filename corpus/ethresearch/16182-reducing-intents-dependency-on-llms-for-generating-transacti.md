---
source: ethresearch
topic_id: 16182
title: Reducing Intents' dependency on LLMs for generating Transaction Object
author: Arch0125
date: "2023-07-25"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/reducing-intents-dependency-on-llms-for-generating-transaction-object/16182
views: 2709
likes: 9
posts_count: 7
---

# Reducing Intents' dependency on LLMs for generating Transaction Object

TLDR; This proposal intends to make a resolver for decoding intents with higher accuracy, also reducing the dependency over LLM for building the transaction object from the intent.

The problem arises with such approach is inaccuracy of calldata/value/amount generated for the intended transaction might not be correct, causing multiple failed transactions which could be prevented by transaction simulation using Alchemy/Tenderly but it seems like a hit and trial method for decoding intents.

## Proposed Method

---

We will take an example intent **“Send 10 USDC to 0x118aeFa610ceb7C42C73d83dfC3D8C54124A4946”**

This intent will be parsed by the LLM and will return an array of objects based on the number of transactions required to reach the final state as intended.

For the above case it will return :

```auto
[{
    "contractAddress": "0x742DfA5Aa70a8212857966D491D67B09Ce7D6ec7",
    "functionId": "0x01",
    "amount": "0xf",
    "toAddress": "0x118aeFa610ceb7C42C73d83dfC3D8C54124A4946",
    "value": "0x"
}]
```

**The response object contains the following :**

- contractAddress : If the transaction needs to interact with a contract
- functionId : A set of predefined hexes for functions defined below
- amount : Amount of ERC20 tokens if required by the transaction
- toAddress : EOA address or any other address that may be required by a contract call or while sending native tokens
- value : Amount of native token to be send along with the transaction if any

**The following hexes will be used for decoding :**

- SEND_NATIVE - 0x00
- SEND_ERC20 - 0x01
- SWAP_EXACT_TOKENS_FOR_TOKENS - 0x02
- SWAP_TOKENS_FOR_EXACT_TOKENS - 0x03
- SWAP_EXACT_ETH_FOR_TOKENS - 0x04
- SWAP_ETH_FOR_EXACT_TOKENS - 0x05
- WRAP - 0x06
- UNWRAP - 0x07

**Ideal Case :**

The response of the LLM is passed on to the resolver which checks the wallet balance, if enough tokens are present for the transaction, it is built and send back to the user for signing the userOp and the gas is sponsored by the Paymaster

**Now arises two other edge-cases :**

- If the token required for the transaction is not present in the wallet : In this case the resolver will append one or more of these functions (0x02, 0x03, 0x04, 0x05) before the intended one to swap out the required token and then build batched transactions.
- If the transaction is no way possible through any routes : The intent is rejected and dropped by the resolver, returning the user a message about the reverted intent

## How Nodes are going to execute intents

---

[![Untitled Diagram.drawio](https://ethresear.ch/uploads/default/original/2X/3/3ef3e1abfedbaa7a3b75cc6a259304e22eeb45d1.png)Untitled Diagram.drawio662×449 42.9 KB](https://ethresear.ch/uploads/default/3ef3e1abfedbaa7a3b75cc6a259304e22eeb45d1)

### Intent flow

- User provides the intent in natural language
- Intent is passed through the resolver and intent object is calculated by the LLM and the response is in the format :

```auto
[{
    "contractAddress": "...",
    "functionId": "...",
    "amount": "...",
    "toAddress": "...",
    "value": "..."
}]
```

- The intent object is passed to the intent mempool, from where the intents are picked up by the intent builders, they encode the intent transaction routes into a 105 bytes long string as defined below and verified by calling the contract function validateIntentOp
- The intent builders auction for the most efficient route within a defined deadline, once a single intent route is finalised, the userOp is built and then sent back to the user for signing the userOp and the gas is sponsored by the Paymaster
- Total encoded intent string is 105 bytes long

1 Byte : Function Identifier
- Next 20 bytes : To address - used to transfer tokens natively or via contract
- Next 20 bytes : Contract Address to interact with
- Next 32 bytes : Value of Native token
- Next 32 bytes : ERC20 Amount

For example “Send 123ETH to 56AeF9d1da974d654D5719E81b365205779161aF”

| Function (1 byte) | To Address (20 bytes) | Contract Address (20 bytes) | Value(32 bytes) | Amount (32 bytes) |
| --- | --- | --- | --- | --- |
| 0x00 | 56AeF9d1da974d654D5719E81b365205779161aF | 0000000000000000000000000000000000000000 | 000000000000000000000000000000000000000000000000000000000000007b | 0000000000000000000000000000000000000000000000000000000000000000 |

- So for an intent “Send 123ETH to 56AeF9d1da974d654D5719E81b365205779161aF” will be encoded to 0x0056AeF9d1da974d654D5719E81b365205779161aF000000000000000000000000000000000000000000000000000000000000007b0000000000000000000000000000000000000000000000000000000000000000

The above proposal of decoding intents works with native token transfer, erc20 token transfers, swap and wrap functionalities, it will be extended to support larger range of transactions and set-up resolvers dedicated for a specific transaction types rather than having a generalised resolver for all.

## Replies

**Arch0125** (2023-07-25):

Tweet link containing demo transaction using above intent architecture : https://twitter.com/Arch_0125/status/1682821056296304641?s=20

---

**sk1122** (2023-07-25):

This is very awesome!

I have 2 points

1. We can reduce LLM dependency if we have a structured way to represent intents, intent’s main goal is to enable users to define what state they want after their transaction, so if we enable users to directly generate intents in a structured format, then we will not need LLMs to convert them.
2. Solvers can have an extra step to validate if they can actually solve those intent or not, this will enable the decentralized network of intents to have more types of solvers, like swap, bridge, loan, social solvers and more

Also would like to point out, Intents should have various representation format, it can be UI, Natural language, Form etc

---

**nlok5923** (2023-07-26):

Amazing proposal [@Arch0125](/u/arch0125)

Few pointers i had

- The current LLM systems work with the data they are already trained upon. In Web3 ecosystem we have almost most of the actions depends on the real-time values (ex: liquidity pools state, NFT auctions prices, network congestion and many more) Have you planned to the integration of some real time data scrappers ?
- I think another angle with intents could be is it to make things optimal. ex: The user can just say i want to stake 100 USDC against max APY.  And its at the solver’s end to figure out the route for making this happen. Do you have any thoughts on how it could be done ?
- Additionally, I think the architecture you are proposing is quite heavily relying on centralized LLMs (where would LLM reside client end ? middleware ?). I think what we could do is Once the user proposed an intent we can directly broadcast the intent to intent mempool and from their independents solver can work on intents to find the optimal routes. Lastly, the route corresponding to the max efficiency could be chosen and proposed to user for signing.

---

**GraphicalDot** (2023-07-26):

In my opinion, making generic intents at this point in time is nearly impossible as the field is still very new. We should start with domain-specific intents and then generalize intents DSL over all the domains.

I agree with [@nlok5923](/u/nlok5923) that the decoding of Intents must be done at the node level, but here is the problem with that approach - Solvers will be domain-specific, i.e., solvers who are actually solving DeFi intents or solvers who are only dealing with intents for social networks (Follow all those people who are NFT Degens ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) ). If the LLM’s are hosted on the solvers’ end, then they have to decode all the intents and then filter out the domain-specific ones - wasting a lot of computational resources and time.

IMHO, the intent decoding should happen at the Wallet level and then be sent to the Intent mempool so that solvers wouldn’t have to decode all the intents and could just filter out the ones that they are interested in.

Alternatively, there could be another layer in between that can provide this functionality along with suggesting intents to the user based on their Tx history or profile. We shouldn’t expect users to be tech-savvy enough to express their intents for their interests.

---

**vestor** (2023-07-26):

Great work Archisman!!!

I feel in future also we can not remove LLM altogether simply for the sake of letting users write their intentions in plain simple words without worrying for the order. Use memorization, caching and pipeline to check where it’s necessary and where it’s not to make the process more efficient. Writing layer by layer, we might someday be able to cover almost everything to be done on blockchain as a standard to map upon. Using pipelines to convert language prompts into a standardized responses that can be used directly as intents by the nodes.

Nodes can be optimised or trained based on the type of requests they are getting and rewarding based sharing of the data needed for the resolver to be robust. This might make us more resistant to false intents and unresolvable intents.

LLMs also helps building the transactions faster than nodes would be able to, currently they can be well trained to perform a lot of actions because blockchain data set is not huge compared to traditional finance. Also i believe even if we reduce the dependency of LLM for building the transactions and put it on intent pool the nodes will be using these same LLM/Algorithms to build the transactions fast being an incentivised model.

---

**Arch0125** (2023-07-26):

I can address to your pointers, getting on to the first one

- Yeah i agree with the fact the current LLMs are trained on previous data and may not produce correct transaction objects, also in terms of defi applications we need real time data, keeping those constraints in mind im also not inclined towards llm dependency over building transactions rather create an abstract of what the user is trying to do in a form that can be easily parsed by a resolver to form the transaction using realtime data, if we take the intent mentioned above, the llm would provide an abstract of what user intents to achieve rather than giving out exact tx values. This abstract object would then be parsed by another resolving node and based on the functionId it would gather any required real time information (lets say uniswap pool details) which is not influenced by any llm, hence building accurate user operation. The nodes indicated in the illustration would be reaponsible for carrying out the non-llm decoding of intents.

Note : The first resolver using LLM, its output could be like a regex for nodes to build transactions on.

Touching on the second and third points regarding the most efficient routes for intent, i think taking the approach similar to cowswap solver bots would work out pretty well and choosing the most efficient route would be chosen in the form of an auction where the builder is awarded with token(like in cowswap) this could also prevent the bad actors to a certain extent from purposely proposing bad routes for their own benefit.

Going by your example “maximising apy” could be solved by the method i mentioned earlier by the nodes fetching real time data (intent specific solvers maybe ? As mentioned by [@GraphicalDot](/u/graphicaldot) ) and using them to finding the correct protocols to execute the transaction.

Lastly coming to where the resolver would be hosted, i see three options

- Hosted on a central server with sole purpose of handling all kinda of intents and converting them to the abstract object, seems like too much computation also risks of ddos attacks
- hosted by each solver node ie, intent mempool would receive the original intent and they would decide the intent based on their preference, extending intent specific solvers.
- intent → abstract object is done in the wallet itself and its sent to the intentmempool, in that case the model would be more trained specific to that user transactions thus more accurate (i highly vouch for this but i dont think it would be possible to do this right now except for metamask snaps for a good alternative for the future)

