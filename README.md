![Gatekeeper](https://socialify.git.ci/zuo-shi-yun/Gatekeeper/image?description=1&descriptionEditable=QChatGPT%E7%9A%84%E7%9C%8B%E9%97%A8%E7%8B%97%EF%BC%8C%E5%8C%85%E5%90%AB%E9%BB%91%E7%99%BD%E5%90%8D%E5%8D%95%E3%80%81%E4%B8%B4%E6%97%B6%E7%94%A8%E6%88%B7%E6%9C%BA%E5%88%B6&logo=https%3A%2F%2Fi.postimg.cc%2FJ4D42xfw%2Fpug.png&name=1&theme=Light)
包含黑名单、白名单、临时用户机制的看门狗，保护流量的守门人。<br/>
(本插件运行于[QChatGPT](https://github.com/RockChinQ/QChatGPT))<br/>
下图是默认配置下的系统流程。
[![image.png](https://i.postimg.cc/ZntkCP5g/image.png)](https://postimg.cc/sQcHLhS9)
<details>
<summary> 

## :muscle:插件功能

</summary>

<details><summary>黑白名单机制</summary>

- 如在白名单直接放行。
- 如在黑名单则禁止请求。
- 可动态控制黑白名单是否开启、黑白名单QQ号。

</details>

<details>
<summary>临时用户机制</summary>

- 临时用户：即不在白名单也不在黑名单的用户。
- 对该类用户分配最大请求配额（可在范围内随机分配），在配额内的请求可以正常发送。
- 超出配额的请求根据配置自动回复超额提示信息。
- 根据配置自动重置配额。
- 可动态控制是否开启临时用户机制。

</details>


</details>

<details>
<summary>

## :crossed_swords:安装与配置

</summary>
<details>
<summary>安装</summary>

- 运行`!plugin get https://github.com/zuo-shi-yun/Gatekeeper.git`
- 进入插件目录执行`pip install -r requirements.txt`

</details>
<details>
<summary>配置</summary>

- 如果你不熟悉yaml格式文件，请使用指令修改配置，所有配置**均可**通过指令动态修改。
- 系统相关配置存于config.py文件中。
- 可于config-temporary.yml文件中查看每一项配置的详细说明。**在该文件修改配置无效！！**
- 可对插件运行逻辑、黑白名单机制、临时用户机制进行配置。

</details>

</details>

<details>
<summary>

## :calling:交互指令

</summary>

### 说明

- 下面的所有指令(cmd)均有两种形式，“**!cmd**”以及“**cmd**”。  
  其中“**cmd**”形式的指令只有当config文件中normal_cmd字段为True时有效（默认为True）。  
  下文中“**!**”省略不写，若使用“!cmd”形式时别忘了加。
- 所有命令**仅对**管理员生效。
- 可以向机器人发送"**看门狗**"快速查看指令说明

<details>
<summary>

### 白名单

</summary>

1. **打开白名单**："打开白名单"。
2. **添加qq号到白名单**："添加白名单 qq号1 qq号2"。  
   tips：不限制添加的qq号数量，以空格分隔。
3. **删除白名单qq号**："删除白名单 qq号"
4. **关闭白名单**："关闭白名单"。
5. **查询白名单中所有的qq号**："查询白名单"

</details>

<details>
<summary>

### 黑名单

</summary>

1. **打开黑名单**："打开黑名单"。
2. **添加qq号到黑名单**："添加黑名单 qq号1 qq号2"。  
   tips：不限制添加的qq号数量，以空格分隔。
3. **删除黑名单qq号**："删除黑名单 qq号"
4. **关闭黑名单**："关闭黑名单"。
5. **查询黑名单中的所有qq号**："查询黑名单"

</details>

<details>
<summary>

### 临时用户

</summary>

1. **打开临时用户机制**："打开临时用户"。
2. **设置临时用户最高配额**："设置最高 请求数"  
   eg：设置临时用户最高请求数为10：设置最高 10  
   tips：当随机配额关闭时，每个用户的最高配额均为该参数。
3. **设置配额刷新天数**："设置天数 天数"  
   eg：设置配额刷新间隔为1天：设置天数 1
4. **设置超额提示信息**："设置信息 提示信息"  
   tips：提示信息中以“{}”代表配额刷新天数，空格代表换行。
5. **打开随机配额机制**："打开随机配额"  
   tips：开启后将随机从[最低配额, 最高配额]范围内给用户随机分配配额
6. **设置临时用户最低配额**："设置最低 请求数"。
7. **关闭临时用户机制**："关闭临时用户"
8. **关闭随机配额机制**："关闭随机配额"

</details>

<details>
<summary>

### 运行逻辑

</summary>

1. **打开"cmd"形式的指令**："打开普通指令"。
2. **关闭"cmd"形式的指令**："关闭普通指令"。
3. **打开阻止其余插件行为**："打开插件阻止"  
   tips：可以通过更改plugins/settings.json中order字段中每个插件名称的前后顺序，以达到精准控制屏蔽某些插件的目的。
4. **关闭阻止其余插件行为**："关闭插件阻止"
5. **查询系统所有配置项**："查询配置"

</details>

</details>