#Jmeno Prijmeni: Daniel Cifka
#Osobni cislo: A23N0100P
#KKY/HDS -> 1.SP Foneticka transkripce

#Importovane knihovny jazyka python
import sys

#Konstanty specifikovane pro prepisova pravidla
V = ["a", "e", "i", "í", "y", "ý", "o", "ó", "u", "ú", "ů", "au", "eu", "ou"]
K = [ "b", "c", "d", "ď", "f", "g", "h", "ch", "j", "k", "l", "m", "n", "ň", "p", "q", "r", "ř", "0", "š", "t", "ť", "v", "w", "x", "z", "ž"]
ZPK = ["b", "d", "ď", "g", "v", "z", "ž", "h", "dz", "dž"]
NPK = ["p", "t", "ť", "k", "f", "s", "š", "ch", "c", "č",]
JK = ["m", "n", "ň", "l", "r", "j"]
NP = ["k", "s", "v", "z"]
Ě = ["b", "p", "v"]
Í = ["i", "í"]

#Funkce pro nacteni dat z textoveho souboru do seznamu
#Vstupnim parametrem je nazev souboru/cesta k souboru
def data_loader(file_name:str) -> list:
    
    f = open(file_name, "r", encoding="utf-8")
    
    return f.readlines()

#Predzpracovani textu
#Vstupem jsou nactene texty ze souboru
def preprocesing(lines:list) -> list:
    
    p_list = []
    
    for x in lines:
        
        x = x.lower() #Text preveden na mala pismena
        x = x.replace("\n","") #Odstraneni odradkovani
        x = x.replace("\ufeff", "") #Odstraneni pocatecni znacky textu
        x = x.replace(",", ", # ") #interpunkce nahrazeny #
        x = x.replace(".",". $") #Pocatky a konce vet nahrazeny za znacky |$|
        x = x.replace("?","? $") #Pocatky a konce vet nahrazeny za znacky |$|
        x = "$ " + x + "\n"
        p_list.append(x)
        
    return p_list

