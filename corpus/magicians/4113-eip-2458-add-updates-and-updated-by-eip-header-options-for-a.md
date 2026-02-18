---
source: magicians
topic_id: 4113
title: "EIP-2458: Add updates and updated-by EIP Header Options for active EIPs"
author: edsonayllon
date: "2020-03-09"
category: EIPs > EIPs informational
tags: []
url: https://ethereum-magicians.org/t/eip-2458-add-updates-and-updated-by-eip-header-options-for-active-eips/4113
views: 508
likes: 0
posts_count: 3
---

# EIP-2458: Add updates and updated-by EIP Header Options for active EIPs

**TLDR;** You’d need to create a new EIP in Accepted to make a normative change to EIP-1 with this proposal.

```auto
---
eip: 2458
title: Add updates and updated-by EIP Header Options for active EIPs
author: Edson Ayllon (@edsonayllon)
discussions-to:
status: Draft
type: Meta
created: 2020-01-06
updates: 1
---
```

## Simple Summary

Adds EIP header options  `updates`  and  `updated-by`  to frontmatter of  `active`  EIPs for use as needed. EIPs.

## Scope

Adds header options. Changes process for updating active EIPs.

## Abstract

EIP headers  `updates`  and  `updated-by`  are used for updating  `active`  EIPs. This is to make the improvement process of EIPs more modular, and have updates to existing  `active`  EIPs receive similar exposures to EIPs which replace existing  `final`  EIPs.

## Motivation

Currently, EIP1 specifies EIP headers:  `updated` ,  `replaces` , and  `superseded-by` . Headers  `replaces`  and  `superseded-by`  indicates when an entire EIP is being replaced by another EIP, indicating when an EIP is now historical, and is updated by a new standard.

The header  `updated`  indicates the date an EIP has received an update by EIP authors and editors, an example EIP being EIP1.  `updated`  is reserved for EIPs in  `draft`  or  `active`  status.

In the case of  `active`  status, an EIP may receive an update, but these updates don’t operate as with EIPs in  `final`  status, where a historical EIP is created, and the new EIP is referenced by the historical one. While these updates are not kept immutably, updates to active EIPs can be done modularly by creating a new EIP that goes through the standard discussion and auditing process EIPs undergo. The EIP headers  `updates`  and  `updated-by`  are to facilitate this modularity. Creating a new EIP also provides sufficient notification to affected stakeholders of an active EIP before that EIP is  `updated` .

## Specification

### updated-by

`updated-by`  is reserved for EIPs in  `active`  status. For an EIP in status  `active` , updates to that EIP, which update the header  `updated` , should be started by opening a new EIP to start vetting for that update. When an  `active`  EIP receives a new entry to header  `updated` , an associated  `updated-by`  EIP listing should be included, where that newly listed EIP has reached  `final`  status, except where changes that don’t change meaning, such as spelling and grammar corrections, are made.

`updates`  should be included as an EIP header, as all EIP headers, and include a reference to an EIP designation. When multiple EIP designations are referenced, each should be separated by a comma. Example:

```auto
---
updated-by: EIP9999, EIP9998
---
```

### updates

`updates`  is reserved for EIPs updating EIPs in  `active`  status. An EIP listed as  `updates`  is implied to also be  `requires` ; only  `updates`  is needed for those EIP listings. Having an EIP listing  `updates`  does not necessarily mean that referenced EIP must reference back with an  `updated-by`  listing.

`updates`  should be included as an EIP header, as all EIP headers, and include a reference to an EIP designation. When multiple EIP designations are referenced, each should be separated by a comma. Example:

```auto
---
updates: EIP1
---
```

## Rationale

`updates`  and  `updated-by`  apply only to EIPs in  `active`  status as updates to EIPs in  `final`  status are already handled by EIP headers  `superseded-by`  and  `replaces` .

The syntax should align with previous EIP header syntax, as this EIP is not updating syntax, simply adding header options.

## Backwards Compatibility

These EIP headers are optional and do not introduce compatibility issues.

## Implementation

This EIP is an example implementation of  `updates` , updating EIP1.

## Security Considerations

This standard is informational and does not introduce technical security issues.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**edsonayllon** (2020-03-09):

Adding this process would standardize changes to EIP-1. Open to hearing thoughts.

---

**edsonayllon** (2020-03-25):

Link to discussion done on Github: https://github.com/ethereum/EIPs/issues/2453

