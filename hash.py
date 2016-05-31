from re import match
from sys import stdout, hexversion, exit, argv
import traceback

TITLE = ("HashID \n"
         "Welcome.")

USAGE = ("\tUsage: \n"
         "\n"
         "\t\t Run in console: python hash.py")

HASHES = (
    ("Blowfish(Eggdrop)", "^\+[a-zA-Z0-9\/\.]{12}$"),
    ("Blowfish(OpenBSD)", "^\$2a\$[0-9]{0,2}?\$[a-zA-Z0-9\/\.]{53}$"),
    ("Blowfish crypt", "^\$2[axy]{0,1}\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    (("DES(Unix)", "DES crypt", "DES hash(Traditional)"), "^.{0,2}[a-zA-Z0-9\/\.]{11}$"),
    ("MD5(Unix)", "^\$1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
    (("MD5(APR)", "Apache MD5"), "^\$apr1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
    ("MD5(MyBB)", "^[a-fA-F0-9]{32}:[a-z0-9]{8}$"),
    ("MD5(ZipMonster)", "^[a-fA-F0-9]{32}$"),
    (("MD5 crypt", "FreeBSD MD5", "Cisco-IOS MD5"), "^\$1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    ("MD5 apache crypt", "^\$apr1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    ("MD5(Joomla)", "^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16,32}$"),
    ("MD5(Wordpress)", "^\$P\$[a-zA-Z0-9\/\.]{31}$"),
    ("MD5(phpBB3)", "^\$H\$[a-zA-Z0-9\/\.]{31}$"),
    ("MD5(Cisco PIX)", "^[a-zA-Z0-9\/\.]{16}$"),
    (("MD5(osCommerce)", "xt:Commerce"), "^[a-fA-F0-9]{32}:[a-zA-Z0-9]{2}$"),
    ("MD5(Palshop)", "^[a-fA-F0-9]{51}$"),
    ("MD5(IP.Board)", "^[a-fA-F0-9]{32}:.{5}$"),
    ("MD5(Chap)", "^[a-fA-F0-9]{32}:[0-9]{32}:[a-fA-F0-9]{2}$"),
    ("Juniper Netscreen/SSG (ScreenOS)", "^[a-zA-Z0-9]{30}:[a-zA-Z0-9]{4,}$"),
    ("Fortigate (FortiOS)", "^[a-fA-F0-9]{47}$"),
    ("Minecraft(Authme)", "^\$sha\$[a-zA-Z0-9]{0,16}\$[a-fA-F0-9]{64}$"),
    ("Lotus Domino", "^\(?[a-zA-Z0-9\+\/]{20}\)?$"),
    ("Lineage II C4", "^0x[a-fA-F0-9]{32}$"),
    ("CRC-96(ZIP)", "^[a-fA-F0-9]{24}$"),
    ("NT crypt", "^\$3\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    ("Skein-1024", "^[a-fA-F0-9]{256}$"),
    (("RIPEMD-320", "RIPEMD-320(HMAC)"), "^[A-Fa-f0-9]{80}$"),
    ("EPi hash", "^0x[A-F0-9]{60}$"),
    ("EPiServer 6.x < v4", "^\$episerver\$\*0\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9\+]{27}$"),
    ("EPiServer 6.x >= v4", "^\$episerver\$\*1\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9]{43}$"),
    ("Cisco IOS SHA256", "^[a-zA-Z0-9]{43}$"),
    ("SHA-1(Django)", "^sha1\$.{0,32}\$[a-fA-F0-9]{40}$"),
    ("SHA-1 crypt", "^\$4\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    ("SHA-1(Hex)", "^[a-fA-F0-9]{40}$"),
    (("SHA-1(LDAP) Base64", "Netscape LDAP SHA", "NSLDAP"), "^\{SHA\}[a-zA-Z0-9+/]{27}=$"),
    ("SHA-1(LDAP) Base64 + salt", "^\{SSHA\}[a-zA-Z0-9+/]{28,}[=]{0,3}$"),
    ("SHA-512(Drupal)", "^\$S\$[a-zA-Z0-9\/\.]{52}$"),
    ("SHA-512 crypt", "^\$6\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    ("SHA-256(Django)", "^sha256\$.{0,32}\$[a-fA-F0-9]{64}$"),
    ("SHA-256 crypt", "^\$5\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
    ("SHA-384(Django)", "^sha384\$.{0,32}\$[a-fA-F0-9]{96}$"),
    ("SHA-256(Unix)", "^\$5\$.{0,22}\$[a-zA-Z0-9\/\.]{43,69}$"),
    ("SHA-512(Unix)", "^\$6\$.{0,22}\$[a-zA-Z0-9\/\.]{86}$"),
    (("SHA-384", "SHA3-384", "Skein-512(384)", "Skein-1024(384)"), "^[a-fA-F0-9]{96}$"),
    (("SHA-512", "SHA-512(HMAC)", "SHA3-512", "Whirlpool", "SALSA-10", "SALSA-20", "Keccak-512", "Skein-512",
      "Skein-1024(512)"), "^[a-fA-F0-9]{128}$"),
    ("SSHA-1", "^({SSHA})?[a-zA-Z0-9\+\/]{32,38}?(==)?$"),
    (("SSHA-1(Base64)", "Netscape LDAP SSHA", "NSLDAPS"), "^\{SSHA\}[a-zA-Z0-9]{32,38}?(==)?$"),
    (("SSHA-512(Base64)", "LDAP {SSHA512}"), "^\{SSHA512\}[a-zA-Z0-9+]{96}$"),
    ("Oracle 11g", "^S:[A-Z0-9]{60}$"),
    ("SMF >= v1.1", "^[a-fA-F0-9]{40}:[0-9]{8}&"),
    ("MySQL 5.x", "^\*[a-f0-9]{40}$"),
    (("MySQL 3.x", "DES(Oracle)", "LM", "VNC", "FNV-164"), "^[a-fA-F0-9]{16}$"),
    ("OSX v10.7", "^[a-fA-F0-9]{136}$"),
    ("OSX v10.8", "^\$ml\$[a-fA-F0-9$]{199}$"),
    ("SAM(LM_Hash:NT_Hash)", "^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$"),
    ("MSSQL(2000)", "^0x0100[a-f0-9]{0,8}?[a-f0-9]{80}$"),
    (("MSSQL(2005)", "MSSQL(2008)"), "^0x0100[a-f0-9]{0,8}?[a-f0-9]{40}$"),
    ("MSSQL(2012)", "^0x02[a-f0-9]{0,10}?[a-f0-9]{128}$"),
    (("substr(md5($pass),0,16)", "substr(md5($pass),16,16)", "substr(md5($pass),8,16)", "CRC-64"),
     "^[a-fA-F0-9./]{16}$"),
    (("MySQL 4.x", "SHA-1", "HAVAL-160", "SHA-1(MaNGOS)", "SHA-1(MaNGOS2)", "TIGER-160", "RIPEMD-160",
      "RIPEMD-160(HMAC)",
      "TIGER-160(HMAC)", "Skein-256(160)", "Skein-512(160)"), "^[a-f0-9]{40}$"),
    (("SHA-256", "SHA-256(HMAC)", "SHA-3(Keccak)", "GOST R 34.11-94", "RIPEMD-256", "HAVAL-256", "Snefru-256",
      "Snefru-256(HMAC)", "RIPEMD-256(HMAC)", "Keccak-256", "Skein-256", "Skein-512(256)"), "^[a-fA-F0-9]{64}$"),
    (("SHA-1(Oracle)", "HAVAL-192", "OSX v10.4, v10.5, v10.6", "Tiger-192", "TIGER-192(HMAC)"), "^[a-fA-F0-9]{48}$"),
    (("SHA-224", "SHA-224(HMAC)", "HAVAL-224", "Keccak-224", "Skein-256(224)", "Skein-512(224)"), "^[a-fA-F0-9]{56}$"),
    (("Adler32", "FNV-32", "ELF-32", "Joaat", "CRC-32", "CRC-32B", "GHash-32-3", "GHash-32-5", "FCS-32", "Fletcher-32",
      "XOR-32"), "^[a-f0-9]{8}$"),
    (("CRC-16-CCITT", "CRC-16", "FCS-16"), "^[a-fA-F0-9]{4}$"),
    (("MD5(HMAC(Wordpress))", "MD5(HMAC)", "MD5", "RIPEMD-128", "RIPEMD-128(HMAC)", "Tiger-128", "Tiger-128(HMAC)",
      "RAdmin v2.x", "NTLM", "Domain Cached Credentials(DCC)", "Domain Cached Credentials 2(DCC2)", "MD4", "MD2",
      "MD4(HMAC)", "MD2(HMAC)", "Snefru-128", "Snefru-128(HMAC)", "HAVAL-128", "HAVAL-128(HMAC)", "Skein-256(128)",
      "Skein-512(128)", "MSCASH2"), "^[0-9A-Fa-f]{32}$"),
)


def identify_hashes(inputHash):
    """
    Identifies all the hashes and returns it as a list.
    :param inputHash: hash as input
    :return: a list
    """

    # List that stores the names of identified hash algorithms
    res = []

    # Loops through all the hashes in the tuple HASHES to find all possible hashes
    for items in HASHES:
        if match(items[1], inputHash):
            res += [items[0]] if (type(items[0]) is str) else items[0]
    return res


def getInput(prompt):
    """
    Maintains Python compatibility with earlier and newer versions
    :param prompt: version number
    :return: returns version number after going through conditions
    """
    if hexversion > 0x03000000:
        return input(prompt)
    else:
        return raw_input(prompt)


def startProcess():
    firstrun = True
    while True:
        print("_" * 80)
        print('\n')

        if firstrun and len(argv) == 2:
            input_hash = argv[1]
            firstrun = False
        else:
            input_hash = getInput("Enter hash: ")

        if len(input_hash) < 1:
            print("\nNo hash input found.")
        else:
            input_hash = input_hash.strip()

            results = identify_hashes(input_hash)

            if len(results) == 0:
                print("\n\nUnknown or invalid hash.")
            elif len(results) > 2:
                print("\nHash algorithm detection results (sorted by high-low probability): ")
                print("[+] " + results[0])
                print("[+] " + results[1])
                for item in range(int(len(results)) - 2):
                    print("[+] " + results[item + 2])
            else:
                print("\nMost probable hash algorithm: \n")
                for item in range(int(len(results))):
                    print("[+] " + results[item])


# noinspection PyBroadException
def main():
    print(TITLE)
    print(USAGE)
    try:
        startProcess()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception:
        traceback.print_exc(file=stdout)
    exit(0)


if __name__ == "__main__":
    main()
