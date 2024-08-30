from node import Node
import random
from flask import Flask, render_template, jsonify
import threading
import pygraphviz as pgv
from IPython.display import Image, display
from time import time

node_counter = 0
expansion_limit = 5
math_problem = """Evaluate the following expression: (7 * 4) ** 2 / 14 - (5 + 3 * 2)"""

# app = Flask(__name__)

class Tree:
    def __init__(self, root: Node):
        self.G = pgv.AGraph(directed=True)
        self.nodes = [{'id': root.id, 'label': root.id, 'short_desc': root.content, 'metadata': 'blank'}]
        text_in_bubble = f"{root.id}\n{root.content}"
        wrapped_text = self.wrap_text(text_in_bubble)
        self.G.add_node(root.id, label=wrapped_text)
        self.edges = []

    def get_graph_data(self):
        graph_data = {
            'nodes': self.nodes,
            'links': self.edges
        }
        return graph_data
    
    def add_node_to_tree(self, node: Node):
        self.nodes.append({'id': node.id, 'label': node.id, 'short_desc': node.content, 'metadata': 'blank'})
        text_in_bubble = f"{node.id}\n{node.q_value}\n{node.content}"
        wrapped_text = self.wrap_text(text_in_bubble)
        self.G.add_node(node.id, label=wrapped_text)
        self.G.add_edge(node.parent.id, node.id)  # fix edge direction
        self.edges.append({'source': node.parent.id, 'target': node.id})

    def wrap_text(self, text):
        wrapped_text = ""
        idx = 0
        for char in text:
            idx+=1
            wrapped_text = wrapped_text + char
            if idx > 50 and char == " ":
                wrapped_text = wrapped_text + "\n"
                idx = 0
        return wrapped_text


# def run_flask_app():
#     app.run(port=5001, debug=False, use_reloader=False)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/graph')
# def graph():
#     return jsonify(tree.get_graph_data())

if __name__ == "__main__":
    default_answers = [
    "The expression evaluates to 7"
    ]

    node_counter += 1
    node = Node(random.choice(default_answers), parent=None, id=str(node_counter))

    node.visits = 1
    node.calculate_q_value(math_problem)
    candidates = {node: node.calculate_uct()}

    tree = Tree(node)  
    tree.G.draw('tree.png', prog='dot')
    display(Image(filename='tree.png'))
    # flask_thread = threading.Thread(target=run_flask_app)
    # flask_thread.start()
    # print("Started Flask app")

    for _ in range(20):
        start_iteration = time()

        for node in candidates.keys():
            candidates[node] = node.calculate_uct()
            print(node, candidates[node])
        node_of_interest = max(candidates, key=candidates.get)

        new_answer = node_of_interest.self_refine(math_problem)
        node_counter += 1
        child_node = Node(new_answer, parent=node_of_interest, id=str(node_counter))
        node_of_interest.num_children += 1

        

        child_node.calculate_q_value(math_problem)

        tree.add_node_to_tree(child_node)

        # update candidates
        candidates[child_node] = child_node.calculate_uct()
        candidates = dict(filter(lambda x: (x[0].num_children < expansion_limit) or (x[0].child_max_q < x[0].q_value), candidates.items()))
        tree.G.draw('tree.png', prog='dot')
        display(Image(filename='tree.png'))
    # flask_thread.join()
