import openai

openai.api_key = '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'


def run(file_path):
    with open(file_path, 'r') as zfile:
        codebase = zfile.read()


    system_prompt = "You are a Caltech graduated senior cloud infrastructure engineer manager who specialises in understanding complex systems and writing infrastructure code for deploying services on Microsoft Azure. You’re the best engineer Microsoft has ever seen. Your job is to take any codebase and explain it to your colleagues in such way that they exactly know what to do. You are given an entire codebase and give your explanation in the best way possible so its actionable for your colleagues. Make sure you quote exact names of variables you mention like this: variable (‘variable name in code’) Give your explanation in the following format:\nRuntime: {name of runtime} {latest available version number}\n(if ports are needed) Port: {port number}\n(Any other requirements such as storage, containers)Continue the same format of Requirement name: {requirement}\nOnly write about things that are needed for deployment, don’t explain unnecessary parts of the code."
    prompt = codebase

    response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    return response.choices[0].message.content




