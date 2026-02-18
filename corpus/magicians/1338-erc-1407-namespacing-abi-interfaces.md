---
source: magicians
topic_id: 1338
title: "ERC 1407 : Namespacing ABI interfaces"
author: wighawag
date: "2018-09-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-1407-namespacing-abi-interfaces/1338
views: 974
likes: 1
posts_count: 6
---

# ERC 1407 : Namespacing ABI interfaces

Hi there,

I created an ERC for namespacing function and events ABI so otherwise conflicting function signatures from different contract interface standard could coexist in one smart contract

Would love to get feedback so we can move that forward and implement it in solidity / vyper …

from : https://github.com/ethereum/EIPs/issues/1407

# Namespacing ABI interface

# Abstract

Currently function and event ABI are entirely defined with their name and type signature.

It would be great to include an extra data to allow namespacing the interfaces.

Solidity and other smart contract languages could add the possibility to annotate function to use different namespace so a contract is not required to support only one namespace.

The default one could be the empty namespace ‘’ for backward compatibility. Or alternatively every new contract would need to declare the default namespace for all functions (the default could be the contract name). Then annotations could be used to specify each function namespace if the one desired is different than the default.

# Motivation

This would allow a contract to support multiple conflicting interfaces at the same time.

For example, let say you plan to use an ERC20 token but would like it to be part of the same contract as an ERC721. (this could allow you to avoid calling external contract to transfer balances for example). When the contract is used as an ERC20 “balanceOf” would return the balance of the ERC20 token represented by that contract and when used as an ERC721 it would return how many NFT you own. The namespacing would simply result in different ABI, so even though the function has the same signature, both can be used.

Currently this is not possible (and won’t be for this particular case even after this EIP get implemented in smart contract languages since the ERC721 and ERC20 ABI has already been decided) but as more smart contract interface standards come into being, the likeliness of interface conflict will increase. The usefulness of combining two conflicting interfaces into one contract will probably rise too.

# Potential Specification

Here is a potential way to achieve that in solidity.

Suggestion are more than welcome. The idea behind creating that issue to find a sensible specification for solving that problem elegantly.

```auto
contract ERC721 {
  function totalSupply() public view returns (uint256) { // use default namespace, that of the Contract Name
  ....
  }

  function balanceOf(address who) public view returns (uint256){

  }

  function test() {
     this.balanceOf(msg.sender);
     this.@ERC20.balanceOf(msg.sender); // could be a way to access namespaced function
  }

  @namespace('ERC20') function totalSupply() public view returns (uint256) { // use namespace ERC20
  ....
  }
  @namespace('ERC20') function balanceOf(address who) public view returns (uint256){

  }

  @namespace('ERC20')  event Transfer(address indexed from, address indexed to, uint256 value);
  event Transfer(address indexed from, address indexed to, uint256 value);
}
```

The ABI for each function could then be

`sha3("<namespace><canonical function signature>")`

instead of

`sha3("<canonical function signature>)"`

## Replies

**Ethernian** (2018-09-23):

Effectively you are suggesting to extend an ERC20 interface by custom methods.

For ERC20 it doesn’t helps any more because the standard is deployed and can’t be changed any more without creating a mess. So it makes sense only for future interface standards.

How a call to such ambiguous function should look like?

```auto
target.erc20transfer(...)
//vs.
target.nft20transfer(...)
```

---

**wighawag** (2018-09-28):

Hi [@Ethernian](/u/ethernian)

As mentioned in the issue I am aware this won;t be applicable to ERC20/ERC721 but for future one it could help us create standard that can be mixed freely. More importantly it allow standard to be created without fear of being incompatible with future standard.

As for how to call it, it would depend on how we implement the namespacing in the resulting ABI.

If we use a simple prefix compatible with solidity syntax. We can do as you say, just prefixing the call. And as such every call will be in the empty namespace.

Alternatively, especially if the encoding rely on a special symbol (not accepted in solidity for function names like @), we could have a special syntax for namespace call like:

```
target.erc20@transfer
```

---

**tjayrush** (2018-09-28):

C++ went through this exact discussion (adding namespaces) back in the 1990s. I would suggest strongly, that whatever direction this idea takes (and I think it’s a good idea), that you carefully study the discussion from that time. I would think that many of the considerations were well discussed. One thing I notice in the above ‘possible specification’ is that the namespace declaration is per-function. That seems a bit error-prone to me. A surrounding code block (such as C++ does)

```
namespace ERC20 {
   // un-altered code here
}
```

also seems possible.

---

**wighawag** (2018-09-28):

Hi [@tjayrush](/u/tjayrush)

Thanks for your feedback. Back of my mind was actually thinking of c++ namespace and other languages. My proposal was not very clear but yes the idea of function specific namespace was for when you want to override the global one and not as the general use. I updated the github issue actually as it was not clear for others there too.

I was thinking the global namespace could be the name of the contract by default or the programming language could force the use of namespace declaration.

Such declaration could well be like you suggest.

Note that the calling of other contract functions is likely to happen cross namespace and a nice looking syntax for it would be welcome.

---

**tjayrush** (2018-09-28):

Namespaces would be very useful in my work, so I support this idea. Hi Ronan.

