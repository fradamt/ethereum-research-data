---
source: magicians
topic_id: 7221
title: "`Wand` aka `DSProxy 2.0`"
author: nikolai
date: "2021-10-06"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/wand-aka-dsproxy-2-0/7221
views: 1365
likes: 1
posts_count: 4
---

# `Wand` aka `DSProxy 2.0`

[github.com](https://github.com/nmushegian/wand)




  ![image](https://opengraph.githubassets.com/a65976922fdc56c9756ba42e60b744d2/nmushegian/wand)



###



DSProxy 2.0










This is a grab bag of proxy contract R&D. I’m publishing this to help bump priority for [SET_INDESTRICTUBLE](https://ethereum-magicians.org/t/eip-2937-set-indestructible-opcode/4571).

Code sketch and README at time of publishing are copied below:

---

```auto
interface WandAuth {
  function canCast(address witch, address spell, bytes4 sigil)
    external returns (bool);
}

contract Wand {
  address public root;
  address public auth;
  address public code;
  address public lock;

  function cast(address spell, bytes calldata data)
    payable public
      returns (bool bit, bytes memory ret)
  {
    require(lock == ZERO, 'ERR_LOCK');
    lock = msg.sender;

    bytes4 sigil; assembly{ sigil := calldataload(data.offset) }

    if (msg.sender != root) {
      require(auth != ZERO, 'ERR_ROOT');
      require(WandAuth(auth).canCast(msg.sender, spell, sigil), 'ERR_AUTH');
    }

    code = spell;
    address root_ = root;
    address auth_ = auth;

    (bit, ret) = spell.delegatecall(data);

    if (msg.sender != root) {
      require(root == root_, 'ERR_SET_ROOT');
      require(auth == auth_, 'ERR_SET_AUTH');
    }
    code = ZERO;
    lock = ZERO;

    // // This doesn't work, but ideally there's some way to detect selfdestruct
    // uint256 size; assembly { size := codesize(); }
    // require(size > 0, 'ERR_BOOM');

    assembly{ log4(caller(), spell, sigil, bit, 0, 0) }
  }

  function give(address dest) public {
    require(lock == ZERO, 'ERR_LOCK');
    require(msg.sender == root, 'ERR_GIVE');
    root = dest;
    assembly{ log3(caller(), 'give', dest, 0, 0) }
  }

  function bind(address what) public {
    require(lock == ZERO, 'ERR_LOCK');
    require(msg.sender == root, 'ERR_BIND');
    auth = what;
    assembly{ log3(caller(), 'bind', what, 0, 0) }
  }

  constructor() {
    root = msg.sender;
    assembly{ log3(0, 'give', caller(), 0, 0) }
  }

  address constant internal ZERO = address(0);
}
```

---

A `Wand` is a variation of the Proxy pattern with some differences and extra features

## canCast authorization

- The authorization pattern for access controlled calls (non-root/owner callers) has
changed from DSProxy. Instead of using DSAuth to access control the proxy object itself,
root (owner) retains sole access to true “root” functions (transfer and update authority),
while cast applies the canCast access control table to the spell being cast. Concretely:

`canCall(address caller, address object, bytes4 sig) -> (bool)`

which was used like

```auto
function exec(address target, bytes calldata data) returns (bytes ret) {
  assert authority.canCall(msg.sender, address(this), msg.sig)`
  ...
}
```

becomes

```auto
`canCast(address caller, address spell, bytes4 sig)`
```

which is called like

```auto
function cast(address spell, bytes calldata data) returns (bool ok, bytes ret) {
  assert auth.canCast(msg.sender, spell, data[0:4]);
  ...
}
```

## protected root and auth

- caller-saved owner (root) and permission table (auth) makes spells
somewhat safer to use.

```auto
address root_ = root;
address auth_ = auth;

// this is in a fresh context, the local execution stack is not visible
(bit, ret) = spell.delegatecall(data);

require(auth == auth_, 'ERR_SUDO');
require(root == root_, 'ERR_SUDO')
```

(The remaining loss of root control danger lies in `SELFDESTRUCT`,

which is easier to statically detect

(mitigated in future by

EIP4571 SET_INDESTRUCTIBLE,

or any way to detect that code has been scheduled for selfdestruct)

## reentry lock and caller reference

- reentry lock saves the caller in storage and exposes it via function,
for access from both the spell being run external contracts. It is zero’d
for gas savings and consistency between spells

```auto
lock = msg.sender;
...

lock = ZERO;
```

## spell (library) code reference

- the code being delegatecalled (the spell that was cast) is also saved
in storage so that the spell knows the actual contract object which has
the code being run (libraries do not have a “library object” reference, but
they could! These would be like singleton stateful libraries). It is also zero’d
after each cast (and/but is “caller save” for spells calling spells)

```auto
code = spell;
...

code = ZERO;
```

## Replies

**PaulRBerg** (2021-10-08):

Lots of good ideas here! Thanks for sharing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nikolai/48/4312_2.png) nikolai:

> the code being delegatecalled (the spell that was cast) is also saved
> in storage so that the spell knows the actual contract object which has
> the code being run

When would this be useful? You mentioned the concept of “singleton stateful libraries” but I’ve never seen that implemented in Ethereum.

---

**poma** (2021-10-12):

Aren’t checks for `LOCK` variable redundant?

1. delegatecall can override it during execution anyway
2. Any changes to root and auth will be caught by guards after the delegatecall

Also `auth` and `root` are read 3 times before they are cached, can slightly save on gas there. I know it’s super minor but reading storage and then caching it immediately catches the attention.

---

**nikolai** (2021-10-15):

You are correct, see this issue and discussion: [Reentry is impossible to prevent when delegate calling · Issue #3 · nmushegian/wand · GitHub](https://github.com/nmushegian/wand/issues/3)

