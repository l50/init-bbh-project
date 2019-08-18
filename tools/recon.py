import argparse
import os
import subprocess
import re

__auth__ = 'Jayson Grace <jayson.e.grace@gmail.com>'


def __parse_args__():
    """Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description='Run a variety of recon tools for bug bounty hunting.')
    parser.add_argument('-d', '--dr', help='Dr. Robot location', required=True)
    parser.add_argument('-s', '--sec', help='SecLists location', required=True)
    return parser.parse_args()

args = __parse_args__()

def __get_name__(site):
    m = re.match(".*\/\/(.*\.\w{3})\/*", site)
    return m.group(1)

def file_to_array(in_file):
    file_contents = []
    with open(in_file) as f:
        for line in f:
            file_contents.append(line.rstrip("\n\r"))
    return file_contents

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

def dr_robot(sites):
    for site in sites:
        print(f"Starting gather phase of dr robot on {site}")
        run_cmd(f"cd {args.dr}; pipenv run python drrobot.py {site} gather -sub -aqua")
        print(f"Copying aggregated hostnames for {site} to {os.path.dirname(os.path.realpath(__file__))}")
        run_cmd(f"cp {args.dr}/output/{site}/aggregated/aggregated_hostnames.txt .")

def dirb(sites):
    for site in sites:
        name = __get_name__(site)
        cmd = f"docker run -v {os.path.dirname(os.path.abspath(__file__))}/dirb:/dirb --rm -it --name=dirb-{name} l505/dirb {site} -o /dirb/{name}"
        print(f"Running the following command: {cmd}")
        run_cmd(cmd)

# https://redteamtutorials.com/2018/11/19/gobuster-cheatsheet/
def gobuster(sites):
    for site in sites:
        name = __get_name__(site)
        cmd = f"gobuster -e -u {site} -w {args.sec}/Discovery/Web-Content/dirb/common.txt -v -f -t 40 -o ./gobuster/{name}.txt"
        print(f"Running the following command: {cmd}")
        run_cmd(cmd)

def nmap(sites):
    for site in sites:
        name = __get_name__(site)
        cmd = f"nmap -sV -p- -A -v -oN recon/nmap/{name} {name}"
        print(f"Running the following command: {cmd}")
        run_cmd(cmd)

def main():
    sites = file_to_array("config/target_sites.txt")
    dirb(sites)
    gobuster(sites)
    nmap(sites)
    print("Recon complete.")


if __name__ == '__main__':
    main()
