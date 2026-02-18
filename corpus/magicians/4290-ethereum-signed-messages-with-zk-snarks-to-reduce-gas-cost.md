---
source: magicians
topic_id: 4290
title: Ethereum Signed Messages with ZK-Snarks to reduce gas cost?
author: 3esmit
date: "2020-05-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/ethereum-signed-messages-with-zk-snarks-to-reduce-gas-cost/4290
views: 812
likes: 1
posts_count: 3
---

# Ethereum Signed Messages with ZK-Snarks to reduce gas cost?

I’ve looked into Tornado Cash smart contracts and it looks like it could be optimized with Ethereum signed messages.

Currently the Withdraw function, https://github.com/tornadocash/tornado-core/blob/a533ad9ffb62163a42d4fa9a09984c5dd4e5c41d/contracts/Tornado.sol#L87, verify all parameters against the ZK-proof.

In the circuit we can see that all this parameters are only multiplied with themselves to proof that who knows the commitment is who is choosing these parameters:


      [github.com](https://github.com/tornadocash/tornado-core/blob/a533ad9ffb62163a42d4fa9a09984c5dd4e5c41d/circuits/withdraw.circom#L33-L35)




####

```circom

1. signal input relayer;  // not taking part in any computations
2. signal input fee;      // not taking part in any computations
3. signal input refund;   // not taking part in any computations

```








I see is not a big problem to introduce parameters in a circuit this way, however is that really necessary, if the parameters are not part of the computation why they have to be part of the proof?

The exit (recipient) address is public anyway, so why not use a signed message coming from this address with those parameters?

Wouldn’t this be more efficient, as ethereum signed messages are less gas intensive than passing all parameters inside ZK-Snarks?

As example for:


      [github.com](https://github.com/tornadocash/tornado-core/blob/a533ad9ffb62163a42d4fa9a09984c5dd4e5c41d/contracts/Tornado.sol#L83-L92)




####

```sol

1. function withdraw(bytes calldata _proof, bytes32 _root, bytes32 _nullifierHash, address payable _recipient, address payable _relayer, uint256 _fee, uint256 _refund) external payable nonReentrant {
2. require(_fee <= denomination, "Fee exceeds transfer value");
3. require(!nullifierHashes[_nullifierHash], "The note has been already spent");
4. require(isKnownRoot(_root), "Cannot find your merkle root"); // Make sure to use a recent one
5. require(verifier.verifyProof(_proof, [uint256(_root), uint256(_nullifierHash), uint256(_recipient), uint256(_relayer), _fee, _refund]), "Invalid withdraw proof");
6.
7. nullifierHashes[_nullifierHash] = true;
8. _processWithdraw(_recipient, _relayer, _fee, _refund);
9. emit Withdrawal(_recipient, _nullifierHash, _relayer, _fee);
10. }

```








Something like this would achieve the same result:

```auto
  function withdraw(bytes calldata _proof, bytes32 _root, bytes32 _nullifierHash, address payable _recipient, address payable _relayer, uint256 _fee, uint256 _refund, bytes calldata _messageSignature) external payable nonReentrant {
    require(_fee <= denomination, "Fee exceeds transfer value");
    require(!nullifierHashes[_nullifierHash], "The note has been already spent");
    require(isKnownRoot(_root), "Cannot find your merkle root"); // Make sure to use a recent one
    require(verifier.verifyProof(_proof, [uint256(_root), uint256(_nullifierHash), uint256(_recipient)]), "Invalid withdraw proof");
    require(
        _recipient == recoverAddress(getSignHash(keccak256(abi.encodePacked(_proof, _relayer, _fee, _refund)), _messageSignature)),
        "Invalid signature"
    );

    nullifierHashes[_nullifierHash] = true;
    _processWithdraw(_recipient, _relayer, _fee, _refund);
    emit Withdrawal(_recipient, _nullifierHash, _relayer, _fee);
  }
```

A valid downside is that _recipient would have to be an externally owned account, however if we need to use it as a smart contract, than we could use a temporary key that would decide all the parameters.

This technique could also be used for supporting function with lots of parameters, as the zk-proof would be trimmed and the rest of the parameters could be passed in a second transaction.

What are your thoughts on this? This is would be indeed more efficient? Where else this could be used?

## Replies

**Amxx** (2020-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/3esmit/48/2255_2.png) 3esmit:

> A valid downside is that _recipient would have to be an externally owned account, however if we need to use it as a smart contract, than we could use a temporary key that would decide all the parameters.

I believe this is the real issue. I want to be able deposit/withdraw from tornado using Argent or Gnosis accounts. Withdrawing to a disposable EOA, and then transfering from the EOA to the account really downgrades the UX. ZK rollups & account abstraction are two awesome things that should be compatible

---

**3esmit** (2020-05-15):

> Withdrawing to a disposable EOA, and then transfering from the EOA to the account really downgrades the UX.

It don’t have to degrade the UX, this can be done under the hood without user having to know about it. For example:

1. The secret itself could be hashed to become this “temporary private key” which would sign the message that specify the parameters. The Dapp could implement this as part of the “proof generator” and it would work in any web3 browser.
2. The wallet could provide “disposable deterministic wallets” for this purpose through the BIP39 tree, however this would have to become a standard for all web3 browsers.

Note that funds don’t have to go first to the “disposable address”, the “disposable address” could itself define the recipient.

E.g.:

```auto
  function withdraw(bytes calldata _proof, bytes32 _root, bytes32 _nullifierHash, address payable _disposableWallet, address payable _recipient, address payable _relayer, uint256 _fee, uint256 _refund, bytes calldata _messageSignature) external payable nonReentrant {
    require(_fee <= denomination, "Fee exceeds transfer value");
    require(!nullifierHashes[_nullifierHash], "The note has been already spent");
    require(isKnownRoot(_root), "Cannot find your merkle root"); // Make sure to use a recent one
    require(verifier.verifyProof(_proof, [uint256(_root), uint256(_nullifierHash), uint256(_recipient)]), "Invalid withdraw proof");
    require(
        _disposableWallet == recoverAddress(getSignHash(keccak256(abi.encodePacked(_proof, _recipient, _relayer, _fee, _refund)), _messageSignature)),
        "Invalid signature"
    );

    nullifierHashes[_nullifierHash] = true;
    _processWithdraw(_recipient, _relayer, _fee, _refund);
    emit Withdrawal(_recipient, _nullifierHash, _relayer, _fee);
  }
```

