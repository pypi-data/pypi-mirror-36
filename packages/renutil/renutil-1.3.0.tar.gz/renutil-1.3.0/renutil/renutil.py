import argparse
import requests
import jsonpickle
from sys import exit
from lxml import html
from tqdm import tqdm
from re import compile
from shutil import rmtree
from zipfile import ZipFile
from stat import S_IRUSR, S_IXUSR
from urllib.request import urlopen
from semantic_version import Version
from contextlib import contextmanager
from subprocess import run, PIPE, Popen
from json.decoder import JSONDecodeError
from os.path import exists, expanduser, join, isdir, isfile, getsize, commonprefix, split
from os import mkdir, R_OK, W_OK, access, listdir, remove, environ, uname, chmod, getcwd, chdir


semver = compile(
    r"^((0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(\.(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)?(\+[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*)?)/?$")


CACHE = join(expanduser("~"), ".renutil")
INSTANCE_REGISTRY = join(CACHE, "index.json")


class ComparableVersion():

    def __init__(self, version=None):
        if isinstance(version, str):
            version = Version(version)
        self.version = version

    def __repr__(self):
        return "ComparableVersion(version={})".format(self.version)

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version

    def __lt__(self, other):
        return self.version < other.version

    def __le__(self, other):
        return self.version <= other.version

    def __gt__(self, other):
        return self.version > other.version

    def __ge__(self, other):
        return self.version >= other.version


class RenpyInstance(ComparableVersion):

    def __init__(self, version=None, path=None):
        super(RenpyInstance, self).__init__(version)
        self.path = path
        self.rapt_path = join(self.path, "rapt")
        self.launcher_path = join(self.path, "launcher")

    def __repr__(self):
        return "RenpyInstance(version={}, path='{}', launcher_path='{}')".format(self.version, self.path, self.launcher_path)


class RenpyRelease(ComparableVersion):

    def __init__(self, version=None, url=None):
        super(RenpyRelease, self).__init__(version)
        self.url = url

    def __repr__(self):
        return "RenpyRelease(version={}, url='{}')".format(self.version, self.url)


@contextmanager
def cd(dir):
    prevdir = getcwd()
    chdir(expanduser(dir))
    try:
        yield
    finally:
        chdir(prevdir)


def is_online():
    return True
    # TODO: check to see if we are completely offline or renpy.org itself is down


def scan_instances(path):
    instances = []
    for folder in listdir(path):
        m = semver.match(folder)
        if m:
            try:
                version = Version(m.group(1))
                instances.append(RenpyInstance(version, folder))
            except ValueError:
                continue
    return instances


def assure_state(func):
    def wrapper(args=None, unknown=None):
        if not isdir(CACHE):
            print("Cache directory does not exist, creating it:\n{}".format(CACHE))
            mkdir(CACHE)
        if not access(CACHE, R_OK | W_OK):
            print("Cache directory is not writeable:\n{}\nPlease make sure this script has permission to write to this directory.".format(CACHE))
            exit(1)
        instances = scan_instances(CACHE)
        if not isfile(INSTANCE_REGISTRY):
            print("Instance registry does not exist, creating it:\n{}".format(INSTANCE_REGISTRY))
            with open(INSTANCE_REGISTRY, "w") as f:
                f.write(jsonpickle.encode(instances))
        else:
            for instance in instances:
                add_to_registry(instance)
        return func(args, unknown)
    return wrapper


@assure_state
def call_assure_state(args=None, unknown=None):
    pass


def get_registry(args=None, unknown=None):
    file = open(INSTANCE_REGISTRY, "r")
    try:
        registry = jsonpickle.decode(file.read())
    except JSONDecodeError as e:
        remove(INSTANCE_REGISTRY)
        call_assure_state()
        return None
    return registry


def remove_from_registry(instance):
    registry = get_registry()
    for i, inst in enumerate(registry):
        if inst.version == instance.version:
            del registry[i]
    with open(INSTANCE_REGISTRY, "w") as f:
        f.write(jsonpickle.encode(registry))


def add_to_registry(instance):
    registry = get_registry()
    if not instance in registry:
        registry.append(instance)
        with open(INSTANCE_REGISTRY, "w") as f:
            f.write(jsonpickle.encode(registry))


def get_instance(version):
    if isinstance(version, str):
        try:
            version = Version(version)
        except ValueError:
            return None
    registry = get_registry()
    for instance in registry:
        if instance.version == version:
            return instance
    return None


def valid_version(version):
    if isinstance(version, str):
        try:
            version = Version(version)
        except ValueError:
            return False
    registry = get_registry()
    for instance in registry:
        if instance.version == version:
            return True
    releases = get_available_versions()
    for release in releases:
        if release.version == version:
            return True
    return False


