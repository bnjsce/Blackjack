# libraries
import pygame as pg
import random

# classes
from Player import *

# colours
C_TABLE = "#0a6e1c"

# setup
WIDTH = 1280
HEIGHT = 800
target_fps = 10 # low framerate to control the time it takes to lay a card down on the table

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Blackjack | Ben Collingridge")
clock = pg.time.Clock()
running = True

# cards
deck = ["ace_of_spades", "2_of_spades", "3_of_spades", "4_of_spades", "5_of_spades", "6_of_spades", "7_of_spades", "8_of_spades", "9_of_spades", "10_of_spades", "jack_of_spades", "queen_of_spades", "king_of_spades",
		"ace_of_hearts", "2_of_hearts", "3_of_hearts", "4_of_hearts", "5_of_hearts", "6_of_hearts", "7_of_hearts", "8_of_hearts", "9_of_hearts", "10_of_hearts", "jack_of_hearts", "queen_of_hearts", "king_of_hearts",
		"ace_of_clubs", "2_of_clubs", "3_of_clubs", "4_of_clubs", "5_of_clubs", "6_of_clubs", "7_of_clubs", "8_of_clubs", "9_of_clubs", "10_of_clubs", "jack_of_clubs", "queen_of_clubs", "king_of_clubs",
		"ace_of_diamonds", "2_of_diamonds", "3_of_diamonds", "4_of_diamonds", "5_of_diamonds", "6_of_diamonds", "7_of_diamonds", "8_of_diamonds", "9_of_diamonds", "10_of_diamonds", "jack_of_diamonds", "queen_of_diamonds", "king_of_diamonds"]

# each card image is 209x303
card_dim = pg.Vector2(209, 303)
x_spacing = 100
y_spacing = 154
bottom_padding = 20

# players
player = Player([], 0, False)
dealer = Player([], 0, False)
turn = 1 # player 1 or 2 (player or dealer)
play_deck = deck

score_text_inner = f"{player.total}"

def value(card):
	# to make things exciting, there's a 50/50 chance that ace is 1 or 11
	if card[0] == "a":
		rng = random.randint(1, 10)
		if rng <= 5:
			return 1
		else:
			return 11
	elif card[0] == "j" or card[0] == "q" or card[0] == "k" or card[0] == "1":
		return 10
	else:
		return int(card[0])

# game loop
while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		elif event.type == pg.KEYUP:
			# space = stand, return/enter = hit
			if turn == 1 and not player.stand:
				if event.key == pg.K_SPACE:
					# stand
					turn = 2
					player.stand = True
				elif event.key == pg.K_RETURN:
					# hit
					rand_card = random.choice(play_deck)
					player.cards.append(rand_card)
					play_deck.remove(rand_card)
					player.total += value(rand_card)
					score_text_inner = f"{player.total}"
					if player.total > 21:
						turn = 2
						player.stand = True

	screen.fill(C_TABLE)
	font = pg.font.Font("freesansbold.ttf", 24)

	if turn == 2 and not dealer.stand:
		# dealer stands on 18+
		if dealer.total < 18:
			rand_card = random.choice(play_deck)
			dealer.cards.append(rand_card)
			play_deck.remove(rand_card)
			dealer.total += value(rand_card)
		elif dealer.total >= 18:
			turn = 1
			dealer.stand = True
			if dealer.total > 21:
				turn = 1
				dealer.stand = True

	# if both players stood, end round
	if player.stand and dealer.stand:
		# five card trick
		if len(player.cards) >= 5 or len(dealer.cards) >= 5:
			if len(player.cards) >= 5 and player.total <= 21 and len(dealer.cards) < 5:
				score_text_inner = f"You win (five card trick)! You: {player.total} | Dealer: {dealer.total}"
			elif len(dealer.cards) >= 5 and dealer.total <= 21 and len(player.cards) < 5:
				score_text_inner = f"Dealer wins (five card trick)! You: {player.total} | Dealer: {dealer.total}"
			elif len(player.cards) >= 5 and player.total <= 21 and len(dealer.cards) >= 5 and dealer.total <= 21:
				score_text_inner = f"Both got a five card trick! You: {player.total} | Dealer: {dealer.total}"
			elif player.total > 21:
				score_text_inner = f"Dealer wins! You: {player.total} | Dealer: {dealer.total}"
			elif dealer.total > 21:
				score_text_inner = f"Dealer wins (five card trick)! You: {player.total} | Dealer: {dealer.total}"

		else: 
			if player.total > dealer.total and player.total <= 21:
				score_text_inner = f"You win! You: {player.total} | Dealer: {dealer.total}"
			elif dealer.total > player.total and dealer.total <= 21:
				score_text_inner = f"Dealer wins! You: {player.total} | Dealer: {dealer.total}"
			elif player.total > 21 and dealer.total <= 21:
				score_text_inner = f"You went bust! You: {player.total} | Dealer: {dealer.total}"
			elif dealer.total > 21 and player.total <= 21:
				score_text_inner = f"Dealer went bust! You: {player.total} | Dealer: {dealer.total}"
			elif player.total == dealer.total and player.total > 21:
				score_text_inner = f"Both went bust! You: {player.total} | Dealer: {dealer.total}"
			else:
				score_text_inner = f"Draw! You: {player.total} | Dealer: {dealer.total}"

	score_text = font.render(f"{score_text_inner}", True, "white")
	text_rect = score_text.get_rect()
	text_rect.center = (screen.get_width() // 2, card_dim.y + y_spacing / 2 + 10)

	# show dealer cards
	for i in range(len(dealer.cards)):
		screen.blit(pg.image.load(f"./img/{dealer.cards[i]}.svg"), pg.Vector2(i * card_dim.x + x_spacing, bottom_padding))

	# show player cards
	for i in range(len(player.cards)):
		screen.blit(pg.image.load(f"./img/{player.cards[i]}.svg"), pg.Vector2(i * card_dim.x + x_spacing, card_dim.y + y_spacing - bottom_padding))

	screen.blit(score_text, text_rect)

	pg.display.update()
	pg.display.flip()
	clock.tick(target_fps)

pg.quit()