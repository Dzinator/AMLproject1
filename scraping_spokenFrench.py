path = '/Users/sunyambagga/Desktop/Applied ML 551/Project 1/SpokenFrench/'

with open(path+'spoken_french.xml', 'a') as w:
    w.write('<dialog>')
    for k in range(1,14):
        with open(path+'ex'+str(k)+'.txt', 'rb') as f:
            l = f.read()
            #     print l
            
            k = re.sub(r'\([^)]*\)', "", l)
            #     print k
            temp = k.splitlines()
            #     print temp
            example = []
            for line in temp:
                if line == '':
                    continue
                example.append(line)
            #     print "\n\n", example
            
            w.write('\n<s>\n')
            for n,utt in enumerate(example):
                #                 print n
                #                 print utt[3:]
                if n%2 == 0:
                    w.write('<utt uid="1">')
                    w.write(utt[3:])
                    w.write('</utt>\n')
                else:
                    w.write('<utt uid="2">')
                    w.write(utt[3:])
                    w.write('</utt>\n')
                if n != 0 and n%11 == 0:
                    w.write('</s>\n<s>\n')
    w.write('</s>\n')
w.write('</dialog>')
