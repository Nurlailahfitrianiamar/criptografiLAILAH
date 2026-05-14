import hashlib
import json
import os
import getpass

# ─────────────────────────────────────────────
#  File penyimpanan data pengguna
# ─────────────────────────────────────────────
DATA_FILE = "data_pengguna.json"

# ─────────────────────────────────────────────
#  Kode warna ANSI
# ─────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

MERAH   = "\033[91m"
HIJAU   = "\033[92m"
KUNING  = "\033[93m"
BIRU    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
PUTIH   = "\033[97m"

BG_BIRU   = "\033[44m"
BG_HIJAU  = "\033[42m"
BG_MERAH  = "\033[41m"
BG_HITAM  = "\033[40m"


# ══════════════════════════════════════════════
#  UTILITAS TAMPILAN
# ══════════════════════════════════════════════

def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def garis(karakter="═", lebar=60, warna=CYAN):
    print(f"{warna}{karakter * lebar}{RESET}")


def judul_banner():
    bersihkan_layar()
    garis("═", 60, CYAN)
    print(f"{CYAN}║{RESET}{BG_BIRU}{BOLD}{PUTIH}{'🔐  SISTEM REGISTRASI & LOGIN AMAN':^58}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{'':^58}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{BIRU}{'  Keamanan Password dengan Hash SHA-256':^58}{RESET}{CYAN}║{RESET}")
    garis("═", 60, CYAN)
    print()


def pesan_sukses(teks):
    print(f"\n  {BG_HIJAU}{BOLD} ✔  {RESET} {HIJAU}{BOLD}{teks}{RESET}")


def pesan_error(teks):
    print(f"\n  {BG_MERAH}{BOLD} ✘  {RESET} {MERAH}{BOLD}{teks}{RESET}")


def pesan_info(teks):
    print(f"\n  {CYAN}ℹ  {teks}{RESET}")


def tekan_enter():
    print(f"\n{DIM}  Tekan Enter untuk melanjutkan...{RESET}", end="")
    input()


def kotak_info(judul, isi_dict):
    lebar = 56
    garis("─", lebar, KUNING)
    print(f"{KUNING}  {BOLD}{judul}{RESET}")
    garis("─", lebar, KUNING)
    for kunci, nilai in isi_dict.items():
        print(f"  {KUNING}{kunci:<20}{RESET}: {PUTIH}{nilai}{RESET}")
    garis("─", lebar, KUNING)


# ══════════════════════════════════════════════
#  FUNGSI DATA
# ══════════════════════════════════════════════

def muat_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def simpan_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def hash_sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ══════════════════════════════════════════════
#  FITUR UTAMA
# ══════════════════════════════════════════════

def registrasi():
    judul_banner()
    print(f"  {MAGENTA}{BOLD}╔══════════════════════════════╗")
    print(f"  ║   📋  REGISTRASI PENGGUNA   ║")
    print(f"  ╚══════════════════════════════╝{RESET}\n")

    data = muat_data()

    print(f"  {PUTIH}Masukkan detail akun baru Anda:{RESET}")
    print()

    username = input(f"  {CYAN}➤  Username   : {RESET}").strip()
    if not username:
        pesan_error("Username tidak boleh kosong!")
        tekan_enter()
        return

    if username in data:
        pesan_error(f"Username '{username}' sudah terdaftar!")
        tekan_enter()
        return

    print(f"  {CYAN}➤  Password   : {RESET}", end="", flush=True)
    password = getpass.getpass(prompt="")
    if not password:
        pesan_error("Password tidak boleh kosong!")
        tekan_enter()
        return

    print(f"  {CYAN}➤  Konfirmasi : {RESET}", end="", flush=True)
    konfirmasi = getpass.getpass(prompt="")

    if password != konfirmasi:
        pesan_error("Password dan konfirmasi tidak cocok!")
        tekan_enter()
        return

    hash_pw = hash_sha256(password)
    data[username] = {"hash_password": hash_pw}
    simpan_data(data)

    print()
    kotak_info("✔  REGISTRASI BERHASIL", {
        "Username"      : username,
        "Hash SHA-256"  : hash_pw[:32] + "...",
        "Hash Lengkap"  : hash_pw,
    })

    pesan_sukses(f"Akun '{username}' berhasil dibuat dan disimpan!")
    tekan_enter()


