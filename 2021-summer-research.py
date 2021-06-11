import random
import math

def LS(machines, jobs):
    min = machines[0][0]
    index = 0
    for index2, item in enumerate(jobs):
        min = machines[index][0]
        for i in range(0, len(machines)):
            if machines[i][0] < min:
                min = machines[i][0]
                index = i
        insert_job(machines, item[0], index)
        machines[index].append([item[0], index2 + 1])
    LS_makespan = makespan(machines)
    for i in range(len(machines)):
        machines[i] = machines[i][1:]
    return LS_makespan

def SET(machines, jobs, c):
    m = len(machines) - 1
    for index, item in enumerate(jobs):
        kj = 0
        k = min(m, math.sqrt(item[0]/c))
        if k == m:
            kj = m
        elif (item[0]/(math.floor(k))+(math.floor(k)-1)*c) <= (item[0]/(math.ceil(k))+(math.ceil(k)-1)*c):
            kj = math.floor(k)
        else:
            kj = math.ceil(k)
        machines.sort(key=lambda machines: machines[0])
        sj = machines[kj-1][0]
        for j in range(kj):
            if machines[j][0] == 0:
                machines[j].append([sj + (item[0]/(kj)+(kj-1)*c), index+1])
            else:
                machines[j].append([str(sj-machines[j][0]), 0])
                machines[j].append([(item[0]/(kj)+(kj-1)*c), index+1])
            machines[j][0] = sj + (item[0]/(kj)+(kj-1)*c)
    SET_makespan = makespan(machines)
    for i in range(len(machines)):
        machines[i] = machines[i][1:]
    return SET_makespan

def LPT(machines, jobs):
    jobs.sort(key=lambda jobs: jobs[0], reverse=True)
    min = machines[0][0]
    index = 0
    for index2, item in enumerate(jobs):
        min = machines[index][0]
        for i in range (0, len(machines)):
            if machines[i][0] < min:
                min = machines[i][0]
                index = i
        insert_job(machines, item[0], index)
        machines[index].append([item[0], index2+1])
    LPT_makespan = makespan(machines)
    for i in range(len(machines)):
        machines[i] = machines[i][1:]
    return LPT_makespan

def makespan(machine_list):
    return max([machine_list[i][0] for i in range(len(machine_list))])

def makespan_machines(machine):
    return sum([machine[i][0] for i in range(len(machine))])

def insert_job(machine_list, job, machine_index):
    machine_list[machine_index][0] += job

def main(m, nj):
    machines = []
    jobs = []
    for i in range(m):
        machines.append([0])
    for i in range(nj):
        jobs.append([random.randint(1,10)])

    # makespan = LPT(machines, jobs)
    # print(makespan)
    # for i in machines:
    #     print(makespan_machines(i), i)
    print(jobs)
    LS(machines, jobs)
    for i in machines:
        print(i)

main(5,8)

