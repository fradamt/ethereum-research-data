---
source: magicians
topic_id: 924
title: Discussion around 2FA implementation within smart contracts
author: Spaded
date: "2018-08-01"
category: EIPs
tags: [authentication]
url: https://ethereum-magicians.org/t/discussion-around-2fa-implementation-within-smart-contracts/924
views: 1734
likes: 2
posts_count: 9
---

# Discussion around 2FA implementation within smart contracts

Hey everyone!

TL;DR: There are two ways to make 2FA on smart contracts. One requires everyone running a node who wants 2fa and you control it yourself. The other is a general smart contract for everyone on the same blockchain. Which is best

I’ve had an idea to allow for 2FA on smart contacts and I want to create an EIP for this. Which I’m working on now, but before I submit it, I wanted to have a general discourse about the idea and make sure I’m not blind to some loophole in the security of it.

I’m curious which route is the best route to take for the EIP, a node based system done individually, or a general contract that manages everyone’s data for the entire blockchain.

2FA for Transfers of assets

Route 1:  Nodes ran independently. (meaning they have their own login servers that are tied to their own accounts, updating the state of the 2FA code on the smart contract)

UseCase: Lets assume Any Dapp has implemented this standard and their token contracts have been updated with a transferWith2FA() function.

`transferWith2FA(address to, uint tokens, uint8 _2FAcode)`

Any Dapp will run its own 2FA Node, which consist of the following:

- A login server with traditional user authenication

- A ethereum address that is registered within the 2fa Contract array of registeredAgents (Registered Agents are the only accounts that can update the code and address in the array… Here is the code example)

```
  address registeredAgent = 0x000000000....4259a8;
    modifier onlyRegisteredAgent {

    require(msg.sender == registeredAgent);
    _;
    }
```

So Any Dapp has set up a special address that they use as their agent, that will be the only address that is allowed to update the 2fa code state. This address is connected to a node running on their servers.

Bob wants to transfer Any Dapp tokens, using the new transferWith2FA() function… the function requires the address of the person receiving the tokens, and the amount. But now this functions wants a input field called 2FAcode, bob needs to get this code and generate it.

Any Dapp has set up a website with a user login, once bob has been traditionally logged in, he sees a code that is changing every few seconds on their screen. Just like when you open a google authenticator app on your phone.

The User will press a button that says “Submit Code” or whatever, this triggers an event on  Any Dapp’s backend server that will execute a transaction from the registeredAgent address setting the current code that was claimed, and the address of the person logged in. That would look like this function in the smart contract.

```
   function set2FA(address _sender, uint8 _2FAcode)
   onlyRegisteredAgent
   returns (uint256)
  {
        codesToAddress[_sender] = _2FAcode;
        //this setting the time on the code for that address, to the current time.
        addressToDatatoTime[_sender][_2FAcode] = now;

    return addressToDatatoTime[_sender][_2FAcode];

    }
```

Now the Bob has his code and can do a normal token transfer, but including this _2FAcode as data.

The transferWith2FA() function would now check the verifyTx function and require that it returns true

```
function verifyTx(address _sender, uint8 _2FAcode)
returns (bool)
{
               //check that timelimit is not expired - can be set via unix timestamp
    require(now < (addressToDatatoTime[_sender][_2FAcode] +500));

               // needs to verify that the person has the correct 2FA
    require(keysToAddress[_sender] == _2FAcode);
    return true;
 }
```

Route 2: Centralized as one smart contract across the blockchain (meaning there is one smart contract that everyone has access to, and owners of contracts can add registeredAgents within that overall smart contract that are allowed to only update the 2FAcode for their contract address. )

Usecase:

2FAManager - this is the overall smart contract that everyone on the public network would have access to

Lets assume ZRX wants to implement this standard on their token contracts and they have upgraded to the new contracts for 2FA discussed here. This is how it would work.

ZRX runs their own login servers like before, but now their registeredAgent account needs to be set up with the 2FAManager

