def createStats():
    import numpy as np
    from collections import defaultdict, deque

    prev_stats = {}

    prev_stats["elo_players"] = defaultdict(int)
    prev_stats["elo_surface_players"] = defaultdict(lambda: defaultdict(int))
    prev_stats["elo_grad_players"] = defaultdict(lambda: deque(maxlen=1000))
    prev_stats["last_k_matches"] = defaultdict(lambda: deque(maxlen=1000))
    prev_stats["last_k_matches_stats"] = defaultdict(lambda: defaultdict(lambda: deque(maxlen=1000)))
    prev_stats["matches_played"] = defaultdict(int)
    prev_stats["h2h"] = defaultdict(int)
    prev_stats["h2h_surface"] = defaultdict(lambda: defaultdict(int))

    return prev_stats

"""
INPUTS:
Match should be a row in the tennis dataset we created in 0.CleanData.ipynb
Prev_stats should be all the stats data we have until the most recent game. We want to update these stats and return a dictionary again

OUTPUT:
Outputs a dictionary with the updated stats
"""
def updateStats(match, prev_stats):
    from utils.common import mean, getWinnerLoserIDS
    import numpy as np

    # Get Winner and Loser ID'S
    p1_id, p2_id, surface, result = match.p1_id, match.p2_id, match.surface, match.RESULT
    w_id, l_id = getWinnerLoserIDS(p1_id, p2_id, result)

    ######################## UPDATE ########################
    ############## ELO ##############
    # Get current ELO ratings (BEFORE this match)
    elo_w = prev_stats["elo_players"].get(w_id, 1500)
    elo_l = prev_stats["elo_players"].get(l_id, 1500)
    elo_surface_w = prev_stats["elo_surface_players"][surface].get(w_id, 1500)
    elo_surface_l = prev_stats["elo_surface_players"][surface].get(l_id, 1500)

    # Calculate expected probabilities
    k = 24
    exp_w = 1/(1+(10**((elo_l-elo_w)/400)))
    exp_l = 1/(1+(10**((elo_w-elo_l)/400)))
    exp_surface_w = 1/(1+(10**((elo_surface_l-elo_surface_w)/400)))
    exp_surface_l = 1/(1+(10**((elo_surface_w-elo_surface_l)/400)))

    # Update ELO ratings for next match
    elo_w += k*(1-exp_w)
    elo_l += k*(0-exp_l)
    elo_surface_w += k*(1-exp_surface_w)
    elo_surface_l += k*(0-exp_surface_l)

    # Store updated ratings
    prev_stats["elo_players"][w_id] = elo_w
    prev_stats["elo_players"][l_id] = elo_l
    prev_stats["elo_surface_players"][surface][w_id] = elo_surface_w
    prev_stats["elo_surface_players"][surface][l_id] = elo_surface_l

    ########################################################
    ############## ELO GRAD ##############
    prev_stats["elo_grad_players"][w_id].append(elo_w)
    prev_stats["elo_grad_players"][l_id].append(elo_l)
    
    ########################################################
    ############## Matches Played ##############
    prev_stats["matches_played"][w_id] += 1
    prev_stats["matches_played"][l_id] += 1

    ########################################################
    ############## % Last K Matches Won ##############
    prev_stats["last_k_matches"][w_id].append(1)
    prev_stats["last_k_matches"][l_id].append(0)

    ########################################################
    ############# H2H and H2H on that surface #############
    prev_stats["h2h"][(w_id, l_id)] += 1
    prev_stats["h2h_surface"][surface][(w_id, l_id)] += 1

    ########################################################
    ############# UPDATE Various Ohter Statistics #############
    if p1_id == getWinnerLoserIDS(p1_id, p2_id, result)[0]:
        w_ace, l_ace = match.p1_ace, match.p2_ace
        w_df, l_df = match.p1_df, match.p2_df
        w_svpt, l_svpt = match.p1_svpt, match.p2_svpt
        w_1stIn, l_1stIn = match.p1_1stIn, match.p2_1stIn
        w_1stWon, l_1stWon = match.p1_1stWon, match.p2_1stWon
        w_2ndWon, l_2ndWon = match.p1_2ndWon, match.p2_2ndWon
        w_bpSaved, l_bpSaved = match.p1_bpSaved, match.p2_bpSaved
        w_bpFaced, l_bpFaced = match.p1_bpFaced, match.p2_bpFaced
    else:
        w_ace, l_ace = match.p2_ace, match.p1_ace
        w_df, l_df = match.p2_df, match.p1_df
        w_svpt, l_svpt = match.p2_svpt, match.p1_svpt
        w_1stIn, l_1stIn = match.p2_1stIn, match.p1_1stIn
        w_1stWon, l_1stWon = match.p2_1stWon, match.p1_1stWon
        w_2ndWon, l_2ndWon = match.p2_2ndWon, match.p1_2ndWon
        w_bpSaved, l_bpSaved = match.p2_bpSaved, match.p1_bpSaved
        w_bpFaced, l_bpFaced = match.p2_bpFaced, match.p1_bpFaced

    if (w_svpt != 0) and (w_svpt != w_1stIn):
        # Percentatge of aces
        prev_stats["last_k_matches_stats"][w_id]["p_ace"].append(100*(w_ace/w_svpt))
        # Percentatge of double faults
        prev_stats["last_k_matches_stats"][w_id]["p_df"].append(100*(w_df/w_svpt))
        # Percentatge of first serve in
        prev_stats["last_k_matches_stats"][w_id]["p_1stIn"].append(100*(w_1stIn/w_svpt))
        # Percentatge of second serve won
        prev_stats["last_k_matches_stats"][w_id]["p_2ndWon"].append(100*(w_2ndWon/(w_svpt-w_1stIn)))
    if l_svpt != 0 and (l_svpt != l_1stIn):
        prev_stats["last_k_matches_stats"][l_id]["p_ace"].append(100*(l_ace/l_svpt))
        prev_stats["last_k_matches_stats"][l_id]["p_df"].append(100*(l_df/l_svpt))
        prev_stats["last_k_matches_stats"][l_id]["p_1stIn"].append(100*(l_1stIn/l_svpt))
        prev_stats["last_k_matches_stats"][l_id]["p_2ndWon"].append(100*(l_2ndWon/(l_svpt-l_1stIn)))

    # Percentatge of first serve won
    if w_1stIn != 0:
        prev_stats["last_k_matches_stats"][w_id]["p_1stWon"].append(100*(w_1stWon/w_1stIn))
    if l_1stIn != 0:
        prev_stats["last_k_matches_stats"][l_id]["p_1stWon"].append(100*(l_1stWon/l_1stIn))
    
    # Percentatge of second serve won
    if w_bpFaced != 0:
        prev_stats["last_k_matches_stats"][w_id]["p_bpSaved"].append(100*(w_bpSaved/w_bpFaced))
    if l_bpFaced != 0:
        prev_stats["last_k_matches_stats"][l_id]["p_bpSaved"].append(100*(l_bpSaved/l_bpFaced))
    
    return prev_stats

