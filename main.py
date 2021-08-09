#!/bin/env python3
from os import path, remove
import random


def tabloya_yaz(table_list, collect, broken, last_player):
    data = '\n' + last_player[0] + ':'

    for den in range(len(table_list)):
        if table_list[den] != 0:
            data += str(den) + '-' + table_list[den] + ':'

    brok = str(broken[0]) + '-bx:'
    data += brok
    brok = str(broken[1]) + '-by:'
    data += brok

    coll = str(collect[0]) + '-cx:'
    data += coll
    coll = str(collect[1]) + '-cy'
    data += coll

    table_file = open('Table.dat', 'a')
    table_file.write(data)
    table_file.close()


def tablodan_oku(table_list, collect, broken, last_player):
    data = open('Table.dat', 'r')
    last_state_list = data.readlines()[-1].split(':  ')
    # First State -> x:0-2x:5-5y:7-3y:11-5x:12-5y:16-3x:18-5x:23-2y:0-bx:0-by:0-cx:0-cy
    #                son_oynayan:tablo_durumu:kirilan_x:kirilan_y:toplanan_x:toplanan_y

    for den in range(24):
        table_list.append(0)
    for state in last_state_list[1:-4]:
        table_list[int(state.split('-')[0])] = state.split('-')[1]

    collect.append(int(last_state_list[-2].split('-')[0]))
    collect.append(int(last_state_list[-1].split('-')[0]))

    broken.append(int(last_state_list[-4].split('-')[0]))
    broken.append(int(last_state_list[-3].split('-')[0]))

    last_player.append(last_state_list[0])
    
    data.close()


def zar_yaz(last_player, zar_durumu):
    if type(zar_durumu) == type(1):
        dice = open('Dice.dat', 'a')
        dice.write('\n' + str(zar_durumu))
        dice.close()
        return

    dice = open('Dice.dat', 'a')
    if last_player[0] == 'y':
        data = '\ny ' + str(zar_durumu[0]) + ' ' + str(zar_durumu[1])
    else:
        data = '\nx ' + str(zar_durumu[0]) + ' ' + str(zar_durumu[1])
    dice.write(data)
    dice.close()


def yeni_oyun(table_list, collect, broken, last_player):
    for den in range(24):
        table_list.append(0)
    table_list[0] = '2x'
    table_list[5] = '5y'
    table_list[7] = '3y'
    table_list[11] = '5x'
    table_list[12] = '5y'
    table_list[16] = '3x'
    table_list[18] = '5x'
    table_list[23] = '2y'

    collect.append(0)
    collect.append(0)

    broken.append(0)
    broken.append(0)

    last_player.append('y')

    if path.exists('Table.dat'):
        remove('Table.dat')
    tabloya_yaz(table_list, collect, broken, last_player)

    if path.exists('Dice.dat'):
        remove('Dice.dat')
        dice = open('Dice.dat', 'x')
        dice.close()

    for den in range(1000):
        x = zar_atma()
        y = zar_atma()
        print("x'in attigi zar: {}".format(x))
        print("y'in attigi zar: {}".format(y))
        if x != y:
            if x > y:
                last_player[0] = 'y'
            else:
                last_player[0] = 'x'

            zar_yaz(last_player, x)
            zar_yaz(last_player, y)
            break
        else:
            print('x ve y ayni sayiyi attigi icin tekrardan zarlar atiliyor.')


def zar_atma():
    return random.randint(1,6)


def tabloyu_goster(table_list, collect, broken):
    print()
    for den in table_list[12:24]:
        print('%4s' % den, end='')
    print('\n\n         Toplanan X: {}    Toplanan Y: {}'.format(collect[0], collect[1]))
    print('         Kirilan  X: {}    Kirilan  Y: {}'.format(collect[0], collect[1]))
    print()
    for den in table_list[11:0:-1]:
        print('%4s' % den, end='')
    print('%4s' % table_list[0], end='')
    print()
    print()


def collect_control(table_list, current_player, broken):
    if current_player == 'x':
        if broken[0] > 0:
            return False
    if current_player == 'y':
        if broken[1] > 0:
            return False

    if current_player == 'x':
        for den in range(18):
            if 'x' in str(table_list[den]):
                return False
        return True
    if current_player == 'y':
        for den in range(6,24):
            if 'x' in str(table_list[den]):
                return False
        return True

    return False


def unique(liste):
    uniq_list = []
    for x in liste:
        if x not in uniq_list:
            uniq_list.append(x)

    return uniq_list


