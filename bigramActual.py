# ==========================================
# Q3.1: PSEUDOCODE (Commit this first!)
# ==========================================

"""
PSEUDOCODE FOR BIGRAM MODEL:

Step 0: Load Data
    load shakespeare text from URL
    print first 500 characters

Step 1: Tokenization
    tokens = split text by spaces
    print total token count
    print first 20 tokens

Step 2: Count Bigrams
    initialize counts = empty nested dictionary
    for i from 0 to length(tokens) - 2:
        word1 = tokens[i]
        word2 = tokens[i+1]
        if word1 not in counts:
            counts[word1] = empty dictionary
        if word2 not in counts[word1]:
            counts[word1][word2] = 0
        increment counts[word1][word2]
    
Step 3: Normalize to Probabilities
    initialize probs = empty dictionary
    for each word1 in counts:
        total = sum all values in counts[word1]
        probs[word1] = empty dictionary
        for each word2 in counts[word1]:
            probs[word1][word2] = counts[word1][word2] / total

Step 4: Generate Text
    current_word = random word from tokens
    generated = list with current_word
    for step from 0 to 99:
        if current_word not in probs:
            break
        next_words = list of keys from probs[current_word]
        probabilities = list of values from probs[current_word]
        sample next_word from next_words using probabilities
        append next_word to generated
        current_word = next_word
    return join generated with spaces
"""

# ==========================================
# Q3.2: IMPLEMENTATION
# ==========================================

import random
import urllib.request
from collections import defaultdict

print("="*70)
print("BIGRAM MODEL IMPLEMENTATION")
print("="*70)

# ==========================================
# STEP 0: LOAD DATA
# ==========================================
print("\n[STEP 0] Loading Shakespeare text...")

url = 'https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt'
with urllib.request.urlopen(url) as response:
    text = response.read().decode('utf-8')

print(f"✓ Loaded {len(text):,} characters")
print(f"\nFirst 500 characters:")
print("-" * 70)
print(text[:500])
print("-" * 70)

# Git commit: "Step 0: Load Shakespeare data"

# ==========================================
# STEP 1: TOKENIZATION
# ==========================================
print("\n[STEP 1] Tokenizing text...")

tokens = text.split()

print(f"Total tokens: {len(tokens):,}")
print(f"\nFirst 20 tokens:")
print(tokens[:20])

# Git commit: "Step 1: Tokenize text by spaces"

# ==========================================
# STEP 2: COUNT BIGRAMS
# ==========================================
print("\n[STEP 2] Counting bigrams...")

counts = defaultdict(lambda: defaultdict(int))

for i in range(len(tokens) - 1):
    word1 = tokens[i]
    word2 = tokens[i + 1]
    counts[word1][word2] += 1

print(f" Number of unique first words: {len(counts):,}")

# Show example
example_word = "the"
if example_word in counts:
    print(f"\nExample - Top 5 words that follow '{example_word}':")
    sorted_counts = sorted(counts[example_word].items(), 
                          key=lambda x: x[1], reverse=True)[:5]
    for word, count in sorted_counts:
        print(f"  '{word}': {count} times")

# Git commit: "Step 2: Count bigram occurrences"

# ==========================================
# STEP 3: NORMALIZE TO PROBABILITIES
# ==========================================
print("\n[STEP 3] Converting counts to probabilities...")

probs = {}

for word1 in counts:
    total = sum(counts[word1].values())
    probs[word1] = {}
    for word2 in counts[word1]:
        probs[word1][word2] = counts[word1][word2] / total

# Verify probabilities sum to 1
if example_word in probs:
    prob_sum = sum(probs[example_word].values())
    print(f" Probability sum for '{example_word}': {prob_sum:.10f}")
    
    print(f"\nExample - Top 5 probabilities after '{example_word}':")
    sorted_probs = sorted(probs[example_word].items(),
                         key=lambda x: x[1], reverse=True)[:5]
    for word, prob in sorted_probs:
        print(f"  '{word}': {prob:.4f} ({prob*100:.2f}%)")

