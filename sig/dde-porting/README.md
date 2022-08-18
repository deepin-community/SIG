# dde-porting SIG

## 小组简介

向不同发行版移植深度桌面环境和软件，包括但不限于 Arch, Debain, Gentoo, NixOS, openSUSE。致力于提高 DDE 软件的可移植性。

## 活动范围与目标

目标：让 deepin 以外的发行版也可以使用上 DDE，并跟进版本更新和 BUG 修复。

活动范围：[Matrix](https://matrix.to/#/#dde-port:matrix.org) [Telegram](https://t.me/ddeport) [GitHub discussions](https://github.com/linuxdeepin/developer-center/discussions?discussions_q=label%3A%22bug+%7C+porting%22) [GitHub issue](https://github.com/linuxdeepin/developer-center/issues?q=is%3Aissue+is%3Aopen+label%3A%22bug+%7C+porting%22)

## 如何加入

DDE 移植小组实际上并不“小”，不同发行版对移植有着不同的要求，因此我们分为 Arch, Debain 等若干个子组，进行特定发行版的移植工作。而不同发行版移植工作又有非常多共性的问题，因此各子组间的交流非常重要，故统合为 DDE 移植 SIG。此外，我们还有一个 DDE 子组，不负责特定发行版移植，而是致力于提高 DDE 的可移植性，方便社区开发者与 deepin 官方交流。

### 加入标准：

欢迎所有热爱开源，喜欢 DDE 的同学加入，作为兴趣小组，我们不会做出任何工作量上的要求，也没有任何能力上的考核。
除了开发者，如果你是 DDE 的忠实用户，关注某个发行版的移植进度，也是欢迎加入的。

想要成为 SIG 管理员，需要满足以下**任意一点**：

- 已经完成了一定工作量，比如移植了一部分 DDE 软件，或者向 DDE 提交过 pr。
- 熟悉目标发行版的打包。
- 熟悉 DDE 的编译和构建。

如果想要建立一个新的(发行版)子组，需要已经完成一定工作量或者至少两名成员有意愿参与。

### 加入方法：

- 加入我们的交流群（Matrix/Telegram/IRC 任一）。
- 对于管理员，向 [SIG 仓库](https://github.com/deepin-community/SIG/tree/master/sig/dde-porting) 提交 pr 添加自己的帐号。如果你是一个新发行版的开拓者，需要添加对应子组。如果需要 Matrix/Telegram 管理权限，可联系群主。

## 小组章程

邮件列表发送月报公布工作进度以及当前问题，必要时进行线上会议讨论相关问题，会议议题以及会议时间会参与方式等信息会提前在邮件列表或者群组内进行公布。

ps: 章程目前还不完善，有兴趣的同学可以加入进来讨论。 

## 讨论渠道

### 专用交流渠道
我们提供了 Matrix，Telegram 和 Libera IRC 的讨论群组方便开发者交流，三者通过桥接消息互通。

- [Matrix](https://matrix.to/#/#dde-port:matrix.org)
- [Telegram](https://t.me/ddeport)
- [IRC](https://web.libera.chat/#dde-port)

### 通用交流渠道
以下渠道交流内容属于泛 deepin/DDE，你可能需要使用“DDE”，“移植”等关键字筛选信息。

如果你发现 DDE 应用的 bug，或是有提高可移植性的建议，可以在 GitHub 提出 issue/discussions， 并加上 <bug | porting> 的 Labels。
- [GitHub issue](https://github.com/linuxdeepin/developer-center/issues)
- [GitHub discussions](https://github.com/linuxdeepin/developer-center/discussions)

如果你想要展示一下自己的移植成果或者进度，可以在官方论坛发帖或者通过邮件列表的方式来展示，但如果有问题需要求助，更推荐使用上方提供的 DDE 移植小组的专用交流渠道。
- [官方论坛](https://bbs.deepin.org)
- [官方邮件列表](https://www.freelists.org/archive/deepin-devel)

## 相关链接

- [Arch](https://archlinux.org/packages/?sort=&q=deepin&maintainer=&flagged=)
- [NixOS](https://github.com/linuxdeepin/dde-nixos)
- [Gentoo](https://github.com/deepin-community/deepin-overlay)