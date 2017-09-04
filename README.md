### 在线站点

[http://blog.dreamgotech.com/](http://blog.dreamgotech.com/)

### 配置相关
- 替换自己的SECRET_KEY(`Blog/settings.py -> SECRET_KEY`)
- 设置自己的数据库连接(`Blog/settings.py -> DATABASES`)
- 设置验证邮件发送的邮箱账户名和密码(`Blog/settings.py -> EMAIL_HOST_USER/EMAIL_HOST_PASSWORD`)
SMTP端口需要根据您使用的邮箱重新设置
- 生产环境置`DEBUG=False`并重设域名
- 创建虚拟环境

		python -m venv environment

- 开启虚拟环境

	Windows：

	    cd environment;
	    cd Scripts;
	    activate.bat;
	    cd ..;
	    cd ..;

	Linux:

	    source environment/bin/activate

- 安装插件

    	pip install -r requirements.txt -i https://pypi.douban.com/simple

- 创建日志文件

    在根目录创建log文件夹并在log文件夹下新建info.log文件

- 同步数据库

	    python manage.py makemigrations
	    python manage.py migrate

- 创建超级管理员

    	python manage.py createsuperuser

- 开启测试服务器

    	python manage.py runserver 0:80

- [apache2配置](http://blog.dreamgotech.com/article/49/)

- 文章读写权限

	在admin中用户部分选择需要修改权限的用户进行修改，在用户权限部分选中 `article|博客|Can add 博客` 即可在前端添加博客，选中 `article|博客|Can change 博客` 即可在前端修改博客

- cnzz配置

    [cnzz官方站点](http://www.cnzz.com/o_index.php)

    统计代码位于`/common/templates/widgets/footer.html`中

    查看统计代码位于`/common/templates/common/version.html`中（要求在admin中为用户设置查看cnzz权限）

###联系方式
QQ:614457662 有任何改进意见、部署错误等可QQ联系