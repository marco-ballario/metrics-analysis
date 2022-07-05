#!/bin/bash


declare -a repos=("FastCSV" "java-jwt" "jsoup" "Java-WebSocket")
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
Color_Off='\033[0m'
Yellow='\033[0;33m'
Green='\033[0;32m'
Blue='\033[0;34m'

# Download and build rust-code-analysis
if [ -d "./rust-code-analysis" ]
then
    echo -e "${Yellow}Updating rust-code-analysis...${Color_Off}"
    cd rust-code-analysis
    git checkout -f master
    git pull
    cargo build -p rust-code-analysis-cli --release
    cd ../
    echo -e "${Green}rust-Code-analysis updated!${Color_Off}"
else
    echo -e "${Yellow}Cloning and building rust-code-analysis...${Color_Off}"
    git clone "https://github.com/mozilla/rust-code-analysis.git"
    cd rust-code-analysis
    cargo build -p rust-code-analysis-cli --release
    cd ../
    echo -e "${Green}rust-code-analysis ready!${Color_Off}"
fi
read -p "$(echo -e ${Blue}"Press enter to continue"${Color_Off})"


# Download repositories to measure
if [ -d "./repositories" ]
then
    echo -e "${Yellow}Repositories already downloaded${Color_Off}"
    cd repositories
    for i in ${!urls[@]}
    do
        echo -e "${Yellow}Updating ${repos[$i]}...${Color_Off}"
        cd ./${repos[$i]}
        git checkout -f master
        git pull
        cd ../
        echo -e "${Green}${repos[$i]} updated!${Color_Off}"
    done
    cd ../
else
    echo -e "${Yellow}Download repositories...${Color_Off}"
    mkdir repositories
    cd repositories
    for i in ${!urls[@]}
    do
        echo -e "${Yellow}Cloning ${repos[$i]}...${Color_Off}"
        git clone ${urls[$i]}
        echo -e "${Green}${repos[$i]} cloned!${Color_Off}"
    done
    cd ../
    echo -e "${Green}Repositories downloaded!${Color_Off}"
fi
read -p "$(echo -e ${Blue}"Press enter to continue"${Color_Off})"


# Produce metrics
for i in "${!repos[@]}"
do
    declare -a repo="${repos[$i]}"
    for version in ${versions[$i]}
    do
        echo -e "${Yellow}Producing $repo $version metrics...${Color_Off}"
        mkdir -p ./data/$repo/$version
        cd ./repositories/$repo/
        git checkout $version
        cd ../../rust-code-analysis/
        cargo run -p rust-code-analysis-cli --release -- -m -p ../repositories/$repo/ -O json -o ../data/$repo/$version/ -l Java
        cd ../
        echo -e "${Green}$repo $version metrics produced!${Color_Off}"
    done
done
