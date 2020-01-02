def generate_hash(password):
  return sha256.hash(password) 
def verify_hash(password, hash):
  return sha256.verify(password, hash)

