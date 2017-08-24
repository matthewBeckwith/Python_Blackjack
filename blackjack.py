# !/usr/bin/python3

# TODO: When there are more than one Aces, 1 - 11 rule doesnt seem to work
# TODO: Split, Double Down, insurance not built
# TODO: GUI


import random


class Player:
    name = "Player"

    hand_count = 0
    hand_wins = 0
    hand_losses = 0
    hand_draws = 0
    credit = 100
    current_bet = 0
    current_cards = []
    current_hand = []

    def total_earnings(self):
        return self.credits - 100

    def add_credits(self, amount):
        self.credits += amount

    def remove_credits(self, amount):
        self.credits -= amount


class Dealer:
    name = "Dealer"

    current_hand = []
    current_cards = []

        
class Game:
    name = "Blackjack"
    deck = {
        'suits': [
            ['hearts', '\u2665'],
            ['clubs', '\u2663'],
            ['diamonds', '\u2666'],
            ['spades', '\u2660'],
        ],
        'cards': [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
        ]
    }
    min_bet = 5
    max_bet = 50
    custom_bet = 0

    @staticmethod
    def show_deck():
        for suit in Game.deck['suits']:
            cards = []

            for card in Game.deck['cards']:
                if card > 10:
                    if card == 11:
                        cards.append('J' + suit[1])
                    elif card == 12:
                        cards.append('Q' + suit[1])
                    elif card == 13:
                        cards.append('K' + suit[1])
                    elif card == 14:
                        cards.append('A' + suit[1])
                else:
                    cards.append(str(card) + suit[1])

            print(cards)

    @staticmethod
    def get_hand_worth(hand):
        value = 0
        
        for card in hand:
            if card < 10:
                value += card
            elif card == 14:
                if value + 11 > 21:
                    value += 1
                else:
                    value += 11
            else:
                value += 10

        return value

    @staticmethod
    def check_dealer_action():
        check = Game.get_hand_worth(Dealer.current_hand)

        if len(Dealer.current_hand) == 2 and Game.get_hand_worth(Dealer.current_hand) == 21:
            Game.show_hand(Dealer.current_cards)
            print("Dealer Dealt himself 21!")

            if Game.get_hand_worth(Player.current_hand) == 21:
                print("You and the Dealer Push; Receive your bet back")
                Player.credit += Player.current_bet
                Player.hand_draws += 1
            else:
                print("you Lose!")
                Player.hand_losses += 1
                
            Player.hand_count += 1
            start_game()
        else:
            if check < 17:
                Game.give_card(Dealer)
                Game.check_dealer_action()
                start_game()
            else:
                if Game.get_hand_worth(Dealer.current_hand) > 21:
                    print(Game.show_hand(Dealer.current_cards))
                    print("Dealer Busted with a value of {}".format(str(Game.get_hand_worth(Dealer.current_hand))))
                    Player.hand_wins += 1
                    Player.hand_count += 1
                    Player.credit += Player.current_bet * 2
                else:
                    print("Now we compare hands!")            
                    print("Dealer has {} worth {}".format(Game.show_hand(Dealer.current_cards),
                                                        str(Game.get_hand_worth(Dealer.current_hand))))
                    print("You have {} worth {}".format(Game.show_hand(Player.current_cards),
                                                        str(Game.get_hand_worth(Player.current_hand))))

                    if Game.get_hand_worth(Dealer.current_hand) == Game.get_hand_worth(Player.current_hand):
                        print("Hand is a Push, Recieve your bet back")
                        Player.credit += Player.current_bet
                        Player.hand_draws += 1
                    elif Game.get_hand_worth(Dealer.current_hand) > Game.get_hand_worth(Player.current_hand):
                        print("You Lose")
                        Player.hand_losses += 1
                    elif Game.get_hand_worth(Dealer.current_hand) < Game.get_hand_worth(Player.current_hand):
                        print("You Win!")
                        Player.credit += Player.current_bet * 2
                        Player.hand_wins += 1

                    Player.hand_count += 1
                    start_game()

    def show_hand(cards):
        hand = ""
        
        for card in cards:
            hand += card + " "

        return hand

    @staticmethod
    def deal():
        if len(Player.current_hand) < 2:
            Game.give_card(Player)
            Game.give_card(Dealer)
            Game.deal()
        else:
            if len(Player.current_hand) == 2 and Game.get_hand_worth(Player.current_hand) == 21:
                print("Player Cards: {}".format(Game.show_hand(Player.current_cards)))
                print("Dealer is showing: " + str(Dealer.current_cards[1]))
                print("You got Blackjack!")
                Player.hand_wins += 1
                Player.credit += Player.current_bet * 2.5
                Player.hand_count += 1
                start_game()
            elif Game.get_hand_worth(Player.current_hand) > 21:
                print("Player Cards: {}".format(Game.show_hand(Player.current_cards)))
                print("Dealer is showing: " + str(Dealer.current_cards[1]))
                print("You Busted!")
                Player.hand_losses +=1
                Player.hand_count += 1
                start_game()
            else:
                print("Player Cards: {}".format(Game.show_hand(Player.current_cards)))
                print("Dealer is showing: " + str(Dealer.current_cards[1]))

                choice = int(input("1 = HIT     2 = STAND\n\n"))

                if choice == 1:
                    Game.give_card(Player)
                    Game.deal()
                elif choice == 2:
                    Game.check_dealer_action()
                else:
                    print("Not a valid choice... Try that again")
                    Game.deal()
            
    @staticmethod
    def give_card(who):
        card = Game.deck['cards'][random.randrange(0, len(Game.deck['cards']))]
            
        who.current_hand.append(card)

        if card > 10:
            if card == 11:
                who.current_cards.append('J ' + Game.deck['suits'][random.randrange(0,
                                                                                    len(Game.deck['suits']))][1])
            elif card == 12:
                who.current_cards.append('Q ' + Game.deck['suits'][random.randrange(0,
                                                                                    len(Game.deck['suits']))][1])
            elif card == 13:
                who.current_cards.append('K ' + Game.deck['suits'][random.randrange(0,
                                                                                    len(Game.deck['suits']))][1])
            elif card == 14:
                who.current_cards.append('A ' + Game.deck['suits'][random.randrange(0,
                                                                                    len(Game.deck['suits']))][1])
        else:
            who.current_cards.append(str(card) + ' ' + Game.deck['suits'][random.randrange(0,
                                                                                           len(Game.deck['suits']))][1])


def start_game():
    Player.current_hand = []
    Player.current_cards = []
    Dealer.current_hand = []
    Dealer.current_cards = []
    
    print("""
       Welcome to Blackjack!

       Current Balance  = ${}

       Total Earnings   = ${}
       
       Games Played = {}
       Games Won    = {}
       Games Lost   = {}
       Games Pushed = {}

    What would you like to do?

    1. Min Bet
    2. Max Bet
    3. Leave Table
""".format(Player.credit,
           Player.credit - 100,
           Player.hand_count,
           Player.hand_wins,
           Player.hand_losses,
           Player.hand_draws))
    choice = int(input())

    if choice == 3:
        quit()
    elif choice == 2:
        if Player.credit >= Game.max_bet:
            Player.credit -= Game.max_bet
            Player.current_bet = Game.max_bet
            Game.deal()
        else:
            print("Not enough money...")
            start_game()
    elif choice == 1:
        if Player.credit >= Game.min_bet:
            Player.credit -= Game.min_bet
            Player.current_bet = Game.min_bet
            Game.deal()
        else:
            print("Not enough money...")
            start_game()
    else:
        print("Please Pick a Valid Choice")
        start_game()

        
start_game()