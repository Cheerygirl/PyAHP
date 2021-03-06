
def makePath(AP, GTS, t = None, pics = False): #If t is not supplied, GTS
                                 #is the GTS. Else, it is the G-value.
    '''Takes an AP and GTS number and returns
    the Windows Path to the .dat file as a string.

    If t is supplied, GTS is taken as the G-value and t the T-value.
    A supplied t will create a path to the traverse (not into the Data) folder.
    
    If pics is True, return a path to the images directory instead.
    For IoO people.

    If both t and pics are specified, which should never happen, pics has precedence.'''

    base = 'AHPDATA/AP{0}/'.format(AP)
    G = GTS/100
    T = (GTS-G*100) / 10
    S = GTS%10
    
    if pics:
        return '{bases}FIT{0}/T{1}/SS{2}/Images/Raw'.format(G, T, S, bases = base)


    if t: #create directory for the traverse rather than for the specific
            #sample station
        return '{bases}FIT{0}/T{1}'.format(GTS, t, bases = base)
    
    #Eric's a bunny
    #Disguised as a human
    #ZOMG
    #kbtw teenie was here
    #AWWWOOOOOOOOOOOOO.

    #AP13 GTS 622 should be:
    #AHPDATA\AP13\FIT6\T2\Data\13-622.dat
    else:
        return r'{bases}FIT{1}/T{2}/Data/{3}-{4}.dat'.format(\
            AP, G, T, AP, GTS, bases = base)

def openFile(AP, GTS):
    '''Open the .dat file and split it.'''

    #About the .dat's:
    #Numbers are stored in the .dat's verbatim from the FDSs, up to column 25
    #for each line. Lines are separated as strings of 99 characters;
    #however, only about 29-30 of them are ever used.
    #split() cannot be used because it is not whitespace separating them,
    #it is chunks of 99 characters.
    #
    #f[0][2] would look for the character on the 0-th line, 2nd column.
    #Remember everything is zero-indexed!
    
    #Column 26 and onward stores ion and other info gathered from the PCEs
    #for lines =< 10 (I think?).
    #Unlike the other fields, a decimal point is already stored there.

    #AP8 creates difficulty because they are not consistent in their
    #encoding to the later APs. For AP9, the AP# is stored as
    #one digit instead of 2, breaking the 0th line (and possibly others).
    
    loc = makePath(AP, GTS)
    try:
        with open(loc, 'r') as fil:
            e = fil.read() #read the file into the variable e without splitting.
    except IOError: #If the file is not there
        print "AP{0}-{1} does not exist.".format(AP, GTS)
        return
    
    #It turns out that we can't use whitespace to separate the lines,
    #so we need to manually split them

    f = []

    ##The below could be heavily optimized.

    # Page 1
    f.append(e[:99].rstrip())
    f.append(e[99:198].rstrip())
    f.append(e[198:297].rstrip())
    f.append(e[297:396].rstrip())
    f.append(e[396:495].rstrip())
    f.append(e[495:594].rstrip())
    f.append(e[594:693].rstrip())
    f.append(e[693:792].rstrip())
    f.append(e[792:891].rstrip())
    f.append(e[891:990].rstrip())

    # Page 2
    f.append(e[990:1089].rstrip())
    f.append(e[1089:1188].rstrip())
    f.append(e[1188:1287].rstrip())
    f.append(e[1287:1386].rstrip())

    #etc, but I don't have support for the rest of page 2.

    ##The above needs to be heavily optimized.    
    
    return f

def existGTS(AP, GTS):
    '''Check if a GTS and its .dat file exists.

    Now deprecated (that was fast!) since openFile checks within the function.
    '''
    try:
        f = open(makePath(AP, GTS))
    except IOError:
        #print "AP{0}-{1} does not exist.".format(AP, GTS)
        return False
    f.close()
    return True
