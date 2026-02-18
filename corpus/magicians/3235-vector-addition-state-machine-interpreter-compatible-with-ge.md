---
source: magicians
topic_id: 3235
title: Vector Addition State Machine interpreter compatible with generalized state channels
author: adklempner
date: "2019-05-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/vector-addition-state-machine-interpreter-compatible-with-generalized-state-channels/3235
views: 1272
likes: 3
posts_count: 4
---

# Vector Addition State Machine interpreter compatible with generalized state channels

I’m experimenting with a novel way to program and run logic in generalized state channels. I’d appreciate any feedback on this idea. Reasons it wouldn’t work, pitfalls to be aware of, whatever the soup is sizzling with ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

https://github.com/adklempner/vasm-cf

## Replies

**boris** (2019-05-02):

This could be interesting to [@johba](/u/johba)

---

**johba** (2019-05-03):

cool stuff,

I’ve been looking into statebox myself for a while, trying to map it to computation in Plasma. What I struggle with is understanding how the state machine can integrate with the underlying ledger assets.

If I understand your setup correctly, then the state machine basically makes decisions about the custody and distributions of assets that have been locked into the state channel initially. But what if some party needs to increase the collateral? Or we need to make a decision based on the genetics of a specific crypto-kitty? Is that possible?

Can you also elaborate why you think Truebit would be useful running VASM? Is this outside of state channels, for contracts with unlimited participants directly on-chain?

---

**adklempner** (2019-05-03):

Hey, great questions!

> What I struggle with is understanding how the state machine can integrate with the underlying ledger assets.
> If I understand your setup correctly, then the state machine basically makes decisions about the custody and distributions of assets that have been locked into the state channel initially.

I think it’s possible to achieve and there’s several ways to go about defining a protocol between the state machine and on-chain resources.

`AppLogic` has a list of indexes like `aliceBalanceIndex` to designate VASM states that are strictly connected to on-chain state.

```auto
struct AppLogic {
    // AppState  AppLogic
    uint256 turnTakerStateIndex;
    uint256 terminalIndex;
    // Ethereum  AppLogic
    uint256 aliceBalanceIndex;
    uint256 bobBalanceIndex;
    // Initial state (before passing in on-chain data)
    int64[] initialPlaces;
    // Transitions
    int64[][MAX_TRANSITIONS] deltas;
  }

AppLogic masterLogic;

constructor(AppLogic _masterLogic) { masterLogic = _masterLogic  }
```

Some of the indexes tell the smart contract where to read data from the machine. Ex: to determine if a terminal state in the machine has been reached, read from `AppState.state[terminalIndex]`

`aliceBalanceIndex` and `bobBalanceIndex` are states in the machine that are “integrated” or “connected” to on-chain assets (in this case state channel deposits). They need to be reliably “loaded” into the machine through the smart contract.

```auto
struct AppState {
    address alice;
    address bob;
    int64[] state;
    AppLogic logic;
  }

// loads the interpreter, called after opening the state channel
loadInterpreter(address alice, address bob) view returns (AppState memory) {
  AppState memory nextState = getInitialState();
  nextState.alice = alice;
  nextState.bob = bob;
  nextState.state[nextState.logic.aliceBalanceIndex] = balanceToInt64(alice);
  nextState.state[nextState.logic.bobBalanceIndex] = balanceToInt64(bob);
  return nextState;
}

// gets initial state from on-chain contract
getInitialState() view returns (AppState memory) {
  return new AppState(0x0,0x0,masterLogic.initialPlaces,masterLogic);
}

// gets account's balance in channel and safely converts to int64
balanceToInt64(address account) view returns (int64);

```

Let’s say Alice opens the channel with 100 DAI. There’s now a place in the machine (`AppState.state[AppState.logic.aliceBalanceIndex]`) with value 100. Alice and Bob send state channel TXs, and when it’s time to `resolve` the channel, the contract reads from that same place to determine what gets sent to Alice and what gets sent to Bob.

```auto
function resolve(bytes calldata encodedState, Transfer.Terms calldata terms)
    external
    pure
    returns (Transfer.Transaction memory)
  {
    AppState memory appState = abi.decode(encodedState, (AppState));
    uint256[] memory amounts = new uint256[](2);
    amounts[0] = uint256(appState.state[uint256(appState.logic.aliceBalanceIndex)]);
    amounts[1] = uint256(appState.state[uint256(appState.logic.bobBalanceIndex)]);

    address[] memory to = new address[](2);
    to[0] = appState.alice;
    to[1] = appState.bob;
    bytes[] memory data = new bytes[](2);

    return Transfer.Transaction(
      terms.assetType,
      terms.token,
      to,
      amounts,
      data
    );
  }
```

Btw, this [resolve](https://specs.counterfactual.com/en/latest/01-app-definition.html#resolution-function) function is the only function that a Counterfactual application *must* implement, which gives a lot of freedom in defining the relationship between the state machine’s logic and the contract’s logic.

> But what if some party needs to increase the collateral? Or we need to make a decision based on the genetics of a specific crypto-kitty? Is that possible?

Yes. This is more difficult to generalize, but basically a transition in the machine would be flagged to require an assertion about the state of the chain/channel to be true in order to fire.

---

I know this might be messy to parse, I’m still figuring out/learning the names for all the pieces involved. I’m preparing some visuals that should make all this easier to explain

