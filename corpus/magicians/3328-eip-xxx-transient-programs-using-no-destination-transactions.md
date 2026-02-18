---
source: magicians
topic_id: 3328
title: "EIP-XXX: Transient programs using no-destination transactions"
author: veox
date: "2019-05-29"
category: EIPs
tags: [evm, eip, transient-program, draft, eoa]
url: https://ethereum-magicians.org/t/eip-xxx-transient-programs-using-no-destination-transactions/3328
views: 1624
likes: 0
posts_count: 2
---

# EIP-XXX: Transient programs using no-destination transactions

This is a draft of a draft; bear with me.

---

## Gist

No-destination transactions (with `to==''`) to have:

- ADDRESS of the EOA (same as from field);
- no extra gas use.

Compare to current:

- ADDRESS nonced - different on every execution;
- 32000 gas paid (G_txcreate), with justification in YP: “Paid by all contract-creating transactions after the Homestead transition.”

## Why this change?

- Allows “chaining” multiple transactions into one, with a bit of EVM bytecode as glue.
- No-destination does not equate contract-creating: see “transient programs” post and lll-multisend program linked therein.

## Why this post?

Soliciting critique on why this is a bad idea. I’m partial and blind to the obvious flaw(s).

## Provenance

Publicly mentioned as OT [here](https://ethereum-magicians.org/t/brainstorming-the-token-standard-in-eth2/3135/7). Privately for a year or so.

Been thinking this is how it’s going to work since PoC3. ![:confused:](https://ethereum-magicians.org/images/emoji/twitter/confused.png?v=15)

## Replies

**veox** (2019-05-29):

Placeholder comment for things-to-consider.

---

Impact on `CREATE`:

- must still use gas (G_create in YP);
- must still mince the nonce to obtain target address; including multiple CREATEs within a single transient program.

Impact on `SSTORE`:

- must not persist on exiting call frame, or revert immediately: would result in EOA with state otherwise.

No-destination call from within existing contract, or nested within another transient program:

- should already be impossible: can’t place an empty item on the stack to be used as argument to call.

