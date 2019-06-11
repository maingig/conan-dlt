from conans import ConanFile, CMake, tools

class DltConan(ConanFile):
    name = "dlt"
    version = "2.18.3"
    license = "https://github.com/GENIVI/dlt-daemon/blob/master/LICENSE"
    author = "https://github.com/GENIVI/dlt-daemon/graphs/contributors"
    url = "https://github.com/GENIVI/dlt-daemon.git"
    description = "GENIVI Diagnostic Log and Trace"
    topics = ("dlt", "logging", "C++", "trace")
    settings = "os", "compiler", "build_type", "arch"
    exports = "*"
    options = {
        "shared": [ True, False ],
        "fPIC": [ True, False ],
        "enable_examples": [ True, False ],
        "dlt_ipc" : [ "FIFO", "UNIX_SOCKET" ]
    }
    default_options = {
        'shared': True,
        'fPIC': True,
        'enable_examples': False,
        'dlt_ipc': "UNIX_SOCKET"
    }
    generators = "cmake"
    source_subfolder = "source_subfolder"

    # Custom variables
    source_url = url
    source_branch = "master"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        self.run("git clone %s %s" % (self.source_url, self.name))
        self.run("cd %s && git checkout tags/v%s" % (self.name, self.version))

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["WITH_DLT_EXAMPLES"] = self.options.enable_examples
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["DLT_IPC"] = self.options.dlt_ipc
        cmake.definitions["WITH_DLT_CXX11_EXT"] = "ON"
        cmake.definitions["WITH_DLT_USE_IPv6"] = "OFF"
        if self.settings.os == "QNX":
        	cmake.definitions["__EXT_BSD"] = "ON"
        cmake.configure(source_folder=self.name)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["dlt"]
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(['psapi', 'ws2_32'])
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['pthread'])
        elif self.settings.os == "QNX":
            self.cpp_info.libs.extend(['socket'])
