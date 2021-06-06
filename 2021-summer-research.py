import random

def LPT(machines, jobs):
    jobs.sort(key=lambda jobs: jobs[0], reverse=True)
    min = machines[1][0]
    index = 1
    for item in jobs:
        min = machines[index][0]
        for i in range (1, machines[0][0]+1):
            if machines[i][0] < min:
                min = machines[i][0]
                index = i
        insert_job(machines, item[0], index)

def makespan(machine_list):
    max = 0
    for i in range(1, len(machine_list)):
        if machine_list[i][0] > max:
            max = machine_list[i][0]
    return max

def insert_job(machine_list, job, machine_index):
    machine_list[machine_index][0] += job

def main(m, nj):
    machines = [[m]]
    jobs = []
    for i in range(m):
        machines.append([0])
    for i in range(nj):
        jobs.append([random.randint(1,10)])

    LPT(machines, jobs)
    print(jobs)
    print(machines)

main(5,8)