def login():
    judul_banner()
    print(f"  {BIRU}{BOLD}╔══════════════════════════════╗")
    print(f"  ║     🔑  LOGIN PENGGUNA      ║")
    print(f"  ╚══════════════════════════════╝{RESET}\n")

    data = muat_data()

    if not data:
        pesan_info("Belum ada pengguna terdaftar. Silakan registrasi terlebih dahulu.")
        tekan_enter()
        return

    print(f"  {PUTIH}Masukkan kredensial Anda:{RESET}\n")

    username = input(f"  {CYAN}➤  Username   : {RESET}").strip()
    if username not in data:
        pesan_error(f"Username '{username}' tidak ditemukan!")
        tekan_enter()
        return

    print(f"  {CYAN}➤  Password   : {RESET}", end="", flush=True)
    password = getpass.getpass(prompt="")

    hash_input    = hash_sha256(password)
    hash_tersimpan = data[username]["hash_password"]

    print()
    kotak_info("🔍  VERIFIKASI PASSWORD", {
        "Username"       : username,
        "Hash Input"     : hash_input[:32] + "...",
        "Hash Tersimpan" : hash_tersimpan[:32] + "...",
        "Cocok?"         : "✔  YA" if hash_input == hash_tersimpan else "✘  TIDAK",
    })

    if hash_input == hash_tersimpan:
        print(f"\n  {BG_HIJAU}{BOLD}{'  ✔  LOGIN BERHASIL! Selamat datang, ' + username + '!  ':^54}{RESET}")
    else:
        print(f"\n  {BG_MERAH}{BOLD}{'  ✘  LOGIN GAGAL! Password salah.  ':^54}{RESET}")

    tekan_enter()


def lihat_pengguna():
    judul_banner()
    print(f"  {KUNING}{BOLD}╔═══════════════════════════════════╗")
    print(f"  ║  📂  DAFTAR PENGGUNA TERDAFTAR  ║")
    print(f"  ╚═══════════════════════════════════╝{RESET}\n")

    data = muat_data()

    if not data:
        pesan_info("Belum ada pengguna yang terdaftar.")
        tekan_enter()
        return

    garis("─", 60, KUNING)
    print(f"  {KUNING}{BOLD}{'No':<5}{'Username':<20}{'Hash SHA-256 (sebagian)'}{RESET}")
    garis("─", 60, KUNING)

    for i, (username, info) in enumerate(data.items(), 1):
        hash_pendek = info["hash_password"][:30] + "..."
        print(f"  {PUTIH}{i:<5}{CYAN}{username:<20}{DIM}{hash_pendek}{RESET}")

    garis("─", 60, KUNING)
    print(f"\n  Total pengguna terdaftar: {HIJAU}{BOLD}{len(data)}{RESET}")
    tekan_enter()


# ══════════════════════════════════════════════
#  MENU UTAMA
# ══════════════════════════════════════════════

def menu_utama():
    while True:
        judul_banner()
        print(f"  {PUTIH}{BOLD}Pilih menu di bawah ini:{RESET}\n")
        print(f"  {BG_HITAM} {HIJAU} 1 {RESET}  {HIJAU}Registrasi Pengguna Baru{RESET}")
        print(f"  {BG_HITAM} {BIRU} 2 {RESET}  {BIRU}Login Pengguna{RESET}")
        print(f"  {BG_HITAM} {KUNING} 3 {RESET}  {KUNING}Lihat Daftar Pengguna{RESET}")
        print(f"  {BG_HITAM} {MERAH} 0 {RESET}  {MERAH}Keluar{RESET}")
        print()
        garis("─", 60, DIM)

        pilihan = input(f"\n  {CYAN}➤  Pilihan Anda [0-3]: {RESET}").strip()

        if pilihan == "1":
            registrasi()
        elif pilihan == "2":
            login()
        elif pilihan == "3":
            lihat_pengguna()
        elif pilihan == "0":
            judul_banner()
            print(f"  {HIJAU}{BOLD}Terima kasih telah menggunakan program ini! 👋{RESET}\n")
            garis("═", 60, CYAN)
            break
        else:
            pesan_error("Pilihan tidak valid! Masukkan angka 0, 1, 2, atau 3.")
            tekan_enter()


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    menu_utama()