---
source: magicians
topic_id: 20249
title: "ERC-7722: Opaque Token"
author: ivica
date: "2024-06-09"
category: ERCs
tags: [erc, token, privacy, security-token]
url: https://ethereum-magicians.org/t/erc-7722-opaque-token/20249
views: 1959
likes: 20
posts_count: 24
---

# ERC-7722: Opaque Token

Dear Ethereum Magicians, I would like to discuss this ERC draft with you. We have successfully applied this mechanism in our own solutions and now aim to formalize it into an ERC and share it with the community. I am looking forward to your feedback!

[ERC-7722](https://eips.ethereum.org/EIPS/eip-7722)

---

## eip: 7722
title: Opaque Token
description: A token specification designed to enhance privacy by concealing balance information.
author: Ivica Aračić (@ivica7), SWIAT
status: Draft
type: Standards Track
category: ERC
created: 2024-06-09

## Abstract

This ERC proposes a specification for an opaque token that enhances privacy by concealing balance information. Privacy is achieved by representing balances as off-chain data encapsulated in hashes, referred to as “baskets”. These baskets can be reorganized, transferred, and managed through token functions on-chain.

## Replies

**Mani-T** (2024-06-11):

Good idea for enhancing token privacy and security in regulated environments.

---

**ivica** (2024-06-11):

Thank you for your feedback. Exactly, having a “token operator” or a “crypto security registrar” involved, which is mostly the case in regulated environment, makes it easier to solve the question of the off-chain data source. Moreover, investors do not have to rely on one single data source exclusively, they can copy the off-chain data that they’re eligible to see to their own storage and check the integrity via hashes on-chain.

---

**ivica** (2024-06-14):

Update:

- moved the part for unifying fungible/non-fungible to future work section in order to keep the complexity low
- introduced the analogy of baskets for better understandability

TODOs:

- token master data (name, decimals, symbol, …)
- allow multiple tokens within one smart contract instance (improves efficiency and privacy)
- propose the authentication mechanism for fetching the basket details

---

**MirkoK** (2024-06-14):

Since contract here is only managing baskets, without knowing what is inside, there is no reason why it could not manage any number of different tokens, so here is my proposal to solve first 2 of TODOs:

Extend basket definition in external data with token id:

```auto
basket: keccak256(abi.encode(salt, value, tokenId)),
      data: {
        salt: ,
        value: ,
        tokenId:
      }
```

this way, we can have any number of different tokens handled by this contract, but now oracle should have another responsibility, to validate that all baskets in reorg have same tokenId. This tokenId can also be used to connect to token master data, that can be stored off-chain or in different smart contract.

Here is an idea for additional functionality: something similar to ERC-20 allowance mechanism would likely be easy to add and can be very useful. For example a method like:

```auto
function approve(address spender, bytes32[] calldata baskets) external;
```

that would give spender ability to transfer a basket owned by caller.

---

**ivica** (2024-06-14):

[@MirkoK](/u/mirkok) good ideas! Thanks a lot. I think extending the interface like this could work (see below, just a rough sketch for now, I will incorporate the changes later into the specification). I was slightly concerned that mint would be too complex, but what could work out is to define the total supply as basket too. And then split this total supply basket via reorg as we go with minting. I guess, we would need two separate reorg functions for that (reorgHolderBaskets, reorgSupplyBaskets), but the good thing is that it works analogously and the same oracle reorg request can be used.

```auto
    /* create a new token */
    function createToken(
        bytes32 tokenId,
        bytes32 totalSupplyBasket,
        bytes32 ref
    ) external;

    /* mint / issue */
    function mint(
        bytes32[] calldata availableSupplyBaskets,
        address receiver,
        bytes32 ref
    ) external;

    /*
    transfers a set of baskets to a new owner.
    */
    function transfer(
        bytes32[] calldata baskets,
        address receiver,
        bytes32 ref
    ) external;

    /*
    reorganizes a set of holder input baskets (basketsIn) and creates as result a new set of baskets (basketsOut)where the sum of all values from input baskets equals the sum of values in output baskets. In order to ensure the integrity, external oracle service is required that will sign the reorg proposal requested by the basket owner.
    */
    function reorgHolderBaskets(
        SIGNATURE[] calldata reorgOracleSignatures,
        bytes32[] calldata basketsIn,
        bytes32[] calldata basketsOut,
        bytes32 ref
    ) external;

    /*
    reorganizes the available supply, e.g. in preparation for a mint
    */
    function reorgSupplyBaskets(
        SIGNATURE[] calldata reorgOracleSignatures,
        bytes32[] calldata basketsIn,
        bytes32[] calldata basketsOut,
        bytes32 ref
    ) external;

    /*
    burns holder baskets and returns them to available supply
    */
    function burn(
        bytes32[] calldata baskets,
        bytes32 ref
    ) external;
```

Also a good idea with “approve”. Although I think, based on the experience that we had so far, it would be better to have something like earmark which blocks a basket, so it can be used for Delivery-vs-Delivery contracts too. That was one of the challenges we had with approve in ERC-20, in order to make Delivery-vs-Delivery work, you would need to transfer the token to the Escrow smart contract, which kind of destroys the link to the beneficiary owner of that balance… but let’s focus first on getting the first part right with multi-token support+mint+burn before we open that box.

---

TODOs:

- integrate the new interface into the token specification

multi-token support
- mint/burn
- token master data endpoint

propose the authentication mechanism for fetching the basket details
earmarking / approve

---

**ivica** (2024-06-15):

Update:

- added multi-token support
- added mint / burn

TODOs:

- propose the authentication mechanism for fetching the basket details
- (add?) token master data endpoint
- (add?) earmarking / approve

---

**mathewmeconry** (2024-06-15):

I like the proposal to increase privacy on-chain, especially when we want users to use the chain for real-world payments where a leak could be inconvenient or even have a greater impact on the person’s life.

What I am curious about is why you opted for oracles and not some linear homomorphic encryption. I am aware that this is currently too expensive gas-wise or not even possible with the current gas limits but I think this would be a great addition to the current set of precompiles or even as a new opcode to make it possible.

The benefit of this encryption scheme is that there is no trusted party needed when it is combined with public key cryptography.

This would remove the need for oracles and some complex logic with slashing and tracking bad behaviour.

Solana added this functionality with their latest token program update and use the ElGamal encryption scheme to keep track of balances and do basic math on encrypted values. [Protocol Overview | Solana Program Library Docs](https://spl.solana.com/confidential-token/deep-dive/overview#twisted-elgamal-encryption)

---

**ivica** (2024-06-15):

[@mathewmeconry](/u/mathewmeconry) before going for the solution with oracles, we first had two prototypes with homomorphic encryption (similar to Solana) and ZKPs.

The ZKP prototype was about implementing equality proof in zokrates for the splitting a basket into two and joining two baskets into one. However, the proof generation was too intensive and the proof verification alone was 1M+ gas. Moreover, it was very costly to join or split multiple baskets at once. I am not sure, eventually now (~3y later) there are more efficient ZKP solutions to solve the challenge, we didn’t further investigate.

The other prototype (~5y ago) was with homomorphic encryption similar like Solana is solving it, however it was too expensive gas-wise as you already mentioned and it involved managing additional public/private key pairs for encryption/decryption. Moreover, we also got stuck in our prototype with solving the range and equality proofs, which Solana seems to have solved elegantly now!

Hence, we decided to go for the solution with oracles. For us it works well, because with banks we’re in a regulated environment where a security token will have a registrar (aka token operator). Like for instance required in German law for electronic securities (aka crypto securities). The registrar is the natural place to place the primary source for the off-chain data and also the oracle function. Moreover, in SWIAT we also have decentralized off-chain data management, which will automatically sync the confidential data between the nodes if the participant is eligible to read it. All these factors together make it a good and much simpler choice for the regulated environment in which we operate.

In regard to Solana’s solution: I like the approach very much, I also agree that Ethereum might also profit from the same confidentiality mechanism.

---

**rahul-aztec** (2024-06-16):

Great idea! Been thinking a decent bit about tokens with privacy that also satisfy some compliance requirements because of my work at Aztec! I enjoy having a token operator that can act as an auditor almost! ZCash and other privacy networks have a concept of viewing keys to enable this.

Through the idea of baskets, you have effectively made something like UTXOs on top of etheruem’s account storage model! I suppose you prevent double spending of the same basket through the oracles which is nice.

> revealing an identity would expose the entire portfolio of that identity from the on-chain data.
> I really like this statement in the ERC. But I may be confused here - it looks like at each transfer event, you are leaking the receiver’s address? So it does continue to leak the other (non opaque) tokens of the receiver? Given a lot of non opaque tokens exist, an interesting idea could be using IDs for addresses? Ids => address mapping are stored privately by the operator and by individual users.
> This ofcourse creates some other problems:

- Nothing changes to discover your baskets
- But before you send tokens to someone, you must first consult the operator’s registry (could also be another endpoint)

If I understand your proposal correctly, the operator (or the oracle provider) anyway knows contents of each baskets so this doesn’t leak any additional privacy

Could you explain a bit about reorgs? Is this a way to avoid why Solana’s token extension had “pending balances”?

Lastly, another function worth adding could be converting your normal ERC20s into an opaque token? At Aztec we call this operation `shield`

Nit; is there a reason the phase `salt` was chosen over `nonce`?

---

**ivica** (2024-06-16):

[@rahul-aztec](/u/rahul-aztec) thank you very much for commenting. You’re absolutely right, there are strong similarities between the basket and UTXO model.

About reorg: It works in the way that it takes a set of input baskets and “reorganizes” it to a set of output baskets under the condition that per tokenId, the sum of all basket values from the input set is equals the sum of all basket values from the output set. `salt` is primarily used to increase the randomness of the basket hash, so brute-forcing the hash isn’t possible. I didn’t check it in details yet, but nonce is most probably not required since we can avoid replay by following some rules (to be exactly defined).

Moreover, you’re also right that the model used “naively” leaks some information. For instance, if we have the following situation:

```auto
A owns basket-a1{salt:, tokenId:1, value:10}
A: transfer basket-a1 to B
B: transfer basket-a1 to C
```

the following information is leaked to:

1. all observers: A is sending something to B & B is sending something to C
2. A: would know what in basket-1 is, since he was in ownership of it, i.e., he would also know B has sent 10 to C

The second one can be solved by using reorg before sending for reshuffling the baskets.

Example with reorg:

```auto
A owns basket-a1{..., value:10}
B owns basket-b1{..., value:5}, basket-b2{..., value:15}, ...
A: transfer basket-a1 to B
B: reorg [basket-a1, basket-b1, basket-b2]
      to [basket-b3{..., value:10}, basket-b4{..., value:10}, basket-b5:{..., value:10}]
      where sum of inputs is the sum of outputs
B: transfer basket-b5{value:10} to C
```

Now A doesn’t know what B is sending to C, since the basket he sent to B has been reorg-ed together with his other baskets.

Note that we can also create baskets with value:0 to add more noise. Baskets with value:0 can also be sent to random receivers to overlay additional noise.

Example with reorg and null-value basket transfers:

```auto
A owns basket-a1{..., value:10}
B owns basket-b1{..., value:5}, basket-b2{..., value:15}, ...
A: transfer basket-a1 to B
B: reorg [basket-a1, basket-b1, basket-b2]
      to [basket-b3{..., value:10}, basket-b4{..., value:10}, basket-b5:{..., value:10},
            basket-b6:{..., value:0}, basket-b7:{..., value:0}]
      where sum of inputs is the sum of outputs
B: transfer basket-b5{value:10} to C
B: transfer basket-b6{value:0}  to D
B: transfer basket-b7{value:0}  to E
```

Now still observers can see who is communicating with whom, but since there is noise introduced, they can not tell actually which of these transfers are real and which are noise.

---

**ivica** (2024-06-17):

[@abcoathup](/u/abcoathup) I’m not entirely sure about the exact process, but from my side, the pull request for the ERC-7722 draft is ready to be merged.

---

**abcoathup** (2024-06-18):

[@ivica](/u/ivica) an ERC editor (which I am not) needs to review a PR before it can be merged.  It may take some time.  Whilst you wait, make sure that the PR isn’t raising any linter issues.

---

**chechuch** (2024-06-24):

Hello [@ivica](/u/ivica) . Congrats for the ideas and the hard work. I’m not coder but I’m invoved in the blockchain ecosystem since 2016. Sometimes when creating this kind of projects I always feel like there were missing something. In this case, and thinking about privacy (and in EU it is very important) regulation is forgotten.

Althought I’m not very deep (but enough) in regulation, I was wondering if something more can be added in terms of regulation (thinking about MiCA) that can be added when creating this kind of tokens. Probably just a signature inside the data or something like that. Probably enough.

It is the third time I come here to take a look to this ERC and it is my first post in the Ethereum Magicians so I hope not been saying any stupid thing. Just trying to bring here my “2 cents”

Anwsering to “why” to my reflection is because I would like to improve enterprises using public systems instead of trying to use any permissioned blockchain networks.

Kind Regards!

---

**ivica** (2024-06-24):

[@chechuch](/u/chechuch) thanks for commenting. I am not quite sure what you’re targeting to. Eventually you can explain more the background here or via the private message.

---

**ivica** (2024-08-09):

[@SamWilsn](/u/samwilsn) thank you very much for taking the time to review the PR. I’ve updated the proposal accordingly.

---

**SamWilsn** (2024-10-14):

Two non-editorial questions/suggestions:

- Is it necessary to standardize createToken, mint, and possibly burn? They feel like admin functions that would only really be called by the token’s creator. If that’s true, you don’t need to include them in the standard because the creator always knows how to interact with their own contract. Notice that neither ERC-20 nor ERC-721 include minting or burning in their interfaces.
- You don’t define under what circumstances each event is emitted, nor do you define their arguments.

---

**ivica** (2024-10-18):

Thank you for the feedback Sam. I will consider if mint and createToken can be removed. You’re right, they would only be used by the token operator, however, for the holder side it is of interest when a token has been created and what the initial supply is. Will think about this in more details.

Will also add documentation for the events.

Just noticed, it’s also missing who is allowed to call which function.

---

**ivica** (2024-11-27):

[@stichlila81](/u/stichlila81) DeFi protocols in Ethereum in general heavily rely on ERC-20 and having the balances on-chain. As written in the draft, ERC-7722 intentionally breaks with this compatibility in favor of hiding balances on-chain.

---

**MirkoK** (2024-11-29):

Hi [@SamWilsn](/u/samwilsn), here is why we have admin functions defined although that is not common practice in other standards:

Create token and mint are part of the framework that enables total supply of a token to be defined, maintained and verified. This is needed since amounts are kept off chain. Total supply is defined in `createToken` and kept in supply basket(s). Mint and burn are then used to move amounts between holder and supply baskets. If we were to remove those methods maintaining integrity of total supply would be negatively affected.

---

**Bobby5424** (2024-12-02):

How does the introduction of the tokenId in the basket definition improve the flexibility of managing multiple tokens in the same contract, and what impact does it have on the validation process?


*(3 more replies not shown)*
