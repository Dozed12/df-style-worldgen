import libtcodpy as libtcod
import math
import time
from random import randint
from random import uniform

WORLD_WIDTH = 65
WORLD_HEIGHT = 65

SCREEN_WIDTH = 65
SCREEN_HEIGHT = 65

INITIAL_CIVS = 1
CIV_MAX_SITES = 10
MAX_SITE_POP = 20000

###################################################################################### - Classes - ######################################################################################

class Tile:

    def __init__(self, height,temp,precip, biome):
        self.temp = temp
        self.height = height
        self.precip = precip
        self.biome = biome

    hasRiver = False
    isCiv = False

    biomeID = 0

class Race:
      
    def __init__(self,Name,PrefBiome,Strenght,Size,ReproductionSpeed):
        self.Name = Name
        self.PrefBiome = PrefBiome
        self.Strenght = Strenght
        self.Size = Size
        self.ReproductionSpeed = ReproductionSpeed

class CivSite:

    def __init__(self,x,y,category,suitable,popcap):
        self.x = x
        self.y = y
        self.category = category
        self.suitable = suitable
        self.popcap = popcap

    Population = 0

class Civ:

    def __init__(self,Race,Name,Agression,Type,Color):
        self.Name = Name
        self.Race = Race
        self.Agression = Agression
        self.Type = Type
        self.Color = Color

    Sites = []
    SuitableSites = []

##################################################################################### - Functions - #####################################################################################

# - General Functions -

def ClearConsole():
    
    for x in xrange(SCREEN_WIDTH):
        for y in xrange(SCREEN_HEIGHT):
            libtcod.console_put_char_ex( 0, x, y, ' ', libtcod.black, libtcod.black)

    libtcod.console_flush()

    return

def PointDistRound(pt1x, pt1y, pt2x, pt2y):

    distance = abs(pt2x - pt1x) + abs(pt2y - pt1y);

    distance = round(distance)

    return distance

def LowestNeighbour(X,Y,hm):   #Diagonals are commented for rivers

    minval = 5

    x = 0
    y = 0

    if libtcod.heightmap_get_value(hm, X + 1, Y) < minval and X + 1 < WORLD_WIDTH:
        minval = libtcod.heightmap_get_value(hm, X + 1, Y)
        x = X + 1
        y = Y

    if libtcod.heightmap_get_value(hm, X, Y + 1) < minval and Y + 1 < WORLD_HEIGHT:
        minval = libtcod.heightmap_get_value(hm, X, Y + 1)
        x = X
        y = Y + 1

    #if libtcod.heightmap_get_value(hm, X + 1, Y + 1) < minval and X + 1 < WORLD_WIDTH and Y + 1 < WORLD_HEIGHT and minval > 0.2:
        #minval = libtcod.heightmap_get_value(hm, X + 1, Y + 1)
        #x = X + 1
        #y = Y + 1

    #if libtcod.heightmap_get_value(hm, X - 1, Y - 1) < minval and X - 1 > 0 and Y - 1 > 0 and minval > 0.2:
        #minval = libtcod.heightmap_get_value(hm, X - 1, Y - 1)
        #x = X - 1
        #y = Y - 1

    if libtcod.heightmap_get_value(hm, X - 1, Y) < minval and X - 1 > 0:
        minval = libtcod.heightmap_get_value(hm, X - 1, Y)
        x = X - 1
        y = Y

    if libtcod.heightmap_get_value(hm, X, Y - 1) < minval and Y - 1 > 0:
        minval = libtcod.heightmap_get_value(hm, X, Y - 1)
        x = X
        y = Y - 1

    #f libtcod.heightmap_get_value(hm, X + 1, Y - 1) < minval and X + 1 < WORLD_WIDTH and Y - 1 > 0 and minval > 0.2:
        #minval = libtcod.heightmap_get_value(hm, X + 1, Y - 1)
        #x = X + 1
        #y = Y - 1

    #if libtcod.heightmap_get_value(hm, X - 1, Y + 1) < minval and X - 1 > 0 and Y + 1 < WORLD_HEIGHT and minval > 0.2 :
        #minval = libtcod.heightmap_get_value(hm, X - 1, Y + 1)
        #x = X - 1
        #y = Y + 1

    return (x,y)

