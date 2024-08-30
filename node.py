from openrouter import oroute_chat
from prompts import *
from math import sqrt
from math import log as ln
import re


c = .3
eps = 0.01
temp = 1.2

class Node:
    errors = 0

    def __init__(self, content, parent, id=None):
        self.content = content
        self.q_value = None
        self.reward = 0
        self.visits = 0
        self.parent = parent
        self.num_children = 0
        self.id = id

        self.child_max_q = 0
        self.total_reward = 0
        self.min_reward = 0

    def determine_reward(self, original_problem):
        grading = oroute_chat(system_message=eval_sys_msg,
                              prompt=eval_prompt(self.content, original_problem),
                              temperature=temp)
        final_score_pattern = r'<final_score>(.*?)</final_score>'
        match = re.search(final_score_pattern, grading, re.DOTALL)
        if match:
            final_score = match.group(1).strip()
            try:
                final_score = max(-100, min(100, float(final_score)))
            except ValueError:
                print(f"Error: Could not convert final score '{final_score}' to float.")
                final_score = 0
                Node.errors += 1
        else:
            # print("Warning: No final score found in grading response.")
            final_score = 0
            Node.errors += 1
        # print(f"SCORE GIVEN BY THE JUDGE FOR {self.id}:", final_score)
        return final_score


    def calculate_q_value(self, original_problem, child_q_value=0, leaf=True):

        # self-evaluation
        reward = self.determine_reward(original_problem)
        self.visits += 1
        self.total_reward += reward
        self.min_reward = reward if reward < self.min_reward else self.min_reward
        self.q_value = (self.min_reward + self.total_reward/self.visits)/2

        # print(f"NEW Q VALUE ASSIGNED TO {self.id}:", self.q_value)

        # backpropagation
        if not leaf:
            if child_q_value > self.child_max_q:
                self.child_max_q = child_q_value
            self.q_value = .5*(self.q_value + self.child_max_q)

        if self.parent is None:
            return
        
        self.parent.calculate_q_value(original_problem, child_q_value=self.q_value, leaf=False)



    def self_refine(self, original_problem):
        critique_response = oroute_chat(system_message=critique_sys_msg, prompt=critique_prompt(
            self.content, original_problem), model="openai/gpt-4o-mini", temperature=temp)
        recommendation_pattern = r'<recommendation>(.*?)</recommendation>'
        match = re.search(recommendation_pattern, critique_response, re.DOTALL)
        if match:
            critique = match.group(1).strip()
            # print(f"CRITIQUE OF {self.id}: ", critique)
        else:
            critique = "No specific recommendation found."
            Node.errors += 1

        new_solution = oroute_chat(system_message=respond_sys_msg, prompt=respond_prompt(
            self.content, original_problem, critique), model="openai/gpt-4-mini", temperature=temp)
        # print(f"NEW SOLUTION FOR {self.id}:", new_solution)
        return new_solution

    def generate_children(self):
        pass

    def calculate_uct(self):
        if self.parent is None:
            uct_value = self.q_value + c*sqrt((ln(self.visits)) + 1 / (self.visits + eps))
            # print(f"UCT OF {self.id}:", uct_value)
            return uct_value
        uct_value = self.q_value + c*sqrt((ln(self.parent.visits)) + 1 / (self.visits + eps))
        # print(f"UCT OF {self.id}:", uct_value)
        return uct_value
    
    def __str__(self):
        return f"Node with id {self.id} and q value {self.q_value}"
