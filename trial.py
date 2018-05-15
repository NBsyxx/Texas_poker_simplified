from judgement import *
served_cards = [['Club', 'J'], ['Heart', '2'], ['Club', '8'], ['Club', 'Q'], ['Spade', '3']]
winners_candidate = [{'player': 'tim', 'money': 7000, 'winner': '', 'handcard': [['Diamond', '4'], ['Heart', 'K']]},
                     {'player': 'tom', 'money': 7000, 'winner': '', 'handcard': [['Club', 'A'], ['Spade', '5']]}]
winners = find_winner(winners_candidate, served_cards)
winner = (winners[0])["winner"]
print(winners)
print(winner)
if "," in winner:
    winner_list = winner.split(",")
else:
    winner_list = [winner]