# - MapGen Functions -

def PoleGen(hm, NS):

    if NS == 0:
        rng = randint(0,4)
        for i in range(WORLD_WIDTH):      
                for j in range(rng):
                    libtcod.heightmap_set_value(hm, i, WORLD_HEIGHT - 1 - j , 0.31)
                rng += randint(1,3)-2
                if rng > 4:
                    rng = 3
                if rng < 1:
                    rng = 1

    if NS == 1:
        rng = randint(0,4)
        for i in range(WORLD_WIDTH):      
                for j in range(rng):
                    libtcod.heightmap_set_value(hm, i, j , 0.31)
                rng += randint(1,3)-2
                if rng > 4:
                    rng = 3
                if rng < 1:
                    rng = 1

    return

def TectonicGen(hm, hor):

    TecTiles = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

    #Define Tectonic Borders
    if hor == 1:
        pos = randint(WORLD_HEIGHT/10,WORLD_HEIGHT - WORLD_HEIGHT/10)
        for x in range(WORLD_WIDTH):
                TecTiles[x][pos] = 1                  
                pos += randint(1,5)-3
                if pos < 0:
                    pos = 0            
                if pos > WORLD_HEIGHT-1:
                    pos = WORLD_HEIGHT-1            
    if hor == 0:
        pos = randint(WORLD_WIDTH/10,WORLD_WIDTH - WORLD_WIDTH/10)
        for y in range(WORLD_HEIGHT):
                TecTiles[pos][y] = 1
                pos += randint(1,5)-3
                if pos < 0:
                    pos = 0
                if pos > WORLD_WIDTH-1:
                    pos = WORLD_WIDTH-1           
                  
    #Apply elevation to borders
    for x in xrange(WORLD_WIDTH/10,WORLD_WIDTH - WORLD_WIDTH/10):
        for y in xrange(WORLD_HEIGHT/10,WORLD_HEIGHT - WORLD_HEIGHT/10):
                if TecTiles[x][y] == 1 and libtcod.heightmap_get_value(hm, x, y) > 0.25:
                    libtcod.heightmap_add_hill(hm, x, y, randint(2,4), uniform(0.15,0.18))                        

    return

def Temperature(temp,hm):

    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
                heighteffect = 0
                if y > WORLD_HEIGHT/2:
                    libtcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT-y-heighteffect)
                else:
                    libtcod.heightmap_set_value(temp, x, y, y-heighteffect)
                heighteffect = libtcod.heightmap_get_value(hm, x, y)
                if heighteffect > 0.8:
                    heighteffect = heighteffect * 5
                    if y > WORLD_HEIGHT/2:
                        libtcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT-y-heighteffect)
                    else:
                        libtcod.heightmap_set_value(temp, x, y, y-heighteffect)
                if heighteffect < 0.25:
                    heighteffect = heighteffect * 10
                    if y > WORLD_HEIGHT/2:
                        libtcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT-y-heighteffect)
                    else:
                        libtcod.heightmap_set_value(temp, x, y, y-heighteffect)                       

    return

def Percipitaion(preciphm):

    libtcod.heightmap_add(preciphm, 2)

    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
                if y > WORLD_HEIGHT/2 - WORLD_HEIGHT/10 and y < WORLD_HEIGHT/2 + WORLD_HEIGHT/10:
                    val = y
                    val = abs(y - WORLD_HEIGHT/2)
                    libtcod.heightmap_set_value(preciphm, x, y, val/4)
                        
    precip = libtcod.noise_new(2,libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)

    libtcod.heightmap_add_fbm(preciphm,precip ,8, 8, 0, 0, 32, 1, 1)

    libtcod.heightmap_normalize(preciphm, 0.0, 1.0)                       

    return