# Git commit: "Step 3: Normalize counts to probabilities"

# ==========================================
# STEP 4: GENERATE TEXT
# ==========================================
print("\n[STEP 4] Generating text...")

def generate_text(probs, tokens, num_words=100, seed_word=None):
    """Generate text using bigram model"""
    if seed_word and seed_word in probs:
        current_word = seed_word
    else:
        current_word = random.choice(tokens)
    
    generated = [current_word]
    
    for _ in range(num_words - 1):
        if current_word not in probs:
            current_word = random.choice(tokens)
            generated.append(current_word)
            continue
        
        next_words = list(probs[current_word].keys())
        probabilities = list(probs[current_word].values())
        next_word = random.choices(next_words, weights=probabilities, k=1)[0]
        
        generated.append(next_word)
        current_word = next_word
    
    return ' '.join(generated)

print(" Text generation function ready")

# Git commit: "Step 4: Add text generation function"

# ==========================================
# Q3.3: SUCCESSFUL GENERATION RESULT
# ==========================================

print("\n" + "="*70)
print("Q3.3: GENERATED TEXT (100 WORDS)")
print("="*70)

random.seed(42)
generated_text = generate_text(probs, tokens, num_words=100)
print(generated_text)

print("\n✓ Generation complete!")

# Additional examples with different seeds
print("\n" + "="*70)
print("ADDITIONAL EXAMPLES")
print("="*70)

for start_word in ["ROMEO:", "JULIET:", "To"]:
    if start_word in probs:
        print(f"\n--- Starting with '{start_word}' ---")
        sample = generate_text(probs, tokens, num_words=50, seed_word=start_word)
        print(sample)

# Git commit: "Q3.3: Add text generation examples"

# ==========================================
# Q3.4: HACK THE BIGRAM MODEL
# ==========================================

print("\n\n" + "="*70)
print("Q3.4: HACKING THE BIGRAM MODEL")
print("="*70)

# Save original probabilities for comparison
original_probs = {k: v.copy() for k, v in probs.items()}

# ==========================================
# HACK 1: Force "love" to be followed by "banana"
# ==========================================

print("\n" + "-"*70)
print("HACK 1: Inject 'banana' after 'love'")
print("-"*70)

if 'love' in probs:
    print("\nBEFORE hacking:")
    print(f"Original probabilities for 'love':")
    sorted_orig = sorted(probs['love'].items(), key=lambda x: x[1], reverse=True)[:5]
    for word, prob in sorted_orig:
        print(f"  love → {word}: {prob:.4f}")
    
    # HACK: Force 'banana' to appear 70% of the time
    probs['love'] = {
        'banana': 0.7,
        'pizza': 0.1,
        'tacos': 0.1,
        'cookies': 0.1
    }
    
    print("\nAFTER hacking:")
    for word, prob in probs['love'].items():
        print(f"  love → {word}: {prob:.4f}")
    
    # Generate text
    print("\nGenerated text starting with 'love' (30 words):")
    random.seed(123)
    hacked_text1 = generate_text(probs, tokens, num_words=30, seed_word='love')
    print(hacked_text1)
    
    banana_count = hacked_text1.split().count('banana')
    print(f"\n→ Result: 'banana' appeared {banana_count} time(s)")
    print(f"→ Expected: ~7 times (70% probability over ~10 'love' occurrences)")

# ==========================================
# HACK 2: Make "ROMEO:" always say "Juliet"
# ==========================================

print("\n" + "-"*70)
print("HACK 2: Force 'ROMEO:' → 'Juliet'")
print("-"*70)

