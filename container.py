#!/usr/bin/python3.7

import subprocess
import sys

import fire

arches = {"i386": "i386/", "x86_64": ""}


class Container:
    def __init__(self, name, repo="bowmanjd"):
        self.docker_exe = ["docker"]
        if not sys.platform == "win32":
            self.docker_exe.insert(0, "sudo")
        self.location = f"{repo}/{name}"

    def build(self, filename="Dockerfile", base=None, clean=False, push=True):
        if not base:
            base = "debian:stable-slim"
            default_base = True
        else:
            default_base = False
        with open(filename) as f:
            tpl = f.read()
        base_cmd = self.docker_exe + ["build"]
        if clean:
            base_cmd.append("--no-cache")
        for arch, prefix in arches.items():
            cmd = base_cmd.copy()
            tags = []
            if default_base:
                tags.append(arch)
                if arch == "i386":
                    tags.append("latest")
            tags.append(arch + "-" + base.replace(":", "-"))
            for tag in tags:
                cmd.extend(["-t", f"{self.location}:{tag}"])
            cmd.append("-")
            dockerfile = tpl.format(base=prefix + base, arch=arch)
            subprocess.run(cmd, input=dockerfile, encoding="utf-8")
            if push:
                for tag in tags:
                    self.push(f"{self.location}:{tag}")

    def push(self, location):
        cmd = self.docker_exe + ["push", location]
        subprocess.run(cmd)

    def run(self):
        cmd = self.docker_exe + ["run", "-it", self.location]
        subprocess.run(cmd)


if __name__ == "__main__":
    fire.Fire(Container)
