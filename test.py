
with open('output.txt', 'r') as file:
    requests = []
    responses = []
    gets = []
    failed = []

    for line in file.readlines():
        if 'executing PUT' in line:
            i = line.find('mid: ')
            requests.append(line[i + 5:i + 5 + 16])
        elif 'completed PUT' in line:
            i = line.find('mid: ')
            responses.append(line[i + 5:i + 5 + 16])
        elif 'executing GET' in line:
            i = line.find('mid: ')
            gets.append(line[i + 5:i + 5 + 16])
        elif 'can\'t find value' in line:
            i = line.find('mid: ')
            failed.append(line[i + 5:i + 5 + 16])

    print(f'PUTS: {len(requests)} requests, {len(responses)} responses')
    print(f'GETS: {len(gets)}, requests, {len(failed)} failures')
    print(f'failed puts {set(requests).difference(set(responses))}')
    print(f'failed gets {failed}')

    for mid in responses:
        if len(list(filter(lambda m: mid == m, responses))) > 1:
            print(f'repeat PUT response: {mid}')

    for mid in gets:
        if len(list(filter(lambda m: mid == m, gets))) > 1:
            print(f'repeat GET response: {mid}')
