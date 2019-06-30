class Configuration:

    # selenium param
    selenium={
        # # 环境一
        # 'chrome_driver_path': '/usr/bin/',  # chromedriver路径，若已经添加到系统path则可为‘’
        # 'chrome_use_dir_path': '/usr/bin/chromeOptions',  # chrome(49版本) 用户配置文件夹路径，window开发环境配置
        # 'temp_dir': '/opt/azkaban/scripts/python/tmp'

        # 环境二：windows开发环境
        # 'chrome_driver_path':'E:\\Workspace\\Python\\Python库\\selenium\\chromedriver.exe', # chromedriver路径，若已经添加到系统path则可直接写‘chromedriver.exe’
        # 'chrome_use_dir_path': 'E:\\Workspace\\Python\\Python库\\selenium\\chromeOptionsTest3',
        # 'temp_dir': 'e:\\crawler_data\\tmp',
    }


conf = Configuration()
