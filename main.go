// Copyright 2019 Jayson Grace. All rights reserved.
// Use of this source code is governed by a MIT-style
// license that can be found in the LICENSE file.

package main

import (
	"flag"
	"log"
	"os"
	"path/filepath"

	utils "github.com/l50/goutils"
)

var (
	target string
	path   string
)

// init specifies the input parameters that init-bbh-project can take.
func init() {
	home, err := utils.GetHomeDir()
	if err != nil {
		log.Fatalln(err.Error())
	}
	flag.StringVar(&target, "t", "", "Target bug bounty program.")
	flag.StringVar(&path, "p", filepath.FromSlash(home+"/bug_bounty_hunting/"), "Path to folder for bug bounty program work.")
}

// usage prints the usage instructions for init-bbh-project
func usage() {
	os.Args[0] = os.Args[0] + " [options]"
	flag.Usage()
	os.Exit(1)
}

func createProgramFolder() {
	log.Printf("Creating folder for %s at %s", target, path)
	projExists := utils.FileExists(path + target)
	if !projExists {
		_ = os.Mkdir(path+target, 0755)
	} else {
		log.Fatalf("%s already exists, exiting...", filepath.FromSlash(path+target))
	}
}

func createReconFolders() {
	log.Printf("Creating recon folders for %s at %s%s/recon", target, path, target)
	_ = os.Mkdir(path+target+"/recon", 0755)
	_ = os.Mkdir(path+target+"/recon/nmap", 0755)
	_ = os.Mkdir(path+target+"/recon/gobuster", 0755)
	_ = os.Mkdir(path+target+"/recon/dirb", 0755)
}

func createConfigFolder() {
	log.Printf("Creating config folder for %s at %s%s/config", target, path, target)
	_ = os.Mkdir(path+target+"/config", 0755)
}

func setupFolders() {
	createProgramFolder()
	createReconFolders()
	createConfigFolder()
}

func createConfigFile() {
	utils.CreateEmptyFile(filepath.FromSlash(path + target + "/config/" + "target_sites.txt"))
}

func copyReconTool() {
	utils.Cp(filepath.FromSlash("tools/recon.py"), filepath.FromSlash(path+target+"/recon.py"))
}

func getSSTool() {
	utils.CloneRepo("https://github.com/maaaaz/webscreenshot", filepath.FromSlash(path+target+"/webscreenshot"))
}

func main() {
	flag.Parse()

	if flag.NFlag() == 0 {
		usage()
	}

	setupFolders()
	createConfigFile()
	copyReconTool()
	getSSTool()
}