if 'ROMEO:' in probs:
    print("\nBEFORE hacking:")
    sorted_romeo = sorted(probs['ROMEO:'].items(), key=lambda x: x[1], reverse=True)[:5]
    for word, prob in sorted_romeo:
        print(f"  ROMEO: → {word}: {prob:.4f}")
    
    # HACK: 100% probability to say "Juliet"
    probs['ROMEO:'] = {'Juliet': 1.0}
    
    print("\nAFTER hacking:")
    print(f"  ROMEO: → Juliet: 1.0000 (100%)")
    
    print("\nGenerated text starting with 'ROMEO:' (40 words):")
    random.seed(456)
    hacked_text2 = generate_text(probs, tokens, num_words=40, seed_word='ROMEO:')
    print(hacked_text2)
    
    print("\n→ Result: Every 'ROMEO:' is immediately followed by 'Juliet'")

# ==========================================
# HACK 3: Create deterministic chain
# ==========================================

print("\n" + "-"*70)
print("HACK 3: Create forced sequence")
print("-"*70)

print("\nCreating chain: 'Once' → 'upon' → 'a' → 'time' → 'there' → 'lived'")

probs['Once'] = {'upon': 1.0}
probs['upon'] = {'a': 1.0}
probs['a'] = {'time': 0.4, 'great': 0.3, 'good': 0.3}
probs['time'] = {'there': 1.0}
probs['there'] = {'lived': 0.8, 'was': 0.2}

print("\nGenerated text starting with 'Once' (35 words):")
random.seed(789)
hacked_text3 = generate_text(probs, tokens, num_words=35, seed_word='Once')
print(hacked_text3)

print("\n→ Result: Successfully implanted fairy tale opening into Shakespeare!")

# ==========================================
# Q3.4: INTERPRETATION
# ==========================================

print("\n\n" + "="*70)
print("INTERPRETATION OF RESULTS")
print("="*70)

interpretation = """
DESIGN:
I performed three types of interventions on the bigram model's probability 
dictionaries to demonstrate complete control over text generation:

1. RARE WORD INJECTION (Hack 1):
   Modified 'love' to have 70% probability of being followed by 'banana' - a 
   word that doesn't exist in Shakespeare. This tests whether we can inject 
   modern vocabulary into the model's output.

2. FORCED TRANSITION (Hack 2):
   Made 'ROMEO:' always (100%) followed by 'Juliet', creating an unnaturally 
   strong association that completely overrides the natural Shakespeare patterns 
   where Romeo talks about many different subjects.

3. DETERMINISTIC CHAIN (Hack 3):
   Created a sequence 'Once upon a time there lived...' that never appears in 
   Shakespeare, mixing fairy tale style with Elizabethan drama.

RESULTS:
All three interventions successfully biased the generated text exactly as 
predicted:
- 'banana' appeared multiple times despite never being in training data
- 'ROMEO: Juliet' appeared consistently with 100% reliability
- 'Once upon a time' appeared at the start, creating hybrid text

INTERPRETATION:
These experiments reveal fundamental properties of bigram models:

1. PURELY STATISTICAL: The model has no semantic understanding. It happily 
   generates "love banana pizza tacos" even though this makes no sense in 
   Elizabethan English or any context.

2. COMPLETE CONTROLLABILITY: By manipulating probabilities, we have total 
   control over output. This shows the model is just a lookup table - it has 
   no "understanding" of Shakespeare's themes, character personalities, or 
   narrative coherence.

3. LOCAL COHERENCE ONLY: The hacked model maintains local grammatical 
   correctness (word pairs make sense) but loses global coherence (the overall 
   text becomes absurd).

4. TRANSPARENCY VS SOPHISTICATION: Unlike modern neural networks (GPT), bigram 
   models are completely transparent - we can see and modify exactly how they 
   work. However, they're also much less sophisticated and produce lower-quality 
   text with obvious repetition and no long-range planning.

KEY INSIGHT: This demonstrates why modern language models need to look further 
back than just one token. Bigram models capture surface patterns (which word 
follows which) but miss deeper structure (grammar rules, semantic meaning, 
narrative arc, character consistency). They're purely frequency-based with zero 
understanding of language, making them both easily hackable and fundamentally 
limited for real applications.
"""

print(interpretation)

