**To run game:** `python -m referee <red module> <blue module>`

_Note:_ both `<red module>` and `<blue module>` can be the same agent, or different agents

By default, we run `python -m referee agent agent`.

**Permission issues:**
`git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights and the repository exists.`

This can be resolved using the following commands:
`git remote -v && git remote set-url origin https://github.com/am-yang/ai-part-b`
