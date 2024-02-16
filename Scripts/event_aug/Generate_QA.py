# API key: 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

import openai
import json
import re
import time

openai.api_key = YOUR_OPENAI_KEY

def Request_GPT_generate(request):
    request = [{"role": "user",
                "content": request}]

    '''make the call,'''
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', max_tokens=2048, temperature=0.3, messages = request)
    response = response['choices'][0]['message']['content']
    def return_with_patten(pattern,response):
        return re.findall(pattern, response)[0].strip()
    results = []
    results.append(return_with_patten(r'Question 1:(.*?)\n',response))
    results.append(return_with_patten(r'Answer 1:(.*?)\n',response))
    results.append(return_with_patten(r'Question 2:(.*?)\n',response))
    results.append(return_with_patten(r'Answer 2:(.*?)\n',response))
    results.append(return_with_patten(r'Question 3:(.*?)\n',response))
    results.append(return_with_patten(r'Answer 3:(.*?)\n',response))
    results.append(return_with_patten(r'Question 4:(.*?)\n',response))
    results.append(return_with_patten(r'Answer 4:(.*?)\n',response))
    results.append(return_with_patten(r'Question 5:(.*?)\n',response))
    results.append(return_with_patten(r'Answer 5:(.*)',response))

    return results

def concat_json(json_file_path,new_list):
    with open(json_file_path, 'r+') as file:
        data = json.load(file)
        data.extend(new_list)
        file.seek(0)  # 移动文件指针到文件开头
        json.dump(data, file, indent=4)  # 将数据写回文件并格式化
        file.truncate()
        file.close()
               
def Generate_QA(event_list,edit,template):
    #import ipdb;ipdb.set_trace()
    # 18391 piece of data
    for loop in range(50):
        QA_list = []
        #import ipdb;ipdb.set_trace()
        for i in range(loop*10,min((loop+1)*10,500)):
            id = event_list[i]['id']
            recall = event_list[i]['recall']
            details = event_list[i]['paragraph']
            edit_piece = edit[id]["requested_rewrite"]['prompt'].format(edit[id]["requested_rewrite"]['subject'])+edit[id]["requested_rewrite"]['target_new']['str']
            Prompting = template.format(recall,edit_piece,details)
            try:
                results = Request_GPT_generate(Prompting)
                assert len(results) == 10
            except:
                print(f'jump {i}')
                continue
            temp_dict = {}
            temp_dict['id'] = id
            temp_dict['QA1'] = [results[0],results[1]]
            temp_dict['QA2'] = [results[2],results[3]]
            temp_dict['QA3'] = [results[4],results[5]]
            temp_dict['QA4'] = [results[6],results[7]]
            temp_dict['QA5'] = [results[8],results[9]]
            QA_list.append(temp_dict)
            print(f'finish {i}')
        
        print("adding into QA list")    
        concat_json('EvEdit/EvEdit_benchmark/QA.json',QA_list)
            
def main():
    with open('EvEdit/EvEdit_benchmark/events.json','r') as f1:
        event_list = json.load(f1)  
    with open ('EvEdit/EvEdit_benchmark/counterfact.json','r') as f2:
        edit = json.load(f2)
    with open('EvEdit/EvEdit_benchmark/QA_prompt.txt','r') as f3:
        template = f3.read()   
    Generate_QA(event_list,edit,template)
    
if __name__ == "__main__":
    main()