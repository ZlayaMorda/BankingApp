const hre = require("hardhat");

async function main() {
  const owner = await hre.ethers.getSigner("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")

  const initialSupply = hre.ethers.parseEther("1000000000000000");
  const Token = await hre.ethers.getContractFactory("BYNToken")
  const token = await Token.connect(owner).deploy(initialSupply);

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
