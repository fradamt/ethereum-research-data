---
source: ethresearch
topic_id: 12516
title: Withdrawal Credentials Exits Based On A Generalized Message Bus
author: arwer13
date: "2022-04-29"
category: The Merge
tags: []
url: https://ethresear.ch/t/withdrawal-credentials-exits-based-on-a-generalized-message-bus/12516
views: 9834
likes: 14
posts_count: 24
---

# Withdrawal Credentials Exits Based On A Generalized Message Bus

Post co-authored with [@vshvsh](/u/vshvsh)

This post is a follow-up of [0x03-withdrawal-credentials post](https://ethresear.ch/t/0x03-withdrawal-credentials-simple-eth1-triggerable-withdrawals/10021) and the discussions.

We use “withdrawer exit” throughout the text to name validator exit triggered by withdrawal credentials. We don’t consider 0x00 type withdrawal credentials, because to withdraw there should be a [rotation to 0x01 type](https://ethresear.ch/t/withdrawal-credential-rotation-from-bls-to-eth1/8722) anyway.

This post aims to:

- elaborate on a possible solution for withdrawer exit requests
- present Generalized Message Bus (GMB) for conveying messages from the execution layer (EL) to the consensus layer (CL)

# Motivation

Currently, control over withdrawal credentials doesn’t provide the capability to initiate the validator exit and withdraw the funds. Thus, when the withdrawals are enabled, delegated staking solutions will not be fully capable of fulfilling stakers requests to withdraw their funds. Thus it seems important that withdrawer exits get enabled in the Ethereum protocol along with the withdrawals.

# Solution

Emit an event from a dedicated smart contract and process it on a beacon chain client similar to the `DepositContract` mechanism. It’s quite alike the solution in [0x03-withdrawal-credentials-simple-eth1-triggerable-withdrawals](https://ethresear.ch/t/0x03-withdrawal-credentials-simple-eth1-triggerable-withdrawals/10021) but with the two main differences:

1. do no checks on EL which require knowledge of the Beacon state
2. generalize the pattern of conveying a message from EL to CL

The purpose of (1) is to avoid complexity and CL and EL coupling (if possible).

## Generalizing

We think there is a pattern general and repetitive enough to consider it as a separate entity. The main components of the pattern are:

- need to convey a message from EL to CL
- need to protect CL from spam from EL

There are at least two types of messages to be sent from EL to CL: withdrawer exit and 0x01 type withdrawal credential rotation. Potentially, other new types are needed as the protocol evolves.

Full GMB spec is available [here](https://hackmd.io/@lido/BkiOdwcmK). Here we describe only the parts related to withdrawer exits.

On CL, we propose to implement a mapping from addresses of trusted contracts to lists of the events types expected from the address. A message is emitted on EL as an EVM event from a smart contract from an allow-list of message bus smart contracts. Then parsed, and processed on a beacon chain client like `DepositEvent` from `DepositContract` is processed (some related parts of the Prysm client: [one](https://github.com/prysmaticlabs/prysm/blob/c1197d7881ba2041e06f12b48ad02ab5a91357f1/beacon-chain/powchain/log_processing.go#L103), [two](https://github.com/prysmaticlabs/prysm/blob/c1197d7881ba2041e06f12b48ad02ab5a91357f1/beacon-chain/cache/depositcache/pending_deposits.go), [three](https://github.com/prysmaticlabs/prysm/blob/c1197d7881ba2041e06f12b48ad02ab5a91357f1/beacon-chain/rpc/prysm/v1alpha1/validator/proposer_deposits.go)).

Message of a GMB is a data structure `Message`.

```auto
contract IBeaconChainMessageBus {
    struct Message {
        uint256 messageType;
        bytes data;
    }

    event MessageEvent(Message message);
}
```

Depending on `messageType`, data is parsed to a specific payload for that type.

As a basic way to protect CL from spam tx fees plus additional ETH burning are proposed to be used. If needed more specific checks can be implemented in the message bus smart contract.

## WithdrawerExitBus contract

Basic (with no specific spam protection beyond EL transaction fees) `WithdrawerExitBus` contract implementation based on GMB might look like this.

```auto
contract WithdrawerExitBus is IBeaconChainMessageBus {
    uint256 constant WITHDRAWER_EXIT_TYPE = 0x00;

    struct WithdrawerExit {
        address withdrawalAddress;  // address corresponding to the 0x01 withdrawal creds
        uint256 validatorIndex; // caller is responsible to get it from validator pubkey
    }

    function initiateValidatorExit(uint256 _validatorIndex) external {
        // optionally require msg.value > some value and lock it on the contract
        WithdrawerExit memory withdrawerExit = WithdrawerExit(msg.sender, _validatorIndex);
        bytes memory encodedData = abi.encode(withdrawerExit);
        emit MessageEvent(Message(WITHDRAWER_EXIT_TYPE, encodedData));
    }
}
```

We suppose it might be possible to provide a sufficient level of spam protection purely by gas costs + additional ETH burning.

The amount of non-malicious withdrawer exit requests is low and won’t clog the queue. The risks come from invalid requests. The idea is to weed them out on CL, because the validity checks are relatively cheap and might not need the limit as low as we need it for voluntary exits.

Sufficient withdrawer exit request ETH costs might be derived from these limitations:

- non-malicious user costs (should be kept low when there’s no attack)
- max amount of validity checks per block on CL (needs to be determined)
- tolerable duration of the withdrawer exit queue lock & price of the attack (needs to be determined)

For example, 24 hours blocking at 25 gwei gas price, and 24332 gas cost of a withdrawer request (call to `initiateValidatorExit`) will cost:

| max validity checks per block | block capacity filled | min attack price |
| --- | --- | --- |
| 16 | 3% | 70 ETH |
| 64 | 10% | 280 ETH |
| 615 | 100% | 2693 ETH |

[Here](https://colab.research.google.com/drive/1iWopTMub1QbNjHTqqFlzhlmztUdDCu91?usp=sharing) is the python code to play with the parameters.

Block capacity filled is calculated for a block gas limit 15m. If it’s 100% it means there is no space left in the block to cram more invalid withdrawer exits.

Note that the attack prices for high block capacity fills are more like lower limits because in these cases the gas price will go up due to the base fee gas price increment.

In the extreme case, for 100% block capacity filled the gas price will become huge `31554 = 25 * 1.25**32` just after a single epoche (assuming the start base fee is 25 gas).

## Consensus layer

A naive extension of the Beacon spec might look like this.

```python
MAX_WITHDRAWER_EXITS = 2**4

class WithdrawerExit(Container):
    validator_index: ValidatorIndex
    withdrawer_address: ExecutionAddress

class BeaconBlockBody(Container):
    # ...
    deposits: List[Deposit, MAX_DEPOSITS]
    voluntary_exits: List[SignedVoluntaryExit, MAX_VOLUNTARY_EXITS]
    withdrawer_exits: List[WithdrawerExit, MAX_WITHDRAWER_EXITS]

def process_operations(state: BeaconState, body: BeaconBlockBody) -> None:
    # ...
    for_ops(body.deposits, process_deposit)
    for_ops(body.voluntary_exits, process_voluntary_exit)
    for_ops(body.withdrawer_exits, process_withdrawer_exit)

def is_withdrawer_exit_valid(state: BeaconState, withdrawer_exit: WithdrawerExit) -> bool:
    validator = state.validators[withdrawer_exit.validator_index]
    # Verify the validator is active
    assert is_active_validator(validator, get_current_epoch(state))
    # Verify exit has not been initiated
    assert validator.exit_epoch == FAR_FUTURE_EPOCH
    # Verify the validator has been active long enough
    assert get_current_epoch(state) >= validator.activation_epoch + SHARD_COMMITTEE_PERIOD

    # Check withdrawer_exit was indeed initiated by withdrawal credentials
    return withdrawer_exit.withdrawer_address == validator.withdrawal_credentials

def process_withdrawer_exit(state: BeaconState, withdrawer_exit: WithdrawerExit) -> None:
    if is_withdrawer_exit_valid(state, withdrawer_exit):
        initiate_validator_exit(state, withdrawer_exit.validator_index)
```

What’s wrong or unclear about it?

1. We probably want the amount of voluntary plus withdrawer exits to be under the same limit MAX_VOLUNTARY_EXITS. They are both still “voluntary” in the sense that not forced by the protocol for misbehavior.
2. Check for validity validate_withdrawer_exit seems to be cheap enough to permit much more of them per slot. But the size of BeaconBlockBody.withdrawer_exits cannot be extended because all its items are supposed to be either discarded as invalid or fulfilled in this block.

A possible way out is to implement a larger amount of validity checks is to validate withdrawer exit requests on the way to `BeaconBlockBody.withdrawer_exits`. Here we assume there is a preliminary queue alike the queue for deposit events. The validity check is the same: call to `is_withdrawer_exit_valid(...)`.

The Beacon spec doesn’t fully cover the question of how `BeaconBlockBody.deposits` gets populated, so let’s turn to Prysm client implementation for an example.

The `BeaconBlockBody.deposits` array is formed in file `proposer_deposits.go` in function `deposits(...)` ([the code](https://github.com/prysmaticlabs/prysm/blob/2f29bb64f621e4832543be0fe0e32829f565c163/beacon-chain/rpc/prysm/v1alpha1/validator/proposer_deposits.go#L65)).

Let’s assume `params.BeaconConfig().MaxWithdrawerExitsPerBlock` equals to `MAX_WITHDRAWER_EXITS`. And `params.BeaconConfig().MaxWithdrawerExitsChecksPerBlock` is max validity checks per block. Then pseudocode of the function to populate `BeaconBlockBody.withdrawer_exits` could look like this.

```auto
func (vs *Server) withdrawer_deposits(
	ctx context.Context,
	beaconState state.BeaconState,
	currentVote *ethpb.Eth1Data,
) ([]*ethpb.Deposit, error) {
	// ...

	var pendingExits []*ethpb.WithdrawerExitContainer
	for i, exit := range allPendingContainers {

		// check of `exit` request validity as it's descripbed in Beacon spec `is_withdrawer_exit_valid`, where `isExitValid` function does the check
		if isExitValid(exit) {
			pendingExits = append(pendingExits, exit)
		}

		// Don't do more than the max allowed amount of checks
		if i == params.BeaconConfig().MaxWithdrawerExitsChecksPerBlock {
		    break
		}

		// Don't try to pack more than the max allowed in a block
		if uint64(len(pendingExits)) == params.BeaconConfig().MaxWithdrawerExitsPerBlock {
			break
		}

	}
	// ...
}
```

So, regarding the desired implementation on the CL client, there are two questions:

1. What is the max amount of is_withdrawer_exit_valid checks per slot from a client performance point of view?
2. Is it reasonable to do the validity checks before the requests get to BeaconBlockBody.withdrawer_exits?

# Security considerations

There is an attack surface when the withdrawer exit request queue gets clogged for a long time by spamming with invalid requests.

### What might be the attack targets?

- Blackmail attack by a validator(-s) threatening to penalize the owner funds
- Attack on staking pools
- Attack on the entire Ethereum protocol

Blackmail attacks by validators seem to be too expensive even for a group of validators.

What happens to the protocol if honest withdrawer exits get blocked for weeks?

It’s not good but not the end of the world. Validator-initiated exits are still available.

It seems that staking pools with untrusted validators are at the most risk. The specific risks and their conditions seem to be much dependent on the pool implementation.

# Questions

1. Should withdrawer exits be added to Shanghai along with the withdrawals?
2. Do you consider the Generalized Message Bus approach worth further development?
3. Are there attacks not outlined in the post?
4. How expensive withdrawer exit validity checks are? Is there a reasonable way to implement them before populating BeaconBlockBody.withdrawer_exits?
5. Better “withdrawer exit” naming?

## Replies

**djrtwo** (2022-05-05):

I would prefer to only introduce a mechanism that is safe from spam of CL through validity conditions on EL.

For example, only one valid exit can/should be made per active validator. Thus you have a very easy way to rate limit if EL has perspective on that which is possible if a beacon_root opcode or some other info is exposed to EL. I’d personally only want to couple this when sufficient proofs can be made in EL to prevent the CL spam, otherwise griefing the ability to exit is too easy.

Similarly, 0x01 rotation (if added) could be rate limited – e.g. one per validator per month – and the EL contract can easily track this (as long as proofs can be made about limited CL state)

1. I don’t think this should be added with withdrawals given the complexity of withdrawals and the many other high priority items attempted to be added. additionally, I only think this is safe for CL with better spam protection which greatly increases the requirements of this proposal
2. Yes, I do agree that EL-based withdrawal credentials should be able to trigger some set of events. At a minimum exits. I’m unsure about the key rotation. that can/should easily be programmed into the 0x01 addr itself… Just use a multisig with some rotation rules or something
3.
4.
5. Maybe ExecutionLayerExit or something

---

**jgm** (2022-05-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/arwer13/48/8826_2.png) arwer13:

> Currently, control over withdrawal credentials doesn’t provide the capability to initiate the validator exit and withdraw the funds

And this was understood from the first version of the beacon chain specifications.  I would be very wary about anything that changed this in case any services relied upon this feature of the specification.

---

**arwer13** (2022-05-06):

I see a trade-off here between

- making EL aware and dependant on the details of CL
- degree of possibility of CL spam

where it is not clear what’s worse.

2 . But we need a way to rotate old 0x01 to the enhanced 0x01 addr in the first place, don’t we?

---

**arwer13** (2022-05-06):

Could you, please, provide an example of such a service or a problem due to the violation of the assumption?

---

**jgm** (2022-05-06):

No idea, I’m not saying that there is anything out there that relies on the specifications.  What I am saying is that there *could* be something out there that relies on the specifications, and changing it could impact them.

If you want a hypothetical: validator key holder runs a validating service on the basis that they charge 50% of the value of the validator over 32 ETH when the withdrawal happens.  They can be sure they will be paid because they can withold the exit transaction until a payment agreement is in place (smart contract, escrow, direct payment, whatever).

---

**A1igator** (2022-05-17):

I would like to propose that this type of proposal might be the only way to keep solo staking competitive with liquid staking options.

Currently a liquid staker can get around 2.5x the returns of a solo staker via usage of leverage such as [icETH | Interest Compounding ETH Index | Index Coop](https://indexcoop.com/interest-compounding-eth-index) with minimal risk

Solo staking needs some kind of liquidity as well to allow borrowing. This seems only possible with allowing protocols to forced exit a validator to get their collateral.

---

**MicahZoltu** (2022-05-18):

Using staked ETH as collateral to borrow is such a bad idea.  It reduces the cost of an attack, and in such case lenders will be wiped out.

---

**arwer13** (2022-05-25):

We’re trying to identify the next steps to elaborate the approach with no CL-aware checks on EL.

It seems, currently the main problem to work on is the question whether it’s OK to not include invalid requests in `BeaconBlockBody`. Namely, from the perspective of capability of lightweight clients to validate the Becon Chain.

If it’s OK, the next question is if the checks on CL clients can be done before the checks for, e. g., the Voluntary Exit requests.

[@djrtwo](/u/djrtwo) and others, what do you think should be our next steps to move this proposal forward?

---

**mkalinin** (2022-06-10):

> It seems, currently the main problem to work on is the question whether it’s OK to not include invalid requests in BeaconBlockBody . Namely, from the perspective of capability of lightweight clients to validate the Becon Chain.

What would be the way to achieve that other than validating requests in the contract? Which would require `BEACONBLOCKROOT` opcode.

---

**ccitizen** (2023-01-13):

Has there been any further discussion on an approach that would allow for exits using only withdrawal credentials?

Likewise, is anybody aware of any further drafting of an EIP proposal in the background that would allow for something like this?

This conversation seems to have been entirely dropped and with withdrawals upcoming this is concerning. To be clear, this is not a criticism of Ethereum contributors.

[@jgm](/u/jgm) you’re always across all critical discussions and your input on this broad conversation since 2020 on the forum and Github has been extremely valuable. Do you have any awareness of additional discussions beyond this latest one?

[@arwer13](/u/arwer13) please share whether further drafts to solve this issue have been discussed with key Ethereum contributors to find a solution that is realistic to include.

---

**ccitizen** (2023-01-13):

[@djrtwo](/u/djrtwo) any input here?

(apologies for double post, can only mention two users per post as a new account on the forum)

---

**jgm** (2023-01-13):

I suspect that once withdrawals are in place any user that is uncomfortable with their reliance on the validator key (or more accurately validator key holder) will exit and re-enter, thus avoiding the issue.

If, once withdrawals are in place, there is a large percentage of validators that cannot withdraw due to recalcitrance on the part of the validator key holder this, or something like this, may become relevant again.

---

**ccitizen** (2023-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> I suspect that once withdrawals are in place any user that is uncomfortable with their reliance on the validator key (or more accurately validator key holder) will exit and re-enter, thus avoiding the issue.

I think this is overly optimistic. We must remember that most stakers are non-technical. Having read a lot of the Lido forums and Discord, and spoken to institutions deploying millions, I’m quite confident that most of the capital in Lido is contributed by people who do not understand that Lido cannot forcefully exit the validators and get the ETH back.

I tend to believe that in the immediate future, this is likely not an issue. Most of the validators are run by reputable node operators, who likely obey the requests.

But, for a long time many of us in the community have been frustrated with the centralization and risk concentration that has happened as a result of Lido.

Yet, there is no way they can improve this without the ability to exit using only withdrawal credentials, without entirely redesigning the protocol, which is unlikely to happen.

Or, perhaps I should say, I truly hope they do not listen to the community and try to decentralize further without first getting a solution to the inability to exit forcibly. But, I fear they likely will.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> If, once withdrawals are in place, there is a large percentage of validators that cannot withdraw due to recalcitrance on the part of the validator key holder this, or something like this, may become relevant again.

I’m not massively concerned that there will be a “large percentage of validators that cannot withdraw due to recalcitrance on the part of the validator key holder”. I’m thinking about the incentives this creates in the system of LSDs, where the node operators need to be a party that can be trusted in this way. This has incentivized heavily centralization beyond what many of us consider ideal, or even acceptable.

Allowing for exits and withdrawals using only the withdrawal credentials makes a significant improvement to the incentives in the system. This improvement could directly lead to meaningful shifts in entity, jurisdiction, server geography and hosting concentrations, by allowing LSDs to admit smaller, solo or anonymous operators into the validator set.

The reality, right now, is that capital concentration is a limiting factor in diversity.  Many operators are willing to run validators, but they do not have the capital, which concentrates with a small group of nodes operators.

Exits using only withdrawal credentials shift the risk calculations massively, allowing LSDs and other parties where the capital is concentrated, to allocate to these new, small or solo operators. Improving diversity and helping to better secure the network.

---

**jgm** (2023-01-17):

Is there any significant difference between exits using withdrawal credentials, and a provider such as Lido holding pre-signed exit transactions provided by their node operators?  The latter requires a bit more effort but has the rather large benefit of existing today.

---

**Wander** (2023-01-17):

Hi all, I’m working on a staking protocol and want to share my POV as well.

First, I agree that most staked ETH will be delegated in the long run, and preparing for this eventuality is important. Ethereum core dev is already behind the LSD market (see [this post](https://old.reddit.com/r/ethereum/comments/107cqi8/ama_we_are_ef_research_pt_9_11_january_2023/j3vy2dz/?context=2) from [@domothy](/u/domothy) during the recent AMA), and it’s important to catch up where possible to reduce added risk for a large portion of the stake.

Second, I respect Lido and believe they will make the right choice on decentralization, but I think it’s important to prioritize improvements which make it safer to run decentralized staking protocols in general. Ideally, Lido decentralizes carefully and many other competitors grow to help divide up the share of stake, but we don’t necessarily live in an ideal world. Lido is a multi-chain DAO which can survive even in the absence of a healthy Ethereum, so it may be unwise to expect caution, especially since it seems that [Lido’s top priority is maintaining and growing market share even when that negatively impacts the health of Ethereum](https://snapshot.org/#/lido-snapshot.eth/proposal/0x10abedcc563b66b1adee60825e78c387105110fa4a1e7354ab57bc9cc1e675c2).

> Is there any significant difference between exits using withdrawal credentials, and a provider such as Lido holding pre-signed exit transactions provided by their node operators?

[@jgm](/u/jgm) Pre-signed exit transactions aren’t valid forever, meaning validators will have to continually submit these in a secure manner to an off-chain protocol administrator. Even if staking protocols go through the effort to implement this scheme, it prevents on-chain automation and therefore stability. Obviously, for Ethereum’s health, we must encourage the stability of staking protocols.

On a more bureaucratic note, there’s clearly a demand for this feature, so how should staking protocols approach this discussion? Is it more important to make the case for prioritization or to iterate on design? I know there are a lot of important features competing for prioritization, but this should be near the top in my opinion, and it seems to me that this approach is sufficient.

---

**ccitizen** (2023-01-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> Is there any significant difference between exits using withdrawal credentials, and a provider such as Lido holding pre-signed exit transactions provided by their node operators?  The latter requires a bit more effort but has the rather large benefit of existing today.

Yes, the former is trustless and allows forceful exits preventing bad actors from holding ETH hostage. It also has the nice ability to allow for mass-exits in a short period, where there might not be sufficient pre-signed messages even among good actors. The ability to forcefully exit is the major difference, which is what changes the incentives here.

The latter has no way to be forced. How do you accurately and reliably check whether a node operator has signed those messages? What do you do if they haven’t? It’s hard to punish the bad actor who does not publish them, because they didn’t publish them, so they can’t be exited.

Messages only last 2 forks and so this needs to be entirely automated. You then need to run an oracle to check on this even, which is another point of centralization, particularly when there is going to be little reward for running this oracle.

---

**Wander** (2023-01-19):

Given that [deposit messages are always valid](https://eth2book.info/altair/part2/building_blocks/signatures#domain-separation-and-forks), could we make that same exception for exit messages? This would solve the problem entirely with a small change to the spec.

The given reasoning for current behavior is that “mixing the fork version into the message ensures that messages from validators that have not upgraded are invalid. They are out of consensus and have no information that is useful to us, so this provides a convenient way to ignore their messages.”

I disagree with this in the case of exits – it is relevant information to the whole CL if a validator wants to exit, and the fork number is irrelevant to that action, just like with deposits.

---

**ccitizen** (2023-01-20):

This partially solves the problem, but not entirely. It is a reasonable solution that does have value though, and could be implemented quite quickly.

If an existing large operator running validators for a LSD pre-signs all of these messages, and they are always valid, at any point the LSD can exit those validators which is fantastic.

But this does not solve the problem of onboarding new operators trustlessly, which is the stem of this issue. An operator would onboard, but could then refuse to sign the message. Automated thousands of times, that’s the same issue as exists now for LSDs.

There would need to be some way to force the validator to send the exit message. At which point, you’re back to the suggestion in the OP essentially.

I do think that this is a good step in the right direction and could be a reasonable enough fix that LSDs could work around. But being able to force the exit with only the withdrawal credentials is, to me, the right solution

---

**Wander** (2023-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/ccitizen/48/11126_2.png) ccitizen:

> An operator would onboard, but could then refuse to sign the message.

Good point. This still helps our project significantly since our system is designed to do operator onboarding via reimbursement (operator creates validator with their own ETH with our contract as the withdrawal address, then is reimbursed), but that still requires an oracle/admin due to EL/CL separation. It’s a lot more stable than the raw permission system that Lido, et al use today, at least.

I’m happy to do the legwork on getting this included in the spec if needed, so I’ll bring this over to the relevant github issue here: [Dual-key voluntary exits · Issue #1578 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/issues/1578)

---

**ccitizen** (2023-01-24):

This would require that the LSD protocol holds the pre-signed (never expiring) exit messages from the validators right? That doesn’t seem like a good, or safe, long term approach. Thoughts?


*(3 more replies not shown)*
