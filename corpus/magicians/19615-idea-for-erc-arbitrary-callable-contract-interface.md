---
source: magicians
topic_id: 19615
title: "IDEA for ERC: arbitrary callable contract interface"
author: zergity
date: "2024-04-11"
category: ERCs
tags: [erc, token-approval]
url: https://ethereum-magicians.org/t/idea-for-erc-arbitrary-callable-contract-interface/19615
views: 354
likes: 0
posts_count: 1
---

# IDEA for ERC: arbitrary callable contract interface

> On Wednesday, 28th of February, Seneca’s Chamber contracts, previously audited by Halborn Security, were affected by a bug approval and users’ funds were compromised. In the attack, Seneca’s Chamber.sol contract was implicated. The attacker exploited Chamber’s performOperations() function, allowing calls to functions in other contracts, and directed a call to .transferFrom() , using the Chamber contracts to send tokens to their address.

https://mirror.xyz/0x289D0033d536eb3Ff53367f0A8CceA00d4Ac63a0/_VPi_1T8CWsnQctOA4Z8WS8jKc2B6lIV0hPcQ2Kb-c4

> The lack of input validation on the contract is still present, but through the blacklist blockage of _transferFrom functions of deposits assets it is now possible to repay debt and withdraw collateral.

Arbitrary calls are often discouraged by Security Audit firms, but in my opinion, they should be properly encouraged with better design, as they represent the trustless nature of smart contract design. If a contract only trusts (or distrusts) certain other contracts, those trusted contracts could become attack vectors, while still limiting the functionality of the applications.

Blacklisting the `transferFrom()` function is also not a comprehensive solution, as it overlooks all other *transfer-from* functions from other token standards (e.g., 721, 1155, etc.), not to mention other non-standard custom functions created by token developers that protocols like Seneca would never have predicted.

Another approach by ERC-6120 (which is also designed with trust-less arbitrary contract calls) to deal with the attack above is by using a special ERC-165 interface ID `0x61206120` that token contracts MUST NEVER implement. This way, ERC-6120 (while holding all user token approval) can support arbitrary contract calls without exposing itself to the `transferFrom` attack. This is based on the fact that legacy and future token contracts would never implement the `0x61206120` interface ID, and any other non-token contract can implement it as needed.

The interface ID checking works as intended, but it isn’t perfect. Unlike other ERC-165 interfaces, arbitrary calls emphasize the absence of an interface instead of its presence. Therefore, there’s a risk that a token contract could accidentally signal support for such an interface ID (like 0x61206120) without being aware of the risk.

I propose using a function with an explicit name and text message to directly warn token developers and auditors. Then, contracts with support for arbitrary calls can verify the absence of the function in ERC-165 style.

```solidity
abstract contract NotToken  {
    function isNotToken() external pure returns (bytes32) {
        return "THIS CONTRACT IS NOT A TOKEN";
    }
}
```

As described by the contract name, function, and literal text, token contracts should never implement it. Any non-token contracts that allow arbitrary calls can implement this function to signal their support.

What do you think of the proposal? Please discuss and give comments.
