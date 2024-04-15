function connect() {

    if (typeof window.ethereum !== "undefined") {
        ethereum
         .request({ method: "eth_requestAccounts" })
         .then((accounts) => {
           const account = accounts[0]
            if (account) {
                alert(`Wallet connected: ${account}`)
            }
           console.log(`Wallet connected: ${account}`);
        }).catch((error) => {
           // Handle error
           console.log(error, error.code);

           // 4001 - The request was rejected by the user
           // -32602 - The parameters were invalid
           // -32603- Internal error
       });
    }
    else {
       window.open("https://metamask.io/download/", "_blank");
    }
    // const MMSDK = new MetaMaskSDK.MetaMaskSDK()
    // // Because init process of the MetaMaskSDK is async.
    // setTimeout(() => {
    //     const ethereum = MMSDK.getProvider() // You can also access via window.ethereum
    //
    //     ethereum.request({ method: 'eth_requestAccounts' })
    // }, 0)
}