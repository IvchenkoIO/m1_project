import openai

def req():
    openai.api_key="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"
    model_engine = "text-davinci-003"
    prompt = "describe the ip"

    # задаем макс кол-во слов
    max_tokens = 128

    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(completion.choices[0].text)
    # выводим ответ
    return completion.choices[0].text

req()