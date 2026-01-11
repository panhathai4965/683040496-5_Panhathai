"""
Panhathai Suporn
683040496-5
P3
"""

from datetime import datetime

class VideoGame:
    total_players = 0
    difficulty_levels = ["Easy", "Medium", "Hard"]
    max_level = 100
    server_start_time = datetime.now()
    active_players = []
    leaderboard = {}

    def __init__(self, player_name, character_type):
        if not VideoGame.is_valid_character_name(player_name):
            raise ValueError("Invalid character name")
        
        self.player_name = player_name
        self.character_type =character_type
        self.level = 1
        self.health = 100
        self.exp = 0
        self.coins = 0
        self.inventory = []
        self.is_alive = True

        VideoGame.total_players += 1
        VideoGame.active_players.append(player_name)
        VideoGame.leaderboard[player_name] = 0


    def level_up(self):
        if self.level < VideoGame.max_level:
            self.level += 1
        self.health = 100

        score = self.level*100 + self.coins
        VideoGame.leaderboard[self.player_name] = score

        print(f"[Level UP] {self.player_name}")
        print(f"Level : {self.level}, Health : {self.health}, Score : {self.score}")
    
    def collect_coins(self, amount):
        self.coins = amount
        score =self.level * 100 + self.coins
        VideoGame.leaderboard[self.player_name] = score

        print(f"[Coins] {self.player_name} collected {amount} coins")
        print(f"Coins: {self.coins}, Score: {score}")

    def take_damage(self, damage):
        if not self.is_alive:
            print(f"{self.player_name} is Dead!!!!!")
            return
        
        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            if self.player_name in VideoGame.active_players:
                VideoGame.active_players.remove(self.player_name)
            print(f"[Dead!!] {self.player_name} has died !!!")
        else:
            print(f"[Hurt!!] {self.player_name}: Health = {self.health}")

    def fight_monster(self, monster_name, monster_level):
        if not self.is_alive:
            print(f"{self.player_name} You are DEAD!!")
            return
        
        print(f"\n {self.player_name} attack {monster_name} (LV: {monster_level})")

        damage = VideoGame.calculate_damage(
            attack_power = 10,
            defense = 5,
            level = monster_level
        )
        self.take_damage(damage)

        if not self.is_alive:
            return
        
        gained_exp = 10 * monster_level
        gained_coins = 3 * monster_level
        
        self.exp += gained_exp
        self.collect_coins(gained_coins)

        exp_needed = VideoGame.calculate_exp_needed(self.level)

        if self.exp >= exp_needed:
            self.exp -= exp_needed
            self.level_up()
        print(f"[FIGHT RESULT] EXP +{gained_exp}, Coins +{gained_coins}")

    def get_stats(self):
        return (
            f"Player: {self.player_name}\n"
            f"Type: {self.character_type}\n"
            f"Level: {self.level}\n"
            f"Health: {self.health}\n"
            f"EXP: {self.exp}\n"
            f"Coins: {self.coins}\n"
            f"Alive: {self.is_alive}\n"
            f"Rank: {VideoGame.get_rank_title(self.level)}"
        )
    

    @classmethod
    def create_party(cls, players, player_type):

        party = []

        for name in players:
            party.append(cls(name, player_type))
        return party
    

    @classmethod
    def get_server_stats(cls):
        uptime = datetime.now() - cls.server_start_time
        print("\n===== SERVER STATS =====")
        print(f"Total Players: {cls.total_players}")
        print(f"Active Players: {cls.active_players}")
        print(f"Leaderboard: {cls.leaderboard}")
        print(f"Server Uptime: {uptime}")

    @classmethod
    def get_leaderboard(cls):
        print("\n====LEADERBOARD====")
        sorted_board = sorted(
            cls.leaderboard.items(),
            key=lambda x:x[1],
            reverse= True
        )
        for i,(player, score) in enumerate(sorted_board, 1):
            print(f"{i}. {player} - {score}")
    
    @classmethod
    def reset_server(cls):
        cls.total_players = 0
        cls.leaderboard.clear()
        cls.active_players.clear()
        cls.server_start_time = datetime.now()
        print("\n[SERVER RESET]............")

    @staticmethod
    def calculate_damage(attack_power, defense, level):
        damage = (attack_power * level) - defense
        return max(damage, 0)
    
    @staticmethod
    def calculate_exp_needed(level):
        return 100 * level
    
    @staticmethod
    def is_valid_character_name(name):
        return 3 <= len(name) <= 20 and name.isalnum()
    
    @staticmethod
    def get_rank_title(level):
        if level < 20:
            return "Rise"
        elif level < 40:
            return "Warrior"
        elif level < 60:
            return "Phoenix"
        elif level < 80:
            return "God"
        else:
            return "Legends never die"



            