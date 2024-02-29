## GPIO


#### 验证了IoTest上测试用例正确性

无论是单独发送，还是连续发送都能验证保证其发送和接收的正确性。


#### 测试用例设计方案

##### 测试环境
1. 一端为**IoTest**
2. 另一端为**树莓派**，可能会遇到以下问题，有以下解决方案
    ```c
    ./USB_GPIO_Test: error while loading shared libraries: libusb-0.1.so.4: cannot open shared object file: No such file or directory
    处理方式
    sudo apt-get update
    sudo apt-get install libusb-0.1-4
    ```
3. 执行`shell脚本`需要`sudo`

4. 编译命令
    ```c
     g++ -o gpioinput gpioinput.cpp -I. -L./lib -lGinkgo_Driver -D OS_UNIX -lusb
    ```

5. 所需要的动态链接库移动到`/usr/lib`目录下，防止在设置环境变量时无法找到

##### 测试用例
测试用例设计思路没有考虑连续发送16位数据，应为那样可能需要更多的控制功能。