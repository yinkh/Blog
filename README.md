### 在线站点

[yinkh](https://www.yinkh.top/)

### 说明

本博客由[vmaig_blog](https://github.com/billvsme/vmaig_blog)升级而来，原作者为billvsme。

版本更新记录如下：

- v1.0 2016/12/08

	1. 支持文章仅对本人可见
	2. 使用[summernote](https://github.com/summernote/django-summernote)作为富文本编辑器
	3. 新增添加文章、修改文章界面
	4. 使用[Bootstrap Material Design](https://github.com/FezVrasta/bootstrap-material-design)作为基础样式
	5. 使用[django cleanup](https://github.com/un1t/django-cleanup)自动清理文章封面

- v1.1 2017/08/15

	1. 为新增文章、修改文章绑定权限
	2. 重新设置新增文章、修改文章界面
	3. 默认缺省页
	4. 重写分页显示、变化逻辑，并解决换页时不保留请求参数的错误。
	5. 使用[DjangoFilter](https://github.com/carltongibson/django-filter)进行标签、分类筛选
	6. 用户邮箱激活功能
	7. 站点地图
	8. SEO支持
	9. 使用[DjangoConstance](https://github.com/jazzband/django-constance)动态设置网站标题、SEO等内容
	10. 新闻详情页

- v1.2 2017/09/04

	1. 文章详情界面中有编辑权限的用户可见编辑按钮
	2. NavBar排序
	3. 可修改文章发布时间
	4. [cnzz](http://www.cnzz.com/o_index.php)统计站点访问量
	5. 加入RSS订阅
	6. admin站点兼容移动端
	7. 修复页面无表单时火狐无法读取csrf token错误
	8. 使用ForeignKeyWidget来快速操作博客分类
	9. 使用[Tag-it](http://aehlke.github.io/tag-it/)来输入标签
	10. 动态标签云


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

- 站点名称、描述设置/SEO设置

    请打开admin中的`Constance->Config`面板进行设置，设置将实时生效。

### 样式

不喜欢MD风格的朋友直接删除`common/templates/base.html`中关于`bootstrap-material-design`的css和js即可


### 联系方式

QQ:614457662 有任何改进意见、部署错误等可QQ联系
