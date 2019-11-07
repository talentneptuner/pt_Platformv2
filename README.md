# *图文标注平台第二版**

## **requirements**

Django (2.0.5)
django-crispy-forms (1.7.2)
django-formtools (2.1)
django-import-export (1.0.1)
django-pure-pagination (0.3.0)
django-reversion (3.0.0)
Jinja2 (2.9.6)
mysqlclient (1.4.2)
PyMySQL (0.9.3)
xlrd (1.1.0)
xlwt (1.3.0)

## 初次使用

- 修改settings.py中的数据库配置

![数据库配置](https://i.loli.net/2019/11/07/9rcA6tNgljCOnXb.png)

- 删除所有app(user, task, label)的migrations文件夹下的除init文件之外的所有文件

- 在manage.py所在的目录环境下cmd运行以下两句后，数据库即创建成功

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

- 运行以下命令并按照步骤执行创建超级用户

  ```
  python manage.py create superuser
  ```

- 运行以下命令来运行系统

  ```
  python manage.py runserver 0.0.0.0:80
  ```

  

## 开始标注任务

- 进入```你的ip/admin```并登录刚刚创建的超级用户账号

- 进入标注任务界面，创建一个标注任务

  ![创建任务](https://i.loli.net/2019/11/07/EoqtKWOrgi5LIZs.png)



- 创建标注任务后，进入大类标签界面，创建标注的大类标签，然后进入字类标签界面创建子类标签；当然也可以通过任务列表右侧的快速按钮就添加大类标签，同理也可以通过大类标签右侧的快速标签添加子类标签

- 在用户界面创建用户，输入用户名(不可重复)和密码，创建一个非管理员用户

- 导入数据，将数据导入到task_dataitem表中，格式为(mid, txt, img_name, time, task_id), mid是自定义id，time是时间，task_id是任务id可以在任务列表看到，该界面提供了导入功能但是现在存在bug正在修改，推荐自行导入

- 将图片放入media文件夹中

- 回到```你的ip/```界面，以管理员身份登录，找到你的添加任务，点击去分配人员，选择要参加标注任务的人员和每条数据要被标注的次数，开始分配任务

  ![分配](https://i.loli.net/2019/11/07/k4UrfNdbvGoIs1P.png)

- 分配任务完毕后，你刚刚创建的非管理员用户就可以登陆系统并选择对应的任务开始标注了