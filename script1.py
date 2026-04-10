import random
import statistics
import numpy as np
import matplotlib.pyplot as plt

TARGET = 6
def urgent_recruitment(fivepity, sixpity):
    rateup = 0
    FiveStarPity = fivepity
    star_level = ["four-star", "five-star", "six-star", "rate-up"]
    arsenal_tickets = 0
    pulls = 0
    SixStarPity = sixpity
    while pulls < 10:
        prob = [0.912, 0.08, 0.004, 0.004]
        pulls += 1
        FiveStarPity += 1
        SixStarPity += 1
        if FiveStarPity >= 10:
            prob = [0,0.992,0.004, 0.004]
        i = random.choices(star_level, weights=prob, k=1)[0]
        if i == "rate-up":
            arsenal_tickets += 2000
            rateup += 1
            SixStarPity = 0
            FiveStarPity = 0
        elif i == "four-star":
            arsenal_tickets += 20
        elif i == "five-star":
            arsenal_tickets += 200
            FiveStarPity = 0
            prob = [0.912, 0.08, 0.004, 0.004]
        elif i == "six-star":
            arsenal_tickets += 2000
            SixStarPity = 0
            FiveStarPity = 0
    return(arsenal_tickets, rateup, FiveStarPity, SixStarPity)



def recruitment():
    rateup = 0
    star_level = ["four-star", "five-star", "six-star", "rate-up"]
    arsenal_tickets = 0
    pulls = 0
    sixpity =0
    fivepity = 0
    while rateup < TARGET:
        prob = [0.912, 0.08, 0.004, 0.004]
        pulls += 1
        sixpity += 1
        fivepity += 1
        if pulls == 30:
            ur = urgent_recruitment(fivepity, sixpity)
            arsenal_tickets += ur[0]
            fivepity = ur[2]
            sixpity = ur[3]
            if ur[1] >= 1:
                firstpulls = pulls
                firsttickets = arsenal_tickets + 2000
                rateup += 1
        if sixpity >= 65:
            prob[0], prob[1], prob[2], prob[3] = 0.912*(1-0.05*(sixpity-64)), 0.08*(1-0.05*(sixpity-64)), 0.004+(0.025*(sixpity-64)), 0.004+(0.025*(sixpity-64))
        if sixpity == 80:
            prob = [0,0,0.5,0.5]
        if fivepity >= 10:
            prob[1] = prob[0] + prob[1]
            prob[0] = 0
        if pulls == 120:
            prob = [0,0,0,1]
        if (pulls % 240) == 0:
            rateup += 1
        x = random.choices(star_level, weights=prob, k=1)[0]
        if x == 'rate-up' and rateup == 0:
            firstpulls = pulls
            firsttickets = arsenal_tickets + 2000
        if x == 'rate-up':
            arsenal_tickets += 2000
            rateup += 1
            sixpity = 0
            fivepity = 0
        elif x == 'five-star':
            arsenal_tickets += 200
            fivepity = 0
        elif x == 'six-star':
            arsenal_tickets += 2000
            sixpity = 0
            fivepity = 0
        else:
            arsenal_tickets += 20
    return(pulls, arsenal_tickets, firstpulls, firsttickets)

def weapon():
    pulls = 0
    rateup = 0
    SixStarPity = 0
    star_level = ["fourandfive-star", "six-star", "rate-up"]
    while rateup < 1:
        pulls += 1
        SixStarPity += 1
        probw = [0.96, 0.03, 0.01]
        prob1 = [0.96, 0.03, 0.01]
        if SixStarPity == 4:
            prob1 = [0,0.75,0.25]
            SixStarPity = 0
        if pulls == 8:
            prob1 = [0,0,1]
        x_list = random.choices(star_level, weights=probw, k=9)
        x_list.append(random.choices(star_level, weights=prob1, k=1)[0])
        for item in x_list:
            if item == 'rate-up':
                rateup += 1
    return pulls

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pulls = []
    arsenal_tickets = []
    firstpulls = []
    firsttickets = []
    maxpity = 0
    weapon_pulls = []
    i = 0
    while i < 10000:
        sim = recruitment()
        wsim = weapon()
        pulls.append(sim[0])
        arsenal_tickets.append(sim[1])
        firstpulls.append(sim[2])
        firsttickets.append(sim[3])
        weapon_pulls.append(wsim)
        if sim[2] == 120:
            maxpity += 1
        i += 1
    average_pulls = statistics.mean(pulls)
    average_arsenal_tickets = statistics.mean(arsenal_tickets)
    average_firstpulls = statistics.mean(firstpulls)
    average_firsttickets = statistics.mean(firsttickets)
    percent_120 = maxpity/10000 # Percentage to hit 120 pulls for first rate-up
    average_weapon_pulls = statistics.mean(weapon_pulls)
    print(average_pulls, average_arsenal_tickets, average_firstpulls, average_firsttickets, percent_120, average_weapon_pulls)

    counts = np.bincount(pulls)
    x = np.arange(len(counts))

    plt.figure(figsize=(10,6))
    plt.plot(x, counts, label="Frequency")

    # --- Dotted milestone lines ---
    for milestone in [240, 480, 720]:
        plt.axvline(
            milestone,
            linestyle=":",
            linewidth=2,
            label=f"{milestone} pulls"
        )

    plt.xlabel("Total Pulls")
    plt.ylabel("Frequency")
    plt.title("Distribution of Total Pulls Needed for 6 Rate-Ups (Per Pull)")
    plt.legend()
    plt.grid(True)
    plt.show()


    counts = np.bincount(firstpulls)
    x = np.arange(len(counts))

    plt.figure(figsize=(10,6))
    plt.hist(firstpulls, bins=120, alpha=0.7, color='blue', edgecolor='black')
    plt.axvline(120, linestyle='--', label='120 Guarantee')
    plt.xlabel("Pulls")
    plt.ylabel("Frequency")
    plt.title("Distribution of Pulls Needed for First Featured Unit")
    plt.legend()
    plt.grid(True)
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
