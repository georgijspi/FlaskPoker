import socket
import threading
from collections import Counter

class PokerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.deck = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.small_blind_index = 0
        self.big_blind_index = 1

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Server listening on {self.host}:{self.port}")

        while len(self.clients) < 2:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Player {len(self.clients)} connected from {addr}")

            # Send welcome message and player number to the new client
            client_socket.send(f"Welcome, you are Player {len(self.clients)}".encode())

            if len(self.clients) == 2:
                self.start_game()

    def start_game(self):
        self.init_deck()
        self.shuffle_deck()
        self.deal_hands()

        # Set blinds and start the first round
        self.current_player_index = 0
        self.place_blinds()
        self.start_betting_round()

        # Deal the turn (4th community card)
        self.deal_community_cards(1)
        self.start_betting_round()

        # Deal the river (5th community card)
        self.deal_community_cards(1)
        self.start_betting_round()

    def init_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        self.deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

    def shuffle_deck(self):
        import random
        random.shuffle(self.deck)

    def deal_hands(self):
        for _ in range(2):
            for client_socket in self.clients:
                card = self.deck.pop()
                client_socket.send(f"Your card: {card['rank']} of {card['suit']}\n".encode())

    def send_hand(self, player_index):
        for i, client_socket in enumerate(self.clients):
            if i == player_index:
                continue
            card1 = self.deck.pop()
            card2 = self.deck.pop()
            client_socket.send(f"Player {player_index + 1}'s hand: {card1['rank']} of {card1['suit']}, "
                               f"{card2['rank']} of {card2['suit']}\n".encode())

    def place_blinds(self):
        small_blind_socket = self.clients[self.small_blind_index]
        big_blind_socket = self.clients[self.big_blind_index]

        small_blind_amount = 1
        big_blind_amount = 2

        small_blind_socket.send(f"You are the small blind. Bet: {small_blind_amount}\n".encode())
        big_blind_socket.send(f"You are the big blind. Bet: {big_blind_amount}\n".encode())

        self.pot += small_blind_amount + big_blind_amount

    def start_betting_round(self):
        for i, client_socket in enumerate(self.clients):
            self.current_player_index = i
            self.current_bet = 0

            client_socket.send("\nBetting Round\n".encode())
            self.send_community_cards()
            self.send_pot()
            self.send_current_bet()

            bet = self.receive_bet(client_socket)
            self.handle_bet(client_socket, bet)

            if self.check_for_winner():
                self.end_game()
                return

        # After the initial round, allow each player to either bet, check, or fold
        for i, client_socket in enumerate(self.clients):
            if i == self.small_blind_index or i == self.big_blind_index:
                continue

            self.current_player_index = i
            self.send_community_cards()
            self.send_pot()
            self.send_current_bet()

            bet = self.receive_bet(client_socket)
            self.handle_bet(client_socket, bet)

            if self.check_for_winner():
                self.end_game()
                return

    def send_community_cards(self):
        for _ in range(3):  # Flop: Deal 3 cards
            card = self.deck.pop()
            self.community_cards.append(card)

        # Inform all players about the new community cards
        community_cards_info = ", ".join(f"{card['rank']} of {card['suit']}" for card in self.community_cards)
        for client_socket in self.clients:
            client_socket.send(f"\nCommunity Cards: {community_cards_info}\n".encode())

    def deal_community_cards(self, num_cards):
        for _ in range(num_cards):
            card = self.deck.pop()
            self.community_cards.append(card)

        # Inform all players about the new community cards
        community_cards_info = ", ".join(f"{card['rank']} of {card['suit']}" for card in self.community_cards)
        for client_socket in self.clients:
            client_socket.send(f"\nCommunity Cards: {community_cards_info}\n".encode())

    def send_pot(self):
        for client_socket in self.clients:
            client_socket.send(f"\nCurrent Pot: {self.pot}\n".encode())

    def send_current_bet(self):
        current_player_socket = self.clients[self.current_player_index]
        current_player_socket.send(f"\nCurrent Bet: {self.current_bet}\n".encode())

    def receive_bet(self, client_socket):
        bet = 0
        while True:
            try:
                client_socket.send("\nYour move (bet 0 to check/fold): ".encode())
                bet_input = client_socket.recv(1024).decode()

                if not bet_input.isdigit():
                    client_socket.send("Invalid input. Please enter a valid bet.\n".encode())
                    continue

                bet = int(bet_input)

                if bet < 0 or bet > self.current_bet + self.pot:
                    client_socket.send("Invalid bet. Please enter a valid bet.\n".encode())
                    continue

                break
            except ValueError:
                client_socket.send("Invalid input. Please enter a valid bet.\n".encode())

        return bet


    def handle_bet(self, client_socket, bet):
        if bet == 0:
            client_socket.send("You checked/folded.\n".encode())
        else:
            self.pot += bet
            self.current_bet = bet
            client_socket.send(f"You bet {bet}\n".encode())

    def check_for_winner(self):
        # Check if only one player is left with chips
        active_players = sum(1 for client_socket in self.clients if client_socket is not None)
        return active_players == 1

    def end_game(self):
        # Determine the winner based on hand strengths
        winner_index = self.determine_winner()
        # Inform all players about the winner
        for i, client_socket in enumerate(self.clients):
            if i == winner_index:
                client_socket.send("Congratulations! You are the winner!\n".encode())
            else:
                client_socket.send(f"Player {winner_index + 1} is the winner.\n".encode())
        # Reset the game state for a new round
        self.reset_game()

    def determine_winner(self):
        best_hands = []

        for i, client_socket in enumerate(self.clients):
            if client_socket is not None:
                player_hand = self.community_cards + self.get_player_hand(i)
                best_hand = self.evaluate_hand(player_hand)
                best_hands.append((i, best_hand))

        # Find the player with the best hand
        winner_index, _ = max(best_hands, key=lambda x: x[1])
        return winner_index

    def get_player_hand(self, player_index):
        return [self.deck.pop() for _ in range(2)]

    def reset_game(self):
        # Reset game-related variables for a new round
        self.deck = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.small_blind_index = (self.small_blind_index + 1) % len(self.clients)
        self.big_blind_index = (self.big_blind_index + 1) % len(self.clients)

if __name__ == "__main__":
    server = PokerServer('localhost', 5555)
    server.start()
