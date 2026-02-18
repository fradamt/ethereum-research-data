---
source: magicians
topic_id: 13058
title: "EIP-8000: Expirable Transaction with Block Number Deadline"
author: hiddenintheworld
date: "2023-02-26"
category: EIPs > EIPs core
tags: [gas, consensus-layer]
url: https://ethereum-magicians.org/t/eip-8000-expirable-transaction-with-block-number-deadline/13058
views: 754
likes: 0
posts_count: 1
---

# EIP-8000: Expirable Transaction with Block Number Deadline

## Abstract

We propose the introduction of a time-based transaction expiration mechanism in Ethereum. The mechanism would allow users to set an expiration block number for their transactions, after which the transaction would expire and be removed from the mempool. This would give users more control over their transactions and reduce unnecessary network traffic caused by failed transactions.

The expiration block number would be a parameter that users could set while creating their transactions. If the transaction is not included in a block before the expiration block number, it would expire, and the gas used for the transaction would be refunded to the sender’s account. This would ensure that users are not charged for transactions that are not processed and also reduce the load on the network.

This EIP proposes the introduction of a new transaction type, based on EIP-1559, with a new format: 0x02 || rlp([chain_id, nonce, expiration_block_number, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s]).

This new transaction type includes an expiration block number, which can be set by the sender. A transaction will only be valid if the current block number is less than or equal to the expiration block number. The transaction specifies the expiration block number as the deadline for when the transaction is valid. If the expiration block number is reached, the transaction will fail, and no gas fee will be paid.

## Motivation

Ethereum has had a significant number of failed transactions, leaving users with no option but to replace transactions with a higher gas fee and 21000 gas limit transaction (ETH native transaction). This process is inefficient, and there is no way for a transaction to timeout and not be mined once it is sent to the mempool.

- Lack of flexbility for user: It can be incredibly frustrating to be unable to cancel an unnecessary transaction, especially when using platforms like Uniswap to swap tokens or when buying NFTs.
- Network traffic with useless transaction meant to fail: In the absence of a transaction expiration mechanism, these failed transactions can remain in the mempool for extended periods of time, leading to unnecessary network traffic. Furthermore, these failed transactions can create network congestion and make it more difficult for other transactions to be processed in a timely manner.

This proposal aims to provide a solution to this inefficiency. With the introduction of an expiration block number, transactions can expire if they are not mined within a specific period, providing users with more flexibility to cancel

## Specification

Transaction is only valid if the expiration_block_number is greater than or equal to the current block number, the transaction is considered expired and cannot be included in the block otherwise.

Block validity is defined in the reference implementation below.

The `NUMBER` (`0x43`) opcode **REPRESENT** the `block.number` as defined in the reference implementation below.

As of `FORK_BLOCK_NUMBER`, a new EIP-2718 transaction is introduced with `TransactionType` 2.

The EIP-2718 `TransactionPayload` for this transaction is `rlp([chain_id, nonce, expiration_block_number, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s])`.

The `signature_y_parity, signature_r, signature_s` elements of this transaction represent a secp256k1 signature over `keccak256(0x02 || rlp([chain_id, nonce, expiration_block_number, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list]))`.

The EIP-2718 `ReceiptPayload` for this transaction is `rlp([status, cumulative_transaction_gas_used, logs_bloom, logs])`.

*Note: `//` is integer division, round down.*

