from collections import defaultdict, Counter
from value import *

# Function to build the transition matrix
def build_transition_matrix(numbers, memory):
    transitions = defaultdict(Counter)
    for i in range(len(numbers) - memory):
        state = tuple(numbers[i:i + memory])
        next_number = numbers[i + memory]
        transitions[state][next_number] += 1
    return transitions

# Function to get probabilities from a transition matrix
def get_probabilities(transition_matrix, state):
    if state in transition_matrix:
        total = sum(transition_matrix[state].values())
        return {k: v / total for k, v in transition_matrix[state].items()}
    return {}

# Function to blend probabilities
def blend_probabilities(local_probs, global_probs, local_weight=0.7, global_weight=0.3):
    combined_probs = defaultdict(float)
    
    # Add weighted local probabilities
    for number, prob in local_probs.items():
        combined_probs[number] += local_weight * prob
    
    # Add weighted global probabilities
    for number, prob in global_probs.items():
        combined_probs[number] += global_weight * prob
    
    return combined_probs

# Predict the next number using blended probabilities
def predict_next_with_baseline(global_matrix, local_matrix, recent_numbers, memory, local_weight=0.7):
    state = tuple(recent_numbers)
    
    # Get probabilities from local and global matrices
    local_probs = get_probabilities(local_matrix, state)
    global_probs = get_probabilities(global_matrix, state)
    
    # If local probabilities are empty, rely entirely on global
    if not local_probs:
        local_weight = 0.0
        global_weight = 1.0
    else:
        global_weight = 1 - local_weight
    
    # Blend the probabilities
    blended_probs = blend_probabilities(local_probs, global_probs, local_weight, global_weight)
    
    # If no valid probabilities, fallback to random choice
    if not blended_probs:
        print("No valid probabilities found, returning fallback value.")
        return 0  # Return a fallback value or an arbitrary number
    
    # Select the number with the highest probability
    next_number = max(blended_probs, key=blended_probs.get)
    return next_number

# Ensure 'values' is correctly defined in your environment
values = valuesa
memory = 5  # Length of the recent numbers to consider

# Check if the dataset is large enough
if len(values) < memory:
    print(f"Error: Dataset has fewer than {memory} elements.")
else:
    # Build global transition matrix using all data
    global_matrix = build_transition_matrix(values, memory)

    # Simulate a scenario with the last 10 numbers as local context
    recent_numbers = values[-memory:]
    local_matrix = build_transition_matrix(values[-20:], memory)  # Use the last 20 numbers for local trends

    # Predict the next number
    predicted_number = predict_next_with_baseline(global_matrix, local_matrix, recent_numbers, memory, local_weight=0.7)

    print(f"Predicted next number: {predicted_number}")
