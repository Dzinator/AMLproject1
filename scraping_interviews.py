path = '/Users/sunyambagga/Desktop/Applied ML 551/Project 1/Interviews/'

with open(path+'interview.xml', 'a') as w:
    w.write('<dialog>')
    for k in range(1,7):
        with open(path+'i'+str(k)+'.txt', 'rb') as f:
            l = f.read()
            temp = l.splitlines()
            interview = []
            for line in temp:
                if line == '':
                    continue
                interview.append(line)

        #     print interview
            
            w.write('\n<s>\n')
            for n,utt in enumerate(interview):
#                 print n
#                 print utt
                if n%2 == 0:
                    w.write('<utt uid="1">')
                    w.write(utt)
                    w.write('</utt>\n')
                else:
                    w.write('<utt uid="2">')
                    w.write(utt)
                    w.write('</utt>\n')
                if n != 0 and n%11 == 0:
                    w.write('</s>\n<s>\n')
            w.write('</s>\n')
    w.write('</dialog>')
