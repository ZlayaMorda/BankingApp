function connect() {
    const MMSDK = new MetaMaskSDK.MetaMaskSDK()
    // Because init process of the MetaMaskSDK is async.
    setTimeout(() => {
        const ethereum = MMSDK.getProvider() // You can also access via window.ethereum

        ethereum.request({ method: 'eth_requestAccounts' })
    }, 0)
}