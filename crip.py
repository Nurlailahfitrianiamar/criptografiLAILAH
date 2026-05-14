import hashlib
import os, json
import getpass

# nama file buat nyimpen data user
file_data = "data_pengguna.json"

# warna buat tampilan di terminal
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
MERAH = "\033[91m"
HIJAU = "\033[92m"
KUNING = "\033[93m"
BIRU = "\033[94m"
CYAN = "\033[96m"
PUTIH = "\033[97m"
BG_HIJAU = "\033[42m"
BG_MERAH = "\033[41m"
BG_BIRU = "\033[44m"
BG_HITAM = "\033[40m"
MAGENTA = "\033[95m"


# fungsi bersihkan layar
def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")

# cetak garis pemisah
def cetak_garis(kar="-", pjg=55, wrn=CYAN):
    print(f"{wrn}{kar * pjg}{RESET}")

# tampilkan header program
def tampil_header():
    bersihkan_layar()
    cetak_garis("=", 55, CYAN)
    print(f"{CYAN}||{RESET}{BG_BIRU}{BOLD}{PUTIH}{'  PROGRAM REGISTRASI DAN LOGIN USER':^51}{RESET}{CYAN}||{RESET}")
    print(f"{CYAN}||{RESET}{'':^51}{CYAN}||{RESET}")
    print(f"{CYAN}||{RESET}{BIRU}{'  Password diamankan dengan SHA-256':^51}{RESET}{CYAN}||{RESET}")
    cetak_garis("=", 55, CYAN)
    print()

# tampilkan pesan berhasil
def sukses(msg):
    print(f"\n  {BG_HIJAU}{BOLD} OK {RESET} {HIJAU}{BOLD}{msg}{RESET}")

# tampilkan pesan error
def error(msg):
    print(f"\n  {BG_MERAH}{BOLD} X {RESET} {MERAH}{BOLD}{msg}{RESET}")

# tampilkan pesan info biasa
def info(msg):
    print(f"\n  {CYAN}>> {msg}{RESET}")

# pause tunggu enter
def tunggu():
    print(f"\n{DIM}  Tekan Enter...{RESET}", end="")
    input()

# tampilkan info dalam kotak sederhana
def tampil_kotak(judul, data_dict):
    cetak_garis("-", 52, KUNING)
    print(f"{KUNING}  {BOLD}{judul}{RESET}")
    cetak_garis("-", 52, KUNING)
    for k, v in data_dict.items():
        print(f"  {KUNING}{k:<18}{RESET}: {PUTIH}{v}{RESET}")
    cetak_garis("-", 52, KUNING)


# load data user dari file json
def load_data():
    if not os.path.exists(file_data):
        return {}
    f = open(file_data, "r")
    isi = json.load(f)
    f.close()
    return isi

# simpan data user ke file json
def save_data(data):
    f = open(file_data, "w")
    json.dump(data, f, indent=4)
    f.close()

# hash password pakai sha256
def enkripsi(pw):
    hasil = hashlib.sha256(pw.encode()).hexdigest()
    return hasil


# fitur registrasi user baru
def daftar():
    tampil_header()
    print(f"  {MAGENTA}{BOLD}+-----------------------------+")
    print(f"  |    FORM REGISTRASI USER    |")
    print(f"  +-----------------------------+{RESET}\n")

    db = load_data()

    uname = input(f"  {CYAN}  Username  : {RESET}").strip()
    if uname == "":
        error("Username gak boleh kosong!")
        tunggu()
        return

    if uname in db:
        error(f"Username {uname} udah ada, coba yang lain.")
        tunggu()
        return

    print(f"  {CYAN}  Password  : {RESET}", end="", flush=True)
    pw = getpass.getpass(prompt="")
    if pw == "":
        error("Password gak boleh kosong!")
        tunggu()
        return

    print(f"  {CYAN}  Ulangi PW : {RESET}", end="", flush=True)
    pw2 = getpass.getpass(prompt="")

    if pw != pw2:
        error("Password sama konfirmasi beda!")
        tunggu()
        return

    # hash password sebelum disimpan
    hpw = enkripsi(pw)
    db[uname] = {"hash_pw": hpw}
    save_data(db)

    print()
    tampil_kotak("REGISTRASI BERHASIL", {
        "Username"    : uname,
        "Hash (SHA256)": hpw[:30] + "...",
        "Hash Lengkap" : hpw,
    })

    sukses(f"Akun {uname} berhasil didaftarkan!")
    tunggu()


