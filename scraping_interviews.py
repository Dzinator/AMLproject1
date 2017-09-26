path = '/Users/sunyambagga/Desktop/Applied ML 551/Project 1/Interviews/'

with open(path+'Interview_OUTPUT.txt', 'a') as w:
    w.write('<dialog>\n')
    for k in range(1,7):
        with open(path+'i'+str(k)+'.txt', 'rb') as f:
            l = f.read()
            w.write('<s>')
            temp = l.splitlines()
            interview = []
            for line in temp:
                if line == '':
                    continue
                interview.append(line)
#            print interview
        
            for n,utt in enumerate(interview):
                
#                print n
#                print utt
                if n%2 == 0:
                    print "I'm here", utt
                    w.write('<utt uid="1">')
                    w.write(utt)
                    w.write('</utt>')
                else:
                    w.write('<utt uid="2">')
                    w.write(utt)
                    w.write('</utt>')
    
            w.write('</s>\n')
    w.write('</dialog>')
