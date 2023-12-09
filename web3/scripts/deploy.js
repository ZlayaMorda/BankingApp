const hre = require("hardhat");

async function main() {

  const initialSupply = hre.ethers.parseEther("1000000000000000");

  const token = await hre.ethers.deployContract("BYNToken", [initialSupply]);

  await token.waitForDeployment();

  console.log(
    `Token with ${initialSupply} initial supply deployed to ${token.target}`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
