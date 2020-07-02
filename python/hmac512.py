from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import json

msg = b'This is the message to use to computer a MAC'
key = get_random_bytes(32)

hmac_generator = HMAC.new(key, digestmod=SHA256)
hmac_generator.update(msg[:10])
hmac_generator.update(msg[10:])

mac = hmac_generator.hexdigest()
print(mac)

# JSON Dictionary
json_dict = {'message': msg.decode('utf-8'),
             'MAC': mac}
# JSON Object
json_obj = json.dumps(json_dict)
print(json_obj)

# Receiver
# key shared securely
# public channel: json object
jo = json.loads(json_obj)

hmac_verifier = HMAC.new(key, digestmod=SHA256)
hmac_verifier.update(jo["message"].encode('utf-8'))

try:
    hmac_verifier.hexverify(jo["MAC"])
    print("The message is authentic\n")
except ValueError:
    print("The message or the key are wrong\n")
