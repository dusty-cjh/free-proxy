import json
import sys
import os
import time
import openai
import logging

# 这里记得修改成自己的 API KEY
openai.api_key = '806601c981dec75e3e69b9984cb155b9'
openai.api_base = 'https://external.hdcjh.xyz/gateway/transmit-openai/v1'


class Conversation:
    def __init__(self, base_prompt=None, max_tokens=256, max_conversation_length=8192, temperature=0.5):
        base_prompt = base_prompt or open(os.path.join(os.path.dirname(__file__), 'prompt.txt'), 'r').read()
        self.messages = [
            {"role": "system", "content": base_prompt},
        ]
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.conversation_length = len(base_prompt)
        self.max_conversation_length = max_conversation_length
        self.last_response_cost_time = 0

    def get_response(self, prompt: str, raise_exception=False, timeout=60, retry=1):
        try:
            start_time = time.time()
            self.messages.append({"role": "user", "content": prompt.strip()})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                n=1,
                timeout=timeout,
            )
            response = completion.choices[0]
            assert response['finish_reason'] in ('stop', None, 'length'), \
                'finsi_reason is not stop, got %s' % response['finish_reason']
            msg = response['message']
            self.messages.append(msg)
            self.conversation_length += len(msg['content'])
            # shrink the conversation length to fit the max_conversation_length
            while self.conversation_length > self.max_conversation_length and len(self.messages) >= 2:
                msg = self.messages.pop(1)
                self.conversation_length -= len(msg['content'])
            self.last_response_cost_time = time.time() - start_time
            return msg['content'].strip()
        except Exception as e:
            if raise_exception:
                raise
            # print error log
            logging.getLogger('error').error('OpenAI ChatCompletion error: %s' % e)
            if retry > 0:
                return self.get_response(prompt, raise_exception, timeout, retry=retry - 1)

    def print_chat_history(self):
        for msg in self.messages:
            print('{}:\n{}\n\n'.format(msg['role'], msg['content'].strip()))

    def dump_chat_history(self, serialize=False):
        data = {
            'messages': self.messages,
            'conversation_length': self.conversation_length,
            'last_response_cost_time': self.last_response_cost_time,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'max_conversation_length': self.max_conversation_length,
        }
        return data if not serialize else json.dumps(data)

    def load_chat_history(self, chat_history, serialized=False):
        data = chat_history if not serialized else json.loads(chat_history)
        self.messages = data['messages']
        self.conversation_length = data['conversation_length']
        self.last_response_cost_time = data['last_response_cost_time']
        self.max_tokens = data['max_tokens']
        self.temperature = data['temperature']
        self.max_conversation_length = data['max_conversation_length']


if __name__ == '__main__':
    # get api key from cmd line
    if len(sys.argv) > 1:
        openai.api_key = sys.argv[1]
    if openai.api_key == None:
        # notice user to input API KEY in terminal
        key = input('Please input your OpenAI API KEY(Default use testing key): ').strip()
        if key:
            key = '806601c981dec75e3e69b9984cb155b9'

    conversation = Conversation()
    print('成功连接！\n给 ChatGPT 说点什么吧！\n(输入 exit 或 quit 退出)\n')
    while True:
        prompt = input('\033[1;36muser:\033[0m\n').strip()
        if prompt in ('exit', 'quit'):
            break
        if not prompt:
            continue
        print('正在生成回复...')
        response = conversation.get_response(prompt)
        print('\033[1;35mbot:\033[0m\n{}\n'.format(response))
    print('Bye, 感谢使用 ChatGPT！')
    print('\033[1;35m[⭐️⭐️⭐️]star me: https://github.com/dusty-cjh/free-proxy/\033[0m\n')
