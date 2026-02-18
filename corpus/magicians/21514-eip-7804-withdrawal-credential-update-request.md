---
source: magicians
topic_id: 21514
title: "EIP-7804: Withdrawal Credential Update Request"
author: mkalinin
date: "2024-10-31"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7804-withdrawal-credential-update-request/21514
views: 458
likes: 4
posts_count: 9
---

# EIP-7804: Withdrawal Credential Update Request

Discussion topic for EIP-7800 [Add EIP: Withdrawal Credential Update Request by lucassaldanha · Pull Request #9005 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9005)

#### Abstract

This proposal defines a mechanism to allow validators to update their withdrawal credentials using a new execution request type (0x3). The request allows for changing the execution address and the withdrawal credential prefix (0x01 or 0x02).

#### Update Log

- 2024-10-31: initial draft Add EIP: Withdrawal Credential Update Request by lucassaldanha · Pull Request #9005 · ethereum/EIPs · GitHub

## Replies

**SoulcoIIector** (2024-11-01):

Hello! How will the proposed mechanism in EIP-7804 ensure the security and integrity of updated withdrawal credentials for Ethereum validators, and are there any potential risks associated with changing execution addresses and credential prefixes?

---

**lucassaldanha** (2024-11-03):

> How will the proposed mechanism in EIP-7804 ensure the security and integrity of updated withdrawal credentials for Ethereum validators

The mechanism proposed is similar to other execution layer requests (e.g., withdrawal requests). When the function to create an update request is called, the smart contract uses the `msg.caller` address as `old_address` when creating the request. Therefore, on the CL side, the protocol can verify that `old_address` matches the current validator withdrawal credential address and only update it if they match. This way, we ensure that only the current `validator.withdrawal_credentials` owner can update the address.

> are there any potential risks associated with changing execution addresses and credential prefixes?

I don’t think there are any extra security considerations for execution addresses. As long as we guarantee that the address can only be updated by the “owner” of the previous address, this is all that is needed.

In terms of changing credential prefixes, there are two possible scenarios: changing from 0x01 to 0x02 and from 0x02 to 0x01.

The first scenario (0x01 → 0x02) is straightforward and does not need any extra consideration and we can re-use the rules from `is_valid_switch_to_compounding_request `.

The second scenario (0x02 → 0x01) is a bit more complicated. Any excess balance needs to go through the churn to prevent sudden changes in staked eth. We are still researching what would be the best way to accomplish this safely.

---

**dgeorgiev06** (2024-11-04):

Hi. Will the solution require validators to go through the exit queue (or any other time delaying mechanism) in the same way that validator consolidations will and therefore be subject to churn limits? Also will the effective balance have an impact on time it takes to update the withdrawal address, eg a validator with EB of 32 vs EB of 2048?

---

**lucassaldanha** (2024-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgeorgiev06/48/13338_2.png) dgeorgiev06:

> Will the solution require validators to go through the exit queue (or any other time delaying mechanism) in the same way that validator consolidations will and therefore be subject to churn limits? Also will the effective balance have an impact on time it takes to update the withdrawal address, eg a validator with EB of 32 vs EB of 2048?

The short answer is yes. We need a mechanism to ensure the excess balance when changing from 0x02 to 0x01 goes through the exit queue. It would probably be something similar to what is done in Pectra (next fork) for partial withdrawals with some extra logic around only effectively changing the credentials upon the balance being completely withdrawn or something like that. I haven’t spent a lot of time defining those mechanisms yet because I wanted to gauge if this EIP will get enough support/traction before spending too much time on the details.

---

**lucassaldanha** (2024-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgeorgiev06/48/13338_2.png) dgeorgiev06:

> Hi. Will the solution require validators to go through the exit queue (or any other time delaying mechanism) in the same way that validator consolidations will and therefore be subject to churn limits?

The challenge with this is to create a mechanism that does not bring a lot of extra complexity to the protocol. One possible solution would be to require a validator that wants to change from compounding (0x02) to execution (0x01) to use a partial withdrawal (introduced in Electra) to bring their balance “close” to 32 ETH. The partial withdrawal mechanism already takes into account the churn and everything. Later, when processing the credential update, as long as the balance is within a certain tolerance of 32 ETH (e.g. < 32.5 ETH).

Using this approach, we can limit the amount of balance that will “leave” the stake per slot (MAX_UPDATES_PER_SLOT * tolerance).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgeorgiev06/48/13338_2.png) dgeorgiev06:

> Also will the effective balance have an impact on time it takes to update the withdrawal address, eg a validator with EB of 32 vs EB of 2048?

I don’t think changing the address requires any special treatment. The consideration is related to changing creds type.

---

**Trying2Cook** (2025-09-14):

If the withdrawal wallet gets compromised, then what stops the attacker from changing the withdrawal address?

---

**lucassaldanha** (2025-09-14):

Unfortunately, if the withdrawal credential is compromised, there is nothing we can do to prevent it from being changed. However, even without EIP-7804, if the withdrawal credentials are compromised, the attacker will have access to the balance of the account, so I believe changing or not changing the address does not change the fact that the funds could be lost.

---

**Trying2Cook** (2025-09-15):

Except while the withdrawal credential is compromised, at least there is a possibility of getting the funds on an exit.

If you allow to change and the attacker changes it first, then there is 0 change of getting the funds on exist.

I think there needs to be a 2 of 3 signed signature to allow validator exit and changing the withdrawal address.  Maybe the introduction of an option to upgrade a validator to a new secure credential that distinguishes it from the 0x01 and 0x02.  Maybe there is a 0x03, which is like 0x01, but has a 2 of 3 signature control and 0x04, like 0x02, but 2 of 3 signature control.

The signatures could be the current withdrawal address, validator mnemic phrase, and deposit address?  I’ve not thought of a good 3rd one because if someone deposits and withdrawal are the same, then they already of 2 of 3 signatures.  Maybe the system needs to force deposits to come from a different address and the deposit and withdrawal address can never be the same.

