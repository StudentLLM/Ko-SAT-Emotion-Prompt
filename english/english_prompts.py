import openai

# 영어는 문제 종류에 따라서 system_prompt에 차이를 두는게 좋을 것 같음..
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

    # for test
    # return system_prompt + user_prompt
    
    # ChatGPT, GPT-4 API generation
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return completion.choices[0].message.content
