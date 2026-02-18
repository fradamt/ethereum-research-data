---
source: magicians
topic_id: 14561
title: A Proposal for Contrab-like Functionality on Ethereum
author: alvinwo
date: "2023-06-03"
category: EIPs
tags: [erc, dapps]
url: https://ethereum-magicians.org/t/a-proposal-for-contrab-like-functionality-on-ethereum/14561
views: 585
likes: 6
posts_count: 6
---

# A Proposal for Contrab-like Functionality on Ethereum

Greetings, fellow Ethereum enthusiasts!

I’m currently exploring the idea of creating a crontab-like functionality for Ethereum. This would introduce a uniform interface for scheduling contracts, allowing any user to deploy one or more of these contracts, deposit assets to them, and set up automated tasks alongside their execution prerequisites. Imagine these contracts functioning similar to a trust fund for your cryptocurrencies, where designated agents check task conditions and execute them on your behalf.

I’ve been working on a potential solution (WIP) and would love your feedback: [GitHub - alvinwo/ProjectX](https://github.com/alvinwo/ProjectX).

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface CrontabInterface {
    struct Job {
        bool isValid;
        string title;
        string description;
        uint256 reward;
        uint256 expiration;
        uint256 lastExecutionTime;
        uint256 lastExecutionBlock;
        uint[] conditionsList;
        uint[] actionList;
    }

    struct ConditionDefinition {
        ConditionType conditionType;
        // should only be used for the TIME_BASED conditions and CONTRACT_INTERACTION_BASED conditions
        uint256 timeInterval;
        // should only be used for the BLOCK_BASED conditions and CONTRACT_INTERACTION_BASED conditions
        uint256 blockNumberInterval;
        // TODO support contract condition later
    }

    enum ConditionOperator {
        AND,
        OR
    }

    enum ConditionType {
        TIME_BASED,
        BLOCK_BASED,
        CONTRACT_INTERACTION_BASED
    }

    struct ActionDefinition {
        ActionType actionType;
        address targetAddress;
        uint256 value;
    }

    enum ActionType {
        TRANSFER
    }

    // function getAllJobs() external view virtual returns (Job[] memory);

    // function getJob(uint jobId) external view returns (Job memory);

    function createCondition(
        ConditionType conditionType,
        uint256 timeInterval,
        uint256 blockNumberInterval
    ) external returns (uint);

    function createAction(
        ActionType actionType,
        address targetAddress,
        uint256 value
    ) external returns (uint);

    function createJob(
        string memory title,
        string memory description,
        uint256 reward,
        uint256 expiration,
        uint[] memory conditions,
        uint[] memory actions
    ) external returns (uint);

    function deposit() external payable;

    // the onwer could withdraw the deposited assets
    function withdraw(uint256 value) external returns (bool);

    function getOwner() external view returns (address);

    function triggerJob(uint jobId) external;

    event Deposit(address indexed owner, uint256 value);
    event Withdraw(address indexed owner, uint256 value);
    event ActionAdded(address indexed owner, uint actionId, ActionDefinition action);
    event ConditionAdded(address indexed owner, uint conditionId, ConditionDefinition condition);
    event JobAdded(address indexed owner, uint jobId, Job job);
    // event JobModified(address indexed _owner, Job job);
    // event JobRemoved(address indexed _owner, Job job);
    event JobExecuted(address indexed owner, address indexed trigger, uint jobId);
}
```

Are there any existing standards or solutions that closely resemble this? I’m also curious to gauge the demand for such an on-chain crontab system. Do you believe there’s a real need for this? Your thoughts and feedback would be greatly appreciated.

## Replies

**ulerdogan** (2023-06-03):

Hi, congrats on the work! Have you checked Chainlink’s [Automation](https://docs.chain.link/chainlink-automation/introduction) solution?

---

**alvinwo** (2023-06-04):

Thanks mate! I’m going to take a look.

---

**abcoathup** (2023-06-05):

Also look at OpenZeppelin Defender and Gelato


      ![](https://ethereum-magicians.org/uploads/default/original/2X/0/00666912b7046afbb017a1accf1a50ad7b7f18e4.png)

      [LogRocket Blog – 8 Aug 22](https://blog.logrocket.com/tools-smart-contract-automation-guide/)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/5/5b9a99eacac2558150a3038cf8f6fa7a738b9634.png)

###



Learn about the core concepts of smart contract automation and the pros and cons of popular smart contract automation tools.



    Est. reading time: 16 minutes

---

**joeblogg801** (2023-06-08):

One of the earliest proposals in the realm of decentralized scheduling that I am aware of is the Ethereum Alarm Clock. The Ethereum Alarm Clock project, which can be found at this GitHub repository: [GitHub - ethereum-alarm-clock/ethereum-alarm-clock: Schedule transactions for the future](https://github.com/ethereum-alarm-clock/ethereum-alarm-clock), was introduced around 2015 and remained active for a couple of years thereafter.

Although the original website associated with the project appears to be unavailable at present, the smart contracts developed for the Ethereum Alarm Clock should still be deployed on the Ethereum mainnet. This project holds significance as an early demonstration of the concept of Miner Extractable Value (MEV). It allowed anyone to receive a payment for invoking scheduled contract calls, marking an early exploration of the possibilities for incentivizing such actions within the Ethereum ecosystem.

---

**alvinwo** (2023-06-08):

Hi [@abcoathup](/u/abcoathup) [@joeblogg801](/u/joeblogg801) , thanks so much for your sharing. My motivation for considering this idea stems from the thought of preserving my tokens for my loved ones in the event of my unforeseen demise. By establishing an inactivity period, my tokens could be automatically distributed as per my wishes if I were to become inactive. This approach mitigates the risk of token loss and eliminates the need to expose my private key.

Are you aware of how popular these automation frameworks are? Do they see many usage in real cryptocurrency world?

