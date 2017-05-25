from collections import deque


def shortest_path_from(from_user):
    shortest_path_to = {from_user["id"]: [[]]}
    frontier = deque((from_user, friend)
                     for friend in from_user["friends"])

    # keep going until empty the queue
    while frontier:

        prev_user, cur_user = frontier.popleft()
        user_id = cur_user["id"]
        paths_to_prev_user = shortest_path_to[prev_user["id"]]
        new_paths_to_user = [path + [user_id] for path in paths_to_prev_user]

        old_paths_to_user = shortest_path_to.get(user_id, [])

        if old_paths_to_user:
            min_path_length = len(old_paths_to_user[0])
        else:
            min_path_length = float('inf')

        new_paths_to_user = [path
                             for path in new_paths_to_user
                             if len(path) <= min_path_length
                             and path not in old_paths_to_user]

        shortest_path_to[user_id] = old_paths_to_user + new_paths_to_user

        frontier.extend((cur_user, friend)
                        for friend in cur_user["friends"]
                        if friend["id"] not in shortest_path_to)

    return shortest_path_to


users = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"}
]

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

for user in users:
    user["friends"] = []
    user["betweenness_centrality"] = 0.0

for i, j in friendships:
    users[i]["friends"].append(users[j])
    users[j]["friends"].append(users[i])

for user in users:
    user["shortest_paths"] = shortest_path_from(user)

for source in users:
    source_id = source["id"]
    for target_id, paths in source["shortest_paths"].items():
        if source_id < target_id:
            num_path = len(paths)
            contrib = 1 / num_path
            for path in paths:
                for _id in path:
                    if _id not in [source_id, target_id]:
                        users[_id]["betweenness_centrality"] += contrib

print(users)
