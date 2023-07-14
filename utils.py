okay = lambda msg, *args: print(f"[+] {msg} {' '.join(map(str, args))}")
warn = lambda msg, *args: print(f"[*] {msg} {' '.join(map(str, args))}")
error = lambda msg, *args: print(f"[-] {msg} {' '.join(map(str, args))}")
