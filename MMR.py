async def MMRcalc(playerData, teamObjScore, teamPlayers):


    # calculation shit to get contribution ratio, too lazy to oneline it
    objScore = (playerData["score"]-playerData["kills"]*100)
    contribution = objScore/teamObjScore
    expectedContribution = 1/teamPlayers
    contributionRatio = contribution/expectedContribution

    KD = playerData["kills"]/playerData["deaths"]

    if contributionRatio > 1:
        scoreMMR = 8 + (5*(contributionRatio - 1 )*4)) # carry bonus
    else:
        scoreMMR = 8*contributionRatio

    if (KD*2.5) > 7: # 2.8kd needed to trigger carry bonus
        kdMMR = 7 + KD
    else:
        kdMMR = KD*2.5

    # expected raw MMR (1kd, 1 contrib. ratio) = 10.5 rawMMR
    # hard carry raw MMR (2.8kd, 1.2 contrib. ratio) = 21.8 rawMMR

    rawMMR = kdMMR + scoreMMR
    return rawMMR
