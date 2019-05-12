# Dynamically generated ipset from public sources

## Requirements

- Python version >=3.6

## How to install
```
pip3 install urllib3
pip3 install pyyaml
cd /opt
git clone https://github.com/heximcz/ipset-blacklist.git
cd ./ipset-blacklist
cp ./config-default.yml ./config.yml
vim ./config.yml
```

## Usage is very easy. Here is some couple config examples

- create huge blacklist ipset

```
ipset:
    # drop all
    blacklist-total:
        ipset-name: blacklist
        list:
            - "http://www.spamhaus.org/drop/drop.txt"
            - "http://www.spamhaus.org/drop/drop.txt"
            - "http://www.spamhaus.org/drop/edrop.txt"
            - "http://lists.blocklist.de/lists/all.txt"
            - "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
            - "https://www.turris.cz/greylist-data/greylist-latest.csv"
        file: 

ipset-temp: tempxlist
verbose: False
```

- create blacklist with my custom file contains ip addresses

```
ipset:
    # drop all
    blacklist-total:
        ipset-name: blacklist
        list:
            - "http://www.spamhaus.org/drop/drop.txt"
        file: "/opt/my-blacklist.txt"

ipset-temp: tempxlist
verbose: False
```

- create multiple ipset

```
ipset:
    blacklist-total:
        ipset-name: blacklist
        list:
            - "http://www.spamhaus.org/drop/drop.txt"
            - "http://www.spamhaus.org/drop/drop.txt"
            - "http://www.spamhaus.org/drop/edrop.txt"
            - "http://lists.blocklist.de/lists/all.txt"
            - "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
            - "https://www.turris.cz/greylist-data/greylist-latest.csv"
        file: "/opt/my-blacklist.txt"

    blacklist-port:
        ipset-name: blacklist-port
        list:
            - "http://www.ipdeny.com/ipblocks/data/countries/cn.zone"
            - "http://www.ipdeny.com/ipblocks/data/countries/tr.zone"
        file:

    whitelist:
        ipset-name: whitelist
        list:
            - "http://www.ipdeny.com/ipblocks/data/countries/cz.zone"
            - "http://www.ipdeny.com/ipblocks/data/countries/sk.zone"
        file:

ipset-temp: tempxlist
verbose: False
```

## Run script
```
python3 /opt/ipset-blacklist/blacklists.py 
```
Running the script is safe. First, the temp ipset is created, and it is swapped into the original ipset when process is done.
 
Amazing and as always, Enjoy!

