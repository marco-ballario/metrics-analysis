#!/bin/bash

declare -a repos=(
    "FastCSV"
    "java-jwt"
    "jsoup"
    "Java-WebSocket"
)
declare -a urls=(
    "https://github.com/osiegmar/FastCSV.git"
    "https://github.com/auth0/java-jwt.git"
    "https://github.com/jhy/jsoup.git"
    "https://github.com/TooTallNate/Java-WebSocket.git"
)
declare -a versions=(
    "v2.2.0 v2.1.0"
    "4.0.0 3.19.2"
    "jsoup-1.15.2 jsoup-1.15.1"
    "v1.5.3 v1.5.2"
)
color_off='\033[0m'
yellow='\033[0;33m'
green='\033[0;32m'
blue='\033[0;34m'

# Download and build rust-code-analysis
if [ -d "./repositories/rust-code-analysis" ]
then
    echo -e "${yellow}Updating rust-code-analysis...${color_off}"
    cd repositories/rust-code-analysis/
    git checkout -f master
    git pull
    cargo build -p rust-code-analysis-cli --release
    cd ../../
    echo -e "${green}rust-code-analysis updated!${color_off}"
else
    echo -e "${yellow}Cloning and building rust-code-analysis...${color_off}"
    cd repositories/
    git clone "https://github.com/mozilla/rust-code-analysis.git"
    cd rust-code-analysis/
    cargo build -p rust-code-analysis-cli --release
    cd ../../
    echo -e "${green}rust-code-analysis ready!${color_off}"
fi
read -p "$(echo -e ${blue}"Press enter to continue"${color_off})"

# Download repositories to measure
for i in ${!urls[@]}
do
    declare -a repo=${repos[$i]}
    declare -a url=${urls[$i]}
    if [ -d "./repositories/$repo" ]
    then
        echo -e "${yellow}Updating $repo...${color_off}"
        cd ./repositories/$repo
        git checkout -f master
        git pull
        cd ../../
        echo -e "${green}$repo updated!${color_off}"
    else
        echo -e "${yellow}Cloning $repo...${color_off}"
        mkdir repositories/$repo
        cd repositories/$repo
        git clone $url
        cd ../../
        echo -e "${green}$repo cloned!${color_off}"
    fi
done
read -p "$(echo -e ${blue}"Press enter to continue"${color_off})"

# Produce metrics
for i in "${!repos[@]}"
do
    declare -a repo="${repos[$i]}"
    for version in ${versions[$i]}
    do
        echo -e "${yellow}Producing $repo $version metrics...${color_off}"
        mkdir -p ./data/$repo/$version
        cd ./repositories/$repo/
        git checkout $version
        cd ../rust-code-analysis/
        cargo run -p rust-code-analysis-cli --release -- -m -p ../$repo/ -O json -o ../../data/$repo/$version/ -l Java
        cd ../../
        echo -e "${green}$repo $version metrics produced!${color_off}"
    done
done
