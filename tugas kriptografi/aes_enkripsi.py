"""
============================================================
  APLIKASI ENKRIPSI FILE MENGGUNAKAN AES (Advanced Encryption Standard)
  Materi  : DES dan AES - Implementasi AES menggunakan Python
  Library : pycryptodome
  Mode AES: CBC (Cipher Block Chaining)
  Kunci   : AES-256 (256 bit / 32 byte)
============================================================
"""

import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import getpass

# ── Warna terminal ──────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
MERAH   = "\033[91m"
HIJAU   = "\033[92m"
KUNING  = "\033[93m"
BIRU    = "\033[94m"
CYAN    = "\033[96m"
PUTIH   = "\033[97m"
MAGENTA = "\033[95m"
BG_BIRU = "\033[44m"
BG_HIJAU= "\033[42m"
BG_MERAH= "\033[41m"

# ── Konstanta ───────────────────────────────────────────────
EKSTENSI_DIDUKUNG = [".txt", ".pdf", ".docx"]
SALT_SIZE         = 16
IV_SIZE           = 16
KEY_SIZE          = 32
PBKDF2_COUNT      = 200_000
EKSTENSI_ENC      = ".enc"


def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")



def cetak_garis(kar="─", pjg=60, wrn=CYAN):
    print(f"{wrn}{kar * pjg}{RESET}")

def tampil_header():
    bersihkan_layar()
    cetak_garis("═", 60, CYAN)
    print(f"{CYAN}║{RESET}{BG_BIRU}{BOLD}{PUTIH}{'  APLIKASI ENKRIPSI FILE AES-256-CBC':^58}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{'':^58}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET}{BIRU}{'  Menggunakan pycryptodome  |  Mode: CBC  |  Key: 256-bit':^58}{RESET}{CYAN}║{RESET}")
    cetak_garis("═", 60, CYAN)
    print()

def sukses(msg):
    print(f"\n  {BG_HIJAU}{BOLD} OK {RESET} {HIJAU}{BOLD}{msg}{RESET}")

def error(msg):
    print(f"\n  {BG_MERAH}{BOLD} ✗ {RESET} {MERAH}{BOLD}{msg}{RESET}")

def info(label, nilai):
    print(f"  {CYAN}➤{RESET}  {DIM}{label:<18}{RESET}{nilai}")

def tampil_ukuran(byte):
    if byte < 1024:       return f"{byte} B"
    elif byte < 1024**2:  return f"{byte/1024:.2f} KB"
    else:                 return f"{byte/1024**2:.2f} MB"


# ── Core enkripsi/dekripsi ───────────────────────────────────
def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=PBKDF2_COUNT)


def enkripsi_file(path_input, password):
    with open(path_input, "rb") as f:
        plaintext = f.read()
    salt       = get_random_bytes(SALT_SIZE)
    iv         = get_random_bytes(IV_SIZE)
    key        = derive_key(password, salt)
    cipher     = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    path_out   = path_input + EKSTENSI_ENC
    with open(path_out, "wb") as f:
        f.write(salt); f.write(iv); f.write(ciphertext)
    return path_out, len(plaintext), os.path.getsize(path_out)


def dekripsi_file(path_enc, password):
    with open(path_enc, "rb") as f:
        salt = f.read(SALT_SIZE); iv = f.read(IV_SIZE); ct = f.read()
    key    = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        plaintext = unpad(cipher.decrypt(ct), AES.block_size)
    except (ValueError, KeyError):
        raise ValueError("Dekripsi gagal! Password salah atau file rusak.")
    base, ext = os.path.splitext(path_enc[:-len(EKSTENSI_ENC)])
    path_out  = base + "_decrypted" + ext
    with open(path_out, "wb") as f:
        f.write(plaintext)
    return path_out, os.path.getsize(path_out)


