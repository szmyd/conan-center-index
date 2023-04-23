from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration

import os

required_conan_version = ">=1.33.0"

class HwlocConan(ConanFile):
    name = "hwloc"
    description = "The Hardware Locality (hwloc) software project"
    license = "BSD-3"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.open-mpi.org/projects/hwloc"
    topics = ("conan", "mpi", "openmpi")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC" :True
    }
    build_requires = (
        "libtool/2.4.7",
    )

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def validate(self):
        if self.settings.os not in ["Linux", "FreeBSD", "Macos"]:
            raise ConanInvalidConfiguration("Only Linux and FreeBSD builds are supported")

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def build(self):
        with tools.chdir(self._source_subfolder):
            self.run("./autogen.sh")
            env_build = AutoToolsBuildEnvironment(self)
            extra_args = list()
            if self.options.shared:
                extra_args.extend(('--enable-static=no',))
            else:
                extra_args.extend(('--enable-shared=no',))
            env_build.configure(".", args=extra_args, build=False, host=False, target=False)
            env_build.make()

    def package(self):
        self.copy("COPYING", src=self._source_subfolder, dst="licenses")
        self.copy("*/hwloc.h", dst="include/", keep_path=False)
        self.copy("*/netloc*.h", dst="include/", keep_path=False)
        self.copy("*.h", dst="include/hwloc", src="%s/include/hwloc" % (self._source_subfolder) , keep_path=False)
        self.copy("*.h", dst="include/netloc", src="%s/include/netloc" % (self._source_subfolder) , keep_path=False)
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so*", dst="lib", keep_path=False, symlinks=True)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
