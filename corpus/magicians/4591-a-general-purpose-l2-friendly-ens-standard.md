---
source: magicians
topic_id: 4591
title: A general-purpose L2-friendly ENS standard
author: vbuterin
date: "2020-09-10"
category: Web > User Experience
tags: [layer-2, ens]
url: https://ethereum-magicians.org/t/a-general-purpose-l2-friendly-ens-standard/4591
views: 6810
likes: 25
posts_count: 12
---

# A general-purpose L2-friendly ENS standard

One challenge of migrating to L2s such as rollups and plasma for scalability is that a lot of infrastructure that we depend on today still depends on L1 blockchain accesses. This post proposes a way to resolve this problem for the specific use case of ENS names.

### Proposal

We define a class of actors called **ENS attesters**. Anyone can become an ENS attester by depositing tokens (ETH but potentially other things too) into an **ENS attester contract**, which has a predefined code whose logic is described below. If a wallet wants to resolve a particular ENS name where that name or a super-domain thereof appears on L1 to be owned by an L2 contract, it can send a message to an ENS attester (discoverable through a specialized p2p network, **the ENS attester network**) asking for a **response message** of the form `(block_height, name, address, signature)` providing the address that the name resolves to at some given block height, plus a signature.

Logic for how ENS attesters are incentivized to respond is outside the scope of this proposal; this could be subsidized by dapp developers, or done through channel payments or some other means.

The ENS attester contract’s logic is as follows.

- Each instance of the contract maps to one ENS attester, and stores the attester’s public key (realistically, an ethereum address that ECDSA signatures can be ECRECOVER’d against)
- Funds deposited in the contract can be withdrawn but only with a 1 week withdrawal window.
- If an ENS attester signs a response message (block_height, name, address, signature), and someone disagrees with the result, then they can take this signature and push it into the ENS attester contract, along with a deposit, via a challenge function
- The challenge function delays any withdrawals and begins a 2 week challenge period. The attester can successfully respond to a challenge by performing any required actions to cause the owner of the name (or a super-domain of the name) to make a contract call assertHistoricalOwnership(block_height, name, address) to the attester contract, asserting that the given name resolved to the given address at the given block height. If the attester successfully responds, they get half the challenger’s deposit and the other half is burned. If they fail to respond, the challenger gets half the attester’s deposit (plus their deposit) and the other half gets burned.

### Rationale

The goal of this design is to be compatible with ENS names being stored in rollup or plasma settings. The goal is that rollups/plasmas would be designed with ENS support in such a way that the plasma/rollup contract would be the actual owner of the ENS name that is transferable inside the plasma/rollup, and the contract would be capable of making a contract call to assert its historical ownership.

Note that the `assertHistoricalOwnership` standard could be applied at any level: at the level of the individual domain, or at the level of an ENS domain that lives entirely inside a rollup/plasma and contains many subdomains.

Asserting historical ownership, rather than present ownership, is needed to prevent attacks where some user `A` asks for an assertation that some given `domain` resolves to `A`, and then quickly sending a transaction making it resolve to `B` instead before the attester can do anything.

## Replies

**jpitts** (2020-09-10):

