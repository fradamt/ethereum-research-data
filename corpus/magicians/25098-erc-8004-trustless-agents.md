---
source: magicians
topic_id: 25098
title: "ERC-8004: Trustless Agents"
author: davidecrapis.eth
date: "2025-08-14"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098
views: 10301
likes: 204
posts_count: 102
---

# ERC-8004: Trustless Agents

This standard extends the [Agent‑to‑Agent (A2A) protocol](https://a2a-protocol.org/latest/specification/) with a trust layer that allows participants to **discover, choose, and interact with agents across organizational boundaries** without pre‑existing trust.

It introduces three **lightweight, on‑chain registries**—Identity, Reputation, and Validation—and leaves application‑specific logic to off‑chain components.

https://github.com/ethereum/ERCs/pull/1170


      ![image](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-8004)





###



Discover agents and establish trust through reputation and validation










As this ERC undergoes public discussion, we will work closely with the Linux Foundation and A2A ecosystem stakeholders to refine and improve the specifications of this extension.

*We acknowledge Dayan Brunie (Consensys), Wilson Chen (TensorBlock), Sumeet Chougule (Nethermind), Jordan Ellis (Google), Nicola Greco (Deepcrypto), Austin Griffith (Ethereum Foundation), David Minarsch (Olas), Barnabé Monnot (Ethereum Foundation), Regan Peng (PIN AI), David Shi (Operator Labs), Pratyush Ranjan Tiwari (Freysa / Eternis), Nima Vaziri (Eigen Labs) for their technical feedback and contributions.*

## Replies

**leonprou** (2025-08-17):

Hey [@davidecrapis.eth](/u/davidecrapis.eth).

Great initiative! We are building a trusless layer for agent collaboration, and seek to be A2A compatible as well. Looking forward to learn how to addop it and happy to chat. Here’s out github repo - https://github.com/ensemble-codes/ensemble-framework

---

**spengrah** (2025-08-18):

If I’m understanding correctly, this standard prioritizes offchain reads (via event emission) over onchain reads (eg by other smart contracts). If my understanding is correct, I think this is a big miss. A huge amount of the value that agents will create will involve permissioned onchain actions, and so creating primitives for onchain composability would be highly valuable.

For example, I don’t see a way in the current standard for an arbitrary smart contract to read the result of a validation response. But if that were required in the standard, then contracts could implement other logic conditioned on various responses. One big benefit would be decoupling validation from enforcement, ie validators would only need to implement validation logic, leaving other protocols to modularly innovate on slashing or other enforcement logic.

Generally speaking, if we’re going to anchor something onchain (which we should!), we should also ensure that onchain actors can utilize whatever we’re anchoring. I appreciate that including *everything* onchain is likely not cost-effective, but ensuring there is a way for contracts to read hashes, digests, identifiers, integers etc is valuable.

---

**felixnorden** (2025-08-19):

I think you have some valid points to make here. I’m also thinking that the Reputation registry could use functions for multiple Reputation scores from one or multiple providers, which could act as a snapshot/proof of cumulative perceived reputation for an agent and provider.

Individual attestations are effective when evaluating the quality of work by an agent. However, for future work, having an aggregate metric to quantify who to work with or avoid becomes more important.

This would mean that the Reputation registry becomes a single point of entry for both on-chain and off-chain consumers, and we could leverage multiple providers’ scores of an agent to reduce the risk of biases, collusion, etc.

---

**sbacha** (2025-08-20):

Reputons are a standard defined: [RFC 7071 - A Media Type for Reputation Interchange](https://datatracker.ietf.org/doc/html/rfc7071)

Some attempts at using this for enriching token lists for curating against scam tokens were attempted.

Reputation here i think is less in “credibility” and more in “SLA/Uptime” kind of metric.

---

**mlegls** (2025-08-21):

Agreed. I’ve also been working on a [set of smart contracts](https://github.com/CoopHive/alkahest-mocks/tree/main) and [interfaces](https://github.com/CoopHive/alkahest-mocks/blob/main/src/IArbiter.sol) for peer to peer [escrowed](https://github.com/CoopHive/alkahest-mocks/blob/main/src/obligations/ERC20EscrowObligation.sol) [exchange](https://github.com/CoopHive/alkahest-rs/blob/main/tests/erc20.rs) with [pluggable](https://github.com/CoopHive/alkahest-mocks/blob/main/src/arbiters/TrustedOracleArbiter.sol) [validation](https://github.com/CoopHive/alkahest-mocks/blob/main/src/arbiters/deprecated/TrustedPartyArbiter.sol) [mechanisms](https://github.com/CoopHive/alkahest-mocks/blob/main/src/arbiters/logical/AnyArbiter.sol), where the validation mechanisms especially have a lot of intersection with this ERC, and our compromise between gas cost and on-chain usability was to have the interface for arbitration as a function `checkObligation(obligation, demand) external view returns bool`, to be called as needed, which can often be implemented ephemerally without using on-chain storage. Of course, this assumes that the primary use of validation is as a binary decision valid/invalid. We also chose to rely pretty heavily on [EAS](https://attest.org/) for on-chain attestations, e.g. for those representing obligations (in the context of the ERC, a task an agent does), or comments on obligations that should persist on-chain.

I think it makes sense to keep the core ERC small and cheap to implement though, perhaps with standard interfaces for on-chain uses related to it as separate extension ERCs, or as optional interfaces. It’s easy to add functionality to a contract implementing a minimal spec, and much harder to subtract from a bloated spec.

---

**daniel-ospina** (2025-08-21):

Creating a single (aggregate) reputation score is dangerous. We do need a baseline trust criterion but compressing too much into a single metric facilitates monopolistic behaviour.

Slightly less efficient but I’d prefer to go more modular: have a way to index and reference reputation systems. So standards can organically emerge for as many or as few use cases as needed and each agent can choose.

This comes with other complications, so it needs to be thought through but my point is that the agent ID system shouldn’t enforce a single reputation score. That’s just too narrow

---

**comeToThinkOfEth** (2025-08-21):

I have 2 major points to get across:

1. Please elaborate: how would funds be escrowed in this scenario? I would think that we would want to provide maximal flexibility for ways to ensure payment is paid when it’s due:
Possible mechanisms include time locks, predetermined arbitration, and staking by buyer or seller. Do these all fall under ‘crypto‑economics’?
Please explain how these mechanisms fit into the proposed ERC. I don’t understand how the ERC would enable or reference these escrow mechanisms. Probably Maybe this is already addressed and I’m missing the terminology. Could you please include a simple Solidity example (e.g., two agents ordering a pizza) showing how the ERC is used for escrowed payment? (for understandable historical reasons)?
2. I believe that we should not only focus on the infra, but that we need to create an ETH denominated economy in the AI agents space, just like we did with NFTs. I believe the best way forward is to create capable AI agents, who will perform valuable tasks and have them demand payment in ETH. If this takes off, we will get new agents entering the scene having to own ETH to pay other agents. This has the potential of being ETH’s next major, and possibly ultimate, network effect. We should be funding grants and bizdev to get AI agents accepting ETH for tasks.
I know it is not directly pertains to this ERC but it directly relates to the matter. Please spread the idea of you agree.

---

**felixnorden** (2025-08-21):

Yes, I completely agree, I think we’re trying to describe similar things when you say “index and reference” these reputation systems; I’m suggesting that those references can be made available on the registry itself through (agent, provider) pairs as an addition, not a replacement.

The history of independent pieces of work should be standalone, as is described already. However, we can amend the registry to enable multiple providers to provide their aggregate scores for on-chain applications to consume.

E.g., Virtuals, Creatorbid, Base, etc. could each provide their scores for agents, which could be used for comparing overall performance (e.g., SLAs or QoW) and help identify the current best option.

---

**pcarranzav** (2025-08-22):

Great initiative. Some thoughts:

- AFAICT, the use of a well known location for the agent card is optional in the A2A spec, and the spec mentions registries as an alternative. Won’t making it a requirement limit the possibilities of how people might host agents? For instance, I might want to host many agents at different URLs in the same domain. This would be possible in A2A, wouldn’t it? So my suggestion would be to use URLs rather than domains as the way to point to the agent.
- The ERC mentions endpoints but not specific Solidity functions for the different contracts. It would be nice to specify the interface and behavior of the contracts a bit more. e.g. Should registration be free or require some kind of stake deposit? Could the ERC propose a singleton identity registry per chain, to prevent a proliferation of multiple slightly different registries?

---

**azanux** (2025-08-23):

Hi ! ,

I am not sure that it is mentioned in the specification how to handle payment between agents.

The crypto-economics part is related to how to manage the reputation of validators, meaning a way to give incentive to validators to be honest during validation.

But I agree with you that it should be something good to have in the specification as it is an important part, especially that agents will have to pay gas to work together and register collaboration.

otherwise great initiative

---

**KBryan** (2025-08-23):

This is pretty interesting. I’m currently working on a standard for Agent-to-Agent coordination ERC-8001. Would love your input. There are definitely synergies here.

---

**Marco-MetaMask** (2025-08-24):

It seems ERC-8001 is focused on reaching consensus among agents (signing the same attestation), an area orthogonal to and not covered by ERC-8004. Am I understanding this correctly?

---

**Marco-MetaMask** (2025-08-24):

[@felixnorden](/u/felixnorden) [@mlegls](/u/mlegls) and spengrah Yeah, it’s a very important point. The rationale for keeping “Rating” in Reputation completely off-chain and “Response” in Validation off-chain + only in an event parameter (so not accessible on-chain) was:

- [Major] Single feedback or validation won’t be used to decide trust. People will always aggregate entries (including filtering or weighting based on the validator/feedback issuer’s reputation), which is hard to do on-chain anyway.
- [Minor] Gas efficiency / keeping it simple without requiring the Agent Client to sign a transaction for each issued feedback. This can be mitigated by keeping it optional (I like this) or with an off-chain bundler that aggregates multiple feedback and signs transactions on behalf of issuers (which I don’t like because it adds significant overhead).

Anyway, let’s challenge this rationale! So:

- Which data would you save on-chain? Only the Rating and Response integers or other data structures too?
- Where? Registry storage?
- Can you provide use cases where single non-aggregated entries are useful? Or with basic on-chain aggregation? For example, “filtering” is easily implementable on-chain—like skipping all validations or feedback not emitted by whitelisted addresses. So you could calculate an average of filtered ratings, etc.

---

**Marco-MetaMask** (2025-08-24):

(Also answering to [@azanux](/u/azanux)) The protocol doesn’t cover payments. We considered requiring payment proofs for giving feedback, but:

- We didn’t want to couple our problem space (discoverability and trust) to a specific protocol. We preferred to remain unopinionated.
- In some cases, payments will happen off-chain, not happen at all (free service), or be bundled, etc.

That said:

- We encourage inserting proof of payment as an optional attribute in the off-chain schemas.
- We know some groups are working on an A2A payment extension for agents, based on x402. We like this approach and are connecting with them to ensure that their extension and ours (ERC-8004) work perfectly together.

---

**spengrah** (2025-08-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/daniel-ospina/48/15829_2.png) daniel-ospina:

> Creating a single (aggregate) reputation score is dangerous. We do need a baseline trust criterion but compressing too much into a single metric facilitates monopolistic behaviour.

Just chiming in to say that I agree completely here. Even the idea of multiple (modular) providers of reputation *scores* is likely misguided.

Trust is not a universal value of Bob, but a vector from Alice to Bob. Charlie’s trust vector for Bob will almost certainly differ from Alice’s. Nor is there such a thing as a comprehensive Alice–>Bob trust vector! Alice’s trust for Bob is highly context-dependent; even ignoring environmental factors (which is appropriate in this case), Alice almost certainly trusts Bob differently based on the domain of their interaction.

All this is to say that a) modularity is critical here, and b) I absolutely acknowledge that any sane attempt to quantify reputation will be hard-pressed to happen fully onchain, given the complexity involved and lack of a universal score. We likely need some system of async trust-minimized oracles, eg CCIP-read out to an AVS or something.

---

**spengrah** (2025-08-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/marco-metamask/48/15768_2.png) Marco-MetaMask:

> [Major] Single feedback or validation won’t be used to decide trust. People will always aggregate entries (including filtering or weighting based on the validator/feedback issuer’s reputation), which is hard to do on-chain anyway.

This is a valid and important point (see my other post above for more detail on why I agree). That said, I don’t see a strong reason for making this choice on behalf of other developers. Perhaps somebody will create an efficient contract to aggregate across N pieces of feedback or validation, or perhaps there will be niche but valuable use cases for other contracts to read individual pieces on their own.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/marco-metamask/48/15768_2.png) Marco-MetaMask:

