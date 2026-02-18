---
source: ethresearch
topic_id: 3539
title: Plasma Leap - a State-Enabled Computing Model for Plasma
author: johba
date: "2018-09-25"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-leap-a-state-enabled-computing-model-for-plasma/3539
views: 8396
likes: 12
posts_count: 8
---

# Plasma Leap - a State-Enabled Computing Model for Plasma

This is a proposed extension to More Viable Plasma. It is inspired by conversations at the [solEVM calls](https://hackmd.io/s/BkAX4LlEm) with [@jdkanani](/u/jdkanani), [@esteban](/u/esteban) and [@mrsmkl](/u/mrsmkl).

## tl;dr

We propose a computing model on Plasma by breaking down smart contracts into smaller programs called Spending Conditions. A computation verification game is given to verify any Spending Condition executed on Plasma. By encapsulating state into non-fungible tokens a stateful programing model is introduced that enables **“Dapps to leap onto Plasma”**. To achieve this, subjective data availability assumptions do not need to be weakened and only minimal modifications to the Plasma exit game are needed.

## Problem Statement

**Enforcing off-chain computation -** a computing model for rules and conditions governing funds on the Plasma chain is required, as well as the enforcement of correct execution of such code. Participants need to be able to prove execution of code and penalize the operator for including transaction with such incorrect transitions. The verification needs to be economically feasible inside the Ethereum Virtual Machine (EVM) and should not exceed the capacity of the Ethereum network at any time [[tb]](https://people.cs.uchicago.edu/~teutsch/papers/truebit.pdf).

**Exit authorization -** if funds are controlled by complex rules and conditions for spending with multiple owners or even no specific owners, these owners might not agree on the availability of data or there might be no-one with the authority to exit the specific funds. Thus, exits can be hard or impossible to coordinate if funds have multiple or undefined ownership [[kf]](https://medium.com/@kelvinfichter/why-is-evm-on-plasma-hard-bf2d99c48df7).

**Spending authorization -** a coordination problem arises for funds that entered the exit queue, but are protected with rules and conditions similar to anyone-can-spend. The possibility for a grieving attack emerges where anyone can spend such funds and cancel the exit [[jb]](https://ethresear.ch/t/why-smart-contracts-are-not-feasible-on-plasma/2598).

## Spending Conditions

Spending conditions are scripts providing the ability to apply specific rules and conditions to the transfer of funds, similar to [Bitcoin P2SH](https://www.soroushjp.com/2014/12/20/bitcoin-multisig-the-hard-way-understanding-raw-multisignature-bitcoin-transactions/). Spending conditions are smart-contract-like scripts written in Solidity. Yet, unlike smart contract spending conditions shall not affect arbitrary state. This would make the exit game for any spending condition infeasible, as described in [[why smart contracts are not feasible]](https://ethresear.ch/t/why-smart-contracts-are-not-feasible-on-plasma/2598). Rather, the output of spending conditions execution should not be affected by storage or other transfers. The inputs and outputs of the transaction fulfilling the spending condition are the only permitted side effects.

```auto
contract SpendingCondition {
    using Reflectable for address;
    uint256 constant nonce = 1234;    // nonce, so that signatures can not be replayed
    address constant spenderAddr = 0xF3beAC30C498D9E26865F34fCAa57dBB935b0D74;

    function fulfil(bytes32 _r, bytes32 _s, uint8 _v,      // signature
        address _tokenAddr,                               // inputs
        address[] _receivers, uint256[] _amounts) public {  // outputs
        require(_receivers.length == _amounts.length);

        // check signature
        address signer = ecrecover(bytes32(ripemd160(address(this).bytecode())), _v, _r, _s);
        require(signer == spenderAddr);

        // do transfer
        ERC20Basic token = ERC20Basic(_tokenAddr);
        for (uint i = 0; i  bytes32) data;

  function read(uint256 _tokenId) public view returns (bytes32) {
    return data[_tokenId];
  }

  function verify(
    uint256 _tokenId,     // the token holding the storage root
    bytes _key,           // key used to do lookup in storage trie
    bytes _value,         // value expected to be returned
    uint _branchMask,     // position of value in trie
    bytes32[] _siblings   // proof of inclusion
  ) public view returns (bool) {
    require(exists(_tokenId));
    return tree.verifyProof(data[_tokenId], _key, _value, _branchMask, _siblings);
  }

  function write(uint256 _tokenId, bytes32 _newRoot) public {
    require(msg.sender == ownerOf(_tokenId));
    data[_tokenId] = _newRoot;
  }
}
```

A single attribute per token is added which is the storage root of a Merkle Patricia Tree. An authenticated function to update the root is provided and a view-only function allows to verify the existence of a key-value pair according to the storage root.

## Application Examples

Let’s have a look at a few application examples that become possible using this model.

```auto
contract CounterCondition {
    using Reflectable for address;
    uint256 constant tokenId = 1234;
    address constant spenderAddr = 0x1234;

    function fulfil(bytes32 _r, bytes32 _s, uint8 _v,   // signature
        address[] _tokenAddr,                           // inputs
        address _receiver, uint256 _amount) public {    // outputs

        // check signature
        address signer = ecrecover(bytes32(ripemd160(address(this).bytecode())), _v, _r, _s);
        require(signer == spenderAddr);

        // update counter
        StorageTokenInterface stor = StorageTokenInterface(_tokenAddr[1]);
        uint256 count = uint256(stor.read(tokenId));
        stor.write(tokenId, bytes32(count + 1));

        // do transfer
        ERC20Basic token = ERC20Basic(_tokenAddr[0]);
        if (count = threshold);

        // do transfer
        ERC20Basic token = ERC20Basic(_tokenAddr[0]);
        token.transfer(address(_receiver), _amount);
    }
}
```

Another example for a spending condition is a stateful multi-signature wallet. In this example Alice, Bob and Charlie combine state that is stored in their personal storage tokens. Once two of the three participants update their storage tokens to point to the same destination address, the funds held under the multi-sig spending condition can be transferred.

## Discussion

By changing perspective, and considering fungible and non-fungible tokens the only first-class citizens on the Plasma chain, a stateful computation model that complies with the known exit game is possible. Yet, limitations are imposed by the constraints of the Plasma design. The assumption of subjective data availability limits the freedom of developers in implementing the fulfillment of conditions. The need to add an exit-authorization function to every condition also puts a limit on the number of parties collaborating in a contract.

In addition to the mentioned challenge, we see the following **limitations and open issues with Plasma Leap:**

- Ability to fit OP-codes with dynamic data size into blockgaslimit is unclear.
- Do computation verification incentives also capture the long tail (holders with small balances) in a single operator model?
- Deeper analysis on limbo exits under MoreVP is needed.
- How to provide compact witnesses to state updates of NSTs?
- UX challenges inflicted by liveliness assumption of L2 solutions in general.

inability to build watch towers for exits.

## Conclusion

We have created a computing model that allows to put tokens under the control of programmable conditions. We have created incentive games that enforce the correct execution of these conditions off-chain by the Plasma operator. Further we have extended the exit game with the ability to exit such Spending Conditions and associated tokens to the Ethereum network. Lastly, we have extended the computing model with the ability to store state across invocations.

Smart contract as known on Ethereum are just one way to enable decentralized applications. With this architecture we hope to have considerably widened the scope of decentralized applications that can be implemented on layers-2 scaling solutions.

**Note:** I am looking for co-authors and reviewers of the [full version](https://docs.google.com/document/d/1vStTjqvqZGyiI5AVtpwCIMlHFnzC_4bbixsCfs27-M8).

## Replies

**kladkogex** (2018-09-25):

The problem with Truebit protocol is that the first version was unsecure and the second version was never published.

I, personally, have never seen a secure spec from Truebit - may be it can be done securely, but no-one published the spec yet …

---

**mtsalenc** (2018-09-25):

Could you include details/links about the insecurity of the protocol you are talking about?

Maybe you will find this interesting: [Multiparty Interactive Verification](https://ethresear.ch/t/multiparty-interactive-verification/1221)

---

**kladkogex** (2018-09-25):

Here is a discussion we had some time ago



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Truebit-protocol front running vulnerability](https://ethresear.ch/t/truebit-protocol-front-running-vulnerability/1215) [Multiparty Computation](/c/cryptography/mpc/14)




> Since people here suggested using Truebit for several purposes,  it is important that we understand security properties of the Truebit whitepaper
> It seems that Truebit protocol is vulnerable to front running  in the following way:
> Truebit pays bounties to verifiers that successfully challenge incorrect computations.
> The problem with the bounties is that parasitic verifiers can verify nothing, and simply wait for good guys to report errors.
> Since everything on the blockchain is public, I can …

---

**johba** (2018-09-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The problem with Truebit protocol is that the first version was unsecure and the second version was never published.

I think what you describe here is Truebit’s incentive layer. If you recall the paper, they have it split into the dispute resolution layer and the incentive layer, second deals with creating an equilibrium for validators.

In this proposal we only borrow the dispute resolution layer from Truebit. The incentives need to be figured out in the context of Plasma:

- I see problems specifically for holders of small balances. Such users will unlikely put down a big deposit to challenge the operator in an invalid transition.
- Replacing the operator with a token-bonded set of PoS validators could be an elegant solution to create a sort of peer pressure to challenge each other.

In both setups I don’t see a reason why rewards for challenges should be split. First-come-first-serve would work perfectly.

---

**mtsalenc** (2018-09-28):

[@johba](/u/johba) since NSTs allow their state to be updated in the plasma chain, doesn’t `fulfil()` need to have a challenge period as well?

Otherwise a spending condition could be fulfilled with outdated NST state right?

---

**johba** (2018-09-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/mtsalenc/48/348_2.png) mtsalenc:

> since NSTs allow their state to be updated in the plasma chain, doesn’t fulfil() need to have a challenge period as well?
>
>
> Otherwise a spending condition could be fulfilled with outdated NST state right?

Good point, I’ve been considering two situations:

[![26%20PM](https://ethresear.ch/uploads/default/original/2X/6/6eadee1ea7874179a44a56b8a67c3c765e837f0d.png)26%20PM400×212 32.4 KB](https://ethresear.ch/uploads/default/6eadee1ea7874179a44a56b8a67c3c765e837f0d)

When **writing** the storage token would be referenced and spent, creating a new output with the latest state. The state transition rules of the Plasma chain stay unchanged, only unspent outputs can be spent. If a spent output is spent again, a classical double-spend situation emerges and the Plasma operator will loose his bond.

[![19%20PM](https://ethresear.ch/uploads/default/original/2X/1/118aac348a7bc9da7a7d80efa83d8f5ba12e4439.png)19%20PM400×209 28.2 KB](https://ethresear.ch/uploads/default/118aac348a7bc9da7a7d80efa83d8f5ba12e4439)

In the **reading** situation the spending transaction would reference a UTXO holding a storage token, but not update the content. The output would not be spent in the UTXO model.

This requires a slight modification to the state transitions rules of the Plasma chain. The read-only input of this transaction would need to have a flag. The double-spend challenge function would need to be extended where an earlier write-spending can challenge a read-input, but a read-input can not challenge a write-spending.

Overall I don’t see the need for a special challenge period for `fulfil()`. If the operator includes a double-spend and publishes the block data, his bond can be slashed.

[@mtsalenc](/u/mtsalenc) did I understand your question correctly?

---

**mtsalenc** (2018-10-01):

Yes it helped me. What I missed is that the NST are actually owned by spending conditions (before the withdrawal) and so can only have it’s storage written by it.

Thanks

