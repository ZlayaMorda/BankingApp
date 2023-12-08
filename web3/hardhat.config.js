require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config()

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  defaultNetwork: "mainnet_fork",
    networks: {
      mainnet_fork: {
            url: 'http://' + process.env.HOST + ':' + process.env.PORT,
            forking: {
                // url: "",
                blockNumber: process.env.BLOCK_NUMBER,
                // accounts: [process.env.PRIVATE_KEY]
            }
      }
    }
};
