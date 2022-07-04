import time
import random

from AI import ALL_AI
from shadow import ShadowGame

# OPTIONS #######
starting_dice = 5
exp_1 = True
exp_1_games = 10000
exp_1_wild_chance = 0.5
exp_2 = True
exp_2_games = 1000
#################


# Run games with all AIs against each other
if exp_1:
    print(f"Starting: Experiment 1; Estimated time: {exp_1_games * 0.002:.2f}s")
    start = time.perf_counter()
    results = {ai.get_name(): 0 for ai in ALL_AI}
    info = []

    # Thread function to run a single game
    def run_game_1():
        # Shuffle and recreate all players each time
        random.shuffle(ALL_AI)
        p = {j: ai(None, starting_dice, j, False) for j, ai in enumerate(ALL_AI)}
        game = ShadowGame(players=p, wild_mode=random.random() < exp_1_wild_chance)
        winner = game.start_game()
        results[winner.get_name()] += 1
        info.append(game.game_info)

    # Run games
    for i in range(1, exp_1_games + 1):
        run_game_1()
    total_time = time.perf_counter() - start
    print(f"Winner count = {results}")
    print(f"Experiment 1 took {total_time:.2f}s; Time per game: {total_time/exp_1_games:.4f}s")

# Consider all possible matchups with 1 of each AI (N! for N AIs)
if exp_2:
    pass
