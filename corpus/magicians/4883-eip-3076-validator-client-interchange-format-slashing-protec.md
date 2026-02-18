---
source: magicians
topic_id: 4883
title: "EIP-3076: Validator client interchange format (slashing protection)"
author: michaelsproul
date: "2020-10-28"
category: EIPs
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/eip-3076-validator-client-interchange-format-slashing-protection/4883
views: 3748
likes: 4
posts_count: 11
---

# EIP-3076: Validator client interchange format (slashing protection)

Discussion thread for EIP-3076:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3076)





###



A JSON interchange format for proof of stake validators to migrate slashing protection data between clients.










> A JSON interchange format for Serenity (eth2) that contains the necessary slashing protection information required to safely migrate keys between clients.

## Replies

**michaelsproul** (2020-11-11):

Discussions with Trent Mohay on the [Eth R&D discord](https://discord.com/channels/595666850260713488/720658991763685377/772636070927532042) raised some deficiencies in the current spec when it comes to potentially invalid data. I’ve been expanding the test coverage in [the test repo](https://github.com/eth2-clients/slashing-protection-interchange-tests/pull/2/), and have a few decisions that I need stakeholders to provide feedback on.

## Decision 1: Duplicate Pubkeys

Presently the spec says nothing of the case where the `data` array contains multiple

entries with the same `pubkey`. We have three options:

- ACCEPT: explicitly allow duplicate pubkeys
- REJECT: explicitly reject duplicate pubkeys
- ABSTAIN: leave duplicate pubkey semantics up to the implementation

### Arguments for ACCEPT

- Simple implementation. No need to add additional checks. Lighthouse and Teku
use ACCEPT semantics, likely by accident.

### Arguments for REJECT

- There is little sense in allowing multiple entries when the inner arrays
serve the same purpose.

### Arguments for ABSTAIN

- I can’t think of any.

### Testing

The `duplicate_pubkey_not_slashable` test case exercises this code path.

## Decision 2: Importing Slashable Data

It’s possible for an interchange file to contain blocks and attestations that

are mutually slashable, i.e. the interchange file contains evidence that the

validator has already committed a slashable offence. It’s also possible for

an interchange to contain messages that are slashable with respect to ones already

in the database.

Our options:

- ACCEPT: require implementations to import files even if they contain slashable data
- ACCEPT_PARTIAL: require implementations to import all validators that are not slashable,
and reject all that are slashable
- REJECT: require implementations to reject any imported file if it contains slashable data
- ABSTAIN: allow implementations to choose a semantics that works for them

### Arguments for ACCEPT

- Rejecting a file could prompt a user to abandon the import rather than going through
the tedious process of editing out the slashable/slashed validators by hand.

### Arguments for ACCEPT_PARTIAL

- As for ACCEPT: more inputs accepted, less user confusion
- Unlike ACCEPT: compatible with databases that can’t store slashable messages (see REJECT).

### Arguments for REJECT

- Many slashing protection strategies assume that the database does not already
contain any slashable messages, and store data according to this
assumption. In these cases, enforcing ACCEPT semantics would greatly
complicate both the specification and implementation, e.g. which of two slashable
attestations that are surrounding should be kept and stored?
- It’s reasonable for a slashing protection implementation to import an interchange file
by processing each message as if it is a new message to be signed, which would necessarily
reject any slashable data contained in the interchange file.

### Arguments for ABSTAIN

- Some slashing protection strategies (like Teku’s) handle this gracefully and can move
forward even in the presence of existing slashable data.

### Testing

The following test cases exercise these code paths:

- single_validator_slashable_blocks
- single_validator_slashable_attestations_double_vote
- single_validator_slashable_attestations_surrounds_existing
- single_validator_slashable_attestations_surrounded_by_existing

## Decision 3: Ordering

The specification doesn’t currently place ordering requirements on blocks or attestations

within a file, but it may simplify implementation to do so.

- ORDERED: require messages to be ordered, and for implementations to reject unordered files
- UNORDERED: allow messages to be unordered, and require implementations to accept unordered files
- ABSTAIN: allow implementations to choose ordered or unordered semantics

### Arguments for ORDERED

- Compatible with the import approach where messages are imported one-at-a-time as if they are
new messages to be signed. If they are unordered, then an import will run afoul of the
ordering conditions (2), (4) and (5).
- It is straight-forward to order messages on export

### Arguments for UNORDERED

- It is also straight-forward to order messages on import, if required by the implementation

### Arguments for ABSTAIN

- I can’t think of any.

### Testing

- single_validator_out_of_order_blocks
- single_validator_out_of_order_attestations

## Decision 4: Signing Roots

Presently signing roots are optional, but this has some downsides, so we could consider making them

mandatory.

- MANDATORY: require signing_root on all blocks and attestations
- OPTIONAL: allow signing_root to be omitted

### Arguments for MANDATORY

- Simplifies slashability considerations: with
the way the spec is worded now, we have to consider a message without a
signing root as slashable with respect to any other message with the same
slot/target epoch. This complicates several things, including:

(Assuming Decision 2: REJECT) Importing the same file twice if it
lacks signing roots. The second time the same messages are imported
they need to be considered slashable wrt the first import (no
idempotence).
- Import/export cycles between different clients. If I export with signing roots from
implementation A, import to another implementation B that erases signing roots,
and then later re-export from B to A, then A has no way of knowing that some of
the included messages are actually fine because they’re the ones it signed earlier.

Most implementations with complete databases support signing roots

(Lighthouse, web3signer, Prysm [soon]). Teku could be adapted to. I don’t

know about Nimbus.

## Arguments for OPTIONAL

- No need to change Teku (particularly post-audit, so close to mainnet).

---

**michaelsproul** (2020-11-11):

Need input on the above decisions from Web3Signer, Teku, Prysm, Nimbus, and my co-author [@sachayves](/u/sachayves) ![:innocent:](https://ethereum-magicians.org/images/emoji/twitter/innocent.png?v=9)

My votes are for:

- Decision 1, Duplicate Pubkeys: REJECT
- Decision 2, Slashable Data: REJECT, or ACCEPT_PARTIAL
- Decision 3, Ordering: weak preference for ORDERED
- Decision 4, Signing Roots: MANDATORY, especially if Decision 2 is REJECT

---

**rain-on** (2020-11-11):

For web3signer we’re thinking:

- Duplicate pubkeys - ACCEPT, its effectively a super-set of both lists
- Slashable Data - ACCEPT, but ensure ‘runtime’ ruleset prevents further resigning of matched (slashable) events
- Ordering - UNORDERED - but will need to consider how to re-calc low-watermark after import
- Signing Roots - weak MANDATORY - a null implies that slot/targetEpoch can never be signed again

---

**rain-on** (2020-11-11):

This is really based on the fact that Web3signer treats the import file as though it were as trusted as our local db - thus if the import conflicts with the database, there’s no way of deciding which is right or wrong; so we keep them both - which in turn probably means you don’t want to sign either conflicting entry again (if given the opportunity)

---

**thezluf** (2020-11-11):

These are my votes:

- Decision 1, Duplicate Pubkeys: REJECT user have to fix his input file and retry
- Decision 2, ACCEPT_PARTIAL if detected as slashable skip the data point (happened to me many times that i wasn’t caught on slashble offences as the network didn’t propagate my slashable attestation ) as a validator i just want to keep participate as long as i am not slashed
- Decision 3, UNORDERED import can handle writing to the right location in its own implementation
- Decision 4, Signing Roots: OPTIONAL  as in minimal data format blocking all attestations when signing root is missing for a certain epoch can be a default

---

**rolfyone** (2020-11-11):

1: ACCEPT,  It makes it easier to combine files and doesn’t seem like its at all difficult to support. Why make it hard for users?  Implementations shouldn’t generate files with duplicate public keys though.

2: ACCEPT/ABSTAIN - teku just keeps a high water mark

arguably, if it’s been signed, it should be considered, and the fact that it *was* slashable is less important than not signing something that potentially interacts with those, so load it so you protect from signing again.

3: UNORDERED - the data format should be as permissive as possible, the implementation can order if required.

4: OPTIONAL - or could remain an implementation decision. Teku has no plans to support providing signing roots, and it would be a difficult argument to have a week before we go to RC.

---

**ajsutton** (2020-11-11):

It’s probably worth noting that the general philosophy for Teku and Web3Signer is:

1. Be as flexible as possible in what input is accepted.
2. Err on the side of not signing rather than risk getting slashed. Being flexible in what input is accepted is a big part of that because having more data makes it safer whereas rejecting data risks rejecting something we actually needed to know to avoid being slashed.

And just to clarify for Decision 4, Signing Roots - they must be optional for Teku.  No point making it an implementation decision or you couldn’t migrate slashing records from Teku to anything that requires signing roots.

---

**rain-on** (2020-11-12):

Web3signer can work with optional signing-roots, I prefer to have them, but not at the expense of other clients.

---

**michaelsproul** (2020-11-12):

Thank you all for the feedback. How about we move forward with these decisions:

1. Duplicate pubkeys: ACCEPT, with caveat “Implementations shouldn’t generate files with duplicate public keys”
2. Slashable data: ACCEPT_PARTIAL, abstain when it comes to whether or not slashable data must be imported (it would be very hard to support ACCEPT in Lighthouse right now)
3. Ordering: UNORDERED
4. Signing Roots: OPTIONAL

The logic for (1) and (3) is that we should be liberal in what we accept, and these are simple cases.

The logic for (2) is similar – mandate accepting as much as possible, with an acknowledgement that accepting *everything* is not feasible for all implementations.

The logic for (4) is: keep the standard compatible with varied implementations (e.g. Teku). Other implementations just need to take care that the `null`/missing root compares as incompatible with *every* other root (including itself). Just like `NaN` ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=9)

---

**ManuNLP** (2023-06-16):

Condition 5 is currently not consistent with [single_validator_resign_attestation.json](https://github.com/eth-clients/slashing-protection-interchange-tests/blob/master/tests/generated/single_validator_resign_attestation.json) tests, and Condition 5 is not consistent with Condition 2.

Condition 5 could be updated as follows:

> Refuse to sign any attestation with target epoch less than or equal to the minimum target epoch present in that signer’s attestations (as seen in data.signed_attestations), except if it is a repeat signing as determined by the signing_root .

See [`single_validator_resign_attestation.json`: Inconsistency with the EIP-3076 specification? · Issue #15 · eth-clients/slashing-protection-interchange-tests · GitHub](https://github.com/eth-clients/slashing-protection-interchange-tests/issues/15) for more details.