def RiverGen(hm, World):

    X = randint(0,WORLD_WIDTH-1)                       
    Y = randint(0,WORLD_HEIGHT-1)

    while libtcod.heightmap_get_value(hm, X, Y) <= 0.8:
        X = randint(0,WORLD_WIDTH-1)                       
        Y = randint(0,WORLD_HEIGHT-1)

    XCoor = [0 for x in range(50)]
    YCoor = [0 for x in range(50)]
      
    XCoor[0] = X
    YCoor[0] = Y

    for x in range(1,50):

        XCoor[x],YCoor[x] = LowestNeighbour(X,Y,hm)          
            
        X = XCoor[x]
        Y = YCoor[x]

        if libtcod.heightmap_get_value(hm, X, Y) < 0.2:
            break

    for x in range(50):
        World[XCoor[x]][YCoor[x]].hasRiver = True

    return

def MasterWorldGen():    #------------------------------------------------------- * MASTER GEN * -------------------------------------------------------------

    print ' * World Gen START * '
    starttime = time.time()

    #Heightmap
    hm = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(50):
        libtcod.heightmap_add_hill(hm, randint(WORLD_WIDTH/10,WORLD_WIDTH- WORLD_WIDTH/10), randint(WORLD_HEIGHT/10,WORLD_HEIGHT- WORLD_HEIGHT/10), randint(12,16), randint(6,10))
    print '- Main Hills -'

    for i in range(200):
        libtcod.heightmap_add_hill(hm, randint(WORLD_WIDTH/10,WORLD_WIDTH- WORLD_WIDTH/10), randint(WORLD_HEIGHT/10,WORLD_HEIGHT- WORLD_HEIGHT/10), randint(2,4), randint(6,10))
    print '- Small Hills -'

    libtcod.heightmap_normalize(hm, 0.0, 1.0)

    noisehm = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    noise2d = libtcod.noise_new(2,libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
    libtcod.heightmap_add_fbm(noisehm, noise2d,4, 4, 0, 0, 64, 1, 1)
    libtcod.heightmap_normalize(noisehm, 0.0, 1.0)
    libtcod.heightmap_multiply_hm(hm, noisehm, hm)
    print '- Apply Simplex -'

    PoleGen(hm, 0)
    print '- South Pole -'

    PoleGen(hm, 1)
    print '- North Pole -'

    TectonicGen(hm,0)
    TectonicGen(hm,1)
    print '- Tectonic Gen -'

    libtcod.heightmap_rain_erosion(hm, WORLD_WIDTH*WORLD_HEIGHT ,0.07,0,0)
    print '- Erosion -'

    libtcod.heightmap_clamp(hm, 0.0, 1.0)
      
    #Temperature
    temp = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)   
    Temperature(temp,hm)
    libtcod.heightmap_normalize(temp, 0.0, 0.8)
    print '- Temperature Calculation -'     

    #Precipitation

    preciphm = libtcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    Percipitaion(preciphm)
    libtcod.heightmap_normalize(preciphm, 0.0, 0.8)
    print '- Percipitaion Calculation -'  
      
    # VOLCANISM - RARE AT SEA FOR NEW ISLANDS (?) RARE AT MOUNTAINS > 0.9 (?) RARE AT TECTONIC BORDERS (?)

    #Initialize Tiles with Map values
    World = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)] #100x100 array
    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
                World[x][y] = Tile(libtcod.heightmap_get_value(hm, x, y),
                                    libtcod.heightmap_get_value(temp, x, y),
                                    libtcod.heightmap_get_value(preciphm, x, y),
                                    0)      

    print '- Tiles Initialized -'

    # - Biome info to Tiles -

    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
            
            if World[x][y].height > 0.2:
                World[x][y].biomeID = 3
                if randint(1,10) < 3:
                    World[x][y].biomeID = 5
            if World[x][y].height > 0.4:
                World[x][y].biomeID = 14
                if randint(1,10) < 3:
                    World[x][y].biomeID = 5
            if World[x][y].height > 0.5:
                World[x][y].biomeID = 8
                if randint(1,10) < 3:
                    World[x][y].biomeID = 14

            if World[x][y].temp <= 0.5 and World[x][y].precip >= 0.5:
                World[x][y].biomeID = 5
                if randint(1,10) < 3:
                    World[x][y].biomeID = 14
            if World[x][y].temp >= 0.5 and World[x][y].precip >= 0.7:
                World[x][y].biomeID = 6

            if World[x][y].precip >= 0.7 and World[x][y].height > 0.2 and World[x][y].height <= 0.4:
                World[x][y].biomeID = 2

            if World[x][y].temp > 0.75 and World[x][y].precip < 0.35:
                World[x][y].biomeID = 4

            if World[x][y].temp <= 0.22 and World[x][y].height > 0.2:
                World[x][y].biomeID = randint(11,13)
            if World[x][y].temp <= 0.3 and World[x][y].temp > 0.2 and World[x][y].height > 0.2 and World[x][y].precip >= 0.6:
                World[x][y].biomeID = 7
                  
            if World[x][y].height > 0.75:
                World[x][y].biomeID = 9
            if World[x][y].height > 0.999:
                World[x][y].biomeID = 10                  
            if World[x][y].height <= 0.2:
                World[x][y].biomeID = 0
            if World[x][y].height <= 0.1:
                World[x][y].biomeID = 0                  

    print '- BiomeIDs Atributed -'
      
    #River Gen
      
    for x in range(2):
        RiverGen(hm, World)
    print '- River Gen -'

    #Free Heightmaps
    libtcod.heightmap_delete(hm)
    libtcod.heightmap_delete(temp)
    libtcod.heightmap_delete(noisehm)                       

    elapsed_time = time.time() - starttime
    print ' * World Gen DONE *    in: ',elapsed_time,' seconds'

    return World