#Funkce pro kontrolu a prepis textu do foneticke podoby
#Vstupem je seznam predzpracovanych vet
def check_rulles(p_lines: list) -> list:
    
    sentence_f_l = [] #Seznam kam se vlozi poupravene vety
    
    for sentenc in p_lines:
        sentence_f = [None] * len(sentenc) #Tvorba seznamu ktery je stejne dlouhy jako je pocet pismen ve vete
        for i in range(len(sentenc)-2, -1, -1):
            
            #Pravidlo pro prepis 'ě' na fonetickou podobu 'je'
            if(sentenc[i] == "ě" and sentenc[i - 1] in Ě):
                sentence_f[i] = "je"
                
            #Pravidlo pro prepis 'd' na fonetickou podobu 'ď'
            elif(sentenc[i] == "d" and sentenc[i + 1] in Í):
                sentence_f[i] = "ď"
                
            #Pravidlo pro prepis 't' na fonetickou podobu 'ť'  
            elif(sentenc[i] == "t" and sentenc[i + 1] in Í):
                sentence_f[i] = "ť"
                
            #Pravidlo pro prepis 'n' na fonetickou podobu 'ň'
            elif(sentenc[i] == "n" and sentenc[i + 1] in Í):
                sentence_f[i] = "ň"
                
            #Pravidlo pro prepis 'd' na fonetickou podobu 'ď'
            elif(sentenc[i] == "d" and sentenc[i + 1] =="ě"):
                sentence_f[i] = "ď"
                
            #Pravidlo pro prepis 'ě' na fonetickou podobu 'e'
            elif(sentenc[i] == "ě" and sentenc[i - 1] =="d"):
                sentence_f[i] = "e"
                
            #Pravidlo pro prepis 't' na fonetickou podobu 'ť'
            elif(sentenc[i] == "t" and sentenc[i + 1] =="ě"):
                sentence_f[i] = "ť"
            
            #Pravidlo pro prepis 'ě' na fonetickou podobu 'e'    
            elif(sentenc[i] == "ě" and sentenc[i - 1] =="t"):
                sentence_f[i] = "e"
                
            #Pravidlo pro prepis 'n' na fonetickou podobu 'ň'
            elif(sentenc[i] == "n" and sentenc[i + 1] =="ě"):
                sentence_f[i] = "ň"
                
            #Pravidlo pro prepis 'ě' na fonetickou podobu 'e'
            elif(sentenc[i] == "ě" and sentenc[i - 1] =="n"):
                sentence_f[i] = "e"
                
            #Pravidlo pro prepis 'm' na fonetickou podobu 'mň'
            elif(sentenc[i] == "m" and sentenc[i + 1] =="ě"):
                sentence_f[i] = "mň"
            
            #Pravidlo pro prepis 'ě' na fonetickou podobu 'e'
            elif(sentenc[i] == "ě" and sentenc[i - 1] =="m"):
                sentence_f[i] = "e"
                
            #Prepis souhlasky dvou hlasky 'kd' na 'gd'
            elif(sentenc[i] == "k" and sentenc[i + 1] =="d"):
                sentence_f[i] = "g"
             #Prepis souhlasky "ř" na mluveny 'ř'
            elif(sentenc[i] == "ř" and sentenc[i - 1] in NPK):
                sentence_f[i] = "R"
            
            #Pravidlo pro presip neznele souhlasky na konci slova na neznelou souhlasku 
            elif(sentenc[i] in NPK and sentenc[i - 1] == "|"):
                sentence_f[i] = sentenc[i]
            
            #Ponechani pismene 'ch' nakonci slova
            elif(sentenc[i] == "c" and sentenc[i + 1] == "h" and sentenc[i + 2] == "|"):
                sentence_f[i] = "c"
            
            #Pokud jsou dve po sobe pismena 's' a 'h' se prepisuje na z
            elif(sentenc[i] == "s" and sentenc[i + 1] =="h"):
                sentence_f[i] = "z"
            
            #Pokud aktualni pismeno je 'v' a nasledujici pismeno je neznela parova souhlaska tak v prepisuji na 'f'
            elif(sentenc[i] == "v" and sentenc[i + 1] in NPK):
                sentence_f[i] = "f"
            #Prepis 'n' na 'ň' pokud jim predchazi pismena 'k' nebo 'g'
            elif(sentenc[i] == "n" and ((sentenc[i + 1] == "k") or (sentenc[i + 1] == "g"))):
                sentence_f[i] = "N"
            elif(sentenc[i] == "r" and ((sentenc[i + 1] in K) or (sentenc[i + 1] == "|")) and (sentenc[i - 1] in K)):
                sentence_f[i] = "P"
            elif(sentenc[i] == "l" and ((sentenc[i + 1] in K) or (sentenc[i + 1] == "|")) and (sentenc[i - 1] in K)):
                sentence_f[i] = "l"
            elif(sentenc[i] == "z" and ((sentenc[i + 1] == "-" and sentenc[i + 1] in JK) or (sentenc[i + 1] == "-" and sentenc[i + 1] == "v"))):
                sentence_f[i] = sentenc[i]
            elif(sentenc[i] == "k" and ((sentenc[i + 1] == "-" and sentenc[i + 1] in JK) or (sentenc[i + 1] == "-" and sentenc[i + 1] == "v"))):
                sentence_f[i] = sentenc[i]
            elif(sentenc[i] == "v" and ((sentenc[i + 1] == "-" and sentenc[i + 1] in JK) or (sentenc[i + 1] == "-" and sentenc[i + 1] == "v"))):
                sentence_f[i] = sentenc[i]
            elif(sentenc[i] == "s" and ((sentenc[i + 1] == "-" and sentenc[i + 1] in JK) or (sentenc[i + 1] == "-" and sentenc[i + 1] == "v"))):
                sentence_f[i] = sentenc[i]
                
            #Pravidlo pro presip znele souhlasky na neznelou souhlasku
            elif(sentenc[i] in ZPK and ((sentenc[i + 1] in NPK) or (sentenc[i + 1] == "-" and sentenc[i + 2] in NPK) or (sentenc[i + 1] == "|" and sentence_f[i + 2] in NPK) or (sentenc[i + 1] == "|" and sentence_f[i + 2] in JK) or (sentenc[i + 1] == "|" and sentence_f[i + 2] in V) or (sentenc[i + 1] == "|" and sentence_f[i + 2] == "?") or (sentenc[i + 1] == "|" and sentence_f[i + 2] == "#"))):
                for x in range(0, len(ZPK)):
                    if(sentenc[i] == ZPK[x]):
                        sentence_f[i] = NPK[x]
            
            #Pravidlo pro presip neznele souhlasky na znelou souhlasku
            elif(sentenc[i] in NPK and ((sentenc[i + 1] in ZPK) or (sentenc[i + 1] == "-" and sentenc[i + 2] in ZPK) or (sentenc[i + 1] == "|" and sentence_f[i + 2] in ZPK))):
                for x in range(0, len(NPK)):
                    if(sentenc[i] == NPK[x]):
                        sentence_f[i] = ZPK[x]
                        
                
            #Pokud je akutalni zvolene pismeno neparova souhlaska a nasleduje pismeno 'v' tak prepis stejnou neparovou souhlasku
            elif(sentenc[i] in NPK and ((sentenc[i + 1] == "v") or (sentenc[i + 1] == "-" and sentenc[i + 2] == "v") or (sentenc[i + 1] == "|" and sentenc[i + 2] == "v"))):
                for x in range(0, len(NPK)):
                    if(sentenc[i] == NPK[x]):
                        sentence_f[i] = NPK[x]
            
            #Pokud je akutalni zvolene pismeno parova souhlaska a nasleduje pauza a pismeno 'v' tak prepis na neparovou souhlasku
            elif(sentenc[i] in ZPK and (sentenc[i + 1] == "|" and sentenc[i + 2] == "v")):
                for x in range(0, len(ZPK)):
                    if(sentenc[i] == ZPK[x]):
                        sentence_f[i] = NPK[x]
            #Pokud je akutalni zvolene pismeno parova souhlaska a nasleduje jedinecna hlaska tak prepis na parovou souhlasku           
            elif(sentenc[i] in ZPK and (sentenc[i + 1] in JK)):
                for x in range(0, len(ZPK)):
                    if(sentenc[i] == ZPK[x]):
                        sentence_f[i] = ZPK[x]
            
        sentence_f_l.append(sentence_f)
        
    return sentence_f_l
        
