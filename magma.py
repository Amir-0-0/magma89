def genKeys(keys1: str):
    'возвращает массив из 8 элементов, где каждый элемент - это 32 бита'
    keys1 = list(map(ord, keys1))
    key = ''
    for i in keys1:
        key += bin(i)[2:].zfill(8)

    if len(key) != 256:
        return 'длина ключа не равно 256 битам'

    keys = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        keys[i] = key[:32]
        key = key[32:]
    return keys


def fileReader(path : str):
    'считывание файла и разделение на блоки'
    with open(path, 'rb') as file:
        datesBlocks = []
        date = file.read(8)
        while date:
            datesBlocks.append(date)
            date = file.read(8)

        # дописываем нули для кратности 8 байтам
        while len(datesBlocks[-1]) != 8:
            datesBlocks[-1] += bytes([0])

    blocks64Bit = []
    for block in datesBlocks:
        binStr = ''
        for j in block:
            binStr += bin(j)[2:].zfill(8)
        blocks64Bit.append(binStr)

    return blocks64Bit

def fileWriter(path : str,datesBlocks : list):
    'запись блоков в файл'
    with open(path, 'wb') as file:
        # Преобразование битовой строки в байты
        for block in datesBlocks[:-1]:
            bytes = bytearray()
            for i in range(0, 64, 8):
                byte = int(block[i:i + 8], 2)
                bytes.append(byte)
            file.write(bytes)

        # записываем последний блок вырезая нули
        bytes = bytearray()
        last = datesBlocks[-1]
        for i in range(0, 64 , 8):
            byte = int(last[i:i + 8], 2)
            if byte == 0:
                break
            bytes.append(byte)

        file.write(bytes)

    print(f'Данные записаны в файл: {path}')


def xor(a: str, b: str):
    res = bin(int(a, 2) ^ int(b, 2))[2:].zfill(len(a))
    return res


def sdvig(str: str, n: int):
    result = str[n:] + str[:n]
    return result

def substitution(N1: str):
    'таблица замен'
    sbox = [
        [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
        [6, 8, 2, 3, 9,	10,	5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
        [11, 3,	5, 8, 2, 15, 10, 13, 14, 1,	7, 4, 12, 9, 6,	0],
        [12, 8,	2, 1, 13, 4, 15, 6,	7,	0,	10,	5,	3,	14,	9, 11],
        [7,	15,	5, 10, 8, 1, 6,	13,	0,	9,	3, 14, 11, 4, 2, 12],
        [5,	13,	15,	6,	9,	2,	12,	10,	11,	7,	8,	1,	4,	3,	14,	0],
        [8,	14,	2,	5,	6,	9,	1,	12,	15,	4,	11,	0,	13,	10,	3, 7],
        [1,	7, 14,	13,	0, 5, 8, 3,	4, 15, 10, 6, 9, 12, 11, 2]
    ]
    # 8 блоков по 4 бита
    blocks4b = []
    for i in range(8):
        blocks4b.append(N1[:4])
        N1 = N1[4:].zfill(4)
    blocksAfterSbox = ''
    for i in range(8):
        blocksAfterSbox += bin(sbox[i][int(blocks4b[i], 2)])[2:].zfill(4)
    return blocksAfterSbox

def round_feistel_scheme(L0: str, R0: str, key: str):
    'один раунд шифрования'
    # RES = (N1 + Ki) mod 2 ^ 32
    RES = bin((int(L0, 2) + int(key, 2)) % 2**32)[2:]
    RES = substitution(RES)
    RES = sdvig(RES, 11)
    L0, R0 = xor(RES, R0), L0
    return L0, R0


def feistel_scheme(block: str, keys: list, mode: int):
    L0 = block[:32]
    R0 = block[32:]
    if mode == 1:
        # K0, K1, K2, K3, K4, K5, K6, K7, K0, K1, K2, K3, K4, K5, K6, K7, K0, K1, K2, K3, K4, K5, K6, K7
        for i in range(3):
            for key in keys:
                L0, R0 = round_feistel_scheme(L0, R0, key)
        # K7, K6, K5, K4, K3, K2, K1, K0
        for key in keys[::-1]:
            L0, R0 = round_feistel_scheme(L0, R0, key)
        L0, R0 = R0, L0
    else:
        # K0, K1, K2, K3, K4, K5, K6, K7

        for key in keys:
            L0, R0 = round_feistel_scheme(L0, R0, key)
        # K7, K6, K5, K4, K3, K2, K1, K0, K7, K6, K5, K4, K3, K2, K1, K0, K7, K6, K5, K4, K3, K2, K1, K0
        for i in range(3):
            for key in keys[::-1]:
                L0, R0 = round_feistel_scheme(L0, R0, key)
        L0, R0 = R0, L0
    return L0 + R0


def gost_zamena(key, path):

    if path[-6:] == '.magma':
        mode = 0
    else:
        mode = 1

    # создание подключей по 32 бита
    keys = genKeys(key)

    # Считываение файла и разделение на блоки по 64 бита
    blocksBin = fileReader(path)

    blocksEncrypt = []
    for block in blocksBin:
        block64b = feistel_scheme(block, keys, mode)
        blocksEncrypt.append(block64b)

    if mode:
        fileWriter(path + '.magma' , blocksEncrypt)
    else:
        fileWriter(path[:-6], blocksEncrypt)

