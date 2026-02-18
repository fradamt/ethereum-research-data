---
source: ethresearch
topic_id: 1931
title: "Scheduling contract execution in Ethereum: Chronos"
author: jfdelgad
date: "2018-05-07"
category: Applications
tags: []
url: https://ethresear.ch/t/scheduling-contract-execution-in-ethereum-chronos/1931
views: 4443
likes: 1
posts_count: 7
---

# Scheduling contract execution in Ethereum: Chronos

Given the structure of Ethereum, it is not possible to schedule calls to contracts at a point in the future. This is because contracts can not subscribe to events and therefore all the actions need to be triggered by an entity external to the contract. In many applications, one may be interested in scheduling an operation (transaction, execution of a particular function) in the future. One specific example is the blockchain-based lotteries and other gambling decentralized applications (Dapps) that base the generation of random numbers on network variables. For security reasons, lotteries need to use parameters of the network taken at some time point in the future. Also, some applications require delaying payments (ether transactions) automatically, a seller may decide to wait for a specific number of block-confirmations before doing the final step towards completing a business transaction, etc.

Chronos is a smart contract that does just that. With Chronos, any contract can register a request to be called at a particular block. The smart contract has been designed to be efficient, reducing gas consumption related to the schedule of the execution of calls. Furthermore, the code is fully available on Github and can be used by anyone. The main features of Chronos are:

- Simple integration with your smart contract.
- Allows for withdrawal of the gas-cost not consumed during the call.
- Single or recurrent call to the contract.
- Available on the Test Network (Rinkeby).

It is straightforward to integrate any smart contract with Chronos. Adding two functions into a contract’s code makes it capable of scheduling and receive calls. The code of the smart contract and examples of how to integrate any contract with Chronos can be obtained [here](https://github.com/jfdelgad/Chronos). Chronos is currently available on the test-net (Rinkeby) at this address: [0x4896FE22970B06b778592F9d56F7003799E7400f](https://rinkeby.etherscan.io/address/0x4896FE22970B06b778592F9d56F7003799E7400f)

Chronos is able to solve the problem described but becomes centralized as currently, the execution depends on one administrator. The following step is to allow anyone on the network to be part of the applications such that the system became less centralized and therefore more reliable. This implies to develop a distributed mechanisms for the front end application.

## Replies

**vbuterin** (2018-05-07):

This seems similar to http://www.ethereum-alarm-clock.com; are there any differences between the two?

---

**jfdelgad** (2018-05-07):

Yes, I am aware of EAC. Differences are in implementation. This uses a single contract (in contrast with the implementation of EAC) with a really simple way to call the service from any other contract. To make this as simple as possible was what motivated me to write the code. Furthermore the code create a balance for every contract that uses the service  such that the gas cost not used during execution is accumulated and can be used in the future or can be withdraw. Although this is running on Rinkeby, is still work in progress.

---

**kosecki123** (2018-05-08):

EAC is using separate contracts per scheduled tx purely for security purposes. Having them separated removes attack vectors that can be applied on a honey pot smart contract.

Also please note that our team (besides EAC) is working on Chronos (name collision, yay) which is next-gen EAC (generalized conditional scheduler), this is our EdCon presentation from few days https://youtu.be/NJ9StJThxZY?t=1h49m5s

---

**jfdelgad** (2018-05-08):

The name collision is unfortunate. I know the EAC and I think is a rather complicated (yet elegant) way to do something that is in essence simple. Let me list what I think are the main differences between EAC, your system, and what I propose:

1. Simplicity: The system that I propose works like this: a) subject request to be called at a particular block (this can directly be extended to time), and forwards the gas cost required. Chronos receive and store the information about the execution request, an off-chain system receive the events and at the requested time execute a callback function in the target contract. There is a fee that is used to incentivize people to execute the call.
2. Chronos creates a balance for each contract so that the gas cost not used is available for future call request or can be withdrawn (the funds are sent to the user contract ). Also, contracts could just fund their accounts on Chronos avoiding the possibility of the gas passed is not enough as the gas price can change with time. All of this has no fees in the system.
3. The gas cost is several times lower than EAC and therefore is lower than in your system. You can see examples of this in the link I publish above, I have several contracts requesting recurrent calls to Chronos, you can see the gas cost used to callback those contracts (the only function of those contracts is to increase a counter)
4. There is no need to release a token for this as I think you suggest in your talk (Let me know if I misunderstood)

