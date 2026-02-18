---
source: magicians
topic_id: 3688
title: "Crypto collectives: membership and role management"
author: rumkin
date: "2019-10-08"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/crypto-collectives-membership-and-role-management/3688
views: 709
likes: 1
posts_count: 1
---

# Crypto collectives: membership and role management

This is a proposal draft. For crypto communities/organizations.

## Problem

1. Each time new member get into the organization or get out of it, someone need to grant/revoke all accesses to the new member. Sometimes new member couldn’t receive required permissions or preserve access to organization infrastructure and continue to receive corporate mails/bills/other sensitive information. Also when this member change a role the process should be run again. This is really insecure and very problematic issue.
2. Today all services around the globe couldn’t determine wether the user has permissions to create account for the specified brand or not. There is no such data layer which can join company ownership data with any database to provide membership/ownership guaranties.

## Solution

Create a contract which can manage team members and their roles. Changes from the contract could be read by another contracts or external software to define/resolve access permissions.

For example it could be used with ENS domain. This will allow user with role `developer` to have permissions to deploy the website, merge PRs, close Issues, etc. and `owner` to create new social network accounts for this host.

### Requirements

1. Role could be added and removed.
2. Role could be suspended and activated.
3. Role could be renamed.
4. Roles count is uint256.
5. Members could have several roles in the same time for example ‘developer’ and ‘sysadmin’ or ‘designer’ and ‘photographer’.
6. Member could be suspended and activated.
7. Contract should emit events for:

membership granting/revoking,
8. members role granting/revoking,
9. role adding/removing,
10. role suspension/activation.

Role granting/revoking process could have different implementations: authoritative, votable, hierarchical.

## Contract interface

```auto
contract ITeam {
    // Role management
    addRole(string name) returns(uint);
    getRoleId(string name) return(uint);
    getRoleName(uint roleId) returns(string);
    countRoles(address member);
    getRoleByIndex(uint index);
    disableRole(uint roleId) returns(bool);
    enableRole(uint roleId) returns(bool);

    // Membership menagement
    setMemberRole(address member, uint roleId) returns(bool);
    hasMemberRole(address member, uint roleId) returns(bool);
    removeMemberRole(address member, uint roleId) returns(bool);
    removeAllMemberRoles(address member);
    countMemberRoles(address member);
    getMemberRoleByIndex(uint index);
    disableMember(address member) returns(bool);
    enableMember(address member) returns(bool);
}
```

## Unresolved questions/probable solutions

- There could be a “standard” roles. To be unified for all solutions.
- There should be a way to avoid role names collision for upgradeability and security issues.

## Example

I’ve realized such contract support in a twitter a-like text-only append log web app to manage collective accounts or groups. Thus it became possible to hire content managers without fear of access loss, buy/sell membership, create earning communities.
