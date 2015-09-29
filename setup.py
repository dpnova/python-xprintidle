# The CFFI docs suggest that you can also use distutils, while technically
# correct you should use setuptools because otherwise you cannot specify
# a dependency on CFFI.
from setuptools import setup
from distutils.command.build import build
from setuptools.command.install import install


# you must import at least the module(s) that define the ffi's
# that you use in your application
def get_ext_modules():
    import xprintidle
    return [xprintidle.ffi.verifier.get_extension()]


class CFFIBuild(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)


setup(
    name="xprintidle",
    version="0.2",
    description="A cffi wrapper around xprintidle.",
    author="David P. Novakovic",
    author_email="davidnovakovic@gmail.com",
    url="https://github.com/dpnova/python-xprintidle",
    py_modules=["xprintidle"],
    install_requires=[
        "cffi",
    ],
    setup_requires=[
        "cffi",
    ],
    cmdclass={
        "build": CFFIBuild,
        "install": CFFIInstall,
    },
    include_package_data=True,
    packages=['src'],
    package_data={'src': ['xprintidle.c']},
    zip_safe=False,
)