@assure_state
def get_available_versions(args=None, unknown=None):
    if not is_online():
        print("Could not retrieve version list: No connection could be established.")
        exit(1)
    releases = []
    r = requests.get("https://www.renpy.org/dl/")
    tree = html.fromstring(r.content)
    links = tree.xpath("//a/text()")
    for link in links:
        m = semver.match(link)
        if not m:
            continue
        try:
            version = Version(m.group(1))
            url = "https://www.renpy.org/dl/{0}/renpy-{0}-sdk.zip".format(m.group(1))
            release = RenpyRelease(version, url)
            releases.append(release)
        except ValueError:
            continue
    return sorted(releases, reverse=True)


def get_installed_versions(args=None, unknown=None):
    return sorted(get_registry(), reverse=True)


@assure_state
def list_versions(args, unknown):
    if args.available:
        releases = get_available_versions()
        if not releases:
            print("No releases are available.")
        else:
            for release in releases[:args.n]:
                print(release.version)
    else:
        instances = get_installed_versions()
        if not instances:
            print("No instances are currently installed.")
        else:
            for release in instances[:args.n]:
                print(release.version)


def installed(version):
    if isinstance(version, str):
        try:
            version = Version(version)
        except ValueError:
            return False
    for instance in get_registry():
        if instance.version == version:
            return True
    return False


def download(url, dest):
    file_size = int(urlopen(url).headers.get("Content-Length", -1))
    if exists(dest):
        first_byte = getsize(dest)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return
    header = {"Range": "bytes={}-{}".format(first_byte, file_size)}
    progress_bar = tqdm(total=file_size, initial=first_byte, unit="B", unit_scale=True, desc=url.split("/")[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dest, "ab")) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress_bar.update(1024)
    progress_bar.close()


def get_members(zip):
    parts = []
    for name in zip.namelist():
        if not name.endswith('/'):
            parts.append(name.split('/')[:-1])
    prefix = commonprefix(parts)
    if prefix:
        prefix = '/'.join(prefix) + '/'
    offset = len(prefix)
    for zipinfo in zip.infolist():
        name = zipinfo.filename
        if len(name) > offset:
            zipinfo.filename = name[offset:]
            yield zipinfo


@assure_state
def install(args, unknown):
    if installed(args.version):
        print("{} is already installed!".format(args.version))
        exit(1)
    if not valid_version(args.version):
        print("Invalid version specifier!")
        exit(1)

    print("Downloading necessary files...")
    sdk_filename = "renpy-{0}-sdk.zip".format(args.version)
    rapt_filename = "renpy-{0}-rapt.zip".format(args.version)
    folder_name = args.version
    SDK_URL = "https://www.renpy.org/dl/{}/{}".format(args.version, sdk_filename)
    RAPT_URL = "https://www.renpy.org/dl/{}/{}".format(args.version, rapt_filename)
    download(SDK_URL, join(CACHE, sdk_filename))
    download(RAPT_URL, join(CACHE, rapt_filename))

    print("Extracting Ren'Py...")
    sdk_zip = ZipFile(join(CACHE, sdk_filename), "r")
    rapt_zip = ZipFile(join(CACHE, rapt_filename), "r")
    sdk_zip.extractall(path=join(CACHE, folder_name), members=get_members(sdk_zip))
    rapt_zip.extractall(path=join(CACHE, folder_name, "rapt"), members=get_members(rapt_zip))

    print("Installing RAPT...")
    environ["PGS4A_NO_TERMS"] = "no"
    rapt_path = join(CACHE, folder_name, "rapt")
    with cd(rapt_path):
        echo = Popen(["echo", """Y
Y
Y
renutil"""], stdout=PIPE)
        install = Popen(["python2", "android.py", "installsdk"], stdin=echo.stdout, stdout=PIPE)
        for line in install.stdout:
            if args.verbose:
                print(str(line.strip(), "utf-8"))
    del environ["PGS4A_NO_TERMS"]

    print("Registering instance...")
    registry = open(INSTANCE_REGISTRY, "r")
    instances = jsonpickle.decode(registry.read())
    instance = RenpyInstance(args.version, folder_name)
    add_to_registry(instance)

    head, tail = split(get_libraries(instance)[0])
    paths = [join(head, "python"), join(head, "pythonw"),
             join(head, "renpy"), join(head, "zsync"), join(head, "zsyncmake")]
    for path in paths:
        chmod(path, S_IRUSR | S_IXUSR)


@assure_state
def uninstall(args, unknown):
    if not installed(args.version):
        print("{} is not installed!".format(args.version))
        exit(1)
    instance = get_instance(args.version)
    remove_from_registry(instance)
    rmtree(join(CACHE, instance.path))


