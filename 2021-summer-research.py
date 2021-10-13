import random
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import colorsys
import copy


def visualization(machines, jobs, algo):
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Processing Time')
    gnt.set_ylabel('Machine')

    yticks = []
    ylabels = []
    for i in range(len(machines)):
        yt = 15 * (i + 1)
        yl = i + 1
        ylabels.append(str(yl))
        yticks.append(yt)
    color = []
    for i in range(len(jobs)):
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        c = '#%02x%02x%02x' % (r, g, b)
        color.append(c)
    # print(color)
    # color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(jobs))]

    # Setting ticks on y-axis
    gnt.set_yticks(yticks)
    # Labelling tickes of y-axis
    gnt.set_yticklabels(ylabels)
    #     print(yticks, ylabels)

    # Setting graph attribute

    gnt.grid(True)
    # Declaring a bar in schedule
    previous = 0

    # for i in range (len(machines)):
    #     for j in range (len(machines[i])):
    #         gnt.broken_barh([(previous, machines[i][j][0])], ((i+1)*10, 9), facecolors =(color[machines[i][j][1]-1]), edgecolor = "black")
    #         previous += machines[i][j][0]
    #     previous = 0

    for i in range(len(machines)):
        for j in range(len(machines[i])):
            if machines[i][j][1] != 0:
                gnt.broken_barh([(previous, machines[i][j][0])], ((i + 1) * 10, 9),
                                facecolors=(color[machines[i][j][1] - 1]), edgecolor="black")
                previous += machines[i][j][0]
            else:
                if (float(machines[i][j][0])) != 0:
                    gnt.broken_barh([(previous, (float(machines[i][j][0])))], ((i + 1) * 10, 9), facecolors='white',
                                    edgecolor="black")
                    previous += (float(machines[i][j][0]))
        previous = 0

    plt.yticks([])
    fig.set_size_inches(37, 21)
    plt.title(algo)
    plt.show()
    plt.savefig("{}.png".format(algo))
    # mpimg.imsave("{}.png".format(algo), fig)
        

def evan(machines, jobs, c):
    machines[0].append([jobs[0][0], 1])
    high = 0
    low = 1
    for index2, item in enumerate(jobs):
        if index2 == 0:
            continue
        if makespan_machines(machines[high]) + item[0] - makespan_machines(machines[low]) <= makespan_machines(
                machines[low]):
            machines[high].append([item[0], index2 + 1])
        elif (item[0] / 2 + c > item[0]) or min(makespan_machines(machines[low]) + item[0],
                                                makespan_machines(machines[high])) >= max(
                makespan_machines(machines[low]) + item[0], makespan_machines(machines[high])) - min(
                makespan_machines(machines[low]) + item[0], makespan_machines(machines[high])):
            machines[low].append([item[0], index2 + 1])
        else:
            machines[low].append([str(makespan_machines(machines[high]) - makespan_machines(machines[low])), 0])
            machines[low].append([item[0]/2+c, index2+1])
            machines[high].append([item[0] / 2 + c, index2+1])
        if makespan_machines(machines[0]) > makespan_machines(machines[1]):
            high = 0
            low = 1
        else:
            high = 1
            low = 0

def evan_greedy(machines, jobs, c):
    low = 0
    high = 1
    for index2, item in enumerate(jobs):
        if item[0]/2 + c < makespan_machines(machines[low]) + item[0]:
            machines[low].append([str(makespan_machines(machines[high]) - makespan_machines(machines[low])), 0])
            machines[low].append([item[0] / 2 + c, index2+1])
            machines[high].append([item[0] / 2 + c, index2+1])
        else:
            machines[low].append([item[0]/2+c, index2+1])
        if makespan_machines(machines[0]) > makespan_machines(machines[1]):
            high = 0
            low = 1
        else:
            high = 1
            low = 0