# ── Menu 1: Enkripsi ─────────────────────────────────────────
def menu_enkripsi():
    cetak_garis()
    print(f"\n  {BOLD}{KUNING}[ ENKRIPSI FILE ]{RESET}\n")

    path = input(f"  {CYAN}Path file (TXT/PDF/DOCX){RESET}: ").strip().strip('"')
    if not path:
        error("Path tidak boleh kosong."); return

    folder = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(path):
        path = os.path.join(folder, path)

    if not os.path.isfile(path):
        error(f"File tidak ditemukan: {path}"); return
    if os.path.splitext(path)[1].lower() not in EKSTENSI_DIDUKUNG:
        error("Ekstensi tidak didukung. Gunakan: .txt / .pdf / .docx"); return

    info("File",   os.path.basename(path))
    info("Ukuran", tampil_ukuran(os.path.getsize(path)))
    print()

    password = getpass.getpass(f"  {CYAN}Masukkan password/key: {RESET}")
    konfirm  = getpass.getpass(f"  {CYAN}Konfirmasi password  : {RESET}")

    if password != konfirm:
        error("Password tidak cocok!"); return
    if len(password) < 6:
        error("Password minimal 6 karakter."); return

    print(f"\n  {KUNING}Mengenkripsi...{RESET}")
    try:
        path_enc, uk_asli, uk_enc = enkripsi_file(path, password)
        sukses("Enkripsi berhasil!")
        print()
        info("File asli",        f"{os.path.basename(path)}  ({tampil_ukuran(uk_asli)})")
        info("File terenkripsi", f"{os.path.basename(path_enc)}  ({tampil_ukuran(uk_enc)})")
        info("Algoritma",        "AES-256-CBC")
        info("Key Derivation",   f"PBKDF2-HMAC-SHA256 ({PBKDF2_COUNT:,} iterasi)")
    except Exception as e:
        error(str(e))


# ── Menu 2: Dekripsi ─────────────────────────────────────────
def menu_dekripsi():
    cetak_garis()
    print(f"\n  {BOLD}{KUNING}[ DEKRIPSI FILE ]{RESET}\n")

    path = input(f"  {CYAN}Path file terenkripsi (.enc){RESET}: ").strip().strip('"')
    if not path:
        error("Path tidak boleh kosong."); return

    folder = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(path):
        path = os.path.join(folder, path)

    if not os.path.isfile(path):
        error(f"File tidak ditemukan: {path}"); return
    if not path.endswith(EKSTENSI_ENC):
        error(f"File harus berekstensi '{EKSTENSI_ENC}'"); return

    info("File",   os.path.basename(path))
    info("Ukuran", tampil_ukuran(os.path.getsize(path)))
    print()

    password = getpass.getpass(f"  {CYAN}Masukkan password/key: {RESET}")

    print(f"\n  {KUNING}Mendekripsi...{RESET}")
    try:
        path_dec, uk_dec = dekripsi_file(path, password)
        sukses("Dekripsi berhasil!")
        print()
        info("File hasil", f"{os.path.basename(path_dec)}  ({tampil_ukuran(uk_dec)})")
        info("Lokasi",     path_dec)
    except Exception as e:
        error(str(e))


