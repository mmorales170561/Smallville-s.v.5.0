
#!/bin/bash
# .devcontainer/setup.sh

# Install requirements
sudo apt-get update && sudo apt-get install -y figlet golang-go

# Create Smallville directory
mkdir -p ~/smallville

# Create the orchestrator (Smallville s.v.5.0)
cat << 'EOF' > ~/smallville/smallville.sh
#!/bin/bash
banner_print() { figlet -f slant "$1"; }

check_tools() {
    for tool in subfinder httpx; do
        if ! command -v $tool &> /dev/null; then
            go install -v github.com/projectdiscovery/$tool/cmd/$tool@latest
            export PATH=$PATH:$(go env GOPATH)/bin
        fi
    done
}

clear
banner_print "ACTION COMICS"
read -s -p "Password: " pass
echo
if [ "$pass" != "superman" ]; then
    echo -e "\e[31mKrypto is barking for you to back off!\e[0m"; exit
fi

for i in {1..3}; do echo -e "\e[5;31mKRYPTON EXPLOSION LOADING...\e[0m"; sleep 0.3; clear; done

banner_print "SMALLVILLE"
read -p "Username: " user
read -s -p "Password: " pword
echo
if [[ "$user" != "clarkkent" || "$pword" != "smallville" ]]; then echo "Access Denied"; exit; fi

cleartarg
banner_print "DAILY PLANET"
echo "Welcome Clark Kent"
echo -e "\e[33mMetropolis Weather (Bakersfield, CA):\e[0m"
curl -s wttr.in/Bakersfield?format=3
echo -e "\n\e[1;36mBREAKING NEWS:\e[0m $(shuf -n 1 -e "Superman can lift 200 quintillion tons." "Superman is powered by yellow sun radiation.")"
read -p "Ready to suit up? (Y/n): " suit

if [[ "$suit" == "Y" || "$suit" == "y" ]]; then
    check_tools
    echo -e "\e[1;36m...entering phone booth...\e[0m"
    sleep 2
    for i in {1..2}; do echo -e "\e[5m...LUTHORCORPS OS LOADING...\e[0m"; sleep 0.5; done
    read -p "Target: " target
    
    clear
    banner_print "BREAKING NEWS"
    echo -e "\e[1;31mSuperman seen in the sky!\e[0m"
    
    subfinder -d "$target" -silent > results.tmp && httpx -l results.tmp -silent > final.tmp 2> error.log
    
    if [ $? -eq 0 ]; then
        banner_print "SAVED THE DAY"
        cat final.tmp
    else
        banner_print "DEATH OF SUPERMAN"
        echo -e "\e[1;31mCause: Kryptonite Error!\e[0m"
    fi
    rm *.tmp
fi
EOF

# Set permissions and alias
chmod +x ~/smallville/smallville.sh
if ! grep -q "alias krypton" ~/.bashrc; then
    echo "alias krypton='~/smallville/smallville.sh'" >> ~/.bashrc
fi