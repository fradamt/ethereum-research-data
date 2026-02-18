---
source: magicians
topic_id: 11407
title: EIP-5805 Voting with delegation
author: Amxx
date: "2022-10-20"
category: EIPs
tags: [erc, governance-ercs]
url: https://ethereum-magicians.org/t/eip-5805-voting-with-delegation/11407
views: 2820
likes: 6
posts_count: 7
---

# EIP-5805 Voting with delegation

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5805)














####


      `master` ← `Amxx:vote_with_delegation`




          opened 10:30AM - 20 Oct 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/25ecfec94e89e81e1553723f9a30aef27c4e1627.jpeg)
            Amxx](https://github.com/Amxx)



          [+406
            -0](https://github.com/ethereum/EIPs/pull/5805/files)

## Replies

**crazyrabbitLTC** (2023-01-09):

Excited to see this get in! Very important for onchain DAOs!

---

**frangio** (2023-01-12):

The current version of the EIP doesn’t give sufficient information to determine what kind of clock is being used. `clock()` returns the *current* timepoint, but more than that is necessary for basic tasks like measuring spans of time, which users have to do when configuring Governor parameters like voting period.

Two examples that could be useful to consider are timestamps with lower granularity:

```auto
function clock1() returns (uint) {
    return (block.timestamp / 1000) * 1000;
}
```

```auto
function clock2() returns (uint) {
    return block.timestamp / 1000;
}
```

The first one is interesting because every 1000 seconds it would appear equivalent to `block.timestamp`, but it isn’t exactly that and in some cases the difference might lead to errors. The second one doesn’t present the same potential for confusion, but a user or an application wouldn’t know (unless they inspect the source code) how to measure a span of time in this clock.

The EIP should define a standard way to identify the clock function. This is difficult because we are allowing arbitrary monotonic functions, but I think we will agree that the user needs to know more properties about the clock than that. The simplest thing would be to add a function returning an enum with options a) block number, b) timestamp, and c) other. The two examples above would be classified as “other”, so if we think it’s valuable to express those we will need something more complex.

---

Another thing that I would consider is defining timepoints as 64 bit values, and making `uint64` the return type of `clock()`. This would allow timepoints to be be packed in storage, otherwise we can make no assumptions about their size. Timepoints as large as `uint256` have way too much granularity that will never be needed.

---

**xinbenlv** (2023-01-12):

I’d rather do none of these `/1000` conversions and just return raw value and leaving the conversion to caller.

```auto
function clock() returns (uint) {
    return block.timestamp;
}
```

---

In addition, from a standardization scoping perspective, I think the representation of time shall be solved in a separate EIP, something like

# EIP-XXX Time Scheme

## Specification

```auto
enum TimeSchemeOption {
  blocknum = 0;
  timestamp = 1;
};

interface ERCTimeScheme {
  function defaultTimeScheme() external pure returns(TimeSchemeOption);
}
```

## Ref Impl

```auto
contract Foo is ERCTimeScheme, ERC1202, ERC5805, ERC5732 {
    function defaultTimeScheme() external pure returns(TimeSchemeOption) {
      return TimeSchemeOption.blocknum;
   }
}
```

This help ensuring whenever a time is being used, the scheme is acquirable and shall be consistent across different functions.

