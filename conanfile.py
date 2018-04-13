#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class MosquittoConan(ConanFile):
    name = "mosquitto"
    version = "1.4.15"
    description = "Keep it short"
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://mosquitto.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "EPL", "EDL"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "mosquitto.patch", "FindOpenSSL.cmake"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_tls": [True, False], "with_srv": [True, False]}
    default_options = "shared=False", "fPIC=True", "with_tls=True", "with_srv=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    # TODO (uilian): Add options with_websockets and with_uuid (uuid if not apple)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.with_tls:
            self.requires.add("OpenSSL/1.0.2o@conan/stable")
        if self.options.with_srv:
            self.requires.add("c-ares/1.14.0@conan/stable")

    def source(self):
        source_url = "https://github.com/eclipse/mosquitto"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        tools.patch(patch_file="mosquitto.patch", base_path=self.source_subfolder)

    def patch_cmakefile(self):
        # do not install manual
        cmake_file = os.path.join(self.source_subfolder, "CMakeLists.txt")
        tools.replace_in_file(cmake_file, "add_subdirectory(man)", "")
        # do not install example
        install = 'install(FILES mosquitto.conf aclfile.example pskfile.example pwfile.example DESTINATION "${SYSCONFDIR}")'
        tools.replace_in_file(cmake_file, install, "")
        # enable to build static
        cmake_lib_file = os.path.join(self.source_subfolder, "lib", "CMakeLists.txt")
        shared_lib_old = 'add_library(libmosquitto SHARED'
        shared_lib_new = 'add_library(libmosquitto'
        tools.replace_in_file(cmake_lib_file, shared_lib_old, shared_lib_new)
        # enable to install to static
        install_lib_old = 'LIBRARY DESTINATION'
        install_lib_new = 'ARCHIVE DESTINATION "${LIBDIR}" LIBRARY DESTINATION'
        tools.replace_in_file(cmake_lib_file, install_lib_old, install_lib_new)

    def configure_cmake(self):
        cmake = CMake(self, parallel=False)
        cmake.verbose = True
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="edl-v10", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="epl-v10", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend([ "m", "rt", "pthread", "dl"])
        elif self.settings.os == "Macos":
            self.cpp_info.libs.extend(["dl", "m"])
