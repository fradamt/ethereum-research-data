---
source: magicians
topic_id: 24761
title: "ERC‑TBD: Minimal Avatar Smart Wallet (MASW) – delegate wallet for EIP‑7702"
author: Mostafas
date: "2025-07-08"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-tbd-minimal-avatar-smart-wallet-masw-delegate-wallet-for-eip-7702/24761
views: 179
likes: 1
posts_count: 6
---

# ERC‑TBD: Minimal Avatar Smart Wallet (MASW) – delegate wallet for EIP‑7702

**Toward a “default” delegate wallet under EIP‑7702**

EIP‑7702 lets an EOA point to on‑chain contract code that runs on every future transaction until the user swaps it out with another 0x04. That’s powerful, but if each wallet ships a different delegate implementation we fragment relayers, dApps and audit tooling.

I’m circulating a candidate baseline—Minimal Avatar Smart Wallet (MASW)—for feedback before submitting an ERC. Below is the condensed tech spec repo [GitHub - MostafaS/MASW: Minimal Avatar Smart Wallet](https://github.com/MostafaS/MASW).

---

### MASW at a glance

| Aspect | Design choice |
| --- | --- |
| Core function | executeBatch(targets[arr ], values[ arr], calldatas [arr], token, fee, expiry, signature) |
| Fee model | Relayer reimbursed inside the call (ETH or ERC‑20) |
| Replay guard | Global metaNonce + expiry + chain‑bound EIP‑712 domain separator |
| Extensibility | Exactly two plug‑ins: |
| • PolicyModule – pre/post guards (spend caps, blacklists, etc.) |  |
| • RecoveryModule – ERC‑1271 guardian/social‑recovery signatures |  |
| Upgradability | None: byte‑code is immutable; user changes behaviour via another 0x04 |
| Security bits | Re‑entrancy guard, OZ‑style ERC‑20 return check, NFT receivers built‑in |

Quick technical spec

```auto
// EIP‑712 type hash
BATCH_TYPEHASH = keccak256(
  "Batch(address[] targets,uint256[] values,bytes[] calldatas,address token,uint256 fee,uint256 exp,uint256 metaNonce)"
);

// Domain separator binds (name="MASW", version="1", chainId, owner)
DOMAIN = keccak256(EIP712Domain(...));

// Storage slots
0: metaNonce
1: _entered  (re‑entrancy flag)
2: policyModule
3: recoveryModule
immutables: owner, DOMAIN
```

Execution flow

1. Check arrays match length > 0; block.timestamp <= expiry.
2. Verify EIP‑712 signature → owner or recoveryModule.
3. Increment metaNonce (prevents grief replay).
4. If policyModule != 0, run preCheck.
5. Loop through (targets[i].call{value:values[i]}(calldatas[i])); revert on first failure.
6. Run postCheck (same semantics).
7. Pay relayer:
token == 0 → native transfer; else ERC‑20 transfer.
8. Emit BatchExecuted(structHash).

Interfaces:

```auto
interface IPolicyModule {
  function preCheck (address sender, bytes calldata) external view returns (bool);
  function postCheck(address sender, bytes calldata) external view returns (bool);
}

interface IRecoveryModule {
  function isValidSignature(bytes32 hash, bytes calldata sig) external view returns (bytes4);
}
```

Hashing helpers use `keccak256(abi.encodePacked(arr))`, matching `ethers.js` packed‑array encoding—signatures generated off‑chain verify on‑chain without friction.

**What MASW is not**

- Intent resolver – unlike ERC‑7806, MASW runs exactly what the user signed, no relayer path‑finding.
- Runtime introspection standard – the delegate itself doesn’t expose a callContext7702() view; that could live in a PolicyModule if the ecosystem agrees it’s useful.
- Upgrade‑by‑delegatecall – deliberate omission to minimise audit surface; changing logic means pointing to a new code hash

**If the design survives scrutiny here I’ll submit the ERC PR. Tear it apart—edge cases, prior art, gas tricks all welcome. Thanks!** ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15)

## Replies

**rmeissner** (2025-07-10):

Interested to understand why this proposal is not following any of the existing modular standards (ERC-7579 or ERC-6900) rather introducing another standard, which goes against the motivation to battle fragmentation.

---

**Mostafas** (2025-07-10):

Good point! MASW targets the Pectra‑era **EIP‑7702** flow, where any EOA can run delegate‑code directly—no 4337 entry‑point, bundler or extra infra. ERC‑7579 and ERC‑6900 are hard‑wired to 4337 smart‑contract accounts, so they don’t easily slot into 7702 wallets.

MASW just suggests a tiny default wallet interface for 7702. we can absolutely revisit a unified modular spec once the 7702 ecosystem matures, but dropping 7579/6900 in as‑is is technically tricky. the upside though: MASW can evolve painlessly—just deploy a new contract and call `0x04`. most wallet needs are covered today by current design, and edge‑cases can be added as needed.

---

**rmeissner** (2025-07-10):

I can understand the rational related to the 4337 logic. For me the more important part would be compatibility of hooks and modules. Your proposed “check” use a different format and therefore 7579 validators could not be used. Aligning with hooks and modules from 7579 could allow for reuse of components.

---

**Mostafas** (2025-07-10):

fair point.

both “preCheck” and “postCheck” are also implemented in the `IERC7579Hook` interface, the parameters MASW propose for the policy aggregator interface, does not include the value as in the `preCheck ` in the `IERC7579Hook` which i’ve missed (appreciate pointing this out) . by adding that MASW will be following the same suggested implementation on `IERC7579Hook`. but the `postCheck` interface in the `IERC7579Hook` should also have the same params as the `preCheck` to handle cases where actual effects of the batch of transactions should be evaluated after all of them are done, which we can unify the param and outputs on both pre & post check functions and make it more versatile.

---

**Mostafas** (2025-08-19):

I’ve updated the MASW implementation to address this:

- Added a ‘value’ parameter to preCheck to enable hook reuse and reduce fragmentation.
- Unified the parameter sets for preCheck and postCheck to align better with modular standards.

You can see the changes here: [ERCs/assets/erc-7988/MASW.sol at masw-erc · MostafaS/ERCs · GitHub](https://github.com/MostafaS/ERCs/blob/masw-erc/assets/erc-7988/MASW.sol).

Does this resolve the concerns? Open to further suggestions— [@rmeissner](/u/rmeissner) , thoughts?

