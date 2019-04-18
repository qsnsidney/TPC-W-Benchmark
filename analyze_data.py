import sys

dataf = open(sys.argv[1])

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
    
endtimes = get_times(data, "endtimes")
starttimes = get_times(data, "starttimes")
wips = get_times(data, "wips")[:config["rampu_t"] + config["measure_t"] + config["rampd_t"]]

average_throughput = sum(wips[config["rampu_t"]-1:config["rampu_t"] + config["measure_t"]+1])/float(config["measure_t"]+2)
print "Average throughput:", average_throughput

response_times = [endtimes[k] - starttimes[k] for k in xrange(len(endtimes))]

rt_measure = []

# get response times in measure interval
for i in xrange(len(starttimes)):
    if starttimes[i]>=config["rampu_t"]*1000 and starttimes[i] <= (config["rampu_t"] + config["measure_t"])*1000:
        rt_measure.append(endtimes[i] - starttimes[i])
# print len(rt_measure), "interractions inside the measurement interval"

average_rt = sum(rt_measure)/float(len(rt_measure))
print "Average Response Time:", average_rt