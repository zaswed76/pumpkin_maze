import subprocess


def run_process(process, lst):
    for line in lst:
        if line:
            if process in line[0]:
                return True


def call(process):
    subprocess.call([process])


def main():
    path_process = r'D:\save\serg\python\bin\Tiled-0.17.1375-win32\tiled.exe'
    lst = [line.split() for line in
           subprocess.check_output("tasklist").splitlines()]
    if not run_process(b'tiled.exe', lst):
        call(path_process)
    else:
        print('tiled.exe run')



main()
