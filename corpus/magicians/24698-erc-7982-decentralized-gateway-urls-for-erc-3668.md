---
source: magicians
topic_id: 24698
title: "ERC-7982: Decentralized Gateway URLs for ERC-3668"
author: 0xc0de4c0ffee
date: "2025-06-30"
category: ERCs
tags: [erc, evm, dweb]
url: https://ethereum-magicians.org/t/erc-7982-decentralized-gateway-urls-for-erc-3668/24698
views: 236
likes: 9
posts_count: 5
---

# ERC-7982: Decentralized Gateway URLs for ERC-3668

## Summary

Extends ERC-3668 (CCIP-Read) to support decentralized storage protocols (IPFS, IPNS, Arweave, Swarm) and ERC-4804 Web3 URLs in gateway arrays.

## Key Features

- Multi-protocol support beyond HTTPS
- Backward compatible with fallback to existing ERC-3668 https gateways
- Minimal extension, no core protocol changes

## Use Cases

- ENS resolution using L2/decentralized storage
- Cross-chain queries via Web3 URLs

## Tech Highlights

- ipfs://, ipns://, ar://, bzz://, web3:// support
- Same fallback behavior as ERC-3668

## Benefits

- Censorship resistance through decentralized sources
- Cost efficiency via cheaper storage
- L2 integration via Web3 URLs

PR link : [Add ERC: Decentralized Gateway URLs for ERC-3668 by 0xc0de4c0ffee · Pull Request #1110 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1110)

## Replies

**taytems** (2025-07-08):

Verification is briefly mentioned in the spec, but I don’t think this can take the same approach to verification that ERC-3668 does. 3668 allows any specific contract/gateway implementation to implement their own application-specific verification mechanism, which works fine because the developer controls both the contract code and gateway code. However, a contract utilising this spec doesn’t control the gateway code, and thus it seems verification can’t be done in some cases (?) with a gateway just returning `{"data": "0x..."}`, or the raw bytes for ERC-4804 calls.

For decentralised storage, validating an IPNS record requires more than just the returned value. I assume that’s the case for ARNS as well. 4804 calls would require more than just the returned value, but those requirements would also depend entirely on the requested chain.

You could specify the required data/format for storage protocols that can’t just be verified from the response data, but that would complicate client implementation and go against this spec being a “minimal extension”. Additionally, I don’t think it’s practical to maintain how each individual 4804 call must be verified for each chain, particularly when considering that those details tend to change with time, and changes would need to be updated on contracts **and** clients.

3668’s biggest strength is the high availability in clients. Significant extra complexity in implementation might mean this spec doesn’t inherit that, which would essentially defeat it’s entire purpose. So to ensure high client availability, I’d suggest removing protocols that can’t be verified with response data.

---

**2color** (2025-07-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/f07891/48.png) taytems:

> For decentralised storage, validating an IPNS record requires more than just the returned value.

The IPNS record and the name which contains the public key (`k51qzi5uqu5dmft2itttwwg6s52y8ben2ny06lqh0mrdlap0bk9o67rfyrehmq`) are enough to verify the integrity . You can also add the public key to the record, such that it’s fully self verifying.

---

**0xc0de4c0ffee** (2025-07-09):

![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)  [@taytems](/u/taytems) thanks for reviewing this ERC.

Current HTTP based CCIP gateways assume that all records are signed by gateway manager for verification. Most CCIP gateways only have 1 server without fallback… ERC-3668 isn’t strict about if/how we verify those results in callback, so I’m skipping that part in this ERC too…

Here’s our old `ccip2.eth` resolver using hardcoded public IPFS gateways for CCIP, it’s storing ENS domain manager’s signature OR their permit for a deterministic ephemeral keys to sign records. Permit+deterministic keys were added for better UX, instead of requesting user wallet to sign each ENS records we use one time permit from manager and let that ephemeral key sign everything in background.



      [github.com/namesys-eth/ccip2-eth-resolver](https://github.com/namesys-eth/ccip2-eth-resolver/blob/1588d1f781773faf661ffaab488b9d680dd9b764/src/CCIP2ETH.sol#L440C5-L473C6)





####

  [1588d1f78](https://github.com/namesys-eth/ccip2-eth-resolver/blob/1588d1f781773faf661ffaab488b9d680dd9b764/src/CCIP2ETH.sol#L440C5-L473C6)



```sol


1. /**
2. * @dev Checks for manager access to an ENS domain for record management
3. * @param _owner - Owner of ENS domain
4. * @param _approvedSigner - Manager address to check
5. * @param _node - Namehash of ENS domain
6. * @param _signature - Signature to verify
7. * @param _domain - String-formatted ENS domain
8. * @return  - Whether manager is approved by the owner
9. */
10. function approvedSigner(
11. address _owner,
12. address _approvedSigner,
13. bytes32 _node,
14. bytes memory _signature,
15. string memory _domain
16. ) public view returns (bool) {
17. address _signer = iCCIP2ETH(this).getSigner(
18. string.concat(
19. "Requesting Signature To Approve ENS Records Signer\n",
20. "\nOrigin: ",


```

  This file has been truncated. [show original](https://github.com/namesys-eth/ccip2-eth-resolver/blob/1588d1f781773faf661ffaab488b9d680dd9b764/src/CCIP2ETH.sol#L440C5-L473C6)










With such setup ENS owners only have to pay for one time for switching resolver and initial cid hash setup, & then they can update their signed records in IPNS 100% gasless/offchain… OR use IPFS storage directly with many records for their domains and subdomains in same CID storage and it only takes one TX to update everything.

Internally we used two types of records called `ownerhash` managing multiple sub/domains in same storage, and `recordhash` managing single ENS domain in IPFS/IPNS hash. Recordhash can be extended with extra feature such that, if wildcard resolve request is for `contenthash` return IPFS hash directly for `/<cid-hash>/index.html`, else CCIP read signed records from `/<cid-hash>/.well-known/eth/<domain>/<request type/record>.json` with `{"data":"0x..."}` result stored in same contenthash.

Verifiable IPFS gateways and local Helia/js IPFS clients can be used to add extra verification layer, but it’s out of scope for this ERC as it’s more specific to whole IPFS protocols specs.

For 4804 `web3://` verification, we can store same ENS domain manager’s permit/signed data over L2 (it’s cheap), or wait for easier and faster state/storage proofs directly using L2 RPCs (err, i forgot those new ERCs)… but basically we’re down to “if we can trust those L2 RPC endpoints”, and same can be said for L1 RPC endpoints used by any clients in first place.

Hope this makes it more clear on verification side, outside of ENS I’m trying to use this for superchain-erc20 bridges & singleton 6909 tokens spread over multiple chains. Also, i’m in touch with Arweave team as their gateways are more decentralized+incentivized but still lacks proper 4xx/5xx errors required to trigger 3668 fallbacks.

---

**talentlessguy** (2025-10-16):

How are the values set? Where is an ipfs URL being set? just returned by a resolver?

