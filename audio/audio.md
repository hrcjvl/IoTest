## AUDIO


#### IoTest

1. 根目录下添加了配置文件`filepath.properties`, 配置了音频播放和保存的文件路径，配置文件内容如下:   
    ``` 
    srcAudioLocation=/resources/audio/srcAudio.wav
    destAudioLocation=/resources/audio/destAudio.wav
    ```
2. 根目录下`resources`文件夹下添加`audio`文件夹，并保存`srcAudio.wav，destAudio.wav`音频文件。

~~3. 运行`AudioTest.java`，音频文件播放。~~


#### 最新版本

1. 继承上面提到的功能

2. 添加`process_audio(thresold=0.6)`方法，用于音频处理

3. 在构建测试用例时，右上角参数栏设置了`RecordTime`录制时长，默认值为`10s`

4. 使用代码验证，`result=process_audio(你想设置的阈值)`，`result`为`true`则通过，否则失败