def evan_76(machines, jobs, c):
    machines[0].append([jobs[0][0], 1])
    high = 0
    low = 1
    job_sum = jobs[0][0]
    r4 = 0
    for index2, item in enumerate(jobs):
        if index2 == 0:
            continue
        job_sum += item[0]
        if makespan_machines(machines[high]) + item[0] <= 7/12 * job_sum:
            machines[high].append([item[0], index2+1])
        elif max(makespan_machines(machines[low])+item[0], makespan_machines(machines[high])) <= 7/12 * job_sum:
            machines[low].append([item[0], index2+1])
        elif makespan_machines(machines[high]) + item[0]/2 + c <= 7/12 * job_sum:
            machines[low].append([str(makespan_machines(machines[high]) - makespan_machines(machines[low])), 0])
            machines[low].append([item[0] / 2 + c, index2 + 1])
            machines[high].append([item[0] / 2 + c, index2 + 1])
        else:
            r4 += 1
            machines[low].append([item[0], index2+1])
            # machines[low].append([str(makespan_machines(machines[high]) - makespan_machines(machines[low])), 0])
            # machines[low].append([item[0] / 2 + c, index2 + 1])
            # machines[high].append([item[0] / 2 + c, index2 + 1])
        if makespan_machines(machines[0]) > makespan_machines(machines[1]):
            high = 0
            low = 1
        else:
            high = 1
            low = 0
        # print(makespan(machines)*2/sum([makespan_machines(machines[0])+makespan_machines(machines[1])]))
    return r4

def khoi12c(machines, jobs, c):
    ij = 0
    block = 0
    const = 12
    if jobs[0][0] <= const*c + ij:
        machines[0].append([jobs[0][0], 1])
        ij = jobs[0][0]
    else:
        machines[0].append([str(jobs[0][0]/2 + c), 1])
        machines[1].append([str(jobs[0][0]/2 + c), 1])
        block += 1
    high = 0
    low = 1
    for index, item in enumerate(jobs):
        if index == 0:
            continue
        if item[0] <= const*c + ij:
            machines[low].append([item[0], index+1])
            if makespan_machines(machines[0]) > makespan_machines(machines[1]):
                ij = makespan_machines(machines[0]) - makespan_machines(machines[1])
            else:
                ij = makespan_machines(machines[1]) - makespan_machines(machines[0])
        else:
            machines[low].append([str(makespan_machines(machines[high]) - makespan_machines(machines[low])), 0])
            machines[low].append([item[0] / 2 + c, index + 1])
            machines[high].append([item[0] / 2 + c, index + 1])
            ij = 0
        if makespan_machines(machines[0]) > makespan_machines(machines[1]):
            high = 0
            low = 1
        else:
            high = 1
            low = 0

def LS(machines, jobs):
    min = machines[0][0]
    index = 0
    for index2, item in enumerate(jobs):
        print(machines)
        min = machines[index][0]
        for i in range(0, len(machines)):
            if machines[i][0] < min:
                min = machines[i][0]
                index = i
        insert_job(machines, item[0], index)
        machines[index].append([item[0], index2 + 1])
    # LS_makespan = makespan(machines)
    for i in range(len(machines)):
        machines[i] = machines[i][1:]
    # return LS_makespan


def SET(machines, jobs, c):
    m = len(machines) - 1
    for index, item in enumerate(jobs):
        kj = 0
        k = min(m, math.sqrt(item[0] / c))
        if k == m:
            kj = m
        elif (item[0] / (math.floor(k)) + (math.floor(k) - 1) * c) <= (
                item[0] / (math.ceil(k)) + (math.ceil(k) - 1) * c):
            kj = math.floor(k)
        else:
            kj = math.ceil(k)
        machines.sort(key=lambda machines: machines[0])
        sj = machines[kj - 1][0]
        for j in range(kj):
            # if machines[j][0] == 0:
            #     machines[j].append([sj + (item[0]/(kj)+(kj-1)*c), index+1])
            # else:
            machines[j].append([str(sj - machines[j][0]), 0])
            machines[j].append([(item[0] / (kj) + (kj - 1) * c), index + 1])
            machines[j][0] = sj + (item[0] / (kj) + (kj - 1) * c)
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
        for i in range(0, len(machines)):
            if machines[i][0] < min:
                min = machines[i][0]
                index = i
        insert_job(machines, item[0], index)
        machines[index].append([item[0], index2 + 1])
    # LPT_makespan = makespan(machines)
    for i in range(len(machines)):
        machines[i] = machines[i][1:]
    return machines

def makespan_machines(machine):
    return sum([float(machine[i][0]) for i in range(len(machine))])

def makespan(machine_list):
    return max([makespan_machines(machine_list[i]) for i in range(len(machine_list))])


def insert_job(machine_list, job, machine_index):
    machine_list[machine_index][0] += job


