import openai


def basic_prompt(model, question, choices, question_plus=""):
    # 여기에 Emotion Prompt를 적용하면 될 것 같음.
    # 예를 들어서 뭐 너는 서울대를 가려고 하는 학생이야! 너는 열심히 공부했고 문제를 잘 풀어낼 수 있을 거야. 그리고 틀리지 않았는지 한 번 검토해보는 것도 잊지 말고!
    # 이런 느낌?? 몰라 나도 잘
    system_prompt = """
        당신은 대학수학능력검정시험을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오.

        문제를 풀이할 때, 반드시 지문을 참고하세요.
         문제는 무조건 1개의 정답만 있습니다.
         문제를 풀이할 때 모든 선택지들을 검토하세요.
         모든 선택지마다 근거를 지문에서 찾아 설명하세요.

         다음의 형식을 따라 답변하세요.

         1번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 1번에 대한 답변)
         2번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 2번에 대한 답변)
         3번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 3번에 대한 답변)
         4번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 4번에 대한 답변)
         5번: "(지문 속 근거가 된 문장)" + (자세한 풀이) + (선택지 5번에 대한 답변)
         최종 정답: (최종 정답)
    """
    
    user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 [조건]이 주어져 있습니다. ~~
            문제의 각 선택지들을 해결하기 위한 배경 지식을 설명해 주고 있는 것이 <조건>로써, 각 선택지들을 지문과 연결시키고, <조건>의 지식을 활용하면 각 선택지의 참과 거짓을 판단할 수 있습니다.
            문제를 해결할 때, 반드시 <조건>의 내용을 이용해서 문제를 해결해야 합니다.
            [조건] :
            {question_plus}
        """
    user_prompt += f"""
        질문 :
        {question}

        선택지 :
        1번 - {choices[0]}
        2번 - {choices[1]}
        3번 - {choices[2]}
        4번 - {choices[3]}
        5번 - {choices[4]}

    """

    """
    질문의 구성 형식이
    paragraph + question_plus + question + choices 인 것 같음.

    우리의 EmotionPrompt는 System Prompt로 주는 것 같은데 이거는 얘기해봐야 할 듯 (system, question 뒤에 두가지 만들어보기로 함)
    """

    # ChatGPT, GPT-4 API generation
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        top_p=0.8,
        frequency_penalty=0.5
    )
    return completion.choices[0].message.content

def no_choice_prompt(model, question, choices, question_plus=""):
    system_prompt = """
        당신은 대학수학능력검정시험을 응시하는 대한민국의 n수생(수험생)으로서 다음의 문제의 답을 구하시오.

        ~~~
         다음의 형식을 따라 답변하세요.

         풀이: (자세한 풀이))
         최종 정답: (최종 정답)
    """

    user_prompt = ""

    if question_plus:
        user_prompt += f"""
            이 문제는 아래와 같이 [조건]이 주어져 있습니다. ~~
            문제의 각 선택지들을 해결하기 위한 배경 지식을 설명해 주고 있는 것이 <조건>로써
            문제를 해결할 때, 반드시 <조건>의 내용을 이용해서 문제를 해결해야 합니다.
            [조건] :
            {question_plus}
        """
    
    user_prompt += f"""
        질문 :
        {question}
    """

    # ChatGPT, GPT-4 API generation
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        top_p=0.8,
        frequency_penalty=0.5
    )
    return completion.choices[0].message.content
