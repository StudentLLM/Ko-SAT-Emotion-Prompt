import json
import logging
import os

import click
import openai
from dotenv import load_dotenv
from tqdm import tqdm
import argparse

from math_prompts import basic_prompt, no_choice_prompt

OPENAI_MODELS = [
    "gpt-4-1106-preview",
    "gpt-4",
    "gpt-3.5-turbo-1106",
    "gpt-3.5"
]

def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument("--test_file", type=str, help="test file path")
    parser.add_argument("--emotion_prompt_path", type=str, help="emotion_prompts file path")
    parser.add_argument("--save_path", type=str, help="save path")
    parser.add_argument("--model", type=str, help=f"select openAI model to use: {OPENAI_MODELS}")
    parser.add_argument("--is_front", type=bool, help="If it's true, prompt will be appended after the system message, and if it's false, it will be appended after the question.")

    return parser.parse_args()

# file load code
def load_test(filepath: str):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'File not found: {filepath}')

    with open(filepath, 'rb') as f:
        test = json.load(f)

    total_score_test(test)
    return test

# total_score compute function
def total_score_test(data):
    total_score = 0

    for pa in data:
        for problem in pa["problems"]:
            total_score += problem["score"]

    assert (total_score == 100)
    print("test passed")

# OpenAI API Key Setup function
def set_openai_key():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    if not openai.api_key:
        raise ValueError("OPENAI API KEY empty!")

def get_prompt_by_type(type_num: int) -> callable:
    # 0 : multiple_choice, 1 : no_choice
    if type_num == 0:
        return basic_prompt
    else:
        return no_choice_prompt

def main():
    args = arg_parse()
    test_file = args.test_file
    save_path = args.save_path
    model = args.model
    is_front = args.is_front
    
    if not test_file:
        raise ValueError("test file not set!")
    if not save_path:
        raise ValueError("save path not set!")
    logging.basicConfig(filename=f"{save_path.split('.')[0]}_log.log", level=logging.INFO)

    set_openai_key()
    if model not in OPENAI_MODELS:
        raise ValueError(f"Unsupported openai model! Please select one of {OPENAI_MODELS}")
    
    test = load_test(test_file)
    with open(filepath, 'rb') as f:
        emotion_prompts = json.load(f)

    _id = 0

    with open(save_path, "w", encoding="UTF-8") as fw:
        for ep_index, ep in tqdm(enumerate(emotion_prompts), total=len(emotion_prompts)):
            for problem_index, problem in tqdm(enumerate(test), total=len(test)):
                _id += 1
                prompt_func = get_prompt_by_type(int(problem["type"]))
                answer = None
    
                for i in range(3):
                    try:
                        answer = prompt_func(
                            model=model,
                            question=problem["question"],
                            choices=problem["choices"],
                            question_plus=problem["question_plus"],
                            is_front=is_front,
                            emotion_prompt=ep
                        )
                        logging.info(answer)
                        break
                    except Exception as e:
                        print(f"RETRY, Failed! id: {_id} exception: {str(e)}")
    
                if not answer:
                    print(f"RETRY FAILED id: {_id}")
                    continue
    
                fw.write(f"""{_id}번 문제: {problem['question']}
                         EmotionPrompt: {ep}
                         정답: {problem['answer']}
                         배점: {problem['score']}
                         GPT 풀이: {answer}
                        ----------------------\n""")
                fw.flush()

if __name__ == "__main__":
    main()
