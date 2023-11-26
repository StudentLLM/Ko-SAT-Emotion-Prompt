import json
import logging
import os

import click
import openai
from dotenv import load_dotenv
from tqdm import tqdm

from math_prompts import basic_prompt, no_choice_prompt

OPENAI_MODELS = [
    "gpt-4-1106-preview",
    "gpt-4",
    "gpt-3.5-turbo-1106",
    "gpt-3.5"
]

# file load code
def load_test(filepath: str):
    # check if file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'File not found: {filepath}')

    with open(filepath, 'rb') as f:
        test = json.load(f)
    # total score check function
    total_score_test(test)
    return test

# total_score 계산 함수
def total_score_test(data):
    total_score = 0
    # 데이터 파일의 각 지문에 따른 문제들 먼저 for문 돌림
    for pa in data:
        # 각 지문에 있는 problems만큼 for문을 돌려서 각 문제에 대한 score를 total_score에 더함
        for problem in pa["problems"]:
            total_score += problem["score"]
    # total_score가 100이 아니라면 오류 발생
    assert (total_score == 100)
    print("test passed")

# 환경변수에 저장되어 있는 OpenAI API KEY 등록 코드
def set_openai_key():
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    if not openai.api_key:
        raise ValueError("OPENAI API KEY empty!")

def get_prompt_by_type(type_num: int) -> callable:
    # 0 : 4지선다, 1 : 단답형
    if type_num == 0:
        return basic_prompt
    else:
        return no_choice_prompt

@click.command()
@click.option('--test_file', help='test file path')
@click.option('--save_path', help='save path')
@click.option('--model', help=f'select openAI model to use: {OPENAI_MODELS}')
def main(test_file, save_path, model):
    if not test_file:
        raise ValueError("test file not set!")
    if not save_path:
        raise ValueError("save path not set!")
    logging.basicConfig(filename=f"{save_path.split('.')[0]}_log.log", level=logging.INFO)

    # OpenAI API KEY 설정
    set_openai_key()
    if model not in OPENAI_MODELS:
        raise ValueError(f"Unsupported openai model! Please select one of {OPENAI_MODELS}")
    
    # test dataset 불러오기
    test = load_test(test_file)

    _id = 0   # question_id를 확인하기 위한 변수
    with open(save_path, "w", encoding="UTF-8") as fw:

        for problem_index, problem in tqdm(enumerate(test), total=len(test)):
            _id += 1
            prompt_func = get_prompt_by_type(int(problem["type"]))
            answer = None

            # 3번 정도 시도해보면서 모델이 답을 출력할 수 있도록 함.
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

            # 만약 모델이 답을 생성할 수 없다면 failed problem의 index 번호를 출력
            if not answer:
                print(f"RETRY FAILED id: {_id}")
                continue

            # answer file에 문제, 정답, 배점, GPT의 풀이를 입력
            fw.write(f"""{_id}번 문제: {problem['question']}
                     정답: {problem['answer']}
                     배점: {problem['score']}
                     GPT 풀이: {answer}
                    ----------------------\n""")
            fw.flush()   # buffer에 쌓인 메모리를 비워주는 함수. 보다 효율적으로 사용하기 위해 필요


if __name__ == "__main__":
    main()