def get_libraries(instance):
    info = uname()
    platform = "{}-{}".format(info.sysname, info.machine)
    root = instance.path
    root1 = root
    root2 = root
    lib = None
    if "Darwin" in info.sysname:
        platform = "darwin-x86_64"
        root1 = root + "/../Resources/autorun"
        root2 = root + "/../../.."
    elif "x86_64" in info.machine or "amd64" in info.machine:
        platform = "linux-x86_64"
        root1 = root
        root2 = root
    elif re.match(r"i.*86", info.machine):
        platform = "linux-i686"
        root1 = root
        root2 = root
    elif "Linux" in info.sysname:
        platform = "linux-{}".format(info.machine)
        root1 = root
        root2 = root

    for folder in [root, root1, root2]:
        lib = join(CACHE, folder, "lib", platform)
        if isdir(lib):
            break
    lib = join(lib, "renpy")

    if not lib:
        print("Ren'Py platform files not found in '{}'".format(join(root, "lib", platform)))

    if "LD_LIBRARY_PATH" in environ and len(environ["LD_LIBRARY_PATH"]) != 0:
        environ["LD_LIBRARY_PATH"] = "{}:{}".format(lib, environ["LD_LIBRARY_PATH"])

    for folder in [root, root1, root2]:
        base_file = join(CACHE, folder, "renpy.py")
        if isfile(base_file):
            break

    return [lib, "-EO", base_file]


@assure_state
def launch(args, unknown):
    if not installed(args.version):
        print("{} is not installed!".format(args.version))
        args.available = False
        args.n = 5
        list_versions(args, unknown)
        exit(1)
    instance = get_instance(args.version)
    environ["SDL_AUDIODRIVER"] = "dummy"
    cmd = get_libraries(instance)
    if not args.direct:
        cmd += [join(CACHE, instance.launcher_path)]
    cmd += unknown
    try:
        run(cmd)
    except KeyboardInterrupt:
        call_assure_state()
    del environ["SDL_AUDIODRIVER"]


@assure_state
def cleanup(args, unknown):
    if not installed(args.version):
        print("{} is not installed!".format(args.version))
        args.available = False
        args.n = 5
        list_versions(args, unknown)
        exit(1)
    instance = get_instance(args.version)
    paths = [join(instance.path, "tmp"), join(instance.rapt_path, "assets"), join(instance.rapt_path, "bin")]
    for path in paths:
        if isdir(join(CACHE, path)):
            rmtree(join(CACHE, path))


def main():
    parser = argparse.ArgumentParser(description="A toolkit for managing Ren'Py instances via the command line.")
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser("list", aliases=["ls"],
                                        description="List all installed versions of Ren'Py, or alternatively query \
                                        available versions from https://renpy.org/dl.",
                                        help="List Ren'Py versions.")
    parser_list.add_argument("-n",
                             type=int,
                             default=5,
                             help="The number of versions to show")
    parser_list.add_argument("-a", "--available",
                             action="store_true",
                             help="Show versions available to be installed")
    parser_list.set_defaults(func=list_versions)

    parser_install = subparsers.add_parser("install", aliases=["i"],
                                           description="Install the specified version of Ren'Py, including RAPT, set \
                                           up for use via 'renutil launch'.",
                                           help="Install a version of Ren'Py.")
    parser_install.add_argument("version", type=str, help="The version to install in SemVer format")
    parser_install.add_argument("-v", "--verbose", action="store_true", help="Print more information when given")
    parser_install.set_defaults(func=install)

    parser_uninstall = subparsers.add_parser("uninstall", aliases=["u", "remove", "r", "rm"],
                                             description="Uninstall the specified version of Ren'Py, removing all \
                                             related artifacts and cache objects.",
                                             help="Uninstall an installed version of Ren'Py.")
    parser_uninstall.add_argument("version",
                                  type=str,
                                  help="The version to uninstall in SemVer format")
    parser_uninstall.set_defaults(func=uninstall)

    parser_launch = subparsers.add_parser("launch", aliases=["l"],
                                          description="Launch the specified version of Ren'Py, pointing to the \
                                          'launcher' project by default.",
                                          help="Launch an installed version of Ren'Py.")
    parser_launch.add_argument("version",
                               type=str,
                               help="The version to launch in SemVer format")
    parser_launch.add_argument("-d", "--direct",
                               action="store_true",
                               help="Launches the Ren'Py script directly")
    parser_launch.set_defaults(func=launch)

    parser_clear_cache = subparsers.add_parser("cleanup", aliases=["clean", "c"],
                                               description="Clean the temporary build artifacts of the specified version \
                                          of Ren'Py.",
                                               help="Clean temporary files of the specified Ren'Py version.")
    parser_clear_cache.add_argument("version",
                                    type=str,
                                    help="The version to clean in SemVer format")
    parser_clear_cache.set_defaults(func=cleanup)

    args, unknown = parser.parse_known_args()
    if vars(args).get("func", None):
        args.func(args, unknown)
    else:
        print("Type 'renutil -h' to see all available actions")

if __name__ == '__main__':
    main()
