---
source: ethresearch
topic_id: 6064
title: Deterministic ABIs
author: tpmccallum
date: "2019-08-31"
category: Data Structure
tags: []
url: https://ethresear.ch/t/deterministic-abis/6064
views: 2152
likes: 2
posts_count: 5
---

# Deterministic ABIs

I am interested in discussing ABI creation. More specifically the potential to standardize ABI creation to the point where ABIs become deterministic and as such are in a canonical form. Once this is achieved, we can easily perform hashing to create unique handles for ABIs.

**Solidity**

The order of functions in Solidity smart contract source code **does not** have an effect on the order of the items in a Solidity generated ABI.

**Vyper**

In contrast, the position of variables, functions and events in Vyper source code **does** have an effect on the position of the variables, functions and events in the Vyper generated ABI.

**EWASM**

Please comment … ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

There is a more elaborate example of the above (with source code and ABI snippets) [here](https://github.com/second-state/es-ss.js/blob/99853ff11b39fd45aab94e605476c0dd58a01e1e/research_and_development/solidity_vs_vyper/ordering_of_abi_items_relative_to_source_code.md) if you are interested.

What are your views on [reproducible builds](https://en.wikipedia.org/wiki/Reproducible_builds) (deterministic compilation) in the context of Ethereum ABIs? Is it fair to say that deterministic compilation is more to do with the bytecode and less to do with the ABI (being that the ABI is not executable).

I personally see value in having deterministic ABIs because they are the key to storing/organizing and discovering contracts on the network. I am currently using a [web3.toHex(web3.sha3(text=_abi))](https://github.com/second-state/smart-contract-search-engine/blob/2bdc1924a69592216ae3f055383c3bdd4f2cb205/python/harvest.py#L292) approach to create a deterministic ABI hash in canonical form (at present by leaving the top level ABI functions as per the Solidity compiler output, but in addition, by sorting the (natively unsorted) internal objects and lists of objects before creating the hash).

For example, [this web page](https://etc.search.secondstate.io/ethAbi2.html) lets you search for contracts using an ABI as the search query

I noticed (after writing this post) that [@axic](/u/axic) has [a suggestion of deterministically sorting lexicographically by values of keys](https://github.com/ethereum/solidity/issues/2731#issuecomment-411187367). I think this makes sense.

## Replies

**tpmccallum** (2019-09-02):

I have written an ABI sorter, as per the above suggestion.

The code dives in and sorts internal `inputs` and `outputs` and then comes out to sort the higher level surface of the ABI. The multi-level sort order is by `type` then by `name`.

Here is an example using the [Standard ERC20 ABI Text](https://github.com/ethereum/wiki/wiki/Contract-ERC20-ABI)

# Example ERC20 input - unsorted

```auto
[{"constant": true, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_from", "type": "address"}, {"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transferFrom", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"payable": true, "stateMutability": "payable", "type": "fallback"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "owner", "type": "address"}, {"indexed": true, "name": "spender", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "name": "from", "type": "address"}, {"indexed": true, "name": "to", "type": "address"}, {"indexed": false, "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"}]
```

# Example ERC20 output - sorted

```auto
[{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]
```

Here is [a link to the code which performs the sort](https://github.com/second-state/smart-contract-search-engine/blob/3ad0c0393d25598f69aa91363b9d413507b350a5/python/utilities_and_tests/abi_research.py).

I ended up writing this without help from Libraries (aside from `import json`). Partly because we can now transpose the logic of my code [to C++](https://github.com/ethereum/solidity/blob/459aed90e0c9832757848b88af762b21b1a61e57/libsolidity/interface/ABI.cpp#L28) and partly because (as it turns out) Python’s `lambda` and Python’s `itemgetter` did not entertain the absence of the `name` key in the fallback function anyway.

---

**tpmccallum** (2019-09-02):

Here is the pretty version of the sorted ABI

```auto
[{
	"anonymous": false,
	"inputs": [{
		"indexed": true,
		"name": "owner",
		"type": "address"
	}, {
		"indexed": true,
		"name": "spender",
		"type": "address"
	}, {
		"indexed": false,
		"name": "value",
		"type": "uint256"
	}],
	"name": "Approval",
	"type": "event"
}, {
	"anonymous": false,
	"inputs": [{
		"indexed": true,
		"name": "from",
		"type": "address"
	}, {
		"indexed": true,
		"name": "to",
		"type": "address"
	}, {
		"indexed": false,
		"name": "value",
		"type": "uint256"
	}],
	"name": "Transfer",
	"type": "event"
}, {
	"payable": true,
	"stateMutability": "payable",
	"type": "fallback"
}, {
	"constant": true,
	"inputs": [{
		"name": "_owner",
		"type": "address"
	}, {
		"name": "_spender",
		"type": "address"
	}],
	"name": "allowance",
	"outputs": [{
		"name": "",
		"type": "uint256"
	}],
	"payable": false,
	"stateMutability": "view",
	"type": "function"
}, {
	"constant": false,
	"inputs": [{
		"name": "_spender",
		"type": "address"
	}, {
		"name": "_value",
		"type": "uint256"
	}],
	"name": "approve",
	"outputs": [{
		"name": "",
		"type": "bool"
	}],
	"payable": false,
	"stateMutability": "nonpayable",
	"type": "function"
}, {
	"constant": true,
	"inputs": [{
		"name": "_owner",
		"type": "address"
	}],
	"name": "balanceOf",
	"outputs": [{
		"name": "balance",
		"type": "uint256"
	}],
	"payable": false,
	"stateMutability": "view",
	"type": "function"
}, {
	"constant": true,
	"inputs": [],
	"name": "decimals",
	"outputs": [{
		"name": "",
		"type": "uint8"
	}],
	"payable": false,
	"stateMutability": "view",
	"type": "function"
}, {
	"constant": true,
	"inputs": [],
	"name": "name",
	"outputs": [{
		"name": "",
		"type": "string"
	}],
	"payable": false,
	"stateMutability": "view",
	"type": "function"
}, {
	"constant": true,
	"inputs": [],
	"name": "symbol",
	"outputs": [{
		"name": "",
		"type": "string"
	}],
	"payable": false,
	"stateMutability": "view",
	"type": "function"
}, {
	"constant": true,
	"inputs": [],
	"name": "totalSupply",
	"outputs": [{
		"name": "",
		"type": "uint256"
	}],
	"payable": false,
	"stateMutability": "view",
	"type": "function"
}, {
	"constant": false,
	"inputs": [{
		"name": "_to",
		"type": "address"
	}, {
		"name": "_value",
		"type": "uint256"
	}],
	"name": "transfer",
	"outputs": [{
		"name": "",
		"type": "bool"
	}],
	"payable": false,
	"stateMutability": "nonpayable",
	"type": "function"
}, {
	"constant": false,
	"inputs": [{
		"name": "_from",
		"type": "address"
	}, {
		"name": "_to",
		"type": "address"
	}, {
		"name": "_value",
		"type": "uint256"
	}],
	"name": "transferFrom",
	"outputs": [{
		"name": "",
		"type": "bool"
	}],
	"payable": false,
	"stateMutability": "nonpayable",
	"type": "function"
}]
```

---

**tpmccallum** (2019-09-04):

I wrote [a sorting and hashing API which you can try out here](https://etc.search.secondstate.io/shaAnAbi.html).

You can paste [the raw text of any of these unsorted mixed up ERC20 ABIs](https://github.com/tpmccallum/mixed_ordered_erc20_abis_for_testing), or [the official ERC20 ABI from the Ethereum Wiki](https://github.com/ethereum/wiki/wiki/Contract-ERC20-ABI), and the resulting hash (for the official ERC20 ABI) will always be `0xfa9452aa0b9ba0bf6eb59facc534adeb90d977746f96b1c4ab2db01722a2adcb`.

---

**jgm** (2019-09-04):

Be aware that the ABI spec changes from time to time so the same contract will produce different ABIs for different versions of the compiler.  It’s also not particularly well-defined, with various fields that can be excluded if they meet a default value.

It may make sense to define a canonical format (*e.g.* all fields must be present) and some sort of versioning as well.