def ReadRaces():

    RacesFile = 'Races.txt'

    NRaces = sum(1 for line in open('Races.txt'))

    f = open(RacesFile)

    Races = [0 for x in range(NRaces)]

    for x in range(NRaces):
        data = f.readline().split(',')
        Races[x] = Race(data[0],int(data[1]),int(data[2]),int(data[3]),int(data[4]))      

    f.close()

    print '- Races Read -'

    return NRaces, Races

def CivGen(Races): #-------------------------------------------------------------------- * CIV GEN * ----------------------------------------------------------------------------------

    Civs = [0 for x in range(INITIAL_CIVS)]

    for x in range(INITIAL_CIVS):

        libtcod.namegen_parse('namegen/jice_fantasy.cfg')
        Name = libtcod.namegen_generate('Fantasy male')
        libtcod.namegen_destroy ()

        Name += "Empire"

        Race = Races[randint(0,NRaces-1)]

        Agression = randint(1,4)

        Type = randint(1,1)

        Color = libtcod.Color(randint(0,255),randint(0,255),randint(0,255))
      
        #Initialize Civ
        Civs[x] = Civ(Race,Name,Agression,Type,Color)

    print '- Civs Generated -'

    return Civs

def SetupCivs(Civs, World, Chars, Colors):

    for x in range(INITIAL_CIVS):

        for i in range(WORLD_WIDTH):
            for j in range (WORLD_HEIGHT):
                if World[i][j].biomeID == Civs[x].Race.PrefBiome:
                    Civs[x].SuitableSites.append(CivSite(i,j,"",1,0))
            
        rand = randint(0,len(Civs[x].SuitableSites)-1)

        X = Civ.SuitableSites[rand].x
        Y = Civ.SuitableSites[rand].y

        World[X][Y].isCiv = True

        del Civs[x].Sites[:]
        PopCap = 3 * Civs[x].Race.ReproductionSpeed + randint (1,100) #Random Site Max Pop
        Civs[x].Sites.append ( CivSite(X,Y,"Village",0,PopCap) )
        Civs[x].Sites[0].Population = 20

        Chars[X][Y] = 31
        Colors[X][Y] = Civs[x].Color

    print '- Civs Setup -'

    print ' * Civ Gen DONE *'

    return

##################################################################################### - PROCESS CIVS - ##################################################################################

