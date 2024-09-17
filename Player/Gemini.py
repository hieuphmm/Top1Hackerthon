# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:52:08 2024

@author: jjb24
"""
import random
from Player import Player


# Initialize OpenAI API key

import google.generativeai as genai #import library
import time
def get_response(prompt): #function to generate question
  genai.configure(api_key="AIzaSyBaVQH1_D8zggcgBPwe4yunpLepCeIimsQ") #use gemini api
  generation_config = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 40
  }
  #set the safety infor
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]
  #create a model
  model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
  #a prompt for asking to generate questions
  print(prompt)
  convo = model.start_chat() #start to chat
  ### question: why these infor in the loop??? maybe it is not optimize
  try:
    convo.send_message(prompt) #ask for the questions
  except:
    time.sleep(5)
    convo.send_message(prompt)
  output = convo.last.text #get the question
  return output #return the question

def find_word_in_string(word, string):
    if word in string:
        return True
    else:
        return False

def choose_option(target, hand):
    prompt = "Chọn 1 câu trong các câu sau: 0. " + hand[0]

    for i in range(1, len(hand)):
        prompt += ", " + str(i) + ". " + hand[i]

    prompt += ". Câu nào là câu phù hợp nhất với câu hỏi được cho: '" + target + "'. Hãy chọn và trả về 1 con số là số thứ tự của câu đã chọn và ghi trên 1 dòng."
    res = get_response(prompt)
    print(res)
    
    ans = -1
    # Kiểm tra mang_so và chọn từ phù hợp
    for i in range(0, len(hand)):
        if find_word_in_string(hand[i], res):
            ans = i
            break
    if(ans==-1):
        return 0
    return ans

class TestPlayer(Player):

    PLAYER_NAME = " BOT Gemini "  # Choose a unique name for your player
    
    def __init__(self):
        super().__init__(self.PLAYER_NAME)

    def choose_card(self, target, hand):
        # Select the index of the card from the cards list that is closest to target
        return choose_option(target, hand)
    
    def judge_card(self, target, player_cards):
        # Select the card that is closest to target
        return player_cards[choose_option(target, player_cards)]
        
    def process_results(self, result):
        # Handle results returned from server
        print("Result", result)

if __name__ == '__main__':
    player = TestPlayer()
    player.run()
