#!/usr/bin/python3.7

import subprocess
import sys
import time

import fire

arches = {"i386": "i386/", "x86_64": ""}


class Container:
    def __init__(self, name, repo="bowmanjd"):
        self.docker_exe = ["docker"]
        if not sys.platform == "win32":
            self.docker_exe.insert(0, "sudo")
        self.location = f"{repo}/{name}"

    def build(self, filename="Dockerfile", base="ubuntu:bionic", clean=False):
        with open(filename) as f:
            tpl = f.read()
        base_cmd = self.docker_exe + ["build"]
        if clean:
            base_cmd.append("--no-cache")
        version = time.strftime("%y%m%d.%H%M")
        for arch, prefix in arches.items():
            cmd = base_cmd.copy()
            tags = [arch, arch + "-" + base.replace(":", "-")]
            for tag in tags:
                cmd.extend(["-t", f"{self.location}:{tag}"])
            cmd.append("-")
            dockerfile = tpl.format(base=prefix + base, arch=arch)
            subprocess.run(cmd, input=dockerfile, encoding="utf-8")

    def push(self, location):
        cmd = self.docker_exe + ["push", location]
        subprocess.run(cmd)

    def run(self):
        cmd = self.docker_exe + ["run", "-it", "--rm", self.location]
        subprocess.run(cmd)


if __name__ == "__main__":
    fire.Fire(Container)