def NewSite(Civ, Origin, World,Chars,Colors):

    rand = randint(0,len(Civ.SuitableSites)-1)

    while PointDistRound(Origin.x, Origin.y, Civ.SuitableSites[rand].x, Civ.SuitableSites[rand].y) > 10 or World[Civ.SuitableSites[rand].x][Civ.SuitableSites[rand].y].isCiv:
        rand = randint(0,len(Civ.SuitableSites)-1)

    X = Civ.SuitableSites[rand].x
    Y = Civ.SuitableSites[rand].y

    World[X][Y].isCiv = True
    PopCap = 3 * Civ.Race.ReproductionSpeed + randint (1,100) #Random Site Max Pop
    Civ.Sites.append ( CivSite(X,Y,"Village",0,PopCap) )
    Civ.Sites[len(Civ.Sites)-1].Population = 20
    Civ.Sites[len(Civ.Sites)-1].Prosperity = Civ.Sites[len(Civ.Sites)-1].Population * 0.25

    Chars[X][Y] = 31
    Colors[X][Y] = Civ.Color

    return

def ProcessCivs(World,Civs,Chars,Colors,Month):

    for x in range(INITIAL_CIVS):

        #GAINS
        for y in range(len(Civs[x].Sites)):

            #Population
            NewPop = Civs[x].Sites[y].Population * Civs[x].Race.ReproductionSpeed/1500

            if Civs[x].Sites[y].Population > Civs[x].Sites[y].popcap / 2:
                NewPop /= 4                                
            
            Civs[x].Sites[y].Population += NewPop

            if Civs[x].Sites[y].Population > Civs[x].Sites[y].popcap:
                #TESTING
                Civs[x].Sites[y].Population = Civs[x].Sites[y].popcap / 2                
                NewSite(Civs[x],Civs[x].Sites[y],World,Chars,Colors)

            print Civs[x].Sites[y].Population

    return

####################################################################################### - MAP MODES - ####################################################################################

# --------------------------------------------------------------------------------- Print Map (Terrain) --------------------------------------------------------------------------------

def TerrainMap(World):  
    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):          
            hm_v = World[x][y].height
            libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '0' , libtcod.blue, libtcod.black)
            if hm_v > 0.1:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '1', libtcod.blue, libtcod.black)
            if hm_v > 0.2:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '2', Palette[0], libtcod.black)
            if hm_v > 0.3:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '3', Palette[0], libtcod.black)
            if hm_v > 0.4:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '4', Palette[0], libtcod.black)
            if hm_v > 0.5:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '5', Palette[0], libtcod.black)
            if hm_v > 0.6:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '6', Palette[0], libtcod.black)
            if hm_v > 0.7:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '7', Palette[0], libtcod.black)
            if hm_v > 0.8:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '8', libtcod.dark_sepia, libtcod.black)
            if hm_v > 0.9:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '9', libtcod.light_gray, libtcod.black)
            if hm_v > 0.99:
                libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '^', libtcod.darker_gray, libtcod.black)                    
    libtcod.console_flush()
    return

def BiomeMap(Chars,Colors):

    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
            libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, Chars[x][y] , Colors[x][y], libtcod.black)
                                                   
    libtcod.console_flush()
    return

def HeightGradMap(World):  # ------------------------------------------------------------ Print Map (Heightmap Gradient) -------------------------------------------------------------------
    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):          
            hm_v = World[x][y].height
            HeightColor = libtcod.Color(255,255,255)
            libtcod.color_set_hsv(HeightColor,0,0,hm_v ) #Set lightness to hm_v so higher heightmap value -> "whiter"
            libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '\333' , HeightColor, libtcod.black)
    libtcod.console_flush()
    return

def TempGradMap(World):  # ------------------------------------------------------------ Print Map (Surface Temperature Gradient) white -> cold red -> warm --------------------------------
    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
            tempv = World[x][y].temp
            tempcolor = libtcod.color_lerp ( libtcod.white, libtcod.red,tempv)
            libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '\333' , tempcolor, libtcod.black)
    libtcod.console_flush()
    return

def PrecipGradMap(World):  # ------------------------------------------------------------ Print Map (Surface Temperature Gradient) white -> cold red -> warm --------------------------------
    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
            tempv = World[x][y].precip
            tempcolor = libtcod.color_lerp ( libtcod.white, libtcod.light_blue,tempv)
            libtcod.console_put_char_ex( 0, x, y + SCREEN_HEIGHT/2 - WORLD_HEIGHT/2, '\333' , tempcolor, libtcod.black)
    libtcod.console_flush()
    return