```python
from typing import Union, Dict, Sequence, List, Tuple, Literal
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class TransactionLegacy:
	signer_nonce: int = 0
	gas_price: int = 0
	gas_limit: int = 0
	destination: int = 0
	amount: int = 0
	payload: bytes = bytes()
	v: int = 0
	r: int = 0
	s: int = 0

@dataclass
class Transaction2930Payload:
    chain_id: int = 0
    signer_nonce: int = 0
    gas_price: int = 0
    gas_limit: int = 0
    destination: int = 0
    amount: int = 0
    payload: bytes = bytes()
    access_list: List[Tuple[int, List[int]]] = field(default_factory=list)
    signature_y_parity: bool = False
    signature_r: int = 0
    signature_s: int = 0

@dataclass
class Transaction2930Envelope:
	type: Literal[1] = 1
	payload: Transaction2930Payload = Transaction2930Payload()

@dataclass
class Transaction8000Payload:
    chain_id: int = 0
    signer_nonce: int = 0
    expiration_block_number: int = 0
    max_priority_fee_per_gas: int = 0
    max_fee_per_gas: int = 0
    gas_limit: int = 0
    destination: int = 0
    amount: int = 0
    payload: bytes = bytes()
    access_list: List[Tuple[int, List[int]]] = field(default_factory=list)
    signature_y_parity: bool = False
    signature_r: int = 0
    signature_s: int = 0

@dataclass
class Transaction8000Envelope:
	type: Literal[2] = 2
	payload: Transaction8000Payload = Transaction8000Payload()

Transaction2718 = Union[Transaction8000Envelope, Transaction2930Envelope]

Transaction = Union[TransactionLegacy, Transaction2718]

@dataclass
class NormalizedTransaction:
    signer_address: int = 0
    signer_nonce: int = 0
    expiration_block_number: int = 0
    max_priority_fee_per_gas: int = 0
    max_fee_per_gas: int = 0
    gas_limit: int = 0
    destination: int = 0
    amount: int = 0
    payload: bytes = bytes()
    access_list: List[Tuple[int, List[int]]] = field(default_factory=list)

@dataclass
class Block:
	parent_hash: int = 0
	uncle_hashes: Sequence[int] = field(default_factory=list)
	author: int = 0
	state_root: int = 0
	transaction_root: int = 0
	transaction_receipt_root: int = 0
	logs_bloom: int = 0
	difficulty: int = 0
	number: int = 0
	gas_limit: int = 0 # note the gas_limit is the gas_target * ELASTICITY_MULTIPLIER
	gas_used: int = 0
	timestamp: int = 0
	extra_data: bytes = bytes()
	proof_of_work: int = 0
	nonce: int = 0
	base_fee_per_gas: int = 0

@dataclass
class Account:
	address: int = 0
	nonce: int = 0
	balance: int = 0
	storage_root: int = 0
	code_hash: int = 0

INITIAL_BASE_FEE = 1000000000
INITIAL_FORK_BLOCK_NUMBER = 10 # TBD
BASE_FEE_MAX_CHANGE_DENOMINATOR = 8
ELASTICITY_MULTIPLIER = 2

class World(ABC):
	def validate_block(self, block: Block) -> None:
		parent_gas_target = self.parent(block).gas_limit // ELASTICITY_MULTIPLIER
		parent_gas_limit = self.parent(block).gas_limit

		# on the fork block, don't account for the ELASTICITY_MULTIPLIER to avoid
		# unduly halving the gas target.
		if INITIAL_FORK_BLOCK_NUMBER == block.number:
			parent_gas_target = self.parent(block).gas_limit
			parent_gas_limit = self.parent(block).gas_limit * ELASTICITY_MULTIPLIER

		parent_base_fee_per_gas = self.parent(block).base_fee_per_gas
		parent_gas_used = self.parent(block).gas_used
		transactions = self.transactions(block)

		# check if the block used too much gas
		assert block.gas_used  parent_gas_limit - parent_gas_limit // 1024, 'invalid block: gas limit decreased too much'

		# check if the gas limit is at least the minimum gas limit
		assert block.gas_limit >= 5000

		# check if the base fee is correct
		if INITIAL_FORK_BLOCK_NUMBER == block.number:
			expected_base_fee_per_gas = INITIAL_BASE_FEE
		elif parent_gas_used == parent_gas_target:
			expected_base_fee_per_gas = parent_base_fee_per_gas
		elif parent_gas_used > parent_gas_target:
			gas_used_delta = parent_gas_used - parent_gas_target
			base_fee_per_gas_delta = max(parent_base_fee_per_gas * gas_used_delta // parent_gas_target // BASE_FEE_MAX_CHANGE_DENOMINATOR, 1)
			expected_base_fee_per_gas = parent_base_fee_per_gas + base_fee_per_gas_delta
		else:
			gas_used_delta = parent_gas_target - parent_gas_used
			base_fee_per_gas_delta = parent_base_fee_per_gas * gas_used_delta // parent_gas_target // BASE_FEE_MAX_CHANGE_DENOMINATOR
			expected_base_fee_per_gas = parent_base_fee_per_gas - base_fee_per_gas_delta
		assert expected_base_fee_per_gas == block.base_fee_per_gas, 'invalid block: base fee not correct'

		# execute transactions and do gas accounting
		cumulative_transaction_gas_used = 0
		for unnormalized_transaction in transactions:
			# Note: this validates transaction signature and chain ID which must happen before we normalize below since normalized transactions don't include signature or chain ID
			signer_address = self.validate_and_recover_signer_address(unnormalized_transaction)
			transaction = self.normalize_transaction(unnormalized_transaction, signer_address)

			signer = self.account(signer_address)

			signer.balance -= transaction.amount
			assert signer.balance >= 0, 'invalid transaction: signer does not have enough ETH to cover attached value'
			# the signer must be able to afford the transaction
			assert signer.balance >= transaction.gas_limit * transaction.max_fee_per_gas

                        # ensure that the transaction has not expired
                        assert transaction.expiration_block_number >= block.number

			# ensure that the user was willing to at least pay the base fee
			assert transaction.max_fee_per_gas >= block.base_fee_per_gas

			# Prevent impossibly large numbers
			assert transaction.max_fee_per_gas = transaction.max_priority_fee_per_gas

			# priority fee is capped because the base fee is filled first
			priority_fee_per_gas = min(transaction.max_priority_fee_per_gas, transaction.max_fee_per_gas - block.base_fee_per_gas)
			# signer pays both the priority fee and the base fee
			effective_gas_price = priority_fee_per_gas + block.base_fee_per_gas
			signer.balance -= transaction.gas_limit * effective_gas_price
			assert signer.balance >= 0, 'invalid transaction: signer does not have enough ETH to cover gas'
			gas_used = self.execute_transaction(transaction, effective_gas_price)
			gas_refund = transaction.gas_limit - gas_used
			cumulative_transaction_gas_used += gas_used
			# signer gets refunded for unused gas
			signer.balance += gas_refund * effective_gas_price
			# miner only receives the priority fee; note that the base fee is not given to anyone (it is burned)
			self.account(block.author).balance += gas_used * priority_fee_per_gas

		# check if the block spent too much gas transactions
		assert cumulative_transaction_gas_used == block.gas_used, 'invalid block: gas_used does not equal total gas used in all transactions'

		# TODO: verify account balances match block's account balances (via state root comparison)
		# TODO: validate the rest of the block

	def normalize_transaction(self, transaction: Transaction, signer_address: int) -> NormalizedTransaction:
		# legacy transactions
		if isinstance(transaction, TransactionLegacy):
			return NormalizedTransaction(
				signer_address = signer_address,
				signer_nonce = transaction.signer_nonce,
				expiration_block_number = transaction.expiration_block_number,
				gas_limit = transaction.gas_limit,
				max_priority_fee_per_gas = transaction.gas_price,
				max_fee_per_gas = transaction.gas_price,
				destination = transaction.destination,
				amount = transaction.amount,
				payload = transaction.payload,
				access_list = [],
			)
		# 2930 transactions
		elif isinstance(transaction, Transaction2930Envelope):
			return NormalizedTransaction(
				signer_address = signer_address,
				signer_nonce = transaction.payload.signer_nonce,
				expiration_block_number = transaction.expiration_block_number,
				gas_limit = transaction.payload.gas_limit,
				max_priority_fee_per_gas = transaction.payload.gas_price,
				max_fee_per_gas = transaction.payload.gas_price,
				destination = transaction.payload.destination,
				amount = transaction.payload.amount,
				payload = transaction.payload.payload,
				access_list = transaction.payload.access_list,
			)
		# 8000 transactions
		elif isinstance(transaction, Transaction8000Envelope):
			return NormalizedTransaction(
				signer_address = signer_address,
				signer_nonce = transaction.payload.signer_nonce,
				expiration_block_number = transaction.expiration_block_number,
				gas_limit = transaction.payload.gas_limit,
				max_priority_fee_per_gas = transaction.payload.max_priority_fee_per_gas,
				max_fee_per_gas = transaction.payload.max_fee_per_gas,
				destination = transaction.payload.destination,
				amount = transaction.payload.amount,
				payload = transaction.payload.payload,
				access_list = transaction.payload.access_list,
			)
		else:
			raise Exception('invalid transaction: unexpected number of items')

	@abstractmethod
	def parent(self, block: Block) -> Block: pass

	@abstractmethod
	def block_hash(self, block: Block) -> int: pass

	@abstractmethod
	def transactions(self, block: Block) -> Sequence[Transaction]: pass

	@abstractmethod
	def execute_transaction(self, transaction: NormalizedTransaction, effective_gas_price: int) -> int: pass

	@abstractmethod
	def validate_and_recover_signer_address(self, transaction: Transaction) -> int: pass

	@abstractmethod
	def account(self, address: int) -> Account: pass
```

## Backwards Compatibility

This proposal is backwards compatible with existing Ethereum transactions to EIP-1559 . It is an optional feature that is only included in transactions that utilize the new format specified in this EIP.

## Security Considerations

### Potentially be exploited by malicious actors

The introduction of an expiration block number feature could potentially be exploited by malicious actors to attempt to invalidate transactions that are still valid. However, this risk is mitigated by setting a minimum block number limit on the expiration block number, which will ensure that transactions remain valid for a reasonable amount of time.

### Nodes gatekeeping

Additionally, nodes on the Ethereum network can enforce a maximum block number limit for expiration block numbers to further reduce the risk of exploitation, the mempool could also drop all transactions that have expired.

## Copyright

Copyright and related rights waived via [CC0].
