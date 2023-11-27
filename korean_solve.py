import json
import logging
import os

import click
import openai
from dotenv import load_dotenv
from tqdm import tqdm
import argparse

from korean_prompts import basic_prompt, literature_prompt, grammar_prompt

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

# 한 문제에 대한 model의 answer 추출 함수
def get_answer_one_problem(data, model: str, paragraph_num: int, problem_num: int, prompt_func: callable = basic_prompt):
    # paragraph_num: 지문 index / problem_num: 각 지문에 속한 problem index
    problem = data[paragraph_num]["problems"][problem_num]
    no_paragraph = False

    # 만약 problem dictionary이 key 값에 'no_paragraph'가 있다면 no_paragraph = True
    # 근데 Ctrl + F로 찾아보니 그런 값은 없던데 머쓱
    if "no_paragraph" in list(problem.keys()):
        no_paragraph = True

    # question_plus가 있다면 따로 question_plus_text 변수에 넣어둠
    if "question_plus" in list(problem.keys()):
        question_plus_text = problem["question_plus"]
    else:
        question_plus_text = ""

    # prompt_func에 모든 값을 넣음. 여기서 prompt_func는 
    return prompt_func(
        model=model,
        paragraph=data[paragraph_num]["paragraph"],
        question=problem["question"],
        choices=problem["choices"],
        question_plus=question_plus_text,
        no_paragraph=no_paragraph
    )

# 과목의 영역을 분류하는 것 같은데, 어차피 우리는 영역이 다 하나씩 밖에 없으니까 각 과목별로 prompt를 만들어서 분류하는 역할을 하는 function으로 만들면 될 것 같음.
# 그러기 위해서는 prompt.py에서 prompt 형식을 각 과목별로 만들어두는 것이 좋을 것 같음.
# ex. 0: 국어, 1: 수학, 2: 영어
def get_prompt_by_type(type_num: int) -> callable:
    # 0 : 비문학, 1 : 문학, 2 : 화법과 작문, 3 : 문법
    if type_num == 0:
        return literature_prompt
    elif type_num == 1:
        return literature_prompt
    elif type_num == 2:
        return literature_prompt
    else:
        return grammar_prompt

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

    # OpenAI API KEY 설정
    set_openai_key()
    if model not in OPENAI_MODELS:
        raise ValueError(f"Unsupported openai model! Please select one of {OPENAI_MODELS}")
    
    # test dataset 불러오기
    test = load_test(test_file)

    _id = 0   # question_id를 확인하기 위한 변수
    with open(save_path, "w", encoding="UTF-8") as fw:
        for paragraph_index, paragraph in enumerate(test):   # (paragraph_index=0,1,2..., paragraph=test[i])로 만듦.

            # 아 데이터셋에서 type을 설정해둔 것이 prompt를 적용하기 위해 설정한 거였네
            # 뭐 우리가 따로 만들든 아니면 그냥 for문 돌아가면서 적절하게 하든, 아님 걍 하나씩 하든 해도 상관 없을 듯.
            # 이왕이면 추가해놓는 게 자동화를 위해서는 더 좋을 듯
            prompt_func = get_prompt_by_type(int(paragraph["type"]))

            # 한 지문에 들어있는 problems를 추출해서 (problem_index=0,1,2..., problem=paragraph["problems"][i])로 만듦.
            for problem_index, problem in tqdm(enumerate(paragraph["problems"]), total=len(paragraph["problems"])):
                _id += 1

                # 만약 문제의 type이 살짝 다르다면 prompt_func를 다르게 설정
                if "type" in list(problem.keys()):
                    prompt_func = get_prompt_by_type(int(problem["type"]))
                answer = None

                # 3번 정도 시도해보면서 모델이 답을 출력할 수 있도록 함.
                for i in range(3):
                    try:
                        answer = get_answer_one_problem(test, model, paragraph_index, problem_index, prompt_func)
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
