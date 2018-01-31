#!/bin/bash
#Date:20180117-v1

# 安装阿里云yum源，更新kernel
yum_install()
{
	rm -rf /etc/yum.repo.d/*
	curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
	yum install kernel-3.10.0-693.11.6.el7 -y
	yum -y install git

}
yum_install


# 检查docker&docker-compose是否安装
docker_install()
{
	yum install https://mirrors.aliyun.com/docker-ce/linux/centos/7/x86_64/stable/Packages/docker-ce-17.12.0.ce-1.el7.centos.x86_64.rpm -y
    curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    systemctl start docker && systemctl enable docker
}
docker_install


# pull docker包
pull_docker()
{
	cd ~
	git clone http://git.listenrobot.com/yunwei/old-telemarket-deploy.git
	docker login --username=deploy-ls@sun-person -p Deployls1  registry.cn-hangzhou.aliyuncs.com
	cd old-telemarket-deploy
	sh 1create_secrete.sh
	docker-compose up -d
	sh create_db.sh
	sleep 1
	docker-compose down -v && mv data/postgresql/db/ data/postgresql/db_new_bk && docker-compose up -d mongodb && docker-compose up -d tm-postgersql
}

pull_docker


# 导入数据
import_data()
{
	cd ~
	read -p "please input ip last number:" num
	tar -zxvf $num_backup.tar.gz /backup/
	cp -rf backup/mongo/* /root/old-telemarket-deploy/data/mongodb/dump/
	cp -rf backup/pg/dbexport.pgsql ~/old-telemarket-deploy/data/postgresql/dump/
	sleep 2
	cd old-telemarket-deploy
	sh restore_mongo.sh
	docker-compose exec tm-postgersql bash /bin/restore_pgsql.sh
}
import_data


# 重建Mongo索引
mongo_index()
{
	docker-compose exec mongodb mongo --username yfsrobot  --password yfsrobotksdw1212180 --authenticationDatabase admin <<EOF

	use yfsrobot
	db.getCollectionNames().forEach(function(collName) {
	db.runCommand({dropIndexes: collName, index: "*"});
	});
EOF

	cd /root/old-telemarket-deploy && docker-compose up -d
	cd /root/old-telemarket-deploy && ./create_db.sh

}
mongo_index


# 重启docker
restart_docker()
{
	docker-compose up -d
	./create_db.sh
}
restart_docker