# fitur login user
def masuk():
    tampil_header()
    print(f"  {BIRU}{BOLD}+-----------------------------+")
    print(f"  |       FORM LOGIN USER       |")
    print(f"  +-----------------------------+{RESET}\n")

    db = load_data()

    if len(db) == 0:
        info("Belum ada user yang daftar, registrasi dulu ya.")
        tunggu()
        return

    uname = input(f"  {CYAN}  Username  : {RESET}").strip()
    if uname not in db:
        error(f"Username {uname} gak ketemu di database.")
        tunggu()
        return

    print(f"  {CYAN}  Password  : {RESET}", end="", flush=True)
    pw = getpass.getpass(prompt="")

    # hash password yang diinput lalu bandingkan
    h_input = enkripsi(pw)
    h_simpan = db[uname]["hash_pw"]

    print()
    tampil_kotak("CEK PASSWORD", {
        "Username"      : uname,
        "Hash Input"    : h_input[:28] + "...",
        "Hash Disimpan" : h_simpan[:28] + "...",
        "Cocok?"        : "YA" if h_input == h_simpan else "TIDAK",
    })

    if h_input == h_simpan:
        print(f"\n  {BG_HIJAU}{BOLD}{'  LOGIN BERHASIL! Halo ' + uname + '!  ':^50}{RESET}")
    else:
        print(f"\n  {BG_MERAH}{BOLD}{'  LOGIN GAGAL. Password salah!  ':^50}{RESET}")

    tunggu()


# tampilkan semua user yang sudah daftar
def list_user():
    tampil_header()
    print(f"  {KUNING}{BOLD}+----------------------------------+")
    print(f"  |    DAFTAR USER YANG TERDAFTAR    |")
    print(f"  +----------------------------------+{RESET}\n")

    db = load_data()

    if len(db) == 0:
        info("Belum ada user sama sekali.")
        tunggu()
        return

    cetak_garis("-", 55, KUNING)
    print(f"  {KUNING}{BOLD}{'No':<5}{'Username':<18}{'Hash (sebagian)'}{RESET}")
    cetak_garis("-", 55, KUNING)

    nomor = 1
    for uname, val in db.items():
        hp = val["hash_pw"][:28] + "..."
        print(f"  {PUTIH}{nomor:<5}{CYAN}{uname:<18}{DIM}{hp}{RESET}")
        nomor += 1

    cetak_garis("-", 55, KUNING)
    print(f"\n  Total: {HIJAU}{BOLD}{len(db)} user{RESET}")
    tunggu()


# menu utama program
def main():
    while True:
        tampil_header()
        print(f"  {PUTIH}{BOLD}Silakan pilih menu:{RESET}\n")
        print(f"  {BG_HITAM} {HIJAU} 1 {RESET}  {HIJAU}Registrasi User Baru{RESET}")
        print(f"  {BG_HITAM} {BIRU} 2 {RESET}  {BIRU}Login{RESET}")
        print(f"  {BG_HITAM} {KUNING} 3 {RESET}  {KUNING}Lihat Semua User{RESET}")
        print(f"  {BG_HITAM} {MERAH} 0 {RESET}  {MERAH}Keluar{RESET}")
        print()
        cetak_garis("-", 55, DIM)

        pil = input(f"\n  {CYAN}  Pilihan [0-3] : {RESET}").strip()

        if pil == "1":
            daftar()
        elif pil == "2":
            masuk()
        elif pil == "3":
            list_user()
        elif pil == "0":
            tampil_header()
            print(f"  {HIJAU}{BOLD}Makasih udah pake program ini!{RESET}\n")
            cetak_garis("=", 55, CYAN)
            break
        else:
            error("Pilihannya salah, masukkan 0 sampai 3.")
            tunggu()


if __name__ == "__main__":
    main()