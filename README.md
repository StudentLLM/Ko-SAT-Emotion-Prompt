# KoSAT Emotion-Prompt 🥼💊

KoSAT high-score with EmotionPrompt!!! We can do it!!!

## Usage

### 1. Environment Setup

```
cd Ko-SAT-Emotion-Prompt
pip install -r reqruiements.txt
```

### 2. OpenAI API Key Setup

```python
import os
import subprocess

# Set OpenAI API Key to environment variable
os.environ["OPENAI_API_KEY"] = "Your OpenAI API key"
```

### 3. Model Inference

**Korean**

```
python korean/korean_solve.py \
    --test_file data/korean/2024_korean.json \
    --emotion_prompt_path emotion_prompts.json \
    --save_path result/2024_korean.txt \
    --model OPENAI_MODEL \
    --is_front False or True
```

**English**

```
python english/english_solve.py \
    --test_file data/english/2024_English.json \
    --emotion_prompt_path emotion_prompts.json \
    --save_path result/2024_english.txt \
    --model OPENAI_MODEL \
    --is_front False or True
```

**Math**

```
python math/math_solve.py \
    --test_file data/math/2024_math.json \
    --emotion_prompt_path emotion_prompts.json \
    --save_path result/2024_math.txt \
    --model OPENAI_MODEL \
    --is_front False or True
```

## Citation

- [KICE_slayer_AI_Korean](https://github.com/NomaDamas/KICE_slayer_AI_Korean/tree/master)

```
@misc{li2023large,
      title={Large Language Models Understand and Can be Enhanced by Emotional Stimuli}, 
      author={Cheng Li and Jindong Wang and Yixuan Zhang and Kaijie Zhu and Wenxin Hou and Jianxun Lian and Fang Luo and Qiang Yang and Xing Xie},
      year={2023},
      eprint={2307.11760},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```