The next step in my development is to allow anyone to be an executor of calls. My preliminary work on this does not have the problem of collision (several executor trying to execute the same request) because the contract also schedules who will have priority on the execution of the most recent call. Basically, executors register to the smart contract and the contract assign slots by looping through the list of registered executor such that everyone is treated equally.

Furthermore, to ensure the execution of the call, executors are deleted from the list (they can register again) if they fail to execute the call assigned to them, but the call is still executed by the next executor in the registered list. One may also enforce this by requiring the executors to put on hold an amount equal to the fee that they get paid. The software that the executor runs, communicates with other executors in a p2p fashion and in this way is known who is online to prevent for calls executions to be missed.

I think this is simple to use, is cheap for the final user and is robust.

Note: I have not made any audit of the contract yet, this is work in progress and there is still work to do.

I may, of course, be missing something. I am looking forward to hearing your comments.

---

**lsaether** (2018-05-08):

Hello, I am another developer who is working on the [Ethereum Alarm Clock](https://github.com/ethereum-alarm-clock/ethereum-alarm-clock%5D) / the [Chronos Protocol](https://github.com/chronologic/chronos). I do think that the two projects appear outwardly similar but are actually different. Namely, I think that what Chronos (this one) is attempting to accomplish is a simple Javascrip-like callback to smart contracts that trigger the fallback function. This requires a deeper level of architectural design from third party developers than what is required to use the EAC for basic smart contract automation calls. In the EAC, a scheduler can pass arbitrary bytecode to be executed. I’m not sure I saw this feature in Chronos (this one).

![](https://ethresear.ch/user_avatar/ethresear.ch/jfdelgad/48/1295_2.png) jfdelgad:

> My preliminary work on this does not have the problem of collision (several executor trying to execute the same request) because the contract also schedules who will have priority on the execution of the most recent call. Basically, executors register to the smart contract and the contract assign slots by looping through the list of registered executor such that everyone is treated equally.

This of course has its tradeoffs like everything else. We’ve considered something similar for EAC / Chronos Protocol but have settled to using a [Priority Queue](https://github.com/chronologic/chronos/blob/master/contracts/PriorityQueue.sol) with executors (Timenodes) staking bonds which position them in higher places in the queue. For this bond we are experimenting with using a token but, I want to highlight that this is not the EAC which uses this but our Chronos protocol which is currently a work in progress.

Either way I think this is very constructive to bring to the table different implementations of schedulers and I think that the trade offs you make for a simpler API and gas optimzations may be different from some of the tradeoffs we’ve made in the EAC, namely trying to create a general purpose time-based scheduling service for all layers of the stack from solidity devs to end application users.

How much gas is currently used for scheduling each execution call? In Chronos we’ve optimized more than we did in EAC and have gotten it to about 200k gas but might be able to bring this lower. We are trying to balance how much state we have to store on chain versus how much can be kept as simply a hash of the input.

---

**jfdelgad** (2018-05-09):

Hi,

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/l/c0e974/48.png) lsaether:

> This requires a deeper level of architectural design from third party developers than what is required to use the EAC for basic smart contract automation calls.

I do not agree with this claim, the method I proposed imply to include a function (provided by Chronos) to call the service and one to receive the call, I do not see how this could be defined as a requirement for “deeper architectural design” on the side of the user.

I do not include arbitrary bytecode execution because I think this opens a lot of questions about security for the executors or many situations that may cause failure of the transactions, which will hurt mainly to the executors. I assume you have come up with solutions for this.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/l/c0e974/48.png) lsaether:

> How much gas is currently used for scheduling each execution call? In Chronos we’ve optimized more than we did in EAC and have gotten it to about 200k gas but might be able to bring this lower. We are trying to balance how much state we have to store on chain versus how much can be kept as simply a hash of the input.

The gas used for calling back a contract is about 60K, but I did not try to optimize it yet, so I am confident that I can bring it down. This value is the cost of calling the function, the total price will then depend on how complex is the function called which is not under the control of Chronos.

I still do not understand why you would like to release a token, Ether will work just fine for this.

I do agree with you that our approaches are different and that each solution has its tradeoffs. My solution has the purpose to solve a demand that I saw in forums, articles, and personal discussions. Future needs will decide if more features should be incorporated as the demand for these features appears, adding them now will just you put all the load (in terms of complexity and cost ) in the users of today, that as far as I can see, are demanding nothing but an easy, not expensive way for scheduling the execution of particular functions in their contracts.

As always, I may be missing something here, therefore I am always interested in hearing comments. I appreciate your explanations and our differences in the view of the problem are nothing but enriching.

