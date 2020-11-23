import sys
import matplotlib.pyplot as plt
import seaborn as sns

# dataf = open(sys.argv[1])
dataf = open("data/tuning.m")

data = dataf.read()
dataf.close()

def gospaces(temp, k):
    while(temp[k] == " "):
        k += 1
    return k

def getend(temp, k):
    k = gospaces(temp, k)
    out = ""
    while(temp[k] != "\n" and temp[k] != " "):
        out += temp[k]
        k += 1
    return out
    
def get(temp, term):
    k = temp.index(term) + len(term)
    return getend(temp, k)

config = {}

# transaction mix
config["mix"] = get(data, "Transaction Mix:")
config["rampu_t"] = int(get(data, "Ramp-up time"))
config["measure_t"] = int(get(data, "Measurement interval"))
config["rampd_t"] = int(get(data, "Ramp-down time"))
config["users"] = int(get(data, "EB Factory"))

print config

def get_times(temp, term):
    k = temp.index(term) + len(term) + 5
    nums = []
    while(temp[k:k+2] != "];"):
        num = ""
        while(temp[k]!="\n"):
            num += temp[k]
            k += 1
        k += 1
        nums.append(int(num))
    return nums
    
# there can be negative values in starttimes because all the times are mentioned as times elapsed from the starttime of the web interraction that ended first
# i.e. every starttimes[j] = startimes[j] - starttimes[0], endtimes[j] = endtimes[j] - starttimes[0] (See the print method of EBStats.java in RBE)
endtimes = get_times(data, "endtimes")
starttimes = get_times(data, "starttimes")
wips = get_times(data, "wips")[:config["rampu_t"] + config["measure_t"] + config["rampd_t"]]

average_throughput = sum(wips[config["rampu_t"]-1:config["rampu_t"] + config["measure_t"]+1])/float(config["measure_t"]+2)
print "Average throughput:", average_throughput

response_times = [(endtimes[k] - starttimes[k]) for k in xrange(len(endtimes))]

## alternative way to calculate average throughout
temp_sum = 0.0

for i in xrange(len(endtimes)):
    if (config["rampu_t"]*1000 < endtimes[i]) and (endtimes[i] <= config["rampu_t"]*1000 + config["measure_t"]*1000):
        temp_sum += 1

print "average throughput (calculated using response times) : " + str(temp_sum / config["measure_t"])

rt_measure = []

# get response times in measure interval
for i in xrange(len(starttimes)):
    if starttimes[i]>=config["rampu_t"]*1000 and endtimes[i] <= (config["rampu_t"] + config["measure_t"])*1000:
        rt_measure.append(endtimes[i] - starttimes[i])
# print len(rt_measure), "interractions inside the measurement interval"

average_rt = sum(rt_measure)/float(len(rt_measure))
print "Average Response Time:", average_rt

# let's plot the results
interval = 1000
curr = interval

average_rts = []
average_tps = []
temp_rts = []

for i in xrange(len(starttimes)):
    if endtimes[i]>curr:
        if len(temp_rts)!=0:
            average_rts.append(float(sum(temp_rts))/len(temp_rts))
            average_tps.append(len(temp_rts))
        else:
            average_rts.append(0)
            average_tps.append(0)
        temp_rts = []
        curr += interval
    else:
        temp_rts.append(endtimes[i] - starttimes[i])

# sns.distplot(response_times)
# plt.show()
plt.plot(average_rts)
plt.ylabel("Average response times per 1 second")
plt.show()

plt.plot(average_tps)
plt.ylabel("Average wips per 1 second")
plt.show()

