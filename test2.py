<<<<<<< HEAD
from Mine import *
from Transaction import *
import time
from flask import Flask, jsonify
from flask import request
import requests
=======
import json
import random
import bitcoin
from flask import Flask, jsonify, request

from Blockchain import Blockchain
>>>>>>> f73e5c5fc1a2cb16e4d04678db2a4d69bd843608

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

b = Blockchain()
<<<<<<< HEAD
m = Mine(b)
t = Transaction(b)


@app.route('/', methods=['GET'])
def get_chain():
    response = {
        'chain': b.chain,
=======


# blockchain 확인
@app.route('/', methods=['GET'])
def get_chain():
    block_json = []
    for block in b.chain:
        if 'list' in str(type(block['transactions'])):
            continue
        transactions = json.loads(block['transactions'])
        transaction_json = []
        for transaction in transactions:
            tx_input_json = []
            for input in json.loads(transaction['tx_inputs']):
                tx_input_json.append(input)
            tx_output_json = []
            for output in json.loads(transaction['tx_outputs']):
                tx_output_json.append(output)
            transaction['tx_inputs'] = tx_input_json
            transaction['tx_outputs'] = tx_output_json
            transaction_json.append(transaction)
        block['transactions'] = transaction_json
        block_json.append(block)
    response = {
        'chain': block_json,
>>>>>>> f73e5c5fc1a2cb16e4d04678db2a4d69bd843608
        'length': len(b.chain)
    }
    return response


<<<<<<< HEAD
@app.route('/mine', methods=['GET'])
def mining():
    block = m.mining()
    responses = {
        'message': 'Congrate! you mined a block!',
        **block
    }
    return responses

@app.route('/transactions', methods=['GET'])
def return_transactions():
    transaction_keys = ['sender', 'receiver', 'amount']
    response = {
        'message': f'available transactions :  {transaction_keys}'
    }
    return response

@app.route('/add_transaction', methods=['GET'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = t.add_transaction(
        sender=json['sender'],
        receiver=json['receiver'],
        amount=json['amount']
    )
    response = {
        'message': f'This transaction will be added to Block {index}'
    }

    print(index)
=======
# 키 생성
@app.route('/generatekey', methods=['GET'])
def generate_key():
    private_key = bitcoin.sha256(random.choice('something'))
    public_key = bitcoin.privkey_to_pubkey(private_key)
    address = bitcoin.pubkey_to_address(public_key)
    info = {
        'private_key': private_key,
        'public_key': public_key,
        'address': address
    }
    return info


# 블록 마이닝
@app.route('/mine', methods=['GET'])
def mining():
    request_json = request.get_json()
    block = b.create_block(request_json.get('private_key'))
    block['transactions'] = json.loads(block['transactions'])
    transaction_json = []
    for transaction in block['transactions']:
        tx_input_json = []
        for input in json.loads(transaction['tx_inputs']):
            tx_input_json.append(input)
        tx_output_json = []
        for output in json.loads(transaction['tx_outputs']):
            tx_output_json.append(output)
        transaction['tx_inputs'] = tx_input_json
        transaction['tx_outputs'] = tx_output_json
        transaction_json.append(transaction)
    block['transactions'] = transaction_json
    responses = {
        'message': 'Congrate! you mined a block!',
        'block': block,
    }
    return responses


@app.route('/add_transaction', methods=['GET'])
def add_transaction():
    request_json = request.get_json()
    transaction_keys = ['amount', 'receiver', 'sender', 'senderPrivate']
    if not all(key in request_json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    value = b.make_transaction(
        amount=request_json['amount'],
        receiver_address=request_json['receiver'],
        sender_address=request_json['sender'],
        sender_private_key=request_json['senderPrivate'],
    )

    if value == '잔액 부족':
        response = {
            'message': value
        }
    else:
        response = {
            'message': f'this transaction\'s hash value is {value}'
        }

>>>>>>> f73e5c5fc1a2cb16e4d04678db2a4d69bd843608
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        b.add_node(node)
    response = {
        'message': 'All the nodes are now connected. The Hatcoin Blockchain now contains the nodes',
        'total_message': list(b.nodes)
    }
    return jsonify(response), 201


@app.route('/update_chain', methods=['GET'])
def update_chain():
    is_chain_updated = b.update_chain()
<<<<<<< HEAD
    if is_chain_updated:
        response = {
            'message': 'The nodes had different chains so the chain was replacted by the longest chain.',
            'new_chain': b.chain
=======
    chain_json = []
    for i in range(len(b.chain)):
        chain_json.append(b.chain[i])
    if is_chain_updated:
        response = {
            'message': 'The nodes had different chains so the chain was replacted by the longest chain.',
            'new_chain': chain_json
>>>>>>> f73e5c5fc1a2cb16e4d04678db2a4d69bd843608
        }
    else:
        response = {
            'message': 'All good. The chain is the largest one.',
<<<<<<< HEAD
            'actual_chain': b.chain
=======
            'actual_chain': chain_json
>>>>>>> f73e5c5fc1a2cb16e4d04678db2a4d69bd843608
        }
    return jsonify(response), 200


<<<<<<< HEAD
=======
@app.route('/transactions', methods=['GET'])
def return_transactions():
    tx_json = []
    tx_list = b.transaction_list
    for tx in tx_list:
        tx['tx_inputs'] = json.loads(tx['tx_inputs'])
        tx['tx_outputs'] = json.loads(tx['tx_outputs'])
        tx_json.append(tx)
    return jsonify(tx_json), 201


>>>>>>> f73e5c5fc1a2cb16e4d04678db2a4d69bd843608
app.run(host='0.0.0.0', port=5001)
