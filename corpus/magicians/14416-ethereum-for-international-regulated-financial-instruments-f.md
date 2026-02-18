---
source: magicians
topic_id: 14416
title: Ethereum for international regulated financial instruments -Fintech and Developers-
author: rafael_manez
date: "2023-05-24"
category: ERCs
tags: [erc, evm]
url: https://ethereum-magicians.org/t/ethereum-for-international-regulated-financial-instruments-fintech-and-developers/14416
views: 590
likes: 1
posts_count: 3
---

# Ethereum for international regulated financial instruments -Fintech and Developers-

The use of Smart contracts for the management of financial instruments, in most countries requires compliance with a series of multilateral requirements according to financial regulations between jurisdictions and the type of financial instrument, conflicts of laws, privacy issues and legal security of those involved in the smart contract.

For this reason it is necessary to determine a *EIP* **ETHEREUM-FINANCIAL-INSTRUMENTS** for this purpose accompanied by development software under MIT License and be totally transparent to the end user. Providing facilities to fintech and developers in the process of financial regulation of their projects.

This proposed standard should be symmetrically standardized with all blockchains like this proposal in

**VEP**  **VENOM-FINANCIAL-INSTRUMENTS** on [Venom](https://forum.venom.foundation/t/venom-for-international-regulated-financial-instruments-fintech-and-developers/168/).

All collaboration and constructive suggestions are welcome.

Knowledge of international financial markets, software development, quantitative analysis are required for this purpose.

## Replies

**rafael_manez** (2023-05-24):

# EIP-001: ETHEREUM FINANCIAL INSTRUMENTS

```auto
 EIP: 1
 author: Rafael Mañez
 status: Idea
 type: Standards Track
 category: Contract
 created: 2023-04-03
```

## Abstract

ETHEREUM FINANCIAL INSTRUMENTS. It is an open standard for the management of financial assets in a multilateral system with different jurisdictions and different financial regulations as well as inter-blockchain compatibility and distributed ledger technologies.

As an example of a regulated financial instrument, I present the case of company shares: To negotiate company shares by ISIN, it is necessary to determine the jurisdiction of validity of the transaction, asset quality, market type, brochures, where to pay taxes for capital returns, transaction revocations, information of the issuer and receiver of the transactions, asset status that we are going to negotiate in a certain jurisdiction, legal blockades, legal recovery and all this among multiple laws that multilaterally affect the transactions of company shares.

## Motivation

The main motivation is to unify financial systems in a decentralized multilateral system with the objective of standardizing the management of financial instruments, without forgetting the particularities and operations of each one.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

- MUST be Open Source Smart Contract MIT License
- MUST have T-solSolididty compatibility only digital and decentralized compatibility
- Centralized support is OPTIONAL
- MUST manage Instruments: company shares, bonds, derivates, contracts
- MUST allow third party audit: National Competent Authorities (NCa’s) and Central Financial Authorities as ADGM Authorities, ESMA, NFRA, SEC, …
- MUST be able to grant permissions for third parties (Access, Views, SeenByThird, operations, privacy level and identities by nominal name or alias)
- MUST interpret Jurisdictional limits.
- MUST allow validation transaction.
- MUST have security on transactions.
- MUST allow Block and Unblock assets.
- MUST allow Revocations and recoveries.
- SHOULD have Asset history.
- MUST allow transform financial rules into programmable financial rules.
- MUST be scriptable functions (Interactive and non-Interactive) for manage by artificial intelligence
- MUST allow rule injection.
- MUST be inter-blockchain and distributed ledger technology compatibility.
- The issuance of the financial instrument MUST be covered by the competent authorities.

---

**rafael_manez** (2024-09-17):

# EIP/VEP-001: DLT FINANCIAL INSTRUMENTS

```auto
 EIP/VEP: 1
 author: Rafael Mañez
 status: Idea
 type: Standards Track
 category: Contract
 created: 2023-04-03
 brief: Create a logic unit for manage regulated multilateral financial instruments.
```

## Abstract

EIP/VEP DLT FINANCIAL INSTRUMENTS. It is an open standard for the management of financial assets in a multilateral system with different jurisdictions and different financial regulations as well as inter-blockchain compatibility and distributed ledger technologies.

As an example of a regulated financial instrument, I present the case of company shares: To negotiate company shares by ISIN, it is necessary to determine the jurisdiction of validity of the transaction, asset quality, market type, brochures, where to pay taxes for capital returns, transaction revocations, information of the issuer and receiver of the transactions, asset status that we are going to negotiate in a certain jurisdiction, legal blockades, legal recovery and all this among multiple laws that multilaterally affect the transactions of company shares.

## Motivation

The main motivation is to unify financial systems in a decentralized multilateral system with the objective of standardizing the management of financial instruments, without forgetting the particularities and operations of each one.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

- MUST be Open Source Smart Contract MIT License
- MUST have T-solSolididty compatibility only digital and decentralized compatibility
- Centralized support is OPTIONAL
- MUST manage Instruments: company shares, bonds, derivates, contracts
- MUST allow third party audit: National Competent Authorities (NCa’s) and Central Financial Authorities as ADGM Authorities, ESMA, NFRA, SEC, …
- MUST be able to grant permissions for third parties (Access, Views, SeenByThird, operations, privacy level and identities by nominal name or alias)
- MUST interpret Jurisdictional limits.
- MUST allow validation transaction.
- MUST have security on transactions.
- MUST allow Block and Unblock assets.
- MUST allow Revocations and recoveries.
- SHOULD have Asset history.
- MUST allow transform financial rules into programmable financial rules.
- MUST be scriptable functions (Interactive and non-Interactive) for manage by artificial intelligence
- MUST allow rule injection.
- MUST be inter-blockchain and distributed ledger technology compatibility.
- The issuance of the financial instrument MUST be covered by the competent authorities.

## Visualization:

```auto
> ![Screenshot from 2024-04-14 19-18-41|690x398](upload://rGrzIMWeEYEVOVcB2aGAE3gsHdZ.png)
>
> ![Symmetric-inter-blockchain-development|690x388](upload://59eZFxMxNO89SyCxwAFEkxZKyeE.png)
>
> ![visual2|690x393](upload://epQQUYRpUaaOQqPbCAOftuvdK5X.png)
>
> ![Case_Check_and_Propagation_new_financial_rules(MiM)|690x388](upload://7VeUrBh7uWKRvjXbWpGhg92760v.png)
>
> ![relation_diagram_for_financial_rules_metadata|690x348](upload://ghwGKcPY8k4ISxgBfcuyiRAwtO0.png)
>
> ![rule_encoder|690x393](upload://6Zb7VKTpvEXkKw2O1PXw2YS9xDK.png)
>
> ## Rationale
```

### Instrument Interface

```auto
interface FinancialInstrument is CompanyShares{
....
}

interface FinancialInstrument {
    //VARIABLE INTERNAL
     // byte financialrules?
    //VARIABLES EXTERNAL


    //@dev @TODO What is the most appropriate data structure? optimize gas primitives 0  address)
    // via byte encode: RULES[ ESMA:EU[10110101], ESCA:UAE[01010110]]   address) map or use pure struct?;
    //@TODO check compatibility gosh.zip converts the text to compressed bytes. gosh.unzip reverts such compression.


    //@dev Is this data structure adequate or is it preferable to use json for calling rules?
    //@dev Is Compatible SolTsol with optimized gas? (YES)
    //@noted Encoded bytes rule (No compatible):
    bytes autority_from = 0xb5; // ESMA:EU      [10110101]
    bytes autority_to = 0x56;   // ESCA:UAE     [01010110]
    autority_from&autority_to;  // Result: 0x14 [00010100] --> Not compatible instrument

    //@noted Encoded bytes rule (compatible):
    bytes autority_from = 0xb5; // ESMA:EU      [10110001]
    bytes autority_to= 0x46;    // ESCA:UAE     [01000110]
    autority_from&autority_to;  // Result: 0x0  [00000000] --> compatible instrument


    // @TODO check compatibility standard struct->metadata->value with json for save history with HEX representation of the signature,
    // @TODO generated using ed25519 algorithm --> very fast, non-reversible
    // @TODO generated using some AES symmetric, very fast, reversible
    // @notice metadata in JSON format
    // @return json The JSON string with metadata
    function getJson() external view responsible returns (string json);



    // @dev metadata structure allows to define particular instrument rule
    // @notice 'title' defining the title information,
    // @notice 'data_type' explaining the data type of the title information added (int, bool, address)
    // @notice 'description' explains little description about the information stored in the instrument"
    struct Metadata {
      string title; //eg tax control,rule,jurisdiction
      string data_type; //'int','bool','address'
      string description; //string
    }

    // @dev structure that defines the parameters for specific instrument and amount which are to be transferred/issued
    // @notice this structure is used to streamline the input parameters for functions of this standard with that of other Token standards like ERC20.
    // @classId is the class id of the instrument.
    // @authority_Id is the authority id of the given instrument class.
    // @amount is the amount of the instrument that will be transferred.
    struct Instrument {
      uint256 class_id; // companyShare
      uint256 authority_id; //rule verification isTransferable?
      uint256 amount;
    }


    // @dev allows the transfer of a financial instruments from one address to another.
    // @param from is the address of the stakeholder whose balance is about to decrease.
    // @param to is the recipient address whose balance is about to increase.
    // @param transaction is the object defining {class, authority and amount of the instrument to be transferred}.
    function transferFrom(address from, address to, Instrument[] transaction) external;

    //@TODO isTransferable(address from, address to, Metadata[] rule)

    // @dev How to control the collision between the bridge (Etherem, Venom) at propagation time. Issue event to bridge of traded assets
    // @notice SOLVED COLLISION IN FEDERATED TRANSACCIONS
    // @notice Solution to the collision of a transaction in progress by arbitration
    function chance(asset Eth, asset Venom) --> winning asset

    // @notice Solution to the collision of the transaction in progress due to pool time
    function seed_time(asset Eth, asset Venom) --> winning asset

    //EVENTS
    ...
}

```

### Type financial instruments:

```auto
.views(involutiveAssetHistoy, privacyLevel) #token fixed lengh for extract/pack history
.attribute
.actions(...) #Common functions
.setOperator #Set Union, Intersection, Difference, Complement of Set and Cartesian Product

contract financialInstrument is CompanyShares {
  ...
}
```

### Header

```auto
pragma ton-solidity >= 0.1.*;

pragma AbiHeader injectRules;
pragma AbiHeader auditState;
pragma AbiHeader expire;
pragma AbiHeader time;
pragma AbiHeader pubkey;

```

### Third party auctions:

```auto
#includes the regulatory nodes that affect the contract
import "https://jurisdiction/financialInstruments/rules/instrument.sol";
import "https://esma/financialInstruments/rules/companyShares.sol";
import "https://adgm/financialInstruments/rules/companyShares.sol";

```

### Libraries and utils

```auto
// Library decode/encode inject rules
...

//Library Auto asset history (cross-chain? (YES)
//@notice Write history for authority registration
//@dev symmetric algorithm SHA-256(currently used by Bitcoin) and Keccak-256(currently used by Ethereum)
bytes32 public constant  AUTHORITY_REGISTRATION= keccak256("asset_history(address from,address to,uint256 units,string isin, string,symbol, uint256 nonce,uint256 deadline)");
//or
bytes32 public constant  AUTHORITY_REGISTRATION= SHA-256("asset_history(address from,address to,uint256 units, string isin, string symbol, uint256 nonce,uint256 date)");

//Write new history and wrap
bytes32 encodeData = keccak256(abi.encode(AUTHORITY_REGISTRATION, from, to, units, isin, symbol, nonces[owner]++, date,));
//or
bytes32 encodeData = SHA-256(abi.encode(AUTHORITY_REGISTRATION, from, to, units, isin, symbol, nonces[owner]++, date,));

// Library  for recode in main thread
#TODO Is this pseudo-code suitable for recode Solidity  T-SOL and useful to update the contract at contract time?
#Receiving an inbound rule injection via fallback by internal/external message from competent financial authority.
#Does the competent authority involved in the contract want to inject any rules with reversal of control.
bool authorityRuleInjection = 0 #the authority speaks to apply a priority action
function isNewRule(address addr) public pure { ... }

function fallback() external {
   #from cell
   /*...*/
}

# or via onCodeUpgrade with direct injection and contract update
#TODO check TVM  EVM compatibility for change on authority demand.
function injectNewRule(...) private {
    /*...*/
}

function recode(TvmCell newcode, TvmCell cell) public pure checkPubkeyAndAccept {
    tvm.setcode(newcode);
    tvm.setCurrentCode(newcode);
    // pass cell to new contract
    injectNewRule(cell);
}

function injectNewRule(TvmCell cell) private pure {
 /*...*/
}

recieveNewRules() external {TVM* = data}

// new contract
function injectNewRule(TvmCell cell) private pure {
    // new code can use cell that was passed from the old version of the contract
}

// Library privacy level and constraints

pragma copyleft , ;  #good but poorly compatible with Ethereum
```

## Metadata

Contains the scheme of logical rules, numbers and limits between participants in the negotiation of a financial instrument on YAML or JSON .

```auto
#Example of purchase and sale of listed company shares.
example: companyShare.json

{
  //rules of the financial authority that included in the transactions.
  "ESMA":{
      //EU
      "rules": [
           anti-application rule .....
           integration and compensation...
           jurisdictional limit of the action on shares of listed companies
           "tax": {
               "brief": taxation of the actions on shares of listed companies
               "jurisdiction": [ESMA, UAE]
               "instant_payment_tax": address
            }
           market data...
          ]

  "ADMG":{
      //UAE
      "rules": [
           anti-application rule .....
           integration and compensation...
           jurisdictional limit of the action on shares of listed companies...
           "tax": {
               "brief": taxation of the actions on shares of listed companies...
               "jurisdiction": [ESMA, UAE]
               "instant_payment_tax_wallet": address
            }
          ]

  }
  //Transmit orders
  "transmitter": [
    "id": my nominal identification or custodial ALIAS
     "ISIN": EU0000000
     "Central Authority": ESMA
     "National Competent Authority": EU
     "Transfer value" ='2.33'
     "units" : "203266"
     "wallet": address
    ....
  },
  "receiver": [
     "id": my nominal identification or custodial ALIAS
     "ISIN": EU0000000
     "central Authority": ADMG
     "National Competent Authority": UAE
     "Acquisition value" : '2.25'
     "units" : "203266"
     "wallet": address
   ....
  }
  ]
}

```

## Backwards compatibility

Unprecedented. Checking EVM <–> TVM compatibility

## Reference implementation

## Test cases

## Security considerations

- Caution on gas from complex formats
- Caution deadly link between regulatory rules

## Implementation

MIT licensed.

Cold device environment.

A library of modular, reusable smart contracts.

`Samples and tests [here ](https://github.com/rafael-manez/venom-financial-instruments)`

## Requires:

TIP-4.1 standard for NFT

TIP-6.1

## References:

```auto
[[ALL] The International Organization of Securities Commissions (IOSCO) promotes co-operation between supervisory authorities of securities and futures markets.](https://www.iosco.org/)

[[EU][LU] Commission de Surveillance du Secteur Financier](https://www.cssf.lu/en/european-and-international-cooperation/#eu-authorities)

[[EU][ESMA] Regulation DLT pilot regime for market infrastructures](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R0858#d1e672-1-1)

[[UAE][ESCA] Regulations SCA’s](https://www.sca.gov.ae/en/regulations/regulations-listing.aspx#page=1)

[[USA][SEC] Strategic Hub for Innovation and Financial Technology (FinHub) ](https://www.sec.gov/finhub)

[[JP][BOJ] Bank of Japan](https://www.boj.or.jp/en/research/wps_rev/lab/lab18e02.htm)
```

## Open question:

- What type of token should the issue or DAO issue? Keep in mind that financial instruments allow issuance, asset expansion, merger, new nomination or reduction of the asset?
- What would be the average number of transactions on the Venom network for financial instruments? gas propagation…

## Required knowledge base:

1. know about financial instruments
Digital asset <> Financial Instrument.
Digital assets as tokens, NFTs are assets not regulated by a competent authority.
Financial Instrument as company shares is a regulated asset by a competent authority.
2. Good level in the discussion and development of smart contracts, standard protocols for a decentralized environment.
3. Expose Idea software (business logic) via an executable script.sh .
4. Expose regulatory idea by visual diagram or metadata Idea through JSON/YAML structure.
5. Test your wallet:
6. Etherscan Verified Contracts Center for Developers to request Test Ethereum tokens to your wallet.
7. Venom Faucet for Developers to request Test Venom tokens to your wallet
8. Test your smart contract.
9. Upload a dummy  smart contract ETH at etherscan verifyContract as wallet-to-wallet transfer.
10. Upload a dummy smart contract Venom at testnet venomscan contracts as wallet-to-wallet transfer.
11. Write the code hash Ethereum at verifyContract) / hash Venom at testnet venomscan  or address at EIP/VEP forum for check address. like this d22feffdf35dad582ae1b75aea7e313afaf574594d26c605750ba13f96aa11fb
12. Welcome to dlt-financial-instruments team.

