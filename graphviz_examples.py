from flask import Flask, render_template, jsonify
import pygraphviz as pgv
import json

# app = Flask(__name__)

# def get_graph_data():

G = pgv.AGraph(directed=True)

# Add nodes with metadata and short descriptions
nodes = [
    {'id': 'A', 'label': 'A', 'short_desc': 'Root node', 'metadata': 'Root node metadata: Full description of node A'},
    {'id': 'B', 'label': 'B', 'short_desc': 'Child of A', 'metadata': 'Child of A metadata: Full description of node B'},
    {'id': 'C', 'label': 'C', 'short_desc': 'Child of A', 'metadata': 'Child of A metadata: Full description of node C'}
]

for node in nodes:
    G.add_node(node['id'], label=f"{node['label']}\n{node['short_desc']}")

# Add edges
G.add_edge('A', 'B')
G.add_edge('A', 'C')

# Convert graph to a JSON format suitable for D3.js
edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]

graph_data = {
    'nodes': nodes,
    'links': edges
}

# return graph_data

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/graph')
# def graph():
#     return jsonify(get_graph_data())
# if __name__ == '__main__':
#     app.run(debug=True)
