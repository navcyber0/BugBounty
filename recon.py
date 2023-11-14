import sys
import subprocess
import time
import os
import json
import glob

def run_amass(domain):
    print("[*] Running amass...")
    result = subprocess.run(["amass", "enum", "-passive", "-d", domain, "-o", f"{domain}/amass.txt"], capture_output=True, text=True)
    print(result.stdout)

def run_subfinder(domain):
    print("[*] Running subfinder...")
    result = subprocess.run(["subfinder", "-d", domain, "-o", f"{domain}/subfinder.txt"], capture_output=True, text=True)
    print(result.stdout)

def run_crtsh(domain):
    print("[*] Running ctfr...")
    result = subprocess.run(["python3", "crtsh.py", "-d", domain, "-o", f"{domain}/crt.txt"], capture_output=True, text=True)
    print(result.stdout)

def run_nuclei(domain):
    print("[*] Running nuclei...")
    result = subprocess.run(["nuclei", "-l", f"{domain}/recon_all.txt", "-t", f"~/nuclei-templates/", "-o", f"{domain}/vulns.txt"], capture_output=True, text=True)
    print(result.stdout)

def run_aquatone(domain):
    print("[*] Running aquatone...")
    result = subprocess.run(["cat", f"{domain}/recon_all.txt", "|", "aquatone", "-out", f"{domain}/aquatone", "-ports", "xlarge"], capture_output=True, text=True)
    print(result.stdout)

def main(domain):
    start_time = time.time()

    # Create directory for the domain
    os.makedirs(domain, exist_ok=True)

    run_amass(domain)
    run_subfinder(domain)
    run_crtsh(domain)

    # Combine all subdomains into a single file
    subprocess.run(f"cat {domain}/amass.txt {domain}/subfinder.txt {domain}/crt.txt {domain}/subbrute.txt | sort -u > {domain}/subdomains.txt", shell=True)

    # Identify active hosts
    print("[*] Running httpx...")
    result = subprocess.run(f"httpx -l {domain}/subdomains.txt -silent -threads 50 -o {domain}/recon_all.txt", shell=True, capture_output=True, text=True)
    print(result.stdout)

    # Inject subdomains into nuclei
    run_nuclei(domain)

    # Take screenshots of the subdomains
    run_aquatone(domain)

    # Print total execution time
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 recon.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"[*] Starting reconnaissance for domain: {domain}")

    main(domain)
