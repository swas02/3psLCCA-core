from .... import standard_keys as c


def calculate_total_cost(cost_data, vehicle_counts):
    distance_total = {c.IT: 0.0, c.ET: 0.0}
    time_total = {c.IT: 0.0, c.ET: 0.0}

    for vehicle, count in vehicle_counts.items():
        if vehicle not in cost_data["distanceCost"]:
            continue

        distance_total[c.IT] += cost_data["distanceCost"][vehicle][c.IT] * count
        distance_total[c.ET] += cost_data["distanceCost"][vehicle][c.ET] * count

        time_total[c.IT] += cost_data["timeCost"][vehicle][c.IT] * count
        time_total[c.ET] += cost_data["timeCost"][vehicle][c.ET] * count

    total = {
        c.IT: distance_total[c.IT] + time_total[c.IT],
        c.ET: distance_total[c.ET] + time_total[c.ET],
    }

    return {
        "distance_total": distance_total,
        "time_total": time_total,
        "total": total,
        c.UNIT: "Rs/km",
    }
