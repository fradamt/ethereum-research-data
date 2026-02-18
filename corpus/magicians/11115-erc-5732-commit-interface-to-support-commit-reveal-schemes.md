---
source: magicians
topic_id: 11115
title: ERC-5732 Commit Interface to support commit-reveal schemes
author: xinbenlv
date: "2022-09-29"
category: EIPs
tags: [erc-721, erc-20, erc1155, erc1202]
url: https://ethereum-magicians.org/t/erc-5732-commit-interface-to-support-commit-reveal-schemes/11115
views: 2732
likes: 1
posts_count: 12
---

# ERC-5732 Commit Interface to support commit-reveal schemes

Hi all, I am proposing a simple commit interface to support commit-reveal schemes.

See the PR here: [Add EIP-5732: Commit Interface by xinbenlv · Pull Request #5732 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5732)

## Links

1. Current published version: ERC-5732: Commit Interface
2. Pending PRs Pull requests · ethereum/EIPs · GitHub

## Open Questions

1. Will there ever be use-cases where the commit function needs a returns value? If so, how important do we see such use cases
2. How shall we handle when a contract wallet is trying to make a commit? Should we add a address from parameter to the commit interface? How often do we see the use case for a contract wallet to need to commit?

## Replies

**fulldecent** (2022-09-30):

This specification assumes that somebody will want to *consume* this information, in a generic way, across multiple implementations. I’m not seeing that spelled out anywhere. And I haven’t seen evidence of such in the wild.

---

**xinbenlv** (2022-09-30):

[@fulldecent](/u/fulldecent) thank you for the feedback.

I am not sure if I fully understand what you mean. Can you ellaborate?

---

**fulldecent** (2022-09-30):

The purpose of having a standard is that somebody else will want to interact with a contracts following that specification.

For example ERC-20 creates fungible tokens. Other things interact with those tokens for DeFi, reporting, and tracking tools. (Those applications are probably all illegal, but I digress.) Such is a strong motivating factor for ERC-20 to be written up.

If ERC-20 was not written up then DeFi, reporting tools would not be possible or there would be extreme effort required to do them.

I would like to see a similar strong motivation for ERC-5732 to be a candidate for publishing. As such I don’t see this. This topic comes up a lot so I have also published this concept at [What kinds of things should be standardized? – William Entriken Blog](https://blog.phor.net/2022/09/30/What-kinds-of-things-should-be-standardized.html)

---

**xinbenlv** (2022-09-30):

Sure. Here is a real world example and prior use case of a commit-reveal: [The Decentraland DAO explained | Decentraland](https://decentraland.org/blog/announcements/the-decentraland-dao-explained/)

```auto
Remember: You must wrap MANA and/or commit LAND/ESTATE before the proposal’s creation block in order to be allowed to vote. You can’t wrap MANA and vote if voting has already commenced.
```

Here is an other example [GitHub - ConsenSys/PLCRVoting: Partial Lock Commit Reveal Voting System that utilizes ERC20 Tokens](https://github.com/ConsenSys/PLCRVoting)

It can be supported by this standardization.

The main use case is for Commit-Reveal of Voting, but it doesn’t limit to voting. The way to pre-commit a future action can be general. The plan is to use this in combine this EIP with a few other executable trust establishing EIPs such as

[Smart Endorsement](https://eips.ethereum.org/EIPS/eip-5453)

Legitimacy, Jurisdiction and Sovereignty

[Smart Proposal](https://eips.ethereum.org/EIPS/eip-5247)

Plus the main voting standard [EIP-1202: Voting Standard](https://eips.ethereum.org/EIPS/eip-1202)

to create a fully operable on-chain governance

---

**xinbenlv** (2022-10-06):

[@fulldecent](/u/fulldecent)

I was just trying to buy a ENS domain and via the TX just stumble upon the ENS ETHRegistrarController.sol that uses a commit mechanism. To my surprise (or not supprisingly) the ETHRegistrarController happen to use the exact same method name `function commit(bytes32)` that I prose, except for that mine have a extra method.



      [github.com](https://github.com/ensdomains/ethregistrar/blob/916dff21bf427771e67af11611b811f870aa7200/contracts/ETHRegistrarController.sol#L79-82)





####



```sol


1.
2. function makeCommitmentWithConfig(string memory name, address owner, bytes32 secret, address resolver, address addr) pure public returns(bytes32) {
3. bytes32 label = keccak256(bytes(name));
4. if (resolver == address(0) && addr == address(0)) {
5. return keccak256(abi.encodePacked(label, owner, secret));
6. }
7. require(resolver != address(0));
8. return keccak256(abi.encodePacked(label, owner, resolver, addr, secret));
9. }
10.
11. function commit(bytes32 commitment) public {
12. require(commitments[commitment] + maxCommitmentAge < now);
13. commitments[commitment] = now;
14. }
15.
16. function register(string calldata name, address owner, uint duration, bytes32 secret) external payable {
17. registerWithConfig(name, owner, duration, secret, address(0), address(0));
18. }
19.
20. function registerWithConfig(string memory name, address owner, uint duration, bytes32 secret, address resolver, address addr) public payable {
21. bytes32 commitment = makeCommitmentWithConfig(name, owner, secret, resolver, addr);


```










Which is a good justification that someone will want to consume such information, e.g. a competing interface or automating interface will need to send `commit` if they want to register an ENS domain

Here is the list of Ethereum mainnet activity of TX with commit

https://etherscan.io/address/0x283af0b28c62c092c9727f1ee09c02ca627eb7f5?method=Commit~0xf14fcbc8

Inviting [@Arachnid](/u/arachnid) for comment

---

**xinbenlv** (2022-10-26):

There are also two other design questions

1. Will there ever be use-cases where the commit function needs a returns value? If so, how important do we see such use cases
2. How shall we handle when a contract wallet is trying to make a commit? Should we add a address from parameter to the commit interface? How often do we see the use case for a contract wallet to need to commit?

---

**lanlan3322** (2022-10-26):

Kleros (blockchain dispute resolution) might be a good use case for you to consider. Jurors voting for more than binary options might require return value during commit. But it would add security concerns during the handling of the returned value too.

---

**xinbenlv** (2022-11-01):

Happy to hear that. Look forward to collaboration

---

**fulldecent** (2022-11-07):

I have addressed some copy editing issues in [Address some copy editing issues by fulldecent · Pull Request #5890 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5890)

---

There are some serious problems in this DRAFT which need to be addressed to be even a specification.

First, the specification requires that commitments have timestamps which are STRICTLY INCREASING. This means two commits cannot happen in the same block.

The proposed reference implementation does not follow any of the proposed best practices identified in the standard. This is not a reference implementation.

The text states that “Do not use the reference implementation in production”. This is a red flag and means that it is not a reference application. Please produce an actual reference implementation. But you are welcome to say “don’t use the DEMO APPLICATION IN PRODUCTION”. Much better still would be to demonstrate that the author is capable of making something useful with the proposed specification.

`secret_salt` is unspecified.

---

**xinbenlv** (2022-11-08):

Thank you [@fulldecent](/u/fulldecent) for the suggestion and reviewing.

> First, the specification requires that commitments have timestamps which are STRICTLY INCREASING. This means two commits cannot happen in the same block.

This is a great. I addressed it in my comment on your PR, in particular, [Address some copy editing issues by fulldecent · Pull Request #5890 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5890/files#r1017045994)

```auto
The text states that “Do not use the reference implementation in production”. This is a red flag and means that it is not a reference application. Please produce an actual reference implementation. But you are welcome to say “don’t use the DEMO APPLICATION IN PRODUCTION”.
```

I wish to! However Currently EIP editor group enforce a very strict policy and it’s very hard to link to actual implementation from EIP. I’d rather just remove reference implementation in this case. Most solidity code are nowhere near production on ERCs in general and my impression that when I and other ERC authors use “reference implementation” they mean more of proof of concept rather than battle tested code. I do like ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12) your better wording “don’t use the DEMO APPLICATION IN PRODUCTION”.

> secret_salt is unspecified.

There is sentence in the second from last requirement in the spec when talking about reveal function.

> But there MUST be a way to supply an extra field of secret_salt , so that committer can later open the secret_salt in the reveal TX that exposes the secret_salt . The size and location of secret_salt is intentionally unspecified in this EIP to maximize flexibility for integration.

And the reason is articulated in Rationale. We intentionally keep it open.

Again, thank you so much for editing and reviewing, let me know if you have any other unaddressed comments!

---

**xinbenlv** (2022-11-10):

Hi [@fulldecent](/u/fulldecent) thank you for the help. With [PR 5910](https://github.com/ethereum/EIPs/pull/5910) and [PR 5909](https://github.com/ethereum/EIPs/pull/5909)

1. The editorial suggestions are accepted and incorporated.
2. The specification ambiguity about “STRICTLY INCREASING” is clarified.
3. The question that secret_salt is unspecified is clarified
4. The demo reference implementations are removed, the only one left is ENS’s actual implementation.

By now I believe I’ve addressed all your feedbacks. Thank you very much!

For you and everyone else, please let me know if there are any other suggestions / feedback for this EIP before we finalize it