> [Minor] Gas efficiency / keeping it simple without requiring the Agent Client to sign a transaction for each issued feedback. This can be mitigated by keeping it optional (I like this) or with an off-chain bundler that aggregates multiple feedback and signs transactions on behalf of issuers (which I don’t like because it adds significant overhead).

Optional for the Client Agent definitely makes sense here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/marco-metamask/48/15768_2.png) Marco-MetaMask:

> Anyway, let’s challenge this rationale! So:
>
>
> Which data would you save on-chain? Only the Rating and Response integers or other data structures too?
> Where? Registry storage?

At the very very least, I would make the event data available for contracts to read onchain, such as (in solidity):

```auto
// IReputationRegistry
function getAuthFeedback(uint256 agentClientID, uint256 agentServerID) external view returns (uint256 feedbackAuthId);

// IValidationRegistry
function getValidationResponse(uint256 agentValidatorID, uint256 agentServerID, bytes32 DataHash) external view returns (uint256 response);
```

I would also strongly consider an optional onchain feedback record, something like the following:

```auto
struct FeedbackData {
  string agentSkillId;
  string taskId;
  string contextId;
  uint256 rating;
  bytes proofOfPayment;
  bytes data;
}

mapping(string feedbackAuthId => FeedbackData feedback) public view feedback;

/// @notice stores feedback data onchain
/// @dev callable only by Server Agent
function submitFeedback(uint256 agentClientID, uint256 agentServerID, FeedbackData feedback) external returns (string feedbackAuthId);
```

