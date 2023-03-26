
import matplotlib.pyplot as plt

player_stats = {
    'Eduardo-Camavinga': [
        ['Statistic', 'Per 90', 'Percentile'], 
        ['Non-Penalty Goals', '0.00', '13'], 
        ['Non-Penalty xG', '0.04', '30']
    ],
    'Lionel-Messi': [
        ['Statistic', 'Per 90', 'Percentile'], 
        ['Non-Penalty Goals', '0.84', '99'], 
        ['Non-Penalty xG', '0.54', '99']
    ],
    'Cristiano-Ronaldo': [
        ['Statistic', 'Per 90', 'Percentile'], 
        ['Non-Penalty Goals', '0.55', '99'], 
        ['Non-Penalty xG', '0.43', '99']
    ]
}


def filterbycharacterstic(data, variable):
    values = []
    for player, stats in data.items():
        for row in stats[1:]:
            if row[0] == variable:
                value = float(row[1])
                percentile = int(row[2])
                values.append((player, value, percentile))

    playername = [t[0] for t in values]
    percent = [t[2] for t in values]
    value1= [t[1] for t in values]

    plt.hist(value1, bins=10, weights=percent)
    plt.title(f"Distribution of {variable} among players")
    plt.xlabel('Value')
    plt.ylabel('percentage')
    plt.xticks(value1, playername)
    plt.subplots_adjust(bottom= 0.4)
    plt.show()

filterbycharacterstic(player_stats, "Non-Penalty xG")