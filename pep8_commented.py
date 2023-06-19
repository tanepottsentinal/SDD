# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/
# requests==2.18.4: pip install requests==2.18.4

# Importing libraries

import datetime 
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


##############################################################################################################

# Blockchain

class Blockchain:

 # Initializing the Blockchain

 def __init__(self):
     self.chain = []
     self.transactions = []
     self.create_block(proof = 1, previous_hash = '0')
     self.nodes = set()
 
 # Creating a new block  

 def create_block(self, proof, previous_hash):
     block = {'index': len(self.chain) + 1,
             'timestamp': str(datetime.datetime.now()),
             'proof': proof,
             'previous_hash': previous_hash,
             'transactions': self.transactions}
     self.transactions = []
     self.chain.append(block)
     return block
 
 # Getting the previous block

 def get_previous_block(self):
     return self.chain[-1]
 
 # Getting the proof of work

 def proof_of_work(self, previous_proof):
     new_proof = 1
     check_proof = False

     # Creating a loop to find the correct proof of work

     while check_proof is False:
         hash_operation = hashlib.sha256,

         # Using the SHA256 algorithm to hash the operation

         (str(new_proof**2 - previous_proof**2).encode()).hexdigest()

         # Checking if the first 4 digits of the hash are equal to 0000
         # If they are equal to 0000, the proof of work is correct
         if hash_operation[:4] == '0000':
             check_proof = True

         # If the proof of work is incorrect, we increment the new_proof by 1 and we try again
         
         else:
             new_proof += 1
     return new_proof
 
 def hash(self, block):
     encoded_block = json.dumps(block, sort_keys = True).encode()
     return hashlib.sha256(encoded_block).hexdigest()
 
 def is_chain_valid(self, chain):
     previous_block = chain[0]
     block_index = 1

     # Checking if the previous hash of the current block is equal to the hash of the previous block

     while block_index < len(chain):
         block = chain[block_index]

         # Checking if the previous hash of the current block is equal to the hash of the previous block

         if block['previous_hash'] != self.hash(previous_block):
             return False
         previous_proof = previous_block['proof']
         proof = block['proof']

         # Checking if the hash of the block is valid

         hash_operation = hashlib.sha256,
         (str(proof**2 - previous_proof**2).encode()).hexdigest()

         # Checking if the first 4 digits of the hash are equal to 0000
         # If they are not equal to 0000, the chain is not valid

         if hash_operation[:4] != '0000':
             return False
         previous_block = block
         block_index += 1
     return True
 
 # Adding a transaction to the Blockchain
 
 def add_transaction(self, sender, receiver, amount):
     self.transactions.append({'sender': sender,
                             'receiver': receiver,
                             'amount': amount})
     previous_block = self.get_previous_block()
     return previous_block['index'] + 1
 
 # Adding a new node to the Blockchain

 def add_node(self, address):
     parsed_url = urlparse(address)
     self.nodes.add(parsed_url.netloc)
 
 # Replacing the chain by the longest chain if needed

 def replace_chain(self):
     network = self.nodes
     longest_chain = None
     max_length = len(self.chain)

     # Looking for chains longer than the pre existing chain

     for node in network:
         response = requests.get(
             f'http://{node}/get_chain')
         
         # Checking if the response is valid

         if response.status_code == 200:
             length = response.json()['length']
             chain = response.json()['chain']

             # Checking if the chain is longer than the pre existing chain and if the chain is valid

             if length > max_length and self.is_chain_valid(chain):
                 max_length = length
                 longest_chain = chain

     # If the chain is longer than the pre existing chain, we replace the pre existing chain by the longest chain
     
     if longest_chain:
         self.chain = longest_chain
         return True
     return False


##############################################################################################################


# Using the Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():

 # Getting the previous block

 previous_block = blockchain.get_previous_block()

 # Getting the proof of work of the previous block

 previous_proof = previous_block['proof']

 # Getting the proof of work of the current block

 proof = blockchain.proof_of_work(previous_proof)

 # Getting the hash of the previous block

 previous_hash = blockchain.hash(previous_block)

 # Adding a transaction to the Blockchain

 blockchain.add_transaction(
     sender = node_address, receiver = 'You', amount = 1)
 block = blockchain.create_block(proof, previous_hash)

 # Creating the response

 response = {'message': 'Congratulations, you just mined a block!',
             'index': block['index'],
             'timestamp': block['timestamp'],
             'proof': block['proof'],
             'previous_hash': block['previous_hash'],
             'transactions': block['transactions']}
 return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
 response = {'chain': blockchain.chain,
             'length': len(blockchain.chain)}
 return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
 is_valid = blockchain.is_chain_valid(blockchain.chain)

 # If the Blockchain is valid return this message

 if is_valid:
     response = {'message': 'All good. The Blockchain is valid.'}

 # If the Blockchain isn't valid return this message

 else:
     response = {
         'message': 'Houston, we have a problem. The Blockchain is not valid.'}
 return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
 json = request.get_json()
 transaction_keys = ['sender', 'receiver', 'amount']

 # If some elements of the transaction are missing, return this message

 if not all(key in json for key in transaction_keys):
     return 'Some elements of the transaction are missing', 400
 
 # If all elements of the transaction are present, add the transaction to the Blockchain

 index = blockchain.add_transaction(
     json['sender'], json['receiver'], json['amount'])
 response = {
     'message': f'This transaction will be added to Block {index}'}
 return jsonify(response), 201

##############################################################################################################

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():

 # Getting the nodes from the request

 json = request.get_json()
 nodes = json.get('nodes')
 if nodes is None:
     return "No node", 400
 
 # Connecting the nodes by looping through each them

 for node in nodes:
     blockchain.add_node(node)
 response = {'message': 'All the nodes are now connected. The Potcoin Blockchain now contains the following nodes:',
             'total_nodes': list(blockchain.nodes)}
 return jsonify(response), 201

# Replacing the chain by the longest chain if needed7
@app.route('/replace_chain', methods = ['GET'])

# Checking if the chain is the longest chain

def replace_chain():
 is_chain_replaced = blockchain.replace_chain()
 if is_chain_replaced:
     response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                 'new_chain': blockchain.chain}
     
 # If the chain is the longest chain, return this message

 else:
     response = {'message': 'All good. The chain is the largest one.',
                 'actual_chain': blockchain.chain}
 return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5001)                                                                                      