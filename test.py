
def measure_failure(file):
    puts = []
    puts_resp = []
    gets = []
    gets_resp = []

    for line in file.readlines():
        if 'executing PUT' in line:
            i = line.find('mid: ')
            puts.append(line[i + 5:i + 5 + 16])
        elif 'completed PUT' in line:
            i = line.find('mid: ')
            puts_resp.append(line[i + 5:i + 5 + 16])
        elif 'executing GET' in line:
            i = line.find('mid: ')
            gets.append(line[i + 5:i + 5 + 16])
        elif 'completed GET' in line:
            i = line.find('mid: ')
            gets_resp.append(line[i + 5:i + 5 + 16])

    print(f'GETs: {len(gets)}, requests, {len(gets_resp)} responses ({len(gets) - len(gets_resp)} unanswered)')
    print(f'PUTs: {len(puts)} requests, {len(puts_resp)} responses ({len(puts) - len(puts_resp)} unanswered)')
    print(f'unanswered GETs {set(gets).difference(set(gets_resp))}')
    print(f'unanswered PUTs {set(puts).difference(set(puts_resp))}')

    repeats = set()
    for mid in gets_resp:
        if len(list(filter(lambda m: mid == m, gets_resp))) > 1:
            repeats.add(mid)
    print(f'repeated GETs: {repeats}')


    repeats = set()
    for mid in puts_resp:
        if len(list(filter(lambda m: mid == m, puts_resp))) > 1:
            repeats.add(mid)
    print(f'repeated PUTs: {repeats}')


def measure_times(file):
    puts = {}
    total = 0
    redirects = []

    for line in file.readlines():
        if 'executing PUT' in line:
            i = line.find('mid: ')
            mid = line[i + 5:i + 5 + 16]
            time = float(line[1:8].strip())
            puts[mid] = (time, time)
            total += 1
        elif 'completed PUT' in line:
            i = line.find('mid: ')
            mid = line[i + 5:i + 5 + 16]
            time = float(line[1:8].strip())
            puts[mid] = (puts[mid][0], time)
        elif 'redirecting' in line:
            i = line.find('mid: ')
            mid = line[i + 5:i + 5 + 16]
            redirects.append(mid)

    latencies = sorted(list(map(lambda t: t[1] - t[0], puts.values())))
    print(f'{len(puts)} puts (total: {total}, max: {latencies[-1]}, min: {latencies[0]})')
    print(f'redirects: {redirects}')
    print(f'median latency: {latencies[int(len(latencies) / 2)]}')


with open('output.txt', 'r') as f:
    measure_failure(f)