This was X-Posted over to the ENS Forum…


      ![image](https://discuss.ens.domains/uploads/db9688/optimized/2X/f/fad3838fbd488ddd89256654d6688bfa0654330c_2_32x32.png)

      [ENS DAO Governance Forum – 10 Sep 20](https://discuss.ens.domains/t/x-post-a-general-purpose-l2-friendly-ens-standard/209)



    ![image](https://discuss.ens.domains/uploads/db9688/original/2X/f/fad3838fbd488ddd89256654d6688bfa0654330c.png)



###





          💬 General Discussion






This proposal was posted over in the Magicians’ Forum:   One challenge of migrating to L2s such as rollups and plasma for scalability is that a lot of infrastructure that we depend on today still depends on L1 blockchain accesses. This post...



    Reading time: 1 mins 🕑
      Likes: 1 ❤

---

**rumkin** (2020-09-10):

Seems like it could be generalized to response verification to verify any kind of information stored into blockchain or sidechains. Attester verifies the call result with some bid and signature providing the block for which the result is valid. So then in the case of mismatch this transaction could be sent back into blockchain to withdraw the bid to punish the attester.

How it works:

1. User sends method call to attester, as a regular method call via eth_call.
2. Attester reads the data from blockchain and generate verified response, which contains:

Method call result.
3. Verification:

contract which holds funds to withdraw.
4. amount to withdraw if the response is wrong.
5. signature.

If the result is wrong, then user can form new transaction with the call data, block number, response, address to withdraw funds, and verifier signature. And submits it to withdraw the proof amount.

This needs a new type of transaction let’s name it *assert* transaction, which could be executed at custom block number, but should be written in the latest block.

## UPD 1

Or it could be made within the blockchain with a new opcode to make a history call. Like this:

```auto
contract AssertContract {
  address public token;
  address public attester;

  function historycalTokenAmount(address owner, uint256 blockN /* ⚠️ */)
    public view returns(bytes memory)
  {
    require(blockN < block.number, 'token_amount/block_number_lt');

    // ⚠️ Then use blockN in the call below 👇 to perform a historical call
    uint256 amount = ERC20(token).balanceOf{block: blockN}(owner)
    return abi.encode('uint256', amount);
  }

  function assertCall(address owner, uint256 blockN, uint amount, bytes32 proof, uint8 r, bytes32 s, bytes32 v)
    public
  {
    bytes memory result = historycalTokenAmount(owner, blockN);

    if (keccak256(result) == proof) {
        return;
    }

    address signer = ecrecover(proof, r, s, v);

    if (signer != attester) {
        return;
    }

    msg.sender.transfer(amount);
  }
}
```

## UPD2

There definitely should be some nonce, to prevent deposit from being withdrawn multiple times.

---

**makoto** (2020-09-11):

Hi, I  am not so well averse to rollups so apologies if my questions are bit off the point.

Can I assume this is for users to register names on L2 and periodically bulk commit these names into L1 or has these names never be committed to L1 but always enquired via ENS attesters?

If this is more for wallet providers to get L1 name on L2, the wallet can just enquire names in L1 as most lookup doesn’t require to be in the same chain. If you want to lookup in the same chain, POA proposed AMB ENS mirroring https://github.com/poanetwork/tokenbridge-contracts/pull/468 . It’s traditionally master-slave model which requires no change on ENS itself, though it remains expensive to register names in L1 and also calling AMB to mirror in L2.

If this is to let users register names on L2 and bulk commit to L1, [@Arachnid](/u/arachnid)  proposed doing it using rollup-ish approach for DNS name proving here https://discuss.ens.domains/t/improving-gas-efficiency-of-dns-domain-claims-with-optimistic-verification/189 . My understanding is that it is only valid for computing intensive work such as validating DNSSEC proof so not for other usage which only uses gas for storage in L1.

With the above alternatives in mind, I am assuming that users only register names on L2 and never commit to L1. In that case, does user have to ask attestant if a name he/she wants to register already exist on L2? Also does the ENS attesters only handle one L2 or it has to enquire every participating L2 chains (Matic/xDAI/OMG/Fuel Labs) etc?

---

**vbuterin** (2020-09-13):

The goal is that they are never committed to L1.

> In that case, does user have to ask attestant if a name he/she wants to register already exist on L2?

Registering names would not be done through this protocol; that would be done through the underlying L2 protocol.

> Also does the ENS attesters only handle one L2 or it has to enquire every participating L2 chains (Matic/xDAI/OMG/Fuel Labs) etc?

Individual attesters could specialize in one or a few L2 chains, but the protocol is designed to be maximally agnostic and support all L2 protocols.

---

**vbuterin** (2020-09-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rumkin/48/1330_2.png) rumkin:

> Seems like it could be generalized to response verification to verify any kind of information stored into blockchain or sidechains. Attester verifies the call result with some bid and signature providing the block for which the result is valid. So then in the case of mismatch this transaction could be sent back into blockchain to withdraw the bid to punish the attester.

I like the idea of trying to generalize it! Though a concern is that the protocol is designed to support many kinds of L2s, many of which will not eg. support the full EVM. I suppose that L2s can adopt a standard of being able to respond to whatever range of static calls against historical state that they are capable of supporting?

> This needs a new type of transaction let’s name it assert transaction, which could be executed at custom block number, but should be written in the latest block.

The problem with this approach is that it would require a transaction to go on-chain (even if inside the rollup), whereas ideally reads could be done without any on-chain action (because that’s how it works now).

---

**Arachnid** (2020-09-14):

Interesting idea! If I’m understanding it correctly, the assumption here is that a client that wants to resolve names is synced to L1, but not to the L2 chain the name they want is on, correct? They have to be synced to L1 in order to determine that an attester is bonded.

Further, I assume that attesters have to manually review each contract they’re prepared to attest for, to ensure that it’s not written in a way that could be used to make false claims about the address a name resolves to?

---

**vbuterin** (2020-09-16):

> Interesting idea! If I’m understanding it correctly, the assumption here is that a client that wants to resolve names is synced to L1, but not to the L2 chain the name they want is on, correct?

Correct. Furthermore, there is an explicit goal that client software should not be forced to have separate software logic for each individual L2, so that ENS infrastructure can still be written once and would automatically work with all of the L2’s out there including new ones created later.

> Further, I assume that attesters have to manually review each contract they’re prepared to attest for

Yes. Assuming by “review” you mean “make sure they’re okay trusting it, in the same way that you need to make sure you trust an L2 contract if you’re storing funds in it”, and not some notion of everyone auditing for themselves. The risk of being an attester is comparable to the risk of holding funds in the same L2.

---

**Arachnid** (2020-09-20):

I like it; my one concern is that this is backwards-looking; a malicious attester could potentially start generating invalid results that direct funds to their own wallet, and get away with it for a full two weeks before they’re slashed! That could add up to a lot more than the cost of their deposit.

---

**vbuterin** (2020-09-22):

Right, I see the concern. I guess one option would be to seek out multiple attesters, and if there’s any disagreement at all, wait until it resolves on-chain. Will think more if there’s better alternatives…

---

**makoto** (2020-09-30):

Hello all.

Vitalik kindly presented his proposal at our ENS online workshop and here is the summary of his presentation with link to the Youtube video.

https://medium.com/the-ethereum-name-service/general-purpose-layer-2-static-calls-proposal-presentation-by-vitalik-buterin-at-ens-online-2d752906719e

---

**makoto** (2020-10-14):

We held follow up meeting and here is the summary write up https://discuss.ens.domains/t/results-of-the-first-ens-layer-2-meeting/256/4

