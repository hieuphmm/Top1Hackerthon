# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:52:08 2024

@author: jjb24
"""
import random
from Player import Player

###
# This player makes all choices completely at random
###

def choose_option(target, hand):
    for i in range(0,len(hand)):
        print(f"{i}. {hand[i]}")
    ans = int(input(f"Nhập số thứ tự bạn chọn phù hợp với câu hỏi {target} "))
    return ans

class OutPlayer(Player):

    PLAYER_NAME = "Out Player" # Choose a unique name for your player
    
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
    player = OutPlayer()
    player.run()