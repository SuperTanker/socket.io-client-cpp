from conans import ConanFile, CMake, tools
import os


class SocketioclientcppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def configure(self):
        if tools.cross_building(self.settings):
            del self.settings.compiler.libcxx

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.source_folder, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")

    def test(self):
        if tools.cross_building(self.settings):
            if self.settings.os == "Emscripten":
                exe_name = "example.js"
            elif self.settings.os == "Windows":
                exe_name = "example.exe"
            else:
                exe_name = "example"
            assert(os.path.exists(os.path.join("bin", exe_name)))
        else:
            env = ""
            if self.settings.os == "Macos":
                env = "DYLD_FALLBACK_LIBRARY_PATH= DYLD_LIBRARY_PATH=./bin"
            elif self.settings.os == "Linux":
                env = "LD_LIBRARY_PATH=./bin"
            exec_path = os.path.join('bin', 'example')
            self.run("%s %s" % (env, exec_path))
