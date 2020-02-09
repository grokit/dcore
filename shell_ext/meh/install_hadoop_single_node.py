"""
https://hive.apache.org/downloads.html
https://hadoop.apache.org/releases.html
"""

_meta_shell_command = 'install_hadoop_single_node'

import os
import glob

import dcore.env_setup as env_setup
import dcore.osrun as osrun

tag_begin = '# HADOOP_%s_BEGIN' % __file__
tag_end = '# HADOOP_%s_END' % __file__


def install_system_dependencies():
    osrun.run_os('sudo apt install default-jre -y')


UNPACK_COMMANDS = """
mkdir -p ~/apache
tar -xvzf hadoop-3.1.2.tar.gz -C ~/apache
mv ~/apache/hadoop-3.1.2 ~/apache/hadoop
tar -xvzf apache-hive-3.1.1-bin.tar.gz -C ~/apache
mv ~/apache/apache-hive-3.1.1-bin ~/apache/hive
""".strip().splitlines()

SSH_SETUP_COMMANDS = """
mkdir -p ~/.ssh
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""
""".strip().splitlines()

SSH_SETUP_COMMANDS_POST = """
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
""".strip().splitlines()


def setup_bashrc():
    content = """
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
export HADOOP_INSTALL=__hadoop_root__
export PATH=$PATH:$HADOOP_INSTALL/bin:$HADOOP_INSTALL/sbin
""".strip()

    filename = os.path.expanduser('~/.bashrc')

    content = content.replace('__hadoop_root__',
                              os.path.expanduser('~/apache/hadoop'))
    env_setup.updateFileContentBetweenMarks(filename, tag_begin, tag_end,
                                            content, True)


def apply_hadoop_templates():
    """
    :::
    folder = os.path.expanduser('~/apache/hadoop/etc/hadoop/hadoop-env.sh')
    files = glob.iglob(folder + '/**/*.**', recursive=True)
    hadoop_env = [f for f in files if '/etc/hadoop/hadoop-env.sh' in f]
    assert len(hadoop_env) == 1
    hadoop_env = hadoop_env[0]
    """
    filename = os.path.expanduser('~/apache/hadoop/etc/hadoop/hadoop-env.sh')
    assert os.path.isfile(filename)
    # ::::
    # ? export JAVA_HOME=usr/lib/jvm/java-8-openjdk-amd64 ?
    content = """
"""
    env_setup.updateFileContentBetweenMarks(filename, tag_begin, tag_end,
                                            content, True)

    filename = os.path.expanduser('~/apache/hadoop/etc/hadoop/core-site.xml')
    assert os.path.isfile(filename)
    content = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>

<property>
    <name>hadoop.tmp.dir</name>
    <value>/app/hadoop/tmp</value>
    <description>tmp.dir</description>
</property>

<property>
    <name>fs.default.name</name>
    <value>hdfs://localhost:54310</value>
    <description>Default FS.</description>
</property>

</configuration>
"""
    open(filename, 'w').write(content)


def apply_hive_templates():
    pass


def unpack():
    for cmd in UNPACK_COMMANDS:
        cmd = cmd.replace('~', os.path.expanduser('~'))
        osrun.run_os(cmd)


def ssh_config():
    if not os.path.isfile(os.path.expanduser('~/.ssh/id_rsa.pub')):
        for cmd in SSH_SETUP_COMMANDS:
            cmd = cmd.replace('~', os.path.expanduser('~'))
            osrun.run_os(cmd)
    for cmd in SSH_SETUP_COMMANDS_POST:
        cmd = cmd.replace('~', os.path.expanduser('~'))
        osrun.run_os(cmd)


if __name__ == '__main__':
    # assert "safety" == "make sure you want to run this, then uncomment this line"

    # install_system_dependencies()
    # unpack()
    # setup_bashrc()
    apply_hadoop_templates()
    # apply_hive_templates()
    # ssh_config()

    print('Please run `. ~/.bashrc`')
    print('You may also need to run `hadoop namenode -format`')