"""
INPUTS:
Player1 and Player2 should be a dictionaries with the following keys for each player: ID, ATP_POINTS, ATP_RANK, AGE, HEIGHT, 
Match should be a dict with common information about the game (like the number of BEST_OF, DRAW_SIZE, SURFACE). (cool thing is that in the future we can add more stuff here).
Prev_stats should be all the stats data we have until the most recent game. If we were predicting new data, we would just pass all the calculated stats in the dataset from 1991 to now.

OUTPUT:
Outputs a dictionary with all the stats calcualted
"""
def getStats(player1, player2, match, prev_stats):
    from utils.common import mean, getWinnerLoserIDS
    import numpy as np

    output = {}
    PLAYER1_ID = player1["ID"]
    PLAYER2_ID = player2["ID"]
    SURFACE = match["SURFACE"]

    # Get Differences
    output["BEST_OF"] = match["BEST_OF"]
    output["DRAW_SIZE"] = match["DRAW_SIZE"]
    output["AGE_DIFF"] = player1["AGE"]-player2["AGE"]
    output["HEIGHT_DIFF"] = player1["HEIGHT"]-player2["HEIGHT"]
    output["ATP_RANK_DIFF"] = player1["ATP_RANK"]-player2["ATP_RANK"]
    output["ATP_POINTS_DIFF"] = player1["ATP_POINTS"]-player2["ATP_POINTS"]

    # Get Stats from Dictionary
    elo_players = prev_stats["elo_players"]
    elo_surface_players = prev_stats["elo_surface_players"]
    elo_grad_players = prev_stats["elo_grad_players"]
    last_k_matches = prev_stats["last_k_matches"]
    last_k_matches_stats = prev_stats["last_k_matches_stats"]
    matches_played = prev_stats["matches_played"]
    h2h = prev_stats["h2h"]
    h2h_surface = prev_stats["h2h_surface"]

    ####################### GET STATS ########################
    output["ELO_DIFF"] = elo_players[PLAYER1_ID] - elo_players[PLAYER2_ID]
    output["ELO_SURFACE_DIFF"] = elo_surface_players[SURFACE][PLAYER1_ID] - elo_surface_players[SURFACE][PLAYER2_ID]
    output["N_GAMES_DIFF"] = matches_played[PLAYER1_ID] - matches_played[PLAYER2_ID]
    output["H2H_DIFF"] = h2h[(PLAYER1_ID, PLAYER2_ID)] - h2h[(PLAYER2_ID, PLAYER1_ID)]
    output["H2H_SURFACE_DIFF"] = h2h_surface[SURFACE][(PLAYER1_ID, PLAYER2_ID)] - h2h_surface[SURFACE][(PLAYER2_ID, PLAYER1_ID)]

    for k in [3, 5, 10, 25, 50, 100, 200]:
        ############## Last K Matches Won ##############
        if len(last_k_matches[PLAYER1_ID]) >= k and len(last_k_matches[PLAYER2_ID]) >= k:
            # Calculate wins in the last k matches
            output["WIN_LAST_"+str(k)+"_DIFF"] = sum(list(last_k_matches[PLAYER1_ID])[-k:])-sum(list(last_k_matches[PLAYER2_ID])[-k:])
        else:
            output["WIN_LAST_"+str(k)+"_DIFF"] = 0
        
        ############## ELO GRAD ##############
        # Calculate gradient BEFORE match
        if len(elo_grad_players[PLAYER1_ID]) >= k and len(elo_grad_players[PLAYER2_ID]) >= k:
            elo_grad_p1 = list(last_k_matches[PLAYER1_ID])[-k:]
            elo_grad_p2 = list(last_k_matches[PLAYER2_ID])[-k:]
            slope_1 = np.polyfit(np.arange(len(elo_grad_p1)), np.array(elo_grad_p1), 1)[0]
            slope_2 = np.polyfit(np.arange(len(elo_grad_p2)), np.array(elo_grad_p2), 1)[0]
            output["ELO_GRAD_LAST_"+str(k)+"_DIFF"] = slope_1-slope_2
        else:
            output["ELO_GRAD_LAST_"+str(k)+"_DIFF"] = 0

        ############# Various Ohter Statistics #############
        output["P_ACE_LAST_"+str(k)+"_DIFF"] = mean(list(last_k_matches_stats[PLAYER1_ID]["p_ace"])[-k:])-mean(list(last_k_matches_stats[PLAYER2_ID]["p_ace"])[-k:])
        output["P_DF_LAST_"+str(k)+"_DIFF"] = mean(list(last_k_matches_stats[PLAYER1_ID]["p_df"])[-k:])-mean(list(last_k_matches_stats[PLAYER2_ID]["p_df"])[-k:])
        output["P_1ST_IN_LAST_"+str(k)+"_DIFF"] = mean(list(last_k_matches_stats[PLAYER1_ID]["p_1stIn"])[-k:])-mean(list(last_k_matches_stats[PLAYER2_ID]["p_1stIn"])[-k:])
        output["P_1ST_WON_LAST_"+str(k)+"_DIFF"] = mean(list(last_k_matches_stats[PLAYER1_ID]["p_1stWon"])[-k:])-mean(list(last_k_matches_stats[PLAYER2_ID]["p_1stWon"])[-k:])
        output["P_2ND_WON_LAST_"+str(k)+"_DIFF"] = mean(list(last_k_matches_stats[PLAYER1_ID]["p_2ndWon"])[-k:])-mean(list(last_k_matches_stats[PLAYER2_ID]["p_2ndWon"])[-k:])
        output["P_BP_SAVED_LAST_"+str(k)+"_DIFF"] = mean(list(last_k_matches_stats[PLAYER1_ID]["p_bpSaved"])[-k:])-mean(list(last_k_matches_stats[PLAYER2_ID]["p_bpSaved"])[-k:])

    return output

if __name__ == '__main__':
    pass