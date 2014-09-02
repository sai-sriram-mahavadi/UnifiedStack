from subprocess import call,Popen,PIPE
from os import chdir
"""This module is installing the prerequistes required for cobbler"""
def installPrerequites():
    """Python-pip and git are being installation are not among the
       prerequistes for cobbler"""
    out=call(["yum", "update"])
    if out:
        return
    out=call(["yum","-y","install","python-pip"])
    if out:
        return
    out=call(["yum","-y","install","git"])
    if out:
        return
    #python-Pygments is required for installing python-cheetah
    #using rpm -qa first it is being checked that python_pygments
    #is already installed or not. If not then it first downloaded
    #from the specified URL in the /tmp and then it is installed.
    p=Popen("rpm -qa | grep python-Pygments",shell= True,stdout=PIPE)
    out,err=p.communicate()
    if out=='':
        out=call(["wget","-P","/tmp","ftp://ftp.icm.edu.pl/vol/rzm3/linux-opensuse/factory/repo/oss/suse/noarch/python-Pygments-1.6-6.2.noarch.rpm"])
        if out:
            return
        out=call(["yum","-y","install","/tmp/python-Pygments-1.6-6.2.noarch.rpm"])
        if out:
            return
    else:

        out=call(["yum","update","python-Pygments"])
        if out:
            return
    p=Popen("rpm -qa | grep epel-release",shell= True,stdout=PIPE)
    out,err=p.communicate()
    if out=='':
        #find latest release and download
        url="http://download.fedoraproject.org/pub/epel/beta/7/x86_64"
        p=Popen("wget -q -O- "+ url + " | grep  epel-release", shell=True,stdout=PIPE,stderr=PIPE)
        epel_filename,err=p.communicate()
        if err!='':
            return
        if epel_filename=='':
            print "No release found for epel at " + url
            return
        epel_filename=epel_filename[epel_filename.find('>')+1:]
        epel_filename=epel_filename[:epel_filename.find('<')]
        #Fix below line. When doing stdout=PIPE the output is going to out, but when
        #doing stdout=PIPE and stderr=PIPE the output is going to stderr thus when checking
        #err after out,err=p.communicate() it is not '' i.e not empty
        p=Popen("wget -P /tmp " + url + "/" + epel_filename,shell=True)
	p=Popen("yum -y install /tmp/" + epel_filename, shell=True,stderr=PIPE)
        out,err=p.communicate()
        if err!='':
            return
    else:
        out=call(["yum","update","epel-release"])
        if out:
            return
    out=call(["yum","-y","install","createrepo","httpd","mkisofs","mod_wsgi","mod_ssl","python-cheetah",\
        "python-netaddr","python-simplejson","urlgrabber","PyYAML","rsync","syslinux","tftp-server",\
        "yum-utils","Django"])
    if out:
        return
     print "Pre-Requistes Installed. Continuing to Cobbler installation"

if __name__=="__main__":
    installPrerequites()