def hareket_yeri(table_list, current_player, zar, broken, collect, last_choice):
    kaynak_listesi = []
    kaynak_temp = []
    gidilecek_yer = ''

    if current_player == 'X':
        cur = 'x'
    else:
        cur = 'y'
    
    for den in range(len(table_list)):
        if cur in str(table_list[den]):
            kaynak_temp.append(den)

    for den in kaynak_temp:
        if cur == 'x':
            coll = collect_control(table_list, cur, broken)
            if coll:
                if den+zar > 23:
                    kaynak_listesi.append(den)
                    continue
            else:
                if den+zar > 23:
                    continue
            if table_list[den+zar] == 0:
                kaynak_listesi.append(den)
            if 'x' in str(table_list[den+zar]):
                kaynak_listesi.append(den)
            if 'y' in str(table_list[den+zar]):
                if table_list[den+zar][:-1] == '1':
                    kaynak_listesi.append(den)
        if cur == 'y':
            coll = collect_control(table_list, cur, broken)
            if coll:
                if den-zar < 0:
                    kaynak_listesi.append(den)
                    continue
            else:
                if den-zar < 0:
                    continue
            if table_list[den-zar] == 0:
                kaynak_listesi.append(den)
            if 'y' in str(table_list[den-zar]):
                kaynak_listesi.append(den)
            if '1x' in str(table_list[den-zar]):
                if table_list[den-zar][:-1] == '1':
                    kaynak_listesi.append(den)
    
    kaynak_listesi = unique(kaynak_listesi)

    if current_player == 'X':
        if broken[0] > 0:
            # 0-5 arasi kontrol edilecek
            if table_list[zar-1] == 0:
                secim_kaynak = -1
                gidilecek_yer = zar-1
            if 'x' in str(table_list[zar-1]):
                secim_kaynak = -1
                gidilecek_yer = zar-1
        else:
            if len(kaynak_listesi) > 0:
                tabloyu_goster(table_list, collect, broken)
                print('Hareket ettirmek istediginiz tasi secin -> ZAR:{}'.format(zar))
                print(kaynak_listesi, ': ', end='')
                secim_kaynak = int(input())
                if zar+secim_kaynak > 23:
                    gidilecek_yer = 24
                    tasi_hareket_ettir(table_list, secim_kaynak, gidilecek_yer, broken, current_player, collect)
                    return
                if table_list[zar+secim_kaynak] == 0:
                    gidilecek_yer = zar+secim_kaynak
                if 'x' in str(table_list[zar+secim_kaynak]):
                    gidilecek_yer = zar+secim_kaynak
                if '1y' in str(table_list[zar+secim_kaynak]):
                    gidilecek_yer = zar+secim_kaynak

    if current_player == 'Y':
        if broken[1] > 0:
            # 18-23 arasi kontrol edilecek
            if table_list[zar-1+18] == 0:
                secim_kaynak = -1
                gidilecek_yer = zar-1+18
            if 'y' in str(table_list[zar-1+18]):
                secim_kaynak = -1
                gidilecek_yer = zar-1+18
        else:
            if len(kaynak_listesi) > 0:
                tabloyu_goster(table_list, collect, broken)
                print('Hareket ettirmek istediginiz tasi secin -> ZAR:{}'.format(zar))
                print(kaynak_listesi, ': ', end='')
                secim_kaynak = int(input())
                if secim_kaynak-zar < 0:
                    gidilecek_yer = -1
                    tasi_hareket_ettir(table_list, secim_kaynak, gidilecek_yer, broken, current_player, collect)
                    return
                if table_list[secim_kaynak-zar] == 0:
                    gidilecek_yer = secim_kaynak-zar
                if 'y' in str(table_list[secim_kaynak-zar]):
                    gidilecek_yer = secim_kaynak-zar
                if '1x' in str(table_list[secim_kaynak-zar]):
                    gidilecek_yer = secim_kaynak-zar
    
    if gidilecek_yer == '':
        print('Tas hareket ettiremiyorsunuz!')
        return

    tasi_hareket_ettir(table_list, secim_kaynak, gidilecek_yer, broken, current_player, collect)