def main(m, nj):
    machines = []
    jobs = []
    for i in range(m):
        machines.append([0])
    for i in range(nj):
        jobs.append([random.randint(1, 10)])

    # machines2 = copy.deepcopy(machines)
    # machines3 = copy.deepcopy(machines)
    # 
    # makespan = SET(machines, jobs, 1)
    # makespan2 = LS(machines2, jobs)
    # makespan3 = LPT(machines3, jobs)
    # 
    # visualization(machines, jobs, "SET Algorithm")
    # visualization(machines2, jobs, "LS Algorithm")
    # visualization(machines3, jobs, "LPT Algorithm")

    # print(makespan)
    # for i in machines:
    #     print(makespan_machines(i), i)
    # print(jobs)
    # LS(machines, jobs)
    # for i in machines:
    #     print(i)

    LS(machines, jobs)
    print(jobs)
    for i in machines:
        print(i)
    # print(makespan(machines)*2/sum([jobs[i][0] for i in range(len(jobs))]))

    visualization(machines, jobs, "Evan algo")
    
# main(5, 20)

def stimulation_2machines():
    maxi = 0
    max_jobs = []
    c_max = 0
    jobs_range = 0
    no_job_max = 0
    no_r4 = 0
    max_r4 = 0
    for j in range(50000):
        nj = random.randint(1000,2000)
        jobs = []
        jr = random.randint(1,500)
        for i in range(nj):
            jobs.append([random.randint(1, jr)])
        machines_evan = [[], []]
        cr = random.randint(2000,3000)
        no_r4 = evan_76(machines_evan, jobs, cr)
        k = makespan(machines_evan)*2/sum([jobs[i][0] for i in range(len(jobs))])
        if k > maxi:
            maxi = k
            max_jobs = copy.deepcopy(jobs)
            c_max = cr
            jobs_range = jr
            no_job_max = nj
            max_r4 = no_r4
            print(maxi, no_r4)

    print(maxi, max_r4)
    print(max_jobs)
    print(c_max)
    print(jobs_range)
    print(no_job_max)
# stimulation_2machines()

# c = 4
# epsilon = 0.01
# l = []
# for i in range (300):
#     if i == 0:
#         l.append([12*c-epsilon])
#     else:
#         l.append([12*(6**i)*c-epsilon])
# m = [[],[]]
# print(evan_76(m, l, c))
# print(l)
# for i in (m):
#     print(i)
# avg = sum(l[i][0] for i in range(len(l)))
# print(len(l))
# print(makespan(m), avg)
# print(makespan(m)*2/avg)

def generate_random_jobs(n, range1):
    job = []
    for x in range (n):
        job.append([random.randint(1, range1)])
    return job

def find_counter(c):
    epsilon = 0.0001*c
    job = [[], []]
    job[0].append(12*c-epsilon)
    li = 0
    si = 1
    for i in range (1000):
        # print('a')
        # print("Bound:", 7/5 * (sum(job[0])+sum(job[1])) - 12/5 * sum(job[si]), 12*sum(job[li]) + 12*c - 7*(sum(job[0])+sum(job[1])) - epsilon)
        lower = 7/5 * (sum(job[0])+sum(job[1])) - 12/5 * sum(job[si])
        # print('a1')
        upper = 12 * sum(job[li]) + 12 * c - 7 * (sum(job[0]) + sum(job[1]))
        # print('a2')
        while epsilon/(upper) < 10**(-2):
            epsilon *= 10
            # print(epsilon/upper)
        # print('a3')
        upper -= epsilon
        lower += epsilon
        k = lower + (upper - lower)*random.random()
        # print(lower, upper, k)
        # print(sum(job[li]))
        if math.isnan(upper):
            break
        job[si].append(upper)
        if sum(job[0]) > sum(job[1]):
            li = 0
            si = 1
        else:
            si = 0
            li = 1
        # print(sum(job[li])/ (max((sum(job[0]) + sum(job[1]))/2, max(job[li]))))
    # for i in (job):
    #     print(i)
    fin_job = []

    for i in range(len(job[1])):
        for j in range(len(job)):
            fin_job.append([job[j][i]])
    return fin_job

