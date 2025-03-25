import numpy as np
from typing import Callable

xi = np.exp(1j*2*np.pi/3)
xi2 = xi ** 2

def cycle_depuis_liste(liste : list) -> Callable[[int],int]:
    def sigma(i):
        if i in liste:
            indice = liste.index(i)
            if indice<len(liste) - 1:
                return liste[indice+1]
            else:
                return liste[0]
        else:
            return i
    return sigma

def cycle_inverse(sigma : Callable[[int],int]) -> Callable[[int],int]:
    def sigma_inverse(i):
        if sigma(i) == i:
            return i
        else:
            for j in range(1,9):
                if sigma(j) == i:
                    return j
    return sigma_inverse

def produit_cycle(cycle_1 : Callable[[int],int], cycle_2 : Callable[[int],int]) -> Callable[[int],int]:
    def cycle_produit(i):
        return cycle_1(cycle_2(i))

    return cycle_produit



def matrice(sigma : Callable[[int],int], orientation : list):
    matrice = np.zeros((8,8), dtype = complex)
    sigma_inverse = cycle_inverse(sigma)
    for i in range(0,8):
        j = sigma_inverse(i+1)-1
        matrice[i,j] = xi**orientation[j]
        
    return matrice

def visualiser_matrice(matrice):
    if np.shape(matrice) == (8,8):
        for i in range(8):
            string = ""
            for j in range(8):
                if matrice[i,j] == 0:
                    string += " ."
                if matrice[i,j] == 1:
                    string += " 0"
                elif matrice[i,j] == xi:
                    string += " 1"
                elif matrice[i,j] == xi2:
                    string += " 2"
            print(string)
    elif np.shape(matrice) == (8,):
        for i in range(8):
            if matrice[i] == 0:
                print(" 0")
            elif matrice[i] == 1:
                print(" 1")
            elif matrice[i] == xi:
                print(" xi")
            elif matrice[i] == xi2:
                print(" xi2")
            else:
                print(str(matrice[i]))
    print()
            

def matrice_mouvement_elementaire(X : str):
    if X == "R":
        sigma_X = sigma_R
        orientation_X = orientation_R
    elif X == "L":
        sigma_X = sigma_L
        orientation_X = orientation_L
    elif X == "U":
        sigma_X = sigma_U
        orientation_X = orientation_U
    elif X == "F":
        sigma_X = sigma_F
        orientation_X = orientation_F
    
    else:
        if X == "R'":
            matrice_X = matrice_depuis_algorithme("RRR")
        if X == "L'":
            matrice_X = matrice_depuis_algorithme("LLL")
        if X == "U'":
            matrice_X = matrice_depuis_algorithme("UUU")
        if X == "F'":
            matrice_X = matrice_depuis_algorithme("FFF")
            
        return matrice_X
    
    matrice_X = matrice(sigma_X, orientation_X)
    
    
    
    return matrice_X

def multiplication_matrices(matrice_1, matrice_2):
    matrice = np.zeros((8,8), dtype = complex)
    for j in range(8):
        for i in range(8):
            
            for k in range(8):
                if matrice_1[i,k] != 0 and matrice_2[k,j] != 0:
                    
                    if matrice_1[i,k] == 1 or matrice_2[k,j] == 1:
                        matrice[i,j] = matrice_1[i,k] if matrice_1[i,k] != 1 else matrice_2[k,j]
                        
                    elif matrice_1[i,k] == xi:
                        matrice[i,j] = xi2 if matrice_2[k,j] == xi else 1
                    
                    elif matrice_2[k,j] == xi:
                        matrice[i,j] = xi2 if matrice_1[i,k] == xi else 1
                    
                    elif matrice_1[i,k] == xi2:
                        matrice[i,j] = 1 if matrice_2[k,j] == xi else xi
                    
                    elif matrice_2[k,j] == xi2:
                        matrice[i,j] = 1 if matrice_1[i,k] == xi else xi
    
    return matrice

