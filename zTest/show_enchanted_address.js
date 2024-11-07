
import { ethers } from 'ethers';

var args = process.argv;
var encryptedPk = args[2];
var password = args[3];

var wallet = await ethers.Wallet.fromEncryptedJson(encryptedPk, password);
console.log(wallet.address);



