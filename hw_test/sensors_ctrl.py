from hardware_ctrl import read_in, read_sensor


if __name__ == '__main__':
    while True:
        bno, mini_l, mini_c, mini_r = read_sensor()

        print(f'X tilting = {bno} deg')
        print(f'Left side distance = {mini_l} mm')
