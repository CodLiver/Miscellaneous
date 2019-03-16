import blockcypher


addr=blockcypher.generate_new_address(coin_symbol='btc-testnet', api_key= '32b0191e07db4a2eaf11dc6568c644b4')

print(addr)

#{'private': 'fc6bcef57f9ae29e25928641a9f70cfc2acbd734a5a445a94fa884bbdb20fb84', 'public': '02c18671d24509524bf64be7688b0cf745029951310de03e371e8eba743cca4cb6', 'address': 'muFrB2JPfA2yEAgi6y8eBo7SZQTCSvjXXV', 'wif': 'cW3NirDSBK8CJjRSDBJbpfpbSY9Kxvkm1Ljr8LB2S8ySySkQt6xx'}

#Specify the inputs and outputs below
#For convenince you can specify an address, and the backend will work out what transaction output that address has available to spend
#You do not need to list a change address, by default the transaction will be created with all change (minus the fees) going to the first input address
inputs = [{'address': 'muFrB2JPfA2yEAgi6y8eBo7SZQTCSvjXXV'}]
outputs = [{'value' : 0, 'script_type':"null-data", 'script':""}]
# outputs = [{'address': 'mpamtqLA66JFVSQNDaPHZ5xMiCz6T2MeNn', 'value': 100}]
"add"
print("OP_RETURN mjqf76".hex())
print(b'OP_RETURN mjqf76'.hex())
#The next line creates the transaction shell, which is as yet unsigned
unsigned_tx = blockcypher.create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc-testnet', api_key='32b0191e07db4a2eaf11dc6568c644b4')

#You can edit the transaction fields at this stage, before signing it.




# # Now list the private and public keys corresponding to the inputs
# private_keys=['fc6bcef57f9ae29e25928641a9f70cfc2acbd734a5a445a94fa884bbdb20fb84']
# public_keys=['02c18671d24509524bf64be7688b0cf745029951310de03e371e8eba743cca4cb6']
# #Next create the signatures
# tx_signatures = blockcypher.make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey_list=private_keys, pubkey_list=public_keys)
# #Finally push the transaction and signatures onto the network
# blockcypher.broadcast_signed_transaction(unsigned_tx=unsigned_tx, signatures=tx_signatures, pubkeys=public_keys, coin_symbol='btc-testnet', api_key='32b0191e07db4a2eaf11dc6568c644b4')
