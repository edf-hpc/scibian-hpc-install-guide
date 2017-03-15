#!/usr/bin/python
import ClusterShell.NodeSet
import cgi
import yaml
import sys
import syslog

sys.stderr = sys.stdout
params = cgi.FieldStorage()
target = params.getvalue('node')

print("Content-Type: text/plain")
print("")

config = yaml.load(open('/etc/hpc-config/bootmenu.yaml'))

def lookup_param(key):
    global config, target
    for nodeset in config:
        if nodeset == 'defaults':
            continue
        if target in ClusterShell.NodeSet.expand(nodeset) and key in config[nodeset]:
            return config[nodeset][key]
    return config['defaults'][key]

ipxe_menu = {
    'params'   : {
        'timeout' : '3000',
        'boot'    : 'boot || goto failed',
        'goto'    : 'goto start',
    },
    'menu'    : {
        'scibian8_ram' : {
            'label'  : 'Run Scibian8 in RAM',
            'url'    : "http://" + lookup_param('diskless_server') + "/scibian8",
            'initrd' : '${base-url}/initrd-3.16.0-4-amd64',
            'kernel' : "${base-url}/vmlinuz-3.16.0-4-amd64 initrd=initrd-3.16.0-4-amd64 " + 
                       " console=" + lookup_param('console') +
                       " ethdevice=" + lookup_param('boot_dev') +
                       " ethdevice-timeout=" + lookup_param('dhcp_timeout') +
                       " cowsize=" + lookup_param('cowsize') +
                       " transparent_hugepage=always " +
                       " disk-format=" + lookup_param('disk_format') +
                       " disk-raid=" + lookup_param('disk_raid') +
                       " boot=live " + 
                       " fetch=http://" + lookup_param('diskless_server') + "/scibian8/scibian8.squashfs.torrent " +
                       lookup_param('kernel_opts'),
        },
        'scibian8_disk' : {
            'label'  : 'Install Scibian8',
            'url'    : "http://"+lookup_param('diskinstall_server')+"/disk/scibian8",
            'initrd' : '${base-url}/debian-installer/amd64/initrd.gz',
            'kernel' : "${base-url}/debian-installer/amd64/linux initrd=initrd.gz console="+lookup_param('console')+" url=${base-url}/install_config auto interface="+lookup_param('boot_dev')+" locale=en_US console-keymaps-at/keymap=fr keyboard-configuration/xkb-keymap=fr languagechooser/language-name=English netcfg/get_domain="+lookup_param('domain')+" netcfg/get_nameservers="+lookup_param('nameserver')+" netcfg/no_default_route=true debian-installer/add-kernel-opts=console="+lookup_param('console')+" priority=critical scibian-installer",
        },
        'discovery' : {
            'label'  : 'Discover/Rescue system',
            'url'    : "http://"+lookup_param('diskless_server')+"/scibian8",
            'initrd' : '${base-url}/initrd-3.16.0-4-amd64',
            'kernel' : "${base-url}/vmlinuz-3.16.0-4-amd64 initrd=initrd-3.16.0-4-amd64 console="+lookup_param('console')+" boot=discovery interface="+lookup_param('boot_dev'),
        },
    },
}

print("#!ipxe")
print("#####################################################################")
print("# IPXE Linux menu specification")
print("#####################################################################")
print("set esc:hex 1b            # ANSI escape character - ^[")
print("set cls ${esc:string}[2J  # ANSI clear screen sequence - ^[[2J")
print("menu Please choose an operating system to boot")
print("echo ${cls}")
for key in ipxe_menu["menu"]:
    print("item  "+key+"     "+ipxe_menu["menu"][key]["label"])
    if key == lookup_param('boot_os'):
        menudft = key
if not menudft:
    menudft = 'discovery'
print("choose --default "+menudft+" --timeout "+ipxe_menu["params"]["timeout"]+" target && goto ${target}")

syslog.syslog("generating menu for " + target + " with default kernel: " + ipxe_menu["menu"][menudft]["kernel"] )

for key in ipxe_menu["menu"]:
    print("")
    print(":"+key)
    print("set base-url "+ipxe_menu["menu"][key]["url"])
    print("initrd "+ipxe_menu["menu"][key]["initrd"])
    print("kernel "+ipxe_menu["menu"][key]["kernel"])
    print(ipxe_menu["params"]["boot"])
    print(ipxe_menu["params"]["goto"])
