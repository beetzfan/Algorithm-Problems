import pandas as pd
import csv
import itertools
import time

def calc_time(a, b, c, d):
    return pd.to_timedelta(round((1 / 5) * ((a - b) ** 2 + (c - d) ** 2) ** 0.5), unit='m')


def two_trips(l, k):
    a_b = calc_time(l['X1'], k['X1'], l['Y1'], k['Y1'])
    b_c = calc_time(k['X1'], l['X2'], k['Y1'], l['Y2'])
    a_d = calc_time(l['X1'], k['X2'], l['Y1'], k['Y2'])
    c_d = calc_time(l['X2'], k['X2'], l['Y2'], k['Y2'])
    a_c = l['Trip Len']
    b_d = k['Trip Len']
    l_start = l['Depart After']
    k_start = k['Depart After']
    l_end = l['Arrive Before']
    k_end = k['Arrive Before']

    fin_pos = []
    p1t = k_start + a_b + a_c
    p2t = k_start + a_b + a_c + c_d
    if p1t < l_end and p2t < k_end:
        if k_start + a_b > l_start:
            fin_pos.append([p2t, [k['Trip #'], l['Trip #'], l['Trip #'], k['Trip #']]])

    p1t = l_start + a_b + b_c
    p2t = l_start + a_b + b_c + c_d
    if p1t < l_end and p2t < k_end:
        if l_start + a_b > k_start:
            fin_pos.append([p2t, [l['Trip #'], k['Trip #'], l['Trip #'], k['Trip #']]])

    p1t = k_start + a_b + a_d + c_d
    p2t = k_start + a_b + a_d
    if p1t < l_end and p2t < k_end:
        if k_start + a_b > l_start:
            fin_pos.append([p2t, [k['Trip #'], l['Trip #'], k['Trip #'], l['Trip #']]])

    p1t = l_start + a_b + b_d + c_d
    p2t = l_start + a_b + b_d
    if p1t < l_end and p2t < k_end:
        if l_start + a_b > k_start:
            fin_pos.append([p2t, [l['Trip #'], k['Trip #'], k['Trip #'], l['Trip #']]])

    p1t = k_start + b_d + a_d + a_c
    p2t = k_start + b_d
    if p1t < l_end and p2t < k_end:
        if k_start + b_d + a_d > l_start:
            fin_pos.append([p2t, [k['Trip #'], k['Trip #'], l['Trip #'], l['Trip #']]])

    p1t = l_start + a_c
    p2t = l_start + a_c + b_c + b_d
    if p1t < l_end and p2t < k_end:
        if l_start + a_c + b_c > k_start:
            fin_pos.append([p2t, [l['Trip #'], l['Trip #'], k['Trip #'], k['Trip #']]])
    min_val = 0
    if len(fin_pos) > 0:
        for i in range(1, len(fin_pos)):
            if fin_pos[i][0] < fin_pos[min_val][0]:
                min_val = i
        return fin_pos[min_val][1]
    else:
        return []


# j, k are elements in the ordered pair, the pair is the order of the pickup/ drop off
# l is new element to try and insert
def three_trips(j, k, l, cur_ord):
    # making life easier
    new_list = []
    for i in range(0, 4):
        if cur_ord[i] == j['Trip #']:
            new_list.append(j)
        else:
            new_list.append(k)
    pos_trips = []
    prev_x = 0
    prev_y = 0
    for i in range(len(cur_ord)):
        new_list.insert(i, l)
        # avoiding double counting combinations
        for n in range(0, len(cur_ord)):
            track = []
            if n != i:
                new_list.insert(n, l)
                for m in range(0, 6):
                    a = new_list[m]
                    # if first time seeing a in list, calculate from first destination
                    if len(track) == 0:
                        track.append(a)
                        # if first in order, no need to do any calculations, set to depart after time
                        time = a['Depart After']
                        track.append(a)
                        continue
                    in_list = False
                    for item in track:
                        if a.all() == item.all():
                            in_list = True
                    if not in_list:
                        # need to calculate distance from prev location to current location and add time
                        time += calc_time(prev_x, a['X1'], prev_y, a['Y1'])
                        # save current location for next iteration of calculation
                        prev_x, prev_y = a['X1'], a['Y1']
                    else:
                        # do calculations for drop off location
                        time += calc_time(prev_x, a['X2'], prev_y, a['Y2'])
                        prev_x, prev_y = a['X2'], a['Y2']
                    # if the times do not align, break look and try a different order
                    if not((new_list[m - 1])['Arrive Before'] >= time >= a['Depart After']):
                        break
                    if m == 5:
                        drive_ord = []
                        for item in new_list:
                            drive_ord.append(item['Trip #'])
                        # if we get to the end of the order and everything works, add to possible trips
                        pos_trips.append([time, drive_ord])
                new_list.pop(n)
        new_list.pop(i)
    if len(pos_trips) == 0:
        # if no three person car trips available, return empty list
        return []
    else:
        # find trip with minimum time required, change order back to just trip numbers
        min_val = 0
        for i in range(1, len(pos_trips)):
            if pos_trips[i][0] < pos_trips[min_val][0]:
                min_val = i
        return pos_trips[min_val][1]