def NormalMap(World):  # ------------------------------------------------------------ Normal Map (Biome + Entities) --------------------------------

    Chars = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
    Colors = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]

    def SymbolDictionary(x):
        return {
            0: '\367',
            1: '\367',
            2: 'n',
            3: 'u',
            4: 'n',
            5: 6-randint(0,1),
            6: 6-randint(0,1),
            7: 6-randint(0,1),
            8: 139,
            9: 127,
            10: 30,
            11: 176,
            12: 177,
            13: 178,
            14: 'n'
        }[x]

    def ColorDictionary(x):
        marshcolor = libtcod.Color(71,114,75)
        icecolor = libtcod.Color(7,125,126)
        return {
            0: libtcod.dark_blue,
            1: libtcod.light_blue,
            2: marshcolor,
            3: libtcod.dark_green,
            4: libtcod.dark_yellow,
            5: libtcod.dark_green,
            6: libtcod.darker_green,
            7: icecolor,
            8: libtcod.dark_green,
            9: libtcod.light_grey,
            10: libtcod.grey,
            11: icecolor,
            12: icecolor,
            13: icecolor,
            14: libtcod.dark_green
        }[x]

    World[0][0].hasRiver = False #Fixes unknown bug
      
    for x in xrange(WORLD_WIDTH):
        for y in xrange(WORLD_HEIGHT):
            Chars[x][y] = SymbolDictionary(World[x][y].biomeID)
            Colors[x][y] = ColorDictionary(World[x][y].biomeID)
            if World[x][y].hasRiver == True:
                Chars[x][y] = 'o'
                Colors[x][y] = libtcod.dark_cyan

    return Chars, Colors

###################################################################################### - Startup - ######################################################################################
      
#Start Console and set costum font
libtcod.console_set_custom_font("Andux_cp866ish.png", libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'pyWorld', False, libtcod.RENDERER_SDL) #Set True for Fullscreen

#Palette
Palette = [libtcod.Color(20,150,30), #Green
           ]

libtcod.sys_set_fps(30)
libtcod.console_set_fullscreen(False)

################################################################################# - Main Cycle / Input - ##################################################################################

isRunning = False

#World Gen
World = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
World = MasterWorldGen()

#Normal Map Initialization
Chars, Colors = NormalMap(World)

#Read Races
NRaces, Races = ReadRaces()

#Civ Gen
Civs = [0 for x in range(INITIAL_CIVS)]
Civs = CivGen(Races)

#Setup Civs
SetupCivs(Civs, World, Chars, Colors)

#Month 0
Month=0

#Select Map Mode
while not libtcod.console_is_window_closed():

    #Simulation
    while isRunning == True:

        ProcessCivs(World,Civs,Chars,Colors,Month)            
            
        #DEBUG Print Mounth
        Month+=1
        print 'Month: ',Month

        #End Simulation
        libtcod.console_check_for_keypress(True)
        if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
            timer = 0
            isRunning = False
            print "*PAUSED*"
            time.sleep(1)

        #Flush Console
        BiomeMap(Chars,Colors)
        libtcod.console_flush()
      
    key = libtcod.console_check_for_keypress(True)

    #Start Simulation
    if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        isRunning = True
        print "*RUNNING*"
        time.sleep(1)     
      
    if key.vk == libtcod.KEY_CHAR:
        if key.c == ord('t'):
            TerrainMap(World)
        elif key.c == ord('h'):
            HeightGradMap(World)
        elif key.c == ord('w'):
            TempGradMap(World)
        elif key.c == ord('p'):
            PrecipGradMap(World)
        elif key.c == ord('b'):
            BiomeMap(Chars,Colors)
        elif key.c == ord('r'):
            print "\n" * 100
            World = MasterWorldGen()
            NRaces, Races = ReadRaces()
            Civs = CivGen(Races)
            Chars, Colors = NormalMap(World)
            SetupCivs(Civs, World, Chars, Colors)            
            ClearConsole()






      
            
        





























































