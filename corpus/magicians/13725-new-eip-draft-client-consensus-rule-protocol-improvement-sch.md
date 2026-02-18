---
source: magicians
topic_id: 13725
title: "New EIP Draft: Client consensus rule protocol improvement scheme based on DVT technology"
author: Ken0928.eth
date: "2023-04-08"
category: EIPs
tags: [dvt, client]
url: https://ethereum-magicians.org/t/new-eip-draft-client-consensus-rule-protocol-improvement-scheme-based-on-dvt-technology/13725
views: 566
likes: 0
posts_count: 5
---

# New EIP Draft: Client consensus rule protocol improvement scheme based on DVT technology

## Abstract

We hope to improve the etheric fang interest specification ([GitHub - ethereum/execution-specs: Specification for the Execution Layer. Tracking network upgrades.](https://github.com/ethereum/execution-specs)) in the consensus of the specifications related to the client, to encourage each client to join the DVT options, or new client development team to develop new clients with DVT options. This proposal aims to enrich the diversity of clients, improve the risk of Ethereum central attack, and make the effect of DVT networks run more stably, so as to effectively reduce the risk of penalty and slash.

## Motivation

At present, ETH has potential risks of consensus layer centralization, which is reflected in wealth centralization, hardware centralization, client centralization, geographical centralization and other aspects. These centralization risks will endanger the security of the Ethereum ecosystem under certain conditions. Therefore, it is necessary to reduce the centralization risk of the Ethereum ecosystem at the consensus level as much as possible. We hope to introduce DVT technology at the client level to improve the client consensus layer specification. The improvement of the client consensus specification can reduce the possibility of various centralized attacks, enrich the diversity of clients and make the corresponding validitor network of each client more stable.

## Specification

### Definition

Single DVT network: A network composed of operators related to validitor private key share fragments, assuming that the validation private key is divided into P pieces, there are P operators in this single network, and 4 operators in SSV form a single DVT network.

Client DVT network: The DVT network is composed of all operators and the corresponding validitor in this client that selects the DVT protocol scheme.

In a single DVT network, f is the maximum number of operators that can ensure the normal operation of all validators in the network, which usually satisfies the number of operators P&gt in the network. It’s equal to 3F plus 1. f is the current number of operator outages in a single network.

In a client DVT network, n is the total number of operators and N is the total number of validators;

## Rationale

**Additional client functionality:**

- Run the view feature:

In the client, it is possible to view the current validitor situation of the solo staking and the validitor situation of the staking using the DVT technique.

- DVT technology selection function:

An operator in the process of adding a validitor, the client provides the option to use the client’s DVT staking solution/to make a separate staking.

The individual staking scheme is the original client-side functionality, so I won’t add anything else here.

- Features related to DVT staking solutions

This is explained in the next section

**Features related to DVT staking solutions**

- Operation 1: validitor entry mechanism

Operator opens client; Request to add a new Validitor with 32ETH; Client checks operator condition (existing mechanism); Make DVT/non-DVT selection - choose DVT modes 3-4, 5-7, etc.; staking ETH; At the same time, the system uses DKG to distribute the verification private key fragments to the existing operators in the DVT network system including itself, and retains the complete verification private key as a disaster recovery scheme; Start PoS

- Operation 2: Validitor exit mechanism:

operator requests to withdraw validitor from a DVT protocol; Initiate all balance withdrawals; Validation private keys in the hands of other operators are invalidated and removed.

- Operation 3: Operator exit mechanism:

operator applies for exit; Exit your validitor with Operation; The fragments of other operator verification private keys are randomly distributed to other unrelated operators

**Initial setup**

- The entry process of the first P − 1 operators:

After selecting the DVT technical scheme, the complete verification private key is also temporarily used for solo staking, but the verification private key fragments are saved by themselves at the same time. When P operators enter the network, their verification private keys are allocated to the DVT network.

- Exit procedure for the p-th operator:

The fourth to last operator of the client requests to quit; Directly destroy the private keys of other operators; The rest operators automatically convert to using their own full verification private key solo staking;

Other possible situations and problems

No forced exit limits or downtime penalties: no forced exit mechanism is triggered even when the operator is too inefficient. The reason why the outage is not punished is that DVT is meant to avoid the slash penalty to a greater extent, so there is no outage penalty, and the mechanism is simplified.

## Backwards Compatibility

This EIP does not change the consensus layer, so there is no backward compatibility issue with this EIP for Ethereum as a whole. Also, it can be compatible with existing clients, but unfortunately, existing non-DVT validitor cannot be added to the network because these accounts did not opt in to DVT during the initial process.

## Reference Implementation

- Technical reference implementation when P<3f+1

//The bool function BLSValid determines whether a fragment collection is valid

def BLSValid(ShareList):

if (len(ShareList) < n - f):

return False

//And a series of other Share sets meet the requirements of the condition judgment;

//Reconstruct Validitor private key

def ValiditorPrivateKeyGen:

if (BLSValid(BLSsign)):

//If the current BLS signature is valid, the BLS signature is preferred and the use of the full verification private key must not be triggered

ValiditorPrivateKey = BLS(ShareList);

else:

//Disaster recovery scheme: If more than f operators are down in a single DVT network, the corresponding contract /validitor takes out its complete ValiditorPrivateKey to sign. ValiditorPrivateKey = this.ValiditorPrivateKey;

Return ValiditorPrivateKey;

## Security Considerations

Whether the DVT connectivity between clients will increase the risk of centralization is a point worth studying later. This solution makes the client more complex to some extent; There are potential security risks of DVT protocol attacks during client upgrade.

## Replies

**Ken0928.eth** (2023-04-08):

This is just a preliminary idea. If it makes sense, we can continue to discuss it.

---

**Ken0928.eth** (2023-04-08):

Author: Ken0928.eth, 0xBlueshark, Alina Li, Jay Lin,  Claudia Wang, Maverick

---

**Ken0928.eth** (2023-04-11):

If You are interested in it, my twitter is @wakk87

---

**Ken0928.eth** (2023-04-17):

If someone interested in it？