def final_preprocesing_and_write(sentence_f_l: list, outputFile: str):      
    list_sentenc = []
    
        
    for i in range(0, len(sentence_f_l)):
        a=""
        for x in range(0, len(sentence_f_l[i])):
            if sentence_f_l[i][x] == None:
                a += p_lines[i][x]
            else:
                a += sentence_f_l[i][x]
        list_sentenc.append(a)
    
    f = open(outputFile, "a")
    
    for x in list_sentenc:
        x = x.replace("ý", "í")
        x = x.replace("y", "i")
        x = x.replace("ů", "ú")
        x = x.replace("í", "I")
        x = x.replace("é", "E")
        x = x.replace("á", "A")
        x = x.replace("ó", "O")
        x = x.replace("ú", "U")
        x = x.replace("š", "S")
        x = x.replace("ž", "Z")
        x = x.replace("ř", "R")
        x = x.replace("ť", "T")
        x = x.replace("ď", "D")
        x = x.replace("ň", "J")
        x = x.replace("č", "C")
        x = x.replace("ch", "x")
        
        x = x.replace("shora", "zhora")
        x = x.replace("shůry,", "zhůry")
        x = x.replace("shluk", "zhluk")
        
        f.write(x)


if __name__=='__main__':
    
    arguments = sys.argv
        
    lines = data_loader(arguments[2])
    p_lines = preprocesing(lines)
    sentence_f_l = check_rulles(p_lines)
    final_preprocesing_and_write(sentence_f_l, arguments[4])