def arrange(group, arr):
    arr = arr.loc[arr['Trip #'].isin(group)]
    # adding all singleton trips
    if len(group) == 1:
        # if one element in time group, order is just pickup - dropoff
        return [arr['Trip #'], arr['Trip #']]
    elif len(group) == 2:
        # two in time group find best order
        l = arr.iloc[0]
        k = arr.iloc[1]
        if not two_trips(l, k):
            return [[group[0], group[0]], [group[1], group[1]]]
        else:
            return two_trips(l, k)
    else:
        pos_trips = []
        for item in group:
            pos_trips.append([item, item])
        # group is size three or more
        for i in range(0, len(arr)):
            l = arr.iloc[i]
            # avoid copying possibilities
            for j in range(i, len(arr)):
                if i != j:
                    k = arr.iloc[j]
                    pair = two_trips(l, k)
                    if len(pair) != 0:
                        pos_trips.append(pair)
                        for m in range(0, len(arr)):
                            if m != i and m != j:
                                third = arr.iloc[m]
                                triple = three_trips(l, k, third, pair)
                                if len(triple) != 0:
                                    pos_trips.append(triple)

        return min_pos_trips(pos_trips, group)


def min_pos_trips(pos_trips, group):
    fin_trip = []
    cur_trip = []
    track = set()
    for i in range(1, len(group)):
        x = list(itertools.combinations(range(len(pos_trips)), i))
        for item in x:
            for y in item:
                people = set(pos_trips[y])
                if people.isdisjoint(track):
                    track = track.union(people)
                    cur_trip.append(pos_trips[y])
                else:
                    break
            if len(track) == len(group):
                fin_trip.append(cur_trip)
            track = set()
            cur_trip = []
    min_val = 0
    for i in range(1, len(fin_trip)):
        if len(fin_trip[i]) < len(fin_trip[min_val]):
            min_val = i
    return fin_trip[min_val]


def schedule(shed, arr):
    car = 1
    group_schedule = []
    track = []
    for i in range(0, len(shed)):
        for j in range(0, len(shed[i])):
            a = shed[i][j] - 1
            if a not in track:
                track.append(a)
                if j == 0:
                    time = arr['Depart After'].iloc[a]
                    group_schedule.append([car, arr['Trip #'].iloc[a], arr['Requester'].iloc[a], arr['X1'].iloc[a],
                                           arr['Y1'].iloc[a], time])
                else:
                    time = group_schedule[-1][-1] + calc_time(arr['X1'].iloc[a],
                                                              group_schedule[-1][3], arr['Y1'].iloc[a],
                                                              group_schedule[-1][4])
                    group_schedule.append(
                        [car, arr['Trip #'].iloc[a], arr['Requester'].iloc[a], arr['X1'].iloc[a], arr['Y1'].iloc[a],
                         time])
                continue
            else:
                time = group_schedule[-1][-1] + calc_time(arr['X2'].iloc[a], group_schedule[-1][3], arr['Y2'].iloc[a],
                                                          group_schedule[-1][4])
                group_schedule.append(
                    [car, arr['Trip #'].iloc[a], arr['Requester'].iloc[a], arr['X2'].iloc[a], arr['Y2'].iloc[a], time])
        car += 1
    return group_schedule


def initialize_data(arr):
    arr = pd.DataFrame(arr, columns=['Requester', 'Trip #', 'Depart After', 'Arrive Before', 'X1', 'Y1', 'X2', 'Y2'])
    arr = arr.drop([arr.index[0]])
    arr['Depart After'] += ':00'
    arr['Arrive Before'] += ':00'
    arr['Depart After'] = pd.to_timedelta(arr['Depart After'])
    arr['Arrive Before'] = pd.to_timedelta(arr['Arrive Before'])
    arr['Trip #'] = pd.to_numeric(arr['Trip #'])
    arr['X1'] = pd.to_numeric(arr['X1'])
    arr['Y1'] = pd.to_numeric(arr['Y1'])
    arr['X2'] = pd.to_numeric(arr['X2'])
    arr['Y2'] = pd.to_numeric(arr['Y2'])
    arr['Trip Len'] = pd.to_timedelta(
        round((1 / 5) * ((arr['X1'] - arr["X2"]) ** 2 + (arr['Y1'] - arr['Y2']) ** 2) ** 0.5), unit='m')
    return arr


def disjoint_trips(arr):
    arr = arr.sort_values('Depart After')
    trip_groups = [[arr['Trip #'].iloc[0]]]
    for l in range(1, len(arr)):
        j = 0
        while j < len(trip_groups):
            arr2 = arr[['Trip #', 'Arrive Before']]
            ind = trip_groups[j][0]
            arr2 = arr2.loc[arr2['Trip #'] == ind]
            if arr['Depart After'].iloc[l] < arr2['Arrive Before'].max():
                if arr['Trip #'].iloc[l] != arr2['Trip #'].iloc[0]:
                    trip_groups[j].append(arr['Trip #'].iloc[l])
                break
            if j + 1 == len(trip_groups):
                trip_groups.append([arr['Trip #'].iloc[l]])
            j += 1
    return trip_groups


# main function
def get_car_schedule(trips):
    trips = initialize_data(trips)
    groups = disjoint_trips(trips)
    fin_sched = []
    for i in range(0, len(groups)):
        possible_schedule = arrange(groups[i], trips)
        if type(possible_schedule[0]) == list:
            fin_sched.append(schedule(possible_schedule, trips))
        else:
            fin_sched.append(schedule([possible_schedule], trips))
    text_file = open("Output.txt", "w")
    for item in fin_sched:
        for y in item:
            text_file.write(str(y) + '\n')
    text_file.close()


# read in .txt file and turn into data frame and initialize all data types
with open('Simpsons.txt') as requests:
    request_trip = csv.reader(requests, delimiter='\t')
    start = time.time()
    print(start)
    get_car_schedule(request_trip)
    end = time.time()
    print(end-start)