In order to set registerAgents on the 2FAManager , they need to call it from the address of the smart contract they are controlling. So, ZRX needs to have an extra function  setUpRegisteredAgent() that would call the 2FAManager so that this contract within 2FAManager would be able to run a function that stores the caller’s address (the ZRX contract) and the registered agents address (provided by the setUpRegisteredAgent within ZRX’s contract) to the 2FAManager.

Now that the registeredAgent is set up on the 2FAManager, ZRX can generate their 2fa codes on their web server and have their registeredAgent address connected to their own node on their backend updating the 2fa code for the accounts  requesting it.

Anyone would be able to do this for their contracts, some exchanges would be able to do this in order to withdrawal from their hot wallets, who knows.

Problems: The login server goes offline. Solution: A bool flag that is controlled by the owner, turning the ability to transfer without fa on and off depending on if the server is online or offline.

What do you guys think about the overall idea? What are some problems, what needs to be fixed and worked out, before the EIP goes live.

Most importantly, which route is best for the ecosystem? Requiring that each contract who wants to do this, run their own authentication, just like how it is now in the real world? If I want to run a technology company (instagram) I need to handle my own user’s data on my own servers.

Or, should there be ONE general smart contract, that anyone can OPT-in to use 2fa on for their contracts? This means that this one general smart contract would be a single point of failure, which is bad.

Thoughts?

## Replies

**koeppelmann** (2018-08-04):

Maybe I am missing something, but why not just use a multisig contract and interact from that with smart contracts?

Check out:

https://twitter.com/koeppelmann/status/1024625797385146368

https://safe.gnosis.io/

---

**Spaded** (2018-08-06):

Adding 2fa to a smart contracts allows for a second level of security for your tokens.

If I have 2fa on a smart contract and I want to withdraw my tokens, the withdraw function takes the 2fa code generated on the site. Therefore, if someone stole my private key and was trying to steal my coins, they would now need to also log into the centralized website and generate a 2FA code to transfer tokens. That means you not only need to steal my private key, but now hack a centralized service as well.

---

**eolszewski** (2018-08-06):

This seems kind of silly - you could just use a multisig as a proxy wallet and set timeouts and limits on withdrawals. This puts the power in your and any other individuals’ hands who you appoint as members of the multisig ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**eolszewski** (2018-08-06):

Shameless plug on proxy wallets

https://medium.com/@eolszewski/ah-sh-t-i-lost-my-ethereum-wallet-321574e6ed79

---

**Spaded** (2018-08-06):

Good article [@eolszewski](/u/eolszewski)

Although, multisig still has many issues.

What if I don’t trust someone with the keys to my coins? So lets assume a person doesn’t want to share their keys with friends or family, but wants another level of security without relying on a person. Maybe I have no friends and can’t trust another human with my keys. This is multisig, just between the trusted third party, and yourself. Without needing to expose your own private key

Another issue with multisig, if I don’t trust another human but instead have the other key locked away in a safety deposit box, or buried underground, then I can’t actually transfer these tokens when I might need.

What it really comes down to is that: there should be multiple secure methods for users, to fit the needs of everyone. *If someone wants to trust a central web authority to generate a security code, and then also use their private key, we should have a way for them to do so. We trust web authorities everyday, we are currently trusting ethereum-magicians to handle our user info, so using that same method attached to the security of a private key, without making it vulnerable, should be designed and offered for users to have.*

This really is the only way to implement an accessible 2fa, with a third party, without sharing the actual private key.

I can now travel the world, with my pkey on my computer, knowing that if someone gets access to that pkey, they cannot remove my altcoins from contracts who use this 2FA, but I can move my tokens by myself, securely from anywhere in the world.

It literally just adds an extra step so that if you want to steal my tokens, you need to also hack /know my login into the central server handling user auth on the 2fa domain. But of course, if the token contract doesn’t implement these 2fa, then its just normal.

I see there are some ‘similar’ solutions, like multisig, but they all have downsides that some users may not want.

This is more about providing UX for people who want 2FA and extra centralized security.

