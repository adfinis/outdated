#!/usr/bin/env python

from os import mkdir
from shutil import rmtree
from tomllib import loads

from jinja2 import Environment, FileSystemLoader

if __name__ == "__main__":
    with open("./timers.toml", "r") as f:
        timers = loads(f.read())["timer"]
    if not timers:
        exit()
    env = Environment(loader=FileSystemLoader("./templates"))
    templates = {
        "service": env.get_template("service"),
        "timer": env.get_template("timer"),
    }
    rmtree("output")
    mkdir("output")
    for timer in timers:
        base_path = "./output/outdated-" + timer["command"]
        for type in ["service", "timer"]:
            with open(f"{base_path}.{type}", "w") as f:
                f.write(templates[type].render(**timer))
