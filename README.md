# Maidwatch
The real watcher for your robo maid :)

This tool kicks Xiaomi mi robot vacuum butt to get the work done.

I have this issue when my friend constantly stops in the middle of its cleaning cycle and says its main brush is blocked. Most of the time, the brush itself looks good; I'm assuming this happens because of my carpet. This situation becomes very annoying when I'm out, miss a notification and, when I back home my friend is just sleeping in the middle of a room. 
Pretty much that's why I wrote this tool. It monitors the vacuum and retries it a few times when the following errors occur:
- Error 5: Main brush is blocked
- Error 8: Clear away any obstacles around the robot

It also sends the vacuum back to a dock station if failed to retry.
I'm not going to explain how to install this project, it should be pretty straight forward, and I don't expect somebody will be using this but me. Though if you find this helpful and have some question feel free to ping me

### Configuration
```shell script
cp config_example.yaml config.yaml
python watcher.py
```

### In action
![sampleone](https://github.com/rooty0/maidwatch/blob/master/sample1.png?raw=true)

### Dependencies
- miio
- yaml
- zeroconf==0.26.3