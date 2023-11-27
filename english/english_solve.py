import json
import logging
import os

import click
import openai
from tqdm import tqdm
import argparse

from english_prompts import basic_prompt, data_prompt, ordering_prompt

OPENAI_MODELS = [
    "gpt-4-1106-preview",
    "gpt-4",
    "gpt-3.5-turbo-1106",
    "gpt-3.5"
]

def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument("--test_file", type=str, help="test file path")
    parser.add_argument("--save_path", type=str, help="save path")
    parser.add_argument("--model", type=str, help=f"select openAI model to use: {OPENAI_MODELS}")

    return parser.parse_args()

# file load function
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
    # 0 : basic, 1 : data, 2 : ordering
    if type_num == 0:
        return basic_prompt
    elif type_num == 1:
        return data_prompt
    else:
        return ordering_prompt

def main():
    args = arg_parse()
    test_file = args.test_file
    save_path = args.save_path
    model = args.model
    
    if not test_file:
        raise ValueError("test file not set!")
    if not save_path:
        raise ValueError("save path not set!")
    logging.basicConfig(filename=f"{save_path.split('.')[0]}_log.log", level=logging.INFO)

    set_openai_key()
    if model not in OPENAI_MODELS:
        raise ValueError(f"Unsupported openai model! Please select one of {OPENAI_MODELS}")
    
    test = load_test(test_file)

    _id = 0

    def get_answer(problem, _id):
        prompt_func = get_prompt_by_type(int(problem["type"]))
        answer = None
        
        for i in range(3):
            try:
                answer = prompt_func(
                    model=model,
                    question=problem["question"],
                    choices=problem["choices"],
                    question_plus=problem["question_plus"],
                )
                logging.info(answer)
                break
            except Exception as e:
                print(f"RETRY, Failed! id: {_id} exception: {str(e)}")

        if not answer:
            print(f"RETRY FAILED id: {_id}")

        return answer
        
    with open(save_path, "w", encoding="UTF-8") as fw:
        answer = None
        
        for problem_index, problem in tqdm(enumerate(test), total=len(test)):
            if "paragraph" in list(problem.keys()):
                paragraph = problem["paragraph"]
                for prob in problem["problems"]:
                    prob["question"] = paragraph + "\n\n" + prob["question"]
                    _id+=1
                    answer = get_answer(prob, _id)

                    # answer file에 문제, 정답, 배점, GPT의 풀이를 입력
                    fw.write(f"""{_id}번 문제: {prob['question'].replace(paragraph, "")}
                             정답: {prob['answer']}
                             배점: {prob['score']}
                             GPT 풀이: {answer}
                            ----------------------\n""")
                    fw.flush()
            else:
                _id+=1
                answer = get_answer(problem, _id)

                fw.write(f"""{_id}번 문제: {problem['question']}
                         정답: {problem['answer']}
                         배점: {problem['score']}
                         GPT 풀이: {answer}
                        ----------------------\n""")
                fw.flush()

if __name__ == "__main__":
    main()
