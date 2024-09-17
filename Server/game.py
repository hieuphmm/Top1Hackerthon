# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:21:04 2024

@author: jjb24
"""

import random
import queue

class Game:
    HAND_SIZE = 7 # Noun cards per hand
    MAX_SCORE = 3 # Game ends when a player reaches the max score or we run out of cards
    
    def __init__(self):
        self.reset()

    def reset(self):
        # Reading and initializing noun cards
        with open('cards/healthcare/answer.txt', 'r') as f:
            self.noun_cards = [line.strip() for line in f]
        random.shuffle(self.noun_cards)
        
        # Reading and initializing adjective cards
        with open('cards/healthcare/wh-question.txt', 'r') as f:
            self.adjective_cards = [line.strip() for line in f]
        random.shuffle(self.adjective_cards)
        
        self.players = {}
        self.rounds_played = 0
        self.state = "registering"
        self.judge_order = queue.Queue()
        self.messages = {'master': queue.Queue()}
        
    def register_player(self, name):
        if self.state != "registering":
            return False, "Trò chơi đang diễn ra. Không thể đăng ký thêm người chơi mới."
        else:
            if len(self.noun_cards) < self.HAND_SIZE:
                return False, "Số lượng thẻ câu trả lời không đủ để tạo ra một người chơi mới."
                
            player_id = random.randint(1,1_000_000_000)
            while (player_id in self.players):
                player_id = random.randint(1,1_000_000_000)
            self.players[player_id] = {'name': name, 'score': 0, 'cards': [self.noun_cards.pop() for i in range(self.HAND_SIZE)]}
            self.judge_order.put(player_id)
            self.messages[player_id] = queue.Queue()
            self.send_message("Player '" + name + "' đã đăng ký với id " + str(player_id), "master")
            return True, str(player_id)

    def start_round(self):
        if self.state == "done":
            return False, "Trò chơi đã kết thúc"
        if len(self.players) < 3:
            return True, "Bạn cần ít nhất 3 người để chơi game này."
            
        self.judge = self.judge_order.get()
        self.judge_order.put(self.judge)
        
        if len(self.adjective_cards) == 0:
            self.state = "done"
            return False, "Không còn thẻ câu hỏi nào nữa. Trò chơi đã kết thúc."
        self.target_card = self.adjective_cards.pop()
        
        for pid in self.players:
            while len(self.players[pid]['cards']) < self.HAND_SIZE:
                if len(self.noun_cards) == 0:
                    self.state = "done"
                    return False, "Không còn thẻ câu trả lời nào nữa. Trò chơi đã kết thúc."
                self.players[pid]['cards'].append(self.noun_cards.pop())
        
        self.state = "round started"
        #self.send_message("Round started.  Target card: '" + self.target_card + "'", "master")
        self.submitted_cards = {}
        self.chosen_card = None
        
        for pid in self.players:
            if pid != self.judge:
                self.send_message({'type': 'choosing', 'target': self.target_card, 'cards': self.players[pid]['cards']}, pid)
                
        return True, "Vòng đấu đã bắt đầu. Câu hỏi mục tiêu: " + self.target_card
        
    def submit_card(self, pid, card_num):
        if self.state == "done":
            return False, "Trò chơi đã kết thúc."
            
        if self.state != "round started":
            return True, "Các dự đoán chỉ có thể được đăng ký trong giai đoạn đầu của một vòng."

        if pid not in self.players:
            return False, "Mã người chơi không hợp lệ. Id: " + str(pid)

        if card_num < 0 or card_num >= self.HAND_SIZE:
            return True, "Dự đoán của người chơi phải nằm trong khoảng từ 0 đến " + (str(self.HAND_SIZE)-1) + ". Nhận dự đoán: " + card_num
        
        if pid in self.submitted_cards:
            return True, "Người chơi đã đăng ký một dự đoán rồi."


        card = self.players[pid]["cards"].pop(card_num)

        self.submitted_cards[pid] = card
        self.send_message("Người chơi '" + self.players[pid]['name'] + "' chọn '" + card + "' so với các lựa chọn: " + str(self.players[pid]["cards"]), "master")
        return True,""

    def judge_card(self, pid, chosen_card):
        if self.state == "done":
            return False, "Trò chơi đã kết thúc"

        if self.state != "judging":
            return True, "Một thẻ chỉ có thể được chọn trong giai đoạn đánh giá của vòng chơi."

        if pid != self.judge:
            return True, "Chỉ có thể thẩm định viên mới có thể chọn thẻ, ID thẩm định viên (" + str(self.judge) + "), chọn ID người chơi (" + str(pid) + ")"

        self.chosen_card = chosen_card
        
        self.send_message("Thẩm định viên '" + self.players[self.judge]['name'] + "' đã chọn '" + chosen_card + "'", "master")
        return True, "Lựa chọn đã được ghi nhận."


    def start_judging(self):
        if self.state == "done":
            return False, "Trò chơi đã kết thúc"

        if self.state != "round started":
            return True, "Một vòng chỉ có thể được đánh giá nếu nó đang ở trạng thái bắt đầu."

        for pid in self.players:
            if pid not in self.submitted_cards and pid != self.judge:
                random_card = random.randrange(0, self.HAND_SIZE)
                self.submit_card(pid, random_card)
                self.send_message("Không nhận được thẻ từ " + self.players[pid]['name'] + ". Chọn ngẫu nhiên '" + self.submitted_cards[pid] + "' cho người chơi này.", "master")                                

        guesses = []            
        for pid in self.submitted_cards:
            guesses.append(self.submitted_cards[pid])
                
        random.shuffle(guesses)
        self.state = "judging"
        
        message = {'type': 'judging', 'target': self.target_card, 'choices': guesses}
        
        self.send_message(message, self.judge)
        
        return True,""
            
    def end_round(self):
        if self.state == "done":
            return False, "Trò chơi đã kết thúc."

        summary = {'type': 'summary'}
        if self.state != "judging":
            return True, "Một thẻ chỉ có thể được chọn bởi thẩm định viên khi trò chơi đang ở giai đoạn đánh giá."
        
        chosen_pid = None
        for pid in self.submitted_cards:
            if self.chosen_card == self.submitted_cards[pid]:
                chosen_pid = pid
                break
        
        if self.chosen_card is None:
            self.send_message("Thẻ được chọn bởi thẩm định viên '" + str(self.chosen_card) + "' không có trong danh sách các thẻ đã chọn. Đang chọn người chiến thắng ngẫu nhiên.", "master")    
            ndx = random.randrange(0,len(self.submitted_cards))
            for pid in self.submitted_cards:
                if ndx == 0:
                    chosen_pid = pid
                    break
                ndx -= 1
        self.players[chosen_pid]['score'] += 1

        # Send message to Web controller        
        results = "Round winner: '" + self.players[chosen_pid]['name'] + "'.<BR><TABLE class='center'><TR><TH>Team</TH><TH>Score</TH></TR>"
        scoreboard = []
        for pid in self.players:
            scoreboard.append((self.players[pid]['name'], self.players[pid]['score']))
        scoreboard = sorted(scoreboard, key= lambda x: x[1])
        for score in scoreboard:
            results += "<TR><TD>" + str(score[0]) + "</TD><TD>" + str(score[1]) + "</TD></TR>"
        results += "</TABLE>"
        self.send_message(results, "master")
        
        if self.players[chosen_pid]['score'] >= self.MAX_SCORE:
            self.send_message("Game over.", 'master')
            self.state = "done"
            summary['game_over'] = True
        else:
            self.state = "round over"     
            
        # Send message to players
        recap = {}
        recap['round_winner'] = self.players[chosen_pid]['name']
        recap['target_card'] =  self.target_card
        recap['submitted_cards'] =  []
        recap['scores'] = []
        for pid in self.submitted_cards:
            recap['submitted_cards'].append((self.players[pid]['name'], self.submitted_cards[pid]))
            recap['scores'].append((self.players[pid]['name'], self.players[pid]['score']))
        summary['recap'] = recap
        
        for pid in self.players:
            self.send_message(summary, pid)
        
        return True, ""



    def send_message(self, message, key):
        self.messages[key].put(str(message))
        
    def read_messages(self, key):
        if key not in self.messages:
            return False, "unknown player id '" + str(key) + "'"
        results = []
        while not self.messages[key].empty():
            results.append(self.messages[key].get())
        return True,results
    

