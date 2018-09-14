from distutils.core import setup
from setuptools import find_packages

setup(name='youtube_livechat_messages',
      version='0.1.0',
      description='Youtube LiveChatMessages API wrapper ',
      author='uehara1414',
      author_email='akiya.noface@gmail.com',
      url='https://github.com/uehara1414/youtube_livechat_messages',
      install_requires=[
            'oauth2client',
            'httplib2',
            'requests',
      ],
      packages=find_packages(),
      )
