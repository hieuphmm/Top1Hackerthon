# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:52:08 2024

@author: jjb24
"""
import random
from Player import Player

###
# This player makes all choices base on LLM
###

import requests
import json

def get_response(prompt):
    url = 'https://ws.gvlab.org/fablab/ura/llama/api/generate_stream'
    data = {"inputs": "<start_of_turn>user\n " + prompt + " <end_of_turn>\n<start_of_turn>model\n"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)

    lines = response.text.strip().split('\n')
    output = ""
    for line in lines:
        if line.strip() == '':
            continue
        data = json.loads(line.replace('data:', ''))
        token_text = str(data['token']['text']).encode('latin1').decode('utf-8')
        if token_text != "<eos>":
            output += token_text

    return output

def choose_option(target, hand):
    prompt = "Chọn 1 câu trong các câu sau: 0. "
    prompt+= hand[0]

    for i in range(1,len(hand)):
        prompt+= ", "+ str(i) + ". " + hand[i]

    prompt+= ". Câu nào là phù hợp nhất với câu hỏi được cho: '"+ target + "'. Hãy chọn và trả về 1 con số là số thứ tự của câu đã chọn và ghi trên 1 dòng."
    res = get_response(prompt)
    print(res)
    bang_anh_xa = str.maketrans("", "", ".,:!*#()")

    # Áp dụng bảng ánh xạ vào chuỗi để loại bỏ các ký tự đặc biệt
    chuoi_sau_khi_xoa = res.translate(bang_anh_xa)

    # Tách chuỗi thành các từ
    tach_tu = chuoi_sau_khi_xoa.split()

    # Lọc và lấy các số từ danh sách các từ
    so = [tu for tu in tach_tu if tu.isdigit()]

    # Chuyển đổi mảng chứa các chuỗi số thành mảng chứa các số nguyên
    mang_so = list(map(int, so))

    ans = 0
    # Kiểm tra mang_so và chọn từ phù hợp
    for i in range(0,len(mang_so)):
        if(mang_so[i]>=0 and mang_so[i]<len(hand)):
            ans = mang_so[i]
            break

    return ans

class TestPlayer(Player):

    PLAYER_NAME = "Người chơi hệ tét" # Choose a unique name for your player
    
    def __init__(self):
        super().__init__(self.PLAYER_NAME)


    def choose_card(self, target, hand):
        ### Select the index of the card from the cards list that is closest to target
        return choose_option(target, hand)
    
    
    def judge_card(self, target, player_cards):
        ### Select the card that is closest to target
        return player_cards[choose_option(target, player_cards)]
        
    
    def process_results(self, result):
        ### Handle results returned from server
        print("Result", result)

if __name__ == '__main__':
    player = TestPlayer()
    player.run()
