did you buy raspberry pi and you can't get access from WAN?
===
I know you pain, I have private ip address too.
This script will help you deal with this problem
#all you need:
- pyhon3
- apache2
- dataplicity agent and account installed
- ngrok account (as many as you will need tunnels at once)

### download git
``` 
git clone https://github.com/RandomGuy090/tunnelToPublicAddresses
cd  tunnelToPublicAddresses
```

## how to get prepared?
### 1. install apache and python
``` 
sudo apt-get install apache2 python3
```

### 2 create account at https://www.dataplicity.com/
![1](https://user-images.githubusercontent.com/64653975/117491269-42fce500-af70-11eb-9338-392e318e2571.png)
### 3 verify email and set password
### 4 install agent with commad given after verification
e.g.
```
curl -s https://www.dataplicity.com/unique_id.py | sudo python
```
![2](https://user-images.githubusercontent.com/64653975/117491272-442e1200-af70-11eb-9223-20405783bc0c.png)

#5 open new device and enable wormhole
![3](https://user-images.githubusercontent.com/64653975/117491274-455f3f00-af70-11eb-8461-85d97a176784.png)
![4](https://user-images.githubusercontent.com/64653975/117491276-45f7d580-af70-11eb-9c62-12bde945998c.png)
### 6 open address got from wormhole
### 7 create accounts at https://ngrok.com/
### 8 download ngrok 
```
cd tunnelToPublicAddresses/ngrok
curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok.zip
```
### 9 get authtoken and paste in ```tokens``` file

## running script 
run python script 
```
python3 run.py -n <protocol> <port> <name>
```
e.g.
```
python3 run.py -n http <5000> <testName>
```
![5](https://user-images.githubusercontent.com/64653975/117494417-95400500-af74-11eb-9afd-da6e04071748.png)

script will create new screen session with tunnel dashboard. Screen session will be still runnig after close terminal!

## run at startup
edit line with ```ExecStart```in ```tunnels.service```, and put there absolute path to the ``` run.sh ``` script

### copy example config directory
```
cp -r .ngrokConfigTemplate .{name}
```
and edit ```ngrok.yaml``` file in copied directory

```
authtoken: YOUR_AUTHTOKEN
log_level: info
log_format: json
log: /tunnelToPublicAddresses/.ngrokConfingTemplate/logs
tunnels:
 http:
  proto: http
  addr: 5001
 ```
replace ``` YOUR_AUTHTOKEN``` with token from account you want to use
replace ``` /tunnelToPublicAddresses/.ngrokConfingTemplate/logs``` with path to log files
replace ``` http:``` after (```tunnels```) with your name
replace ``` http:``` after (```proto:```) with protocol do you want to use (tcp or http)
replace ``` addr:```  with port witch you want to forward

### edit run.sh file
copy commented line and personalise 
``` 
/absolute/path/ngrok/./ngrok start -config /absolute/path/.name_of_config/ngrok.yml  name &
```
### add ```tunnels.service``` to the systemd directory 
```
sudo cp -r  tunnels.service /etc/systemd/system/
```
### test start
```
sudo systemctl start tunnels.service
```
and check status
```
sudo systemctl status tunnels.service
```
after ~ one minute in ```/var/www/html``` should appear new file with tunnel's address<br>
tcp tunnels will be a ```.txt``` fille, and http will be ```.html``` pages with redirection to the tunnel address<br>
<br>
To get access to the first http tunnel go to the: https://example-wormhole-2137.dataplicity.io/index.html<br>
To get access to the first tcp tunnel go to the: https://example-wormhole-2137.dataplicity.io/ip.txt


