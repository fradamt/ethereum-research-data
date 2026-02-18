---
source: magicians
topic_id: 19368
title: Deploy ERC20 Contract using Smart Account (ERC-4337)
author: AkashWarlocks
date: "2024-03-26"
category: EIPs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/deploy-erc20-contract-using-smart-account-erc-4337/19368
views: 394
likes: 1
posts_count: 1
---

# Deploy ERC20 Contract using Smart Account (ERC-4337)

```auto
(async () => {
  // Fund your account address with ETH to send for the user operations
  console.log("Smart Account Address: ", client.getAddress()); // Log the smart account address
  const param1 = client.getAddress(); // Example parameter
  const param2 = client.getAddress(); // Example parameter

  const encodedParams = encodeAbiParameters([{
    name:"defaultAdmin",
    type: "address"
  },{
     name:"minter",
     type: "address"
  }],[client.getAddress(),client.getAddress()])
  console.log({encodedParams})
  const bytecodeWithParams = MyToken.bytecode + encodedParams.substring(2);

  const elligibility = await client.checkGasSponsorshipEligibility({
  target: "0x0000000000000000000000000000000000000000",
  data: bytecodeWithParams,
  value: 0n, // value in bigint or leave undefined
});

console.log(
  `User Operation is ${
    elligibility ? "eligible" : "ineligible"
  } for gas sponsorship`
);

const uop = await client.buildUserOperation({
    uo:{
        target:"0x0000000000000000000000000000000000000000",
        data:bytecodeWithParams,
        value:0n
    }
})
const signedUop = await client.signUserOperation({uoStruct:uop})
  const {hash} = await client.sendUserOperation({uo:signedUop.callData})

  console.log({hash})

  //Deploy contract
  const txHash = await client.waitForUserOperationTransaction({hash:hash});
  console.log(txHash);

})();
```

Initially I used this way to send data over AA account, then i dived deep into Entrypoint contract and it uss

`call(g, a, v, in, insize, out, outsize)`, while to deploy contract using assembly we need `create(v, p, n)` or

`create2(v, p, n, s)`.

Is there a way I can deploy a contract using smart account ? Is it by design we can’t deploy contract using Entrypoint