def tasi_hareket_ettir(table_list, secim_kaynak, gidilecek_yer, broken, current_player, collect):
    if gidilecek_yer > 23:
        if table_list[secim_kaynak] == '1x':
            table_list[secim_kaynak] = 0
        else:
            temp_value = int(table_list[secim_kaynak][:-1])
            temp_value -= 1
            table_list[secim_kaynak] = str(temp_value) + 'x'
        collect[0] += 1
        return
    if gidilecek_yer < 0:
        if table_list[secim_kaynak] == '1y':
            table_list[secim_kaynak] = 0
        else:
            temp_value = int(table_list[secim_kaynak][:-1])
            temp_value -= 1
            table_list[secim_kaynak] = str(temp_value) + 'y'
        collect[1] += 1
        return

    if current_player == 'X':
        if secim_kaynak == -1:
            broken[0] -= 1
        else:
            if table_list[secim_kaynak] == '1x':
                table_list[secim_kaynak] = 0
            else:
                temp_value = int(table_list[secim_kaynak][:-1])
                temp_value -= 1
                table_list[secim_kaynak] = str(temp_value) + 'x'

        if table_list[gidilecek_yer] == '1y':
            table_list[gidilecek_yer] = '1x'
            broken[1] += 1
        elif table_list[gidilecek_yer] == 0:
            table_list[gidilecek_yer] = '1x'
        else:
            temp_value = int(table_list[gidilecek_yer][:-1])
            temp_value += 1
            table_list[gidilecek_yer] = str(temp_value) + 'x'

    if current_player == 'Y':
        if secim_kaynak == -1:
            broken[1] -= 1
        else:
            if table_list[secim_kaynak] == '1y':
                table_list[secim_kaynak] = 0
            else:
                temp_value = int(table_list[secim_kaynak][:-1])
                temp_value -= 1
                table_list[secim_kaynak] = str(temp_value) + 'y'

        if table_list[gidilecek_yer] == '1x':
            table_list[gidilecek_yer] = '1y'
            broken[0] += 1
        elif table_list[gidilecek_yer] == 0:
            table_list[gidilecek_yer] = '1y'
        else:
            temp_value = int(table_list[gidilecek_yer][:-1])
            temp_value += 1
            table_list[gidilecek_yer] = str(temp_value) + 'y'
        

def game(table_list, collect, broken, last_player, last_choice):
    while(True):
        if collect[0] == 15:
            if collect[1] == 0:
                print('Mars :) Oyunu X Kazandi')
            else:
                print('Oyunu X Kazandi')
            break
        if collect[1] == 15:
            if collect[0] == 0:
                print('Mars :) Oyunu Y Kazandi')
            else:
                print('Oyunu Y Kazandi')
            break

        if last_player[0] == 'x':
            current_player = 'Y'
        else:
            current_player = 'X'

        zarlar = []
        zar1 = zar_atma()
        zar2 = zar_atma()
        zar_durumu = []
        print('{}\nAtilan Zar {}-{}'.format(current_player, zar1, zar2))
        if zar1 == zar2:
            zarlar.append(zar1)
            zarlar.append(zar1)
            zarlar.append(zar1)
            zarlar.append(zar1)
            zar_durumu.append(zar1)
            zar_durumu.append(zar1)
        else:
            zarlar.append(zar1)
            zarlar.append(zar2)
            zar_durumu.append(zar1)
            zar_durumu.append(zar2)

        for zar in zarlar:
            hareket_yeri(table_list, current_player, zar, broken, collect, last_choice)

        if current_player == 'X':
            last_player[0] = 'x'
            print('\nOyun y ile devam ediyor.\n')
        else:
            last_player[0] = 'y'
            print('\nOyun x ile devam ediyor.\n')

        tabloya_yaz(table_list, collect, broken, last_player)
        zar_yaz(last_player, zar_durumu)



if __name__ == '__main__':
    table_list = []
    # collect = [x, y]
    collect = []
    # broken = [x, y]
    broken = []
    # last_player = [x]
    last_player = []
    # last_choice = [c or 1,2,3,,,6]
    last_choice = []

    print("Erkek Tavlasi'na hosgeldiniz")
    
    if path.exists('Table.dat'):
        decision = input('Onceki oyundan devam etmek ister misiniz? (y|n): ')
        if decision == 'y':
            tablodan_oku(table_list, collect, broken, last_player)
        if decision == 'n':
            yeni_oyun(table_list, collect, broken, last_player)
    else:
        yeni_oyun(table_list, collect, broken, last_player)

    if last_player[0] == 'x':
        print('\nOyun y ile basliyor.\n')
    else:
        print('\nOyun x ile basliyor.\n')
    
    game(table_list, collect, broken, last_player, last_choice)
