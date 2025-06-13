- Create a new image in `XenOrchestra`
- Attach the Rodan-Data boot disk (It's an ext4 drive, 100GB. We may need to move to something larger. )
- You will need `nfs-common` to mount the Xen tools iso.
  - From the console menu in XenOrchestra, select the `guest-tools.iso` disk.
  - `apt-get install nfs-common`
  - `mount /dev/cdrom /mnt`
  - `bash /mnt/Linux/install.sh`
  - `umount /dev/cdrom`

### Firewall rules

Only specific IPs are allowed to SSH into the Rodan Staging VM, you may add a new computer if the Lab Manager says this is ok with the following command. All labs on this floor are in this subnet, including the printers. That is why we need to restrict by specific ip, and not by subnet. Do not add your home addresses.

- `ufw allow from 132.206.14.221 proto tcp to any port 22`

The `Staging` server should only be accessible to our subnet. Therefore:

- `ufw allow from 132.206.14.0/24 proto tcp to any port 80,443`

### Install Docker-CE

The current iteration of docker is the Community Edition. You may install it by adding Docker's private repository listing to your package manager.

- Make sure all previous versions of docker is uninstalled.
- Install docker-ce. (Ubuntu)

```bash
sudo apt-get remove docker docker-engine docker.io
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update && sudo apt-get install docker-ce
service docker start
```

- Install docker-ce. (CentOS)

```bash
yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum-config-manager --enable docker-ce-edge
yum-config-manager --enable docker-ce-test
yum-config-manager --disable docker-ce-edge
yum install docker-ce
systemctl start docker
```

### Docker + Firewall

Most the time, people **do not** add `DOCKER_OPTS="--iptables=false"` to `vim /etc/default/docker`. There is very little use case for this, when docker itself uses `iptables` heavily. The docker option `--iptables=false` is not 100% respected, `swarmkit` will still write to `netfilter`.

If you add a deny rule to the iptable/ufw, and a port gets published, the `INPUT` rule is not respected because it is in `FORWARD`. Docker has a table that it will not modify for when you wish to define rules for things related to `FORWARD`.

### Docker + FS (FileSystem) Security

App Armor manages security on a per application basis. Even applications with administrative authority should not have access over the entire filesystem. A security profile, like the one attached, should not need to change very much, but you should do your own due diligence just in case.

- Install app-armor
  - `apt-get install apparmor apparmor-profiles apparmor-utils`
- Create a profile
  - `aa-autodep docker`
- Add custom profile to AppArmor complain
  - `aa-complain docker`
- Customize the rules
  - `aa-logprof`

This is our profile for the Docker application.
Name it and place it here: `/etc/apparmor.d/docker-nginx`

```
#include <tunables/global>


profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,
  network inet icmp,

  deny network raw,

  deny network packet,

  file,
  umount,

  deny /bin/** wl,
  deny /boot/** wl,
  deny /dev/** wl,
  deny /etc/** wl,
  deny /home/** wl,
  deny /lib/** wl,
  deny /lib64/** wl,
  deny /media/** wl,
  deny /mnt/** wl,
  deny /opt/** wl,
  deny /proc/** wl,
  deny /root/** wl,
  deny /sbin/** wl,
  deny /srv/** wl,
  deny /tmp/** wl,
  deny /sys/** wl,
  deny /usr/** wl,

  audit /** w,

  /var/run/nginx.pid w,

  /usr/sbin/nginx ix,

  deny /bin/dash mrwklx,
  deny /bin/sh mrwklx,
  deny /usr/bin/top mrwklx,


  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

Add it to the apparmor parser like this.

- `apparmor_parser -r -W /etc/apparmor.d/docker-nginx`
- `aa-status` to see which configuration files are being enforced.

### Installing Suricata

Suricata is an IDS `Intrusion Detection System`. (Ubuntu)

- `sudo add-apt-repository ppa:oisf/suricata-stable`
- `sudo apt-get update`
- `sudo apt-get install suricata suricata-dbg`

Configure Suricata

- `make install-rules`
- `vim /etc/suricata/suricata.yaml`
- Change `HOME_NET: "[...]"` to `HOME_NET: "[ip of network block to defend]"`
- Change `EXTERNAL_NET: "[...]"` to `EXTERNAL_NET: "!$HOME_NET"`

Test Suricata

- `ethtool -K eth0 gro off lro off`
- `vim /etc/suricata/rules/test.rules`
  - `alert icmp any any -> $HOME_NET any (msg:"ICMP connection attempt"; sid:1000002; rev:1;)`
  - `alert tcp any any -> $HOME_NET 23 (msg:"TELNET connection attempt"; sid:1000003; rev:1;)`
- Add the rule to the yaml file.
- `vim /etc/suricata/suricata.yaml`
  - `rule-files: -test.rules`
- Start Suricata.
- `/usr/bin/suricata -D -c /etc/suricata/suricata.yaml -i eth0`
- Send a request suricata should be listening for.
  - `ping <ip of HOME_NET>`
  - `telnet <ip of HOME_NET>`
- Check the logs
  - `tail -f /var/log/suricata/fast.log`
- Check that suricata has NFQ compatability.
- `/usr/bin/suricata --build-info` and look for `NFQ` between features.

Run Suricata

- `/usr/bin/suricata -D -c /etc/suricata/suricata.yaml -i eth0 -q 0`

```bash
sudo iptables -I INPUT -p tcp --sport 22,80,443  -j NFQUEUE
sudo iptables -I OUTPUT -p tcp --dport 22,80,443 -j NFQUEUE
```

- **Disclamer**: How paranoid do you want to be? Our firewall denies everything except those ports already. We could run ssh on non-privileged ports (>= 1024) (it is set in `/etc/ssh/sshd_config`).

Automatically `Suricata`'s update rules

- `sudo apt-get install oinkmaster`
- `vim /etc/oinkmaster.conf`
  - Write `url = http://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz`
- `vim /etc/suricata/suricata.yaml`
  - `classification-file: /etc/suricata/rules/classification.config`
  - `reference-config-file: /etc/suricata/rules/reference.config`

Start `Oinkmaster`

- `/etc/oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules`

Test rules again

- `/usr/bin/suricata -c /etc/suricata/suricata.yaml -i eth0`