## Contributors

> Contributions are always welcome!

> Terms to collaborate
>
>
> We do not doubt that you are the best developer or the best businessman but we can only see your capacity through the facts and the commitment that the effort gives. The rest is luck. It is a long-term core project and required by Fintech Defi that want to be regulated to trade financial instruments.
>
>
> You should know that every time you develop dapps for (DEX, BROKERS, BANKS, FINANCIAL AUTHORITIES, AUDITORS, NOTARIES, LAWYERS, FINANCIAL INDUSTRY …) to manage regulated financial instruments. You will need this library to regulate with a competent financial authority
>
>
> It is blind contact through facts and milestones without background by skills. estimated time: around 20 hours from scratch-
> It is a project for the core protocols in smart contracts. A Web3 expert is not necessary, a cross-blockchain smart contract expert is necessary.
> The project is not led or of a presidential format, it is community based on merits carried out. On equal terms.
> It is not an interview, do not send personal data to forum or chats. It is a selection by operational capacity for the collaboration. Members are anonymous unless they want to be published.
> The remuneration - or prize distribution - is based on the finished public development tickets.
> The error is tolerable. The rigor and try until it works is necessary.
> Take the time you need. The completed development tickets mark the times. -dev tickets are not reserved.-
>
>
>  For projects looking for individuals: (If so DM at forum)
>
>
> Project name: dlt-financial-instruments
> Project track: Idea and EIP/VEP at forum "Venom/Ethereum for international regulated financial instruments -Fintech and Developers- "
> Unique selling point (USP) or core feature : Cross-chain financial instruments and web3 trading
> Role that is needed : Quantitative experience in financial systems and financial instruments, Development experience in smart contracts “t-sol & sol” and cross-chain
> Type of remuneration: Collaborator. It is a long-maintenance MIT license project.
>
>
> Any recommendations from the community for the interface? and avoid turning the project into a single criteria?
> Decentralized projects must be 100% decentralized to be adopted by users.
>
>
>
> ## Open Collaborators Tickets (They are not reserved, discuss in forum.)
>
>
>
>
>
>
> Item
> In Stock
> Role
> -
>
>
>
>
> Bash Script for deploy Infrastructure Open Api generator cli/stub server/web3connect
> True
> DEV
> -
>
>
> Consolidated Financial Rules schema/model (JSON/YAML)
> True
> QUANT
> -
>
>
> Deploy interactive test infrastructure -not web, only command line-
> True
> DEV
> -
>
>
> Document the source urls of the competent financial authorities to convert them into logical schemas.
> True
> QUANT
> -
>
>
> Branding design (Header and Footer) for mustage , css, html templates and logo venom financial instruments.
> True
> BRAND
> -
>
>
> Actor model hipotesis for pre-transactions, transaction, post-transaction, pre-validation of metadata, inline-validation, post-validations metadata
> True
> DEV
> -

## Gratitude

Thanks for the all likes and encouragement post.

For reasons of clarity we will update on the VEP/EIP post and the likes and post will be removed.

Only the “likes” of the header will remain.

Only posts of constructive criticism of the projects will remain.

## Copyright

Copyright and related rights waived via [CC0 ]

