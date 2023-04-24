import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.33.0"

class SeastarConan(ConanFile):
    name = "seastar"
    description = "ForestDB is a KeyValue store based on a Hierarchical B+-Tree."
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/ForestDB-KVStore/forestdb"
    topics = ("kv-store", "mvcc", "wal")
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    generators = "cmake", "cmake_find_package"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def export_sources(self):
        self.copy("CMakeLists.txt")
#        for patch in self.conan_data.get("patches", {}).get(self.version, []):
#            self.copy(patch["patch_file"])

    def build_requirements(self):
        self.build_requires("ninja/1.11.1")
        self.build_requires("ragel/6.10")

    #xfslibs-dev
    #systemtap-sdt-dev
    def requirements(self):
        self.requires("boost/1.81.0")
        self.requires("c-ares/1.19.0")
        self.requires("cryptopp/8.7.0")
        self.requires("fmt/8.1.1")
        self.requires("gnutls/3.7.8")
        self.requires("hwloc/2.8.0")
        self.requires("libpciaccess/0.17")
        self.requires("lksctp-tools/1.0.19")
        self.requires("lz4/1.9.4")
        self.requires("yaml-cpp/0.7.0")

    def validate(self):
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("Windows Builds Unsupported")
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 11)

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def build(self):
#        for patch in self.conan_data.get("patches", {}).get(self.version, []):
#            tools.patch(**patch)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses/")
        # Parent Build system does not support library type selection
        # and will only install the shared object from cmake; so we must
        # handpick our libraries.
        self.copy("*.a*", dst="lib", src="lib")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.so*", dst="lib", src="lib", symlinks=True)
        self.copy("*.dylib*", dst="lib", src="lib", symlinks=True)
        self.copy("*.dll*", dst="lib", src="lib")
        self.copy("*.hh", dst="include", src="%s/include" % (self._source_subfolder) , keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["forestdb"]
        self.cpp_info.system_libs.extend(["pthread", "m", "dl"])
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["rt"])