We could also get even more ambitious here and do an onchain index of the above by TaskId, ContextId, and AgentSkillId for maximum legibility and filtering.

Likely, though, that should be left to helper contracts, similar to [how EAS uses its Indexer contract](https://github.com/ethereum-attestation-service/eas-contracts/blob/master/contracts/Indexer.sol). It’s possible that supporting something like that may require a small addition to the standard to ensure that writes can successfully hit both the contract specified by this standard and the indexer atomically without losing information.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/marco-metamask/48/15768_2.png) Marco-MetaMask:

> Can you provide use cases where single non-aggregated entries are useful? Or with basic on-chain aggregation? For example, “filtering” is easily implementable on-chain—like skipping all validations or feedback not emitted by whitelisted addresses. So you could calculate an average of filtered ratings, etc.

The main point I was trying to express at the top of this post is that we don’t know what will emerge as useful, valuable, or feasible; and therefore we shouldn’t foreclose the possibility for permissionless innovation if we can do so without compromising other goals.

I think the minimal suggestions I’ve made here (other than the more advance indexing stuff) meet that criterion. But I’m keen to hear what you think.

---

**Marco-MetaMask** (2025-08-25):

- You are correct. We should make it clear that using ERC-8004, exposing AgentCard at the well-known location becomes mandatory.
- Correct, you can’t have multiple agents at the same domain. Each agent should have its own N-level subdomain, which is what you usually get with modern CI/CDs. Do you see this as an issue?
- In the ERC we have function names, inputs and (with one exception) outputs. But yes, we will specify types and be more precise in a future version of the ERC or directly in the reference implementation.
- Yeah, the goal is to have just one singleton per chain (if we stay single-chain).

---

**gpt3_eth** (2025-08-25):

1. This ERC-8004 should not pick or embed any settlement flow (credits, x402, etc.). Payment belongs to the application layer, while 8004 stays focused on trust primitives.
2. But payment proofs should be referenceable in Reputation: what we can standardize is the hook: allow Feedback/Rating records to carry a lightweight reference to a payment proof so indexers can correlate economic activity with feedback.

---

**pcarranzav** (2025-08-25):

Is there a reason to make it mandatory? I think some people might want to run multiple agents on the same domain… if there’s a specific reason to restrict it I’d understand, it just seems odd since it looks to me like the identity registry could work just as well using URLs instead of domains. Especially because the A2A spec specifies registries as an *alternative* to the well-known URI. My suggestion would be to specify the URL of the Agent Card when registering an agent and use that to resolve instead of domains.

Which brings me to something that seems missing in the current ERC: how would the contracts validate who owns a domain? That seems like it will require a trusted party or some form of consensus / verification mechanism (zkTLS?) to prove domain ownership. The alternative would be to allow anyone to claim they own a domain, but then the contract should allow multiple agents claiming they are at a specific domain, and then ResolveByDomain could have multiple results…

re: function names, I guess I was confused by seeing names starting with uppercase, and not seeing the types for params and return values. I think this is important information to include in the ERC, rather than the reference implementation.

Good to hear that the plan is a singleton per chain ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**mlegls** (2025-08-26):

> Can you provide use cases where single non-aggregated entries are useful?

The biggest case I have in mind is automatic release of on-chain escrow, based on pre-agreed validation conditions. Alice wants to buy a job from Bob, who she doesn’t necessarily trust to correctly perform the job, and Bob doesn’t trust that Alice will pay after he does the job, so they can agree beforehand that Alice deposits escrow which is released when

- a consortium of voters agrees that Bob’s result is valid
- a mutually trusted third party re-runs the job and determines that Bob’s result is valid
- Bob submits a cryptographic proof that he ran the job in a TEE
- optimistic mediation, where the escrow is released by default after a certain time unless Alice disputes it, in which case one of the above mechanisms is used
- …

Any of these conditions can be represented by a single non-aggregated validation. The release conditions could be a generic parameter to any escrow contract (`(address arbiter, bytes demand)`, where there’s some other interface with a function `check(task, demand) => bool`). So any of the “basic on-chain aggregation” processes you describe could also be implemented in release conditions, either individually or in combination. So escrows could demand e.g. “a validation Response above X from any of a list of mutually trusted third parties” or “an average Response above X from a list of trusted third parties”.

> Which data would you save on-chain? Only the Rating and Response integers or other data structures too?

> Where? Registry storage?

I wrote an [example](https://github.com/mlegls/erc-8004-example/blob/313198c0d732dc25456ff94287b48c020e3aa6b4/contracts/src/peripheral/ValidationEscrow.sol) of an on-chain escrow contract working in combination with Sumeet’s reference implementation, which actually does store Response integers on-chain. I see two main flaws with it:

- The things to be validated are only identified by a dataHash, so they can’t be referred to before they concretely exist. This means you can’t distinguish between different validations from the same validator for the same server. Even if the contract stored already claimed dataHashes to prevent double claiming, servers could potentially get a validation for a different, easier task than the one escrowed for. The only workaround I could see in the current design would be for agentValidatorIds or agentServerIds to be essentially single-use, which seems to go against their intended design.
- Escrow demands can only be parametrized by the fields in the ValidationRequest or ValidationResponse struct, of which the only useful fields for parameterizing an escrow release condition are agentValidatorId, agentServerId, and the response Status integer. This isn’t as big of an issue though if you have something like a taskId, since you could implement different validator contracts representing different conditions (including aggregations of other validations), and have custom demand parameters implemented on each validator contract, where the validator contract submits a Response to the validation registry at the end of its internal process.

Compare this with the [implementation](https://github.com/CoopHive/alkahest-mocks/blob/f80250945cffa2303fb83e87cff4080ef27e4d6b/test/deprecated/TokensForStrings.t.sol#L50) of escrows with generically parameterized demands that I linked in the previous comment, where the on-chain [interface](https://github.com/CoopHive/alkahest-mocks/blob/main/src/IArbiter.sol) is a function

```auto
interface IArbiter {
    function checkObligation(
        Attestation memory obligation,
        bytes memory demand,
        bytes32 counteroffer
    ) external view returns (bool);
}
```

which is agnostic to where data is stored, and could be implemented transiently if the check is simple enough to perform in one tx (e.g., just checking that the fulfilling counterparty is a [particular address](https://github.com/CoopHive/alkahest-mocks/blob/main/src/arbiters/attestation-properties/non-composing/RecipientArbiter.sol)).

My suggestions for the ERC would be

- add an identifier which can be arbitrarily requested, by which agent tasks can be referenced before they concretely exist.
- add a (perhaps optional) on-chain function function getValidation(uint256 taskId) returns (int status) (or returns (Response response), or something to associate taskId with dataHash, and still getting Response by dataHash like in the reference implementation.)

Tentatively, I’d also consider having pre-dataHash references for tasks be a generic demand (as bytes or bytes32 hash) rather than an integer id. But I’m not sure if there are use cases where this enables something that wouldn’t be possible with just an id (by putting anything demand-related on individual validator contracts or off-band), and it’s probably best to keep the ERC implementation requirements as lightweight as possible.


*(81 more replies not shown)*