# ── Menu 3: Penjelasan ───────────────────────────────────────
def tampil_penjelasan():
    cetak_garis()
    print(f"\n  {BOLD}{KUNING}[ PENJELASAN AES & MODE CBC ]{RESET}\n")

    bagian = [
        ("AES (Advanced Encryption Standard)", [
            "Standar enkripsi simetris yang ditetapkan NIST pada tahun 2001.",
            "Mengenkripsi data dalam blok 128-bit.",
            "Mendukung kunci 128-bit, 192-bit, dan 256-bit.",
            "Program ini menggunakan AES-256 (kunci 32 byte = level keamanan tertinggi).",
        ]),
        ("Ronde Transformasi AES-256 (14 ronde)", [
            "1. SubBytes   → Substitusi non-linear setiap byte melalui S-Box.",
            "2. ShiftRows  → Pergeseran siklik baris-baris state ke kiri.",
            "3. MixColumns → Transformasi linear kolom (perkalian matriks di GF(2^8)).",
            "4. AddRoundKey → XOR state dengan sub-kunci ronde.",
        ]),
        ("Mode CBC (Cipher Block Chaining)", [
            "Setiap blok plaintext di-XOR dengan ciphertext blok sebelumnya.",
            "Blok pertama di-XOR dengan IV (Initialization Vector) acak.",
            "Rumus enkripsi : C[i] = AES_Enc(P[i] XOR C[i-1])",
            "Rumus dekripsi : P[i] = AES_Dec(C[i]) XOR C[i-1]",
            "Keunggulan     : Pola data plaintext tidak terlihat di ciphertext.",
        ]),
        ("Key Derivation: PBKDF2-HMAC-SHA256", [
            "Password teks dikonversi ke kunci 256-bit menggunakan PBKDF2.",
            f"Salt    : {SALT_SIZE} byte acak → mencegah rainbow table attack.",
            f"IV      : {IV_SIZE} byte acak → memastikan ciphertext unik.",
            f"Iterasi : {PBKDF2_COUNT:,}× → memperlambat brute-force attack.",
        ]),
        ("Format File .enc", [
            f"[ SALT {SALT_SIZE} byte ] + [ IV {IV_SIZE} byte ] + [ CIPHERTEXT n byte ]",
            "Plaintext di-padding dengan PKCS7 agar kelipatan 16 byte.",
        ]),
    ]

    for judul, poin in bagian:
        print(f"  {BOLD}{MAGENTA}{judul}{RESET}")
        for p in poin:
            print(f"    {CYAN}•{RESET} {p}")
        print()


# ── Menu 4: Buat file contoh ─────────────────────────────────
def buat_file_contoh():
    folder = os.path.dirname(os.path.abspath(__file__))
    path   = os.path.join(folder, "contoh_plaintext.txt")
    isi = (
        "============================================\n"
        "  DATA MAHASISWA - CONTOH FILE UNTUK DEMO\n"
        "============================================\n"
        "\n"
        "Nama    : Mahasiswa Kriptografi\n"
        "NIM     : 123456789\n"
        "Nilai   : A (Sangat Memuaskan)\n"
        "Prodi   : Teknik Informatika\n"
        "\n"
        "Catatan Rahasia:\n"
        "  File ini berisi data sensitif yang perlu diamankan.\n"
        "  Setelah dienkripsi dengan AES-256-CBC, isinya tidak\n"
        "  bisa dibaca tanpa password yang benar.\n"
        "\n"
        "AES-256-CBC adalah algoritma enkripsi paling aman!\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(isi)
    sukses(f"File contoh dibuat!")
    info("Lokasi", path)
    info("Ukuran", tampil_ukuran(os.path.getsize(path)))


# ── Menu utama ───────────────────────────────────────────────
def main():
    tampil_header()

    while True:
        print(f"\n  {BOLD}MENU UTAMA{RESET}")
        cetak_garis("─", 60, CYAN)
        print(f"  {HIJAU}[1]{RESET} Enkripsi File")
        print(f"  {BIRU}[2]{RESET} Dekripsi File")
        print(f"  {KUNING}[3]{RESET} Penjelasan AES & Mode CBC")
        print(f"  {MAGENTA}[4]{RESET} Buat File TXT Contoh (untuk demo)")
        print(f"  {MERAH}[0]{RESET} Keluar")
        cetak_garis("─", 60, CYAN)

        pilihan = input(f"\n  {CYAN}Pilih menu{RESET} [0-4]: ").strip()

        if pilihan == "1":
            menu_enkripsi()
        elif pilihan == "2":
            menu_dekripsi()
        elif pilihan == "3":
            tampil_penjelasan()
        elif pilihan == "4":
            buat_file_contoh()
        elif pilihan == "0":
            print(f"\n  {CYAN}Terima kasih. Program selesai.{RESET}\n")
            sys.exit(0)
        else:
            error("Pilihan tidak valid. Masukkan angka 0-4.")

        input(f"\n  {DIM}Tekan Enter untuk kembali ke menu...{RESET}")
        tampil_header()


if __name__ == "__main__":
    main()

