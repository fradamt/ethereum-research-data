---
source: magicians
topic_id: 21313
title: EOF Implementers call #60, October 16 2024
author: abcoathup
date: "2024-10-09"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-60-october-16-2024/21313
views: 60
likes: 0
posts_count: 1
---

# EOF Implementers call #60, October 16 2024

#### Agenda

[EOF Implementers Call #60 · Issue #1167 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1167)

#### Notes

Notes by [@shemnon](/u/shemnon) *(Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1167#issuecomment-2417261891))*

##### Testing

- Pectra-devnet-4 is occupying most of the test teams time
- Will merge new test, EOF WRap tool
- Client need to start activating on Osaka
- Osaka fixture are published
- 7702 coverage needs delegation testing, should be in fixtures. Will add more as needed

##### Clients & Compilers

- Nethermind passing Up to v1.1.0 tests
- revm - need to propagate Osaka fork and release
- Geth - RSVPed absent
- evmone - no updates - need to add Osaka fork
- Besu - Osaka is published in main, fixed callf bug found checking traces

##### Spec updates

- EIP-721 - HASCODE / EXTCODESIZE

@Frangio wants to re-enable EXTCODE opcodes to avoid risk, opcodes will happen via legacy contacts if not added, so we may as well add it.
- Marius doesn’t want to compromise on removing introspection, 7702 and migration may make EOAs irrelevant
- Separate from 721 the inability to determine if code lis legacy will break proxyies.
- Danno - We can still jumper out to legacy contracts to use EXTCODE* to get the answers we want from HASCODE
- Frangio would want EXTCODE brought in as-is, this still preserves opaqueness for EOF code
- Charles - EOAs can never revert and return data, that is how it is detected.
- ipsilon - agrees with Marius on keeping removing introspection in, but if not an option HASCODE is preferable to EXTCODE*
- Frangio - without this we will never be able to migrate legacy without some facility like EXTCODE
- ben - HASCODE is just checking a code attribute like we already do when executing EOF vs. non-EOF code. These are not deep introspections, doesn’t violate the code/memory barrier. Current handling of EXTCODE doesn’t violate the introspection for EOF code, and can be circumvented via legacny contract calls.
- frangio - understands ZK motivation, but needs more clarification on how HASCODE/EXTCODE breaks the ZK motivations.
- charles HASCODE does not preculed AA future, just all accoutns will return true

##### EXT*CALL return codes

- add new return code to clarify when a failure occured
- Pawel - motivation was that solidity wanted to know when a user caused a REVERT, and to behave differently. In process of implementing light errors were joined in with revert (to prevent some info leaks relating to gas introspection? i.e. failures relating to reserved gas returning a 2 could be used to divine gas levels)
- Charles - reverts can be detected with exiting return buffer,
- We should confirm with solidity this is useful.
- Charles - also, this allows for callstack introspection to determine that failure is callstack related.,
- danno/pitor - but 63/64ths rule would require billions of gas to reach the callstack limit.
- Current spec is 1 - not all gas consumed 2 - all call gas was consumed.

##### EOFCREATE hashing

- Goal is to reduce number of hashing calls needed, right now there is a double hashing per call.
- Discussions are ongoing on discord.
- Will come back in two weeks.
- Wants to be able to predict addresses from physical code
- Want collision-free addresses
- container path may be the solution instead of simple container offset for current container.

##### Other

- Tracing

Danno wants PC=0 is start of container
- evmone - starts from pc=0, it’s easier for a global pc counter. PC=0 is section 0 byte 0. It’s a pointer in evmone, so it’s all math in the trace anyway
- dragan - can work either way
- Ben - makes sense
- Pitor - container = 0 allows for impossible PCs to exist. Code section 0 prevents impossible PC indexes from showing up in traces.
- PC=0 at section 0 also helps indicating where a new call starts, apart from depth increasing.
- More consistent with legacy
- evmone - pc=0 at section 0, section 1 offset
- reth pc=0 at section 0, section 1 is zeroed
- nethermind pc=o at section 0, section 1 is zered.
- continuous PC (section1 bytes 0 != 0) is needed for fuzzing.

EOF quality of life list from ipsilon

[ipsilon/eof#165](https://github.com/ipsilon/eof/issues/165)

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2304dcb4aa8307250d51ea404fc67cf2e93fc7f3.jpeg)](https://www.youtube.com/watch?v=FLtlemN2W8w)
