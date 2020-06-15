import pandas as pd
import numpy as np
import math


# Complete the sockMerchant function in the editor below.
# It must return an integer representing the number of matching pairs of socks that are available.
# sockMerchant has the following parameter(s):
#    n: the number of socks in the pile
#    ar: the colors of each sock

def sockMerchant(n, ar):
    df = pd.DataFrame({'socks': ar})
    count = df['socks'].value_counts()
    new_count = np.array(count)
    tot_pair = 0
    for i in range(0, np.size(new_count)):
        if new_count[i] % 2 == 1:
            new_count[i] = new_count[i] - 1
        pair = new_count[i] / 2
        tot_pair += pair
    return int(tot_pair)


# see if two string A and B can be made the same.
# B is all capitalized with letters from the alphabet.
# A has a combination of capitalized and un-capitalized
# you can only edit A by the following two rules:
# 1. you may capitalize letters in A
# 2. you can delete letters in A


def abbreviation(a, b):
    list1 = list(a)
    list2 = list(b)

    i = 0
    j = 0
    while i < len(list1):
        if list1[i].capitalize() == list2[j]:
            i += 1
            if j + 1 < len(list2):
                j += 1
        elif list1[i].capitalize() != list2[j]:
            list1.pop(i)

    if len(list1) == len(list2):
        return True
    else:
        return False


# Return an integer that denotes the number of valleys Gary traversed.
# String is a sequence in {UD}.
# U is +1 and D is -1, a valley is steps below sea level.
# Gary starts and ends at sea level
# n is length of path, s is the string describing his path

def countingValleys(n, s):
    num_val = 0
    cum_sum = 0
    for item in s:
        if item == 'U':
            cum_sum += 1
        else:
            if cum_sum - 1 < 0 and cum_sum >= 0:
                num_val += 1
            cum_sum -= 1
    return num_val


# get the minimum number of jumps needed to get to the end of the list
# can only jump 1 or 2 ahead, can jump on 0, cannot jump on 1
# start and end with 0
# it is always possible to win the game

def jumpingOnClouds(c):
    min_jumps = 0
    i = 0
    while i < len(c) - 2:
        if c[i + 2] == 0:
            i += 2
            min_jumps += 1
            continue
        if c[i + 1] == 0:
            i += 1
            min_jumps += 1
            continue
    return min_jumps


# string s, int n, s repeats infinitely and contains a's
# return number of a's in first n bits of the string

def repeatedString(s, n):
    num_a = 0
    tot_num_a = 0
    multi = math.floor(n / len(s))
    rem_len = n % len(s)
    for i in range(0, len(s)):
        if i < rem_len:
            if s[i] == 'a':
                num_a += 1
        if s[i] == 'a':
            tot_num_a += 1
    tot_num_a = tot_num_a * multi
    return tot_num_a + num_a


# given an 6x6 array, find hourglass shape that gives the max sum
# hourglass: 111   sum = 7
#            010
#            111
# input: a list of six lists
# output: max hourglass sum

def hourglassSum(arr):
    max_sum = 0
    cur_sum = 0
    for i in range(1, 5):
        for j in range(1, 5):
            cur_sum = arr[i][j] + arr[i - 1][j] + arr[i - 1][j - 1] + arr[i - 1][j + 1] + arr[i + 1][j] + arr[i + 1][
                j - 1] + arr[i + 1][j + 1]
            if cur_sum >= max_sum:
                max_sum = cur_sum
    return max_sum


# input: a, array of int, d, number of left rotations (d < len(a))
# return array after it has been rotated d times


def rotLeft(a, d):
    rot_arr = [0] * len(a)
    for i in range(0, len(a)):
        place = (i - d) % len(a)
        rot_arr[place] = a[i]
    return rot_arr


def minimumBribes(q):
    min_bribes = 0
    for i in range(0, len(q)):
        if q[i] - i - 1 > 2:
            return "too chaotic"
        for j in range(i, len(q)):
            if q[j] < q[i]:
                min_bribes += 1
    return min_bribes


def candies(n, arr):
    candy_dist = [1] * n
    for i in range(1, n):
        if arr[n - i - 1] > arr[n - i]:
            candy_dist[n - i - 1] = candy_dist[n - i] + 1
    for i in range(0, n - 1):
        if arr[i + 1] > arr[i]:
            candy_dist[i + 1] = max(candy_dist[i] + 1, candy_dist[i + 1])
    return sum(candy_dist)


def maxCircle(queries):
    links  = {} # reference for which set they are in
    length = {} # collection of the lengths
    results = []
    maxl = 2

    def getroot(x):
        while x != links[x]:
            x = links[x]
        return x

    def init(x):
        if x in links:
            return getroot(x)
        length[x] = 1
        links[x] = x
        return x

    for a,b in queries:
        a = init(a)
        b = init(b)
        if a != b:
            # this next line needed to pass test #10
            if length[b]>length[a]: a,b=b,a
            links[b] = a
            length[a] += length[b]
            maxl = max(maxl,length[a])
        results.append(maxl)
    return results

