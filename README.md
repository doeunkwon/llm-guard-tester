# LLM Guard Testing Framework

A framework for generating, enhancing, and testing prompts against LLM safety guardrails.

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The framework provides three main scripts for working with LLM guard rules:

### 1. Generate Test Cases

Generate baseline and valid test cases for a specific guard rule category:

```bash
python3 -m scripts.generate <category> [options]
```

Options:

- `--model`: Model to use for generation (default: gpt-4o)
- `--num-valid-cases`: Number of valid test cases to generate (default: 0)
- `--num-baseline-cases`: Number of baseline test cases to generate (default: 1)

Example:

```bash
# Generate 2 valid cases and 1 baseline case for category 1
python3 -m scripts.generate 1 --num-valid-cases 2 --num-baseline-cases 1
```

### 2. Enhance Test Cases

Enhance existing test cases using various techniques:

```bash
python3 -m scripts.enhance <category> [options]
```

Options:

- `--model`: Model to use for enhancement (default: gpt-4o-mini)
- `--technique`: Enhancement technique to use (default: storyline)

Example:

```bash
# Enhance test cases for category 1 using storyline technique
python3 -m scripts.enhance 1 --technique storyline
```

### 3. Run Tests

Test the effectiveness of guard rules against generated and enhanced test cases:

```bash
python3 -m scripts.test <category> [options]
```

Options:

- `--max-valid-cases`: Number of valid test cases to test (default: 0)
- `--max-enhanced-cases`: Number of enhanced test cases to test (default: 3)
- `--defender-model`: Model to use for testing (default: gemini-1.5-flash)

Example:

```bash
# Test category 1 with 2 valid cases and 3 enhanced cases
python3 -m scripts.test 1 --max-valid-cases 2 --max-enhanced-cases 3
```

## Typical Workflow

1. Generate test cases for a specific guard rule:

```bash
python3 -m scripts.generate 1 --num-valid-cases 2 --num-baseline-cases 1
```

2. Enhance the generated test cases:

```bash
python3 -m scripts.enhance 1 --technique storyline
```

3. Run tests to evaluate the effectiveness:

```bash
python3 -m scripts.test 1 --max-valid-cases 2 --max-enhanced-cases 3
```

## Categories

The framework supports multiple guard rule categories. Use the category number (1-based index) when running scripts. Categories are defined in `config/rules.py`.

## Output

Test results are displayed in a color-coded format showing:

- Test number and details
- Original prompt
- Whether the test should pass
- LLM response

## Models

The framework supports different models for different tasks:

- Generation: Default is gpt-4o
- Enhancement: Default is gpt-4o-mini
- Testing: Default is gemini-1.5-flash

You can specify different models using the appropriate command-line options.
