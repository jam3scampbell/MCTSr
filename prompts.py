critique_sys_msg = (
    "You are working on a tough math problem.\n"
    "Point out flaws in the original problem.\n"
)


def critique_prompt(parent_content, original_problem):
    return (
        "Consider this math problem inside of <math_problem></math_problem> tags:\n"
        f"<math_problem>{original_problem}</math_problem>\n"
        "A student generated a solution to the original problem, inside of <draft_solution></draft_solution> tags.\n"
        f"<draft_solution>{parent_content}</draft_solution>\n"
        "Think of suggestions on how to improve this problem inside of <possible_refinement> tags.\n"
        "Reason through the problem inside of <reasoning> tags.\n"
        "Finally, conclude with a specific recommendation on how the student could improve their response inside of <recommendation> tags.\n"
        "Your final recommendation inside of <recommendation> tags should be at most a paragraph."
        "Your recommendation should make sense in a vacuum; reference the original problem to the student has proper context.\n"
        "Good luck!"
    )


respond_sys_msg = (
    "You are writing a second draft of a math problem solution.\n"
    "Attend to your teacher's critique and improve upon your previous solution.\n"
)


def respond_prompt(parent_content, original_problem, critique):
    return (
        "Consider this math problem inside of <math_problem></math_problem> tags:\n"
        f"<math_problem>{original_problem}</math_problem>"
        "You previously generated a solution to the original problem, inside of <draft_solution></draft_solution> tags.\n"
        f"<draft_solution>{parent_content}</draft_solution>\n"
        "Your teacher left you some valuable feedback, delimited by <teacher_feedback> tags.\n"
        f"<teacher_feedback>{critique}<teacher_feedback>\n"
        "Solve the math problem (in <math_problem> tags) again, incorporating the teacher's feedback.\n"
        "Do not put your response in XML tags. Just format it normally.\n"
        "Good luck!"
    )


eval_sys_msg = (
    "You are a teacher grading the a response to a math problem.\n"
    "Be strict but fair.\n"
)


def eval_prompt(student_solution, original_problem):
    return (
        f"<math_problem>{original_problem}</math_problem>\n"
        f"<student_solution>{student_solution}</student_solution>\n"
        "Please grade the student's solution to the math problem above, using the following rubric:\n"
        "UNDERSTANDING (30 points)\n"
        "- Conceptual Understanding (15 points)\n"
        "  - Does the student demonstrate a grasp of the core concepts required to solve the problem?\n"
        "  - Do they apply the relevant mathematical principles correctly?\n"
        "- Reasoning (15 points)\n"
        "  - Does the student provide clear explanations for each step of their solution?\n"
        "  - Do they justify their approach and avoid making unexplained leaps?\n"
        "CORRECTNESS (30 points)\n"
        "- Calculations (20 points)\n"
        "  - Are the student's calculations mathematically valid?\n"
        "  - Are the intermediate results correct?\n"
        "- Final Answer (10 points)\n"
        "  - Does the student arrive at the correct final answer?\n"
        "COMPLETENESS (15 points)\n"
        "- Addressing All Parts (10 points)\n"
        "  - Does the student's solution address all parts of the original problem?\n"
        "  - Are any required diagrams, graphs, or explanations missing?\n"
        "- Units and Labeling (5 points)\n"
        "  - Does the student include appropriate units for numerical answers?\n"
        "  - Are diagrams, graphs, tables, etc. properly labeled?\n"
        "CLARITY (15 points)\n"
        "- Organization (10 points)\n"
        "  - Is the student's work well-structured and easy to follow?\n"
        "  - Do they present their solution in a logical order?\n"
        "- Formatting (5 points)\n"
        "  - Are equations properly formatted?\n"
        "  - Is the handwriting or typing legible?\n"
        "EFFICIENCY (10 points)\n"
        "- Problem-Solving Strategy (5 points)\n"
        "  - Does the student use an appropriate and efficient strategy for solving the problem?\n"
        "- Conciseness (5 points)\n"
        "  - Does the student arrive at the solution in a reasonable number of steps?\n"
        "  - Is their work free of unnecessary detours or redundant calculations?\n"
        "Please give the score for each category and subcategory, along with an overall score.\n"
        "Explain your scoring with a few paragraphs for each subcategory.\n"
        "Conclude your evaluation with specific, actionable suggestions the student could implement to improve their solution.\n"
        "Finally, at the end, output the student's final score (0 - 100) inside of <final_score></final_score> tags. Only include the final number without any extra stuff and DON'T include '/100' in your answer.\n"
    )
