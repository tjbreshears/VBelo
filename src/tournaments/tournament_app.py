import os
import sys
import time
import national
import bwc
import cc
import eiva
import iva
import miva
import mpsf
import nec
import siac

simulations = 50000

menu_options = {
    1: 'ALL',
    2: 'NCAA',
    3: 'BWC',
    4: 'CC',
    5: 'EIVA',
    6: 'IVA',
    7: 'MIVA',
    8: 'MPSF',
    9: 'NEC',
    10: 'SIAC',
    11: 'Exit',
}


def clear():
    os.system('cls')


def print_menu():
    print("VBelo Tournament Projections")
    print(f"Number of Simulations: {simulations}\n")
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def option1():
    print('\n')
    national.national(simulations)
    print('\n')
    bwc.bwc(simulations)
    print('\n')
    cc.cc(simulations)
    print('\n')
    eiva.eiva(simulations)
    print('\n')
    iva.iva(simulations)
    print('\n')
    miva.miva(simulations)
    print('\n')
    mpsf.mpsf(simulations)
    print('\n')
    nec.nec(simulations)
    print('\n')
    siac.siac(simulations)
    print('\n')
    os.system('pause')
    clear()


def option2():
    print('\n')
    national.national(simulations)
    print('\n')
    os.system('pause')
    clear()


def option3():
    print('\n')
    bwc.bwc(simulations)
    print('\n')
    os.system('pause')
    clear()


def option4():
    print('\n')
    cc.cc(simulations)
    print('\n')
    os.system('pause')
    clear()


def option5():
    print('\n')
    eiva.eiva(simulations)
    print('\n')
    os.system('pause')
    clear()


def option6():
    print('\n')
    iva.iva(simulations)
    print('\n')
    os.system('pause')
    clear()


def option7():
    print('\n')
    miva.miva(simulations)
    print('\n')
    os.system('pause')
    clear()


def option8():
    print('\n')
    mpsf.mpsf(simulations)
    print('\n')
    os.system('pause')
    clear()


def option9():
    print('\n')
    nec.nec(simulations)
    print('\n')
    os.system('pause')
    clear()


def option10():
    print('\n')
    siac.siac(simulations)
    print('\n')
    os.system('pause')
    clear()


if __name__ == '__main__':
    clear()
    while True:
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 6:
            option6()
        elif option == 7:
            option7()
        elif option == 8:
            option8()
        elif option == 9:
            option9()
        elif option == 10:
            option10()
        elif option == 11:
            print('\n\nGoodbye!')
            time.sleep(3)
            sys.exit()
        else:
            clear()
            print('Invalid option. Please enter a number between 1 and 9.\n\n')
