loadScript("ZigBeeComplianceAddress.js")
loadScript("ZigBeeCompliance.js")
var ZigBeeContract = web3.eth.contract(JSON.parse(ZigBeeCompliance.contracts["ZigBeeCompliance.sol:ZigBeeCompliance"].abi));
var ZigBee = eth.contract(ZigBeeContract.abi).at(ZigBeeComplianceAddress);

loadScript("ModelInfoAddress.js")
loadScript("ModelInfo.js")
var ModelInfoContract = web3.eth.contract(JSON.parse(ModelInfoOutput.contracts["ModelInfo.sol:ModelInfo"].abi));
var ModelInfo = eth.contract(ModelInfoContract.abi).at(ModelInfoAddress);

loadScript("DeviceSecurityAddress.js")
loadScript("DeviceSecurity.js")
var DeviceSecurityContract = web3.eth.contract(JSON.parse(DeviceSecurityOutput.contracts["DeviceSecurity.sol:DeviceSecurity"].abi));
var DeviceSecurity = eth.contract(DeviceSecurityContract.abi).at(DeviceSecurityAddress);

loadScript("MetaDataAddress.js")
loadScript("MetaData.js")
var MetaDataContract = web3.eth.contract(JSON.parse(MetaDataOutput.contracts["MetaData.sol:MetaData"].abi));
var MetaData = eth.contract(MetaDataContract.abi).at(MetaDataAddress);

loadScript("SimpleStorageAddress.js")
loadScript("SimpleStorage.js")
var SimpleStorageContract = web3.eth.contract(JSON.parse(SimpleStorage.contracts["SimpleStorage.sol:SimpleStorage"].abi));
var SimpleStorage = eth.contract(SimpleStorageContract.abi).at(SimpleStorageAddress);

