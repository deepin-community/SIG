# SIG 创建指南

## SIG 的创建

SIG 的创建请求通过向 GitHub 中 [deepin-community 组织下的 SIG 仓库中](https://github.com/deepin-community/SIG/)发起 GitHub Pull Request 的形式，在此目录下根据指定格式创建 SIG 对应文件夹并放置对应文件的形式发起。SIG 委员会将通过对相应 Pull Request 的 Review 过程对申请进行评审。当 Pull Request 最终被合入时，SIG 即创建完成。

### SIG 创建要求

在创建之前，请确认小组满足如下要求：

- 小组兴趣和活动内容与 deepin 和/或 DDE 具备相关性
- 小组能够保持活动公开\*
- 小组活动能有对整个 deepin 社区公开的活动产出\*\*
- 小组必须存在至少两名成员（建议有至少五名成员时再进行创建）

\* 活动开展平台可以为任意平台。对于公开的即时聊天平台，我们推荐小组使用 Matrix（[参考资料](https://wiki.mozilla.org/Matrix)）。具有对应 Matrix 房间后，可在 https://matrix.to/#/#deepin-community:matrix.org 联系我们协助将房间加入到 deepin Space 中，便于社区贡献者查找并参与讨论。

\*\* 小组应当每个季度至少有一篇进度汇报或成果展示性质的博客来展示相关成果。为了方便小组进行成果展示，我们也会在小组建立时建立一个 `sig-` 前缀的仓库用于提供静态博客服务。如小组本身已有相关平台进行展示，请单独进行说明。

### 信息准备

在创建 SIG 时，你需要准备下列信息：

- SIG 组名（推荐同时提供中英文名称）
- 小组 ID（仅包含小写字母与连字符）
- 创建原因
- 小组简介
- 活动范围与目标
- 公开讨论渠道
- 小组组员信息和小组管理员的 GitHub 账号信息

当您准备就绪后，即可进行后续步骤。

### 创建步骤

您需要 Fork 此仓库，复制此目录下的 `.template.zh_CN` 文件夹内的文件到一个新的目录，以小组 ID 作为新目录的名字，并编辑此目录下的文件以使其符合您要创建的小组的实际情况，最终推送修改并发起 Pull Request。

在编辑模板信息时，请注意模板中给出的描述。在 `metadata.yml` 声明的信息会被公开呈现，其中列出的成员将被邀请加入 deepin-community 组织。

在发起 Pull Request 时，请以 `[新 SIG 提案] SIG 名称` 为格式作为 Pull Request 的标题，并按下面段落的格式，在描述区域提供小组的创建原因和管理员 GitHub 账号信息。

``` markdown
## 创建原因

在这里描述创建 SIG 的原因。

## 仓库创建

此 SIG 需在 deepin-community 组织下创建如下仓库：

- sig-小组ID
- ...

（注：若小组不需要对应仓库，可直接删除“仓库创建”一节）
```

若您或其它组员均对 GitHub 的 Pull Request 工作流程不熟悉，您也可以开启 Issue ，提供上述信息，来请求 SIG 委员会协助。

注：尽管这里允许 SIG 在 deepin-community 创建用来放置小组项目的仓库，但小组的活动并不强制要求在此 GitHub 组织下进行，小组可选择任何合适的公开位置进行 SIG 活动的展开，例如使用其它 GitHub 组织，或是使用其它平台，例如 Gitee。

### 后续步骤

Pull Request 发起后，SIG 委员会会在三个工作日内予以反馈。若提出了反馈意见，则申请人或其它小组成员应在 Pull Request 中与委员会进行讨论并达成一致。

当 Pull Request 最终被合入时，SIG 即创建完成。若最终决定不再创建 SIG，则可直接关闭对应的 Pull Request。

## SIG 变更申请流程

当小组需要更新小组的相关信息时，仍通过常规 Pull Request 的形式对已有文件进行编辑，并由 SIG 委员会评审后，通过合入的形式完成编辑。

若您或其它组员均对 GitHub 的 Pull Request 工作流程不熟悉，您也可以开启 Issue ，提供要编辑的信息，来请求 SIG 委员会协助。
