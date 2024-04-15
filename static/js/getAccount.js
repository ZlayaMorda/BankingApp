function getAccount(){
    if (typeof window.ethereum !== "undefined") {
        ethereum
         .request({ method: "eth_requestAccounts" })
         .then((accounts) => {
           const account = accounts[0]
           console.log(`Wallet connected: ${account}`);
           $("#id_bc_account").val(account)
        }).catch((error) => {
           // Handle error
           console.log(error, error.code);
           $("#id_bc_account").val("Connect wallet and account")
           // 4001 - The request was rejected by the user
           // -32602 - The parameters were invalid
           // -32603- Internal error
       });
    }
    else {
        $("#id_bc_account").val("Connect wallet and account")
       window.open("https://metamask.io/download/", "_blank");
    }
}