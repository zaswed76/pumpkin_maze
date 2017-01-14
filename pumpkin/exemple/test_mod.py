import os


def get_path(direct):
    lst = []
    for root, dirs, files in os.walk(direct):  # пройти по директории рекурсивно
        for name in files:
            fullname = os.path.join(root,
                                    name)  # получаем полное имя файла
            lst.append(fullname)  # делаем что-нибудь с ним
    return lst


d = r"Компьютер\WALKMAN NWZ-B173 \Storage Media\Music\MartinIden"

print(get_path(d))