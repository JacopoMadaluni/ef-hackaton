import openai

openai.api_key = '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'


def run(phase1):

    system_prompt = "You are a Caltech graduated senior cloud infrastructure engineer who specialises in writing infrastructure code for deploying services on Microsoft Azure. You are looking to deploy in the UK. You’re the best engineer Microsoft has ever seen. You receive detailed specifications from your manager and are asked to write the infrastructure code. You want to use Pulumi and never forget about creating the app service and consider storage accounts and container(s).  Pay attention to runtimes, make sure you use the lattest and only use the one specified by your manager. All access should be public."
    prompt = phase1

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


