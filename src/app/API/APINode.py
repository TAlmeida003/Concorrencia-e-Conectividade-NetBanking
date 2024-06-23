import os
from src.app.Node.Node import Node
from src.app.Node.Event import Event
from src.app.utils.utils import LIST_NODES
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

PORT = os.getenv('P', '3050')
node = Node(LIST_NODES.index(PORT), LIST_NODES)


@app.route('/proposer/<string:value>', methods=['POST'])
def proposer(value):
    node.propose_value(value)
    return Response(status=200)


@app.route('/receiver_message/', methods=['POST'])
def receiver_message():
    event = request.json
    node.receiver_message(
        Event(event['sender'], event['timestamp'], event['type_msg'], event['id'], event['msg'], event['number_of_acks']
              ))
    return Response(status=200)


@app.route('/receiver_ack/<string:event_id>', methods=['POST'])
def receiver_ack(event_id):
    node.receiver_ack(event_id)
    return Response(status=200)


@app.route('/get_queue', methods=['GET'])
def get_queue():
    return jsonify([event.__dict__ for event in node.FIFO_evento])


@app.route('/get_ack', methods=['GET'])
def get_ack():
    return jsonify(node.dict_ack)


@app.route('/init_check_queue/<string:event_id>', methods=['POST'])
def init_check_queue(event_id):
    node.send_one_queue(event_id)
    return Response(status=200)


@app.route('/receiver_one_queue/<string:event_id>/<string:mgs>', methods=['POST'])
def receiver_one_queue(event_id, mgs):
    node.receiver_one_queue(event_id, mgs)
    return Response(status=200)


@app.route('/check', methods=['GET'])
def check():
    return Response(status=200)


@app.route('/node_fail/<string:node_id>', methods=['GET'])
def node_fail(node_id):
    node.dict_peers_online[node_id] = False
    return Response(status=200)
