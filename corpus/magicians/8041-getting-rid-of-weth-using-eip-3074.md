---
source: magicians
topic_id: 8041
title: Getting rid of WETH using EIP-3074
author: axic
date: "2022-01-19"
category: EIPs > EIPs core
tags: [eip-3074, weth]
url: https://ethereum-magicians.org/t/getting-rid-of-weth-using-eip-3074/8041
views: 2299
likes: 8
posts_count: 5
---

# Getting rid of WETH using EIP-3074

(Originally posted [here](https://hackmd.io/@axic/HJKDHbUpF).)

While randomly looking at [WETH](https://etherscan.io/address/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2#code) I was wondering,

> Hmm, this was written such a long time ago, what would it look like with modern Solidity?

WETH9 was written for 0.4.18 (2017!) and we are at 0.8.10 today. ([@MrChico](/u/mrchico), what does 9 stands for?)

So I started iteratively changing it, adding small improvements one-by-one:

1. Turning those constants into actual constants
2. Upgrading the syntax of the fallback function
3. Adding the emit keyword to events
4. Fine-tuning public into external where it makes sense
5. Using custom errors (revert InsufficientBalance())
6. Adding even more type casting, especially for that comparison with -1
7. (And maybe renaming wad )

Cool. This took a few minutes. The code was pretty nice to begin with as it didn’t had any unneeded complexity. Now what?

I remembered those old attempts of trying to get rid of WETH as it is a nuisance. There were some proposals to enshrine it as a “precompile”. There was a proposal, [WETH10](https://github.com/WETH10/WETH10), to introduce [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) permits and flash loans into it. And a rewrite into Yul+, [WETH11](https://github.com/dmihal/WETH11), mostly motivated by saving gas ([some explainer thread here](https://twitter.com/dmihal/status/1475949119483088898)).

Getting rid of WETH for good always intrigued me as a goal, therefore spent some time in the past thinking about those enshrining proposals. It just occurred to me that perhaps with [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074) we can make this happen!

One would need to call `authorize` on this new contract, and from that point it gains access to the authorizer’s Ether. Transfers are still subject to the well known allowance system. (I assume by the time EIP-3074 goes live there will be nice ways to revoke authorizations.)

Here’s the rough code I put together in a few minutes:

**Disclaimer: do not use this for anything.**

```auto
pragma solidity ^0.8.0;

library EIP3074 {
    function transferEther(bytes32 commit, uint8 yParity, uint r, uint s, address sender, address recipient, uint amount) public {
        assembly {
            // NOTE: Verbatim actually isn't enabled in inline assembly yet
            function auth(a, b, c, d) -> e {
                e := verbatim_4i_1o(hex"f6", a, b, c, d)
            }
            function authcall(a, b, c, d, e, f, g, h) -> i {
                i := verbatim_8i_1o(hex"f7", a, b, c, d, e, f, g, h)
            }

            let authorized := auth(commit, yParity, r, s)
            if iszero(eq(authorized, sender)) { revert(0, 0) }

            let success := authcall(gas(), recipient, 0, amount, 0, 0, 0, 0)
            if iszero(success) { revert(0, 0) }
        }
    }
}

contract WETH3074 {
    string public constant name     = "Wrapped Ether";
    string public constant symbol   = "WETH";
    uint8  public constant decimals = 18;

    event  Approval(address indexed src, address indexed guy, uint wad);
    event  Transfer(address indexed src, address indexed dst, uint wad);

    mapping (address => mapping (address => uint)) public allowance;

    struct AuthParams {
        bytes32 commit;
        uint8 yParity;
        uint r;
        uint s;
    }
    mapping (address => AuthParams) private authParams;

    function totalSupply() external pure returns (uint) {
        // TODO: what to do with this?
        return uint(int(-1));
    }

    function balanceOf(address account) public view returns (uint) {
        return account.balance;
    }

    function approve(address guy, uint wad) external returns (bool) {
        allowance[msg.sender][guy] = wad;
        emit Approval(msg.sender, guy, wad);
        return true;
    }

    function transfer(address dst, uint wad) external returns (bool) {
        return transferFrom(msg.sender, dst, wad);
    }

    function transferFrom(address src, address dst, uint wad)
        public
        returns (bool)
    {
        require(balanceOf(src) >= wad); // TODO use custom error

        if (src != msg.sender && allowance[src][msg.sender] != uint(int(-1))) {
            require(allowance[src][msg.sender] >= wad); // TODO use custom error
            allowance[src][msg.sender] -= wad;
        }

        AuthParams memory params = authParams[src];
        EIP3074.transferEther(params.commit, params.yParity, params.r, params.s, src, dst, wad);

        emit Transfer(src, dst, wad);

        return true;
    }

    function authorize(bytes32 commit, uint8 yParity, uint r, uint s) external {
        authParams[msg.sender] = AuthParams(commit, yParity, r, s);
    }
}
```

It has at least the following problems:

1. The totalSupply is not set properly – it is not possible to extract this information from within the chain, yet
2. The Transfer event is only emitted if transfer is done via the token, but accounts can still natively do transfers
3. EIP-3074 actually doesn’t yet allow valueExt, i.e. transfers of Ether of the authorizing account
4. EIP-3074 is nowhere near to adoption yet
5. The authorisation parameters could be stored more efficiently

Coincidentally this also solves the [complaint](https://twitter.com/nicksdjohnson/status/1392590935498715137) of WETH9 not emitting a transfer on deposit, since there’s no need for depositing.

Thanks [@hrkrshnn](/u/hrkrshnn) and [@matt](/u/matt) for the brief review.

P.S. There are security considerations about EIP-3074, which are not specific to this use case. It is probably better discussing them in the [existing issues](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880).

## Replies

**axic** (2022-09-09):

I am still intrigued by the possibility of making Ether ERC-20 compatible with such a simple “trick”.

One of currently not fully solved problems of EIP-3074 is that authorisation cannot be easily withdrawn (there are multiple proposals for it). It occurred to me that in the case of this contract, as long as it has no “bugs”, having an `authorize` and `deauthorize` function could be sufficient:

```auto
    /// Authorise for sender.
    function authorize(bytes32 commit, bool yParity, uint r, uint s) external {
        authParams[msg.sender] = AuthParams(commit, (yParity ? (1 << 255) : 0) | r, s);
    }

    /// Removes authorisation for sender account.
    function deauthorize() external {
        delete authParams[msg.sender];
    }
```

---

**axic** (2022-09-09):

Created a repository for the fun of it, and to have a better track of iterations: [GitHub - axic/weth3074](https://github.com/axic/weth3074)

---

**albertocuestacanada** (2022-09-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> what does 9 stands for?)

WETH9 uses [kelvin versioning](https://jtobin.io/kelvin-versioning), meaning that 9 is the first version, and subsequent versions use a smaller number. The intention is that as the version number approaches zero, developers are more and more aware that further changes are not recommended.

Obviously I had no idea about that when I coded [WETH10](https://github.com/WETH10/WETH10) ![:man_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/man_shrugging.png?v=12)

---

**axic** (2022-09-14):

[@edsonayllon](/u/edsonayllon) suggested that the name should be different to WETH and to not use an EIP number to avoid confusion. The suggested name is “AETH” aka “Authorized Ether”. I think that may not be a bad name.