def multiplication_matrice_colonne(matrice, vecteur):
    vecteur_sortie = np.zeros((8,), dtype = complex)
    
    for i in range(8):
        for k in range(8):
            
            if matrice[i,k] !=0 and vecteur[k] != 0:
                vecteur_sortie[i] = matrice[i,k] * vecteur[k]
                break
    
    return vecteur_sortie
    
                        
                    


def matrice_depuis_algorithme(algorithme : str):
    matrice = np.identity(8)
    
    i = 0
    while i < len(algorithme):
        if i < len(algorithme)- 1 and algorithme[i+1] == "'":
            X = algorithme[i] + "'"
            i += 2
        else:
            X = algorithme[i]
            i += 1
        
        matrice_X = matrice_mouvement_elementaire(X)
        
        # matrice = np.matmul(matrice, matrice_X)
        matrice = multiplication_matrices(matrice, matrice_X)
        
    
    return matrice

def visualiser_polynome(coefficients):
    string = ""
    for num, coef in enumerate(coefficients):
        string += str(np.round(coef,3))
        if num != 0:
            string += "X" + str(num)
        string += " + "
    print(string)

def mouvement_inverse(X):
    if len(X) == 0:
        return ""
    elif len(X) == 1:
        return X + "'"
    else:
        if X[1] == "'":
            return mouvement_inverse(X[2:]) + X[:1]
        else:
            return mouvement_inverse(X[1:]) + X[0] + "'"

def commutateur(X_1,X_2):
    string = X_1 + X_2 + mouvement_inverse(X_1) + mouvement_inverse(X_2)
    return string


def changer_base(matrice, base : list):
    matrice_passage = np.zeros((8,8), dtype = complex)
    for j in range(8):
        matrice_passage[base[j]-1,j] = 1
    
    matrice_passage_inv = np.linalg.inv(matrice_passage)
    
    matrice = np.matmul(matrice, matrice_passage)
    matrice = np.matmul(matrice_passage_inv, matrice)
    
    return matrice

def decomposer_cycle_support_disjoint(cycle : Callable[[int], int]):
    liste_cycles_disjoints = []
    liste_listes_cycles = []
    
    support_cycle = [k for k in range(1,9) if cycle(k) != k]
    points_fixes_cycle = [k for k in range(1,9) if cycle(k) == k]
    
    liste_indice_a_traiter = [k for k in support_cycle]
    
    while liste_indice_a_traiter != []:
        liste_sous_cycle = [min(liste_indice_a_traiter)]
        
        liste_indice_a_traiter.remove(liste_sous_cycle[0])
        i = cycle(liste_sous_cycle[0])
        while i != liste_sous_cycle[0]:
            if i not in liste_sous_cycle:
                
                liste_sous_cycle.append(i)
                liste_indice_a_traiter.remove(i)
                
            i = cycle(i)
            
        liste_listes_cycles.append(liste_sous_cycle)
        sous_cycle = cycle_depuis_liste(liste_sous_cycle)
        liste_cycles_disjoints.append(sous_cycle)
    
    # if points_fixes_cycle != []:
    #     sous_cycle = lambda i : i
    #     liste_cycles_disjoints.append(sous_cycle)
    
    return liste_cycles_disjoints, liste_listes_cycles

def cycle_depuis_algorithme(algorithme):
    sigma = lambda k : k
    
    i = 0
    while i < len(algorithme):
        if i < len(algorithme)- 1 and algorithme[i+1] == "'":
            X = algorithme[i] + "'"
            i += 2
        else:
            X  = algorithme[i]
            i += 1
        
        if X == "R":
            sigma_X = sigma_R
        elif X == "L":
            sigma_X = sigma_L
        elif X == "U":
            sigma_X = sigma_U
        elif X == "F":
            sigma_X = sigma_F
        
        else:
            if X == "R'":
                sigma_X = cycle_inverse(sigma_R)
            if X == "L'":
                sigma_X = cycle_inverse(sigma_L)
            if X == "U'":
                sigma_X = cycle_inverse(sigma_U)
            if X == "F'":
                sigma_X = cycle_inverse(sigma_F)
        
        sigma = produit_cycle(sigma, sigma_X)
                
    return sigma



