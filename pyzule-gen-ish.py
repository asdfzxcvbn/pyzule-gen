#!/usr/bin/env python3
# pyzule-gen, used to generate .pyzule files: github.com/asdfzxcvbn/pyzule-gen
import os
import json
import atexit
import argparse
from zipfile import ZipFile, ZIP_DEFLATED
from tempfile import TemporaryDirectory as td

parser = argparse.ArgumentParser(description="a tool to generate .pyzule files.")
parser.add_argument("-o", metavar="output", type=str, required=True,
                    help="the name of the .pyzule file to generate")
parser.add_argument("-n", metavar="name", type=str, required=False,
                    help="modify the app's name")
parser.add_argument("-v", metavar="version", type=str, required=False,
                    help="modify the app's version")
parser.add_argument("-b", metavar="bundle id", type=str, required=False,
                    help="modify the app's bundle id")
parser.add_argument("-m", metavar="minimum", type=str, required=False,
                    help="change MinimumOSVersion")
parser.add_argument("-x", metavar="entitlements", type=str, required=False,
                    help="a file containing entitlements to sign the app with")
parser.add_argument("-l", metavar="plist", type=str, required=False,
                    help="a plist to merge with the existing Info.plist")
parser.add_argument("-r", metavar="url", type=str, required=False,
                    help="url schemes to add", nargs="+")
parser.add_argument("-f", metavar="files", nargs="+", type=str,
                    help="tweak files to inject into the ipa")
parser.add_argument("-u", action="store_true",
                    help="remove UISupportedDevices")
parser.add_argument("-w", action="store_true",
                    help="remove watch app")
parser.add_argument("-d", action="store_true",
                    help="enable files access")
parser.add_argument("-s", action="store_true",
                    help="fakesigns the ipa (for use with appsync)")
parser.add_argument("-e", action="store_true",
                    help="remove app extensions")
parser.add_argument("-g", action="store_true",
                    help="remove encrypted extensions")
parser.add_argument("-p", action="store_true",
                    help="inject into @executable_path")
parser.add_argument("-t", action="store_true",
                    help="use substitute instead of substrate")
args = parser.parse_args()

if not any((args.f, args.u, args.w, args.m, args.d, args.n, args.v, args.b, args.s, args.e, args.r, args.x, args.l)):
    parser.error("at least one option to modify the ipa must be present")
elif args.m and any(char not in "0123456789." for char in args.m):
    parser.error(f"invalid OS version: {args.m}")
elif args.x and not os.path.isfile(args.x):
    parser.error("the entitlements file does not exist")
elif args.l and not os.path.isfile(args.l):
    parser.error("the plist to merge does not exist")
elif args.f and (nonexistent := ", ".join(ne for ne in args.f if not os.path.exists(ne))):
    # yes, TOTALLY required. bc we have PROPER GRAMMAR 'round here!
    if not nonexistent.count(", "):
        print(f"[!] {nonexistent} does not exist")
    else:
        print(f"[!] {nonexistent} do not exist")
    exit(1) 


@atexit.register
def cleanup() -> None:
    try:
        print("[*] deleting temporary directory..")
        tmpdir.cleanup()
    except NameError:
        pass


tmpdir = td()
args.o = os.path.normpath(args.o)
if not args.o.endswith(".pyzule"):
    args.o += ".pyzule"
if os.path.exists(args.o):
    overwrite = input(f"[<] {args.o} already exists. overwrite? [Y/n] ").lower().strip()
    if overwrite in ("y", "yes", ""):
        del overwrite
    else:
        print("[>] quitting.")
        exit()

real_args = dict(vars(args))
del real_args["o"]
for key in "fxl":
    if real_args[key]:
        real_args[key] = True
    else:
        del real_args[key]
used = {k: v for k, v in real_args.items() if v}

print("[*] generating..")
with ZipFile(args.o, "w", ZIP_DEFLATED, compresslevel=4) as zf:
    with zf.open("config.json", "w") as f:
        f.write(json.dumps(used).encode())

    if args.f:
        for i in args.f:
            if os.path.isfile(i):
                zf.write(i, f"inject/{os.path.basename(i)}")
            else:  # i fucking hate the zipfile module.
                for dp, _, files in os.walk(i):
                    for f in files:
                        thing = os.path.join(dp, f)
                        zf.write(thing, f"inject/{os.path.relpath(thing, os.path.dirname(i))}")

    if args.x:
        zf.write(args.x, "new.entitlements")

    if args.l:
        zf.write(args.l, "merge.plist")
