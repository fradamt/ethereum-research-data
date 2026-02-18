---
source: magicians
topic_id: 12316
title: "EIP-6224: Contracts Dependencies Registry"
author: Arvolear
date: "2022-12-29"
category: EIPs
tags: [smart-contracts, registry, dependencies]
url: https://ethereum-magicians.org/t/eip-6224-contracts-dependencies-registry/12316
views: 3509
likes: 11
posts_count: 15
---

# EIP-6224: Contracts Dependencies Registry

## Abstract

This EIP introduces an on-chain registry system that a decentralized protocol may use to manage its smart contracts.

The proposed system consists of two components: `ContractsRegistry` and `Dependant`. The `ContractsRegistry` contract stores references to every smart contract used within a protocol, optionally making them upgradeable by deploying self-managed proxies on top, and acts as a hub the `Dependant` contracts query to fetch their required dependencies from.

## Motivation

In the ever-growing Ethereum ecosystem, projects tend to become more and more complex. Modern protocols require portability and agility to satisfy customer needs by continuously delivering new features and staying on pace with the industry. However, the requirement is hard to achieve due to the immutable nature of blockchains and smart contracts. Moreover, the increased complexity and continuous delivery bring bugs and entangle the dependencies between the contracts, making systems less supportable.

Applications that have a clear architectural facade; which are designed with forward compatibility in mind; which dependencies are transparent and clean are easier to develop and maintain. The given EIP tries to solve the aforementioned problems by presenting two smart contracts: the `ContractsRegistry` and the `Dependant`.

The advantages of using the provided system might be:

- Structured smart contracts management via specialized contracts.
- Ad-hoc upgradeability provision of a protocol.
- Runtime addition, removal, and substitution of smart contracts.
- Dependency injection mechanism to keep smart contracts’ dependencies under control.
- Ability to specify custom access control rules to maintain the protocol.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Overview

The system consists of two smart contracts:

- ContractsRegistry that is a singleton registry to manage and upgrade a protocol’s smart contracts.
- Dependant that is a mix-in which enables a dependency injection mechanism.

The following diagram depicts the relationship between the registry and its dependants:

[![diagram](https://ethereum-magicians.org/uploads/default/optimized/2X/3/34714099c8e66681ee694b0d556fb2fdab4c3846_2_587x499.png)diagram944×804 15.8 KB](https://ethereum-magicians.org/uploads/default/34714099c8e66681ee694b0d556fb2fdab4c3846)

### ContractsRegistry

The `ContractsRegistry` is the main contract of the proposed system. It MUST store the references to every standalone contract used within a protocol. The `ContractRegistry` MAY be configured to deploy a proxy contract of choice on top of the registered contracts.

Additionally, the `ContractsRegistry` MUST reject the registration of zero addresses.

The `ContractsRegistry` MUST implement the following interface:

```solidity
pragma solidity ^0.8.0;

interface IContractsRegistry {
    /**
     * @notice The event that is emitted when the contract gets added to the registry
     * @param name the name of the contract
     * @param contractAddress the address of the added contract
     */
    event ContractAdded(string name, address contractAddress);

    /**
     * @notice The event that is emitted when the proxy contract gets added to the registry
     * @param name the name of the contract
     * @param contractAddress the address of the proxy contract
     * @param implementation the address of the implementation contract
     */
    event ProxyContractAdded(string name, address contractAddress, address implementation);

    /**
     * @notice The event that is emitted when the proxy contract gets upgraded through the registry
     * @param name the name of the contract
     * @param newImplementation the address of the new implementation contract
     */
    event ProxyContractUpgraded(string name, address newImplementation);

    /**
     * @notice The event that is emitted when the contract gets removed from the registry
     * @param name the name of the removed contract
     */
    event ContractRemoved(string name);

    /**
     * @notice The function that returns an associated contract by the name.
     *
     * MUST revert if the requested contract is `address(0)`
     *
     * @param name the name of the contract
     * @return the address of the contract
     */
    function getContract(string memory name) external view returns (address);

    /**
     * @notice The function that checks if a contract with a given name has been added
     * @param name the name of the contract
     * @return true if the contract is present in the registry
     */
    function hasContract(string memory name) external view returns (bool);

    /**
     * @notice The function that injects dependencies into the given contract.
     *
     * MUST call the `setDependencies()` with `address(this)` and `bytes("")` as arguments on the provided contract
     *
     * @param name the name of the contract
     */
    function injectDependencies(string memory name) external;

    /**
     * @notice The function that injects dependencies into the given contract with extra data.
     *
     * MUST call the `setDependencies()` with `address(this)` and `data` as arguments on the provided contract
     *
     * @param name the name of the contract
     * @param data the extra context data that will be passed to the dependant contract
     */
    function injectDependenciesWithData(
        string memory name,
        bytes memory data
    ) external;

    /**
     * @notice The function that upgrades added proxy contract with a new implementation.
     *
     * It is the Owner's responsibility to ensure the compatibility between implementations.
     *
     * MUST emit `ProxyContractUpgraded` event
     *
     * @param name the name of the proxy contract
     * @param newImplementation the new implementation the proxy will be upgraded to
     */
    function upgradeContract(string memory name, address newImplementation) external;

    /**
     * @notice The function that upgrades added proxy contract with a new implementation, providing data
     *
     * It is the Owner's responsibility to ensure the compatibility between implementations.
     *
     * MUST emit `ProxyContractUpgraded` event
     *
     * @param name the name of the proxy contract
     * @param newImplementation the new implementation the proxy will be upgraded to
     * @param data the data that the proxy will be called with after upgrade. This can be an ABI encoded function call
     */
    function upgradeContractAndCall(
        string memory name,
        address newImplementation,
        bytes memory data
    ) external;

    /**
     * @notice The function that adds pure (non-proxy) contracts to the `ContractsRegistry`. The contracts MAY either be
     * the ones the system does not have direct upgradeability control over or those that are not upgradeable by design.
     *
     * MUST emit `ContractAdded` event. Reverts if the provided address is `address(0)`
     *
     * @param name the name to associate the contract with
     * @param contractAddress the address of the contract to be added
     */
    function addContract(string memory name, address contractAddress) external;

    /**
     * @notice The function that adds the proxy contracts to the registry by deploying them above the provided implementation.
     *
     * The function may be used to add a contract that the `ContractsRegistry` has to be able to upgrade.
     *
     * MUST emit `ProxyContractAdded` event. Reverts if implementation address is `address(0)`
     *
     * @param name the name to associate the contract with
     * @param contractAddress the address of the implementation to point the proxy to
     */
    function addProxyContract(string memory name, address contractAddress) external;

    /**
     * @notice The function that adds the proxy contracts to the registry by deploying them above the provided implementation,
     * providing data.
     *
     * The function may be used to add a contract that the `ContractsRegistry` has to be able to upgrade.
     *
     * MUST emit `ProxyContractAdded` event. Reverts if implementation address is `address(0)`
     *
     * @param name the name to associate the contract with
     * @param contractAddress the address of the implementation
     * @param data the data that the proxy will be called with. This can be an ABI encoded initialization call
     */
    function addProxyContractAndCall(
        string memory name,
        address contractAddress,
        bytes memory data
    ) external;

    /**
     * @notice The function that adds an already deployed proxy to the `ContractsRegistry`. It MAY be used
     * when the system migrates to the new `ContractRegistry`. In that case, the new registry MUST have the
     * credentials to upgrade the newly added proxies.
     *
     * MUST emit `ProxyContractAdded` event. Reverts if implementation address is `address(0)`
     *
     * @param name the name to associate the contract with
     * @param contractAddress the address of the proxy
     */
    function justAddProxyContract(string memory name, address contractAddress) external;

    /**
     * @notice The function to remove contracts from the ContractsRegistry.
     *
     * MUST emit `ContractRemoved` event. Reverts if the contract is already removed
     *
     * @param name the associated name with the contract
     */
    function removeContract(string memory name) external;
}
```

### Dependant

The `ContractsRegistry` works together with the `Dependant` contract. Every standalone contract of a protocol MUST inherit `Dependant` in order to support the dependency injection mechanism.

The required dependencies MUST be set in the overridden `setDependencies` method, not in the `constructor` or `initializer` methods.

Only the injector MUST be able to call the `setDependencies` and `setInjector` methods. The initial injector will be a zero address, in that case, the call MUST NOT revert on access control checks.

The `Dependant` contract MUST implement the following interface:

```solidity
pragma solidity ^0.8.0;

interface IDependant {
    /**
     * @notice The function that is called from the `ContractsRegistry` to inject dependencies.
     *
     * The contract MUST perform a proper access check of `msg.sender`. The calls should only be possible from `ContractsRegistry`
     *
     * @param contractsRegistry the registry to pull dependencies from
     * @param data the extra data that might provide additional application-specific context
     */
    function setDependencies(address contractsRegistry, bytes memory data) external;

    /**
     * @notice The function that sets the new dependency injector.
     *
     * The contract MUST perform proper access check of `msg.sender`
     *
     * @param injector the new dependency injector
     */
    function setInjector(address injector) external;

    /**
     * @notice The function that gets the current dependency injector
     * @return the current dependency injector
     */
    function getInjector() external view returns (address);
}
```

- The Dependant contract MAY store the dependency injector (usually ContractsRegistry) address in the special slot 0x3d1f25f1ac447e55e7fec744471c4dab1c6a2b6ffb897825f9ea3d2e8c9be583 (obtained as bytes32(uint256(keccak256("eip6224.dependant.slot")) - 1)).

## Rationale

There are a few design decisions that have to be explicitly specified:

### ContractsRegistry Rationale

#### Contracts Identifier

The `string` contracts identifier is chosen over the `uint256` and `bytes32` to maintain code readability and reduce the human error chances when interacting with the `ContractsRegistry`. Being the topmost smart contract of a protocol, it MAY be typical for the users to interact with it via block explorers or DAOs. Clarity was prioritized over gas usage.

Due to the `string` identifier, the event parameters are not indexed. The `string indexed` parameter will become the `keccak256` hash of the contract name if it is larger than 32 bytes. This fact reduces readability, which was prioritized.

#### Reverts

The `getContract` view function reverts if the requested contract is `address(0)`. This is essential to minimize the risks of misinitialization of a protocol. Correct contracts SHOULD be added to the registry prior to any dependency injection actions.

The `addContract`, `addProxyContract`, `addProxyContractAndCall`, and `justAddProxyContract` methods revert if the provided address is `address(0)` for the same risk minimization reason.

### Dependant Rationale

#### Dependencies

The `data` parameter is provided to carry additional application-specific context. It MAY be used to extend the method’s behavior.

#### Injector

The `setInjector` function is made `external` to support the dependency injection mechanism for factory-made contracts. However, the method SHOULD be used with extra care.

## Reference Implementation

> Note that the reference implementation depends on OpenZeppelin contracts 4.9.2.

### ContractsRegistry Implementation

```solidity
pragma solidity ^0.8.0;

import {Address} from "@openzeppelin/contracts/utils/Address.sol";
import {TransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

import {Dependant} from "./Dependant.sol";

interface IContractsRegistry {
    event ContractAdded(string name, address contractAddress);
    event ProxyContractAdded(
        string name,
        address contractAddress,
        address implementation
    );
    event ProxyContractUpgraded(string name, address newImplementation);
    event ContractRemoved(string name);

    function getContract(string memory name) external view returns (address);

    function hasContract(string memory name) external view returns (bool);

    function injectDependencies(string memory name) external;

    function injectDependenciesWithData(string memory name, bytes memory data)
        external;

    function upgradeContract(string memory name, address newImplementation)
        external;

    function upgradeContractAndCall(
        string memory name,
        address newImplementation,
        bytes memory data
    ) external;

    function addContract(string memory name, address contractAddress) external;

    function addProxyContract(string memory name, address contractAddress)
        external;

    function addProxyContractAndCall(
        string memory name,
        address contractAddress,
        bytes memory data
    ) external;

    function justAddProxyContract(string memory name, address contractAddress)
        external;

    function removeContract(string memory name) external;
}

contract ProxyUpgrader {
    using Address for address;

    address private immutable _OWNER;

    modifier onlyOwner() {
        _onlyOwner();
        _;
    }

    constructor() {
        _OWNER = msg.sender;
    }

    function upgrade(address what_, address to_, bytes calldata data_) external onlyOwner {
        if (data_.length > 0) {
            TransparentUpgradeableProxy(payable(what_)).upgradeToAndCall(to_, data_);
        } else {
            TransparentUpgradeableProxy(payable(what_)).upgradeTo(to_);
        }
    }

    function getImplementation(address what_) external view onlyOwner returns (address) {
        // bytes4(keccak256("implementation()")) == 0x5c60da1b
        (bool success_, bytes memory returndata_) = address(what_).staticcall(hex"5c60da1b");

        require(success_, "ProxyUpgrader: not a proxy");

        return abi.decode(returndata_, (address));
    }

    function _onlyOwner() internal view {
        require(_OWNER == msg.sender, "ProxyUpgrader: not an owner");
    }
}

contract ContractsRegistry is IContractsRegistry, OwnableUpgradeable {
    ProxyUpgrader private _proxyUpgrader;

    mapping(string => address) private _contracts;
    mapping(address => bool) private _isProxy;

    function __ContractsRegistry_init() public initializer {
        _proxyUpgrader = new ProxyUpgrader();

        __Ownable_init();
    }

    function getContract(string memory name_) public view returns (address) {
        address contractAddress_ = _contracts[name_];

        require(
            contractAddress_ != address(0),
            "ContractsRegistry: this mapping doesn't exist"
        );

        return contractAddress_;
    }

    function hasContract(string memory name_) public view returns (bool) {
        return _contracts[name_] != address(0);
    }

    function getProxyUpgrader() external view returns (address) {
        return address(_proxyUpgrader);
    }

    function injectDependencies(string memory name_) public virtual onlyOwner {
        injectDependenciesWithData(name_, bytes(""));
    }

    function injectDependenciesWithData(string memory name_, bytes memory data_)
        public
        virtual
        onlyOwner
    {
        address contractAddress_ = _contracts[name_];

        require(
            contractAddress_ != address(0),
            "ContractsRegistry: this mapping doesn't exist"
        );

        Dependant dependant_ = Dependant(contractAddress_);
        dependant_.setDependencies(address(this), data_);
    }

    function upgradeContract(string memory name_, address newImplementation_)
        public
        virtual
        onlyOwner
    {
        upgradeContractAndCall(name_, newImplementation_, bytes(""));
    }

    function upgradeContractAndCall(
        string memory name_,
        address newImplementation_,
        bytes memory data_
    ) public virtual onlyOwner {
        address contractToUpgrade_ = _contracts[name_];

        require(
            contractToUpgrade_ != address(0),
            "ContractsRegistry: this mapping doesn't exist"
        );
        require(
            _isProxy[contractToUpgrade_],
            "ContractsRegistry: not a proxy contract"
        );

        _proxyUpgrader.upgrade(contractToUpgrade_, newImplementation_, data_);

        emit ProxyContractUpgraded(name_, newImplementation_);
    }

    function addContract(string memory name_, address contractAddress_)
        public
        virtual
        onlyOwner
    {
        require(
            contractAddress_ != address(0),
            "ContractsRegistry: zero address is forbidden"
        );

        _contracts[name_] = contractAddress_;

        emit ContractAdded(name_, contractAddress_);
    }

    function addProxyContract(string memory name_, address contractAddress_)
        public
        virtual
        onlyOwner
    {
        addProxyContractAndCall(name_, contractAddress_, bytes(""));
    }

    function addProxyContractAndCall(
        string memory name_,
        address contractAddress_,
        bytes memory data_
    ) public virtual onlyOwner {
        require(
            contractAddress_ != address(0),
            "ContractsRegistry: zero address is forbidden"
        );

        address proxyAddr_ = _deployProxy(
            contractAddress_,
            address(_proxyUpgrader),
            data_
        );

        _contracts[name_] = proxyAddr_;
        _isProxy[proxyAddr_] = true;

        emit ProxyContractAdded(name_, proxyAddr_, contractAddress_);
    }

    function justAddProxyContract(string memory name_, address contractAddress_)
        public
        virtual
        onlyOwner
    {
        require(
            contractAddress_ != address(0),
            "ContractsRegistry: zero address is forbidden"
        );

        _contracts[name_] = contractAddress_;
        _isProxy[contractAddress_] = true;

        emit ProxyContractAdded(
            name_,
            contractAddress_,
            _proxyUpgrader.getImplementation(contractAddress_)
        );
    }

    function removeContract(string memory name_) public virtual onlyOwner {
        address contractAddress_ = _contracts[name_];

        require(
            contractAddress_ != address(0),
            "ContractsRegistry: this mapping doesn't exist"
        );

        delete _isProxy[contractAddress_];
        delete _contracts[name_];

        emit ContractRemoved(name_);
    }

    function _deployProxy(
        address contractAddress_,
        address admin_,
        bytes memory data_
    ) internal virtual returns (address) {
        return
            address(
                new TransparentUpgradeableProxy(contractAddress_, admin_, data_)
            );
    }
}
```

### Dependant Implementation

```solidity
pragma solidity ^0.8.0;

interface IDependant {
    function setDependencies(address contractsRegistry, bytes memory data) external;

    function setInjector(address injector) external;

    function getInjector() external view returns (address);
}

abstract contract Dependant is IDependant {
    /**
     * @dev bytes32(uint256(keccak256("eip6224.dependant.slot")) - 1)
     */
    bytes32 private constant _INJECTOR_SLOT =
        0x3d1f25f1ac447e55e7fec744471c4dab1c6a2b6ffb897825f9ea3d2e8c9be583;

    modifier dependant() {
        _checkInjector();
        _;
        _setInjector(msg.sender);
    }

    function setDependencies(address contractsRegistry_, bytes memory data_) public virtual;

    function setInjector(address injector_) external {
        _checkInjector();
        _setInjector(injector_);
    }

    function getInjector() public view returns (address injector_) {
        bytes32 slot_ = _INJECTOR_SLOT;

        assembly {
            injector_ := sload(slot_)
        }
    }

    function _setInjector(address injector_) internal {
        bytes32 slot_ = _INJECTOR_SLOT;

        assembly {
            sstore(slot_, injector_)
        }
    }

    function _checkInjector() internal view {
        address injector_ = getInjector();

        require(injector_ == address(0) || injector_ == msg.sender, "Dependant: not an injector");
    }
}
```

## Security Considerations

It is crucial for the owner of `ContractsRegistry` to keep their keys in a safe place. The loss/leakage of credentials to the `ContractsRegistry` will lead to the application’s point of no return. The `ContractRegistry` is a cornerstone of a protocol, access must be granted to the trusted parties only.

### ContractsRegistry Security

- The ContractsRegistry does not perform any upgradeability checks between the proxy upgrades. It is the user’s responsibility to make sure that the new implementation is compatible with the old one.

### Dependant Security

- The Dependant contract MUST set its dependency injector no later than the first call to the setDependencies function is made. That being said, it is possible to front-run the first dependency injection.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**xinbenlv** (2023-01-03):

[@Arvolear](/u/arvolear) thank you for this proposal. It looks very important. Two questions

1. Do you anticipate the addProxyContract  and justAddProxyContract  to be guarded by access control?
2. Do you anticipate the setInjector to carry additional context at any case?

---

**Arvolear** (2023-01-04):

Hey, [@xinbenlv](/u/xinbenlv), thank you very much for the feedback.

1. Yes, to be precise, all the non-view functions should be guarded by access control. It may be as simple as Ownable from Openzeppelin or as complex as a custom DAO. You can find the Ownable preset right here.
2. Actually it might. The injector is a special account that has permission of injecting dependencies into the dependant contracts. Here, the ContractsRegistry possesses both roles: injector and registry. However, these roles may be split and used separately. There is a case with a factory that deploys dependant contracts where the separation becomes visible. The factory would temporarily become the injector to provide the necessary dependencies upon deployment and set the injector to a proper contract afterward.

---

**xinbenlv** (2023-01-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Yes, to be precise, all the non-view functions should be guarded by access control. It may be as simple as Ownable from Openzeppelin or as complex as a custom DAO. You can find the Ownable preset right here .

Cool, in that case, consider [ERC-5750: General Extensibility for Method Behaviors](https://eips.ethereum.org/EIPS/eip-5750) to give it extra data for future expansion. For example, when using EIP-5750 it opens up *future possibility* for your ERC adopter to *also* use a Commit-Reveal ([ERC-5732: Commit Interface](https://eips.ethereum.org/EIPS/eip-5732)) for sealed action or Commit-Delay for timelock action? It also provides future possibility for support a general permit based on [ERC-5453: Endorsement - Permit for Any Functions](https://eips.ethereum.org/EIPS/eip-5453)  which allow you to do

- Admin Alice: sign(offline) an endorsement and give it to another Bob then
- User Bob: sends TX with Alice’s endorsement to conduct the action

I am also working on a more general Access Control EIP which hopefully generalize access control [Add EIP-5982: Role-based Access Control by xinbenlv · Pull Request #5982 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5982). Your feedback will be appreciated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Actually it might. The injector is a special account that has permission of injecting dependencies into the dependant contracts. Here, the ContractsRegistry possesses both roles: injector and registry. However, these roles may be split and used separately. There is a case with a factory that deploys dependant contracts where the separation becomes visible. The factory would temporarily become the injector to provide the necessary dependencies upon deployment and set the injector to a proper contract afterward.

Then consider how do this interface represent passing in or out the context. For example, if you use r [ERC-5750: General Extensibility for Method Behaviors](https://eips.ethereum.org/EIPS/eip-5750) for `setInjector` and any functions that might take context. EIP-5750 is a way to allow interface designer and caller to agree with each other how to pass in more context in the same function call as extra parameter. But I could imagine you might also consider other methods / additional metheds like `setContext(...)`

---

**Arvolear** (2023-01-05):

Thanks, will take a look. The [EIP-5750: General Extensibility for Method Behaviors](https://eips.ethereum.org/EIPS/eip-5750) might be useful for the `setDependencies` method.

---

**Arvolear** (2023-01-10):

Hey, [@xinbenlv](/u/xinbenlv), I have updated the sheet with the new method `injectDependenciesWithData()` and an extra parameter in `setDependencies()` function. Would be amazing if you could take a look.

---

**xinbenlv** (2023-01-10):

Cool. that sounds great!

---

**bitcoinbrisbane** (2023-04-15):

Good stuff, I really like the intent of this EIP as I’ve rolled out a few registry contracts.  My suggestions:

- Include a ContractUpdated event.
- I think param “name” should be calldata, not memory

---

**Arvolear** (2023-04-15):

Hey [@bitcoinbrisbane](/u/bitcoinbrisbane), thanks for the feedback. The addition of the event sounds like a good idea. However, I see two options here:

1. Add UpgradedContract(string name, address newImplemetation) and split AddedContract in two to reflect the implementation address used by the proxy. For example, AddedContract(string name, address contractAddress) and AddedProxyContract(string name, address contractAddress, address implementation).
2. Just be UpgradedContract(string name) and change nothing else.

As for the calldata, I will change that in the interfaces because there are a bit messed up right now.

What do you think?

---

**bitcoinbrisbane** (2023-04-15):

Thanks for the reply.  To me, 2 seems the simplest and most explicit.  Of course, someone could always remove and add should they want to, to achieve the same result.

Probably best to index the address on the AddedContract and UpgradedContract too.  Such as [contracts.horse.link/I6224.sol at HL-673-6224 · horse-link/contracts.horse.link · GitHub](https://github.com/horse-link/contracts.horse.link/blob/HL-673-6224/contracts/I6224.sol#L11)

FWIW, my personal preference for the verbiage would be “ContractAdded” as opposed to “AddedContract”

---

**Arvolear** (2023-04-21):

I have opened a [pull request](https://github.com/ethereum/EIPs/pull/6911) to move the EIP to the Review stage. Would be amazing if everyone interested could take a look.

[@xinbenlv](/u/xinbenlv), tagging you because the eth-bot has suggested you as a reviewer. Could you please kindly review the PR?

---

**bitcoinbrisbane** (2023-04-25):

Horse link are about to deploy on arbitrum with this standard… maybe im the first in the wild implementation?

---

**Arvolear** (2023-04-25):

That is amazing! Good luck! However, not the first. Here is the link to my [reference implementation](https://github.com/dl-solidity-library/dev-modules/tree/master/contracts/contracts-registry). So probably DEXE network is the first ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Arvolear** (2023-12-05):

Updated the spec. Added proper reference implementation.

---

**Arvolear** (2024-02-07):

The EIP has been propagated to the **review stage**. I am open to any suggestions or critiques.