I’m open to hear why this is a bad idea though, thats the whole point of this thread!

---

**dontpanic** (2018-08-07):

of the two common types of 2fa, TOTP & HOTP, only hotp could be used reliably on chain. The two largest issues with totp is block times are every 15s and their is no guarantee of which block your tx will be in. Hotp would be trivial to implement if you had some time to grind out hashes.

First generate a private key:

K= key

C=counter

2fa number:

HOTP(K, C) = Truncate(HMAC(K, C))

so the counter starts at zero an increments after each use.

on contract you would need a counter, an array of hashes,  and a function like:

function 2fa(uint _key) returns (bool){

require(sha256(_key)==hashs[counter]);

counter++;

return true;

}

on contract creation(or sometime else) you would need to populate the hash array. They are the hashs of the 2fa numbers generated above. since you have the private you are able to generate 0…n numbers trivially.

Where 2fa fails is the hashes on contract are public. so with a normal 6 character 2fa a rainbow table can easily be made and the entire experience moot. the fix would be using longer 2fa numbers but at some point it reaches diminishing returns

---

**Spaded** (2018-08-09):

[@dontpanic](/u/dontpanic) Thanks for the thoughtful response. Although you are correct using traditional 2FA exposing the generated key, either via publicly viewable on the chain, or from cracking via rainbow tables. But, even if someone cracked/knows the 2FA code, they still cannot do anything with my funds. They would need my private key to initiate the transaction.

---

**Spaded** (2018-08-09):

Here is the implementation in a smart contract. As you can see, there needs to be a ‘registeredAgent’ that is the trusted person to upload the newly generated 2FA code to the smart contract. This is why, using traditional HOTP styles probably won’t be required or even used. Any code, either known or unknown, will work as the code simply acts as a time sensitive approval.

The main concern here is the registereddAgent, this would need to be an account that is unlocked and running 24/7 on an ethereum node on the server of whomever is implementing this system. If an exchange wanted to implement this system, they would be the one running the registered Agent account.

```
pragma solidity ^0.4.21;

contract manager2FA {

    mapping(address => bool) public registeredAgent;
    modifier onlyRegisteredAgent {

    require(registeredAgent[msg.sender] == true);
    _;
    }

    //time in unix timestamp
    uint256 constant TIMELIMIT = 500;
    mapping(address => uint) public codesToAddress;
    mapping(address => mapping(uint256 => uint256)) public addressToDatatoTime;
    address public owner;
    //getters

    constructor(){
        owner = msg.sender;
    }
     function verifyTx(address _sender, uint256 _2FAcode) returns (bool){
        //check that timelimit is not expired by checking the timestamp the code was generated + 500.
        require(now < (addressToDatatoTime[_sender][_2FAcode] +500));
        // needs to verify that the person has the correct 2FA
        require(codesToAddress[_sender] == _2FAcode);
        return true;
                }

    //set 2FA called from registeredAgent which is running on the backend of some companies servers
       function set2FA(address _sender, uint256 _2FAcode)
       onlyRegisteredAgent
       returns (uint256)
      {
            codesToAddress[_sender] = _2FAcode;
            //this setting the time on the code for that address, to the current time.
            addressToDatatoTime[_sender][_2FAcode] = now;

        return addressToDatatoTime[_sender][_2FAcode];

        }

    function registerAgent(address _agent) returns (bool){
        require(msg.sender == owner);
        require(registeredAgent[_agent] == false);
        registeredAgent[_agent] = true;
        return registeredAgent[_agent];
    }

}
```

And a simple test for the contract

```
pragma solidity ^0.4.21;

import "./manager2fa.sol";

contract Test2FA {


     manager2FA instance;

    function setAddress(address _addr){

        instance = manager2FA(_addr);
    }
   function confirmCode(uint256 _2FAcode) returns (bool){
       require(instance.verifyTx(msg.sender, _2FAcode));
       return true;

   }

}
```

I just put these together to kind of explain what I am talking about/show an example. These are not finished/finalized, there could be bugs, don’t use these in a working implementation…

