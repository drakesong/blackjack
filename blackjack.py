import random
import os

suits = ('Clubs', 'Diamonds', 'Hearts', 'Diamonds')
ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
value = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
        'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

class Deck:
    def __init__(self):
        self.deck = []
        for a in suits:
            for b in ranks:
                self.deck.append(Card(a, " %s" %(b)))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

    def new_deck(self):
        self.deck = []
        for a in suits:
            for b in ranks:
                self.deck.append(Card(a, " %s" %(b)))

class Player:
    def __init__(self, money, hand, hand_value):
        self.money = money
        self.hand = hand
        self.hand_value = hand_value

    def lose_money(self, num):
        self.money -= num

    def win_money(self, num):
        self.money += num

def clear():
    os.system('cls')

def place_bet(player):
    global bet
    correct_bet = False
    while (correct_bet == False):
        try:
            bet_temp = int(raw_input("Enter your bet: "))
        except ValueError:
            print "Error! Please enter an integer!"
        else:
            if bet_temp > 0 and bet_temp <= player.money:
                bet = bet_temp
                correct_bet = True
            else:
                print "Error. Please enter a valid bet!"

def deal_hands(p1, p2):
    global status, a, b, c, d, hand_value, ace_in_play, player_ace_count, dealer_ace_count

    hand_value = 0
    ace_in_play = False

    player_ace_count = 0
    dealer_ace_count = 0

    a = deck.deal()
    b = deck.deal()
    p1.hand.append(a)
    p2.hand.append(b)
    print "Your first card is: %s" %(a)

    c = deck.deal()
    d = deck.deal()
    p1.hand.append(c)
    p2.hand.append(d)
    print "Your second card is: %s" %(c)

    if (a.get_rank().replace(" ", "") != "A"):
        p1.hand_value += value[a.get_rank().replace(" ", "")]
    else:
        ace_in_play = True

    if (c.get_rank().replace(" ", "") != "A" and ace_in_play == False):
        p1.hand_value += value[c.get_rank().replace(" ", "")]
        print "\nYour hand has a value of: %s" %(p1.hand_value)
    elif (c.get_rank().replace(" ", "") == "A" and ace_in_play == False):
        if (a.get_rank().replace(" ", "") == '10' or
        a.get_rank().replace(" ", "") == 'J' or
        a.get_rank().replace(" ", "") == 'Q' or
        a.get_rank().replace(" ", "") == 'K'):
            p1.hand_value += 11
            print "\nBlack Jack!"
        else:
            p1.hand_value += 11
            print "\nYour hand has a value of: soft %s" %(p1.hand_value)
    elif (ace_in_play == True and (c.get_rank().replace(" ", "") == '10' or
    c.get_rank().replace(" ", "") == 'J' or
    c.get_rank().replace(" ", "") == 'Q' or
    c.get_rank().replace(" ", "") == 'K')):
        p1.hand_value = 21
        print "\nBlack Jack!"
    elif (ace_in_play == True):
        p1.hand_value += 11
        p1.hand_value += value[c.get_rank().replace(" ", "")]
        print "\nYour hand has a value of: soft %s" %(p1.hand_value)
    else:
        p1.hand_value = 12
        print "\nYour hand has a value of: soft %s" %(p1.hand_value)

    print "\nDealer turns over her first card and reveals: %s \n" %(b)

    if (a.get_rank().replace(" ","") == "A"):
        player_ace_count += 1
    if (c.get_rank().replace(" ", "") == "A"):
        player_ace_count += 1
    if (b.get_rank().replace(" ","") == "A"):
        dealer_ace_count += 1
    if (d.get_rank().replace(" ", "") == "A"):
        dealer_ace_count += 1