def algo_finding_simulation_three_machines():
    alpha = 0
    beta = 0
    c = 0
    best_ratio = float('inf')
    for i in range(1, 100):
        for j in range(1,11):
            for q in range(1, 1000):
                worst_case = 0
                w_alpha = 0
                w_beta = 0
                w_c = 0
                for iter in range(1000):
                    machines = [[], [], []]
                    makespan = [0, 0, 0]
                    jobs = generate_random_jobs(5000, 1000)
                    opt = sum([jobs[i][0] for i in range(len(jobs))]) / 3
                    max_machine = 0
                    min_machine = 1
                    med_machine = 2
                    for _ in range(len(jobs)):
                        ij = makespan[max_machine] - makespan[med_machine] - makespan[min_machine]
                        if jobs[_][0] <= i * q + j * ij:
                            machines[min_machine].append([jobs[_][0], _ + 1])
                            makespan[min_machine] += jobs[_][0]

                            max_machine = makespan.index(max(makespan))
                            min_machine = makespan.index(min(makespan))
                            med_machine = 3 - max_machine - min_machine
                        else:
                            machines[max_machine].append([jobs[_][0] / 3 + 2 * q, _ + 1])
                            makespan[max_machine] += jobs[_][0] / 3 + 2 * q

                            machines[min_machine].append([str(makespan[max_machine] - makespan[min_machine]), 0])
                            machines[med_machine].append([str(makespan[max_machine] - makespan[med_machine]), 0])

                            max_machine = makespan.index(max(makespan))
                            min_machine = makespan.index(min(makespan))
                            med_machine = 3 - max_machine - min_machine

                            makespan[med_machine] = makespan[max_machine]
                            makespan[min_machine] = makespan[max_machine]

                    algo = max(makespan)
                    ratio = algo / opt
                    if ratio > worst_case:
                        worst_case = ratio
                        w_alpha = i
                        w_beta = j
                        w_c = q
                if worst_case < best_ratio:
                    best_ratio = worst_case
                    alpha = w_alpha
                    beta = w_beta
                    c = w_c
                    print(best_ratio, alpha, beta, c)

    print(best_ratio, alpha, beta, c)

def three_machines_worstcase():

    min_ratio = 10000
    mina = 0
    minb = 0
    for _ in range(1, 1001):
        for alpha in range (1, 1000, 10):
            beta = _/1000
            if beta == 1.001:
                beta = 1
            idle = 0
            algo = 0
            opt = 0
            for i in range (500):
                first = alpha + beta*idle
                algo += first
                opt += first/3

                idle += 2*first
                second = alpha + beta*idle
                algo += second/3 + 2
                opt += second/3

            print(algo/opt)
            if algo/opt < min_ratio:
                mina, minb = alpha, beta
                min_ratio = algo/opt

    print("Min: " + str(min_ratio) + " with alpha = " + str(mina) + " and beta = " + str(minb))

def test_hypo(m, n):
    machine = [(1-1/m)**i for i in range (m)]
    job = [i for i in machine]
    for i in range(n*m):
        new_job = max(machine)/(1-1/m) - min(machine)
        job.append(new_job)
        machine[-1] += new_job
        machine.sort(reverse=True)
    rawjob = copy.deepcopy(job)
    job.sort(reverse = True)
    return machine[0], rawjob, job

def hypo_visualization(machines, jobs, algo):
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Processing Time')
    gnt.set_ylabel('Machine')

    yticks = []
    ylabels = []
    for i in range(len(machines)):
        yt = 15 * (i + 1)
        yl = i + 1
        ylabels.append(str(yl))
        yticks.append(yt)
    color = []
    for i in range(len(jobs)):
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        c = '#%02x%02x%02x' % (r, g, b)
        color.append(c)


    # Setting ticks on y-axis
    gnt.set_yticks(yticks)
    # Labelling tickes of y-axis
    gnt.set_yticklabels(ylabels)

    gnt.grid(True)
    # Declaring a bar in schedule
    previous = 0

    for i in range(len(machines)):
        for j in range(len(machines[i])):
            if machines[i][j][1] != 0:
                gnt.broken_barh([(previous, machines[i][j][0])], ((i + 1) * 10, 9),
                                facecolors=(color[j]), edgecolor="black")
                previous += machines[i][j][0]
            else:
                if (float(machines[i][j][0])) != 0:
                    gnt.broken_barh([(previous, (float(machines[i][j][0])))], ((i + 1) * 10, 9), facecolors='white',
                                    edgecolor="black")
                    previous += (float(machines[i][j][0]))
        previous = 0

    plt.yticks([])
    fig.set_size_inches(37, 21)
    plt.title(algo)
    plt.show()
    plt.savefig("{}.png".format(algo))
    # mpimg.imsave("{}.png".format(algo), fig)


m = 150
iter = 50
algo, rawjob, job = test_hypo(m, iter)

job = [[job[i]] for i in range(len(job))]
machines = LPT([[0] for i in range(m)], job)

hypo_visualization(machines, job, "test")
print(machines)
print(len(machines))
# print(max([machines[i][0] for i in range(len(machines))]))
# print(rawjob)
# print(rawjob.index(max(rawjob)))
# for i in range(len(rawjob), 0, -1):
#     rawjob[i] /= rawjob[i-1]
# rawjob[0] = 1
# print(rawjob)

# algo_finding_simulation_three_machines()
