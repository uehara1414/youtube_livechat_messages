# youtube_livechat_messages
Youtube LiveChatMessages list API wrapper.


## Installation
```sh
pipenv install youtube_livechat_messages
```

## Quick Start
```python
import os
from youtube_livechat_messages import get_credentials, API

credentials = get_credentials()

api = API(credentials=credentials)

for item in api.cursor(video_id=os.getenv('VIDEO_ID')):
    print(item)

```

## Todo
- [ ] 動画終了時の処理

## Contributing
個人的に必要な状況で十分に使える程度の実装しかしていません。
足りない機能、不具合などたくさん有るかと思うので、バグ報告・要望・修正はIssues, PullRequests にお気軽に。
気づいていないようであれば [uehara1414](https://twitter.com/uehara1414/)にDMかメンションしてください。
