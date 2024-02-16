# API key: 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

import openai
import json
import re
import time

openai.api_key = YOUR_OPENAI_KEY
#openai.organization = ''

# request for the filtering of data
def Request_GPT_filter(request):
    '''create the message'''
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "Who won the world series in 2020?"},
    #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #     {"role": "user", "content": "Where was it played?"}
    # ]
    request = [{"role": "user",
                "content": request}]

    '''make the call,'''
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', max_tokens=50, temperature=1, messages = request)
    response = response['choices'][0]['message']['content']
    print(response)
    try:
        pattern = r'<(.*?)>'
        matches = re.findall(pattern, response)[0]
        if matches == 'Considered impossible':
            return 0
        elif matches == 'Considered possible':
            return 2
    except Exception:
        print('jump this example')
        return 3

#request for the generaetion of event data

def Request_GPT_generate(request):
    request = [{"role": "user",
                "content": request}]

    '''make the call,'''
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', max_tokens=2048, temperature=1, messages = request)
    response = response['choices'][0]['message']['content']
    pattern = r'<(.*?)>'
    matches = re.findall(pattern, response)
    recall = matches[0]
    #event_paragraph = matches[-1]
    event_triple = matches[1:]
    # extract what's after the paragraph
    pattern = r'Paragraph Events:(.*)'
    event_paragraph = re.search(pattern, response).group(1)
    return response,recall,event_triple,event_paragraph
        
def concat_json(json_file_path,new_list):
    with open(json_file_path, 'r+') as file:
        data = json.load(file)
        data.extend(new_list)
        file.seek(0)  # 移动文件指针到文件开头
        json.dump(data, file, indent=4)  # 将数据写回文件并格式化
        file.truncate()
        file.close()
    
def filter_counterfact(template_judge,template_generation):
    data_path = '/shared/nas2/jiateng5/Editing/data/GPT/triplets/counterfact.json'
    with open(data_path,'r') as f:
        counterfactual_list = json.load(f)
        # record the rejected samples collected: 
        reject_sample = 0
        #import ipdb;ipdb.set_trace()
        for loop in range(200):
            filtering_results=[]
            generation_list = [] # store all the GPT-4 output
            event_list = [] # store all the extracted events
            for i in range(loop*100,(loop+1)*100):
                argument = counterfactual_list[i]['requested_rewrite']['prompt'].format(counterfactual_list[i]['requested_rewrite']['subject']) + ' ' + counterfactual_list[i]['requested_rewrite']['target_new']['str']
                request = template_judge.format(argument)
                #print(request)
                try:
                    response = Request_GPT_filter(request)
                    time.sleep(3)
                except Exception:
                    continue
                new_dict = {}
                new_dict['ids'] = i
                new_dict['filter'] = response
                filtering_results.append(new_dict)
                if response == 0:
                    reject_sample = reject_sample + 1
                else:
                    request_gen = template_generation.format(argument)
                    try:
                        event_response = Request_GPT_generate(request_gen)
                        time.sleep(3)
                    except Exception:
                        continue
                    temp_dict = {}
                    temp_dict['id'] = i
                    temp_dict['recall'] = event_response[1]
                    temp_dict['triples'] = event_response[2]
                    temp_dict['paragraph'] = event_response[3]
                    generation_list.append(event_response[0])
                    event_list.append(temp_dict)
                    # Parse event 
            
            concat_json('new_results/events.json',event_list)
            concat_json('new_results/generation.json',generation_list)
            concat_json('new_results/filter.json',filtering_results)
                
                
def main():
    with open('JudgeType_new.txt','r') as f1:
        content_judge = f1.read()  
    with open('Transform_edition.txt','r') as f2:
        content_gen = f2.read()   
    filter_counterfact(content_judge,content_gen)
    #print(request)
    
if __name__ == "__main__":
    main()
      
        