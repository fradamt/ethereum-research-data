---
source: ethresearch
topic_id: 4798
title: ERC20 backward-compatible gas abstraction using Constantinople's EIP 1014
author: nourharidy
date: "2019-01-12"
category: Economics
tags: [gas-abstraction]
url: https://ethresear.ch/t/erc20-backward-compatible-gas-abstraction-using-constantinoples-eip-1014/4798
views: 5655
likes: 5
posts_count: 7
---

# ERC20 backward-compatible gas abstraction using Constantinople's EIP 1014

**Prerequisites**

- Layer 2 gas payment abstraction
- EIP 1014.

**Motivation**

Transaction gas abstraction, sometimes known as meta-transactions, should ideally be backward-compatible with existing contracts, most notably ERC20 contracts. We cannot assume that all existing contracts can add [@vbuterin](/u/vbuterin)’s [submitSignedPayments()](https://ethresear.ch/t/layer-2-gas-payment-abstraction/4513) or any other gas payment abstraction protocol to their code.

On the other hand, we cannot rely on ERC20 `approve()` to extend ERC20 contracts in the context of gas payment abstraction because this first step requires the external account to pay for its gas fee in Ether which defies the purpose.

However, I think a solution may be possible in a few days thanks to Constantinople’s [EIP 1014](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1014.md).

**Basic Protocol**

Using `EIP 1014`'s new `CREATE2` opcode we can allow for deployment gas abstraction for any contract, including “*smart wallets*”, leading to ERC20 backward-compatible layer 2 gas payment abstraction:

- A public factory contract is deployed once on the mainnet allowing anyone to deploy CREATE2 contracts by providing init_code and salt.
- Alice creates a new external account key pair with 0 Ether balance
- Alice generates init_code for a gas abstraction wallet contract, or smart_wallet, of her choice and sets a fixed ERC20 fee, say in Dai, for msg.sender in the constructor.
- Alice selects a random salt and combines it with the init_code and the factory address to deterministically generate an address for her smart_wallet contract before deployment.
- Alice uses her off-chain smart_wallet address instead of her external account address to receive Dai.
- When the smart_wallet's Dai balance exceeds the fee set in the contract constructor, Alice can send the init_code and salt of her smart_wallet to a relayer, Bob, to deploy it using the factory and redeem the Dai fee.
- Alice can now use a gas abstraction protocol set in her smart_wallet.
- Nowhere in this process Alice needs to get or know about Ether.

**Discussion**

- Alice may receive tokens at her smart_wallet address but cannot find a relayer potentially because the ERC20 token fee previously set in the constructor is not, or no longer is, sufficient to cover a relayer’s gas fees. The worst case scenario here is one where Alice chooses to acquire Ether on her external account and take the role of the relayer herself. To avoid this, this one time fee must be sufficiently high to accommodate for volatility risks. Although either way, Alice’s funds are never stuck forever. A potential improvement would be for the contract’s constructor to know the current token price in Ether using Uniswap’s getTokenToEthInputPrice() exchange interface to dynamically set the constructor fee but that may put Alice in some volatility risk herself. Although at a fee scale the volatility may be negligible. If not, again, Alice can relay for herself. Better improvements? Edit: This problem was solved here.
- Relayer front-running should not be usable as an attack vector against Alice but I’m curious to know how it would affect relayers’ availability, price competition and decentralization.
- What are other applications of contract deployment gas abstraction other than counterfactual contracts or backwards compatible submitSignedPayments()?
- What are the potential attack vectors, bad scenarios, black swan scenarios, etc that I haven’t considered?

## Replies

**miohtama** (2019-01-12):

> Transaction gas abstraction, sometimes known as meta-transactions, should ideally be backward-compatible with existing contracts, most notably ERC20 contracts.

While this is ideal, we should not sacrifice alternative simpler implementations to strive for this design goal. However, I need to admit, I have not read alternative proposals, so I cannot comment if this is the case or not. I should want to throw my 2 weis here as a feedback.

I have issued out many ERC-20 tokens myself. All of the cases they have come with a bold disclaimer saying that the technology is still experimental. If the tokens need to be swapped to a new version to support more advanced features, I’d rather do this than having more complex implementation for the gas abstraction mechanism itself.

E.g. if the existing token contract needs to be changed to have very straightforward gas abstraction implementation, this is better than trying to overlay the gas abstraction model on old plain ERC-20.

ERC-20 tokens can be upgraded

- Through built-in mechanisms
- Token swaps - send old tokens to the smart contract to be burned or hold forever, get new tokens back in return

---

**sir_assistant** (2019-01-13):

For the problem of the fee:

The creator could create a private key, the factory method could include a signed amount as a parameter and the init code could revert if the ecrecover of the signature doesn’t match the creator address , and send the amount otherwise.

I’m not very familiar with the create2 so I don’t know if the init code can include constructor arguments…

But for what I have read it should, so with this you could give the relayer the init code, salt and the signed amount you are paying him

---

**nourharidy** (2019-01-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/miohtama/48/885_2.png) miohtama:

> E.g. if the existing token contract needs to be changed to have very straightforward gas abstraction implementation, this is better than trying to overlay the gas abstraction model on old plain ERC-20.

There is no reason for ERC20 to be changed provided an alternative that does not add significant trade-offs beyond more engineering complexity (rather than usability trade-offs). Which can be argued to be the case for this proposal. In fact, the user is already expected to use relays using `submitSignedPayments()`. Therefore, the same relays can be used to deploy smart contract wallets without much additional complexity. Of course, the wallet frontend will hide this process from the user the same way it would with `submitSignedPayments()`.

![](https://ethresear.ch/user_avatar/ethresear.ch/miohtama/48/885_2.png) miohtama:

> ERC-20 tokens can be upgraded
>
>
> Through built-in mechanisms
> Token swaps - send old tokens to the smart contract to be burned or hold forever, get new tokens back in return

Replacing external accounts with a smart contract wallet architecture can also allow for easier upgradability/extensibility in the future by moving standardization from the token side to the wallet side; something that external accounts do not allow. Multisigs are an example of this. They are not going to be standardized into token contracts because people want to have a wide variety of token multisigs that no token side standard can accommodate for. While upgrading wallet contracts only requires a decision to be made by the wallet owner. Token standardization can be a double-edged sword. And even if ERC20 can be “upgraded” across most relevant token contracts soon (which I believe to be a strong assumption), it will only become more and more difficult as these contracts gain more adoption.

![](https://ethresear.ch/user_avatar/ethresear.ch/sir_assistant/48/3170_2.png) sir_assistant:

> For the problem of the fee:
> The creator could create a private key, the factory method could include a signed amount as a parameter and the init code could revert if the ecrecover of the signature doesn’t match the creator address , and send the amount otherwise.
> I’m not very familiar with the create2 so I don’t know if the init code can include constructor arguments…
> But for what I have read it should, so with this you could give the relayer the init code, salt and the signed amount you are paying him

You’re right. The ability to negotiate the fee with the relay on contract deployment would solve the problem. From the [clarification](https://eips.ethereum.org/EIPS/eip-1014) and [code example](https://github.com/stanislaw-glogowski/create2) that I found, the constructor parameters seem to be included in `init_code`. Therefore, changing the parameters would also change the computed contract address. That said, there is a work around. The wallet contract stores the factory address in its constructor using `msg.sender`. We add a `transferRelayFee(address relay, uint256 fee, address tokenContract)` function to the contract code that only allows the factory to transfer any amount of tokens to any address. As you proposed, the relay can then submit the `init_code` to the factory contract alongside a signed message from the wallet owner allowing the relay a fee in tokens provided they deploy the `init_code`.

In this case, the factory deployment function header becomes:

`deployCreate2(bytes memory code, uint salt, uint fee, address tokenContract, uint8 v, bytes32 r, bytes32 s)`

Factory implementation:

1. Use create2 to deploy code
2. Query the deployed contract’s owner address
3. Recover the signer address from v,r,s and keccak256(salt, fee, tokenContract) and compare it to owner.
4. Call transferRelayFee(msg.sender, fee, tokenContract) on the new contract
5. If any of above steps fails, revert transaction and reverse contract deployment.

It’s worth mentioning that the reason `transferRelayFee()` is called by the factory instead of a separate transaction by the relay is to avoid an attack where the owner quickly empties their token balance before the relay has a chance to withdraw their fee after deployment.

---

**3esmit** (2019-01-15):

Interesting proposal. Create2 would make what you describe possible.

Currently for that problem of no initial eth gas, in Status, without create2 we would allow a convert, but would only work using SNT, for that  I implemented on the MiniMeToken Controller contract a function to “convert” a regular (externally owned) account into a account contract (as ERC725) with gas relay adaptors.

But with the support of create2 on mainnet what you described will certainly be implemented, as removing the SNT requirement for this fundamental UX problem is desirable for web3.

Exactly what you proposed or something similar would be implemented in the project I’m working. I might also adapt it to also support the offchain payment channel, that helps reducing the cost of gas relay by agreeing in gas payment value offchain between gas relayer and account contract.

The gas channel also would benefit create2, as the created address is used in an offchain signed message, to  pay the first iteration “createGasChannel”, which basically allows account owner to create a channel, transfer ERC20 to it, and allow this newly generated channel to pay the gas relayer, which will have a signed message for that gasChannel from account owner with value that can be withdrawn.

For reference,

convertGasRelay method: https://github.com/status-im/snt-gas-relay/blob/3af343c4d090f68e388a4176529b51cad95321eb/test-dapp/contracts/status/StatusNetwork.sol#L48

createGasChannel method: https://github.com/status-im/snt-gas-relay/blob/3af343c4d090f68e388a4176529b51cad95321eb/test-dapp/contracts/gasrelay/SimpleGasChannel.sol#L25

---

**3esmit** (2019-01-30):

I implemented a variance of this on Status gas relayer, which is more simple.

I am not gas relaying the constructor call, instead, the first relayer would do it for free and agree on the first gas relay to have a higher gasPrice which would be able to cover the cost of creation, or a payment transaction that would be executed right after the creation.

The only use of EIP1014 is ability to users deposit in a not yet created account contract, so enhances a lot the UX for onboarding users into those account contracts.

---

**nourharidy** (2019-04-14):

[@3esmit](/u/3esmit) would like to take a look at your implementation.

We also worked on implementing this at [Lamarkaz](https://lamarkaz.com) in the form of a DAI mobile wallet called Metacash. It’s available on the mainnet for early access on Android [here](https://play.google.com/store/apps/details?id=com.lamarkaz.metacash) (iOS release will be published soon).

Contracts code is verified on Etherscan [here](https://etherscan.io/address/0x0A6d9D8e98146d5c36ef97C752DF215854573536#code). Take a look at that and let me know if you got any questions about the code. It contains 4 important contracts:

- Factory is the CREATE2 factory contract
- SmartWallet is the smart wallet/account contract implementation. Only a single instance is deployed for all users and it’s only called using DELEGATECALL.
- Proxy is the contract deployed for each user using CREATE2 through the Factory. It forwards all calls to SmartWallet using DELEGATECALL. It also allows user-activated upgradability such that users can forward calls to their address to a new implementation.
- RelayRegistry contains a list of whitelisted relays to prevent relay frontrunning spam attacks until we find a secure multi-relay architecture. I would love to know how you guys approach this problem at Status.

In terms of gas consumption, we have two kinds of transactions:

- Deploy + pay, the 1st relayed transaction of each user, it deploys their smart wallet and sends DAI to a recipient in 1 tx: About 400K gas
- Pay, every relayed transfer transaction after the first deploy+pay: About 100k gas

We can probably drive these numbers lower by optimizing the code or by batching txs when reaching high volumes. Maybe if someone can look at the code and give some advice on how gas cost can be reduced, we can do that using the DELEGATECALL upgrade.

We’ll be publishing a full write-up soon. Meanwhile, you can also discuss the implementation on [Telegram](https://t.me/joinchat/Gar4_UgwWh2c42hpDreG6w).