Complying contracts of [EIP-1202](https://eips.ethereum.org/EIPS/eip-1202) probably need to align with the same sense of time too. The [ERC-5007: Time NFT, ERC-721 Time Extension](https://eips.ethereum.org/EIPS/eip-5007) however choose to use int64 for unix stamp.

(posted as [EIP-XXX Time Scheme](https://ethereum-magicians.org/t/eip-xxx-time-scheme/12545) to see if there is interest to consolidate)

---

**frangio** (2023-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I’d rather do none of these /1000 conversions and just return raw value and leaving the conversion to caller.

The EIP as currently written allows arbitrary monotic functions for the clock, so I was giving examples that are valid according to the spec.

---

**deluca-mike** (2023-07-20):

What is the rationale to emit the old and new weight in the `DelegateVotesChanged` event, when this is inconsistent with `ERC20`-styled `Transfer` events that simply emit the delta (the amount that was moved), so that indexers can, if they so choose, rebuild state from events. The requirement to fetch the previous power and new power (after other contract functions manipulated, in some more complex vote token contract, for example) is cumbersome and can result in inefficiencies (extra SLOADS, even if hot/warm). These inefficiencies can instead be pushed onto off-chain systems (indexers, front ends, etc) that can parse events.

It seems to be of popular opinion that events should emit what occurred (i.e. 5 points of voting power was moved from alice to bob), and not what the state was and became (i.e. alice started with 10 points of voting power and ended up with 5 points of voting power, and, bob started with 100 points of voting power and ended up with 105 points of voting power). There is a lot of waste here, and is especially inconsistent when a token mixes `ERC20` `transfer` events and `EIP5805` `DelegateVotesChanged` events.

I’d recommend either doing away with both `DelegateChanged ` and `DelegateVotesChanged ` in favour of:

```plaintext
event Delegation(address indexed delegator, address indexed fromDelegate, address indexed toDelegate, uint256 amount);
```

which allows indexers to watch fewer events, and yet still infer all the same information.

Another option, albeit less optimal, is replacing `DelegateVotesChanged` with:

```plaintext
event DelegateVotesIncreased(address indexed delegate, uint256 amount);
event DelegateVotesDecreased(address indexed delegate, uint256 amount);
```

And, while in the same vein, but much less of an issue, `delegateBySig` takes `nonce` as an argument (such that the signer will be recovered), while `ERC20Permit`’s `permit` takes `owner` as an argument (such that the nonce is fetched and used from storage, and the recovered signer is compared to the owner). To be clear, the proposed `delegateBySig` here is a **better** solution than `ERC20Permit`’s `permit`, where `owner` is redundantly included in the digest, despite being recovered, requiring an unnecessary check that the recovered signer matches the owner argument (and that it is not zero). I am just curious on the rationale behind deviating from what is, fortunately or unfortunately, already adopted.

---

**frangio** (2023-08-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/deluca-mike/48/2957_2.png) deluca-mike:

> I’d recommend either doing away with both DelegateChanged  and DelegateVotesChanged  in favour of:
>
>
>
> ```auto
> event Delegation(address indexed delegator, address indexed fromDelegate, address indexed toDelegate, uint256 amount);
> ```
>
>
>
> which allows indexers to watch fewer events, and yet still infer all the same information.

If I was redesigning the interface today, I would definitely prefer this.

The explanation why the spec looks like this is mainly that we took the interface from the Comp token, which was already being forked by many projects, and implemented it in OpenZeppelin Contracts.



      [github.com](https://github.com/compound-finance/compound-protocol/blob/a3214f67b73310d547e00fc578e8355911c9d376/contracts/Governance/Comp.sol#L51)





####



```sol


1. /// @notice The EIP-712 typehash for the delegation struct used by the contract
2. bytes32 public constant DELEGATION_TYPEHASH = keccak256("Delegation(address delegatee,uint256 nonce,uint256 expiry)");
3.
4. /// @notice A record of states for signing / validating signatures
5. mapping (address => uint) public nonces;
6.
7. /// @notice An event thats emitted when an account changes its delegate
8. event DelegateChanged(address indexed delegator, address indexed fromDelegate, address indexed toDelegate);
9.
10. /// @notice An event thats emitted when a delegate account's vote balance changes
11. event DelegateVotesChanged(address indexed delegate, uint previousBalance, uint newBalance);
12.
13. /// @notice The standard EIP-20 transfer event
14. event Transfer(address indexed from, address indexed to, uint256 amount);
15.
16. /// @notice The standard EIP-20 approval event
17. event Approval(address indexed owner, address indexed spender, uint256 amount);
18.
19. /**
20. * @notice Construct a new Comp token
21. * @param account The initial account to grant all the tokens


```










Only later once we added support for timestamps we documented it in this EIP. If we want to change it at this point it’s a much larger conversation unfortunately. Not impossible but probably better done as a new EIP.

---

I actually prefer permit’s approach to specify the signer as an explicit argument, and keep the nonce implicit. A side effect of the opposite approach taken by `delegateBySig` is that you can generate a random signature and submit it, resulting in getting a random account to delegate to you (or some other account). There is no serious consequence because there’s negligible probability that the random account will have any voting power, but I prefer the permit approach where it is much harder to generate a valid signature.