def dealer_turn(player):
    global f, dealer_ace_count

    print "\nDealer's second card is: %s" %(d)

    if (b.get_rank().replace(" ", "") == "A"):
        if (d.get_rank().replace(" ","") == "10" or
        d.get_rank().replace(" ","") == "J" or
        d.get_rank().replace(" ","") == "Q" or
        d.get_rank().replace(" ","") == "K"):
            print "\nBlack Jack!"
            player.hand_value = 21
        elif (d.get_rank().replace(" ", "") == "A"):
            player.hand_value = 12
            print "Dealer's hand has a value of: soft %s" %(player.hand_value)
        else:
            player.hand_value += value[d.get_rank().replace(" ", "")]
            player.hand_value += 11
            print "Dealer's hand has a value of: soft %s" %(player.hand_value)
    elif (d.get_rank().replace(" ", "") == "A"):
        if (b.get_rank().replace(" ","") == "10" or
        b.get_rank().replace(" ","") == "J" or
        b.get_rank().replace(" ","") == "Q" or
        b.get_rank().replace(" ","") == "K"):
            print "\nBlack Jack!"
            player.hand_value = 21
        else:
            player.hand_value = value[b.get_rank().replace(" ", "")]
            player.hand_value += 11
            print "Dealer's hand has a value of: soft %s" %(player.hand_value)
    else:
        player.hand_value = value[b.get_rank().replace(" ", "")]
        player.hand_value += value[d.get_rank().replace(" ", "")]
        print "Dealer's hand has a value of: %s" %(player.hand_value)

    while (player.hand_value < 17):
        f = deck.deal()
        player.hand.append(f)

        if (f.get_rank().replace(" ", "") != "A"):
            player.hand_value += value[f.get_rank().replace(" ", "")]
        else:
            player.hand_value += 11

        print "\nDealer's next card is: %s" %(f)

        if (f.get_rank().replace(" ", "") == "A"):
            dealer_ace_count += 1

        if (player.hand_value > 21 and dealer_ace_count > 0):
            player.hand_value -= 10
            dealer_ace_count -= 1

        print "Dealer's hand has a value of: %s" %(player.hand_value)

        if (player.hand_value > 21):
            print "\nDealer Bust! Round over! \n"

def determine_winner(p1, p2):
    if (p2.hand_value > 21):
        print "\nCongrats! You won!\n"
        p1.win_money(bet)
        p2.lose_money(bet)
    elif (p1.hand_value > p2.hand_value):
        print "\nCongrats! You won!\n"
        p1.win_money(bet)
        p2.lose_money(bet)
    elif (p1.hand_value == p2.hand_value):
        print "\nPush!\n"
    else:
        print "\nSorry. You lost!\n"
        p1.lose_money(bet)
        p2.win_money(bet)
    end_round(p1, p2)

def hit(p1, p2):
    global e, status, player_ace_count

    e = deck.deal()
    p1.hand.append(e)

    if (e.get_rank().replace(" ", "") == "A"):
        player_ace_count += 1

    if (e.get_rank().replace(" ", "") != "A"):
        p1.hand_value += value[e.get_rank().replace(" ", "")]
    else:
        p1.hand_value += 11

    print "\nYour next card is: %s" %(e)

    if (p1.hand_value > 21 and player_ace_count > 0):
        p1.hand_value -= 10
        player_ace_count -= 1

    print "Your hand has a value of: %s\n" %(p1.hand_value)

    if (p1.hand_value > 21):
        print "Bust! Round over! \n"
        p1.hand_value = 0
        status = "s"
        p1.money -= bet
        p2.money += bet

def play_round(p1, p2):
    global status
    status = ""

    print "\n\n\n"
    print "Dealer has $%s" %(p2.money)
    print "You have $%s\n" %(p1.money)
    place_bet(p1)
    print "The pot is now: $%s \n" %(2 * bet)
    deal_hands(p1, p2)
    while status != 's':
        status = raw_input("Hit (enter h) or stand (enter s)?\n")
        if status == 'h':
            hit(p1, p2)
        elif status == 's':
            dealer_turn(p2)
            determine_winner(p1, p2)
        else:
            print "\nError! Please enter 'h' or 's'!\n"
    if (p1.money == 0):
        print "You ran out of money! Thanks for playing!"
    elif (p2.money == 0):
        print "Dealer ran out of money! Thanks for playing!"

def end_round(p1, p2):
    p1.hand = []
    p2.hand = []
    p1.hand_value = 0
    p2.hand_value = 0


clear()
print "\nWelcome to BlackJack! \n"
deck = Deck()
print "Dealer will bet the same amount as you."
print  "You will win the game when Dealer runs out of money."
print "Good luck!\n"
deck.shuffle()
player1 = Player(1000, [], 0)
dealer = Player(1000, [], 0)
while (player1.money > 0 and dealer.money > 0):
    deck.new_deck()
    deck.shuffle()
    play_round(player1, dealer)
