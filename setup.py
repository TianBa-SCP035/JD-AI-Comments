from setuptools import setup, find_packages

# 定义包的元信息
setup(
    name='comment-analyze-app',  # 包名
    version='0.1',  # 版本号
    packages=find_packages(),  # 自动查找包
    include_package_data=False,  # 包含包内的数据文件
    install_requires=[
        'fastapi==0.110.0',
        'jieba==0.42.1',
        'langchain==0.1.11',
        'langchain_core==0.1.30',
        'pydantic==2.6.3',
        'snownlp==0.12.3',
        'sumy==0.11.0',
        'uvicorn==0.28.0',
    ],
    entry_points={  # 可执行脚本入口点
        'console_scripts': [
            'comment-analyze-app = main:main',  # 你的主模块和函数
        ],
    },
    description='评论分析，评论压缩接口',  # 包的描述
    long_description='',  # 包的详细描述，通常从README文件中读取
    long_description_content_type='text/markdown',  # 详细描述的内容类型
    url='https://github.com/your-username/your-fastapi-app',  # 项目URL
    author='yancongcong',  # 作者名
    author_email='yancongcong@ilarge.cn',  # 作者邮箱
    classifiers=[  # 包分类信息
        'Environment :: Web Environment',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # 其他分类...
    ],
)