def matrice_permutation(sigma : Callable[[int],int]):
    matrice = np.zeros((8,8), dtype = complex)
    sigma_inverse = cycle_inverse(sigma)
    for i in range(0,8):
        j = sigma_inverse(i+1)-1
        matrice[i,j] = 1
        
    return matrice
        
    







sigma_R = cycle_depuis_liste([2,7,8,3])
orientation_R = [0,1,2,0,0,0,2,1]


sigma_L = cycle_depuis_liste([1,4,5,6])
orientation_L = [2,0,0,1,2,1,0,0]

sigma_U = cycle_depuis_liste([1,2,3,4])
orientation_U = [0,0,0,0,0,0,0,0]

sigma_F = cycle_depuis_liste([1,6,7,2])
orientation_F = [1,2,0,0,0,2,1,0]


# D = RRLLULLRR

# algorithme = "RUR'U'R'FRRU'R'U'RUR'F'"    # permutation de 2, 3. 15 mvts
# algorithme = commutateur("R","U") + "R'FRRU'R'" + commutateur("U'","R") + "F'"

# algorithme = "R'UR'UR'URU'RU'RU'"     # orientation de 2, 3

# algorithme = "R'UURUUR'FRUR'U'R'F'RRU'"     # 3 4

# algorithme = "RUR'U'R'FRRU'R'U'RUR'F'"  # 4R ; 4R' ; 2U ; 3U' ; 1F ; 1F' ; 2 3

# algorithme = "U'R'UURUUR'FRUR'U'R'F'RR"    # 6R ; 2R' ; 6U ; 1U' ; 1F ; 1F'

# relation : RRUUR'UURRUURRUUR'UURR
# relation : R'U'RU R URU'R' U'

# algorithme = "RUR'U'R'FRRU'R'U'RUR'F'FRUR'U'R'FRRU'R'U'RUR'F'F'"



# U'RFUF
algorithme = "RUR'U'R'FRRU'R'U'RUR'F'"


# algorithme = commutateur("RU","R")
print(algorithme)
print()

M = matrice_depuis_algorithme(algorithme)
# M = matrice_depuis_algorithme(com)
# M = matrice_depuis_algorithme("R'UR'UR'URU'RU'RU'")     # orientation de 2, 3
# M = matrice_depuis_algorithme("U")

visualiser_matrice(M)
print()

cycle_algorithme = cycle_depuis_algorithme(algorithme)
sigma_RURRRUUU = produit_cycle(produit_cycle(sigma_R,sigma_U),produit_cycle(cycle_inverse(sigma_R),cycle_inverse(sigma_U)))
liste_cycles, liste_listes_cycles = decomposer_cycle_support_disjoint(cycle_algorithme)

# print(liste_listes_cycles)

matrice_chgmt = changer_base(M, [2,7,3,4,1,5,6,8])

base = []
for cycle_liste in liste_listes_cycles :
    base += cycle_liste
for i in range(1,9):
    if i not in base:
        base.append(i)


matrice_chgmt = changer_base(M, base)
visualiser_matrice(matrice_chgmt)
# print()


X = np.array([0,0,0,0,0,1,0,0])
MX = multiplication_matrice_colonne(M, X)
# visualiser_matrice(MX)




PMX = multiplication_matrice_colonne(matrice_permutation(cycle_inverse(cycle_algorithme)) ,MX)

# visualiser_matrice(PMX)






## VALEURS, VECTEURS PROPRES ##

# # np.set_printoptions(precision=1)
# # np.set_printoptions(suppress=True)

# PRINT=np.linalg.eig(M)

# for j,X in enumerate(PRINT[1]):
#     print('lambda',PRINT[0][j])
#     for i in X:
#         print(i)
#     print()



    

# visualiser_polynome(np.poly(PRINT[1]))