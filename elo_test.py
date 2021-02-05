import math
from random import randint

#Starting
team1 = ['UH', 1250]
team2 = ['BYU', 1200]

# Function to calculate the Probability
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


def eloRating(t1, r1, t2, r2, d):
    K = 30

    p1 = probability(r2, r1)
    p2 = probability(r1, r2)

    if (d == 1):
        r1 = r1 + K * (1 - p1)
        r2 = r2 + K * (0 - p2)

    else:
        r1 = r1 + K * (0 - p1)
        r2 = r2 + K * (1 - p2)
    print("Updated Ratings:")
    print(d)
    print(f"{t1}:", round(r1, 6)," t2 =", round(r2, 6))
    team1[1] = r1
    team2[1] = r2


#Test Data
#K = 30
#d = 1

i=0
while i < 100:
    eloRating(team1[0], team1[1], team2[0], team2[1], randint(0,1))
    i += 1
