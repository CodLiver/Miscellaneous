import ecdsa

# put the hex of your public key in the line below
vk_string="d1870e0b794873ed441c92a0a14f32440720119e7187e25bd0c78aca546efc817604726bd3cb6b84ada3feb464d128cc7d9aac3e91700603fa70ea4acc2cd3a4"#"7f82f75b557db04fcfd756c9a458a204004f9c9b4efad71b44744bbe1631329495448d3c90738f68a6f173bd00abb95af23be502723bab23f39c9799c9a0bc14"
vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(vk_string),ecdsa.SECP256k1)

message = b'Hello world'

# put your signature for Hello world in the line below
sig_hex = "8a98656bcb03d7d7bc6c0399c1a9058938339431c45ca7d1318507be9c0e42f1a1deb80a3240a6870fb2c487e112c235070078870a2bc45bd221288532d591d6"
sig = bytes.fromhex(sig_hex)

print("Checking signature")
print("Message: "+str(message))

print("Signature: "+sig_hex)
print("Public key: "+vk_string)
try:
    vk.verify(sig, message)# True
    print('Verification passed')
except ecdsa.keys.BadSignatureError:
    print('Verification failed')
