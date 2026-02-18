---
source: ethresearch
topic_id: 335
title: Validation code for abstraction
author: vbuterin
date: "2017-12-17"
category: Sharding
tags: []
url: https://ethresear.ch/t/validation-code-for-abstraction/335
views: 1825
likes: 3
posts_count: 9
---

# Validation code for abstraction

```auto
# Expects transaction data to be formatted as:
# 0-95: sig
# 96-127: nonce
# 128-159: gasprice
# 160-191: value
# 192-223: to
# 224+: data
['seq',
    # Memory: 32...127 = sig, 128... = other data
    ['calldatacopy', 96, 32, ['sub', ['calldatasize'], 96]],
    # Load txgas to the end of data
    ['mstore', ['txgas'], 'msize'],
    # Compute sighash = sha3(nonce ++ gasprice ++ value ++ to ++ data ++ txgas
    ['mstore', ['sha3', 128, ['sub', 'msize', 128]], 0],
    # Verify signature
    ['call', 3000, 1, 0, 0, 128, 0, 32],
    ['assert', ['eq', ['mload', 0]], ],
    # Verify and increment nonce
    ['assert', ['eq', ['calldataload', 96], ['sload', 0]]],
    ['sstore', ['add', ['sload', 0], 1]],
    # Call PAYGAS
    ['paygas', ['calldataload', 128]],
    # Make the main call
    ['with', 'x', ['calldataload',
                    ['sub', ['gas'], 5000],  # gas
                    ['calldataload', 192],   # to
                    ['calldataload', 160],   # value
                    256,                     # data starts from (in memory)
                    ['sub', ['msize'], 288], # data length (elide last 32 bytes as that's TXGAS)
                    0,
                    0],
        # Propagate return data, and success or failure
        ['seq',
            ['returndatacopy', 0, ['returndatasize']],
            ['if', x, ['return', 0, ['returndatasize']],
                      ['throw', 0, ['returndatasize']]]]]
]
```

## Replies

**jannikluhn** (2017-12-27):

Just for fun and because it’s possible, here’s a Bitcoin-style UTXO validation contract (totally untested of course): https://gist.github.com/jannikluhn/373d5d0eb782feb8b551acf1c165c812

Note that there are no nonces. Instead, executing the same (valid) transaction twice would fail, as the same outputs would be spent (hence, UTXO).

There’s also no PAYGAS. Miners will have to peek into the transaction and check if they are the recipient of enough coins. This is possible in constant time (as is checking how much gas executing the transaction will consume).

Only thing that could happen is that the transaction is invalid (outputs already spent, invalid signatures, etc.). Then the miner would have to do work for which he isn’t rewarded. But this is the case for Bitcoin as well and they seem to be doing fine in this regard.

---

**vbuterin** (2017-12-27):

Nice! I’d say just put a PAYGAS opcode at the very end, and that would make it fit into the same format.

---

**jannikluhn** (2018-01-04):

I’d like to put a couple of additional features up for discussion for the standard validation contract:

- nonce getter: Right now the nonce is inaccessible for other contracts. I think one can at least imagine some usecases in which this would be nice to have, for instance to check that a specific account hasn’t been touched for some amount of time.
 Also, clients need to access the nonce to create new transactions. If there were a standardized getter, they could just use that one, whereas without one they’d need account-specific code to peek into the storage to get it.
 On the other hand, it would make the code more complicated, increase gas costs slightly and it would make assumptions on the contract ABI.
- target block range: Optionally we could add a target block range, outside of which the transaction would be invalid. This would enable transactions which are signed now but only become valid at some point in the future. Also, if users set a maximum block number they could be certain that the transaction won’t be included after some time, for example if they used a too low gas price, whereas now they are just floating around which may feel a bit unpleasant.
 Disadvantages would again be more complexity and gas cost in the contract, and also a larger transaction size.
- generalized precondition checker: Generalizing above point, we could optionally have a generalized precondition check by having transactions specify a contract address and some parameters. The contract would be called before PAYGAS and if it returns an error, the transaction would become invalid. Examples could be above block range checks, but also token balance checks or contract state checks (“is the auction still running?”).
 Arguably, this would be less complex than the target block range check, at least in the base contract. Still, it would use more gas than the original version and some miners might be unwilling to accept such transactions – all these checks could also be done after PAYGAS, but there miners would be paid.

---

**vbuterin** (2018-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Generalizing above point, we could optionally have a generalized precondition check by having transactions specify a contract address and some parameters.

All looks good. The main concern I have with generalized precondition checkers is that if a standard transaction requires calling another contract, that would substantially increase the required witness size (unless you do something fancy like grinding an address that’s very close to the address of the contract). This seems like a complexity gain that’s worth avoiding. Otherwise, the suggestions make sense.

Another thing on my wishlist is a gasprice that goes up over time as the block number increases, allowing easier/safer gasprice optimization for less time sensitive transactions.

---

**jannikluhn** (2018-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The main concern I have with generalized precondition checkers is that if a standard transaction requires calling another contract, that would substantially increase the required witness size

It’s optional, if users don’t think the added costs are worth it they can leave it empty and no call will be made.

> Another thing on my wishlist is a gasprice that goes up over time as the block number increases, allowing easier/safer gasprice optimization for less time sensitive transactions.

Love this idea!

Another one I forgot to mention earlier: A `get_address` method returning the address (corresponding to the private key, not the contract address). Reason is that there are applications that let users sign messages with their private key and subsequently verify against `msg.sender`. This doesn’t work anymore as `msg.sender` will be a contract address, not derived from a private key. With `get_address` (not liking the name very much to be honest) they can continue to do the same thing, albeit with another call to the validation contract.

---

**vbuterin** (2018-01-05):

> get_address method returning the address (corresponding to the private key, not the contract address)

I like this too, though I think we should consider something like `get_validation_code` instead. The reason is that if we want to abstract beyond ECDSA, then it would be nice to have this abstraction extend to message signing too, and so we may as well just reuse Casper’s validation code mechanism.

---

**jannikluhn** (2018-01-05):

Makes sense. I’m not familiar with the Casper code, what exactly would `get_validation_code` do?

Return an address to a contract with a function `validate(message, signature)`? If so, why not have this function directly in the main contract (which of course could call another contract from within)?

---

**vbuterin** (2018-01-06):

The validation code in Casper doesn’t have functions, it just accepts a piece of data, interprets the first 32 bytes as a hash and the rest as a signature, and throws if the signature fails and returns 1 if it passes.

